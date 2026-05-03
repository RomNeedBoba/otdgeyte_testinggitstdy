import logging
from celery import Celery
from core.config import settings

# Setup logging for the worker
logger = logging.getLogger(__name__)

# Initialize Celery using settings from .env
celery_app = Celery(
    "vits2_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Important: Load the model engine ONCE per worker process.
# We do this at the top level so it's loaded into VRAM when the worker boots.
try:
    from engines.manager import model_manager
    tts_engine = model_manager.get_engine()
except Exception as e:
    logger.critical(f"FATAL: Worker failed to load TTS Engine: {e}")
    # We do NOT exit here, Celery handles worker process deaths, 
    # but the logs will scream that the model failed to load.
    tts_engine = None

@celery_app.task(name="tasks.generate_audio_task", bind=True, max_retries=0)
def generate_audio_task(self, text: str, audio_dir: str, base_url: str):
    """
    Secure background task for audio generation.
    - max_retries=0: If VITS2 crashes on a text, do NOT retry. It will just OOM again.
    """
    if tts_engine is None:
        logger.error("Attempted to synthesize, but engine is not loaded.")
        raise RuntimeError("TTS Engine is offline.")

    logger.info(f"Worker processing task {self.request.id} for text length: {len(text)}")
    
    try:
        # Run the heavy synthesis securely
        result = tts_engine.synthesize(text=text, audio_dir=audio_dir, base_url=base_url)
        
        logger.info(f"Task {self.request.id} completed successfully.")
        return result
        
    except ValueError as ve:
        # Catch our custom validation errors (like text too long)
        logger.error(f"Validation error in worker for task {self.request.id}: {ve}")
        raise
        
    except Exception as e:
        # Catch all other errors (CUDA out of memory, PyTorch errors)
        logger.error(f"Critical failure in worker for task {self.request.id}: {str(e)}")
        # We re-raise the error so Celery marks the task as FAILED in Redis
        raise