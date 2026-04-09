"""
Database models/schemas for F1 predictions.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RacePrediction:
    """Data class for race prediction records."""
    driver: str
    team: str
    track: str
    year: int
    round: int
    q1: Optional[float] = None
    q2: Optional[float] = None
    q3: Optional[float] = None
    start_position: Optional[int] = None
    finish_position: Optional[int] = None
    rain: bool = False
    d_elo: Optional[float] = None
    t_elo: Optional[float] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'driver': self.driver,
            'team': self.team,
            'q1': self.q1,
            'q2': self.q2,
            'q3': self.q3,
            'start_position': self.start_position,
            'finish_position': self.finish_position,
            'track': self.track,
            'rain': self.rain,
            'd_elo': self.d_elo,
            't_elo': self.t_elo,
            'year': self.year,
            'round': self.round,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

# SQL table schema
RACE_PREDICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS race_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver VARCHAR(100) NOT NULL,
    team VARCHAR(100) NOT NULL,
    q1 FLOAT,
    q2 FLOAT,
    q3 FLOAT,
    start_position INT,
    finish_position INT,
    track VARCHAR(100) NOT NULL,
    rain BOOLEAN DEFAULT FALSE,
    d_elo FLOAT,
    t_elo FLOAT,
    year INT NOT NULL,
    round INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_race (driver, year, round),
    INDEX idx_year_round (year, round),
    INDEX idx_driver (driver),
    INDEX idx_team (team),
    INDEX idx_track (track)
)
"""
