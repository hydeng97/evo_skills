#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read effective memory context for a mode"
    )
    parser.add_argument("--meta", required=True, help="Path to child skill meta.json")
    parser.add_argument("--memory-dir", required=True, help="Path to memory/<skill_id>")
    parser.add_argument("--user-id", required=True, help="User identifier")
    parser.add_argument(
        "--mode", required=True, help="Mode: teach/coach/reflect/execute"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    memory_runtime = meta.get("memory_runtime", {})
    read_layers = memory_runtime.get("read_by_mode", {}).get(args.mode, [])
    user_dir = Path(args.memory_dir).resolve() / "users" / args.user_id

    print(f"# Memory Context ({args.mode})")
    print()

    for layer in read_layers:
        if layer == "profile":
            path = user_dir / "profile.md"
            if path.exists():
                print("## profile")
                print(path.read_text(encoding="utf-8"))
        elif layer == "progress":
            path = user_dir / "progress.md"
            if path.exists():
                print("## progress")
                print(path.read_text(encoding="utf-8"))
        elif layer == "sessions":
            sessions_dir = user_dir / "sessions"
            print("## sessions")
            if sessions_dir.exists():
                for path in sorted(sessions_dir.glob("*.md")):
                    print(f"### {path.name}")
                    print(path.read_text(encoding="utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
