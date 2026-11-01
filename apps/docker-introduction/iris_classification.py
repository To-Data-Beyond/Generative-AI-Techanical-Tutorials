import json
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

def train_and_evaluate():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target)
    model = LogisticRegression(max_iter=300, random_state=42).fit(X_train, y_train)
    prediction = model.predict(X_test)
    assert np.isfinite(model.coef_).all()
    return {'dataset': 'iris', 'train_rows': len(y_train), 'test_rows': len(y_test),
            'accuracy': float(accuracy_score(y_test, prediction)),
            'correct': int((prediction == y_test).sum()),
            'predictions': prediction.tolist(), 'targets': y_test.tolist(),
            'confusion_matrix': confusion_matrix(y_test, prediction).tolist()}

if __name__ == '__main__':
    print(json.dumps(train_and_evaluate(), sort_keys=True))
