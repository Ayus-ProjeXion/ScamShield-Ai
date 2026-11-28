from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# ============================================================================
# 1. SCAN SCHEMAS
# ============================================================================

class TextScanRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Raw SMS, WhatsApp, or chat message to analyze")
    client_id: Optional[str] = Field("web_client", description="Client identifier for rate-limiting and tracking")
    channel: Optional[str] = Field("SMS", description="Communication channel: SMS, WHATSAPP, TELEGRAM, URL")

class EmailScanRequest(BaseModel):
    email_text: Optional[str] = Field(None, description="Full RFC email text including From, Subject, and Body")
    raw_email: Optional[str] = Field(None, description="Alias for email_text")
    client_id: Optional[str] = Field("email_client", description="Client identifier for rate-limiting")

class SecurityTokenSchema(BaseModel):
    nonce: str
    timestamp: int
    hmac_signature: str
    tamper_proof: bool = True
    algorithm: str = "HMAC-SHA256-256BIT"

class ScanResponse(BaseModel):
    scan_id: str
    text_preview: str
    threat_level: str
    risk_score: float
    is_scam: bool
    ml_probability: float
    urgency_score: float
    badges: List[str]
    why_its_risky: List[Dict[str, str]]
    explanation: Optional[str] = None
    recommended_actions: List[str]
    complaint_draft: str
    security_token: SecurityTokenSchema
    cached_response: bool = False
    rate_limited: bool = False
    processing_time_ms: float
    channel: str
    audio_meta: Optional[Dict[str, Any]] = None
    email_meta: Optional[Dict[str, Any]] = None
    created_at: str

# ============================================================================
# 2. COMMUNITY REPORT SCHEMAS
# ============================================================================

class CommunityReportRequest(BaseModel):
    ioc_value: str = Field(..., min_length=3, description="Suspicious Phone Number, UPI ID, Domain, or URL")
    ioc_type: str = Field("PHONE_NUMBER", description="Type: PHONE_NUMBER, UPI_VPA, DOMAIN, URL")
    category: str = Field("IMPERSONATION", description="Scam Category: IMPERSONATION, UPI_PAYMENT_FRAUD, PHISHING_URL, etc.")
    title: str = Field(..., min_length=5, max_length=120, description="Short summary of scam attempt")
    description: str = Field(..., min_length=10, max_length=2000, description="Detailed incident description")
    evidence_url: Optional[str] = Field(None, description="Optional screenshot or hosted evidence link")
    reporter_id: Optional[str] = Field(None, description="Optional user UUID")

class CommunityReportResponse(BaseModel):
    id: str
    ioc_value: str
    ioc_type: str
    category: str
    title: str
    description: str
    upvote_count: int = 1
    status: str = "PENDING"
    created_at: str
    message: str = "Report submitted successfully to ScamShield Community Intelligence"

# ============================================================================
# 3. THREAT FEED SCHEMAS
# ============================================================================

class ThreatFeedItem(BaseModel):
    id: str
    ioc_type: str
    ioc_value: str
    severity: str
    category: str
    description: Optional[str] = None
    confidence: float
    is_blacklisted: bool
    source: str
    created_at: str

class ThreatFeedResponse(BaseModel):
    total_count: int
    items: List[ThreatFeedItem]

# ============================================================================
# 4. HEALTH SCHEMAS
# ============================================================================

class HealthResponse(BaseModel):
    status: str
    project: str
    version: str
    ai_engine_status: str
    model_loaded: bool
    ml_confidence_sample: float
    avg_inference_latency_ms: float
    p50_latency_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None
    p99_latency_ms: Optional[float] = None
    circuit_breaker_status: Optional[str] = "CLOSED_NORMAL"
    database_connected: bool
    timestamp: str

# ============================================================================
# 5. HYBRID AI COPILOT SCHEMAS
# ============================================================================

class CopilotChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")

class CopilotChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's query about the current scan")
    scan_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Current scan result payload to ground the response")
    history: Optional[List[CopilotChatMessage]] = Field(default_factory=list, description="Recent conversation turns")

class CopilotChatResponse(BaseModel):
    reply: str
    suggested_chips: List[str] = []
    engine_used: str
    latency_ms: float
    timestamp: str
