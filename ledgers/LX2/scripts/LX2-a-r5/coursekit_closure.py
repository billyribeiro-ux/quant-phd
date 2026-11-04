"""Prerequisite closures used by the LX2 hub claim (usage: python3 -I coursekit_closure.py <repo_root>)."""

import sys

sys.path.insert(0, sys.argv[1] + "/tools")
import coursekit as k  # noqa: E402

for unit in ["LX2", "FC1"]:
    print(unit, "prerequisite closure:", sorted(k.prerequisite_closure(unit)))
