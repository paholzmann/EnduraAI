from fastapi import APIRouter, HTTPException, status
from app.schemas.race_database import *
from app.core.utils.file_utils import FileUtils
from app.core.utils.dataframe_utils import DataFrameUtils
from app.services.utmb.process import ProcessUTMBData

race_database_router = APIRouter(prefix="/api/v1/race_database", tags=["Race Database"])
file_utilities = FileUtils()
dataframe_utilities = DataFrameUtils()

utmb_df = FileUtils().read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")
# utmb_df = ProcessUTMBData().parse_race_results(utmb_df=utmb_df)

@race_database_router.post("/get_race_database", response_model=GetRaceDatabaseResponse, status_code=status.HTTP_200_OK, summary="Getting race database")
async def getr_race_database_endpoint(payload: GetRaceDatabaseRequest) -> GetRaceDatabaseResponse:
    """
    curl -X POST http://127.0.0.1:8000/api/v1/race_database/get_race_database -H "Content-Type: application/json" -d "{\"limit\": 100, \"offset\": 0}"
    """
    try:
        result = utmb_df
        result = result[payload.offset:payload.offset + payload.limit]
        result = dataframe_utilities.df_to_dict(df=result)
        return GetRaceDatabaseResponse(result=result, message="Getting race database successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))