#!/usr/bin/env python3
"""Create an app-first scaffold, run Gemini CLI inside it, then verify and package.

This is the drop-in route for users who want the prepared scaffold and
instruction kernel to be visible to Gemini automatically.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from create_build_like_web_app import create


DEFAULT_MODEL = "gemini-3-flash-preview"


WORKER_PROMPT = """You are executing inside a prepared app-first Vite/React/Tailwind project.

Read these local files before editing:

- GEMINI.md
- task.md
- BUILD_ENVIRONMENT.md
- AIS_REFERENCE_COMMONS.md
- prompt-seeds/empirical-build-like-drivers.md
- design_skills/design-philosophy.md
- design_skills/image-generation.md
- design_skills/shadcn-ui.md
- every file under source-prompts/ if present
- src/App.tsx
- src/data.ts
- src/types.ts
- src/index.css
- src/components/README.md

Write files into the current working directory. Do not answer with a single
HTML document in chat. Replace the neutral starter source with the requested
application. Keep the source artifact as a runnable app project. The main
process will run install, lint, build, and packaging after your edit pass.
"""


def resolve_command(command: str) -> str:
    candidate = f"{command}.cmd" if sys.platform == "win32" and not command.endswith(".cmd") else command
    resolved = shutil.which(candidate) or shutil.which(command)
    if not resolved:
        raise FileNotFoundError(f"Could not find executable: {command}")
    return resolved


def run(command: list[str], cwd: Path, log: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if log:
        log.write_text(
            f"$ {' '.join(command)}\n\n## STDOUT\n{completed.stdout}\n\n## STDERR\n{completed.stderr}\n",
            encoding="utf-8",
            newline="\n",
        )
    return completed


def read_brief(args: argparse.Namespace) -> str:
    if args.brief_file:
        return Path(args.brief_file).read_text(encoding="utf-8")
    return args.brief or ""


def run_gemini(root: Path, gemini: str, model: str, timeout_seconds: int) -> None:
    prompt_path = root / "app_first_worker_prompt.md"
    prompt_path.write_text(WORKER_PROMPT, encoding="utf-8", newline="\n")
    prompt = WORKER_PROMPT
    executable = resolve_command(gemini)
    command = [
        executable,
        "--yolo",
        "--skip-trust",
        "-m",
        model,
        "--output-format",
        "text",
        "-p",
        prompt,
    ]
    completed = run(command, root, root / "gemini_design_run.log")
    if completed.returncode != 0:
        raise RuntimeError(f"Gemini CLI failed. See {root / 'gemini_design_run.log'}")


def npm(root: Path, args: list[str], log_name: str) -> None:
    executable = resolve_command("npm")
    completed = run([executable, *args], root, root / log_name)
    if completed.returncode != 0:
        raise RuntimeError(f"`npm {' '.join(args)}` failed. See {root / log_name}")


def package(root: Path) -> None:
    from package_vite_dist_single_html import package as package_dist

    package_dist(root / "dist", root / "standalone.html")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one Gemini design pass in an app-first scaffold.")
    parser.add_argument("root", help="target artifact directory")
    parser.add_argument("--name", required=True, help="app display name")
    parser.add_argument("--brief", default="", help="brief text")
    parser.add_argument("--brief-file", help="file containing brief text")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--gemini", default="gemini")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--force", action="store_true", help="overwrite existing scaffold files")
    parser.add_argument("--no-install", action="store_true", help="skip npm install")
    parser.add_argument("--no-build", action="store_true", help="skip lint, build, and standalone packaging")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    create(root, args.name, read_brief(args), args.force)
    run_gemini(root, args.gemini, args.model, args.timeout_seconds)

    if not args.no_install:
        npm(root, ["install"], "npm_install.log")
    if not args.no_build:
        npm(root, ["run", "lint"], "npm_lint.log")
        npm(root, ["run", "build"], "npm_build.log")
        package(root)

    print(f"artifact root: {root}")
    if (root / "standalone.html").exists():
        print(f"standalone: {root / 'standalone.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
