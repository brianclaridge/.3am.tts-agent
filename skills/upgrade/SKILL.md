---
name: upgrade
description: Update the tts-agent plugin to the latest version
allowed-tools: ["Bash", "Read"]
---

# Upgrade TTS Agent

Update the .3am.tts-agent plugin to the latest version from GitHub.

## Steps

1. Determine the plugin root directory:
   - Use `${CLAUDE_PLUGIN_ROOT}` if set
   - Otherwise use `$CLAUDE_PROJECT_DIR/.claude/tts-agent`

2. Check current state:
   ```bash
   cd "<plugin-root>" && git status && git log --oneline -1
   ```

3. Fetch and show what's new:
   ```bash
   cd "<plugin-root>" && git fetch origin
   git log --oneline HEAD..origin/main
   ```

4. If there are updates, pull them:
   ```bash
   cd "<plugin-root>" && git pull --ff-only origin main
   ```

5. If `--ff-only` fails (local changes), report the conflict and suggest:
   - `git stash && git pull --ff-only origin main && git stash pop`
   - Or `git reset --hard origin/main` if user confirms

6. Show the new version:
   ```bash
   cd "<plugin-root>" && git log --oneline -1
   ```

7. If installed as a submodule, remind the user to commit the update in their parent project.
