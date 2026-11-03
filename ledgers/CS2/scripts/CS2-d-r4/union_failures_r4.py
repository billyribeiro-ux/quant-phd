"""Round-4: union of failing test names over seeds 0-49 for each candidate (over-constraint check)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_alts import parse, run  # noqa: E402

for name in sys.argv[2:]:
    union: dict[str, int] = {}
    for seed in parse(sys.argv[1]):
        ok, out = run(Path(name).resolve(), seed)
        if not ok:
            for t in re.findall(r"FAILED \S+::(\S+)", out):
                union[t] = union.get(t, 0) + 1
    print(Path(name).name, "failing tests over seeds:", union or "none")
