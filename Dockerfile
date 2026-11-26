# ==============================================================================
# ScamShield AI — Multi-Stage Production Container
# ==============================================================================

FROM python:3.12-slim AS base

# Install OS audio and networking dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    flac \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifest and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY ai/ /app/ai/
COPY backend/ /app/backend/
COPY database/ /app/database/
COPY verify_supabase.py /app/
COPY test_security_deep_audit.py /app/

# Create non-root security user
RUN useradd -m -u 1001 scamshield && \
    chown -R scamshield:scamshield /app

USER scamshield

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
