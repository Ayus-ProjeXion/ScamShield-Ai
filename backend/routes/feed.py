from fastapi import APIRouter, Query, Response
from typing import Optional, List

from backend.schemas import ThreatFeedResponse, ThreatFeedItem
from backend.database import db

router = APIRouter(prefix="/feed", tags=["Threat Intelligence Feed"])

@router.get("", response_model=ThreatFeedResponse, summary="Get Live Verified Threat Intelligence Feed")
async def get_threat_feed(
    response: Response,
    limit: int = Query(50, ge=1, le=100, description="Max feed items to return"),
    category: Optional[str] = Query(None, description="Filter by category (PHISHING_URL, SMISHING_SMS, etc.)")
):
    # Set Edge & Browser Caching headers (60s browser, 300s shared CDN)
    response.headers["Cache-Control"] = "public, max-age=60, s-maxage=300"
    items = await db.get_threat_feed(limit=limit, category=category)
    return ThreatFeedResponse(
        total_count=len(items),
        items=[ThreatFeedItem(**i) for i in items]
    )
