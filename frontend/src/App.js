import React, { useState, useEffect } from 'react';
import './App.css';
import Card from './components/Card';
import Button from './components/Button';
import { fetchNextRacePrediction } from './services/api';

function App() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [eventName, setEventName] = useState('');

  useEffect(() => {
    const loadPredictions = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchNextRacePrediction();
        setPredictions(data);
        if (data.length > 0) {
          // Event name should be consistent across all predictions
          setEventName(data[0].Driver ? 'Next F1 Race Predictions' : '');
        }
      } catch (err) {
        setError(err.message || 'Failed to load predictions. Make sure the backend API is running on localhost:8000');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadPredictions();
  }, []);

  return (
    <div className="container-app">
      {/* HERO SECTION */}
      <section className="section bg-grid" style={{ position: 'relative' }}>
        <div className="section-inner">
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <h1 style={{ marginBottom: '1rem' }}>
              F1 Race <span className="gradient-text">Predictor</span>
            </h1>
            <p style={{ fontSize: '1.125rem', color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>
              AI-powered predictions for the next Formula 1 race. Powered by XGBoost and Live Elo ratings.
            </p>
          </div>
        </div>
      </section>

      {/* PREDICTIONS SECTION */}
      <section className="section">
        <div className="section-inner">
          <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Next Race Predictions</h2>

          {/* Loading State */}
          {loading && (
            <div style={{ textAlign: 'center', padding: '3rem 0' }}>
              <div style={{ 
                display: 'inline-block', 
                width: '40px', 
                height: '40px', 
                border: '3px solid rgba(247, 147, 26, 0.3)',
                borderTop: '3px solid var(--accent-primary)',
                borderRadius: '50%',
                animation: 'spin-slow 1s linear infinite'
              }} />
              <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading predictions...</p>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <Card style={{ border: '1px solid rgba(234, 88, 12, 0.5)', backgroundColor: 'rgba(234, 88, 12, 0.05)' }}>
              <h3 style={{ color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>Connection Error</h3>
              <p style={{ color: 'var(--text-muted)', margin: 0 }}>{error}</p>
              <Button 
                variant="primary" 
                onClick={() => window.location.reload()}
                style={{ marginTop: '1rem' }}
              >
                Retry
              </Button>
            </Card>
          )}

          {/* Data State */}
          {!loading && !error && predictions.length > 0 && (
            <>
              {/* Summary Card */}
              <Card className="card-glass" style={{ marginBottom: '2rem', textAlign: 'center' }}>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  TOTAL DRIVERS
                </div>
                <div style={{ fontSize: '2.5rem', color: 'var(--accent-primary)', fontWeight: 'bold' }}>
                  {predictions.length}
                </div>
              </Card>

              {/* Results Table */}
              <div style={{ overflowX: 'auto' }}>
                <table style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  fontSize: '0.875rem'
                }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid rgba(247, 147, 26, 0.3)' }}>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontFamily: 'var(--ff-mono)', fontWeight: 500 }}>Position</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontFamily: 'var(--ff-mono)', fontWeight: 500 }}>Driver</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontFamily: 'var(--ff-mono)', fontWeight: 500 }}>Team</th>
                      <th style={{ padding: '1rem', textAlign: 'center', color: 'var(--accent-primary)', fontFamily: 'var(--ff-mono)', fontWeight: 500 }}>Grid</th>
                      <th style={{ padding: '1rem', textAlign: 'right', color: 'var(--accent-primary)', fontFamily: 'var(--ff-mono)', fontWeight: 500 }}>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {predictions.map((pred, idx) => (
                      <tr 
                        key={idx} 
                        style={{ 
                          borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                          transition: 'background-color 200ms ease'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.backgroundColor = 'rgba(247, 147, 26, 0.05)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.backgroundColor = 'transparent';
                        }}
                      >
                        <td style={{ padding: '1rem', color: 'var(--accent-tertiary)', fontWeight: 'bold', fontFamily: 'var(--ff-mono)' }}>
                          #{pred['Predicted_Position']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-primary)', fontWeight: 500 }}>
                          {pred['Driver']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>
                          {pred['Team']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-muted)', fontFamily: 'var(--ff-mono)' }}>
                          {pred['Starting Position']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'right' }}>
                          <span style={{
                            background: 'linear-gradient(to right, var(--accent-secondary), var(--accent-primary))',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
                            fontFamily: 'var(--ff-mono)',
                            fontWeight: 'bold'
                          }}>
                            {pred['Predicted_Score'].toFixed(4)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Info Card */}
              <Card style={{ marginTop: '2rem', backgroundColor: 'rgba(255, 214, 0, 0.05)', border: '1px solid rgba(255, 214, 0, 0.3)' }}>
                <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  <strong style={{ color: 'var(--accent-tertiary)' }}>💡 Info:</strong> Predictions are based on XGBoost model trained on historical F1 data, current driver/team Elo ratings, and qualifying session times.
                </p>
              </Card>
            </>
          )}

          {/* Empty State */}
          {!loading && !error && predictions.length === 0 && (
            <Card style={{ textAlign: 'center', padding: '3rem' }}>
              <p style={{ color: 'var(--text-muted)' }}>No predictions available yet. Try again later.</p>
            </Card>
          )}
        </div>
      </section>

      {/* FOOTER */}
      <footer style={{
        padding: '2rem',
        textAlign: 'center',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        color: 'var(--text-muted)',
        fontSize: '0.875rem'
      }}>
        <p>F1 Race Predictor • Powered by FastAPI + XGBoost + React</p>
      </footer>
    </div>
  );
}

export default App;

