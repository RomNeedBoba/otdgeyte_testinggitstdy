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

# 3. Security: Configure CORS
# In strict production, change "*" to your actual frontend domain (e.g., ["https://myfrontend.com"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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