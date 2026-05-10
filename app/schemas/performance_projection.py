from pydantic import BaseModel, Field

class EffortBasedRaceMatchingRequest(BaseModel):
    distance: float = Field(..., description="Race distance", example=17.0)
    elevation: float = Field(..., description="Race elevation", example=700)
    min_effort_ratio: float = Field(0.85, description="Minimum effort ratio", example=0.85)
    max_effort_ratio: float = Field(1.2, description="Maximum effort ratio", example=1.2)
    limit: int = Field(20, ge=1, le=100, description="Items per page")
    offset: int = Field(0, ge=0, description="Items to skip")

class EffortBasedRaceMatchingResponse(BaseModel):
    result: list
    message: str

class RacePlacementProjectionRequest(BaseModel):
    distance: float = Field(..., description="Race distance", example=17.0)
    elevation: float = Field(..., description="Race elevation", example=700)
    total_time: float = Field(..., description="Total race time in hours", example=1.5)
    limit: int = Field(20, ge=1, le=100, description="Items per page")
    offset: int = Field(0, ge=0, description="Items to skip")

class RacePlacementProjectionResponse(BaseModel):
    result: list
    message: str