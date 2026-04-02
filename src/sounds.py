"""Beep module — winsound on Windows, terminal bell elsewhere."""
from __future__ import annotations

import platform
import sys


def play(params: tuple[int, int] | list[tuple[int, int]] | None) -> None:
    if params is None:
        return
    if isinstance(params, list):
        for freq, dur in params:
            _beep(freq, dur)
    else:
        _beep(*params)


def _beep(frequency: int, duration: int) -> None:
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(frequency, duration)
    else:
        print("\a", end="", flush=True, file=sys.stderr)


if __name__ == "__main__":
    from config import CONFIG, resolve_beep

    beeps = CONFIG.get("beeps", {})
    for name in beeps:
        params = resolve_beep(name)
        label = f"sequence ({len(params)} tones)" if isinstance(params, list) else f"{params[0]}Hz for {params[1]}ms"
        print(f"Playing '{name}': {label}")
        play(params)
