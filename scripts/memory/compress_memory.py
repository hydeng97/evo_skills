#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compress session summaries into durable memory"
    )
    parser.add_argument("--memory-dir", required=True, help="Path to memory/<skill_id>")
    parser.add_argument("--user-id", required=True, help="User identifier")
    return parser.parse_args()


def append_section(path: Path, title: str, lines: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else f"# {title}\n\n"
    content = (
        existing.rstrip()
        + "\n\n## Update\n\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n"
    )
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    user_dir = Path(args.memory_dir).resolve() / "users" / args.user_id
    sessions_dir = user_dir / "sessions"
    session_files = sorted(sessions_dir.glob("*.md")) if sessions_dir.exists() else []

    if not session_files:
        print("No session summaries to compress.")
        return 0

    session_summaries = []
    for path in session_files:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line and not line.startswith("#") and not line.startswith("##"):
                session_summaries.append(line)
                break

    append_section(user_dir / "progress.md", "Progress", session_summaries)
    append_section(
        user_dir / "profile.md", "Profile", ["Updated after session compression"]
    )
    print(
        f"Compressed {len(session_files)} session summaries into durable memory files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
