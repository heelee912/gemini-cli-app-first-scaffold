#!/usr/bin/env python3
"""Package a Vite dist folder into a browser-openable single HTML file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SCRIPT_RE = re.compile(
    r'<script\s+type="module"\s+crossorigin\s+src="([^"]+)"></script>|'
    r'<script\s+type="module"\s+src="([^"]+)"></script>'
)
STYLE_RE = re.compile(
    r'<link\s+rel="stylesheet"\s+crossorigin\s+href="([^"]+)">|'
    r'<link\s+rel="stylesheet"\s+href="([^"]+)">'
)


def local_asset(dist: Path, raw: str) -> Path:
    value = raw.strip()
    if value.startswith("./"):
        value = value[2:]
    elif value.startswith("/"):
        value = value[1:]
    path = (dist / value).resolve()
    dist_resolved = dist.resolve()
    if not str(path).lower().startswith(str(dist_resolved).lower()):
        raise ValueError(f"Asset escapes dist folder: {raw}")
    if not path.exists():
        raise FileNotFoundError(f"Missing asset: {path}")
    return path


def package(dist: Path, output: Path) -> None:
    index = dist / "index.html"
    html = index.read_text(encoding="utf-8")

    def replace_style(match: re.Match[str]) -> str:
        href = match.group(1) or match.group(2)
        css = local_asset(dist, href).read_text(encoding="utf-8")
        return f"<style>\n{css}\n</style>"

    def replace_script(match: re.Match[str]) -> str:
        src = match.group(1) or match.group(2)
        js = local_asset(dist, src).read_text(encoding="utf-8")
        return f'<script type="module">\n{js}\n</script>'

    html = STYLE_RE.sub(replace_style, html)
    html = SCRIPT_RE.sub(replace_script, html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inline Vite dist assets into one direct-open HTML file.")
    parser.add_argument("dist", help="Vite dist folder")
    parser.add_argument("output", help="output HTML path")
    args = parser.parse_args()
    package(Path(args.dist).expanduser().resolve(), Path(args.output).expanduser().resolve())
    print(str(Path(args.output).expanduser().resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
