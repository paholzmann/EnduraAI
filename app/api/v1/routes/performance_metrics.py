from fastapi import APIRouter, HTTPException, status
from app.domain.performance_metrics import Performance_Metrics
from app.schemas.performance_metrics import *

performance_metrics_router = APIRouter(prefix="/api/v1/performance_metrics", tags=["Performance Metrics"])
performance_metrics = Performance_Metrics()


@performance_metrics_router.post("/race_effort", response_model=CalculateWithDistanceElevationResponse, status_code=status.HTTP_200_OK, summary="Calculating race effort")
async def calculate_race_effort_endpoint(payload: CalculateWithDistanceElevationRequest) -> CalculateWithDistanceElevationResponse:
    """
    curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/race_effort -H "Content-Type: application/json" -d "{\"distance\": 10, \"elevation\": 500}"
    """
    try:
        race_effort = performance_metrics.calculate_race_effort(
            payload.distance, payload.elevation)
        return CalculateWithDistanceElevationResponse(result=race_effort, message="Calculating race effort successfull")

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@performance_metrics_router.post("/vertical_rate", response_model=CalculateWithDistanceElevationResponse, status_code=status.HTTP_200_OK, summary="Calculating vertical rate")
async def calculate_vertical_rate_endpoint(payload: CalculateWithDistanceElevationRequest) -> CalculateWithDistanceElevationResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/vertical_rate -H "Content-Type: application/json" -d "{\"distance\": 10, \"elevation\": 500}"
    """
    try:
        vertical_rate = performance_metrics.calculate_vertical_rate(
            payload.distance, payload.elevation
        )
        return CalculateWithDistanceElevationResponse(result=vertical_rate, message="Calculating vertical rate successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@performance_metrics_router.post("/estimated_pace_on_flat_equivalent", response_model=CalculateWithTimeRaceEffortResponse, status_code=status.HTTP_200_OK, summary="Calculating estimated pace on flat equivalent")
async def calculate_estimated_pace_on_flat_equivalent_endpoint(payload: CalculateWithTimeRaceEffortRequest) -> CalculateWithTimeRaceEffortResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/estimated_pace_on_flat_equivalent -H "Content-Type: application/json" -d "{\"total_time\": 1.0, \"race_effort\": 15}"
    """
    try:
        estimated_pace = performance_metrics.calculate_estimated_pace_on_flat_equivalent(payload.total_time, payload.race_effort)
        return CalculateWithTimeRaceEffortResponse(result=estimated_pace, message="Calculating estimated pace on flat equivalent successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@performance_metrics_router.post("/vertical_per_hour", response_model=CalculateWithTotalHoursElevationResponse, status_code=status.HTTP_200_OK, summary="Calculating vertical per hour")
async def calculate_vertical_per_hour_endpoint(payload: CalculateWithTotalHoursElevationRequest) -> CalculateWithTotalHoursElevationResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/vertical_per_hour -H "Content-Type: application/json" -d "{\"total_hours\": 15.0, \"elevation\": 6000}"
    """
    try:
        vertical_per_hour = performance_metrics.calculate_vertical_per_hour(total_hours=payload.total_hours, elevation_gain=payload.elevation)
        return CalculateWithTotalHoursElevationResponse(result=vertical_per_hour, message="Calculating vertical per hour successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@performance_metrics_router.post("/race_difficulty_score", response_model=CalculateRaceDifficultyScoreResponse, status_code=status.HTTP_200_OK, summary="Calculating race difficulty score")
async def calculate_race_difficulty_score_endpoint(payload: CalculateRaceDifficultyScoreRequest) -> CalculateRaceDifficultyScoreResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/race_difficulty_score -H "Content-Type: application/json" -d "{\"distance\": 15.0, \"elevation\": 700}"
    """
    try:
        race_difficulty_score = performance_metrics.calculate_race_difficulty_score(distance=payload.distance, elevation=payload.elevation, alpha=payload.alpha, c=payload.c, k=payload.k)
        return CalculateRaceDifficultyScoreResponse(result=race_difficulty_score, message="Calculating race difficulty score successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@performance_metrics_router.post("/race_category", response_model=CalculateRaceCategoryResponse, status_code=status.HTTP_200_OK, summary="Calculating race category")
async def calculate_race_category_router(payload: CalculateRaceCategoryRequest) -> CalculateRaceCategoryResponse:
    """
        curl -X POST http://127.0.0.1:8000/api/v1/performance_metrics/race_category -H "Content-Type: application/json" -d "{\"distance\": 15.0, \"elevation\": 700}"
    """
    try:
        race_category = performance_metrics.calculate_race_category(distance=payload.distance, elevation=payload.elevation)
        return CalculateRaceCategoryResponse(result=race_category, message="Calculating race category successfull")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))