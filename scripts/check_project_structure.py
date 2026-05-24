#!/usr/bin/env python3
"""Check app-like project shape."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "package.json",
    "tsconfig.json",
    "index.html",
    "src/main.tsx",
    "src/App.tsx",
]

VITE_CANDIDATES = ["vite.config.ts", "vite.config.js", "vite.config.mts"]
STYLE_CANDIDATES = ["src/index.css", "src/App.css", "src/styles.css"]


def inspect(root: Path) -> dict[str, object]:
    missing = [name for name in REQUIRED_FILES if not (root / name).exists()]
    if not any((root / name).exists() for name in VITE_CANDIDATES):
        missing.append("vite.config.ts or equivalent")
    if not any((root / name).exists() for name in STYLE_CANDIDATES):
        missing.append("src/index.css or equivalent")
    tsx_files = [p for p in root.rglob("*.tsx") if "node_modules" not in p.parts]
    status = "ok" if not missing and tsx_files else "fail"
    return {
        "root": str(root),
        "status": status,
        "missing": missing,
        "tsx_files": [str(p.relative_to(root)) for p in tsx_files[:80]],
        "reason": "app-like Vite React project detected" if status == "ok" else "not an app-like Vite React project",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project structure.")
    parser.add_argument("root", help="artifact project root")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = inspect(Path(args.root).expanduser().resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{str(result['status']).upper()}: {result['reason']}")
        if result["missing"]:
            print("Missing:")
            for item in result["missing"]:
                print(f"- {item}")
        print(f"TSX files: {len(result['tsx_files'])}")
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
