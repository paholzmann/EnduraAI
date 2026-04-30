from fastapi import APIRouter, HTTPException, status
from app.domain.performance_projection import PerformanceProjection
from app.schemas.performance_projection import *
from app.core.utils.file_utils import FileUtils
from app.core.utils.dataframe_utils import DataFrameUtils
from app.services.utmb.process import ProcessUTMBData

performance_projection_router = APIRouter(prefix="/api/v1/performance_projection", tags=["Performance Projection"])
performance_projection = PerformanceProjection()
dataframe_utils = DataFrameUtils()

utmb_df = FileUtils().read_csv_as_df(csv_path="data/processed/utmb/utmb-race-data-features.csv")
utmb_df = ProcessUTMBData().parse_race_results(utmb_df=utmb_df)

@performance_projection_router.post("/effort_based_race_matching", response_model=EffortBasedRaceMatchingResponse, status_code=status.HTTP_200_OK, summary="Effort based race matching")
async def effort_based_race_matching_endpoint(payload: EffortBasedRaceMatchingRequest) -> EffortBasedRaceMatchingResponse:
    """
    curl -X POST http://127.0.0.1:8000/api/v1/performance_projection/effort_based_race_matching -H "Content-Type: application/json" -d "{\"distance\": 10, \"elevation\": 500}"
    """
    filtered_utmb_df = dataframe_utils.columns_to_keep(df=utmb_df, cols=["Race_Effort", "Distance", "Elevation_Gain"])
    try:
        result = performance_projection.effort_based_race_matching(utmb_df=filtered_utmb_df, distance=payload.distance, elevation=payload.elevation, min_effort_ratio=payload.min_effort_ratio, max_effort_ratio=payload.max_effort_ratio)
        result = dataframe_utils.df_to_dict(df=result)
        return EffortBasedRaceMatchingResponse(result=result, message="Effort based race matching successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@performance_projection_router.post("/race_placement_projection", response_model=RacePlacementProjectionResponse, status_code=status.HTTP_200_OK, summary="Race placement projection")
async def race_placement_projection_endpoint(payload: RacePlacementProjectionRequest) -> RacePlacementProjectionResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_projection/race_placement_projection -H "Content-Type: application/json" -d "{\"distance\": 17, \"elevation\": 700, \"total_time\": 90}"
    """
    try:
        fitting_races_df = performance_projection.race_placement_projection(utmb_df=utmb_df, distance=payload.distance, elevation=payload.elevation, total_time=payload.total_time)
        filtered_df = dataframe_utils.columns_to_keep(df=fitting_races_df, cols=["Race_Effort", "Results", "Distance", "Elevation_Gain", "Time_Based_On_Flat_Equivalent", "Pace_on_flat_equivalent", "Possible_Placement"])
        result = dataframe_utils.df_to_dict(df=filtered_df)
        return RacePlacementProjectionResponse(result=result, message="Race placement projection successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))