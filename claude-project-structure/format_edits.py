"""A bounded PostToolUse formatter; not a general security sandbox."""
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    try:
        payload = sys.stdin.read(1_000_001)
        if len(payload) > 1_000_000:
            raise ValueError("Hook input exceeds the limit.")
        event = json.loads(payload)
        if not isinstance(event, dict):
            raise ValueError("Hook input must be a JSON object.")
        if event.get("hook_event_name") != "PostToolUse" or event.get("tool_name") not in {"Edit", "Write"}:
            return 0
        root = Path(os.environ["CLAUDE_PROJECT_DIR"]).resolve(strict=True)
        cwd = Path(event["cwd"]).resolve(strict=True)
        if cwd != root:
            raise ValueError("Hook cwd does not match the configured project.")
        name = event["tool_input"]["file_path"]
        if not isinstance(name, str) or not name or "\x00" in name:
            raise ValueError("Missing file path.")
        candidate = Path(name)
        target = (candidate if candidate.is_absolute() else root / candidate).resolve(strict=True)
        relative = target.relative_to(root)
        if any(part in {".git", ".venv", "node_modules"} for part in relative.parts):
            raise ValueError("Generated/internal paths are excluded.")
        if target.name.startswith(".env") or not target.is_file():
            raise ValueError("Expected an ordinary project source file.")
        if target.suffix != ".py":
            return 0
        result = subprocess.run([sys.executable, "-m", "ruff", "format", "--", str(target)],
            capture_output=True, text=True, timeout=10, check=False)
        if result.returncode:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Formatter hook: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
