"""Round 20 fail-loud check for the L04 twin's loader: mutated CSVs must raise ValueError (not skip or fill).

Loads the twin's helpers without running main() (the last line is stripped in memory), then feeds scratch CSVs.
Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/fail_loud_L04_r20.py
"""
import tempfile
from pathlib import Path

src = Path("tests/labs/LX1/lab-LX1-L04-1.py").read_text(encoding="utf-8")
assert src.rstrip().endswith("main()")
ns: dict = {"__name__": "twin_helpers"}
exec(compile(src.rstrip()[: -len("main()")], "twin", "exec"), ns)
load_column = ns["load_column"]
base = Path("course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()
header = base[0].split(",")
gi = header.index("GBP")
cases = {}
rows = base[1:]
i1990 = [i for i, r in enumerate(rows) if r.startswith("1990-01,")][0]
def mut(fn):
    out = [list(r.split(",")) for r in rows]
    fn(out)
    return [base[0]] + [",".join(r) for r in out]
def blank(o):
    o[i1990][gi] = ""
def text(o):
    o[i1990][gi] = "n/a"
def gap(o):
    del o[i1990]
def nonpositive(o):
    o[i1990][gi] = "0"
cases = {"blank GBP cell 1990-01": mut(blank), "text GBP cell 1990-01": mut(text),
         "missing month 1990-01 (gap)": mut(gap), "zero rate 1990-01": mut(nonpositive)}
results = {}
with tempfile.TemporaryDirectory() as d:
    for name, lines in cases.items():
        p = Path(d) / "fx.csv"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        try:
            load_column(p, "GBP")
            results[name] = "NO ERROR (FAIL)"
        except ValueError as e:
            results[name] = f"ValueError: {e}"
    p = Path(d) / "fx2.csv"
    p.write_text("\n".join(["month,AUD"] + [r.split(",")[0] + "," + r.split(",")[1] for r in rows]) + "\n", encoding="utf-8")
    try:
        load_column(p, "GBP")
        results["missing GBP column"] = "NO ERROR (FAIL)"
    except ValueError as e:
        results["missing GBP column"] = f"ValueError: {e}"
for k, v in results.items():
    print(f"{k}: {v}")
print("all raise:", all(v.startswith("ValueError") for v in results.values()))
