"""Round-16 verifier sweep for M7 slice d: page-valid random cases, including starts at the 1e-9 tolerance.

For each seeded case: the reference is run; its output is certified by an independent exact recomputation (probe module
v16_probe.py, page definitions project.html:309-321); each equivalent/ file is compared with the reference field by
field. Usage (repository root): .venv/bin/python -I ledgers/M7/scripts/M7-d-r16/v16_sweep.py [count] [seed]
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402

F = Fraction
TOL = F(1, 10**9)


def valid_start(case: dict[str, Any]) -> bool:
    """The page's starting-portfolio checks in exact arithmetic (project.html:321, 326)."""
    n = len(case["mu"])
    w0 = [F(x) for x in case["w0"]]
    lo = [F(x) for x in case["lower"]]
    up = [F(x) for x in case["upper"]]
    if abs(sum(w0, F(0)) - 1) > TOL:
        return False
    if any(w0[i] < lo[i] - TOL or w0[i] > up[i] + TOL for i in range(n)):
        return False
    for k, cap in enumerate(case["sector_caps"]):
        if sum((w0[i] for i in range(n) if case["sector"][i] == k), F(0)) > F(cap) + TOL:
            return False
    return all(lo[i] <= up[i] for i in range(n))


def gen(rng: random.Random) -> dict[str, Any]:
    n = rng.choice([2, 3, 4])
    z = rng.choice([1, 2])
    sector = list(range(z)) + [rng.randrange(z) for _ in range(n - z)]
    rng.shuffle(sector)
    m = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
    sigma = [[sum(m[k][i] * m[k][j] for k in range(n)) / 1000 + (1 / 1000 if i == j else 0) for j in range(n)] for i in range(n)]
    scale = rng.choice([1e-3, 0.05, 1.0, 1000.0])
    mu = [round(rng.gauss(0, 1) * scale, 6) for _ in range(n)]
    raw = [rng.randint(1, 60) for _ in range(n)]
    total = sum(raw)
    w0 = [r / total for r in raw]
    w0 = [round(x, 6) for x in w0]
    w0[-1] = round(1 - sum(w0[:-1]), 6)
    lower, upper = [], []
    for i in range(n):
        lower.append(w0[i] if rng.random() < 0.3 else round(w0[i] - rng.uniform(0.0, 0.5), 4))
        upper.append(w0[i] if rng.random() < 0.2 else round(w0[i] + rng.uniform(0.0, 0.5), 4))
        if rng.random() < 0.15:
            lower[i] = -1.0
        if rng.random() < 0.15:
            upper[i] = 2.0
    caps = []
    for k in range(z):
        s = sum(w0[i] for i in range(n) if sector[i] == k)
        caps.append(round(s + rng.choice([0.0, 0.0, rng.uniform(0.0, 0.3)]), 6))
    tau = rng.choice([0.0, 1e-10, 5e-10, 1e-9, 1e-6, 0.05, 0.2, 2.0])
    gamma = rng.choice([1.0, 1e-6, 1e-9, 0.5, 2.0, 3.0])
    case: dict[str, Any] = {
        "label": "SIMULATED sweep case",
        "gamma": gamma,
        "mu": mu,
        "sigma": sigma,
        "w0": w0,
        "lower": lower,
        "upper": upper,
        "sector": sector,
        "sector_caps": caps,
        "turnover_limit": tau,
    }
    # tolerance-level perturbations (each within 1e-9 of the page's starting checks)
    r = rng.random()
    if r < 0.35:
        i = rng.randrange(n)
        if lower[i] == w0[i]:
            case["w0"][i] = round(w0[i] - rng.choice([5e-10, 1e-9]), 12)
        elif upper[i] == w0[i]:
            case["w0"][i] = round(w0[i] + rng.choice([5e-10, 1e-9]), 12)
    if rng.random() < 0.35:
        k = rng.randrange(z)
        case["sector_caps"][k] = round(case["sector_caps"][k] - rng.choice([5e-10, 1e-9]), 12)
    if rng.random() < 0.35:
        j = rng.randrange(n)
        case["w0"][j] = round(case["w0"][j] + rng.choice([5e-10, -5e-10]), 12)
    return case


