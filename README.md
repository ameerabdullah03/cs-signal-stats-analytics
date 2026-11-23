# Signal & Stats Analytics

A reproducible CSV analysis tool for paired numeric observations. It reports descriptive statistics, Pearson correlation, a simple least-squares line, RMSE, and R². The included dataset is synthetic and deliberately small so the calculations can be followed.

## Course connection

Probability and Statistics, Linear Algebra, Numerical Computing and Lab, Database Management System.

## Run

```bash
python analyze.py sample.csv --x study_hours --y score
```

CSV columns must contain finite numeric values. The tool prints row count, means, sample standard deviations, covariance, correlation, regression equation, and in-sample fit metrics. No external dependencies or network access are needed.

## Interpretation

Correlation and regression describe association in the supplied sample. They do not establish causation, and in-sample fit is not a measure of future predictive performance. For a real portfolio analysis, replace the synthetic sample with a dataset you are allowed to publish, document its source and license, and use a held-out evaluation split.
