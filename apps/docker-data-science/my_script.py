import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv(Path(__file__).parent / "data/training.csv")
assert data.shape == (6, 2)
artifact = Path("/tmp/tdb-summary.png")
sns.lineplot(data=data, x="feature", y="target")
plt.tight_layout()
plt.savefig(artifact)
plt.close("all")
assert artifact.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
print(json.dumps({"rows": len(data), "feature_mean": float(data.feature.mean()),
                  "target_mean": float(data.target.mean()), "plot_bytes": artifact.stat().st_size}, sort_keys=True))
