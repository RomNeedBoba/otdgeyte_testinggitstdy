# worker.py
from celery import Celery
import os
from tts_singleton import get_tts_singleton

# Initialize Celery connected to local Redis
celery_app = Celery(
    "tts_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Load the model into the worker's memory
tts = get_tts_singleton()

@celery_app.task(name="generate_audio_task")
def generate_audio_task(text: str, audio_dir: str, base_url: str):
    """
    This runs in the background queue, preventing FastAPI from blocking!
    """
    print(f"Worker picking up task for text: {text}")
    
    # Run the actual synthesis
    result = tts.synthesize(text=text, audio_dir=audio_dir, base_url=base_url)
    
    return result