"""SC1 slice a, round 9: owner of every concept linked from index.html, L01, L02, L03, and closure membership.

Run from the checkout root with: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/concept_owner_r9.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
import coursekit  # noqa: E402

owners = coursekit.concept_owner()
closure = coursekit.prerequisite_closure("SC1")
print("closure:", sorted(closure))
pages = ["index.html", "L01.html", "L02.html", "L03.html"]
seen: dict[str, tuple[str, str]] = {}
for page in pages:
    text = (ROOT / "course/modules/SC/SC1" / page).read_text(encoding="utf-8")
    for m in re.finditer(r'class="concept" data-concept="([^"]+)"', text):
        cid = m.group(1)
        seen.setdefault(cid, (page, owners.get(cid, "UNDEFINED")))
for cid, (page, owner) in sorted(seen.items()):
    ok = owner in closure or owner == "SC1"
    print(f"{cid:35s} first-seen={page:10s} owner={owner:6s} in_closure_or_SC1={ok}")
# the hub's From-M4 / From-M5 / From-M6 / From-P0.1 lists assert owners; print owners for the named ones
for cid in ["geometric-series","proof-by-contradiction","limit","derivative","random-variable","normal-distribution","multivariate-normal","independence","expectation","variance","moment-generating-function","characteristic-function","cauchy-sequence","completeness-of-reals","uniform-convergence","probability-space","sigma-algebra","filtration","martingale","stopping-time","optional-stopping-theorem","dominated-convergence-theorem","evidence-grade","project-ladder"]:
    print("claimed-owner", cid, owners.get(cid))
