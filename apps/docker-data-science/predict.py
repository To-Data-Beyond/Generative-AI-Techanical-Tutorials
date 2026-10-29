import json
from pathlib import Path

import joblib
import numpy as np

# Load only the model created by our own build stage, never an untrusted upload.
model = joblib.load(Path(__file__).parent / "models/regression.joblib")
inputs = np.asarray([[6.0], [7.0]])
predictions = model.predict(inputs)
np.testing.assert_allclose(predictions, [20.0, 23.0])
print(json.dumps({"inputs": inputs.ravel().tolist(), "predictions": predictions.round(8).tolist()}, sort_keys=True))
