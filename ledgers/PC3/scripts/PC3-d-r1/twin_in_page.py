"""For each PC3 lesson, report twin output lines (run under python -I -W error) that are absent from the lesson HTML.

Run: python3 -I ledgers/PC3/scripts/PC3-d-r1/twin_in_page.py  (from the checkout root)
"""
import html
import pathlib
import sys

root = pathlib.Path(".")
missing_total = 0
for lesson in ("L01", "L02", "L03", "L04", "L05", "L06"):
    out = pathlib.Path(f"ledgers/PC3/scripts/PC3-d-r1/out/twin-{lesson}.out").read_text(encoding="utf-8").splitlines()
    page = html.unescape(pathlib.Path(f"course/modules/PC/PC3/{lesson}.html").read_text(encoding="utf-8"))
    miss = [line for line in out if line.strip() and line.strip() not in page]
    missing_total += len(miss)
    print(f"{lesson}: {len(out)} twin lines, {len(miss)} not found verbatim in the page")
    for line in miss[:5]:
        print("   missing:", line)
sys.exit(0 if missing_total == 0 else 1)
