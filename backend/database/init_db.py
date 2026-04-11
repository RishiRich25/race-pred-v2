"""
Initialize the MySQL database with the F1 predictions schema.
Run this script to set up the database tables.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'f1_predictions')
DB_USER_FULL = os.getenv('DB_USER_FULL', 'full_user')
DB_PASSWORD_FULL = os.getenv('DB_PASSWORD_FULL', '')
DB_USER_HOST = os.getenv('DB_USER_HOST', '%')

def create_database():
    """Create the main database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✓ Database '{DB_NAME}' created/exists")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error creating database: {e}")
        raise

def create_tables():
    """Create tables in the database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Create main predictions table
        create_table_sql = """
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
        
        cursor.execute(create_table_sql)
        print("✓ Table 'race_predictions' created/exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error creating tables: {e}")
        raise

def create_users():
    """Create database users with appropriate privileges."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create full_user if it doesn't exist
        try:
            cursor.execute(f"DROP USER IF EXISTS '{DB_USER_FULL}'@'{DB_USER_HOST}'")
            print(f"✓ Dropped existing user '{DB_USER_FULL}'@'{DB_USER_HOST}'")
        except:
            pass

        if not DB_PASSWORD_FULL:
            raise ValueError("DB_PASSWORD_FULL must be set to create the full user")

        cursor.execute(
            f"CREATE USER '{DB_USER_FULL}'@'{DB_USER_HOST}' IDENTIFIED BY %s",
            (DB_PASSWORD_FULL,)
        )
        print(f"✓ User '{DB_USER_FULL}' created for host '{DB_USER_HOST}'")
        
        # Grant privileges
        cursor.execute(
            f"GRANT SELECT, INSERT, UPDATE ON {DB_NAME}.* TO '{DB_USER_FULL}'@'{DB_USER_HOST}'"
        )
        print(f"✓ Granted SELECT, INSERT, UPDATE privileges to '{DB_USER_FULL}'")
        
        # Grant root all privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'{DB_USER_HOST}'")
        print(f"✓ Granted ALL PRIVILEGES to '{DB_USER}'@'{DB_USER_HOST}'")
        
        cursor.execute("FLUSH PRIVILEGES")
        print("✓ Privileges flushed")
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error creating users: {e}")
        raise

def main():
    """Run all initialization steps."""
    print("=" * 50)
    print("F1 Predictions Database Setup")
    print("=" * 50)
    
    try:
        print("\n1. Creating database...")
        create_database()
        
        print("\n2. Creating tables...")
        create_tables()
        
        print("\n3. Creating users...")
        create_users()
        
        print("\n" + "=" * 50)
        print("✓ Database setup completed successfully!")
        print("=" * 50)
        print(f"\nDatabase: {DB_NAME}")
        print(f"Root user: {DB_USER}")
        print(f"Full user: {DB_USER_FULL}")
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        raise

if __name__ == "__main__":
    main()
