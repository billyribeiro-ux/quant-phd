"""Independent re-derivation of fetch_data._invert (round 28, part B).

Usage: python -I <checkout>/ledgers/S7/scripts/data-tooling-r28-B/invert_check.py <checkout> <raw_dir>
Reference: exact Fraction arithmetic, the decade found by integer comparison (not by string length), half-to-even
by hand, and the output built from the integer digits. Compared with tools/fetch_data.py::_invert on
(1) the real raw Federal Reserve zips and the committed CSVs, (2) seeded random plain decimals, (3) exact-tie and
power-of-ten neighbourhoods, (4) the three expected strings of tests/test_fetch_data.py.
"""

from __future__ import annotations

import csv
import random
import sys
from fractions import Fraction
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
RAW = Path(sys.argv[2])
sys.path.insert(0, str(CHECKOUT / "tools"))
import fetch_data as fd  # noqa: E402


def ref_invert(value: str) -> str:
    x = Fraction(value)
    if x == 0:
        raise ValueError("zero")
    inv = 1 / abs(x)
    e = 0
    while inv >= Fraction(10) ** (e + 1):
        e += 1
    while inv < Fraction(10) ** e:
        e -= 1
    q = inv * Fraction(10) ** (7 - e)  # in [10^7, 10^8)
    n0 = q.numerator // q.denominator
    r = q - n0
    if r > Fraction(1, 2) or (r == Fraction(1, 2) and n0 % 2 == 1):
        n0 += 1
    if n0 == 10**8:
        n0, e = 10**7, e + 1
    k = e - 7  # value = n0 * 10**k
    s = str(n0)
    if k >= 0:
        body = s + "0" * k
    else:
        s = s.rjust(-k + 1, "0")
        body = s[:k] + "." + s[k:]
    return ("-" if x < 0 else "") + body


def tool_invert(value: str) -> str:
    return fd._invert(value)


failures: list[str] = []
counts: dict[str, int] = {}


def check(label: str, value: str) -> None:
    counts[label] = counts.get(label, 0) + 1
    a, b = ref_invert(value), tool_invert(value)
    if a != b and len(failures) < 50:
        failures.append(f"{label}: {value!r} ref={a} tool={b}")
    elif a != b:
        failures.append("...")


# (4) the expected strings of the test (pairs copied from tests/test_fetch_data.py lines 102-121 at c9beb92)
src = (CHECKOUT / "tests/test_fetch_data.py").read_text(encoding="utf-8")
import ast  # noqa: E402

pairs = []
start = src.index("def test_inversion_keeps_eight_significant_digits_in_plain_decimal")
block = src[src.rindex("@pytest", 0, start) : src.index("\ndef ", start + 10)]
for node in ast.walk(ast.parse(block)):
    if isinstance(node, ast.Tuple) and len(node.elts) == 2 and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
        if node.elts[0].value not in ("value", "expected"):
            pairs.append((node.elts[0].value, node.elts[1].value))
bad_expected = []
for x, expected in pairs:
    got = ref_invert(x)
    if got != expected:
        bad_expected.append((x, expected, got))
    check("test-cases", x)
print(f"test-cases: {len(pairs)} (value, expected) pairs read from the test; reference disagreements with the test's expected strings: {bad_expected}")

# (1) real raw data and the committed CSVs
spec = {d.id: d for d in fd.load_spec()}
real_cells = 0
real_mismatch: list[str] = []
for dsid, raw_name in (("fx_daily", "fx_daily.raw"), ("fx_monthly", "fx_monthly.raw")):
    d = spec[dsid]
    tr = d.transform
    raw = (RAW / raw_name).read_bytes()
    series = tr["series"]
    data = fd._sdmx_series(raw, tr["member"], set(series.values()))
    invert = set(tr.get("invert") or [])
    committed = list(csv.DictReader((CHECKOUT / "course/assets/data/market" / f"{dsid}.csv").read_text().splitlines()))
    keycol = "date" if "date" in committed[0] else "month"
    for row in committed:
        key = row[keycol]
        for col, name in series.items():
            if col not in invert or not row.get(col):
                continue
            if dsid == "fx_daily":
                raw_v = data[name].get(key)
                if raw_v is None:
                    real_mismatch.append(f"{dsid} {key} {col}: no raw value")
                    continue
                real_cells += 1
                if ref_invert(raw_v) != row[col]:
                    real_mismatch.append(f"{dsid} {key} {col}: raw {raw_v} ref {ref_invert(raw_v)} csv {row[col]}")
            else:
                # month_end: the CSV holds the column's last available value in the month
                days = sorted(dd for dd in data[name] if dd.startswith(key))
                if not days:
                    real_mismatch.append(f"{dsid} {key} {col}: no raw value in month")
                    continue
                last = data[name][days[-1]]
                real_cells += 1
                if ref_invert(last) != row[col]:
                    real_mismatch.append(f"{dsid} {key} {col}: raw {last} ref {ref_invert(last)} csv {row[col]}")
    for col, name in series.items():
        if col in invert:
            for dd, v in data[name].items():
                if tr["start"] <= dd <= tr["end"]:
                    check("real-raw", v)
print(f"real data: inverted CSV cells re-derived from the raw zips: {real_cells}; mismatches: {len(real_mismatch)} {real_mismatch[:5]}")

# (2) seeded random plain decimals (seed 20261028)
rng = random.Random(20261028)
for _ in range(200_000):
    nd = rng.randint(1, 40)
    digits = str(rng.randint(10 ** (nd - 1), 10**nd - 1)) if nd > 1 else str(rng.randint(1, 9))
    if rng.random() < 0.3:
        digits = digits.rstrip("0") or "1"
        digits += "0" * rng.randint(0, 4)
    point = rng.randint(0, len(digits))
    v = digits[:point] + "." + digits[point:] if 0 < point < len(digits) else digits + ".0" if point == len(digits) else "0." + digits
    if rng.random() < 0.2:
        v = "-" + v
    if Fraction(v) == 0:
        continue
    check("random", v)

# (3) targeted: ties at the eighth digit and neighbourhoods of powers of ten (seed 20261029)
rng = random.Random(20261029)
for _ in range(20_000):
    m = rng.randint(10**7, 10**8 - 1)
    e = rng.randint(-12, 12)
    T = Fraction(2 * m + 1, 2) * Fraction(10) ** (e - 7)  # an exact tie of the 8-digit rounding of 1/x
    x = 1 / T
    # plain decimal, truncated at 40 significant digits, then one unit above it
    scale = 40 - len(str(int(x)))
    trunc = int(x * Fraction(10) ** scale)
    for n in (trunc, trunc + 1):
        s = str(n)
        s = s.rjust(scale + 1, "0")
        v = s[: len(s) - scale] + "." + s[len(s) - scale :] if scale > 0 else s + "0" * (-scale)
        if Fraction(v) == 0:
            continue
        check("targeted-tie", v)
for _ in range(20_000):
    k = rng.randint(-12, 12)
    dd = Fraction(rng.randint(1, 10**9 - 1), 10**9)
    T = Fraction(10) ** k * (1 - dd)
    x = 1 / T
    scale = 40 - len(str(int(x)))
    trunc = int(x * Fraction(10) ** scale)
    for n in (trunc, trunc + 1):
        s = str(n).rjust(scale + 1, "0")
        v = s[: len(s) - scale] + "." + s[len(s) - scale :] if scale > 0 else s + "0" * (-scale)
        if Fraction(v) == 0:
            continue
        check("targeted-decade", v)

print("counts:", counts)
print("disagreements (ref vs fetch_data._invert):", len(failures), failures[:20])
