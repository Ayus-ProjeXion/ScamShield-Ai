import time
import datetime
from collections import deque
from fastapi import APIRouter

from backend.schemas import HealthResponse
from backend.config import settings
from backend.database import db
from ai.detector import ScamDetector

router = APIRouter(tags=["System Health"])

# Rolling window of recent inference latencies for P50/P95/P99 observability
_recent_latencies = deque(maxlen=100)

@router.get("/health", response_model=HealthResponse, summary="System Health & AI Engine Metrics")
@router.get("/api/v1/health", response_model=HealthResponse, summary="System Health & AI Engine Metrics (v1)")
async def health_check():
    detector = ScamDetector()
    
    # Measure live microsecond inference benchmark
    t0 = time.perf_counter()
    sample_scan = detector.analyze("Test health ping", client_id="health_probe")
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    _recent_latencies.append(latency_ms)
    
    # Calculate P50, P95, and P99 percentiles
    sorted_lats = sorted(_recent_latencies)
    n = len(sorted_lats)
    p50 = sorted_lats[int(n * 0.50)] if n else latency_ms
    p95 = sorted_lats[min(int(n * 0.95), n - 1)] if n else latency_ms
    p99 = sorted_lats[min(int(n * 0.99), n - 1)] if n else latency_ms
    
    circuit_state = "OPEN_FAILING_FAST" if time.time() < db.circuit_open_until else "CLOSED_NORMAL"
    
    return HealthResponse(
        status="HEALTHY",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        ai_engine_status="ACTIVE",
        model_loaded=detector.model is not None,
        ml_confidence_sample=sample_scan.get("ml_probability", 0.0),
        avg_inference_latency_ms=latency_ms,
        p50_latency_ms=round(p50, 2),
        p95_latency_ms=round(p95, 2),
        p99_latency_ms=round(p99, 2),
        circuit_breaker_status=circuit_state,
        database_connected=db.is_connected,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
