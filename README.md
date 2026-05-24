# Gemini Build Parity Scaffold

Local scaffold and instruction kernel for pushing Gemini CLI or Hermes design workers toward AI Studio Build-like frontend output.

This repository is not a fork of Hermes WebUI and is not affiliated with Google AI Studio. It is a standalone workflow package: create an app-first Vite/React/Tailwind workspace, give the design model a Build-like execution context, verify real browser rendering, then optionally package the built app into a direct-open single HTML file.

## Multilingual Overview

### English

This project turns a plain Gemini CLI design request into an app-first workflow. It creates a Vite, React, TypeScript, and Tailwind workspace, places the design kernel and scaffold context where Gemini can read them, runs Gemini inside that workspace, then builds and optionally packages the result as standalone HTML.

### 한국어

이 프로젝트는 Gemini CLI 디자인 요청을 단순 HTML 생성이 아니라 앱 우선 워크플로로 바꿉니다. Vite, React, TypeScript, Tailwind 작업 공간을 만들고, Gemini가 읽을 수 있는 위치에 디자인 커널과 스캐폴드 문맥을 배치한 뒤, 그 작업 공간 안에서 Gemini를 실행하고 빌드 및 단일 HTML 패키징까지 진행합니다.

### 日本語

このプロジェクトは、Gemini CLI へのデザイン依頼を単なる HTML 生成ではなく、アプリ優先のワークフローに変換します。Vite、React、TypeScript、Tailwind の作業環境を作成し、Gemini が読める場所にデザインカーネルとスキャフォールド文脈を配置し、その作業環境内で Gemini を実行して、ビルドと必要に応じた単一 HTML へのパッケージ化を行います。

### 中文

本项目把 Gemini CLI 的设计请求从简单的 HTML 生成提升为应用优先的工作流。它会创建 Vite、React、TypeScript 和 Tailwind 工作区，把设计内核和脚手架上下文放到 Gemini 可以读取的位置，然后在该工作区内运行 Gemini，完成构建，并在需要时打包为可直接打开的单文件 HTML。

## Why This Exists

Directly asking a model for a single HTML file often collapses rich interface work into a static page. The stronger route is:

1. Prepare a real app workspace.
2. Keep the user's task intact.
3. Let the design worker own the visual direction.
4. Build and render the result in Chrome.
5. Package to standalone HTML only after the app source exists.

The goal is not to hardcode one visual style. The scaffold supplies execution shape and verification tools, not a house aesthetic.

## What Is Included

| Path | Purpose |
| --- | --- |
| `profile/GEMINI.md` | Design-worker execution kernel. |
| `profile/SKILL.md` | Hermes/Codex skill wrapper. |
| `profile/design_skills/` | Supplemental design craft guidance. |
| `profile/prompt-seeds/` | General high-performing prompt drivers with task content removed. |
| `profile/source-prompts/README.md` | Placeholder for optional source prompt corpus. Raw external prompt files are not redistributed. |
| `scripts/create_build_like_web_app.py` | Creates the Vite/React/Tailwind scaffold. |
| `scripts/package_vite_dist_single_html.py` | Inlines Vite `dist` assets into one browser-openable HTML file. |
| `scripts/capture_chrome_cdp_fullpage.mjs` | Captures desktop and 390px mobile full-page screenshots through Chrome CDP. |
| `scripts/check_project_structure.py` | Confirms app-like project shape. |
| `docs/render-evidence.md` | Explains how to capture reproducible render proof for generated artifacts. |
| `evidence/` | Public-safe screenshots showing the workflow difference on fictional test artifacts. |

## Quick Start: Full One-Shot Route

If the official Gemini CLI is installed and logged in, this is the intended
drop-in command:

```powershell
cd C:\path\to\gemini-build-parity-scaffold
python scripts\run_gemini_design_once.py out\fictional-profile --name "Fictional Profile" --brief-file examples\fictional-recruiter-profile\brief.md --force
```

What this does:

1. Creates the app-first scaffold.
2. Copies `profile/GEMINI.md`, `design_skills/`, `prompt-seeds/`, and `source-prompts/` into the artifact workspace.
3. Runs Gemini CLI inside that workspace, so the local `GEMINI.md` and copied context files are visible to the worker.
4. Runs `npm install`, `npm run lint`, and `npm run build`.
5. Packages `dist` into `standalone.html`.

The scaffold benefit is only fully active when Gemini runs inside the generated
artifact folder. Running Gemini from another directory and merely pasting the
brief will not reproduce the same setup.

## Manual Scaffold Route

```powershell
cd C:\path\to\gemini-build-parity-scaffold
python scripts\create_build_like_web_app.py out\fictional-profile --name "Fictional Profile" --brief-file examples\fictional-recruiter-profile\brief.md --force
cd out\fictional-profile
npm install
```

Then run your design worker in that generated folder. The worker should read `GEMINI.md`, `task.md`, `BUILD_ENVIRONMENT.md`, `AIS_REFERENCE_COMMONS.md`, `design_skills/`, and any optional `source-prompts/` files that you are legally allowed to use.

After the worker edits source files:

```powershell
npm run lint
npm run build
cd ..\..
python scripts\package_vite_dist_single_html.py out\fictional-profile\dist out\fictional-profile\standalone.html
node scripts\capture_chrome_cdp_fullpage.mjs "file:///C:/path/to/gemini-build-parity-scaffold/out/fictional-profile/standalone.html" out\fictional-profile\captures --settle-ms 5000
```

The Chrome CDP capture script is optional. It exists only to make screenshot
evidence reproducible for users who do not already have browser automation in
their agent environment. If your agent can open the local artifact and capture
desktop/mobile screenshots, use that instead.

## Hermes Installation

Install the profile into a Hermes home directory:

```powershell
python scripts\install_hermes_profile.py --hermes-home C:\path\to\.hermes-home --profile design --force
```

This copies the profile to:

```text
<hermes-home>\profiles\design\skills\build-parity-design-director
```

Hermes still needs an agent or task runner that calls either:

```powershell
python scripts\run_gemini_design_once.py <artifact-root> --name "<artifact name>" --brief-file <brief.md> --force
```

or the manual scaffold route above. The install script gives Hermes the skill
and instruction context; the run script gives Gemini the prepared artifact
workspace.

## Workflow Proof Snapshot

These examples use a fictional candidate. They are not about a real person.

| Run | Route | Evidence |
| --- | --- | --- |
| Baseline 1830 | Direct/simple HTML-oriented Gemini run | ![Baseline 1830 desktop](evidence/baseline-1830/desktop-fullpage.png) |
| Baseline 1840 | Early universal rules route | ![Baseline 1840 desktop](evidence/baseline-1840/desktop-fullpage.png) |
| Final 0003 | App-first scaffold, design kernel, standalone packaging | ![Final 0003 desktop](evidence/final-0003/desktop-fullpage.png) |

These screenshots are proof of the execution route. They show why the repository exists: the scaffolded app-first route gives the model a stronger working environment than a plain static-output request.

## Publication Boundary

This public package deliberately excludes:

- Personal career data.
- Account names, OAuth state, cookies, API keys, tokens, or local auth folders.
- Company-internal facts or confidential implementation details.
- Raw external prompt corpora whose redistribution rights are unclear or incompatible.
- Copied browser-extension backends or native messaging code.

If you add optional external source prompts under `profile/source-prompts/`, verify their license and redistribution rights before publishing your fork.

## License

MIT. See `LICENSE`.
