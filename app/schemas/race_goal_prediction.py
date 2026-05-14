from pydantic import BaseModel, Field


class RecentRaceInput(BaseModel):
    distance: float = Field(..., description="Recent race distance in km", example=17.0)
    elevation: float = Field(..., description="Recent race elevation gain in m", example=700)
    finish_time: float = Field(..., description="Recent race finish time in hours", example=1.5)


class TargetRaceInput(BaseModel):
    distance: float = Field(..., description="Target race distance in km", example=42.0)
    elevation: float = Field(..., description="Target race elevation gain in m", example=2000)


class RaceGoalPredictionRequest(BaseModel):
    recent_race: RecentRaceInput = Field(..., description="Runner's recent completed race")
    target_race: TargetRaceInput = Field(..., description="Target race to predict goal for")


class RaceGoalPredictionResponse(BaseModel):
    predicted_time_hours: float = Field(..., description="Predicted finish time in hours")
    predicted_time_str: str = Field(..., description="Predicted finish time formatted as HH:MM:SS")
    recent_pace_on_flat: float = Field(..., description="Runner's pace on flat equivalent from recent race")
    adjusted_pace_on_flat: float = Field(..., description="Conservative adjusted pace (85% of recent)")
    message: str = Field(..., description="Status message")
