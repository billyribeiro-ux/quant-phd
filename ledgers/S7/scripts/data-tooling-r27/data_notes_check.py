"""Re-derive the claims of the fx_daily / fx_monthly notes from the saved live H.10 zip (round 27).

Usage: python -I data_notes_check.py <raw H.10 zip> ; run from the checkout root so tools/ imports.
Claims checked: (a) the release's monthly series RXI$US_N.M.EU equals the mean of the daily RXI$US_N.B.EU values
of the same month to 4 decimal places in every month (the note's parenthetical); (b) the number of such
months and the two exact half-way cases.
"""

from __future__ import annotations

import calendar
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
import fetch_data  # noqa: E402

raw = Path(sys.argv[1]).read_bytes()
daily = fetch_data._sdmx_series(raw, "H10_data.xml", {"RXI$US_N.B.EU", "RXI$US_N.M.EU"})
monthly_series = fetch_data._sdmx_series(raw, "H10_data.xml", {"RXI$US_N.M.EU"})["RXI$US_N.M.EU"]
by_month: dict[str, list[Decimal]] = {}
for d, v in daily["RXI$US_N.B.EU"].items():
    by_month.setdefault(d[:7], []).append(Decimal(v))
agree = 0
bad: list[tuple[str, str, str]] = []
halfway: list[str] = []
for mdate, mv in sorted(monthly_series.items()):
    month = mdate[:7]
    if month < "1999-01":
        continue
    vals = by_month.get(month, [])
    if not vals:
        bad.append((month, mv, "no daily values"))
        continue
    mean = sum(vals) / len(vals)
    rounded = mean.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    if Decimal(mv).quantize(Decimal("0.0001")) == rounded:
        agree += 1
    else:
        bad.append((month, mv, str(mean)))
    if len(str(mean).split(".")[-1]) == 5 and str(mean)[-1] == "5":
        halfway.append(month)
print(f"EUR months 1999-01..last: {agree} agree to 4 dp (mean of daily values, half-up), disagree: {len(bad)}")
for b in bad[:10]:
    print("  disagree", b)
print(f"months with an exact half-way mean at the 5th decimal: {halfway}")
print(f"monthly series months from 1999-01 with a value: {sum(1 for m in monthly_series if m >= '1999-01')}")
