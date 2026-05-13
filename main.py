import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logger import setup_logger
from api.routes import router as api_router

# 1. Initialize secure logging
logger = setup_logger()
logger.info("Starting VITS2 Production API...")

# 2. Initialize FastAPI app
app = FastAPI(
    title="VITS2 High-Security API",
    description="Scalable, asynchronous backend for TTS inference.",
    version="1.0.0",
    docs_url="/docs",  # You can set this to None in strict production to hide docs
    redoc_url=None
)

# 3. Security: Configure CORS - RESTRICTED to authorized origins only
# ============================================
# IMPORTANT: Update these origins for your deployment
# Local Development: http://localhost:5173
# Production (Vercel): https://ethan-alpha.vercel.app
# ============================================

allowed_origins = [
    "https://ethan-alpha.vercel.app",  # Production
    "http://localhost:5173",            # Local development (Vite default)
    "http://localhost:3000",            # Alternative local port
]

# Optional: Read from environment variable for flexibility
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    allowed_origins = [origin.strip() for origin in allowed_origins]

logger.info(f"✅ CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,      # ✅ Only specified origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],      # ✅ Only GET and POST
    allow_headers=[
        "Content-Type",
        "x-api-key",
        "Authorization"
    ],                                   # ✅ Only required headers
    max_age=86400,                       # Cache preflight requests for 24 hours
)

# 4. Ensure Audio Storage Exists and Serve It
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")

# 5. Include our secure API routes
app.include_router(api_router)

@app.get("/", tags=["Health"])
def health_check():
    """Simple health check endpoint that does not require an API key."""
    return {"status": "healthy", "service": "VITS2 TTS API"}
