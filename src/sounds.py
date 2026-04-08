"""Beep module — winsound on Windows, synthesized WAV via paplay/aplay on Linux."""
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
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.Beep(frequency, duration)
    elif system == "Linux":
        _beep_linux(frequency, duration)
    else:
        print("\a", end="", flush=True, file=sys.stderr)


def _beep_linux(frequency: int, duration: int) -> None:
    import io
    import math
    import struct
    import subprocess
    import wave

    sample_rate = 22050
    num_samples = int(sample_rate * duration / 1000)
    fade_samples = max(1, int(sample_rate * 0.003))  # 3ms fade to avoid clicks

    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            fade = min(1.0, i / fade_samples, (num_samples - i) / fade_samples)
            val = int(32767 * 0.5 * fade * math.sin(2 * math.pi * frequency * i / sample_rate))
            frames.extend(struct.pack("<h", val))
        w.writeframes(bytes(frames))

    wav_bytes = buf.getvalue()
    for cmd in (["paplay"], ["aplay", "-q"]):
        try:
            subprocess.run(cmd, input=wav_bytes, capture_output=True, timeout=10)
            return
        except FileNotFoundError:
            continue
    print("sounds: no player found (tried paplay, aplay)", file=sys.stderr)


if __name__ == "__main__":
    from config import CONFIG, resolve_beep

    beeps = CONFIG.get("beeps", {})
    for name in beeps:
        params = resolve_beep(name)
        label = f"sequence ({len(params)} tones)" if isinstance(params, list) else f"{params[0]}Hz for {params[1]}ms"
        print(f"Playing '{name}': {label}")
        play(params)
