from fastapi import APIRouter, Query
from typing import Optional, List

from backend.schemas import ThreatFeedResponse, ThreatFeedItem
from backend.database import db

router = APIRouter(prefix="/feed", tags=["Threat Intelligence Feed"])

@router.get("", response_model=ThreatFeedResponse, summary="Get Live Verified Threat Intelligence Feed")
async def get_threat_feed(
    limit: int = Query(50, ge=1, le=100, description="Max feed items to return"),
    category: Optional[str] = Query(None, description="Filter by category (PHISHING_URL, SMISHING_SMS, etc.)")
):
    items = await db.get_threat_feed(limit=limit, category=category)
    return ThreatFeedResponse(
        total_count=len(items),
        items=[ThreatFeedItem(**i) for i in items]
    )
