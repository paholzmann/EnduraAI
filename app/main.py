from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.performance_metrics import performance_metrics_router
from app.api.v1.routes.performance_projection import performance_projection_router
from app.api.v1.routes.race_database import race_database_router
from app.api.v1.routes.activity import activity_router

app = FastAPI(title="UTMB API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(performance_metrics_router)
app.include_router(performance_projection_router)
app.include_router(race_database_router)
app.include_router(activity_router)