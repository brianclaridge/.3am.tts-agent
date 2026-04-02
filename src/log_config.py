"""Logger configuration for tts-agent."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

from config import CONFIG

_PLUGIN_DIR = Path(__file__).resolve().parent.parent


def configure_logger(session_id: str) -> None:
    logger.remove()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H")
    log_path = _PLUGIN_DIR / CONFIG["log_path"].format(
        session_id=session_id, stamp=stamp,
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.add(log_path, format=CONFIG["log_format"])
