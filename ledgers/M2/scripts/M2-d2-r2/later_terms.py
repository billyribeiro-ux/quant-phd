"""Find later-module or undeclared concept names in the slice text, with the sentence (prose-only is allowed per Architect Q5-Q8)."""
import re, sys
from pathlib import Path
pat = re.compile(r"yield to maturity|day.count|clean price|dirty price|forward rate|spot rate|macaulay|modified duration|DV01|convex|"
                 r"lagrang|multiplier|fubini|riemann|lebesgue|epsilon|continu|hessian|jacobian|gradient|schwarz|matrix|linear map|"
                 r"vector space|sequence|bond|option|call|prepay|annuit|perpetu|automatic|dual number|forward-mode|reverse|"
                 r"Lipschitz|cash flow|coupon|par\b|basis point|Taylor|remainder|envelope|implicit|kink|cancellation|quadrat|"
                 r"Fraction|exact rational|golden", re.I)
for path in sys.argv[1:]:
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    counts = {}
    for i, l in enumerate(lines, 1):
        for m in pat.finditer(l):
            counts[m.group(0).lower()] = counts.get(m.group(0).lower(), 0) + 1
    print(Path(path).name, sorted(counts.items(), key=lambda x: -x[1]))
