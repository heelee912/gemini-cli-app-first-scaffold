# Hermes Installation Notes

This repository can be used beside Hermes WebUI without modifying Hermes core.

## Install The Profile

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
<hermes-home>/profiles/design/skills/app-first-design-director
```

The important files are:

- `GEMINI.md`
- `SKILL.md`
- `design_skills/`
- `prompt-seeds/`
- `source-prompts/README.md`

## Use As An External Runner

Keep this repository separate and call its scripts from Hermes tasks:

```bash
python /path/to/gemini-cli-app-first-scaffold/scripts/run_gemini_design_once.py /path/to/artifact --name "Artifact" --brief-file /path/to/brief.md --force
```

This creates the scaffold, runs Gemini CLI inside the artifact folder, then runs
lint, build, and standalone packaging.

If Hermes already manages Gemini delegation itself, use the manual scaffold
command instead:

```bash
python /path/to/gemini-cli-app-first-scaffold/scripts/create_build_like_web_app.py /path/to/artifact --name "Artifact" --brief-file /path/to/brief.md --force
```

Then ensure the Gemini worker executes from `/path/to/artifact`, not from the
repository root.

## Suggested Hermes Main-Agent Instruction

Use this shape when delegating a visual web artifact:

```text
Use the app-first-design-director profile.
Create the artifact workspace with run_gemini_design_once.py.
Run Gemini from inside the generated artifact workspace.
Do not ask Gemini to answer with a single HTML file first.
After the app is edited, return the runnable source path and standalone.html path.
```

This repository provides the profile and runner. Hermes remains responsible for
goal orchestration, task tracking, and deciding when to call the runner.

## Browser Use

This repository does not ship a browser-control backend. Use the browser tools
already available in your agent environment to open the generated
`standalone.html` or Vite preview.

For logged-in real browser tabs, use your environment's official browser-control
backend and follow its tab-claiming rules. Do not mix local preview checks with
account-page automation.
