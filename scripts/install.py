#!/usr/bin/env python3
"""Install the single public skill shipped by this repository."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_NAME = "image25-prompt-migrator"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return base / "skills"


def install(destination: Path, *, force: bool = False) -> Path:
    """Copy only this repository's public skill into a Codex skills directory."""

    source = repository_root() / "skills" / SKILL_NAME
    if not (source / "SKILL.md").is_file():
        raise RuntimeError(f"Packaged skill is incomplete: {source}")

    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / SKILL_NAME
    if target.exists() and not force:
        raise FileExistsError(
            f"{target} already exists. Re-run with --force to replace this skill."
        )

    staging_root = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}-", dir=destination))
    staged_skill = staging_root / SKILL_NAME
    try:
        shutil.copytree(
            source,
            staged_skill,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        if not (staged_skill / "SKILL.md").is_file():
            raise RuntimeError("Staged copy is missing SKILL.md")

        if target.exists():
            shutil.rmtree(target)
        staged_skill.replace(target)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)

    return target


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install image25-prompt-migrator into a Codex skills directory."
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=default_destination(),
        help="Skills directory (default: CODEX_HOME/skills or ~/.codex/skills)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing image25-prompt-migrator installation.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        target = install(args.destination, force=args.force)
    except (FileExistsError, OSError, RuntimeError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 2

    print(f"Installed {SKILL_NAME} at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
