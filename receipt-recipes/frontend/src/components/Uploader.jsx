import React, { useState, useRef } from 'react';

// --- Configuration ---
const API_URL = 'http://127.0.0.1:8000/uploads/';
// Custom styles for consistent dark theme
const customStyles = {
    bodyBg: '#0d1117',
    cardBg: '#161b22',
    uploadBtnBg: '#238636',
    uploadBtnHoverBg: '#2ea043',
    textColor: '#c9d1d9'
};

// --- Status Enumeration ---
const UploadStatus = {
    IDLE: 'idle',
    UPLOADING: 'uploading',
    SUCCESS: 'success',
    ERROR: 'error',
};

// Component for displaying the upload status and messages
const StatusArea = ({ status, message }) => {
    if (status === UploadStatus.IDLE) return null;

    const isError = status === UploadStatus.ERROR;

    if (status === UploadStatus.UPLOADING) {
        return (
            <div className="flex items-center justify-center p-3 mt-4 text-sm text-blue-400">
                <div 
                    className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-100 border-r-2 border-l-transparent mr-3" 
                    style={{ borderTopColor: customStyles.textColor, borderLeftColor: customStyles.textColor, borderRightColor: customStyles.uploadBtnBg }}
                ></div>
                <span>Uploading files...</span>
            </div>
        );
    }
    
    // Success or Error message display
    return (
        <div className={`p-3 rounded-xl shadow-inner text-sm ${isError ? 'bg-red-900 text-red-300' : 'bg-green-900 text-green-300'}`}>
            <h3 className="font-bold mb-1">{isError ? '❌ Upload Failed!' : '✅ Upload Successful!'}</h3>
            {message}
        </div>
    );
};


// Main Application Component (now acts as the improved FileUploader container)
const App = () => {
    // Stores an array of File objects
    const [selectedFiles, setSelectedFiles] = useState([]); 
    const [status, setStatus] = useState(UploadStatus.IDLE);
    const [statusMessage, setStatusMessage] = useState(null);
    const fileInputRef = useRef();

    // Clears the status and stores the selected files (multiple files allowed)
    function handleFileChange(e) {
        if (e.target.files && e.target.files.length > 0) {
            // Store array of File objects
            setSelectedFiles(Array.from(e.target.files));
            setStatus(UploadStatus.IDLE);
            setStatusMessage(null);
        } else {
            setSelectedFiles([]);
        }
    }

    // Triggers the hidden file input
    function handleButtonClick() {
        fileInputRef.current.click();
    }
    
    // Main upload logic refactored for multiple files
    const handleFileUpload = async () => {
        if (selectedFiles.length === 0) return;

        setStatus(UploadStatus.UPLOADING);
        setStatusMessage(null);

        try {
            // 1. Prepare FormData
            const formData = new FormData();
            
            // Append each file using the same key 'file'
            selectedFiles.forEach(file => {
                formData.append("file", file, file.name); 
            });

            // 2. Send the POST request
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                // Handle HTTP error codes (4xx, 5xx)
                const errorMessage = data.detail || JSON.stringify(data) || 'Unknown server error.';
                setStatus(UploadStatus.ERROR);
                setStatusMessage(`Server responded with status ${response.status}: ${errorMessage}`);
                return;
            }

            // 3. Handle Success
            setStatus(UploadStatus.SUCCESS);
            
            // Assuming the backend returns the saved results, we display the count
            const resultMessage = Array.isArray(data) 
                ? `${data.length} files processed.` 
                : (data.saved_to ? `1 file processed: ${data.filename}` : `All ${selectedFiles.length} files successfully sent to the server.`);

            setStatusMessage(
                <>
                    <p className="text-xs">{resultMessage}</p>
                    <p className="mt-3 font-semibold">Next Step: Run <code className="bg-gray-800 p-1 rounded-md">/recipes/generate/</code></p>
                </>
            );

        } catch (error) {
            // Handle network errors (e.g., server not running)
            console.error('Network or Fetch Error:', error);
            setStatus(UploadStatus.ERROR);
            setStatusMessage(`Fatal Error: Could not connect to backend server at ${API_URL}. Check if the server is running on port 8001.`);
        }
    };

    const isUploading = status === UploadStatus.UPLOADING;
    const isFileSelected = selectedFiles.length > 0;
    const canUpload = isFileSelected && !isUploading;
    
    // Calculate total size for display
    const totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0);
    const formatFileSize = (bytes) => (bytes / 1024 / 1024).toFixed(2); // Convert to MB
    
    return (
        <div style={{ backgroundColor: customStyles.bodyBg, color: customStyles.textColor }} 
             className="flex items-center justify-center min-h-screen p-4 font-sans">

            <div className="card p-8 rounded-xl w-full max-w-lg" style={{ backgroundColor: customStyles.cardBg }}>
                
                <h1 className="text-3xl font-bold mb-6 text-center text-white">Receipt Uploader</h1>
                <p className="mb-4 text-sm text-center text-gray-400">
                    Uploads multiple receipt images to the FastAPI server for batch inventory analysis.
                </p>

                <div className="space-y-4">
                    
                    {/* Hidden File Input */}
                    <input 
                        type='file' 
                        multiple 
                        ref={fileInputRef} 
                        onChange={handleFileChange} 
                        accept="image/*"
                        style={{ display: "none" }}
                    />
                    
                    {/* File Selection Button */}
                    <button 
                        className='w-full text-white font-semibold py-3 px-4 rounded-lg shadow-md focus:outline-none focus:ring-4 focus:ring-gray-600 focus:ring-opacity-50 transition duration-150 bg-gray-700 hover:bg-gray-600 disabled:opacity-50'
                        onClick={handleButtonClick}
                        disabled={isUploading}
                    >
                        {isFileSelected ? `Selected: ${selectedFiles.length} files` : "Choose Receipt Images"}
                    </button>

                    {/* File Details Section */}
                    {isFileSelected && (
                        <div className="uploads-section rounded-xl bg-gray-800 p-4 shadow-inner text-sm space-y-1">
                            <p className="font-semibold text-white">Batch Details:</p>
                            <p>Files Count: <code className="font-mono text-xs">{selectedFiles.length}</code></p>
                            <p>Total Size: <code className="font-mono text-xs">{formatFileSize(totalSize)} MB</code></p>
                            {/* Optionally list file names */}
                            <details className="mt-2 pt-2 border-t border-gray-700">
                                <summary className="cursor-pointer text-gray-400">View File List</summary>
                                <ul className="list-disc list-inside text-xs mt-1 space-y-0.5 max-h-24 overflow-y-auto">
                                    {selectedFiles.map((file, index) => (
                                        <li key={index}><code className="font-mono">{file.name}</code></li>
                                    ))}
                                </ul>
                            </details>
                        </div>
                    )}

                    {/* Upload Action Button */}
                    <button 
                        onClick={handleFileUpload}
                        disabled={!canUpload}
                        className="w-full text-white font-semibold py-3 px-4 rounded-lg shadow-md focus:outline-none focus:ring-4 focus:ring-green-600 focus:ring-opacity-50 flex items-center justify-center transition duration-150 disabled:opacity-50"
                        style={{ backgroundColor: customStyles.uploadBtnBg }}
                    >
                        {isUploading ? (
                            <span className="flex items-center">Uploading Batch...</span>
                        ) : (
                            'Start Inventory Upload'
                        )}
                    </button>
                    
                    {/* Status Area */}
                    <div className="mt-6">
                        <StatusArea status={status} message={statusMessage} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
