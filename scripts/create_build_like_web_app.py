#!/usr/bin/env python3
"""Create a local app-builder-style Vite/React scaffold.

The scaffold gives a design model a real app editing surface without seeding a
fixed visual style.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = REPO_ROOT / "profile"


PACKAGE_JSON = {
    "name": "app-first-scaffold-app",
    "private": True,
    "version": "0.0.0",
    "type": "module",
    "scripts": {
        "dev": "vite --port=3000 --host=0.0.0.0",
        "build": "vite build",
        "preview": "vite preview",
        "lint": "tsc --noEmit",
    },
    "dependencies": {
        "@google/genai": "^2.4.0",
        "@tailwindcss/vite": "^4.1.14",
        "@vitejs/plugin-react": "^5.0.4",
        "dotenv": "^17.2.3",
        "express": "^4.21.2",
        "lucide-react": "^0.546.0",
        "motion": "^12.23.24",
        "react": "^19.0.1",
        "react-dom": "^19.0.1",
        "vite": "^6.2.3",
    },
    "devDependencies": {
        "@types/express": "^4.17.21",
        "@types/node": "^22.14.0",
        "autoprefixer": "^10.4.21",
        "esbuild": "^0.25.0",
        "tailwindcss": "^4.1.14",
        "tsx": "^4.21.0",
        "typescript": "~5.8.2",
    },
}


INDEX_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""


VITE_CONFIG = """import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';

