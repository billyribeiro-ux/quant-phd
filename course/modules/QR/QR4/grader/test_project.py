"""Acceptance test suite for QR4 project (Contamination-Safe Text Signal).

Tests mathematical invariants, point-in-time filing store causality,
Loughran-McDonald sublinear tone calculation, cross-sectional standardization,
and permutation contamination diagnostics across seeded instances.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance

try:
    from text_signal import (
        ContaminationAuditor,
        CrossSectionalSignalEngine,
        PointInTimeFilingStore,
        compute_sublinear_tone,
        tokenize,
    )
except ImportError:
    from reference import (
        ContaminationAuditor,
        CrossSectionalSignalEngine,
        PointInTimeFilingStore,
        compute_sublinear_tone,
        tokenize,
    )


@pytest.fixture
def inst() -> dict[str, Any]:
    seed_str = os.environ.get("QF_SEED", os.environ.get("ATLAS_SEED", "0"))
    seed = int(seed_str)
    return make_instance(seed)


# ---------------------------------------------------------------------------
# 1. Tokenization and Sublinear Tone Tests
# ---------------------------------------------------------------------------


def test_tokenize_basic_and_validation() -> None:
    text = "The Company's revenue grew 25% year-over-year; operating profits improved!"
    tokens = tokenize(text)
    assert "revenue" in tokens
    assert "grew" in tokens
    assert "operating" in tokens
    assert "profits" in tokens
    assert "improved" in tokens
    # Numbers and single characters should be filtered
    assert "25" not in tokens
    assert "s" not in tokens

    with pytest.raises(ValueError):
        tokenize(12345)


def test_compute_sublinear_tone_invariants() -> None:
    pos = {"profitable", "growth", "exceeded"}
    neg = {"loss", "default", "impairment"}

    # Pure neutral / empty
    assert compute_sublinear_tone([], pos, neg) == 0.0
    assert compute_sublinear_tone(["operating", "capital"], pos, neg) == 0.0

    # Symmetric counts -> tone == 0.0
    tokens_sym = ["growth", "loss"]
    assert math.isclose(compute_sublinear_tone(tokens_sym, pos, neg), 0.0, abs_tol=1e-6)

    # Sublinear scaling: 4 occurrences of 'growth' should weigh 1 + ln(4) ≈ 2.386, NOT 4.0
    tokens_single = ["growth"]
    tokens_repeated = ["growth", "growth", "growth", "growth"]
    tone_single = compute_sublinear_tone(tokens_single, pos, neg)
    tone_repeated = compute_sublinear_tone(tokens_repeated, pos, neg)
    assert tone_single > 0.99  # Pure positive
    assert tone_repeated > 0.99  # Pure positive

    # Mixed with repeated words
    # pos weight: 1 + ln(4) ≈ 2.38629
    # neg weight: 1.0 (single 'loss')
    # tone should equal (2.38629 - 1.0) / (2.38629 + 1.0) ≈ 1.38629 / 3.38629 ≈ 0.40938
    tokens_mixed = ["growth", "growth", "growth", "growth", "loss"]
    tone_mixed = compute_sublinear_tone(tokens_mixed, pos, neg)
    expected_tone = (1.0 + math.log(4) - 1.0) / (1.0 + math.log(4) + 1.0)
    assert math.isclose(tone_mixed, expected_tone, rel_tol=1e-4)

    # Input validation
    with pytest.raises(ValueError):
        compute_sublinear_tone("not a list", pos, neg)
    with pytest.raises(ValueError):
        compute_sublinear_tone(["growth"], ["not a set"], neg)


# ---------------------------------------------------------------------------
# 2. Point-in-Time Filing Store Tests
# ---------------------------------------------------------------------------


def test_filing_store_validation_and_causality() -> None:
    store = PointInTimeFilingStore()

    with pytest.raises(ValueError):
        store.add_filing("", "2023-01-15", "Valid text")
    with pytest.raises(ValueError):
        store.add_filing("AAPL", "2023/01/15", "Invalid date format")
    with pytest.raises(ValueError):
        store.add_filing("AAPL", "2023-01-15", "")

    store.add_filing("AAPL", "2023-01-15", "Q1 filing strong growth")
    store.add_filing("AAPL", "2023-04-15", "Q2 filing profitable expansion")
    store.add_filing("AAPL", "2023-07-15", "Q3 filing operating loss")

    # Strict causality: query at 2023-04-15 under execution_lag_days=1 CANNOT see the 2023-04-15 filing
    accessible = store.get_as_of_filings("AAPL", "2023-04-15", execution_lag_days=1)
    assert len(accessible) == 1
    assert accessible[0]["filing_date"] == "2023-01-15"

    latest = store.get_latest_filing("AAPL", "2023-04-15", execution_lag_days=1)
    assert latest is not None
    assert latest["filing_date"] == "2023-01-15"

    # Query before any filing returns empty list / None
    assert store.get_as_of_filings("AAPL", "2022-12-31") == []
    assert store.get_latest_filing("AAPL", "2022-12-31") is None

    # Invalid query date or lag
    with pytest.raises(ValueError):
        store.get_as_of_filings("AAPL", "invalid-date")
    with pytest.raises(ValueError):
        store.get_as_of_filings("AAPL", "2023-05-01", execution_lag_days=0)


# ---------------------------------------------------------------------------
# 3. Cross-Sectional Signal Engine Tests
# ---------------------------------------------------------------------------


def test_cross_sectional_scores_invariants(inst: dict[str, Any]) -> None:
    store = PointInTimeFilingStore()
    for f in inst["filings"]:
        store.add_filing(f["ticker"], f["filing_date"], f["content"])

    engine = CrossSectionalSignalEngine(store, set(inst["pos_words"]), set(inst["neg_words"]))
    tickers = inst["tickers"]
    query_date = inst["query_date"]

    scores = engine.compute_cross_sectional_scores(tickers, query_date)
    assert len(scores) == len(tickers)

    vals = np.array([scores[t] for t in tickers], dtype=np.float64)

    # Invariant: cross-sectional z-scores must have mean 0.0 within float tolerance
    assert math.isclose(float(np.mean(vals)), 0.0, abs_tol=1e-7)

    # Invariant: sample standard deviation must equal 1.0 (if variance > 0)
    std_val = float(np.std(vals))
    if std_val > 1e-4:
        assert math.isclose(std_val, 1.0, abs_tol=1e-5)

    # Missing filings should raise ValueError
    with pytest.raises(ValueError):
        engine.compute_cross_sectional_scores(["UNKNOWN_TICKER"], query_date)


# ---------------------------------------------------------------------------
# 4. Contamination Auditor Tests
# ---------------------------------------------------------------------------


def test_contamination_split_performance(inst: dict[str, Any]) -> None:
    auditor = ContaminationAuditor()
    results = auditor.evaluate_split_performance(
        inst["signals_history"],
        inst["returns_history"],
        inst["cutoff_date"],
    )

    assert "pre_ic" in results
    assert "post_ic" in results
    assert "ic_decay" in results
    assert "is_contaminated" in results

    # Instance pretraining period was constructed with high correlation that vanishes post-cutoff
    assert results["pre_ic"] > 0.15
    assert results["post_ic"] < results["pre_ic"]
    assert results["ic_decay"] > 0.50
    assert results["is_contaminated"] is True


def test_permutation_test_properties(inst: dict[str, Any]) -> None:
    auditor = ContaminationAuditor()

    # Strong signal should yield tiny p-value (< 0.05)
    res_strong = auditor.run_time_permutation_test(
        inst["sig_1d"],
        inst["ret_1d_strong"],
        n_permutations=200,
        seed=inst["seed"],
    )
    assert res_strong["observed_corr"] > 0.50
    assert res_strong["perm_pvalue"] < 0.05
    assert math.isclose(res_strong["null_mean"], 0.0, abs_tol=0.15)

    # Null signal should yield high p-value (> 0.05)
    res_null = auditor.run_time_permutation_test(
        inst["sig_1d"],
        inst["ret_1d_null"],
        n_permutations=200,
        seed=inst["seed"],
    )
    assert res_null["perm_pvalue"] > 0.05

    # Validation: mismatched lengths
    with pytest.raises(ValueError):
        auditor.run_time_permutation_test(np.array([1.0, 2.0]), np.array([1.0]))
