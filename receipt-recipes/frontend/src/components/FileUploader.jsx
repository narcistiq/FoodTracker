import { useRef, useState } from 'react';
import './FileUploader.css';

const UploadStatus = {
    IDLE: 'idle',
    UPLOADING: 'uploading',
    SUCCESS: 'success',
    ERROR: 'error',
};
export default function FileUploader() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState(UploadStatus.IDLE);
    const fileInputRef = useRef();
    function handleFileChange(e) {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    }
    const handleFileUpload = (e) => {
        const formData = new FormData();
        formData.append(
            "file",
            file,
            file.name
        );
        const requestOptions = {
            method: 'POST',
            body: formData
        };
        fetch('http://127.0.0.1:8000/uploads/', requestOptions)
        .then(response => response.json())
        .then(function(response) {
            console.log(response)
        })
    }
    function handleButtonClick() {
        fileInputRef.current.click();
    }
    return (
        <div className="flex flex-col items-start min-h-screen p-6 space-y-1">
            <input type='file' ref={fileInputRef} onChange={handleFileChange} style={{ display: "none" }}/>
            {file && (
                <div className="uploads-section rounded-lg bg-white p-6 shadow-md w-full sm:w-96">
                    <p>File name: {file.name}</p>
                    <p>Size: {(file.size/1024).toFixed(2)} KB</p>
                    <p>Type: {file.type}</p>
                </div>
            )}
            <button className='upload-btn' onClick={handleButtonClick}>
                {file ? `Selected: ${file.name}` : "Choose File"}
            </button>
            {file && status !== 'uploading' && <button onClick={handleFileUpload}>Upload</button>}
            {status == 'success' && (
                <p style={{ color: '#16a34a' }} className="text-sm">File uploaded successfully!</p>
            )}
            {status == 'error' && (
                <p style={{ color: '#ff2929ff' }} className="text-sm">Upload Failed. Please try again.</p>
            )}
        </div>
    );
}