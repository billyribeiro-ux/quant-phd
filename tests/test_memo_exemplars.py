"""Every number in the S7 project's memo exemplars is pinned to the code that computes it.

The integrity memo (course/modules/S/S7/project.html, rung 3) is graded by rubric against annotated exemplars.
Each number an exemplar's memo text quotes sits in a ``<span data-num="<key>" data-format="<spec>">``; the key
names a value computed here from the code that produces it, and the format spec is the one the exemplar uses:

* the trial set: the project's Lab 3 twin (``tests/labs/S7/lab-S7-project-3.py``), which must build exactly the
  matrix of Lesson 8's Lab 4 twin;
* every integrity statistic: the A8 reference solution (``grader/reference.py``), called with the contract's
  defaults, as the memo specification requires of the student's own module;
* the effective number of trials: the Lesson 8 Lab 4 twin; the pure-noise PBO range: Lesson 8's Lab 2 output;
* the retrieval date: MANIFEST.json.

A regenerated value that changes therefore breaks this test. The memo text may contain no other digits, apart
from references to lessons, labs, sections and the milestone. The annotations must agree with the exemplar's
per-criterion scores, which the self-assessment form (assets/js/rubric.js) reveals.
"""

from __future__ import annotations

import contextlib
import functools
import importlib.util
import inspect
import io
import json
import math
import os
import re
import runpy
import sys
from collections import Counter
from pathlib import Path
from statistics import NormalDist
from types import ModuleType
from typing import Any

import numpy as np
import pytest

from coursekit import MARKET_DATA, ROOT, Node, load_page, twin_workdir

S7 = ROOT / "course" / "modules" / "S" / "S7"
TWINS = ROOT / "tests" / "labs" / "S7"
PROJECT = S7 / "project.html"
DSR_BAR = 0.95  # the exemplars' decision bar for the DSR: Lesson 7's conventional 0.95
S_CHECKS = (8, 10)  # the block counts the exemplars report as checks on PBO
BLOCK_CHECKS = (5.0, 20.0)  # the mean block lengths the exemplars report as checks on StepM
# References to course material, which the memo text may contain besides pinned numbers.
REFERENCE_TOKEN = re.compile(
    r"\b(?:L0[1-8]|A8|H\.10|Lab [1-6]|Lesson [1-8]|Section [1-9]|Problem [MPER][1-4]"
    r"|(?:Theorem|Proposition|Definition|Remark|Lemma|Misconception) [1-9](?:\.[1-9])?)\b|equation \([1-9]\)|\\SR_0"
)


