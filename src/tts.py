"""Cross-platform TTS — SAPI COM (Windows), say (macOS), spd-say/espeak (Linux)."""
from __future__ import annotations

import platform
import subprocess
import sys


def speak(text: str, *, detach: bool = False, voice_name: str | None = None) -> None:
    os_name = platform.system()
    if os_name == "Windows":
        _speak_windows(text, detach=detach, voice_name=voice_name)
    elif os_name == "Darwin":
        _speak_macos(text, detach=detach)
    elif os_name == "Linux":
        _speak_linux(text, detach=detach)
    else:
        print(f"tts: unsupported OS {os_name!r}", file=sys.stderr)


def _speak_windows(text: str, *, detach: bool = False, voice_name: str | None = None) -> None:
    try:
        import comtypes.client  # type: ignore[import-untyped]
    except ImportError:
        print("tts: comtypes not installed, falling back to PowerShell", file=sys.stderr)
        _speak_windows_fallback(text, detach=detach)
        return

    from config import get_voice_config, resolve_voice_name
    cfg = get_voice_config().get("windows", {})

    engine = comtypes.client.CreateObject("SAPI.SpVoice")

    effective_voice = resolve_voice_name(voice_name) or resolve_voice_name(cfg.get("name"))
    if effective_voice:
        voices = engine.GetVoices()
        for i in range(voices.Count):
            if effective_voice.lower() in voices.Item(i).GetDescription().lower():
                engine.Voice = voices.Item(i)
                break

    if cfg.get("rate") is not None:
        engine.Rate = cfg["rate"]
    if cfg.get("volume") is not None:
        engine.Volume = cfg["volume"]

    engine.Speak(text, 1 if detach else 0)


def _speak_windows_fallback(text: str, *, detach: bool = False) -> None:
    safe = text.replace('"', '`"')
    ps_script = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f'$synth.Speak("{safe}")'
    )
    cmd = ["powershell", "-NoProfile", "-Command", ps_script]
    if detach:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0x00000200 | 0x00000008,
        )
    else:
        subprocess.run(cmd, capture_output=True, timeout=30)


def _speak_macos(text: str, *, detach: bool = False) -> None:
    from config import get_voice_config
    cfg = get_voice_config().get("macos", {})

    cmd = ["say"]
    if cfg.get("name"):
        cmd.extend(["-v", cfg["name"]])
    if cfg.get("rate"):
        cmd.extend(["-r", str(cfg["rate"])])
    cmd.append(text)

    if detach:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    else:
        subprocess.run(cmd, capture_output=True, timeout=30)


def _speak_linux(text: str, *, detach: bool = False) -> None:
    from config import get_voice_config
    cfg = get_voice_config().get("linux", {})
    rate = cfg.get("rate")

    commands = [["spd-say", text], ["espeak", text]]
    if rate:
        commands = [["spd-say", "-r", str(rate), text], ["espeak", "-s", str(rate), text]]

    for cmd in commands:
        try:
            if detach:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            else:
                subprocess.run(cmd, capture_output=True, timeout=30)
            return
        except FileNotFoundError:
            continue
    print("tts: no engine found (tried spd-say, espeak)", file=sys.stderr)


if __name__ == "__main__":
    speak("TTS test: alerts are working")
