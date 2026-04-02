# .3am.tts-agent

Cross-platform TTS notifications and audio cues for all 25 Claude Code hook events. Part of the 3am plugin suite.

## Architecture

```
src/
  notify.py      # Entry point: stdin JSON -> event config -> beep/speak
  config.py      # YAML config loader (tts-agent.yml at repo root)
  sounds.py      # Beep module (winsound on Windows, terminal bell elsewhere)
  tts.py         # Cross-platform TTS (SAPI COM, say, spd-say/espeak)
  resolve.py     # Path resolution utility
  log_config.py  # Loguru logger setup
```

## How it works

1. Claude Code fires a hook event
2. `notify.py` reads JSON from stdin
3. Resolves event config via variant matching from `tts-agent.yml`
4. Plays beep (if mode includes `sound`)
5. Speaks message (if mode includes `tts`)
6. Logs to `.data/logs/`

## Config

`tts-agent.yml` at repo root. Sections: `voice`, `voice_aliases`, `beeps`, `events`.

## Test

```bash
echo '{"hook_event_name":"SessionStart","source":"startup","session_id":"test"}' | uv run src/notify.py
uv run src/sounds.py
uv run src/tts.py
```
