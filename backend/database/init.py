"""Initialize PostgreSQL database from scratch."""
import psycopg2
from psycopg2 import sql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [DB_NAME]
        )
        
        if not cursor.fetchone():
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            ))
            print(f"✓ Database '{DB_NAME}' created successfully")
        else:
            print(f"✓ Database '{DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        raise


if __name__ == "__main__":
    create_database()
    
    # After database is created, initialize schema
    from schema import init_db
    init_db()
