from pydantic import BaseModel, Field

class ActivitySummaryResponse(BaseModel):
    summary: dict
    message: str