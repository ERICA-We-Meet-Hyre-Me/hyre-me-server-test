from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env at repository root.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")


settings = Settings()
