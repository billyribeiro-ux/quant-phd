"""List unlinked occurrences of prerequisite-owned concept names in CF8 hub, L01, L02 (run with python -I)."""
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]) / "course/modules/CF/CF8"
PHRASES = [
    "net present value", "net working capital", "present value", "discount factor", "balance sheet",
    "income statement", "cash-flow statement", "cash flow statement", "annuity", "NPV",
]
for name in ["index.html", "L01.html", "L02.html"]:
    lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, 1):
        # drop linked spans and dfn
        stripped = re.sub(r'<a class="concept"[^>]*>.*?</a>', lambda m: "@" * len(m.group(0)), line)
        stripped = re.sub(r'<dfn[^>]*>.*?</dfn>', lambda m: "@" * len(m.group(0)), stripped)
        # skip script and attribute-only text
        for p in PHRASES:
            for mm in re.finditer(re.escape(p), stripped, re.I):
                ctx = stripped[max(0, mm.start() - 40): mm.end() + 20]
                print(f"{name}:{i}: [{p}] ...{ctx}...")
