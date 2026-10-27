# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Independent re-derivation of Lab 2's printed values and of Lab 1's three revenue answers (AC2 project).

Usage (from the repository root): .venv/bin/python -I ledgers/AC2/scripts/project-r1/lab2_lab1_check.py

Lab 2 (completion problem): recomputes DuPont, ROIC and the cash-flow accrual from the lab's SIMULATED statements with
fractions.Fraction (exact), then compares with the page's printed values to the printed precision.
Lab 1 (worked example): evaluates the reference standardize on the lab's FILER for the three as-of dates and prints
the revenue by period end, to compare with the page's three printed answers.
"""

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def lab2() -> None:
    st = {
        "2021-12-31": {"revenue": 1000, "net_income": 80, "total_assets": 900, "equity": 400, "operating_income": 120,
                       "long_term_debt": 150, "cash": 60, "cfo": 95},
        "2022-12-31": {"revenue": 1200, "net_income": 110, "total_assets": 1100, "equity": 460, "operating_income": 160,
                       "long_term_debt": 180, "cash": 90, "cfo": 130},
    }
    prev, end = "2021-12-31", "2022-12-31"
    tax = Fraction(1, 4)
    avg_ta = Fraction(st[end]["total_assets"] + st[prev]["total_assets"], 2)
    avg_eq = Fraction(st[end]["equity"] + st[prev]["equity"], 2)
    roe = Fraction(st[end]["net_income"]) / avg_eq
    nm = Fraction(st[end]["net_income"], st[end]["revenue"])
    at = Fraction(st[end]["revenue"]) / avg_ta
    lev = avg_ta / avg_eq
    print("DuPont identity exact:", roe == nm * at * lev)
    print("roe", round(float(roe), 6), "net margin", round(float(nm), 6))
    ic = lambda e: Fraction(st[e]["equity"] + st[e]["long_term_debt"] - st[e]["cash"])  # noqa: E731
    nopat = Fraction(st[end]["operating_income"]) * (1 - tax)
    roic = nopat / ((ic(end) + ic(prev)) / 2)
    print("nopat", float(nopat), "roic", round(float(roic), 6))
    accr = Fraction(st[end]["net_income"] - st[end]["cfo"]) / avg_ta
    print("cash-flow accruals", round(float(accr), 6))


def lab1() -> None:
    src = (ROOT / "tests/labs/AC2/lab-AC2-project-1.py").read_text(encoding="utf-8")
    ns: dict = {}
    exec(compile(src.replace("print(", "(lambda *a, **k: None)("), "lab1", "exec"), ns)
    ref = load("ref_l1", ROOT / "course/modules/AC/AC2/grader/reference.py")
    filer = ns["FILER"]
    for label, cut in (("latest knowledge", None), ("known on 2023-03-01", "2023-03-01"), ("known on 2022-01-31", "2022-01-31")):
        st = ref.standardize(filer, cut)
        print("revenue,", label + ":", {k: v["revenue"] for k, v in st.items() if "revenue" in v})


def main() -> int:
    lab2()
    lab1()
    return 0


if __name__ == "__main__":
    sys.exit(main())
