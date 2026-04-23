from pydantic import BaseModel, Field


class CalculateWithDistanceElevationRequest(BaseModel):
    """
    distance in km
    elevation in m+
    """
    distance: float = Field(..., description="Race distance", example=17.0)
    elevation: float = Field(..., description="Race elevation", example=700)

class CalculateWithDistanceElevationResponse(BaseModel):
    result: float
    message: str

class CalculateWithTimeRaceEffortRequest(BaseModel):
    """
    total_time in hours
    race_effort in km
    """
    total_time: float = Field(..., description="Total time", example=1.0)
    race_effort: float = Field(..., description="Race effort", example=15.0)

class CalculateWithTimeRaceEffortResponse(BaseModel):
    result: float
    message: str

class CalculateWithTotalHoursElevationRequest(BaseModel):
    """
    total hours in h
    elevation in m+
    """
    total_hours: float = Field(..., description="Total hours", example=15.0)
    elevation: float = Field(..., description="Race elevation", example=6000)


class CalculateWithTotalHoursElevationResponse(BaseModel):
    """
    
    """
    result: float
    message: str

class CalculateRaceDifficultyScoreRequest(BaseModel):
    distance: float = Field(..., description="Distance", example=15.0)
    elevation: float = Field(..., description="Elevation gain", example=700)
    alpha: float = Field(0.7, description="Weight of vertical rate", example=0.7)
    c: float = Field(80.0, description="Sigmoid center", example=80.0)
    k: float = Field(0.05, description="Sigmoid steepness", example=0.05)

class CalculateRaceDifficultyScoreResponse(BaseModel):
    result: float
    message: str

class CalculateRaceCategoryRequest(BaseModel):
    distance: float
    elevation: float

class CalculateRaceCategoryResponse(BaseModel):
    result: str
    message: str