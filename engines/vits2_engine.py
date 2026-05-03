import os
import re
import uuid
import time
import logging
from dataclasses import dataclass
import numpy as np
import soundfile as sf
import torch

from core.config import settings
from engines.base import BaseTTSEngine

# Assuming your utils and model imports are still available in the python path
from utils.task import load_checkpoint, load_vocab
from utils.hparams import get_hparams_from_file
from model.models import SynthesizerTrn
from text import tokenizer

logger = logging.getLogger(__name__)

@dataclass
class EngineMeta:
    sample_rate: int
    device: str
    model_name: str

class VITS2Engine(BaseTTSEngine):
    def __init__(self):
        self.model_name = settings.TTS_MODEL_NAME
        self.config_path = settings.TTS_CONFIG_PATH
        self.checkpoint_path = settings.TTS_CHECKPOINT_PATH
        self.vocab_path = settings.TTS_VOCAB_PATH
        self.device = settings.TTS_DEVICE

        self.hps = None
        self.symbols = None
        self.net_g = None
        self.meta = None

        self.noise_scale = settings.TTS_NOISE_SCALE
        self.noise_scale_w = settings.TTS_NOISE_SCALE_W
        self.length_scale = settings.TTS_LENGTH_SCALE

    def load(self):
        logger.info(f"Loading VITS2 Model: {self.model_name} on {self.device}")
        
        if self.device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA not available. Falling back to CPU. This will degrade performance.")
            self.device = "cpu"

        # Security: Ensure paths actually exist before loading to prevent unhandled OS errors
        for path in [self.config_path, self.vocab_path, self.checkpoint_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Critical configuration missing: {path}")

        self.hps = get_hparams_from_file(self.config_path)
        self.symbols = load_vocab(self.vocab_path)

        filter_length = self.hps.data.n_mels if self.hps.data.use_mel else self.hps.data.n_fft // 2 + 1
        segment_size = self.hps.train.segment_size // self.hps.data.hop_length

        self.net_g = SynthesizerTrn(len(self.symbols), filter_length, segment_size, **self.hps.model).to(self.device)
        self.net_g.eval()
        
        # Note on PyTorch Security: load_checkpoint relies on torch.load. 
        # In a fully zero-trust environment, ensure your .pth files are strictly internally sourced.
        _ = load_checkpoint(self.checkpoint_path, self.net_g, None)

        self.meta = EngineMeta(
            sample_rate=int(self.hps.data.sample_rate),
            device=self.device,
            model_name=self.model_name,
        )
        logger.info("VITS2 Model loaded successfully.")

    def _tokenize_ids(self, text: str):
        return tokenizer(text, self.symbols, cleaner_names=self.hps.data.text_cleaners, language=self.hps.data.language)

    def synthesize(self, text: str, audio_dir: str, base_url: str) -> dict:
        if self.net_g is None:
            raise RuntimeError("Engine not loaded before synthesis request.")

        # Defense in Depth: Enforce a strict maximum length (e.g., 500 chars) to prevent GPU OOM
        # We will also catch this in the API layer, but the engine must protect itself.
        MAX_CHARS = 1000
        if len(text) > MAX_CHARS:
            logger.error(f"Text exceeded maximum length of {MAX_CHARS} characters.")
            raise ValueError(f"Text too long. Maximum allowed is {MAX_CHARS} characters.")

        t0 = time.time()
        text_norm_ids = self._tokenize_ids(text)
        
        stn_tst = torch.LongTensor(text_norm_ids)
        x_tst = stn_tst.to(self.device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(self.device)

        with torch.inference_mode():
            out = self.net_g.infer(
                x_tst,
                x_tst_lengths,
                noise_scale=self.noise_scale,
                noise_scale_w=self.noise_scale_w,
                length_scale=self.length_scale,
            )
            audio = out[0][0, 0].data.detach().cpu().float().numpy()

        waveform = audio.astype(np.float32)

        # SECURITY: Path Traversal Protection
        # We enforce strict UUID generation so no user-provided input can alter the filename
        filename = f"{uuid.uuid4().hex}.wav"
        
        # Ensure the output directory exists
        os.makedirs(audio_dir, exist_ok=True)
        
        # Use abspath to strictly pin the file to the allowed directory
        safe_audio_dir = os.path.abspath(audio_dir)
        path = os.path.abspath(os.path.join(safe_audio_dir, filename))
        
        if not path.startswith(safe_audio_dir):
            # This should mathematically never happen with uuid, but is mandatory for high-security audits
            raise PermissionError("Path traversal attempt detected in audio synthesis.")

        # Save audio
        sf.write(path, waveform, self.meta.sample_rate, subtype="PCM_16")

        audio_url = f"{base_url.rstrip('/')}/audio/{filename}"

        return {
            "stage4_audio_url": audio_url,
            "meta": {
                "sample_rate": self.meta.sample_rate,
                "device": self.meta.device,
                "model_name": self.meta.model_name,
                "elapsed_ms": int((time.time() - t0) * 1000),
            }
        }