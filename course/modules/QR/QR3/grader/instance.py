"""Deterministic instance generator for QR3 project (Atlas A17: ML Pipeline).

Generates seeded financial feature panels, point-in-time entity event streams,
cross-validation partitioning benchmarks, and model registry artifacts.
"""

from __future__ import annotations

import functools
from typing import Any

import numpy as np


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic ML pipeline verification instance for the given seed."""
    rng = np.random.default_rng(seed)

    n_samples = 240 + int(rng.integers(0, 60))  # 240 to 300 observations
    n_features = 8 + int(rng.integers(0, 4))  # 8 to 12 features

    # 1. Feature matrix with collinearity and factor structure
    latent_factors = rng.normal(0.0, 1.0, size=(n_samples, 3))
    factor_loadings = rng.normal(0.0, 1.0, size=(3, n_features))
    idiosyncratic_noise = rng.normal(0.0, 0.5, size=(n_samples, n_features))
    x_raw = latent_factors @ factor_loadings + idiosyncratic_noise

    # Standardize features
    x_mean = np.mean(x_raw, axis=0)
    x_std = np.std(x_raw, axis=0)
    x_std[x_std < 1e-8] = 1.0
    x_features = (x_raw - x_mean) / x_std

    # 2. Target return with low signal-to-noise ratio and nonlinear interactions
    beta = np.zeros(n_features)
    beta[0] = float(rng.uniform(0.15, 0.35))
    beta[1] = -float(rng.uniform(0.15, 0.35))
    nonlinear_signal = 0.20 * x_features[:, 0] * x_features[:, 2] if n_features > 2 else 0.0
    linear_signal = x_features @ beta
    signal = linear_signal + nonlinear_signal

    noise_scale = float(rng.uniform(1.2, 1.8))
    noise = rng.normal(0.0, noise_scale, size=n_samples)
    y_target = signal + noise

    # 3. Feature store entity event streams
    entities = ["ASSET_A", "ASSET_B", "ASSET_C", "ASSET_D"]
    feature_names = [f"feat_{j}" for j in range(4)]
    store_events: list[dict[str, Any]] = []

    for entity in entities:
        base_val = float(rng.uniform(10.0, 50.0))
        n_events = 30 + int(rng.integers(0, 20))
        event_times = np.sort(rng.choice(n_samples * 2, size=n_events, replace=False))
        curr_val = base_val
        for t in event_times:
            for feat in feature_names:
                curr_val += float(rng.normal(0.0, 1.0))
                store_events.append(
                    {
                        "entity_id": entity,
                        "timestamp": int(t),
                        "feature_name": feat,
                        "value": float(curr_val),
                    }
                )

    # Queries for as-of join
    n_queries = 20
    query_entities = [str(rng.choice(entities)) for _ in range(n_queries)]
    query_times = [int(rng.integers(10, n_samples * 2)) for _ in range(n_queries)]
    query_keys = list(zip(query_entities, query_times, strict=True))

    # 4. Cross-validation parameters
    cv_n_splits = 5
    label_lookahead = 3 + int(rng.integers(0, 3))  # 3 to 5 bars
    embargo_pct = 0.02

    cpcv_n_groups = 6
    cpcv_k_test_groups = 2

    # 5. Hyperparameters for estimators
    ridge_alpha = float(rng.uniform(0.5, 2.0))
    lasso_alpha = float(rng.uniform(0.05, 0.15))
    tree_max_depth = 3
    tree_min_leaf = 5

    # 6. Test query vector for TreeSHAP local attribution
    shap_query_idx = int(rng.integers(0, n_samples))
    shap_query_x = x_features[shap_query_idx, :]

    # 7. Model registry metadata
    model_name = f"AlphaModel_v{seed}"
    model_metadata = {
        "seed": seed,
        "author": "AtlasResearcher",
        "features": [f"feat_{j}" for j in range(n_features)],
        "target": "forward_1d_return",
        "in_sample_mse": float(rng.uniform(0.5, 1.5)),
        "oos_r2": float(rng.uniform(0.01, 0.06)),
        "oos_sharpe": float(rng.uniform(0.8, 1.6)),
    }

    # 8. Out-of-sample forward returns for backtest integration
    forward_returns = rng.normal(0.0003, 0.015, size=n_samples)

    return {
        "seed": seed,
        "n_samples": n_samples,
        "n_features": n_features,
        "X": x_features,
        "y": y_target,
        "entities": entities,
        "feature_names": feature_names,
        "store_events": store_events,
        "query_keys": query_keys,
        "cv_n_splits": cv_n_splits,
        "label_lookahead": label_lookahead,
        "embargo_pct": embargo_pct,
        "cpcv_n_groups": cpcv_n_groups,
        "cpcv_k_test_groups": cpcv_k_test_groups,
        "ridge_alpha": ridge_alpha,
        "lasso_alpha": lasso_alpha,
        "tree_max_depth": tree_max_depth,
        "tree_min_leaf": tree_min_leaf,
        "shap_query_x": shap_query_x,
        "model_name": model_name,
        "model_metadata": model_metadata,
        "forward_returns": forward_returns,
    }
