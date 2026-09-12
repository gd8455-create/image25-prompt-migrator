#!/usr/bin/env python3
"""Validate the public skill package without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


SKILL_NAME = "image25-prompt-migrator"
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
IGNORED_PARTS = {".git", ".pytest_cache", ".venv", "__pycache__"}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(markdown: str) -> dict[str, str]:
    lines = markdown.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "NOTICE"}:
            yield path


def validate_skill_layout(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    skill_dirs = sorted(path.name for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    if skill_dirs != [SKILL_NAME]:
        errors.append(f"skills/ must contain exactly {SKILL_NAME}; found {skill_dirs}")
        return errors

    skill_root = skills_root / SKILL_NAME
    entrypoint = skill_root / "SKILL.md"
    if not entrypoint.is_file():
        errors.append("The public skill is missing SKILL.md")
        return errors

    try:
        frontmatter = parse_frontmatter(entrypoint.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
        return errors

    if frontmatter.get("name") != SKILL_NAME:
        errors.append(f"SKILL.md name must be {SKILL_NAME!r}")
    if not frontmatter.get("description"):
        errors.append("SKILL.md must have a non-empty description")

    agent_metadata = skill_root / "agents" / "openai.yaml"
    if not agent_metadata.is_file():
        errors.append("The public skill is missing agents/openai.yaml")

    references = skill_root / "references"
    if not references.is_dir() or not any(references.glob("*.md")):
        errors.append("The public skill must include its referenced guidance")
    return errors


INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)


def relative_targets(markdown: str):
    for match in INLINE_LINK.finditer(markdown):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1 : raw.index(">")]
        else:
            raw = raw.split(maxsplit=1)[0]
        yield raw
    for match in REFERENCE_LINK.finditer(markdown):
        yield match.group(1).strip("<>")


def validate_relative_links(root: Path) -> list[str]:
    errors: list[str] = []
    for document in root.rglob("*.md"):
        if any(part in IGNORED_PARTS for part in document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in relative_targets(text):
            target = unquote(raw_target.split("#", 1)[0])
            if not target:
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            linked = (document.parent / target).resolve()
            try:
                linked.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{document.relative_to(root)} links outside the repository: {raw_target}")
                continue
            if not linked.exists():
                errors.append(f"{document.relative_to(root)} has a broken link: {raw_target}")
    return errors


def forbidden_patterns() -> list[tuple[str, re.Pattern[str]]]:
    windows_profile = r"[A-Za-z]:[\\/]+" + "Users" + r"[\\/]+[^\\/\s]+"
    mac_profile = "/" + "Users" + r"/[^/\s]+"
    linux_profile = "/" + "home" + r"/[^/\s]+"
    cloud_folder = "One" + "Drive"
    private_key = "-----BEGIN " + r"(?:RSA |EC |OPENSSH )?" + "PRIVATE KEY-----"
    return [
        ("Windows user profile path", re.compile(windows_profile, re.IGNORECASE)),
        ("macOS user profile path", re.compile(mac_profile)),
        ("Linux user profile path", re.compile(linux_profile)),
        ("personal cloud path", re.compile(re.escape(cloud_folder), re.IGNORECASE)),
        ("private key", re.compile(private_key)),
        ("GitHub token", re.compile(r"(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
        ("OpenAI-style secret", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
        ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
        (
            "embedded secret assignment",
            re.compile(
                r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
            ),
        ),
        ("credential in URL", re.compile(r"https?://[^\s/:]+:[^\s/@]+@", re.IGNORECASE)),
    ]


def validate_public_content(root: Path) -> list[str]:
    errors: list[str] = []
    patterns = forbidden_patterns()
    for path in iter_text_files(root):
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns:
            if pattern.search(text):
                errors.append(f"{path.relative_to(root)} contains {label}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    if not root.is_dir():
        return [f"Repository root does not exist: {root}"]
    errors: list[str] = []
    errors.extend(validate_skill_layout(root))
    errors.extend(validate_relative_links(root))
    errors.extend(validate_public_content(root))
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repository_root())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    errors = validate(args.root)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
