#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a short session summary")
    parser.add_argument("--memory-dir", required=True, help="Path to memory/<skill_id>")
    parser.add_argument("--user-id", required=True, help="User identifier")
    parser.add_argument(
        "--summary", required=True, help="One-line or short session summary"
    )
    parser.add_argument("--follow-up", default="", help="Optional follow-up note")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sessions_dir = Path(args.memory_dir).resolve() / "users" / args.user_id / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".md"
    path = sessions_dir / filename
    path.write_text(
        f"# Session Summary\n\n## Summary\n\n{args.summary}\n\n## Follow-up\n\n{args.follow_up or '-'}\n",
        encoding="utf-8",
    )
    print(f"Wrote session summary to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
