---
name: test
description: Test TTS voice and beep sounds
allowed-tools: ["Bash", "Read"]
---

# Test TTS

Test the text-to-speech engine and beep sounds.

## Steps

1. Test a full hook event (beep + speech):
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}" && echo '{"hook_event_name":"SessionStart","source":"startup","session_id":"test"}' | uv run src/notify.py
   ```

2. Test each named beep sound:
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}" && uv run src/sounds.py
   ```

3. Test direct speech:
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}" && uv run src/tts.py
   ```

4. Report which tests passed and any errors.
