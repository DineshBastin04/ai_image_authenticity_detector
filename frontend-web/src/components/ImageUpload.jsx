import React, { useState, useRef } from 'react';

const ImageUpload = ({ onImageSelected }) => {
    const [dragActive, setDragActive] = useState(false);
    const [preview, setPreview] = useState(null);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files[0]);
        }
    };

    const handleFiles = (file) => {
        // Create preview
        const reader = new FileReader();
        reader.onloadend = () => {
            setPreview(reader.result);
            onImageSelected(file, reader.result);
        };
        reader.readAsDataURL(file);
    };

    const onButtonClick = () => {
        inputRef.current.click();
    };

    return (
        <div className="upload-container">
            <div
                className={`upload-area ${dragActive ? "dragging" : ""}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={onButtonClick}
            >
                <input
                    ref={inputRef}
                    type="file"
                    className="file-input"
                    onChange={handleChange}
                    accept="image/*"
                />

                {preview ? (
                    <img src={preview} alt="Preview" style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain' }} />
                ) : (
                    <div className="placeholder">
                        <div className="upload-icon">☁️</div>
                        <p>Drag & Drop your image here or <strong>Click to Upload</strong></p>
                        <p style={{ fontSize: '0.8rem', color: '#71717a', marginTop: '0.5rem' }}>Supports JPG, PNG</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ImageUpload;
