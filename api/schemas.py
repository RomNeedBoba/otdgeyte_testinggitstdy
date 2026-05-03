from pydantic import BaseModel, Field
from typing import Optional, Dict

class TTSRequest(BaseModel):
    # SECURITY: Hard limit the length to prevent OOM attacks (e.g., max 500 chars)
    # Strip whitespace to prevent users bypassing validation with spaces
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="The text to synthesize. Maximum 500 characters."
    )
    
    # Optional field for future multi-speaker support
    speaker_id: int = Field(
        default=0, 
        ge=0, 
        description="ID of the speaker to use."
    )

class TaskResponse(BaseModel):
    status: str
    task_id: str
    message: str

class StatusResponse(BaseModel):
    status: str
    data: Optional[Dict] = None
    error: Optional[str] = None