"""Round 10 witnesses for AC1-a (L01-L03). Run as: python -I this.py <checkout>"""
import html
import random
import types
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
TWINS = root / "tests/labs/AC1"


def load(path: Path) -> dict:
    src = path.read_text(encoding="utf-8").replace("\nmain()\n", "\n")
    mod = types.ModuleType("lab_under_test")
    sys.modules["lab_under_test"] = mod
    exec(compile(src, str(path), "exec"), mod.__dict__)
    return mod.__dict__


def raises(fn) -> str:
    try:
        fn()
    except ValueError as exc:
        return f"ValueError: {exc}"
    return "accepted"


# W1-W3: L01 posting check
l1 = load(TWINS / "lab-AC1-L01-1.py")
Entry, Line, check = l1["Entry"], l1["Line"], l1["check_entry"]
neither = Entry(day=1, memo="line with neither side", lines=(Line("cash"), Line("sales", credit=0)))
print("W1 L01 line with neither side:", raises(lambda: check(neither)))
both = Entry(day=1, memo="both sides", lines=(Line("cash", debit=5, credit=5), Line("sales", credit=0)))
print("W2 L01 line with both sides:", raises(lambda: check(both)))
unknown = Entry(day=1, memo="unknown account", lines=(Line("interest_income", debit=5), Line("sales", credit=5)))
print("W3 L01 unknown account:", raises(lambda: check(unknown)))
wrong_acct = Entry(day=1, memo="right amounts, wrong account", lines=(Line("operating_expense", debit=5), Line("sales", credit=5)))
print("W3b L01 balanced entry on a valid wrong account:", raises(lambda: check(wrong_acct)))

# W4: L02 and L03 chart of accounts contain no interest or tax account
for name in ("lab-AC1-L02-1.py", "lab-AC1-L03-1.py"):
    ns = load(TWINS / name)
    accts = sorted(ns["TYPES"])
    rev_exp = sorted(a for a, t in ns["TYPES"].items() if t in ("revenue", "expense"))
    print(f"W4 {name} revenue and expense accounts: {rev_exp}")
    print(f"W4 interest or tax account present: {any(k in a for a in accts for k in ('interest', 'tax'))}")

# W5: L02 and L03 generators: which expense postings carry no cash line
for name in ("lab-AC1-L02-1.py", "lab-AC1-L03-1.py"):
    ns = load(TWINS / name)
    ledger = ns["Ledger"]()
    ns["generate"](ledger, random.Random(ns["SEED"]))
    no_cash: dict[str, int] = {}
    for e in ledger.entries:
        if any(line.account == "cash" for line in e.lines):
            continue
        for line in e.lines:
            if ns["TYPES"][line.account] == "expense":
                no_cash[line.account] = no_cash.get(line.account, 0) + 1
    with_cash = set()
    for e in ledger.entries:
        if any(line.account == "cash" for line in e.lines):
            for line in e.lines:
                if ns["TYPES"][line.account] == "expense":
                    with_cash.add(line.account)
    print(f"W5 {name} expense accounts in entries with no cash line: {sorted(no_cash)}; expense accounts in cash entries: {sorted(with_cash)}")

# W6: page data-run block equals twin
for page, twin in (("L01", "lab-AC1-L01-1.py"), ("L02", "lab-AC1-L02-1.py"), ("L03", "lab-AC1-L03-1.py")):
    text = (root / "course/modules/AC/AC1" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r"<code class=\"language-python\" data-run>(.*?)</code>", text, re.S)
    body = html.unescape(m.group(1))
    twin_text = (TWINS / twin).read_text(encoding="utf-8")
    print(f"W6 {page} data-run equals twin:", body.strip() == twin_text.strip())
