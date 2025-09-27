import React, { useCallback, useMemo } from 'react'
import { useDropzone } from 'react-dropzone'

const baseStyle = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 2,
  borderColor: '#eeeeee',
  borderStyle: 'dashed',
  backgroundColor: '#fafafa',
  color: '#bdbdbd',
  outline: 'none',
  transition: 'border .24s ease-in-out',
  cursor: 'pointer', // Important for click-to-select functionality
};

function FileUploader({ onFilesDropped }) {
  const onDrop = useCallback(acceptedFiles => {
    // acceptedFiles is an array of File objects from the user's computer
    console.log('Dropped files:', acceptedFiles);
    
    // Pass the files up to the parent component for processing (e.g., uploading)
    onFilesDropped(acceptedFiles);
    
  }, [onFilesDropped]); // Dependency array includes the prop function

  // 2. Use the useDropzone hook
  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject
  } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [] }, // only access jpeg and png images
  })

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? { borderColor: '#2196f3' } : {}),
    ...(isDragAccept ? { borderColor: '#00e676' } : {}),
    ...(isDragReject ? { borderColor: '#ff1744' } : {})
  }), [isDragActive, isDragAccept, isDragReject]);

  return (
    // 3. Apply the root props to the drop zone container
    <div {...getRootProps({ style })}>
      {/* 4. Apply the input props to the hidden file input */}
      <input {...getInputProps()} />
      
      {/* 5. Display dynamic content based on the drag state */}
      {isDragActive ? (
        <p>Drop the files here ...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
      
      <button style={{ marginTop: '10px' }}>Select Files</button>
    </div>
  );
}

export default FileUploader;