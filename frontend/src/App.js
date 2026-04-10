import React, { useState, useEffect } from 'react';
import './App.css';
import Card from './components/Card';
import Button from './components/Button';
import { fetchNextRacePrediction, fetchRacePrediction } from './services/api';

function App() {
  // Next race state
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Historical predictions state
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear() - 1);
  const [selectedRound, setSelectedRound] = useState(1);
  const [historicalPredictions, setHistoricalPredictions] = useState([]);
  const [historicalLoading, setHistoricalLoading] = useState(false);
  const [historicalError, setHistoricalError] = useState(null);

  // Load next race predictions on mount
  useEffect(() => {
    const loadPredictions = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchNextRacePrediction();
        setPredictions(data);
      } catch (err) {
        setError(err.message || 'Failed to load predictions. Make sure the backend API is running on localhost:8000');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadPredictions();
  }, []);

  // Fetch historical predictions
  const handleHistoricalPrediction = async () => {
    try {
      setHistoricalLoading(true);
      setHistoricalError(null);
      setHistoricalPredictions([]);
      const data = await fetchRacePrediction(selectedYear, selectedRound);
      setHistoricalPredictions(data);
    } catch (err) {
      setHistoricalError(err.message || `Failed to load predictions for ${selectedYear} Round ${selectedRound}`);
      console.error(err);
    } finally {
      setHistoricalLoading(false);
    }
  };

  // Generate year options
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 2017 }, (_, i) => 2018 + i);

  const teamLogos = [
    {
      name: 'Red Bull Racing',
      logoUrl: '/logos/2026redbullracinglogowhite.avif'
    },
    {
      name: 'Ferrari',
      logoUrl: '/logos/2026ferrarilogowhite.avif'
    },
    {
      name: 'Mercedes',
      logoUrl: '/logos/2026mercedeslogowhite.avif'
    },
    {
      name: 'McLaren',
      logoUrl: '/logos/2026mclarenlogowhite.avif'
    },
    {
      name: 'Aston Martin',
      logoUrl: '/logos/2026astonmartinlogowhite.avif'
    },
    {
      name: 'Alpine',
      logoUrl: '/logos/2026alpinelogowhite.avif'
    },
    {
      name: 'Williams',
      logoUrl: '/logos/2026williamslogowhite.avif'
    },
    {
      name: 'Racing Bulls',
      logoUrl: '/logos/2026racingbullslogowhite.avif'
    },
    {
      name: 'Cadillac',
      logoUrl: '/logos/2026cadillaclogowhite.avif'
    },
    {
      name: 'Haas',
      logoUrl: '/logos/2026haasf1teamlogowhite.avif'
    },
    {
      name: 'Audi',
      logoUrl: '/logos/2026audilogowhite.avif'
    }
  ];

  const logoMarqueeItems = [...teamLogos, ...teamLogos];

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
              AI-powered predictions for Formula 1 races. Powered by XGBoost and Live Elo ratings.
            </p>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="section-inner">
          <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Teams</h2>
          <div className="logo-marquee" role="presentation">
            <div className="logo-marquee__track" aria-label="Formula 1 teams">
              {logoMarqueeItems.map((team, index) => (
                <div className="logo-marquee__item" key={`${team.name}-${index}`}>
                  <div className="logo-marquee__image-wrap">
                    <img
                      src={team.logoUrl}
                      alt={`${team.name} logo`}
                      className="logo-marquee__img"
                      loading="lazy"
                      onError={(event) => {
                        event.currentTarget.style.opacity = '0.3';
                      }}
                    />
                  </div>
                  <span className="logo-marquee__label">{team.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* LIVE PREDICTIONS SECTION */}
      <section className="section">
        <div className="section-inner">
          <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Next Race Predictions</h2>

          {loading && (
            <div style={{ textAlign: 'center', padding: '3rem 0' }}>
              <div style={{
                display: 'inline-block',
                width: '40px',
                height: '40px',
                border: '3px solid rgba(32, 68, 146, 0.3)',
                borderTop: '3px solid var(--accent-primary)',
                borderRadius: '50%',
                animation: 'spin-slow 1s linear infinite'
              }} />
              <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading predictions...</p>
            </div>
          )}

          {error && !loading && (
            <Card style={{ border: '1px solid rgba(32, 68, 146, 0.5)', backgroundColor: 'rgba(32, 68, 146, 0.05)' }}>
              <h3 style={{ color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>Connection Error</h3>
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

          {!loading && !error && predictions.length > 0 && (
            <>
              <Card className="card-glass" style={{ marginBottom: '2rem', textAlign: 'center' }}>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  TOTAL DRIVERS
                </div>
                <div style={{ fontSize: '2.5rem', color: 'var(--accent-primary)', fontWeight: 'bold' }}>
                  {predictions.length}
                </div>
              </Card>

              {predictions[0]?.Race_Status === "Next Race" ? null : (
                <Card style={{ marginBottom: '2rem', backgroundColor: 'rgba(255, 165, 0, 0.1)', border: '1px solid rgba(255, 165, 0, 0.5)' }}>
                  <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                    <strong style={{ color: '#FFA500' }}>⚠️ Note:</strong> {predictions[0]?.Race_Status || 'Upcoming race data not yet available'}
                  </p>
                </Card>
              )}

              <div style={{ overflowX: 'auto' }}>
                <table className="prediction-table" style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  fontSize: '0.875rem'
                }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid rgba(32, 68, 146, 0.3)' }}>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Position</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Driver</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Team</th>
                      <th style={{ padding: '1rem', textAlign: 'center', color: 'var(--accent-primary)', fontWeight: 500 }}>Grid</th>
                      <th style={{ padding: '1rem', textAlign: 'right', color: 'var(--accent-primary)', fontWeight: 500 }}>Score</th>
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
                          e.currentTarget.style.backgroundColor = 'rgba(32, 68, 146, 0.05)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.backgroundColor = 'transparent';
                        }}
                      >
                        <td style={{ padding: '1rem', color: 'var(--accent-tertiary)', fontWeight: 'bold' }}>
                          #{pred['Predicted_Position']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-primary)', fontWeight: 500 }}>
                          {pred['Driver']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>
                          {pred['Team']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                          {pred['Starting Position']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'right' }}>
                          <span style={{
                            background: 'linear-gradient(to right, var(--accent-secondary), var(--accent-primary))',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
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

              <Card style={{ marginTop: '2rem', backgroundColor: 'rgba(74, 127, 219, 0.05)', border: '1px solid rgba(74, 127, 219, 0.3)' }}>
                <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  <strong style={{ color: 'var(--accent-primary)' }}>💡 Info:</strong> Predictions are based on XGBoost model trained on historical F1 data, current driver/team Elo ratings, and qualifying session times.
                </p>
              </Card>
            </>
          )}

          {!loading && !error && predictions.length === 0 && (
            <Card style={{ textAlign: 'center', padding: '3rem' }}>
              <p style={{ color: 'var(--text-muted)' }}>No predictions available yet. Try again later.</p>
            </Card>
          )}
        </div>
      </section>

      {/* HISTORICAL PREDICTIONS SECTION */}
      <section className="section">
        <div className="section-inner">
          <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Historical Race Predictions</h2>

          <Card style={{ marginBottom: '2rem' }}>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="year-select">Year</label>
                <select
                  id="year-select"
                  className="select"
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                >
                  {years.map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="round-input">Round Number</label>
                <input
                  id="round-input"
                  className="input"
                  type="number"
                  min="1"
                  max="24"
                  value={selectedRound}
                  onChange={(e) => setSelectedRound(parseInt(e.target.value))}
                  placeholder="e.g., 1, 2, 3..."
                />
              </div>
            </div>

            <Button
              variant="primary"
              onClick={handleHistoricalPrediction}
              disabled={historicalLoading}
              style={{ width: '100%' }}
            >
              {historicalLoading ? 'Loading...' : 'Get Predictions'}
            </Button>
          </Card>

          {/* Historical Loading */}
          {historicalLoading && (
            <div style={{ textAlign: 'center', padding: '3rem 0' }}>
              <div style={{
                display: 'inline-block',
                width: '40px',
                height: '40px',
                border: '3px solid rgba(32, 68, 146, 0.3)',
                borderTop: '3px solid var(--accent-primary)',
                borderRadius: '50%',
                animation: 'spin-slow 1s linear infinite'
              }} />
              <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading predictions...</p>
            </div>
          )}

          {/* Historical Error */}
          {historicalError && !historicalLoading && (
            <Card style={{ border: '1px solid rgba(255, 24, 1, 0.5)', backgroundColor: 'rgba(255, 24, 1, 0.05)' }}>
              <h3 style={{ color: '#FF1801', marginBottom: '0.5rem' }}>Data Not Available</h3>
              <p style={{ color: 'var(--text-muted)', margin: 0 }}>{historicalError}</p>
              <p style={{ color: 'var(--text-muted)', margin: '1rem 0 0 0', fontSize: '0.875rem' }}>
                Please try a different year or round number. Qualifying data may not be available for all historical races.
              </p>
            </Card>
          )}

          {/* Historical Results */}
          {!historicalLoading && !historicalError && historicalPredictions.length > 0 && (
            <>
              <Card className="card-glass" style={{ marginBottom: '2rem', textAlign: 'center' }}>
                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  {selectedYear} • ROUND {selectedRound}
                </div>
                <div style={{ fontSize: '2.5rem', color: 'var(--accent-primary)', fontWeight: 'bold' }}>
                  {historicalPredictions.length} Drivers
                </div>
              </Card>

              <div style={{ overflowX: 'auto' }}>
                <table className="prediction-table" style={{
                  width: '100%',
                  borderCollapse: 'collapse',
                  fontSize: '0.875rem'
                }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid rgba(32, 68, 146, 0.3)' }}>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Position</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Driver</th>
                      <th style={{ padding: '1rem', textAlign: 'left', color: 'var(--accent-primary)', fontWeight: 500 }}>Team</th>
                      <th style={{ padding: '1rem', textAlign: 'center', color: 'var(--accent-primary)', fontWeight: 500 }}>Grid</th>
                      <th style={{ padding: '1rem', textAlign: 'right', color: 'var(--accent-primary)', fontWeight: 500 }}>Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historicalPredictions.map((pred, idx) => (
                      <tr
                        key={idx}
                        style={{
                          borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                          transition: 'background-color 200ms ease'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.backgroundColor = 'rgba(32, 68, 146, 0.05)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.backgroundColor = 'transparent';
                        }}
                      >
                        <td style={{ padding: '1rem', color: 'var(--accent-tertiary)', fontWeight: 'bold' }}>
                          #{pred['Predicted_Position']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-primary)', fontWeight: 500 }}>
                          {pred['Driver']}
                        </td>
                        <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>
                          {pred['Team']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                          {pred['Starting Position']}
                        </td>
                        <td style={{ padding: '1rem', textAlign: 'right' }}>
                          <span style={{
                            background: 'linear-gradient(to right, var(--accent-secondary), var(--accent-primary))',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
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

              <Card style={{ marginTop: '2rem', backgroundColor: 'rgba(74, 127, 219, 0.05)', border: '1px solid rgba(74, 127, 219, 0.3)' }}>
                <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                  <strong style={{ color: 'var(--accent-primary)' }}>📊 Historical Data:</strong> These predictions show what the model would have predicted based on qualifying data from {selectedYear} Round {selectedRound}.
                </p>
              </Card>
            </>
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

