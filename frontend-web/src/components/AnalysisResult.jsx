import React from 'react';

const AnalysisResult = ({ result, heatmap, artifacts }) => {
    if (!result) return null;

    const isReal = result.result === "Real";
    const confidence = result.confidence;

    return (
        <div className="results-container">
            {/* Result Card */}
            <div className="card">
                <h3>Detection Result</h3>
                <div style={{ marginTop: '1rem' }}>
                    <div className={`score-badge ${isReal ? 'real' : 'ai'}`}>
                        {result.result.toUpperCase()}
                    </div>
                    <p style={{ fontSize: '0.9rem' }}>Confidence: <strong>{confidence}%</strong></p>

                    <div style={{ marginTop: '1.5rem', textAlign: 'left' }}>
                        <h4>Detected Anomalies</h4>
                        {artifacts && artifacts.length > 0 ? (
                            <ul className="artifacts-list">
                                {artifacts.map((item, index) => (
                                    <li key={index}>⚠️ {item}</li>
                                ))}
                            </ul>
                        ) : (
                            <p style={{ color: '#71717a', fontStyle: 'italic', marginTop: '0.5rem' }}>
                                No obvious artifacts detected by rule-based engine.
                            </p>
                        )}
                    </div>
                </div>
            </div>

            {/* Heatmap Card */}
            {heatmap && (
                <div className="card">
                    <h3>Analysis Heatmap</h3>
                    <p style={{ fontSize: '0.8rem', color: '#a1a1aa', marginBottom: '1rem' }}>
                        Highlights regions with high variance/noise often found in deepfakes.
                    </p>
                    <div className="image-preview">
                        <img src={`data:image/jpeg;base64,${heatmap}`} alt="Analysis Heatmap" />
                    </div>
                </div>
            )}
        </div>
    );
};

export default AnalysisResult;
