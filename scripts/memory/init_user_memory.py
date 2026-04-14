#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize user memory from shared templates"
    )
    parser.add_argument("--memory-dir", required=True, help="Path to memory/<skill_id>")
    parser.add_argument("--user-id", required=True, help="User identifier")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    memory_dir = Path(args.memory_dir).resolve()
    shared_dir = memory_dir / "shared"
    user_dir = memory_dir / "users" / args.user_id
    sessions_dir = user_dir / "sessions"
    user_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(parents=True, exist_ok=True)

    mapping = {
        shared_dir / "profile.template.md": user_dir / "profile.md",
        shared_dir / "progress.template.md": user_dir / "progress.md",
    }

    for src, dst in mapping.items():
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    sessions_readme = sessions_dir / "README.md"
    if not sessions_readme.exists():
        sessions_readme.write_text(
            "# Sessions\n\nStore short session summaries here before compression.\n",
            encoding="utf-8",
        )

    print(f"Initialized user memory at {user_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
