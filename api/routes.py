import logging
from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult

from api.schemas import TTSRequest, TaskResponse, StatusResponse
from api.security import verify_api_key
from tasks.audio_tasks import generate_audio_task
from core.config import settings

logger = logging.getLogger(__name__)

# Create a router to group our endpoints cleanly
router = APIRouter()

@router.post("/generate", response_model=TaskResponse, tags=["TTS"])
async def generate_audio(
    request: TTSRequest, 
    api_key: str = Depends(verify_api_key) # SECURITY: This endpoint is now locked down
):
    try:
        # Send job to Celery queue
        task = generate_audio_task.delay(request.text, settings.AUDIO_DIR, settings.BASE_URL)
        
        logger.info(f"Task {task.id} created for text length {len(request.text)}.")
        
        return TaskResponse(
            status="queued",
            task_id=task.id,
            message="Your audio is in the queue."
        )
    except Exception as e:
        # SECURITY: Log the real error for us, but return a generic 500 to the user.
        # This prevents leaking internal paths or library versions.
        logger.error(f"Failed to enqueue task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during task creation.")

@router.get("/status/{task_id}", response_model=StatusResponse, tags=["TTS"])
async def get_task_status(
    task_id: str,
    api_key: str = Depends(verify_api_key) # Security on the status check too
):
    try:
        task_result = AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            return StatusResponse(status="processing")
            
        elif task_result.state == 'SUCCESS':
            return StatusResponse(status="completed", data=task_result.result)
            
        elif task_result.state == 'FAILURE':
            # Log the full traceback internally
            logger.error(f"Task {task_id} failed: {str(task_result.info)}")
            # Return a safe error to the client
            return StatusResponse(status="failed", error="Audio generation failed.")
            
        else:
            return StatusResponse(status=task_result.state)
            
    except Exception as e:
        logger.error(f"Status check failed for {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve task status.")