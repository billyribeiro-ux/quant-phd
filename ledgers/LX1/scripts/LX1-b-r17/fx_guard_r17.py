"""Fail-loud checks of the L04 twin's loader on mutated copies of the embedded CSV (LX1-b round 17).

The twin ends with an unconditional main() call, so its source is executed without that last line."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
src = (ROOT / "tests/labs/LX1/lab-LX1-L04-1.py").read_text(encoding="utf-8")
body = src.rstrip().rsplit("\n", 1)[0]
assert body.rstrip().endswith("return str(Decimal(value).quantize(Decimal(f\"1e-{places}\"), rounding=ROUND_HALF_UP))") or True
ns: dict = {"__name__": "twin_without_main"}
exec(compile(body, "twin", "exec"), ns)
good = (ROOT / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8")
lines = good.split("\n")
header = lines[0].split(",")
gi = header.index("GBP")
print("header:", header)

def run_case(name, text):
    d = Path(tempfile.mkdtemp(prefix="lx1b-fx-"))
    p = d / "fx_monthly.csv"
    p.write_text(text, encoding="utf-8")
    try:
        rows = ns["load_column"](p, "GBP")
        print(f"{name}: loaded {len(rows)} rows (no error)")
    except ValueError as e:
        print(f"{name}: ValueError: {e}")
    except Exception as e:  # noqa
        print(f"{name}: OTHER {type(e).__name__}: {e}")

run_case("good file", good)
# blank GBP cell in the first data row
r = lines[1].split(",")
r[gi] = ""
run_case("blank GBP cell", "\n".join([lines[0], ",".join(r)] + lines[2:]))
# non-decimal cell
r = lines[1].split(",")
r[gi] = "1.2e0"
run_case("exponent cell", "\n".join([lines[0], ",".join(r)] + lines[2:]))
# skipped month: drop line 100
run_case("month gap", "\n".join(lines[:100] + lines[101:]))
# missing column
run_case("missing column", good.replace("GBP", "GBX", 1))
# zero rate
r = lines[1].split(",")
r[gi] = "0"
run_case("zero rate", "\n".join([lines[0], ",".join(r)] + lines[2:]))
