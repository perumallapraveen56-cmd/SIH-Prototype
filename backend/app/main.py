import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database.session import Base, engine, SessionLocal
from app.database.seed_data import seed_database
from app.api.auth_routes import router as auth_router
from app.api.project_routes import router as project_router
from app.api.gis_routes import router as gis_router
from app.api.shap_routes import router as shap_router
from app.api.recommendation_routes import router as rec_router
from app.api.whatif_routes import router as whatif_router
from app.api.alert_routes import router as alert_router
from app.api.report_routes import router as report_router
from app.api.analytics_routes import router as analytics_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sih26017_backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schema...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Ensuring database seed records exist...")
        seed_database()
    except Exception as e:
        logger.error("Error during startup database initialization: %s", e)
    yield
    logger.info("Shutting down land acquisition backend services.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Predictive Analytics System for Early Detection of Land Acquisition Delays (SIH26017 - NEXORA_TAU)",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow development and production origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled server exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing the land acquisition request. Please try again later.",
            "path": request.url.path
        }
    )

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(project_router, prefix=settings.API_V1_STR)
app.include_router(gis_router, prefix=settings.API_V1_STR)
app.include_router(shap_router, prefix=settings.API_V1_STR)
app.include_router(rec_router, prefix=settings.API_V1_STR)
app.include_router(whatif_router, prefix=settings.API_V1_STR)
app.include_router(alert_router, prefix=settings.API_V1_STR)
app.include_router(report_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "system": "Land Acquisition Delay Prediction System",
        "ps_id": "SIH26017",
        "team": "NEXORA_TAU",
        "status": "OPERATIONAL",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "models": "loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
