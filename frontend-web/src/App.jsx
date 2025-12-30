import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import AnalysisResult from './components/AnalysisResult';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelected = (selectedFile, previewData) => {
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const analyzeImage = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Assuming backend is running on localhost:8000
      const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to the analysis engine. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
        <h1>AI Reality Check</h1>
        <p className="subtitle">Advanced Deepfake & AI Image Detection Engine</p>
      </div>

      <ImageUpload onImageSelected={handleImageSelected} />

      {file && !loading && !result && (
        <button className="btn-primary" onClick={analyzeImage}>
          Analyze Authenticity
        </button>
      )}

      {loading && (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <div className="loader"></div>
          <p>Scanning pixel artifacts...</p>
        </div>
      )}

      {error && (
        <div style={{ color: '#ef4444', marginTop: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>
          {error}
        </div>
      )}

      {result && (
        <AnalysisResult
          result={result}
          heatmap={result.heatmap}
          artifacts={result.artifacts}
        />
      )}
    </div>
  );
}

export default App;
