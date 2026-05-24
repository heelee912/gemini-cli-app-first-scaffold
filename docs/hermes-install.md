# Hermes Installation Notes

This repository can be used beside Hermes WebUI without modifying Hermes core.

## Option A: Install The Profile

Run:

```bash
python scripts/install_hermes_profile.py --hermes-home /path/to/.hermes-home --profile design --force
```

On Windows:

```powershell
python scripts\install_hermes_profile.py --hermes-home C:\path\to\.hermes-home --profile design --force
```

This copies `profile/` into:

```text
<hermes-home>/profiles/design/skills/build-parity-design-director
```

The important files are:

- `GEMINI.md`
- `SKILL.md`
- `design_skills/`
- `prompt-seeds/`
- `source-prompts/README.md`

## Option B: Use As An External Runner

Keep this repository separate and call its scripts from Hermes tasks:

```bash
python /path/to/gemini-build-parity-scaffold/scripts/run_gemini_design_once.py /path/to/artifact --name "Artifact" --brief-file /path/to/brief.md --force
```

This creates the scaffold, runs Gemini CLI inside the artifact folder, then runs
lint, build, and standalone packaging.

If Hermes already manages Gemini delegation itself, use the manual scaffold
command instead:

```bash
python /path/to/gemini-build-parity-scaffold/scripts/create_build_like_web_app.py /path/to/artifact --name "Artifact" --brief-file /path/to/brief.md --force
```

Then ensure the Gemini worker executes from `/path/to/artifact`, not from the
repository root.

## Browser Verification

For local artifacts, CDP screenshots are optional evidence helpers:

```bash
node /path/to/gemini-build-parity-scaffold/scripts/capture_chrome_cdp_fullpage.mjs "file:///absolute/path/to/standalone.html" /path/to/captures --settle-ms 5000
```

For logged-in real browser tabs, use your environment's official browser-control backend and follow its tab-claiming rules. Do not mix local preview verification with account-page automation.
