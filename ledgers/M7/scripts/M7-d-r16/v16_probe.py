"""Round-16 verifier probes for M7 slice d (reference start handling, certificate, equivalence sweep).

Independent of the reference's own certificate code: residuals are recomputed here in exact Fractions from the
project page definitions (project.html:309-321), from the float weights and float multipliers a solver returns.
Run from the repository root: .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/v16_probe.py
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M7/grader"
EQUIV = ROOT / "ledgers/M7/equivalent"
MUTANTS = ROOT / "ledgers/M7/mutants"


def load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


REF = load(GRADER / "reference.py", "ref_m7d")
F = Fraction


def fr(x: float) -> Fraction:
    return Fraction(x)


def recomputed(case: dict[str, Any], out: dict[str, Any]) -> dict[str, Fraction]:
    """Page definitions (project.html:309-321), exact in the floats the solver returned."""
    n = len(case["mu"])
    gamma = fr(case["gamma"])
    sigma = [[fr(x) for x in row] for row in case["sigma"]]
    mu = [fr(x) for x in case["mu"]]
    w = [fr(x) for x in out["weights"]]
    w0 = [fr(x) for x in case["w0"]]
    lo = [fr(x) for x in case["lower"]]
    up = [fr(x) for x in case["upper"]]
    caps = [fr(x) for x in case["sector_caps"]]
    sec = case["sector"]
    tau = fr(case["turnover_limit"])
    m = out["multipliers"]
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    ssum = [sum((w[i] for i in range(n) if sec[i] == k), F(0)) for k in range(len(caps))]
    gl = [lo[i] - w[i] for i in range(n)]
    gu = [w[i] - up[i] for i in range(n)]
    gs = [ssum[k] - caps[k] for k in range(len(caps))]
    gp = [d[i] - t[i] for i in range(n)]
    gm = [-d[i] - t[i] for i in range(n)]
    gt = sum(t, F(0)) - tau
    primal = max([F(0), abs(sum(w, F(0)) - 1), *gl, *gu, *gs, gt])
    nu = fr(m["budget"])
    lam_l = [fr(x) for x in m["lower"]]
    lam_u = [fr(x) for x in m["upper"]]
    eta = [fr(x) for x in m["sector"]]
    al = [fr(x) for x in m["turnover_plus"]]
    be = [fr(x) for x in m["turnover_minus"]]
    kap = fr(m["turnover_total"])
    stat = F(0)
    for i in range(n):
        gw = gamma * sum((sigma[i][j] * w[j] for j in range(n)), F(0)) - mu[i]
        rw = gw + nu - lam_l[i] + lam_u[i] + eta[sec[i]] + al[i] - be[i]
        rt = kap - al[i] - be[i]
        stat = max(stat, abs(rw), abs(rt))
    dual = max(F(0), -min([*lam_l, *lam_u, *eta, *al, *be, kap]))
    comp = max(
        abs(p * g)
        for p, g in zip(
            [*lam_l, *lam_u, *eta, *al, *be, kap], [*gl, *gu, *gs, *gp, *gm, gt], strict=True
        )
    )
    return {"primal": primal, "stationarity": stat, "dual": dual, "complementary": comp, "budget_gap": abs(sum(w, F(0)) - 1)}


def check(case: dict[str, Any], out: dict[str, Any]) -> tuple[bool, dict[str, float]]:
    rec = recomputed(case, out)
    rep = out["certificate"]
    agree = max(
        abs(F(rep["primal_residual"]) - rec["primal"]),
        abs(F(rep["stationarity_residual"]) - rec["stationarity"]),
        abs(F(rep["dual_residual"]) - rec["dual"]),
        abs(F(rep["complementary_slackness"]) - rec["complementary"]),
    )
    feas = max(rec["primal"], rec["stationarity"], rec["dual"], rec["complementary"])
    ok = feas <= F(1, 10**8) and agree <= F(1, 10**9)
    return ok, {"feas": float(feas), "agree": float(agree), "budget_gap": float(rec["budget_gap"])}


def case_of(**over: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "label": "SIMULATED probe case",
        "gamma": 1.0,
        "mu": [1000.0, 0.0],
        "sigma": [[1.0, 0.0], [0.0, 1.0]],
        "w0": [0.5, 0.5],
        "lower": [-1.0, -1.0],
        "upper": [2.0, 2.0],
        "sector": [0, 0],
        "sector_caps": [2.0],
        "turnover_limit": 2.0,
    }
    base.update(over)
    return base


def show(title: str, case: dict[str, Any]) -> None:
    try:
        out = REF.allocate(case)
    except Exception as exc:  # report, do not hide
        print(f"[{title}] raised {type(exc).__name__}: {exc}")
        return
    ok, info = check(case, out)
    print(f"[{title}] weights={out['weights']} ok={ok} info={info}")
    print(f"[{title}] certificate={out['certificate']}")


def named_cases() -> None:
    print("== named probe cases (reference as shipped at e896b7a4) ==")
    show("A tau=1e-9 mu=[1000,0]", case_of(turnover_limit=1e-9))
    show("E upper0=1/2+1e-9 tau=2", case_of(upper=[0.5 + 1e-9, 2.0]))
    show("tau=1e-10 mu=[100,0]", case_of(turnover_limit=1e-10, mu=[100.0, 0.0]))
    # budget gap probe: start sums to 1+1e-9 (accepted) and asset 0 sits 1e-9 under its lower bound (accepted), so the
    # snap raises asset 0 to its bound and the sum becomes 1+2e-9.
    show(
        "B1 budget gap 2e-9 via snap",
        case_of(mu=[0.0, 0.0], lower=[0.5, -1.0], w0=[0.5 - 1e-9, 0.5 + 2e-9], turnover_limit=2.0),
    )
    # start sums to 1 - 1e-9 and asset 0 sits 1e-9 over its upper bound: the snap lowers asset 0, the sum becomes 1-2e-9.
    show(
        "B2 budget gap -2e-9 via snap",
        case_of(mu=[0.0, 0.0], upper=[0.5, 2.0], w0=[0.5 + 1e-9, 0.5 - 2e-9], turnover_limit=2.0),
    )
    # fallback: zero-tolerance turnover with a bound breach inside the tolerance
    show("F tau=0 lower breach 5e-10", case_of(mu=[0.0, 0.0], lower=[0.5 + 5e-10, -1.0], w0=[0.5, 0.5], turnover_limit=0.0))
    show("G tau=0 lower breach 5e-10 mu=[-1000,0]", case_of(mu=[-1000.0, 0.0], lower=[0.5 + 5e-10, -1.0], w0=[0.5, 0.5], turnover_limit=0.0))
    show("H tau=5e-10 lower breach 5e-10 mu=[-1000,0]", case_of(mu=[-1000.0, 0.0], lower=[0.5 + 5e-10, -1.0], w0=[0.5, 0.5], turnover_limit=5e-10))
    show("I tau=1e-9 lower breach 1e-9 mu=[-1000,0]", case_of(mu=[-1000.0, 0.0], lower=[0.5 + 1e-9, -1.0], w0=[0.5, 0.5], turnover_limit=1e-9))


if __name__ == "__main__":
    named_cases()
