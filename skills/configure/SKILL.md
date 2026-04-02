---
name: configure
description: Edit TTS voice, event, and beep configuration
allowed-tools: ["Bash", "Read", "Edit"]
---

# Configure TTS Agent

Help the user customize their TTS agent settings.

## Steps

1. Read the current config:
   ```bash
   cd "${CLAUDE_PLUGIN_ROOT}" && cat tts-agent.yml
   ```

2. Ask the user what they want to change:
   - **Voice:** name, rate, volume (per platform)
   - **Events:** mode (sound/tts/both/none), beep, message
   - **Beeps:** add/edit named beep sequences

3. Edit `tts-agent.yml` with the requested changes.

4. Test the changes using the `/test` skill.
