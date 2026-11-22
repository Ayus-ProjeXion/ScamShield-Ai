import os
import time
import tempfile
import uuid
import asyncio
import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
from typing import Optional

from backend.schemas import (
    TextScanRequest, EmailScanRequest, ScanResponse, SecurityTokenSchema
)
from backend.database import db
from ai.detector import ScamDetector

router = APIRouter(prefix="/scan", tags=["Threat Scanning"])

# Singleton detector instance shared across requests
_detector_instance = None

def get_detector() -> ScamDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = ScamDetector()
    return _detector_instance

@router.post("/text", response_model=ScanResponse, summary="Scan SMS, WhatsApp, or Text Message")
async def scan_text(
    payload: TextScanRequest,
    background_tasks: BackgroundTasks,
    detector: ScamDetector = Depends(get_detector)
):
    start_time = time.perf_counter()
    client_id = payload.client_id or "web_client"
    
    # Run AI evaluation
    raw_res = detector.analyze(payload.text, client_id=client_id)
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    scan_id = str(uuid.uuid4())
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    token = raw_res.get("security_token", {})
    sec_token = SecurityTokenSchema(
        nonce=token.get("nonce", ""),
        timestamp=token.get("timestamp", int(time.time())),
        hmac_signature=token.get("hmac_signature", ""),
        tamper_proof=token.get("tamper_proof", True),
        algorithm=token.get("algorithm", "HMAC-SHA256-256BIT")
    )
    
    response_data = ScanResponse(
        scan_id=scan_id,
        text_preview=raw_res.get("sanitized_preview") or payload.text[:120],
        threat_level=raw_res["threat_level"],
        risk_score=raw_res["risk_score"],
        is_scam=raw_res["is_scam"],
        ml_probability=raw_res.get("ml_probability", 0.0),
        urgency_score=raw_res.get("urgency_score", 0.0),
        badges=raw_res.get("badges", []),
        why_its_risky=raw_res.get("why_its_risky", []),
        recommended_actions=raw_res.get("recommended_actions", []),
        complaint_draft=raw_res.get("complaint_draft", ""),
        security_token=sec_token,
        cached_response=raw_res.get("cached_response", False),
        rate_limited=raw_res.get("rate_limited", False),
        processing_time_ms=duration_ms,
        channel=payload.channel or "SMS",
        created_at=now_str
    )
    
    # Instant in-memory registration for immediate zero-latency retrieval
    db.scans[scan_id] = response_data.model_dump()
    # Asynchronously synchronize with Supabase in background
    background_tasks.add_task(db.save_scan, response_data.model_dump())
    return response_data

@router.post("/email", response_model=ScanResponse, summary="Scan RFC Email Headers & Body")
async def scan_email(
    payload: EmailScanRequest,
    background_tasks: BackgroundTasks,
    detector: ScamDetector = Depends(get_detector)
):
    start_time = time.perf_counter()
    client_id = payload.client_id or "email_client"
    
    raw_res = detector.analyze_email(payload.email_text, client_id=client_id)
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    scan_id = str(uuid.uuid4())
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    token = raw_res.get("security_token", {})
    sec_token = SecurityTokenSchema(
        nonce=token.get("nonce", ""),
        timestamp=token.get("timestamp", int(time.time())),
        hmac_signature=token.get("hmac_signature", ""),
        tamper_proof=token.get("tamper_proof", True),
        algorithm=token.get("algorithm", "HMAC-SHA256-256BIT")
    )
    
    response_data = ScanResponse(
        scan_id=scan_id,
        text_preview=raw_res.get("sanitized_preview") or payload.email_text[:120],
        threat_level=raw_res["threat_level"],
        risk_score=raw_res["risk_score"],
        is_scam=raw_res["is_scam"],
        ml_probability=raw_res.get("ml_probability", 0.0),
        urgency_score=raw_res.get("urgency_score", 0.0),
        badges=raw_res.get("badges", []),
        why_its_risky=raw_res.get("why_its_risky", []),
        recommended_actions=raw_res.get("recommended_actions", []),
        complaint_draft=raw_res.get("complaint_draft", ""),
        security_token=sec_token,
        cached_response=raw_res.get("cached_response", False),
        rate_limited=raw_res.get("rate_limited", False),
        processing_time_ms=duration_ms,
        channel="EMAIL",
        email_meta=raw_res.get("email_metadata"),
        created_at=now_str
    )
    
    db.scans[scan_id] = response_data.model_dump()
    background_tasks.add_task(db.save_scan, response_data.model_dump())
    return response_data

