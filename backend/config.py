import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ScamShield AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Supabase Credentials (optional in local offline mode)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://mock.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "mock-anon-key")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "mock-service-role-key")
    
    # Security & CORS (Hardened: No wildcard credentials)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "scamshield-super-secret-hmac-key-2026")
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
        ).split(",") if origin.strip()
    ]
    
    # Rate Limiting & Cooldown
    SCAN_COOLDOWN_SECONDS: float = 1.0
    MAX_SCANS_PER_MINUTE: int = 30
    
    # Hybrid AI Copilot Settings
    GROQ_API_KEY: Optional[str] = (
        os.getenv("GROQ_API_KEY") or
        os.getenv("GROQ_KEY") or
        os.getenv("GROQ_API_TOKEN") or
        os.getenv("groq_api_key") or
        os.getenv("GROQ_TOKEN")
    )
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    COPILOT_MODEL_GROQ: str = os.getenv("COPILOT_MODEL_GROQ", "qwen/qwen3.8-27b")
    COPILOT_MODEL_GEMINI: str = os.getenv("COPILOT_MODEL_GEMINI", "gemini-1.5-flash")

settings = Settings()
