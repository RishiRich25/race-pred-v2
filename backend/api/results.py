from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_now, predict_prev
import pandas as pd

app = FastAPI(title="F1 Race Prediction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict/next")
def get_next_prediction():
    """
    Predict the outcome of the next F1 race.
    Returns predicted positions and scores for all drivers.
    """
    try:
        result = predict_now()
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predict/race")
def get_race_prediction(year: int, round: int):
    """
    Predict the outcome of a specific F1 race.
    
    Parameters:
    - year: The year of the race (2018-present)
    - round: The round number of the race
    
    Returns predicted positions and scores for all drivers.
    """
    try:
        result = predict_prev(year, round)
        return JSONResponse(content=result.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "F1 Race Prediction API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
