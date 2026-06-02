from fastapi import APIRouter, HTTPException, status
import pandas as pd
from app.ml.pipelines.race_outcome.prediction import RaceOutcomePredictor
from app.schemas.ml.race_outcome import *

race_outcome_router = APIRouter(prefix="/api/v1/race_outcome", tags=["Race Outcome Engine"])
model_path = "reports/race_outcome/2026-05-31_20-02-35/model.pkl"
race_outcome_predictor = RaceOutcomePredictor(model_path=model_path)


@race_outcome_router.post("/prediction", response_model=RaceOutcomePredictionResponse, status_code=status.HTTP_200_OK, summary="Predicting race outcome")
async def race_outcome_endpoint(payload: RaceOutcomePredictionRequest) -> RaceOutcomePredictionResponse:
    """
    curl -X POST http://127.0.0.1:8000/api/v1/race_outcome/prediction -H "Content-Type: application/json" -d "{\"distance\": 10, \"elevation\": 500, \"race_effort\": 15, \"elevation_per_km\": 50, \"effort_per_km\": 150, \"n_results\": 200}"
    """
    try:
        input_df = {"Distance": [payload.distance], "Elevation_Gain": [payload.elevation], "Elevation_per_km": [payload.elevation_per_km], "Race_Effort": [payload.race_effort], "Effort_per_km": [payload.effort_per_km], "N_Results": [payload.n_results]}
        input_df = pd.DataFrame(input_df)
        # print(input_df)
        result = race_outcome_predictor.get_prediction(input_df=input_df)
        return RaceOutcomePredictionResponse(result=result, message="Predicting race outcome successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))