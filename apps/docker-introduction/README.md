# Docker introduction — complete Iris application

Build with `docker build -t iris-introduction .` and run with `docker run --rm iris-introduction`. The pinned official Python image and complete dependency file reproduce the demonstrated environment. No model is downloaded; Iris is bundled with scikit-learn.

The application trains LogisticRegression on a fixed stratified split, prints real held-out predictions/targets and confusion matrix, and runs as UID10001. One small split is a teaching example, not a production quality benchmark.

See `../../series/docker/Docker_Data_Science_Introduction.ipynb` for real local-engine lifecycle and registry examples with guarded cleanup.