export default defineConfig(() => {
  return {
    base: './',
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    server: {
      hmr: process.env.DISABLE_HMR !== 'true',
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
    define: {
      'process.env.API_KEY': JSON.stringify(process.env.API_KEY ?? process.env.GEMINI_API_KEY ?? ''),
      'process.env.GEMINI_API_KEY': JSON.stringify(process.env.GEMINI_API_KEY ?? process.env.API_KEY ?? ''),
    },
  };
});
"""


TSCONFIG = """{
  "compilerOptions": {
    "target": "ES2022",
    "experimentalDecorators": true,
    "useDefineForClassFields": false,
    "module": "ESNext",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "moduleDetection": "force",
    "allowJs": true,
    "jsx": "react-jsx",
    "paths": {
      "@/*": ["./*"]
    },
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
"""


MAIN_TSX = """import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App.tsx';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
"""


APP_TSX = """import {scaffoldRecords} from './data.ts';

export default function App() {
  return <main data-scaffold-records={scaffoldRecords.length}></main>;
}
"""


TYPES_TS = """export type ArtifactPrimitive = string | number | boolean;

export type ArtifactRecord = Record<
  string,
  ArtifactPrimitive | ArtifactPrimitive[] | null
>;
"""


DATA_TS = """import type {ArtifactRecord} from './types.ts';

export const scaffoldRecords: ArtifactRecord[] = [];
"""


INDEX_CSS = """@import "tailwindcss";
"""


COMPONENTS_README = """# Components

Create brief-specific components here when the artifact benefits from real app
structure, state surfaces, inspectors, controls, comparison views, export
surfaces, or responsive section boundaries.

This folder intentionally contains no reusable visual house style.
"""


ENV_EXAMPLE = """GEMINI_API_KEY="MY_GEMINI_API_KEY"
APP_URL="MY_APP_URL"
"""


GITIGNORE = """node_modules/
dist/
coverage/
.env*
!.env.example
*.log
"""


METADATA_JSON = {
    "name": "",
    "description": "App-first scaffold generated web application.",
    "requestFramePermissions": [],
    "majorCapabilities": ["MAJOR_CAPABILITY_SERVER_SIDE_GEMINI_API"],
}


BUILD_ENVIRONMENT = """# Build Environment

This workspace is a local compatibility layer for app-builder-style output.

Reusable scaffold facts:

- Vite preview and build.
- React and TypeScript source files.
- Tailwind v4 through `@tailwindcss/vite`.
- `@google/genai` and AI Studio-style environment variables for Gemini API apps.
- `lucide-react` and `motion` are available when useful.
- `metadata.json`, `.env.example`, `.gitignore`, `README.md`, `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html`, `src/main.tsx`, `src/App.tsx`, `src/data.ts`, `src/types.ts`, `src/components/`, and `src/index.css`.
- `source-prompts/` is optional and may contain legally usable external prompt context.
- `prompt-seeds/` stores general high-performing prompt drivers with task content removed.
- `design_skills/` stores supplemental craft guidance.

The scaffold must not prescribe a concrete visual style. It deliberately does not include a palette, layout, motif, card system, typography system, domain content, reusable visual component, starter UI, or placeholder page copied from any reference output.

The starter source is intentionally neutral. A strong design pass should replace it with brief-specific data, state, components, and interaction logic.
"""


AIS_REFERENCE_COMMONS = """# Reference Commons

These are reusable execution and packaging facts, not visual design directions.

## Common File Shape

- `package.json`
- `index.html`
- `metadata.json`
- `.env.example`
- `.gitignore`
- `vite.config.ts`
- `tsconfig.json`
- `src/main.tsx`
- `src/App.tsx`
- `src/index.css`

No concrete design component, palette, motif, typography decision, copy block, layout, or domain content is part of the reusable scaffold.

## Common Runtime

- Vite
- React
- TypeScript
- Tailwind through `@tailwindcss/vite`
- `@google/genai`
- `lucide-react`
- `motion`
- `dotenv`
- `express`

The presence of a dependency means it is available when the brief benefits from it. It does not require the generated app to use every dependency.
"""


README = """# Generated App-First Scaffold App

Install and build:

```bash
npm install
npm run lint
npm run build
```

Package after build:

```bash
python ../../scripts/package_vite_dist_single_html.py dist standalone.html
```
"""


TASK = """# App-First Scaffold Task

App name: {app_name}

## User Brief

{brief}

## Worker Instruction

Replace the neutral starter source with the requested application.

Use the prepared app-builder-style runtime as the execution environment.
Do not preserve starter names, placeholder models, starter layout, or starter styling.
The scaffold intentionally provides app structure without a concrete visual seed.
"""


def safe_name(name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip().lower()).strip("-")
    return value or "app-first-scaffold-app"


def write_text(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: object, force: bool) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n", force)


def copy_tree(source: Path, target: Path) -> None:
    if not source.exists():
        return
    target.mkdir(parents=True, exist_ok=True)
    for item in sorted(source.iterdir()):
        if item.is_file():
            shutil.copyfile(item, target / item.name)


def copy_profile_files(root: Path) -> None:
    for name in ("GEMINI.md", "SKILL.md"):
        source = PROFILE_ROOT / name
        if source.exists():
            shutil.copyfile(source, root / name)
    copy_tree(PROFILE_ROOT / "design_skills", root / "design_skills")
    copy_tree(PROFILE_ROOT / "prompt-seeds", root / "prompt-seeds")
    copy_tree(PROFILE_ROOT / "source-prompts", root / "source-prompts")


def resolve_command(command: list[str]) -> list[str]:
    executable = "npm.cmd" if sys.platform == "win32" and command[0] == "npm" else command[0]
    resolved = shutil.which(executable)
    if not resolved:
        raise FileNotFoundError(f"Could not find executable: {executable}")
    return [resolved, *command[1:]]


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(resolve_command(command), cwd=str(cwd), check=True)


def read_brief(args: argparse.Namespace) -> str:
    if args.brief_file:
        return Path(args.brief_file).read_text(encoding="utf-8")
    return args.brief or ""


def create(root: Path, app_name: str, brief: str, force: bool) -> None:
    package = dict(PACKAGE_JSON)
    package["name"] = safe_name(app_name)
    metadata = dict(METADATA_JSON)
    metadata["name"] = app_name

    write_json(root / "package.json", package, force)
    write_text(root / "index.html", INDEX_HTML.format(title=app_name), force)
    write_json(root / "metadata.json", metadata, force)
    write_text(root / ".env.example", ENV_EXAMPLE, force)
    write_text(root / ".gitignore", GITIGNORE, force)
    write_text(root / "README.md", README, force)
    write_text(root / "vite.config.ts", VITE_CONFIG, force)
    write_text(root / "tsconfig.json", TSCONFIG, force)
    write_text(root / "src/main.tsx", MAIN_TSX, force)
    write_text(root / "src/App.tsx", APP_TSX, force)
    write_text(root / "src/types.ts", TYPES_TS, force)
    write_text(root / "src/data.ts", DATA_TS, force)
    write_text(root / "src/components/README.md", COMPONENTS_README, force)
    write_text(root / "src/index.css", INDEX_CSS, force)
    write_text(root / "task.md", TASK.format(app_name=app_name, brief=brief.strip() or "(No brief was provided.)"), force)
    write_text(root / "BUILD_ENVIRONMENT.md", BUILD_ENVIRONMENT, force)
    write_text(root / "AIS_REFERENCE_COMMONS.md", AIS_REFERENCE_COMMONS, force)
    copy_profile_files(root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an app-first Vite React scaffold.")
    parser.add_argument("root", help="target artifact directory")
    parser.add_argument("--name", default="App-First Scaffold App", help="app display name")
    parser.add_argument("--brief", default="", help="brief text")
    parser.add_argument("--brief-file", help="file containing brief text")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument("--install", action="store_true", help="run npm install")
    parser.add_argument("--build", action="store_true", help="run npm run build")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    create(root, args.name, read_brief(args), args.force)

    if args.install:
        run(["npm", "install"], root)
    if args.build:
        run(["npm", "run", "build"], root)

    print(f"created app-first scaffold: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
