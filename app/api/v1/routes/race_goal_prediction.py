from fastapi import APIRouter
from app.schemas.race_goal_prediction import (
    RaceGoalPredictionRequest,
    RaceGoalPredictionResponse,
)
from app.domain.race_goal_prediction import RaceGoalPrediction

race_goal_prediction_router = APIRouter(prefix="/api/v1/race_goal", tags=["race_goal"])
race_goal_predictor = RaceGoalPrediction()


@race_goal_prediction_router.post("/predict", response_model=RaceGoalPredictionResponse)
async def predict_race_goal(payload: RaceGoalPredictionRequest):
    """
    Predict a realistic (challenging but achievable) race goal based on recent race performance.

    Input:
    - recent_race: Distance (km), elevation (m), and finish time (hours) from a completed race
    - target_race: Distance (km) and elevation (m) for the target race

    Output:
    - Predicted finish time in hours and HH:MM:SS format
    - Runner's pace on flat equivalent (from recent race)
    - Adjusted pace (85% of recent = conservative estimate)

    The prediction uses an 0.85 adjustment factor, meaning it predicts 15% slower than
    the runner's recent pace—accounting for unknowns and providing a challenging but
    realistic goal.
    """
    result = race_goal_predictor.predict_goal_time(
        recent_distance=payload.recent_race.distance,
        recent_elevation=payload.recent_race.elevation,
        recent_finish_time=payload.recent_race.finish_time,
        target_distance=payload.target_race.distance,
        target_elevation=payload.target_race.elevation,
    )

    return RaceGoalPredictionResponse(
        predicted_time_hours=result["predicted_time_hours"],
        predicted_time_str=result["predicted_time_str"],
        recent_pace_on_flat=result["recent_pace_on_flat"],
        adjusted_pace_on_flat=result["adjusted_pace_on_flat"],
        message="Race goal prediction successful",
    )