def compare(ref: dict[str, Any], other: dict[str, Any]) -> float:
    worst = 0.0
    if ref["weights"] != other.get("weights"):
        worst = max(worst, max(abs(a - b) for a, b in zip(ref["weights"], other["weights"], strict=True)))
    for key in ref["multipliers"]:
        a, b = ref["multipliers"][key], other["multipliers"][key]
        if isinstance(a, list):
            worst = max(worst, max(abs(x - y) for x, y in zip(a, b, strict=True)) if a else 0.0)
        else:
            worst = max(worst, abs(a - b))
    for key in ref["certificate"]:
        worst = max(worst, abs(ref["certificate"][key] - other["certificate"][key]))
    return worst


def load_mut(path: Path, name: str) -> Any:
    return P.load(path, name)


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    rng = random.Random(seed)
    equiv_files = sorted(P.EQUIV.glob("*.py"))
    mods = {p.stem: load_mut(p, "eq_" + p.stem) for p in equiv_files}
    stats: dict[str, Any] = {"cases": 0, "answered": 0, "refused": 0, "valid_start_refused": 0,
                             "cert_fail": [], "agree_fail": [], "max_budget_gap": 0.0, "max_feas": 0.0}
    diffs: dict[str, dict[str, Any]] = {name: {"max": 0.0, "over_1e-9": 0, "examples": []} for name in mods}
    for idx in range(count):
        case = gen(rng)
        stats["cases"] += 1
        start_ok = valid_start(case)
        try:
            out = P.REF.allocate(json.loads(json.dumps(case)))
        except Exception as exc:  # the reference refuses; record why
            stats["refused"] += 1
            if start_ok:
                stats["valid_start_refused"] += 1
                stats.setdefault("valid_refusals", []).append({"idx": idx, "error": f"{type(exc).__name__}: {exc}", "case": case})
            continue
        if not start_ok:
            stats.setdefault("invalid_but_answered", []).append(idx)
            continue
        stats["answered"] += 1
        ok, info = P.check(case, out)
        stats["max_feas"] = max(stats["max_feas"], info["feas"])
        stats["max_budget_gap"] = max(stats["max_budget_gap"], info["budget_gap"])
        if info["feas"] > 1e-8:
            stats["cert_fail"].append({"idx": idx, "feas": info["feas"], "case": case, "out": out})
        if info["agree"] > 1e-9:
            stats["agree_fail"].append({"idx": idx, "agree": info["agree"]})
        for name, mod in mods.items():
            other = mod.allocate(json.loads(json.dumps(case)))
            d = compare(out, other)
            rec = diffs[name]
            rec["max"] = max(rec["max"], d)
            if d > 1e-9:
                rec["over_1e-9"] += 1
                if len(rec["examples"]) < 3:
                    rec["examples"].append({"idx": idx, "diff": d, "case": case})
    summary = {k: v for k, v in stats.items() if k not in ("cert_fail", "valid_refusals", "agree_fail")}
    summary["cert_fail_count"] = len(stats["cert_fail"])
    summary["agree_fail_count"] = len(stats["agree_fail"])
    summary["valid_refusal_count"] = len(stats.get("valid_refusals", []))
    print(json.dumps({"count": count, "seed": seed, "summary": summary, "equivalence_diffs": {
        k: {"max": v["max"], "over_1e-9": v["over_1e-9"]} for k, v in diffs.items()}}, indent=1, default=str))
    for item in stats["cert_fail"][:3]:
        print("CERT_FAIL", json.dumps({"idx": item["idx"], "feas": item["feas"], "case": item["case"]}, default=str))
    for item in stats.get("valid_refusals", [])[:3]:
        print("VALID_REFUSED", json.dumps({"idx": item["idx"], "error": item["error"], "case": item["case"]}, default=str))
    for name, v in diffs.items():
        for ex in v["examples"][:1]:
            print("EQUIV_DIFF", name, json.dumps({"idx": ex["idx"], "diff": ex["diff"], "case": ex["case"]}, default=str))


if __name__ == "__main__":
    main()
