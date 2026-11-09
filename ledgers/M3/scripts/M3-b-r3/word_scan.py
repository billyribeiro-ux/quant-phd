"""Round-3 slice b: print every occurrence (line number and context) of selected words in L04-L06 pages and cards.json."""
import re
import sys
from pathlib import Path

ROOT = Path(".")
words = sys.argv[1:] or ["covariance", "correlat", "variance", "expectation", "cholesky", "floating", "IEEE",
                         "principal", "portfolio", "shrinkage", "independen", "regression", "projection", "discount",
                         "Monte", "distribution", "least squares", "present value", "mean"]
files = [ROOT / f"course/modules/M/M3/L0{i}.html" for i in (4, 5, 6)] + [ROOT / "course/modules/M/M3/cards.json"]
for w in words:
    pat = re.compile(re.escape(w), re.I)
    for f in files:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in pat.finditer(line):
                s = max(0, m.start() - 60)
                print(f"[{w}] {f.name}:{n}: ...{line[s:m.end() + 60]}...")
