"""Print every line-numbered match of a symbol pattern in the E3 slice files (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/symbol_scan.py PATTERN FILE [FILE ...]
"""

import re
import sys

pattern = re.compile(sys.argv[1])
for path in sys.argv[2:]:
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            for m in pattern.finditer(line):
                lo = max(0, m.start() - 35)
                hi = min(len(line), m.end() + 35)
                print(f"{path}:{n}: ...{line[lo:hi].rstrip()}...")
