"""Round-8 verifier script: complete the two partial alternatives by splicing one changed class into the reference module."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-CS2-d")
A = ROOT / "ledgers/CS2/scripts/CS2-d-r8/alts"
REF = (ROOT / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")


def splice(ref: str, cls: str, new_src: str) -> str:
    start = ref.index(f"class {cls}")
    nxt = re.search(r"\n\n\nclass ", ref[start + 1:])
    end = start + 1 + nxt.start() + 3 if nxt else len(ref)
    return ref[:start] + new_src.strip("\n") + "\n" + ("\n\n" + ref[end:].lstrip("\n") if nxt else "")


# alt_r8_03: Welford with the delta-squared identity, spliced into the full reference
alt03 = (A / "alt_r8_03_welford_delta_identity.py").read_text(encoding="utf-8")
w = alt03[alt03.index("class WelfordAccumulator"):]
full03 = splice(REF, "WelfordAccumulator", w)
full03 = full03.replace('"""Reference solution', '"""Alternative (full module): Welford with the delta-squared identity. Reference solution', 1)
(A / "alt_r8_03_welford_delta_identity_full.py").write_text(full03, encoding="utf-8")

# alt_r8_04: exact stored-rank sketch, spliced into the full reference
alt04 = (A / "alt_r8_04_sketch_exact_fraction_stored_ranks.py").read_text(encoding="utf-8")
q = alt04[alt04.index("class QuantileSketch"):]
full04 = splice(REF, "QuantileSketch", q)
full04 = full04.replace("from fractions import Fraction\n", "from fractions import Fraction\n", 1)
full04 = full04.replace("import math\nfrom bisect import bisect_right\n", "import bisect\nimport math\nfrom bisect import bisect_right\n", 1)
(A / "alt_r8_04_sketch_exact_fraction_stored_ranks_full.py").write_text(full04, encoding="utf-8")
print("ok")
