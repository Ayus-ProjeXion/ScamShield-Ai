from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from backend.schemas import CommunityReportRequest, CommunityReportResponse
from backend.database import db

router = APIRouter(prefix="/report", tags=["Community Reporting"])

@router.post("", response_model=CommunityReportResponse, summary="Submit Crowd-Sourced Scam Report")
async def submit_scam_report(payload: CommunityReportRequest):
    record = await db.save_report(payload.model_dump())
    return CommunityReportResponse(**record)

@router.get("s", summary="List Community Scam Reports")
async def list_scam_reports(limit: int = Query(20, ge=1, le=100)):
    reports = await db.get_reports(limit=limit)
    return {"total": len(reports), "reports": reports}
