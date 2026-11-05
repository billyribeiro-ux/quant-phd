"""LX1-b round 12: the L04 twin's data guards, exercised on scratch CSVs. The twin's last line (main()) is dropped
so only its functions are loaded; nothing is written into the checkout.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r12/guard_r12.py <checkout>
"""
import pathlib
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
src = (root / "tests/labs/LX1/lab-LX1-L04-1.py").read_text(encoding="utf-8")
assert src.rstrip().endswith("main()")
ns: dict[str, object] = {"__name__": "twin_functions"}
exec(compile(src.rstrip()[: -len("main()")], "twin", "exec"), ns)
load_column = ns["load_column"]
HEADER = "month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK\n"
GOOD = "1971-01,2.4,1.0,1.0,1.0,1.0,2.4174,1.0,1.0,1.0,1.0\n1971-02,2.4,1.0,1.0,1.0,1.0,2.4200,1.0,1.0,1.0,1.0\n"
cases = {
    "good two rows": (HEADER + GOOD, False),
    "blank GBP cell": (HEADER + GOOD.replace("2.4200", ""), True),
    "NA GBP cell": (HEADER + GOOD.replace("2.4200", "NA"), True),
    "month gap": (HEADER + "1971-01,2.4,1,1,1,1,2.4174,1,1,1,1\n1971-03,2.4,1,1,1,1,2.4200,1,1,1,1\n", True),
    "missing GBP column": ("month,AUD,EUR\n1971-01,2.4,1.0\n", True),
    "zero rate": (HEADER + GOOD.replace("2.4200", "0"), True),
    "signed value": (HEADER + GOOD.replace("2.4200", "-2.42"), True),
    "exponent": (HEADER + GOOD.replace("2.4200", "2.42e0"), True),
    "month 13": (HEADER + "1971-13,2.4,1,1,1,1,2.4174,1,1,1,1\n", True),
    "duplicate month": (HEADER + "1971-01,2.4,1,1,1,1,2.4174,1,1,1,1\n1971-01,2.4,1,1,1,1,2.4200,1,1,1,1\n", True),
}
ok = True
with tempfile.TemporaryDirectory() as d:
    for name, (text, should_raise) in cases.items():
        p = pathlib.Path(d) / f"{name.replace(' ', '_')}.csv"
        p.write_text(text, encoding="utf-8")
        try:
            rows = load_column(p, "GBP")  # type: ignore[operator]
            raised = False
            detail = f"rows={len(rows)}"
        except ValueError as exc:
            raised = True
            detail = f"ValueError: {exc}"
        verdict = "OK" if raised == should_raise else "MISMATCH"
        ok &= verdict == "OK"
        print(f"{name:20s} raised={raised!s:5s} expected={should_raise!s:5s} {verdict}  {detail}")
print("GUARDS:", "PASS" if ok else "FAIL")
