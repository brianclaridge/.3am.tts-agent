"""Configuration loader for tts-agent."""
from __future__ import annotations

from pathlib import Path

import yaml

_PLUGIN_DIR = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _PLUGIN_DIR / "tts-agent.yml"
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is not None:
        return _cache
    with open(_CONFIG_PATH) as f:
        _cache = yaml.safe_load(f)
    return _cache


CONFIG = _load()


def get_event(event: str) -> dict:
    return CONFIG.get("events", {}).get(event, {})


def get_event_config(event: str, payload: dict) -> dict:
    base = get_event(event)
    if not base:
        return {}

    variant_key = base.get("variant_key")
    if variant_key:
        variant_value = payload.get(variant_key, "")
        variants = base.get("variants", {})
        variant_cfg = variants.get(variant_value)

        if variant_cfg:
            return {**base, **variant_cfg}
        default_cfg = base.get("default")
        if default_cfg:
            return {**base, **default_cfg}

    return base


def resolve_beep(beep_ref: list | str | None) -> tuple[int, int] | list[tuple[int, int]] | None:
    if beep_ref is None:
        return None

    if isinstance(beep_ref, list) and len(beep_ref) == 2 and isinstance(beep_ref[0], int):
        return (beep_ref[0], beep_ref[1])

    if isinstance(beep_ref, str):
        beep = CONFIG.get("beeps", {}).get(beep_ref)
        if not beep:
            return None
        if "sequence" in beep:
            return [(f, d) for f, d in beep["sequence"]]
        return (beep["frequency"], beep["duration"])

    return None


def get_voice_config() -> dict:
    return CONFIG.get("voice", {})


def resolve_voice_name(name: str | None) -> str | None:
    if not name:
        return None
    aliases = CONFIG.get("voice_aliases", {})
    return aliases.get(name, name)
