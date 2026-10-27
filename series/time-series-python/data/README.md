# Dataset provenance

Retrieved October 27, 2026. Snapshot files are public research/educational data, not synthetic substitutes. Original inputs are downloaded at an immutable revision and checked against embedded SHA-256 digests by notebook setup.

## Original author files

Repository: [youssefHosni/Time-Series-Analysis](https://github.com/youssefHosni/Time-Series-Analysis/tree/65d4ae5d3436be3c0a921a3dcbda1b52e3ac8597).

- Manipulation: `google.csv`, `listings.xlsx`, `monthly unemployment rate.csv`, `ozone_nyc.csv`, `price.csv`, `stocks.csv`.
- Analysis: `DJI.csv`, `HRB.csv`, `AMZN.csv`.
- Visualization: `discoveries.csv`, `co2_levels.csv`, `airline_passengers.csv`, `meat.csv`, `employment.csv`.

Setup derives `sp500.csv` from the original `price.csv` SP500 column, aliases the original unemployment filename, and uses the same original four-asset prices for `asset.csv`. No observations are fabricated.

## Verified replacement snapshots

### gdp_growth.csv

[Official source](https://fred.stlouisfed.org/graph/fredgraph.csv?id=A191RL1Q225SBEA&cosd=2010-01-01&coed=2017-01-01). BEA/FRED real GDP percent change from the preceding quarter, seasonally adjusted annual rate. 29 quarterly observations, 2010 Q1–2017 Q1. Rename observation_date and A191RL1Q225SBEA to date and gdp_growth. The original tutorial screenshot starts earlier; this snapshot is the documented replacement, not an exact reproduction of that unavailable CSV.

- Raw download SHA-256: `82e72cf949d522e6f770c29ce8c8d311d876656797485c883007b52c05d8d20c`
- Committed snapshot SHA-256: `5173321a194285d3958c70e9c7dac9f285414df6087feecbf8aec6f1c109ec2a`

### new_york_temperature.csv

[Official source](https://www.ncei.noaa.gov/data/global-summary-of-the-year/access/USW00094728.csv). NOAA Global Summary of the Year, New York City Central Park station USW00094728. Select DATE 1870–2016 inclusive: 147 annual TAVG observations. Convert Celsius to Fahrenheit with TAVG × 1.8 + 32, round to one decimal and name AVG. DATE is an integer year. Annual level forecasts cover 2017–2046; this is a historical model exercise, not new temperature observations.

- Raw download SHA-256: `26b6058b6cbe90890ddff695c9e8827f765b338ef39407b5a1d519a9eeaf221b`
- Committed snapshot SHA-256: `a441555f74d927bb1280abade71e63e693a153168bede758c8b844de7a1efa4c`

The original author repository and local inventory do not contain the two missing CSVs. These replacements were explicitly approved by the user. Do not describe their outputs as reproductions of the original screenshots.

## Additional original inputs for Parts 4–6

All files below are downloaded at the same immutable author revision and verified by setup. No CSV replacement was necessary. Original records are retained; Amazon is sorted chronologically after loading.

| Original path | SHA-256 |
| --- | --- |
| `Arima Models in Python/candy_production.csv` | `6b09ba45d482a23459499b98006d2e4911f31a06ded14ac2a1192dd5279c9056` |
| `Arima Models in Python/amazon_close.csv` | `f73498d0e1efa5cf9936bd4d2f810259c67ef39b3436f406b194de778fdf40ec` |
| `Arima Models in Python/co2.csv` | `a777e6a6000ff2dbf9bc12ff652a73a59b3d9c9e459f4330c3fd2574c6768b5c` |
| `Arima Models in Python/earthquakes.csv` | `0d6e92b04f0337d13ea6055785032189763652ee4ec4bffbd80961964d6bbff9` |
| `Machine Learning For Time Series/prices.csv` | `d6fbdd4831ec8fd5884a690740d38bfc9dff44cfde0decc78ba122e70f58ebf6` |
| `Machine Learning For Time Series/preprocessed_prices.csv` | `23e45fb2fbba7cc93ede87805546df86cba5531e82cc8e3cbdb4d63ddab3b176` |
