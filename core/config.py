import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

class Settings:
    # API Config
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    
    # Redis Config
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Model Config
    TTS_MODEL_NAME = os.getenv("TTS_MODEL_NAME", "khmer_base_fe")
    TTS_CONFIG_PATH = os.getenv("TTS_CONFIG_PATH", "assets/configs/config.yaml")
    TTS_VOCAB_PATH = os.getenv("TTS_VOCAB_PATH", "assets/vocabs/vocab.txt")
    TTS_CHECKPOINT_PATH = os.getenv("TTS_CHECKPOINT_PATH", "assets/checkpoints/G_207000.pth")
    TTS_DEVICE = os.getenv("TTS_DEVICE", "cuda")
    
    # Audio Settings
    TTS_NOISE_SCALE = float(os.getenv("TTS_NOISE_SCALE", "0.667"))
    TTS_NOISE_SCALE_W = float(os.getenv("TTS_NOISE_SCALE_W", "0.8"))
    TTS_LENGTH_SCALE = float(os.getenv("TTS_LENGTH_SCALE", "1.0"))
        
    # Storage
    AUDIO_DIR = os.getenv("AUDIO_DIR", "storage/generated_audio")

# Create a global settings object to use everywhere
settings = Settings()