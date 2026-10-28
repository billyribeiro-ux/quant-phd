"""Round 9 witnesses for AC1-a: run the lab modules' own check code and ledgers under python -I.

Usage: python -I witness_r9.py <checkout>
Reads the lab twins as text, drops the trailing main() call, and executes them as modules.
"""

import contextlib
import io
import re
import sys
import types
import html as h
from pathlib import Path

root = Path(sys.argv[1])


def load(name: str) -> dict[str, object]:
    src = (root / "tests/labs/AC1" / name).read_text(encoding="utf-8")
    src = src.rsplit("\nmain()", 1)[0]
    import types

    mod = types.ModuleType(name.replace("-", "_").removesuffix(".py"))
    sys.modules[mod.__name__] = mod
    exec(compile(src, name, "exec"), mod.__dict__)
    return mod.__dict__


l01 = load("lab-AC1-L01-1.py")
Entry, Line, check_entry = l01["Entry"], l01["Line"], l01["check_entry"]
zero_line = Entry(3, "zero-zero line", (Line("cash"), Line("cash", debit=5), Line("sales", credit=5)))
try:
    check_entry(zero_line)  # type: ignore[operator]
    print("W1 L01 check_entry accepts a line with neither debit nor credit: True")
except ValueError as exc:
    print(f"W1 L01 check_entry accepts a line with neither debit nor credit: False ({exc})")

l03 = load("lab-AC1-L03-1.py")
gen, Ledger = l03["generate"], l03["Ledger"]
ledger = Ledger()
gen(ledger, __import__("random").Random(20261027))  # type: ignore[operator]
no_cash_expense_memos = {
    e.memo
    for e in ledger.entries  # type: ignore[attr-defined]
    if any(line.account == "cost_of_sales" for line in e.lines)
    and not any(line.account == "cash" for line in e.lines)
}
print(f"W2 L03 ledger: expense entries with no cash line (memos): {sorted(no_cash_expense_memos)}")

# W3: Proposition 3.2 (L02) is stated for any ledger of balanced entries whose only equity accounts are
# common stock and dividends. Add one more revenue account (interest income, not one of the four of Definition 2.1)
# and one balanced entry; the balance sheet of Lab 2 is then compared at the year end.
l02 = load("lab-AC1-L02-1.py")
ledger2 = l02["Ledger"]()
l02["generate"](ledger2, __import__("random").Random(20261027))  # type: ignore[operator]
l02["TYPES"]["interest_income"] = "revenue"  # type: ignore[index]
Entry2, Line2 = l02["Entry"], l02["Line"]
ledger2.post(Entry2(2025, 4, "interest received", "operating", (Line2("cash", debit=1000), Line2("interest_income", credit=1000))))  # type: ignore[operator]
sheet = l02["balance_sheet"](ledger2, 2025)  # type: ignore[operator]
gap = sheet["total_assets"] - sheet["total_liabilities_and_equity"]  # type: ignore[index]
print(f"W3 L02 ledger plus one interest entry of 1000 cents: 2025 year end assets less liabilities and equity = {gap} cents")

# W4: scope witness for Proposition 3.2 (L01), hypothesis (i) excludes write-offs.
sales, write_off, collections = 100, 30, 0
R, K = sales, collections
dA = sales - write_off - collections  # receivable after a write-off of 30 on sales of 100 with no collections
print(f"W4 write-off 30 on sales 100, no collections: R={R} K={K} dA={dA} R-K={R - K} identity holds: {R - K == dA}")

# W5: data-run block of each page equals its twin (rstrip of the final newline).
import re

for page, twin in (("L01", "lab-AC1-L01-1.py"), ("L02", "lab-AC1-L02-1.py"), ("L03", "lab-AC1-L03-1.py")):
    html = (root / f"course/modules/AC/AC1/{page}.html").read_text(encoding="utf-8")
    blocks = re.findall(r"<code class=\"language-python\" data-run>(.*?)</code>", html, re.S)
    import html as h

    body = h.unescape(blocks[0]) if blocks else ""
    same = body.rstrip("\n") == (root / "tests/labs/AC1" / twin).read_text(encoding="utf-8").rstrip("\n")
    print(f"W5 {page} data-run blocks: {len(blocks)}, equal to twin: {same}")

# W6: wrong-charge witness (r8 witness repeated): change the 2025-2027 quarterly charge by one cent in the
# lab source and rerun the lab's own checks; list which printed checks read False.
src = (root / "tests/labs/AC1/lab-AC1-L03-1.py").read_text(encoding="utf-8")
mutant = src.replace("depreciation = 25_000_000 + (7_500_000 if year >= 2026 else 0)",
                     "depreciation = 25_000_000 + 1 + (7_500_000 if year >= 2026 else 0)")
assert mutant != src
mutant = mutant.rsplit("\nmain()", 1)[0]
import contextlib, io

mod = types.ModuleType("mutant_l03")
sys.modules[mod.__name__] = mod
exec(compile(mutant, "mutant_l03", "exec"), mod.__dict__)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mod.__dict__["main"]()
false_lines = [ln for ln in buf.getvalue().splitlines() if ln.rstrip().endswith("False")]
print("W6 mutant: lines ending in False:")
for ln in false_lines:
    print("   ", ln)
print("W6 final line:", buf.getvalue().splitlines()[-1])
