from abc import ABC, abstractmethod

class BaseTTSEngine(ABC):
    """
    Abstract Base Class for all TTS Engines.
    Ensures a unified, secure interface for any model added in the future.
    """
    
    @abstractmethod
    def load(self) -> None:
        """Loads the model into memory securely."""
        pass

    @abstractmethod
    def synthesize(self, text: str, audio_dir: str, base_url: str) -> dict:
        """
        Synthesizes text to audio.
        Must return a standardized dictionary containing the secure audio URL.
        """
        pass    