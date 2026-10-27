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
