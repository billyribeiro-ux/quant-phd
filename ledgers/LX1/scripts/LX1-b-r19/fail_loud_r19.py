"""Round 19: exercise the L04 twin's parse_rate and load_column on bad inputs (functions only; main() is not run).

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/fail_loud_r19.py
"""
import csv
import pathlib
import tempfile

src = pathlib.Path("tests/labs/LX1/lab-LX1-L04-1.py").read_text(encoding="utf-8")
head = src.split("\ndef main()")[0]
ns: dict = {"__name__": "twin_defs"}
exec(compile(head, "twin_defs", "exec"), ns)
parse_rate, load_column = ns["parse_rate"], ns["load_column"]
for label, text in (("blank", ""), ("n/a", "n/a"), ("zero", "0"), ("exponent", "1e-3")):
    try:
        parse_rate(text, "2000-01")
        print(label, "-> no error (UNEXPECTED)")
    except ValueError as exc:
        print(label, "-> ValueError:", exc)
d = tempfile.mkdtemp(prefix="lx1b-r19-fail-")
p = pathlib.Path(d) / "bad.csv"
with p.open("w", newline="", encoding="utf-8") as h:
    w = csv.writer(h)
    w.writerow(["month", "GBP"])
    w.writerow(["1996-01", "1.5"])
    w.writerow(["1996-03", "1.6"])  # skipped 1996-02
try:
    load_column(p, "GBP")
    print("skipped month -> no error (UNEXPECTED)")
except ValueError as exc:
    print("skipped month -> ValueError:", exc)
p2 = pathlib.Path(d) / "blank.csv"
with p2.open("w", newline="", encoding="utf-8") as h:
    w = csv.writer(h)
    w.writerow(["month", "GBP"])
    w.writerow(["1996-01", ""])
try:
    load_column(p2, "GBP")
    print("blank cell in file -> no error (UNEXPECTED)")
except ValueError as exc:
    print("blank cell in file -> ValueError:", exc)
try:
    load_column(p2, "EUR")
    print("missing column -> no error (UNEXPECTED)")
except ValueError as exc:
    print("missing column -> ValueError:", exc)
import shutil
shutil.rmtree(d)
