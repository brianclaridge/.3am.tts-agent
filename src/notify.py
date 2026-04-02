"""Single dispatcher for all hook events."""
from __future__ import annotations

import json
import sys

from loguru import logger

from config import get_event_config, resolve_beep
from log_config import configure_logger
from sounds import play
from tts import speak


def _resolve_message(cfg: dict, payload: dict) -> str | None:
    template_field = cfg.get("template_field")
    template = cfg.get("template")
    if template_field and template:
        value = payload.get(template_field, "")
        if value:
            return template.format(**{template_field: value})
    return cfg.get("message")


def main() -> None:
    raw = sys.stdin.read()

    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        payload = {}

    event = payload.get("hook_event_name", "")
    cfg = get_event_config(event, payload)
    if not cfg:
        return

    session_id = payload.get("session_id", "unknown")
    configure_logger(session_id)

    if cfg.get("skip_on_interrupt") and payload.get("is_interrupt"):
        logger.info("{}: skipped (interrupt)", event)
        return

    mode = cfg.get("mode", "sound")
    if mode == "none":
        return

    msg = _resolve_message(cfg, payload)
    detach = cfg.get("detach", False)

    if mode in ("sound", "both"):
        play(resolve_beep(cfg.get("beep")))
    if mode in ("tts", "both") and msg:
        speak(msg, detach=detach, voice_name=cfg.get("voice"))

    logger.info("{}: {} | mode={}", event, msg, mode)


if __name__ == "__main__":
    main()
