# Gemini CLI App-First Scaffold

Runnable app-first scaffolding for pushing Gemini CLI and Hermes design workers toward AI Studio Build-like frontend artifacts.

It gives the model a better working medium: a real Vite app, local design instructions, optional source-prompt slots, craft notes, and a packaging route from app source to standalone HTML.

## Languages

- English
- [한국어](docs/README.ko.md)
- [日本語](docs/README.ja.md)
- [中文](docs/README.zh-CN.md)

## What Changes

Plain CLI prompting often collapses into one static HTML file. This repository makes the worker operate inside a real frontend project first, then exports the result only after the app exists.

All outputs in this table are one-shot results from the same public-safe brief.

| Route | One-shot public-safe output |
| --- | --- |
| Vanilla simple instruction v1 | <img src="evidence/baseline-1818/desktop-fullpage.png" alt="Vanilla simple instruction v1 one-shot output" width="520"> |
| Vanilla simple instruction v2 | <img src="evidence/baseline-1848/desktop-fullpage.png" alt="Vanilla simple instruction v2 one-shot output" width="520"> |
| App-first scaffold 0003 | <img src="evidence/final-0003/desktop-fullpage.png" alt="App-first scaffold 0003 one-shot output" width="520"> |

### 0003 Interaction Proof

The final artifact is not just a static page. Controls change the whole view context and expose different app states.

<img src="evidence/final-0003/interaction-demo.gif" alt="0003 interaction demo" width="900">

All images use fictional content. They document the practical effect of the workflow.

## Quick Start For Gemini CLI

```powershell
git clone https://github.com/heelee912/gemini-cli-app-first-scaffold.git
cd gemini-cli-app-first-scaffold
python scripts\run_gemini_design_once.py out\fictional-profile --name "Fictional Profile" --brief-file examples\fictional-recruiter-profile\brief.md --force
```

The runner does this:

1. Creates a Vite + React + TypeScript + Tailwind workspace.
2. Copies `profile/GEMINI.md`, `profile/SKILL.md`, `design_skills/`, `prompt-seeds/`, and `source-prompts/` into that workspace.
3. Writes the user brief into `task.md`.
4. Runs Gemini CLI from inside the generated workspace so Gemini can read the scaffold files directly.
5. Runs `npm install`, `npm run lint`, and `npm run build`.
6. Packages Vite `dist` into `standalone.html`.

Expected result:

```text
out\fictional-profile\standalone.html
```

## Manual Agent Route

If your agent already controls Gemini, create only the scaffold:

```powershell
python scripts\create_build_like_web_app.py out\my-artifact --name "My Artifact" --brief-file brief.md --force
```

Then run the design worker from `out\my-artifact`, not from the repository root. The worker should read:

```text
GEMINI.md
task.md
BUILD_ENVIRONMENT.md
AIS_REFERENCE_COMMONS.md
design_skills/
prompt-seeds/
source-prompts/
src/
```

After the worker edits the app:

```powershell
cd out\my-artifact
npm install
npm run lint
npm run build
cd ..\..
python scripts\package_vite_dist_single_html.py out\my-artifact\dist out\my-artifact\standalone.html
```

## Hermes Setup

Install the design profile into a Hermes home:

```powershell
python scripts\install_hermes_profile.py --hermes-home C:\path\to\.hermes-home --profile design --force
```

It copies this repository's profile into:

```text
<hermes-home>\profiles\design\skills\app-first-design-director
```

Then a Hermes main agent can use the profile in either of these ways:

```text
Use the app-first-design-director profile.
Create an artifact workspace with run_gemini_design_once.py.
Run the Gemini design worker inside that artifact workspace.
Return the runnable source path and standalone.html path.
```

or:

```text
Use create_build_like_web_app.py first.
Delegate to Gemini from inside the generated workspace.
After Gemini edits the app, run npm install, npm run lint, npm run build, and package_vite_dist_single_html.py.
```

Hermes does not need a fork of its core for this repository. The integration point is a profile plus an external runner.

## What Gemini Sees

Every generated artifact is intentionally self-describing:

```text
artifact/
  GEMINI.md
  SKILL.md
  task.md
  BUILD_ENVIRONMENT.md
  AIS_REFERENCE_COMMONS.md
  design_skills/
  prompt-seeds/
  source-prompts/
  package.json
  vite.config.ts
  tsconfig.json
  index.html
  src/
    App.tsx
    data.ts
    types.ts
    index.css
    components/
      README.md
```

The important point is execution context. Gemini is not merely given a prompt. It is placed inside an app workspace that already explains the expected medium, available dependencies, mobile requirements, packaging route, and optional source context.

## Optional Source Prompts

Raw AI Studio prompt files are not redistributed here. If you have prompt files that you may legally use, place them in:

```text
profile\source-prompts\
```

The scaffold copies that folder into every generated artifact so Gemini can read it locally.

## Repository Contents

| Path | Purpose |
| --- | --- |
| `profile/GEMINI.md` | Design-worker execution kernel. It tells Gemini to build app-first and own the visual direction. |
| `profile/SKILL.md` | Skill wrapper for Hermes or other agent systems. |
| `profile/design_skills/` | Supplemental craft notes copied into every generated artifact. |
| `profile/prompt-seeds/` | General high-performing prompt drivers with task content removed. |
| `profile/source-prompts/README.md` | Placeholder for optional source prompt corpus that is not redistributed here. |
| `scripts/run_gemini_design_once.py` | End-to-end scaffold, Gemini CLI run, install, lint, build, and standalone HTML package route. |
| `scripts/create_build_like_web_app.py` | Creates only the Vite/React/Tailwind scaffold. Use this when another agent controls Gemini. |
| `scripts/install_hermes_profile.py` | Installs the profile into a Hermes home. |
| `scripts/package_vite_dist_single_html.py` | Inlines Vite `dist` assets into one browser-openable HTML file. |
| `examples/fictional-recruiter-profile/` | Public-safe example brief. |
| `evidence/` | Fictional screenshots and interaction GIF documenting the workflow. |

## Related Work

This repository follows the broader idea of scaffolding: surround the model with workspace structure, tools, instructions, state, and execution feedback instead of relying on a single prompt.

- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](https://arxiv.org/abs/2604.03515)
- [app.build: A Production Framework for Scaling Agentic Prompt-to-App Generation with Environment Scaffolding](https://arxiv.org/abs/2509.03310)
- [BISCUIT: Scaffolding LLM-Generated Code with Ephemeral UIs in Computational Notebooks](https://machinelearning.apple.com/research/biscuit-scaffolding-llm)
- [TableTalk: Scaffolding Spreadsheet Development with a Language Agent](https://www.microsoft.com/en-us/research/publication/tabletalk-scaffolding-spreadsheet-development-with-a-language-agent/)

## Publication Boundary

This public package deliberately excludes:

- Personal career data.
- Account names, OAuth state, cookies, API keys, tokens, or local auth folders.
- Company-internal facts or confidential implementation details.
- Raw external prompt corpora whose redistribution rights are unclear or incompatible.
- Copied browser-extension backends or native messaging code.

## License

MIT. See `LICENSE`.
