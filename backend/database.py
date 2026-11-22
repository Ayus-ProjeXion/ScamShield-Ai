import os
import uuid
import datetime
from typing import Dict, Any, List, Optional
from backend.config import settings

# Pre-seeded in-memory store mirroring database/seed.sql
INITIAL_IOCS = [
    {
        "id": "ioc-001",
        "ioc_type": "DOMAIN",
        "ioc_value": "sbi-kyc-verification-login.com",
        "severity": "CRITICAL",
        "category": "PHISHING_URL",
        "description": "Spoofed State Bank of India KYC phishing portal harvesting netbanking credentials",
        "confidence": 0.99,
        "is_blacklisted": True,
        "source": "ScamShield Threat Intel",
        "created_at": "2026-11-22T10:00:00Z"
    },
    {
        "id": "ioc-002",
        "ioc_type": "DOMAIN",
        "ioc_value": "hdfc-rewards-points-claim.xyz",
        "severity": "CRITICAL",
        "category": "PHISHING_URL",
        "description": "Malicious reward claim phishing landing page targeting HDFC cardholders",
        "confidence": 0.98,
        "is_blacklisted": True,
        "source": "ScamShield Threat Intel",
        "created_at": "2026-11-22T10:05:00Z"
    },
    {
        "id": "ioc-003",
        "ioc_type": "PHONE_NUMBER",
        "ioc_value": "+919876543210",
        "severity": "CRITICAL",
        "category": "SMISHING_SMS",
        "description": "High-volume smishing number dispatching fake electricity bill cutoff alerts",
        "confidence": 0.96,
        "is_blacklisted": True,
        "source": "National Cybercrime Feed",
        "created_at": "2026-11-22T10:10:00Z"
    },
    {
        "id": "ioc-004",
        "ioc_type": "UPI_VPA",
        "ioc_value": "custom.duty.clearance@ybl",
        "severity": "CRITICAL",
        "category": "UPI_PAYMENT_FRAUD",
        "description": "Extortion payment handle associated with fake customs parcel threats",
        "confidence": 0.99,
        "is_blacklisted": True,
        "source": "ScamShield Blacklist",
        "created_at": "2026-11-22T10:15:00Z"
    },
    {
        "id": "ioc-005",
        "ioc_type": "DOMAIN",
        "ioc_value": "onlinesbi.sbi",
        "severity": "SAFE",
        "category": "PHISHING_URL",
        "description": "Official State Bank of India netbanking domain",
        "confidence": 1.00,
        "is_blacklisted": False,
        "source": "Verified Whitelist",
        "created_at": "2026-11-22T10:20:00Z"
    }
]

INITIAL_REPORTS = [
    {
        "id": "rep-001",
        "ioc_value": "sbi-kyc-verification-login.com",
        "ioc_type": "DOMAIN",
        "category": "PHISHING_URL",
        "title": "Fake SBI Netbanking link sent via SMS",
        "description": "Received SMS claiming PAN card is expired and asking to log in here. The page steals OTP.",
        "evidence_url": "https://imgbb.com/sample-evidence-sbi",
        "upvote_count": 47,
        "status": "VERIFIED_SCAM",
        "created_at": "2026-11-22T11:00:00Z"
    },
    {
        "id": "rep-002",
        "ioc_value": "+919876543210",
        "ioc_type": "PHONE_NUMBER",
        "category": "SMISHING_SMS",
        "title": "Electricity Power Cutoff Threat Spammer",
        "description": "Sent mass messages to 5 of my family members claiming power will be cut at 9:30 PM.",
        "evidence_url": None,
        "upvote_count": 31,
        "status": "VERIFIED_SCAM",
        "created_at": "2026-11-22T11:30:00Z"
    },
    {
        "id": "rep-003",
        "ioc_value": "custom.duty.clearance@ybl",
        "ioc_type": "UPI_VPA",
        "category": "UPI_PAYMENT_FRAUD",
        "title": "Fake FedEx / Customs Clearance UPI Payment",
        "description": "Caller claiming they intercepted illegal drugs in my courier package and demanded Rs 5,000 clearance fee.",
        "evidence_url": None,
        "upvote_count": 64,
        "status": "VERIFIED_SCAM",
        "created_at": "2026-11-22T12:00:00Z"
    }
]

