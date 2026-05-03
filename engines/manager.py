import logging
from engines.vits2_engine import VITS2Engine

logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None
    _engine = None

    def __new__(cls):
        """Strict Singleton to prevent memory leaks from multiple model instances."""
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def get_engine(self) -> VITS2Engine:
        if self._engine is None:
            logger.info("Initializing TTS Engine for the first time...")
            self._engine = VITS2Engine()
            self._engine.load()
        return self._engine

# Export a single secure instance
model_manager = ModelManager()