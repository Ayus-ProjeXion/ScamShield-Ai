import time
import uuid
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.routes import scan, report, feed, health, copilot, whatsapp
from ai.detector import ScamDetector

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ScamShieldAPI")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Warm up AI detector and model in memory
    logger.info("Initializing ScamShield AI Engine in memory...")
    t0 = time.perf_counter()
    detector = ScamDetector()
    _ = detector.analyze("Engine warm up ping", client_id="warmup_probe")
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"ScamShield AI Engine warmed up in {elapsed} ms. Ready for incoming traffic!")
    yield
    logger.info("ScamShield API shutting down gracefully.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Production REST API Gateway for ScamShield AI. "
        "Delivers multi-modal real-time fraud threat intelligence across SMS, Email, Hinglish, and Voice Audio."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (Permits configured origins + all Vercel deployment subdomains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Performance Timing, Correlation ID & Observability Middleware
@app.middleware("http")
async def add_observability_headers(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = round((time.perf_counter() - start_time) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(process_time)
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Engine"] = "ScamShield-Dual-Core-ML"
    return response

# Mount API Routers
app.include_router(health.router)
app.include_router(scan.router, prefix=settings.API_V1_PREFIX)
app.include_router(report.router, prefix=settings.API_V1_PREFIX)
app.include_router(feed.router, prefix=settings.API_V1_PREFIX)
app.include_router(copilot.router, prefix=settings.API_V1_PREFIX)
app.include_router(whatsapp.router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Root"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "Multi-Modal Cyber-Fraud Threat Intelligence API",
        "documentation": "/docs",
        "health_check": "/health",
        "endpoints": {
            "scan_text": f"{settings.API_V1_PREFIX}/scan/text",
            "scan_email": f"{settings.API_V1_PREFIX}/scan/email",
            "scan_audio": f"{settings.API_V1_PREFIX}/scan/audio",
            "submit_report": f"{settings.API_V1_PREFIX}/report",
            "threat_feed": f"{settings.API_V1_PREFIX}/feed",
            "whatsapp_webhook": f"{settings.API_V1_PREFIX}/webhook/whatsapp",
            "whatsapp_simulate": f"{settings.API_V1_PREFIX}/webhook/whatsapp/simulate"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
