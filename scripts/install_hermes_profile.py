#!/usr/bin/env python3
"""Install the app-first design profile into a Hermes home directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_SOURCE = REPO_ROOT / "profile"
SKILL_NAME = "app-first-design-director"


def default_hermes_home() -> Path:
    if os.environ.get("HERMES_HOME"):
        return Path(os.environ["HERMES_HOME"]).expanduser()
    return Path.home() / ".hermes"


def copy_profile(target: Path, force: bool) -> None:
    if target.exists():
        if not force:
            raise FileExistsError(f"{target} already exists. Use --force to overwrite.")
        shutil.rmtree(target)
    shutil.copytree(PROFILE_SOURCE, target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install app-first profile into Hermes.")
    parser.add_argument("--hermes-home", default=str(default_hermes_home()), help="Hermes home directory")
    parser.add_argument("--profile", default="design", help="Hermes profile name")
    parser.add_argument("--global-skill", action="store_true", help="install under <hermes-home>/skills instead of profile skills")
    parser.add_argument("--force", action="store_true", help="overwrite existing installed profile")
    args = parser.parse_args()

    hermes_home = Path(args.hermes_home).expanduser().resolve()
    if args.global_skill:
        target = hermes_home / "skills" / SKILL_NAME
    else:
        target = hermes_home / "profiles" / args.profile / "skills" / SKILL_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    copy_profile(target, args.force)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
