"""Database models and ORM setup (optional SQLAlchemy models for future use)."""
from datetime import datetime


class HistoricalRace:
    """Represents a historical Formula 1 race record."""
    
    def __init__(self, driver, team, q1, q2, q3, start_position, finish_position,
                 track, rain, d_elo, t_elo, year, round, id=None, created_at=None):
        self.id = id
        self.driver = driver
        self.team = team
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.start_position = start_position
        self.finish_position = finish_position
        self.track = track
        self.rain = rain
        self.d_elo = d_elo
        self.t_elo = t_elo
        self.year = year
        self.round = round
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
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
            'created_at': self.created_at
        }
