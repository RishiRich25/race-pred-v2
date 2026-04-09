import pandas as pd
import os
import xgboost as xgb
import fastf1
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.ml.preprocessing import Preprocessor
from backend.database.connection import DatabaseConnection

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "backend" / "api" / "cache"
ML_DIR = PROJECT_ROOT / "backend" / "ml"
DATA_DIR = PROJECT_ROOT / "data"

if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache(str(CACHE_DIR))

def load_model():
    model = xgb.Booster()
    model.load_model(str(ML_DIR / "f1_rank_model.json"))
    return model

def load_preprocessor():
    prep = Preprocessor()
    prep.load_encoders(str(ML_DIR / "encoders.pkl"))
    return prep

model = load_model()
prep = load_preprocessor()

def predict_now():
    current_year = datetime.now().year
    try:
        schedule = fastf1.get_event_schedule(current_year, backend="ergast")
    except:
        raise Exception("Could not load schedule. Please try again later.")
    now = pd.Timestamp.now()

    next_event = schedule[schedule["EventDate"] >= now].iloc[0]
    event_name = next_event["EventName"]
    round_number = next_event["RoundNumber"]

    try:
        session = fastf1.get_session(current_year, round_number, "Q")
        session.load()
        quali = session.results
    except Exception:
        raise Exception("Qualifying not available yet. Come back after qualifying is over on a Saturday")

    if len(quali) == 0:
        round_number -= 1
        try:
            session = fastf1.get_session(current_year, round_number, "Q")
            session.load()
            quali = session.results
        except Exception:
            raise Exception("Qualifying not available yet. Come back after qualifying is over on a Saturday")

    race_df = pd.DataFrame({
        "Driver": quali["DriverId"],
        "Team": quali["TeamId"],
        "Q1": quali["Q1"].dt.total_seconds().fillna(0),
        "Q2": quali["Q2"].dt.total_seconds().fillna(0),
        "Q3": quali["Q3"].dt.total_seconds().fillna(0),
        "Start": quali["Position"],
        "Track": event_name,
        "Rain": 0
    })

    driver_elo = pd.read_csv(str(DATA_DIR / "this_year_driver.csv"), encoding="latin1")
    driver_elo = driver_elo.rename(columns={
        "Name": "Driver"
    })
    team_elo = pd.read_csv(str(DATA_DIR / "this_year_team.csv"), encoding="latin1")
    team_elo = team_elo.rename(columns={
        "Name": "Team"
    })

    race_df["Driver_Name"] = race_df["Driver"]
    race_df["Team_Name"] = race_df["Team"]

    race_df = race_df.merge(
        driver_elo[["Driver", "Elo"]],
        on="Driver",
        how="left"
    ).rename(columns={"Elo": "D_Elo"})

    race_df = race_df.merge(
        team_elo[["Team", "Elo"]],
        on="Team",
        how="left"
    ).rename(columns={"Elo": "T_Elo"})

    race_df["D_Elo"] = race_df["D_Elo"].fillna(1200)
    race_df["T_Elo"] = race_df["T_Elo"].fillna(1800)

    FEAT = [
        "Driver", "Team", "Start",
        "D_Elo", "T_Elo"
    ]

    race_df = prep.encode(
        race_df,
        mode="update",
        save=True
    )

    FEATURES = [
        "Driver", "Team", "Track", "Rain",
        "Q1", "Q2", "Q3", "Start",
        "D_Elo", "T_Elo"
    ]
    race_df = race_df.dropna().reset_index(drop=True)

    dtest = xgb.DMatrix(race_df[FEATURES])
    dtest.set_group([len(race_df)])

    scores = model.predict(dtest)

    race_df["Predicted_Score"] = scores
    race_df = race_df.sort_values(
        by="Predicted_Score",
        ascending=False
    ).reset_index(drop=True)
    race_df["Predicted_Position"] = race_df.index + 1
    return race_df[[
            "Predicted_Position",
            "Driver_Name",
            "Team_Name",
            "Start",
            "Predicted_Score"
        ]].rename(columns={
            "Driver_Name": "Driver",
            "Team_Name": "Team",
            "Start":"Starting Position"
        })
    


def predict_prev(yr, rd):
    current_year = datetime.now().year
    if yr >= 2018 and yr < current_year:
        None
    else:
        raise Exception(f"Year must be between 2018 and {current_year}")

    if rd <= 1 or rd > 24:
        raise Exception(f"Round number must be between 1 and 24 for the year {yr}")

    # Fetch data from database
    db = DatabaseConnection(user_type='full_user')
    
    try:
        query = """
            SELECT driver, team, q1, q2, q3, start_position, track, rain, d_elo, t_elo
            FROM race_predictions
            WHERE year = %s AND round = %s
        """
        results = db.execute_query(query, (yr, rd))
        db.disconnect()
    except Exception as e:
        raise Exception(f"Error fetching data from database: {str(e)}")

    if not results or len(results) == 0:
        raise Exception(f"No prediction data found for year {yr}, round {rd}")

    # Build race_df from database results
    race_df = pd.DataFrame(results)
    
    # Rename columns to match expected structure
    race_df = race_df.rename(columns={
        'driver': 'Driver',
        'team': 'Team',
        'q1': 'Q1',
        'q2': 'Q2',
        'q3': 'Q3',
        'start_position': 'Start',
        'track': 'Track',
        'rain': 'Rain',
        'd_elo': 'D_Elo',
        't_elo': 'T_Elo'
    })
    
    # Add driver and team names (same as driver and team for display)
    race_df["Driver_Name"] = race_df["Driver"]
    race_df["Team_Name"] = race_df["Team"]

    # Handle missing Elo values
    race_df["D_Elo"] = race_df["D_Elo"].fillna(1200)
    race_df["T_Elo"] = race_df["T_Elo"].fillna(1800)

    # Encode features
    race_df = prep.encode(
        race_df,
        mode="update",
        save=True
    )

    FEATURES = [
        "Driver", "Team", "Track", "Rain",
        "Q1", "Q2", "Q3", "Start",
        "D_Elo", "T_Elo"
    ]
    race_df = race_df.dropna().reset_index(drop=True)

    dtest = xgb.DMatrix(race_df[FEATURES])
    dtest.set_group([len(race_df)])

    scores = model.predict(dtest)

    race_df["Predicted_Score"] = scores
    race_df = race_df.sort_values(
        by="Predicted_Score",
        ascending=False
    ).reset_index(drop=True)
    race_df["Predicted_Position"] = race_df.index + 1
    
    return race_df[[
            "Predicted_Position",
            "Driver_Name",
            "Team_Name",
            "Start",
            "Predicted_Score"
        ]].rename(columns={
            "Driver_Name": "Driver",
            "Team_Name": "Team",
            "Start":"Starting Position"
        })