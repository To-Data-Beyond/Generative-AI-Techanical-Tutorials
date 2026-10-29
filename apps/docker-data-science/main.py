import json
import sys
from pathlib import Path

path = Path("/app/data/results.json")
mode = sys.argv[1] if len(sys.argv) > 1 else "write"
if mode == "write":
    previous = json.loads(path.read_text()) if path.exists() else {"runs": 0}
    value = {"runs": previous["runs"] + 1, "rows_processed": 6}
    path.write_text(json.dumps(value, sort_keys=True))
elif mode == "read":
    value = json.loads(path.read_text())
else:
    raise ValueError("Choose write or read")
print(json.dumps(value, sort_keys=True))
