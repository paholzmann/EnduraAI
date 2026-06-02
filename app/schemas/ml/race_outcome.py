from pydantic import BaseModel, Field


class RaceOutcomePredictionRequest(BaseModel):
    distance: float = Field(..., description="Race distance", example=17.0)
    elevation: float = Field(..., description="Race elevation", example=700)
    elevation_per_km: float = Field(..., description="Elevation gain per km", example=40)
    race_effort: float = Field(..., description="Race effort", example=21.0)
    effort_per_km: float = Field(..., description="Effort per km", example=140)
    n_results: int = Field(..., description="Number of participants", example=200)

class RaceOutcomePredictionResponse(BaseModel):
    result: dict
    message: str