"""Database schema initialization and management."""
import psycopg2
from connection import get_connection, get_db_cursor


def create_tables():
    """Create the historical_races table."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS historical_races (
        id SERIAL PRIMARY KEY,
        driver VARCHAR(100) NOT NULL,
        team VARCHAR(100) NOT NULL,
        q1 FLOAT,
        q2 FLOAT,
        q3 FLOAT,
        start_position INT,
        finish_position INT,
        track VARCHAR(100) NOT NULL,
        rain BOOLEAN NOT NULL DEFAULT FALSE,
        d_elo FLOAT,
        t_elo FLOAT,
        year INT NOT NULL,
        round INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(driver, team, year, round, track)
    );
    """
    
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(create_table_sql)
            print("✓ Table 'historical_races' created successfully")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise


def create_indexes():
    """Create indexes for better query performance."""
    indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_historical_races_year ON historical_races(year);",
        "CREATE INDEX IF NOT EXISTS idx_historical_races_driver ON historical_races(driver);",
        "CREATE INDEX IF NOT EXISTS idx_historical_races_team ON historical_races(team);",
        "CREATE INDEX IF NOT EXISTS idx_historical_races_track ON historical_races(track);",
        "CREATE INDEX IF NOT EXISTS idx_historical_races_year_round ON historical_races(year, round);",
    ]
    
    try:
        with get_db_cursor(commit=True) as cursor:
            for sql in indexes_sql:
                cursor.execute(sql)
            print("✓ Indexes created successfully")
    except psycopg2.Error as e:
        print(f"Error creating indexes: {e}")
        raise


def drop_tables():
    """Drop the historical_races table (use with caution)."""
    drop_sql = "DROP TABLE IF EXISTS historical_races CASCADE;"
    
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(drop_sql)
            print("✓ Table 'historical_races' dropped successfully")
    except psycopg2.Error as e:
        print(f"Error dropping table: {e}")
        raise


def init_db():
    """Initialize the database with tables and indexes."""
    print("Initializing database...")
    create_tables()
    create_indexes()
    print("✓ Database initialization complete")


if __name__ == "__main__":
    init_db()
