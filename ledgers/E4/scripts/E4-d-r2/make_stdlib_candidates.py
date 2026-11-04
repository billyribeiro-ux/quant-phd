"""Write two correct standard-library-only solvers that import extra stdlib modules (verifier, slice d, round 2).

Each candidate is grader/reference.py with one stdlib import added and used harmlessly, so the solver stays correct.
Usage: python -I ledgers/E4/scripts/E4-d-r2/make_stdlib_candidates.py <repo-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/E4/scripts/E4-d-r2/candidates"
out.mkdir(parents=True, exist_ok=True)

assert src.count("import math\n") == 1 and src.count("def _check_inputs") == 1
collections_cand = src.replace("import math\n", "import math\nimport collections\n", 1)
collections_cand = collections_cand.replace(
    "def _check_inputs", "PARAMS = collections.OrderedDict(a=RISK_AVERSION)\n\n\ndef _check_inputs", 1
)
(out / "stdlib_collections_solver.py").write_text(collections_cand, encoding="utf-8")

decimal_cand = src.replace("import math\n", "import math\nimport decimal\nimport statistics\n", 1)
decimal_cand = decimal_cand.replace(
    "def _check_inputs",
    "DECIMAL_ZERO = decimal.Decimal(0)\nNORMAL = statistics.NormalDist()\n\n\ndef _check_inputs",
    1,
)
(out / "stdlib_decimal_statistics_solver.py").write_text(decimal_cand, encoding="utf-8")
print("wrote 2 candidates")
