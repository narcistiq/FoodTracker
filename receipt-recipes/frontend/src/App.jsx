import { useState } from 'react'
import Uploader from './components/Uploader'
import FileUploader from './components/FileUploader'
import './App.css'

function App() {
  const [files, setFile] = useState([])
  const FilesDropped = (dropped) => { setFile(dropped) };

  return (
    <div>
      <h1>Receipt Recipes</h1>
      <div className='upload-btn'>
        <FileUploader />
      </div>
    
      {/* <h1>Food Track</h1>
      
      <Uploader onDrop={FilesDropped} />

      {files.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h2>Files Ready for Upload:</h2>
          <ul>
            {files.map(file => (
              // The 'name' property is a standard part of the File object
              <li key={file.path || file.name}>
                {file.name} - {file.size} bytes
              </li>
            ))}
          </ul>
          <button onClick={() => console.log('Uploading files...', files)}>
            Final Upload
          </button>
        </div>
      )} */}
    </div>
  )
}

export default App
