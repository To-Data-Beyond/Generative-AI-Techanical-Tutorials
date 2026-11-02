#!/usr/bin/env bash
set -euo pipefail
exec python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/format_edits.py"
