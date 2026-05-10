from pydantic import BaseModel, Field


class GetRaceDatabaseRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="Items per page")
    offset: int = Field(0, ge=0, description="Items to skip")

class GetRaceDatabaseResponse(BaseModel):
    result: list
    message: str