from fastapi import APIRouter, UploadFile, File, HTTPException, status
import tempfile
import shutil
import os
from app.schemas.activity import *
from app.gpx.activities.activity import Activity

activity_router = APIRouter(prefix="/api/v1/activity", tags=["Activity"])
activity = Activity()

@activity_router.post("/health")
async def health():
    return "OK"

@activity_router.post("/summary", response_model=ActivitySummaryResponse, status_code=status.HTTP_200_OK, summary="Activity summary")
async def activity_summary_endpoint(file: UploadFile = File(...)) -> ActivitySummaryResponse:
    """
    curl -X POST http://127.0.0.1:8000/api/v1/activity/summary -F "file=@C:/Users/patri/100k+ Entwickler/EndurAI/data/raw/gpx/10k_400m.gpx"
    """
    if not file.filename.lower().endswith(".gpx"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .gpx files are allowed.")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gpx") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        summary = activity.activity_summary(filepath=temp_file_path)
        return ActivitySummaryResponse(summary=summary, message="Getting activity summary successfull")
    finally:
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)