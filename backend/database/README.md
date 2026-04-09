# Database Setup

This directory contains the PostgreSQL database configuration and initialization scripts for the Race Prediction ML model.

## Prerequisites

- PostgreSQL 12 or higher installed and running
- Python 3.8+
- `psycopg2` Python package

## Installation

1. Install PostgreSQL if not already installed:
   - **Windows**: Download from https://www.postgresql.org/download/windows/
   - **Mac**: `brew install postgresql`
   - **Linux**: `sudo apt-get install postgresql`

2. Install the required Python package:
   ```bash
   pip install psycopg2-binary
   ```

## Database Configuration

Configure the database connection using environment variables:

```bash
# .env file or system environment variables
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=race_pred
```

If not specified, defaults are:
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `postgres`
- Database: `race_pred`

## Initializing the Database

1. Ensure PostgreSQL is running
2. Create the database:
   ```bash
   psql -U postgres -c "CREATE DATABASE race_pred;"
   ```

3. Run the schema initialization:
   ```bash
   python schema.py
   ```

## Table Structure

### historical_races

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| driver | VARCHAR(100) | Driver name |
| team | VARCHAR(100) | Team name |
| q1 | FLOAT | Q1 qualifying time |
| q2 | FLOAT | Q2 qualifying time |
| q3 | FLOAT | Q3 qualifying time |
| start_position | INT | Starting position in race |
| finish_position | INT | Finishing position in race |
| track | VARCHAR(100) | Race track name |
| rain | BOOLEAN | Whether it rained during the race |
| d_elo | FLOAT | Driver ELO rating |
| t_elo | FLOAT | Team ELO rating |
| year | INT | Race year |
| round | INT | Race round number |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Record update timestamp |

## Usage

### Connecting to the Database

```python
from connection import get_db_cursor

with get_db_cursor(commit=True) as cursor:
    cursor.execute("SELECT * FROM historical_races WHERE year = %s", (2025,))
    results = cursor.fetchall()
```

### Inserting Data

```python
from connection import get_db_cursor

with get_db_cursor(commit=True) as cursor:
    cursor.execute("""
        INSERT INTO historical_races 
        (driver, team, q1, q2, q3, start_position, finish_position, 
         track, rain, d_elo, t_elo, year, round)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (driver, team, q1, q2, q3, start, finish, track, rain, d_elo, t_elo, year, round_num))
```

## File Reference

- **config.py** - Database configuration and connection strings
- **connection.py** - Connection management and context managers
- **schema.py** - Table creation and database initialization
- **README.md** - This file

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL service is running
- Check host, port, and credentials in config.py

### Database Does Not Exist
- Run: `psql -U postgres -c "CREATE DATABASE race_pred;"`

### Permission Denied
- Ensure the PostgreSQL user has proper permissions
- Run: `ALTER USER postgres WITH SUPERUSER;` if needed
