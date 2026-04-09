"""
Import race data from CSV into MySQL database.
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.database.connection import get_connection

def import_csv_to_db(csv_path):
    """Import CSV data into the race_predictions table."""
    
    # Read CSV with different encodings
    print(f"Reading CSV from: {csv_path}")
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 encoding failed, trying latin-1...")
        df = pd.read_csv(csv_path, encoding='latin-1')
    
    # Drop empty rows
    df = df.dropna(how='all')
    
    # Replace nan with None for MySQL compatibility
    df = df.where(pd.notna(df), None)
    
    print(f"Found {len(df)} records to insert")
    
    # Connect to database
    with get_connection('root') as db:
        cursor = db.connection.cursor()
        
        insert_query = """
        INSERT INTO race_predictions 
        (driver, team, q1, q2, q3, start_position, finish_position, track, rain, d_elo, t_elo, year, round)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        count = 0
        for idx, row in df.iterrows():
            try:
                # Convert boolean rain value
                rain = True if str(row['Rain']).upper() == 'TRUE' else False
                
                values = (
                    row['Driver'],
                    row['Team'],
                    float(row['Q1']) if pd.notna(row['Q1']) else None,
                    float(row['Q2']) if pd.notna(row['Q2']) else None,
                    float(row['Q3']) if pd.notna(row['Q3']) else None,
                    int(row['Start']) if pd.notna(row['Start']) else None,
                    int(row['Finish']) if pd.notna(row['Finish']) else None,
                    row['Track'],
                    rain,
                    float(row['D_Elo']) if pd.notna(row['D_Elo']) else None,
                    float(row['T_Elo']) if pd.notna(row['T_Elo']) else None,
                    int(row['Year']),
                    int(row['Round'])
                )
                
                cursor.execute(insert_query, values)
                count += 1
                
                # Commit every 100 rows
                if count % 100 == 0:
                    db.connection.commit()
                    print(f"  ✓ Inserted {count} records...")
            
            except Exception as e:
                print(f"  ✗ Error inserting row {idx}: {e}")
                print(f"    Row data: {row.to_dict()}")
                continue
        
        # Final commit
        db.connection.commit()
        print(f"\n✓ Successfully inserted {count} records into the database!")
        cursor.close()

if __name__ == "__main__":
    csv_file = "c:\\Users\\DELL\\Desktop\\db_data_initial.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)
    
    try:
        import_csv_to_db(csv_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
