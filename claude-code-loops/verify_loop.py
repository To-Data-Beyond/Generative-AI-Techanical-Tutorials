"""Read-only mechanical checks; this does not invoke Claude or enforce a sandbox."""
import hashlib
from pathlib import Path

ALLOWED = {"PROGRESS.md", "outputs/daily-review.md"}
REPORT_SECTIONS = ("Summary", "Files reviewed", "Meaningful changes", "Blockers or unresolved questions", "Recommended next actions")
STATE_SECTIONS = ("Current State", "Last Run", "Needs Human Review", "Next Run Should")


def snapshot(root):
    root = Path(root).resolve()
    result = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError(f"Symlinks are outside this fixture workflow: {rel}")
        if path.is_file():
            result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def verify(root, before):
    root = Path(root).resolve()
    after = snapshot(root)
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    failed = [f"Forbidden file modified: {k}" for k in changed if k not in ALLOWED]
    for file, sections in [("outputs/daily-review.md", REPORT_SECTIONS), ("PROGRESS.md", STATE_SECTIONS)]:
        path = root / file
        if not path.is_file():
            failed.append(f"Missing file: {file}")
            continue
        text = path.read_text()
        for heading in sections:
            marker = "## " + heading
            if marker not in text.splitlines():
                failed.append(f"Missing section: {file}: {heading}")
            else:
                content = text.split(marker, 1)[1].split("\n## ", 1)[0].strip()
                if not content or content in {"-", "TODO", "TBD"}:
                    failed.append(f"Empty section: {file}: {heading}")
    if before.get("PROGRESS.md") == after.get("PROGRESS.md"):
        failed.append("PROGRESS.md was not updated")
    return {"accepted": not failed, "failed": failed, "changed": changed}
