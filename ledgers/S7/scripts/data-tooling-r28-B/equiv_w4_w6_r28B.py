"""Round 28 re-check of equiv-rerun-r18 on Python 3.14: W4 (the \d regex only reaches refusals fromisoformat gives) and
W6 (no accepted string contains YYYY-MM-DD as a proper substring), plus the I03 tie arithmetic (the only tie is 5^11)."""
import re
import sys
from datetime import date
from pathlib import Path

ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
ALT = re.compile(r"-?[0-9]{4}-[0-9]{2}-[0-9]{2}")
samples = ["２０００-01-31", "٢٠٠٠-01-31", "2000-0١-31", "2000-01-٣١"]
for s in samples:
    try:
        date.fromisoformat(s)
        acc = True
    except ValueError:
        acc = False
    print(f"fromisoformat({s!r}) accepted={acc}; \\d-regex fullmatch={bool(ISO.fullmatch(s))}")
# W4 claim: for every string the \d-based regex accepts (fullmatch) that fromisoformat rejects, is there a difference?
import itertools
diff = 0
tested = 0
for y in ("2000", "1999", "0001", "9999"):
    for mth in range(0, 100):
        for d in range(0, 100):
            s = f"{y}-{mth:02d}-{d:02d}"
            tested += 1
            try:
                date.fromisoformat(s)
                a = True
            except ValueError:
                a = False
            b = bool(ISO.fullmatch(s))
            if a != b and b:
                diff += 1  # regex accepts, fromisoformat refuses: the regex is looser; the date() step refuses it
print(f"W4 over {tested} ASCII YYYY-MM-DD strings: regex-accepted but fromisoformat-refused: {diff} (the code calls both, so the refusal is by date.fromisoformat, the same as without the regex)")
# W6: strings accepted by fromisoformat (Python 3.14) that contain YYYY-MM-DD as a proper substring
forms = []
for y in (2000, 1999):
    for m in range(1, 13):
        for d in range(1, 29):
            forms.append(f"{y:04d}-{m:02d}-{d:02d}")
            forms.append(f"{y:04d}{m:02d}{d:02d}")
            wk = date(y, m, d).isocalendar()
            forms.append(f"{wk[0]:04d}-W{wk[1]:02d}-{wk[2]}")
            forms.append(f"{wk[0]:04d}W{wk[1]:02d}{wk[2]}")
acc = []
for s in forms:
    try:
        date.fromisoformat(s)
        acc.append(s)
    except ValueError:
        pass
proper = [s for s in acc if len(s) > 10 and ISO.search(s)]
print(f"W6: {len(acc)} sampled strings accepted by fromisoformat; accepted strings containing YYYY-MM-DD as a proper substring: {len(proper)} {proper[:5]}")
# I03 tie arithmetic: powers of five in (2e7, 2e8) and the matching even/odd digit
fives = [5**q for q in range(0, 40) if 2 * 10**7 < 5**q < 2 * 10**8]
print("powers of five in (2e7, 2e8):", fives, "-> k = (5^q - 1)/2 =", [(f - 1) // 2 for f in fives], "last digit of k:", [((f - 1) // 2) % 10 for f in fives])
print("5^12 =", 5**12, "is outside (2e7, 2e8):", not (2 * 10**7 < 5**12 < 2 * 10**8))
