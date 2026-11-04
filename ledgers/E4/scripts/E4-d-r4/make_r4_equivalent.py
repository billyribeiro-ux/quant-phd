"""Write the round-4 observationally equivalent candidate (price slope without the uninformed term) into the scripts dir.

Usage: python -I ledgers/E4/scripts/E4-d-r4/make_r4_equivalent.py <repo-root>. Its equivalence argument is the row
proof-price-slope-equivalent in ledgers/E4/E4-d.json (round 4).
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
ref_doc_end = ref.index('"""', 3) + 3
body = ref[ref_doc_end:]
old = "    b_s = (lam * tau_e + (1.0 - lam) * tau_y) / denominator"
assert body.count(old) == 1
text = (
    '"""Price slope b_s drops the uninformed term (1 - lam) tau_y from its numerator (observationally equivalent).\n\n'
    "Single edit of grader/reference.py, written by the verifier (slice E4-d, round 4). Not a fault: see the fragment.\n"
    '"""'
)
out = text + body.replace(old, "    b_s = (lam * tau_e) / denominator")
(root / "ledgers/E4/scripts/E4-d-r4/equivalent_candidate_price_slope.py").write_text(out, encoding="utf-8")
print("wrote equivalent candidate")
