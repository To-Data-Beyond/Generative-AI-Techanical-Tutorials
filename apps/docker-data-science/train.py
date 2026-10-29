import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv(Path(__file__).parent / "data/training.csv")
model = LinearRegression().fit(data[["feature"]].to_numpy(), data.target.to_numpy())
np.testing.assert_allclose(model.coef_, [3.0])
np.testing.assert_allclose(model.intercept_, 2.0)
np.testing.assert_allclose(model.predict([[6.0], [7.0]]), [20.0, 23.0])
Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/regression.joblib")
print(json.dumps({"training_rows": len(data), "coefficient": float(model.coef_[0]),
                  "intercept": float(model.intercept_)}, sort_keys=True))
