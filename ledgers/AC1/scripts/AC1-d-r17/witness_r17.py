"""Witnesses for the three round-17 survivors and one probe of each. Usage: python3 -I witness_r17.py <statements dir>"""
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

base = Path(sys.argv[1])
ref = load("ref", base / "reference.py")
m01 = load("m01", base / "v17_m01.py")
m02 = load("m02", base / "v17_m02.py")
m03 = load("m03", base / "v17_m03.py")

def attempt(label, fn):
    try:
        out = fn()
        print(label, "-> accepted:", out)
    except Exception as e:  # noqa: BLE001 - witness script prints the outcome
        print(label, "-> raised", type(e).__name__, str(e))

tx = lambda d, lines: [{"date": d, "lines": lines}]
attempt("ref slash date", lambda: ref.post(tx("2024/01/02", [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}])))
attempt("m01 slash date", lambda: m01.post(tx("2024/01/02", [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}])))
attempt("ref line both sides, balanced entry", lambda: ref.post(tx("2024-01-02", [{"account": "cash", "debit": 5, "credit": 3}, {"account": "sales", "debit": 0, "credit": 2}])))
attempt("m03 line both sides, balanced entry", lambda: m03.post(tx("2024-01-02", [{"account": "cash", "debit": 5, "credit": 3}, {"account": "sales", "debit": 0, "credit": 2}])))
attempt("ref balance_sheet 2100-03-31", lambda: ref.income_statement([], "2100-03-31")["net_income"])
attempt("m02 balance_sheet 2100-03-31", lambda: m02.income_statement([], "2100-03-31")["net_income"])
attempt("m02 balance_sheet 2100-02-28", lambda: m02.income_statement([], "2100-02-28")["net_income"])
attempt("m02 balance_sheet 2000-03-31", lambda: m02.income_statement([], "2000-03-31")["net_income"])
