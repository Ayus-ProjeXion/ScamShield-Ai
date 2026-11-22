import time
import datetime
from fastapi import APIRouter

from backend.schemas import HealthResponse
from backend.config import settings
from backend.database import db
from ai.detector import ScamDetector

router = APIRouter(tags=["System Health"])

@router.get("/health", response_model=HealthResponse, summary="System Health & AI Engine Metrics")
@router.get("/api/v1/health", response_model=HealthResponse, summary="System Health & AI Engine Metrics (v1)")
async def health_check():
    detector = ScamDetector()
    
    # Measure live microsecond inference benchmark
    t0 = time.perf_counter()
    sample_scan = detector.analyze("Test health ping", client_id="health_probe")
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    
    return HealthResponse(
        status="HEALTHY",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        ai_engine_status="ACTIVE",
        model_loaded=detector.model is not None,
        ml_confidence_sample=sample_scan.get("ml_probability", 0.0),
        avg_inference_latency_ms=latency_ms,
        database_connected=db.is_connected,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