@router.post("/audio", response_model=ScanResponse, summary="Upload & Transcribe Voice Call Audio (.wav, .mp3)")
async def scan_audio(
    file: UploadFile = File(..., description="Audio recording of phone call (.wav, .mp3, .m4a)"),
    client_id: Optional[str] = Form("audio_client"),
    background_tasks: BackgroundTasks = None,
    detector: ScamDetector = Depends(get_detector)
):
    start_time = time.perf_counter()
    file_ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if file_ext not in [".wav", ".mp3", ".m4a", ".ogg"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{file_ext}'. Allowed formats: .wav, .mp3, .m4a, .ogg"
        )
        
    content = await file.read()
    # 15MB DoS File Size Guard
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Audio file exceeds 15MB maximum size threshold."
        )
        
    with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_audio_path = tmp_file.name
        
    try:
        # Run speech recognition in thread with 25s timeout to prevent thread deadlock
        raw_res = await asyncio.wait_for(
            asyncio.to_thread(detector.analyze_audio, tmp_audio_path, client_id or "audio_client"),
            timeout=25.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Audio transcription timed out after 25s.")
    finally:
        if os.path.exists(tmp_audio_path):
            try:
                os.remove(tmp_audio_path)
            except Exception:
                pass
                
    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
    scan_id = str(uuid.uuid4())
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    token = raw_res.get("security_token", {})
    sec_token = SecurityTokenSchema(
        nonce=token.get("nonce", ""),
        timestamp=token.get("timestamp", int(time.time())),
        hmac_signature=token.get("hmac_signature", ""),
        tamper_proof=token.get("tamper_proof", True),
        algorithm=token.get("algorithm", "HMAC-SHA256-256BIT")
    )
    
    response_data = ScanResponse(
        scan_id=scan_id,
        text_preview=raw_res.get("sanitized_preview") or raw_res.get("transcribed_text", "")[:120],
        threat_level=raw_res["threat_level"],
        risk_score=raw_res["risk_score"],
        is_scam=raw_res["is_scam"],
        ml_probability=raw_res.get("ml_probability", 0.0),
        urgency_score=raw_res.get("urgency_score", 0.0),
        badges=raw_res.get("badges", []),
        why_its_risky=raw_res.get("why_its_risky", []),
        recommended_actions=raw_res.get("recommended_actions", []),
        complaint_draft=raw_res.get("complaint_draft", ""),
        security_token=sec_token,
        cached_response=raw_res.get("cached_response", False),
        rate_limited=raw_res.get("rate_limited", False),
        processing_time_ms=duration_ms,
        channel="CALL",
        audio_meta={
            "filename": file.filename,
            "transcription_engine": raw_res.get("transcription_engine", "Whisper STT"),
            "transcribed_text": raw_res.get("transcribed_text", "")
        },
        created_at=now_str
    )
    
    db.scans[scan_id] = response_data.model_dump()
    if background_tasks:
        background_tasks.add_task(db.save_scan, response_data.model_dump())
    else:
        await db.save_scan(response_data.model_dump())
    return response_data

@router.get("/{scan_id}", summary="Retrieve Scan Details & Incident Report")
async def get_scan_details(scan_id: str):
    scan = await db.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail=f"Scan with ID '{scan_id}' not found.")
    return scan