@functools.cache
def reference() -> ModuleType:
    spec = importlib.util.spec_from_file_location("s7_memo_reference", S7 / "grader" / "reference.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolve their module while the class is built
    spec.loader.exec_module(module)
    return module


def run_twin(name: str) -> dict[str, Any]:
    """The globals of a lab twin, run as run_labs.py runs it: in a directory whose data/ holds fx_monthly.csv."""
    here = Path.cwd()
    with twin_workdir(("fx_monthly.csv",)) as work, contextlib.redirect_stdout(io.StringIO()):
        os.chdir(work)
        try:
            return runpy.run_path(str(TWINS / name))
        finally:
            os.chdir(here)


def joined(values: list[int]) -> str:
    """1, 3, 6 and 12."""
    return ", ".join(str(v) for v in values[:-1]) + f" and {values[-1]}"


@functools.cache
def values() -> dict[str, Any]:
    ref = reference()
    memo, lab4 = run_twin("lab-S7-project-3.py"), run_twin("lab-S7-L08-4.py")
    trials, pick, grid = memo["trials"], memo["pick"], memo["grid"]
    n_obs, n_trials = trials.shape
    defaults = {k: p.default for k, p in inspect.signature(ref.integrity_report).parameters.items() if k != "trials"}
    report = ref.integrity_report(ref.TrialSet(trials, pick, 12), **defaults)
    selected = trials[:, pick]
    sharpe = trials.mean(axis=0) / trials.std(axis=0, ddof=1)
    p_values = [1.0 - NormalDist().cdf(float(s) * math.sqrt(n_obs)) for s in sharpe]
    n_blocks = defaults["n_blocks"]
    manifest = {e["file"]: e for e in json.loads((MARKET_DATA / "MANIFEST.json").read_text())["datasets"]}
    lab2 = load_page(S7 / "L08.html").dom.first(None, None, id="lab-S7-L08-2")
    expected = lab2.first("pre", "expected") if lab2 is not None else None
    largest = re.search(r"largest (\d+\.\d+)", expected.text() if expected is not None else "")
    assert largest is not None, "Lesson 8's Lab 2 output no longer reports its largest pure-noise PBO"
    months = memo["months"]

    def checked_rejections(mean_block: float) -> int:
        return int(ref.romano_wolf(trials, defaults["alpha"], defaults["n_boot"], mean_block, defaults["seed"]).sum())

    file_months = [row[0] for row in memo["rows"][1:]]
    return {
        "retrieved": manifest["fx_monthly.csv"]["retrieved"],
        "n_currencies": len(memo["currencies"]),
        "prices_from": months[0],
        "window_start": months[memo["first"]],
        "window_end": months[-1],
        "file_start": file_months[0],
        "holdout_end": file_months[memo["start"] - 1],
        "holdout_currencies": int((~np.isnan(memo["prices"][0])).sum()),
        "lookbacks": joined(sorted({lb for lb, _, _ in grid})),
        "holdings": joined(sorted({h for _, h, _ in grid})),
        "n_trials": report.n_trials,
        "n_obs": n_obs,
        "periods_per_year": 12,
        "selected_label": memo["labels"][pick],
        "sr_month": report.selected_sharpe,
        "sr_ann": report.selected_sharpe_annualized,
        "sr_median_ann": float(np.median(sharpe)) * math.sqrt(12),
        "sr_min_ann": float(sharpe.min()) * math.sqrt(12),
        "mean_ann": float(selected.mean()) * 12,
        "vol_ann": float(selected.std(ddof=1)) * math.sqrt(12),
        "skew": ref.sample_skewness(selected),
        "kurt": ref.sample_kurtosis(selected),
        "psr": report.psr,
        "psr_p": 1.0 - report.psr,
        "sr_sd": math.sqrt(float(np.var(sharpe, ddof=1))),
        "sr0": report.expected_max_sharpe,
        "sr0_ann": report.expected_max_sharpe * math.sqrt(12),
        "dsr": report.dsr,
        "dsr_p": 1.0 - report.dsr,
        "dsr_bar": DSR_BAR,
        "pbo": report.pbo,
        "pbo_null": math.floor((n_trials + 1) / 2) / n_trials,
        "n_blocks": n_blocks,
        "n_splits": math.comb(n_blocks, n_blocks // 2),
        "block_months": n_obs // n_blocks,
        "rows_dropped": n_obs % n_blocks,
        "s_check_1": S_CHECKS[0],
        "s_check_2": S_CHECKS[1],
        "pbo_check_1": ref.probability_of_backtest_overfitting(trials, S_CHECKS[0]).pbo,
        "pbo_check_2": ref.probability_of_backtest_overfitting(trials, S_CHECKS[1]).pbo,
        "lab2_null_max": float(largest.group(1)),
        "alpha": defaults["alpha"],
        "q": defaults["q"],
        "n_boot": defaults["n_boot"],
        "mean_block": defaults["mean_block"],
        "seed": defaults["seed"],
        "stepm_rejections": int(report.romano_wolf_rejections.sum()),
        "bh_rejections": int(report.bh_rejections.sum()),
        "block_check_1": BLOCK_CHECKS[0],
        "block_check_2": BLOCK_CHECKS[1],
        "stepm_check_1": checked_rejections(BLOCK_CHECKS[0]),
        "stepm_check_2": checked_rejections(BLOCK_CHECKS[1]),
        "p_min": min(p_values),
        "p_min_count": sum(p <= defaults["q"] for p in p_values),
        "rho": lab4["rho"],
        "n_pr": lab4["participation"],
        "n_eff": lab4["n_eff"],
        "sr0_eff": lab4["sr0_eff"],
        "dsr_eff": lab4["psr"](lab4["selected"], lab4["sr0_eff"]),
    }


def shown(value: Any, spec: str) -> str:
    """The value as an exemplar shows it: through its format spec, with a typographic minus."""
    text = format(value, spec) if spec else str(value)
    return text.replace("-", "−") if isinstance(value, int | float) else text


def exemplars() -> list[Node]:
    found = load_page(PROJECT).dom.select("article", "exemplar")
    assert len(found) >= 2, "the project needs exemplars at two or more levels"
    return found


def test_the_memo_trial_set_is_lesson_8_lab_4s() -> None:
    memo, lab4 = run_twin("lab-S7-project-3.py"), run_twin("lab-S7-L08-4.py")
    assert np.array_equal(memo["trials"], lab4["trials"]), "the project's Lab 3 must rebuild Lab 4's matrix"
    assert memo["pick"] == lab4["pick"]


def test_the_reference_module_agrees_with_lesson_8_lab_4() -> None:
    v, lab4 = values(), run_twin("lab-S7-L08-4.py")
    assert math.isclose(v["dsr"], lab4["psr"](lab4["selected"], lab4["sr0"]), rel_tol=1e-12)
    assert math.isclose(v["pbo"], lab4["pbo"](lab4["trials"], v["n_blocks"]), rel_tol=1e-12)


def test_every_exemplar_number_is_pinned_to_its_computation() -> None:
    v = values()
    checked = 0
    for exemplar in exemplars():
        for span in exemplar.select(None, None, data_num=None):
            key, spec = span.get("data-num"), span.get("data-format")
            assert key in v, f"{exemplar.get('id')}: data-num {key!r} names no computed value"
            assert span.text() == shown(v[key], spec), (
                f"{exemplar.get('id')}: {key} shows {span.text()!r}, the computation gives {shown(v[key], spec)!r}"
            )
            checked += 1
    assert checked >= 40, f"only {checked} pinned numbers: the exemplars should quote their evidence"


def test_memo_text_has_no_unpinned_digits() -> None:
    def text_without_pins(node: Node) -> str:
        if node.get("data-num"):
            return " "
        return "".join(c if isinstance(c, str) else text_without_pins(c) for c in node.children)

    for exemplar in exemplars():
        memo = exemplar.select(None, "memo-text")
        assert memo, f"{exemplar.get('id')}: memo passages need class memo-text"
        for passage in memo:
            text = REFERENCE_TOKEN.sub(" ", text_without_pins(passage))
            stray = re.findall(r"\S*\d\S*", text)
            assert not stray, f"{exemplar.get('id')}: unpinned numbers {stray} in “{text.strip()[:80]}…”"


def test_annotations_agree_with_the_exemplar_scores() -> None:
    page = load_page(PROJECT)
    rubric = page.dom.first("table", "rubric")
    assert rubric is not None
    criteria = [row.get("data-criterion") for row in rubric.select("tr", None, data_criterion=None)]
    assert len(criteria) == len(rubric.select("tr")) - 1, "every rubric row needs data-criterion"
    levels = []
    for exemplar in exemplars():
        name = exemplar.get("id")
        scores = [int(x) for x in exemplar.get("data-scores").split(",")]
        assert len(scores) == len(criteria), f"{name}: data-scores needs one level per criterion"
        assert all(1 <= s <= 4 for s in scores)
        assert int(exemplar.get("data-level")) == Counter(scores).most_common(1)[0][0], (
            f"{name}: data-level must be the level it reaches most often"
        )
        levels.append(int(exemplar.get("data-level")))
        for passage in exemplar.select(None, "passage"):
            assert passage.select("li", None, data_criterion=None), f"{name}: every passage needs an annotation"
        notes = exemplar.select("li", None, data_criterion=None)
        for criterion, score in zip(criteria, scores, strict=True):
            mine = [n for n in notes if n.get("data-criterion") == criterion]
            meets = [int(n.get("data-level")) for n in mine if "meets" in n.classes]
            misses = [int(n.get("data-level")) for n in mine if "misses" in n.classes]
            assert meets or misses, f"{name}: no annotation on {criterion}"
            reached = max(meets, default=1)
            assert reached == score, f"{name}: {criterion} meets level {reached}, scored {score}"
            assert all(m > score for m in misses), f"{name}: {criterion} misses a level at or below its score {score}"
    assert len(set(levels)) >= 2, "exemplars at two or more levels"


@pytest.mark.parametrize("key", ["dsr", "pbo", "psr", "sr_ann", "n_trials", "stepm_rejections", "bh_rejections"])
def test_each_required_number_appears_in_the_strongest_exemplar(key: str) -> None:
    best = max(exemplars(), key=lambda e: int(e.get("data-level")))
    assert any(s.get("data-num") == key for s in best.select(None, None, data_num=None)), key
