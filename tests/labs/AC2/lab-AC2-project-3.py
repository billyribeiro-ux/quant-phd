import numpy as np

# SIMULATED firm-years for the modified Jones model (Dechow, Sloan & Sweeney 1995). Currency units. Not real firms.
SAMPLE = [
    {"total_accruals": -4.0e6, "lag_assets": 1.0e8, "d_revenue": 6.0e6, "d_receivables": 1.0e6, "ppe": 3.0e7},
    {"total_accruals": -2.5e6, "lag_assets": 8.0e7, "d_revenue": 3.0e6, "d_receivables": 0.5e6, "ppe": 2.4e7},
    {"total_accruals": -5.2e6, "lag_assets": 1.3e8, "d_revenue": 9.0e6, "d_receivables": 2.0e6, "ppe": 4.5e7},
    {"total_accruals": -1.1e6, "lag_assets": 5.0e7, "d_revenue": 1.5e6, "d_receivables": 0.2e6, "ppe": 1.1e7},
    {"total_accruals": 0.9e6, "lag_assets": 6.0e7, "d_revenue": -0.5e6, "d_receivables": 0.4e6, "ppe": 2.0e7},
    {"total_accruals": -3.3e6, "lag_assets": 9.0e7, "d_revenue": 4.0e6, "d_receivables": 1.2e6, "ppe": 3.2e7},
]

# Total accruals and each regressor are scaled by lagged assets; the model has no intercept.
lag = np.array([row["lag_assets"] for row in SAMPLE])
y = np.array([row["total_accruals"] for row in SAMPLE]) / lag
X = np.column_stack(
    [
        1.0 / lag,
        (np.array([row["d_revenue"] for row in SAMPLE]) - np.array([row["d_receivables"] for row in SAMPLE])) / lag,
        np.array([row["ppe"] for row in SAMPLE]) / lag,
    ]
)
coef = np.linalg.lstsq(X, y, rcond=None)[0]
fitted = X @ coef
print("coefficients (a1, a2, a3):", np.round(coef, 6).tolist())
print("discretionary (scaled):", np.round(y - fitted, 6).tolist())
print("rank of the design:", int(np.linalg.matrix_rank(X)))
