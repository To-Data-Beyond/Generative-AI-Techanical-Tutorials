# Time Series with Python

Complete companion notebooks for the six published parts of the series. Start with setup, then run every cell in order in Python 3.11 or Colab. No API keys or GPU are required. Setup installs pinned packages and verifies downloaded historical datasets by SHA-256. Restart an already-used kernel before running.

## Contents

| Part | Article | Notebook | Colab |
| --- | --- | --- | --- |
| 1 | [Manipulating Time Series Data In Python](https://todatabeyond.com/blog/manipulating-time-series-data-in-python) | [01_Time_Series_Manipulation.ipynb](./01_Time_Series_Manipulation.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/01_Time_Series_Manipulation.ipynb) |
| 2 | [Time Series Data Analysis In Python](https://todatabeyond.com/blog/time-series-data-analysis-in-python) | [02_Time_Series_Analysis.ipynb](./02_Time_Series_Analysis.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/02_Time_Series_Analysis.ipynb) |
| 3 | [Time Series Data Visualization In Python](https://todatabeyond.com/blog/time-series-data-visualization-in-python) | [03_Time_Series_Visualization.ipynb](./03_Time_Series_Visualization.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/03_Time_Series_Visualization.ipynb) |
| 4 | [Time Series Forecasting with ARIMA Models In Python [Part 1]](https://todatabeyond.com/blog/time-series-forecasting-with-arima-models-in-python-part-1) | [04_ARIMA_Models_Part_1.ipynb](./04_ARIMA_Models_Part_1.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/04_ARIMA_Models_Part_1.ipynb) |
| 5 | [Time Series Forecasting with ARIMA Models In Python [Part 2]](https://todatabeyond.com/blog/time-series-forecasting-with-arima-models-in-python-part-2) | [05_ARIMA_Models_Part_2.ipynb](./05_ARIMA_Models_Part_2.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/05_ARIMA_Models_Part_2.ipynb) |
| 6 | [Machine Learning for Time Series Data in Python [Regression]](https://todatabeyond.com/blog/machine-learning-for-time-series-data-in-python-regression) | [06_Machine_Learning_Regression.ipynb](./06_Machine_Learning_Regression.ipynb) | [Run](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/time-series-python/06_Machine_Learning_Regression.ipynb) |

## Data and maintenance

See [data provenance](./data/README.md). Setup uses the original author repository at immutable commit `65d4ae5d3436be3c0a921a3dcbda1b52e3ac8597`; the original 14 input files are not silently reduced. Missing GDP and annual temperature files use the documented public snapshots. The source multi-asset data are recovered from the original `price.csv`.

The index example uses the source-intended 2016 window, label-aligned company share counts and common observed benchmark dates. It is an educational historical construction, not a validated investment backtest. Amazon data are quarterly adjusted stock prices, not revenue. The temperature forecast is a univariate statistical exercise, not a physical climate projection.

All 136 code cells (69 manipulation, 21 analysis, 46 visualization) were executed in fresh Python 3.11.14 kernels. Final regression cells independently verify returns, window means, weighted-index calculations, OLS/ACF/AR recurrences, forecast means and intervals, seasonal decomposition and correlations. Notebooks remain output-free in Git. All 129 complete original embedded code blocks are retained verbatim in nonexecuting markdown appendices.

## ARIMA, SARIMA and machine-learning regression

Parts 4–6 add 81 executed code cells (15/28/38) using six complete original inputs: 564 candy months, 1,259 Amazon closing prices, 727 CO2 months, 99 earthquake years, 84,912 long-form stock rows and a 1,278×46 preprocessed matrix. No replacement data or paid API is required. Keep the Amazon records sorted chronologically.

ARIMA Part 1 includes manual integration and direct twenty-step forecasts with independent state/covariance interval checks. Part 2 runs all 59 original grid candidates and the full stepwise seasonal bounds, checks convergence, uses separate raw/detrended/differenced series and tests exact save/reload parity for twenty-four forecasts. Optimization start-parameter warnings remain visible; no failed final model is certified as converged.

Regression distinguishes same-day cross-company association from the past-only seven-lag AIG forecast. The actual chronological same-day holdout R² is −0.338, while the lag example’s holdout R² is 0.941. These historical results are not investment guidance. Shuffled and ordinary KFold examples demonstrate why those splits are inappropriate for forward forecasting. Independent checks cover Ridge/R², all lag/window features, interpolation, 110 forward-fold correlations and deterministic descriptive coefficient resampling. Overlapping-fold resampling is not claimed to establish confidence-interval coverage.

All 75 original gist blocks for these three parts are retained verbatim in nonexecuting markdown appendices. Code cells are committed without outputs or execution counts. Actual text outputs and forty-one computed plots appear in the website articles alongside their original figures. Across Parts 1–6, 217 cells have executed and 204 original gist blocks are preserved.
