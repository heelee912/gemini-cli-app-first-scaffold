# Hermes Installation Notes

This repository can be used beside Hermes WebUI without modifying Hermes core.

## Option A: Use As A Reference Skill

Copy the `profile/` folder into your Hermes skill or profile area and name it `build-parity-design-director`.

The important files are:

- `GEMINI.md`
- `SKILL.md`
- `design_skills/`
- `prompt-seeds/`
- `source-prompts/README.md`

## Option B: Use As An External Scaffold

Keep this repository separate and call its scripts from Hermes tasks:

```bash
python /path/to/gemini-build-parity-scaffold/scripts/create_build_like_web_app.py /path/to/artifact --name "Artifact" --brief-file /path/to/brief.md --force
```

Then ask the design worker to operate inside the generated artifact folder.

## Browser Verification

For local artifacts, use CDP screenshots:

```bash
node /path/to/gemini-build-parity-scaffold/scripts/capture_chrome_cdp_fullpage.mjs "file:///absolute/path/to/standalone.html" /path/to/captures --settle-ms 5000
```

For logged-in real browser tabs, use your environment's official browser-control backend and follow its tab-claiming rules. Do not mix local preview verification with account-page automation.