class DatabaseManager:
    """
    Asynchronous Database Abstraction Layer.
    Connects to live Supabase PostgreSQL when credentials are provided;
    smoothly falls back to high-performance in-memory storage for offline development.
    """
    def __init__(self):
        self.supabase = None
        self.is_connected = False
        self._init_client()
        
        # Local mock storage
        self.scans: Dict[str, Dict[str, Any]] = {}
        self.reports: List[Dict[str, Any]] = list(INITIAL_REPORTS)
        self.iocs: List[Dict[str, Any]] = list(INITIAL_IOCS)

    def _init_client(self):
        if settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock"):
            try:
                from supabase import create_client
                self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                self.is_connected = True
            except Exception:
                self.is_connected = False
        else:
            self.is_connected = False

    async def save_scan(self, scan_data: Dict[str, Any]) -> str:
        scan_id = scan_data.get("scan_id") or str(uuid.uuid4())
        scan_data["scan_id"] = scan_id
        scan_data["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # In-memory store
        self.scans[scan_id] = scan_data
        
        # If connected to live Supabase, persist asynchronously
        if self.is_connected and self.supabase:
            try:
                self.supabase.table("threat_scans").insert({
                    "id": scan_id,
                    "channel": scan_data.get("channel", "SMS"),
                    "raw_payload": scan_data.get("text_preview", ""),
                    "created_at": scan_data["created_at"]
                }).execute()
            except Exception:
                pass
                
        return scan_id

    async def get_scan(self, scan_id: str) -> Optional[Dict[str, Any]]:
        if scan_id in self.scans:
            return self.scans[scan_id]
            
        if self.is_connected and self.supabase:
            try:
                res = self.supabase.table("threat_scans").select("*").eq("id", scan_id).execute()
                if res.data:
                    return res.data[0]
            except Exception:
                pass
        return None

    async def save_report(self, report_dict: Dict[str, Any]) -> Dict[str, Any]:
        rep_id = str(uuid.uuid4())
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record = {
            "id": rep_id,
            "ioc_value": report_dict["ioc_value"],
            "ioc_type": report_dict.get("ioc_type", "PHONE_NUMBER"),
            "category": report_dict.get("category", "IMPERSONATION"),
            "title": report_dict["title"],
            "description": report_dict["description"],
            "evidence_url": report_dict.get("evidence_url"),
            "upvote_count": 1,
            "status": "PENDING",
            "created_at": now_str,
            "message": "Report submitted successfully to ScamShield Community Intelligence"
        }
        self.reports.insert(0, record)
        
        # Live Supabase sync
        if self.is_connected and self.supabase:
            try:
                self.supabase.table("community_reports").insert(record).execute()
            except Exception:
                pass
                
        return record

    async def get_reports(self, limit: int = 50) -> List[Dict[str, Any]]:
        if self.is_connected and self.supabase:
            try:
                res = self.supabase.table("community_reports").select("*").order("created_at", desc=True).limit(limit).execute()
                if res.data:
                    return res.data
            except Exception:
                pass
        return self.reports[:limit]

    async def get_threat_feed(self, limit: int = 50, category: Optional[str] = None) -> List[Dict[str, Any]]:
        items = self.iocs
        if category:
            items = [i for i in items if i.get("category") == category]
            
        if self.is_connected and self.supabase:
            try:
                q = self.supabase.table("threat_iocs").select("*").order("created_at", desc=True).limit(limit)
                if category:
                    q = q.eq("category", category)
                res = q.execute()
                if res.data:
                    return res.data
            except Exception:
                pass
        return items[:limit]

db = DatabaseManager()
