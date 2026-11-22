import os
from typing import List
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
    
    # Security & CORS
    SECRET_KEY: str = os.getenv("SECRET_KEY", "scamshield-super-secret-hmac-key-2026")
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]
    
    # Rate Limiting & Cooldown
    SCAN_COOLDOWN_SECONDS: float = 1.0
    MAX_SCANS_PER_MINUTE: int = 30

settings = Settings()
