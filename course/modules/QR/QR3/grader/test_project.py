"""Acceptance test suite for Atlas A17: Machine Learning Pipeline (atlas.ml).

Tests mathematical invariants, point-in-time temporal causality,
purged cross-validation boundaries, coordinate descent soft-thresholding,
TreeSHAP additivity, and model lifecycle governance across seeded instances.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance

try:
    from atlas.ml import (
        CombinatorialPurgedCV,
        DecisionTreeRegressor,
        FeatureStore,
        GradientBoostingRegressor,
        LassoRegressor,
        ModelLifecycleState,
        ModelRegistry,
        NeuralNetworkRegressor,
        PurgedKFold,
        RandomForestRegressor,
        RidgeRegressor,
        TreeSHAPExplainer,
        evaluate_ml_strategy,
    )
except ImportError:
    from reference import (
        CombinatorialPurgedCV,
        DecisionTreeRegressor,
        FeatureStore,
        GradientBoostingRegressor,
        LassoRegressor,
        ModelLifecycleState,
        ModelRegistry,
        NeuralNetworkRegressor,
        PurgedKFold,
        RandomForestRegressor,
        RidgeRegressor,
        TreeSHAPExplainer,
        evaluate_ml_strategy,
    )


@pytest.fixture
def inst() -> dict[str, Any]:
    seed_str = os.environ.get("ATLAS_SEED", "0")
    seed = int(seed_str)
    return make_instance(seed)


# ---------------------------------------------------------------------------
# 1. Feature Store & As-Of Point-in-Time Causality Tests
# ---------------------------------------------------------------------------


def test_feature_store_causality_and_as_of_join(inst: dict[str, Any]) -> None:
    store = FeatureStore()
    events = inst["store_events"]
    assert isinstance(events, list)

    for ev in events:
        store.add_feature_record(
            entity_id=ev["entity_id"],
            timestamp=ev["timestamp"],
            feature_name=ev["feature_name"],
            value=ev["value"],
        )

    # Test causality explicitly with controlled sequence
    store.register_entity("CAUSAL_TEST_ASSET")
    store.add_feature_record("CAUSAL_TEST_ASSET", 10.0, "price_feat", 100.0)
    store.add_feature_record("CAUSAL_TEST_ASSET", 20.0, "price_feat", 200.0)

    # Query before first observation must be NaN
    val_early = store.get_point_in_time("CAUSAL_TEST_ASSET", 5.0, ["price_feat"])["price_feat"]
    assert math.isnan(val_early)

    # Query at t=15 must be exactly 100.0 (cannot see future record at t=20)
    val_mid = store.get_point_in_time("CAUSAL_TEST_ASSET", 15.0, ["price_feat"])["price_feat"]
    assert math.isclose(val_mid, 100.0, abs_tol=1e-8), f"Lookahead detected: expected 100.0, got {val_mid}"

    # As-of join test
    query_keys = inst["query_keys"]
    feature_names = inst["feature_names"]
    assert isinstance(query_keys, list) and isinstance(feature_names, list)

    matrix = store.as_of_join(query_keys, feature_names)
    assert matrix.shape == (len(query_keys), len(feature_names))

    with pytest.raises(ValueError):
        store.get_point_in_time("NON_EXISTENT_ASSET_XYZ", 100.0)


# ---------------------------------------------------------------------------
# 2. Cross-Validation Purging and Embargo Tests
# ---------------------------------------------------------------------------


def test_purged_kfold_no_overlap_and_embargo(inst: dict[str, Any]) -> None:
    n_samples = int(inst["n_samples"])
    n_splits = int(inst["cv_n_splits"])
    lookahead = int(inst["label_lookahead"])
    embargo_pct = float(inst["embargo_pct"])

    cv = PurgedKFold(n_splits=n_splits, label_lookahead=lookahead, embargo_pct=embargo_pct)
    splits = cv.split(n_samples)

    assert len(splits) == n_splits
    h_embargo = math.ceil(embargo_pct * n_samples)

    all_test_indices = []
    for train_idx, test_idx in splits:
        assert len(test_idx) > 0
        all_test_indices.extend(test_idx.tolist())

        test_start = int(test_idx[0])
        test_end = int(test_idx[-1])

        # Invariant 1: No test sample in train sample
        overlap = np.intersect1d(train_idx, test_idx)
        assert len(overlap) == 0

        # Invariant 2: Left purge enforcement
        for i in train_idx:
            msg = f"Purge violated: train index {i} overlaps test fold [{test_start}, {test_end}]"
            assert not (i <= test_end and i + lookahead - 1 >= test_start), msg

        # Invariant 3: Embargo enforcement
        for i in train_idx:
            msg = f"Embargo violated: train index {i} falls in window ({test_end}, {test_end + h_embargo}]"
            assert not (test_end < i <= test_end + h_embargo), msg

    assert sorted(all_test_indices) == list(range(n_samples))

    with pytest.raises(ValueError):
        PurgedKFold(n_splits=1)
    with pytest.raises(ValueError):
        PurgedKFold(label_lookahead=0)


def test_combinatorial_purged_cv_splits(inst: dict[str, Any]) -> None:
    n_samples = int(inst["n_samples"])
    n_groups = int(inst["cpcv_n_groups"])
    k_test = int(inst["cpcv_k_test_groups"])
    lookahead = int(inst["label_lookahead"])
    embargo_pct = float(inst["embargo_pct"])

    cpcv = CombinatorialPurgedCV(
        n_groups=n_groups,
        k_test_groups=k_test,
        label_lookahead=lookahead,
        embargo_pct=embargo_pct,
    )
    splits = cpcv.split(n_samples)

    expected_n_splits = math.comb(n_groups, k_test)
    assert len(splits) == expected_n_splits

    for train_idx, test_idx in splits:
        assert len(test_idx) > 0
        overlap = np.intersect1d(train_idx, test_idx)
        assert len(overlap) == 0


# ---------------------------------------------------------------------------
# 3. Regularized Linear Estimators (Ridge & Lasso)
# ---------------------------------------------------------------------------


def test_ridge_and_lasso_regularization(inst: dict[str, Any]) -> None:
    x_features = np.asarray(inst["X"], dtype=np.float64)
    y_target = np.asarray(inst["y"], dtype=np.float64)
    ridge_alpha = float(inst["ridge_alpha"])
    lasso_alpha = float(inst["lasso_alpha"])

    # Fit Ridge
    ridge = RidgeRegressor(alpha=ridge_alpha, fit_intercept=True)
    ridge.fit(x_features, y_target)
    ridge_preds = ridge.predict(x_features)
    assert len(ridge_preds) == len(y_target)
    assert np.all(np.isfinite(ridge_preds))
    assert ridge.coef_ is not None

    # L2 shrinkage test
    ridge_large = RidgeRegressor(alpha=ridge_alpha * 50.0, fit_intercept=True)
    ridge_large.fit(x_features, y_target)
    assert ridge_large.coef_ is not None
    assert np.linalg.norm(ridge_large.coef_) <= np.linalg.norm(ridge.coef_) + 1e-10

    # Fit Lasso
    lasso = LassoRegressor(alpha=lasso_alpha, fit_intercept=True)
    lasso.fit(x_features, y_target)
    lasso_preds = lasso.predict(x_features)
    assert len(lasso_preds) == len(y_target)
    assert np.all(np.isfinite(lasso_preds))
    assert lasso.coef_ is not None

    # Sparsity / L1 shrinkage test
    lasso_heavy = LassoRegressor(alpha=lasso_alpha * 30.0, fit_intercept=True)
    lasso_heavy.fit(x_features, y_target)
    assert lasso_heavy.coef_ is not None
    n_zeros_normal = int(np.sum(np.abs(lasso.coef_) < 1e-4))
    n_zeros_heavy = int(np.sum(np.abs(lasso_heavy.coef_) < 1e-4))
    assert n_zeros_heavy > 0, "Lasso with heavy regularization must drive coefficients to zero"
    assert n_zeros_heavy >= n_zeros_normal


# ---------------------------------------------------------------------------
# 4. Tree and Ensemble Estimators
# ---------------------------------------------------------------------------


def test_decision_tree_and_ensembles(inst: dict[str, Any]) -> None:
    x_features = np.asarray(inst["X"], dtype=np.float64)
    y_target = np.asarray(inst["y"], dtype=np.float64)
    max_depth = int(inst["tree_max_depth"])
    min_leaf = int(inst["tree_min_leaf"])

    # 1. Decision Tree
    tree = DecisionTreeRegressor(max_depth=max_depth, min_samples_leaf=min_leaf)
    tree.fit(x_features, y_target)
    tree_preds = tree.predict(x_features)
    assert len(tree_preds) == len(y_target)
    assert np.all(np.isfinite(tree_preds))

    # 2. Random Forest
    rf = RandomForestRegressor(n_estimators=5, max_depth=max_depth, min_samples_leaf=min_leaf, seed=123)
    rf.fit(x_features, y_target)
    rf_preds = rf.predict(x_features)
    assert len(rf_preds) == len(y_target)
    assert np.all(np.isfinite(rf_preds))

    # 3. Gradient Boosting
    gbdt = GradientBoostingRegressor(n_estimators=8, learning_rate=0.1, max_depth=2, min_samples_leaf=min_leaf)
    gbdt.fit(x_features, y_target)
    gbdt_preds = gbdt.predict(x_features)
    assert len(gbdt_preds) == len(y_target)
    assert np.all(np.isfinite(gbdt_preds))

    # 4. Neural Network
    nn = NeuralNetworkRegressor(hidden_layers=[12, 6], learning_rate=0.01, l2_reg=1e-3, epochs=25, seed=42)
    nn.fit(x_features, y_target)
    nn_preds = nn.predict(x_features)
    assert len(nn_preds) == len(y_target)
    assert np.all(np.isfinite(nn_preds))


# ---------------------------------------------------------------------------
# 5. TreeSHAP Additivity Test
# ---------------------------------------------------------------------------


def test_tree_shap_local_additivity(inst: dict[str, Any]) -> None:
    x_features = np.asarray(inst["X"], dtype=np.float64)
    y_target = np.asarray(inst["y"], dtype=np.float64)
    max_depth = int(inst["tree_max_depth"])
    min_leaf = int(inst["tree_min_leaf"])
    query_x = np.asarray(inst["shap_query_x"], dtype=np.float64)

    tree = DecisionTreeRegressor(max_depth=max_depth, min_samples_leaf=min_leaf)
    tree.fit(x_features, y_target)

    explainer = TreeSHAPExplainer(tree)
    phi = explainer.explain(query_x)

    assert len(phi) == x_features.shape[1]
    assert np.all(np.isfinite(phi))

    # Local additivity axiom: phi_0 + sum(phi) == f(x)
    pred_val = float(tree.predict(query_x.reshape(1, -1))[0])
    total_shap = explainer.expected_value + float(np.sum(phi))

    err_msg = f"TreeSHAP additivity violated: base {explainer.expected_value} + sum {np.sum(phi)} != pred {pred_val}"
    assert math.isclose(total_shap, pred_val, abs_tol=1e-7), err_msg


# ---------------------------------------------------------------------------
# 6. Model Registry Lifecycle Governance
# ---------------------------------------------------------------------------


def test_model_registry_governance(inst: dict[str, Any]) -> None:
    registry = ModelRegistry()
    m_name = str(inst["model_name"])
    metadata = dict(inst["model_metadata"])

    dummy_model = {"weights": [1.0, 2.0]}
    registry.register_model(m_name, dummy_model, metadata)

    _, _, state = registry.get_model(m_name)
    assert state == ModelLifecycleState.DRAFT

    # Illegal transition: DRAFT -> DEPLOYED must raise ValueError
    with pytest.raises(ValueError):
        registry.transition_state(m_name, ModelLifecycleState.DEPLOYED)

    # Legal transition: DRAFT -> VALIDATED
    registry.transition_state(m_name, ModelLifecycleState.VALIDATED)
    _, _, state = registry.get_model(m_name)
    assert state == ModelLifecycleState.VALIDATED

    # Legal transition: VALIDATED -> DEPLOYED
    registry.transition_state(m_name, ModelLifecycleState.DEPLOYED)
    _, _, state = registry.get_model(m_name)
    assert state == ModelLifecycleState.DEPLOYED

    # Legal transition: DEPLOYED -> RETIRED
    registry.transition_state(m_name, ModelLifecycleState.RETIRED)
    _, _, state = registry.get_model(m_name)
    assert state == ModelLifecycleState.RETIRED

    with pytest.raises(ValueError):
        registry.register_model(m_name, dummy_model, metadata)


# ---------------------------------------------------------------------------
# 7. Pipeline Strategy Evaluation with Strictly Positive Lag
# ---------------------------------------------------------------------------


def test_strategy_evaluation_lag_enforcement(inst: dict[str, Any]) -> None:
    y_target = np.asarray(inst["y"], dtype=np.float64)
    fwd = np.asarray(inst["forward_returns"], dtype=np.float64)

    # Lag 0 must be rejected
    with pytest.raises(ValueError):
        evaluate_ml_strategy(y_target, fwd, lag=0)

    # Valid lag >= 1
    metrics = evaluate_ml_strategy(y_target, fwd, lag=1)
    assert "oos_r2" in metrics
    assert "sharpe" in metrics
    assert "mean_return" in metrics
    assert "volatility" in metrics
    assert "max_drawdown" in metrics
    assert math.isfinite(metrics["sharpe"])
