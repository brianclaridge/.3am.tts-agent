# .3am.tts-agent

Cross-platform TTS notifications and audio cues for all 25 Claude Code hook events.

> DISCLOSURE. This was created with the help of Claude Code.

## Install

### Option A: Git submodule (recommended)

```bash
git submodule add https://github.com/brianclaridge/.3am.tts-agent .claude/tts-agent
```

Hooks auto-register via `hooks/hooks.json` — no manual settings.json edits needed.

### Option B: Standalone clone

```bash
git clone https://github.com/brianclaridge/.3am.tts-agent /path/to/tts-agent
claude --plugin-dir /path/to/tts-agent
```

### Option C: GitHub marketplace

```bash
/plugin marketplace add brianclaridge/.3am.tts-agent
/plugin install tts-agent@3am.bot
```

## Configuration

Edit `tts-agent.yml` at the plugin root:

### Voice

Per-platform TTS settings — voice name, rate, volume:

```yaml
voice:
  windows:
    name: zira # or use voice_aliases
    rate: 0
    volume: 100
  macos:
    name: null
    rate: 200
  linux:
    rate: null
```

### Beeps

Named multi-tone sequences (frequency Hz, duration ms):

```yaml
beeps:
  chime:
    sequence: [[500, 80], [600, 60], [550, 90]]
```

### Events

Per-event mode (`sound`, `tts`, `both`, `none`), beep reference, message template:

```yaml
events:
  TaskCompleted:
    mode: both
    beep: bell
    message: "Task complete."
    template: "Completed: {task_subject}"
    template_field: task_subject
```

## Platforms

| Platform | Beeps             | TTS Engine            |
| -------- | ----------------- | --------------------- |
| Windows  | `winsound.Beep()` | SAPI COM via comtypes |
| macOS    | Terminal bell     | `say` command         |
| Linux    | `paplay`/`aplay`  | `espeak-ng`           |

## Test

```bash
echo '{"hook_event_name":"SessionStart","source":"startup","session_id":"test"}' | uv run src/notify.py
uv run src/sounds.py    # play all beep sequences
uv run src/tts.py       # speak a test phrase
```
