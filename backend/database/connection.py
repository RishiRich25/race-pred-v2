"""
MySQL database connection module for F1 predictions.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """Manages MySQL database connections."""
    
    def __init__(self, user_type='root'):
        """
        Initialize database connection.
        
        Args:
            user_type: 'root' for admin access or 'full_user' for limited access
        """
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.database = os.getenv('DB_NAME', 'f1_predictions')
        
        if user_type == 'root':
            self.user = os.getenv('DB_USER', 'root')
            self.password = os.getenv('DB_PASSWORD', 'Rishit123$')
        elif user_type == 'full_user':
            self.user = os.getenv('DB_USER_FULL', 'full_user')
            self.password = os.getenv('DB_PASSWORD_FULL', 'FullUser123$')
        else:
            raise ValueError("user_type must be 'root' or 'full_user'")
        
        self.connection = None
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"Connected to {self.database} as {self.user}")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from database")
    
    def execute_query(self, query, params=None):
        """
        Execute a SELECT query.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or list)
        
        Returns:
            List of dictionaries with query results
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or list)
        
        Returns:
            Number of affected rows
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as e:
            self.connection.rollback()
            print(f"Error executing update: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

# Helper functions
def get_connection(user_type='root'):
    """Get a database connection context manager."""
    return DatabaseConnection(user_type)
