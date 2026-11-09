"""Run one method file on the instances of seeds first..last and report which path answered each call.

Usage: python -I path_stats.py <repo_root> <method.py> <first_seed> <last_seed>
Prints the count of front-end answers, fallback answers, the largest certificate residual, and the slowest call.
"""

import json
import sys
import time
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

repo, method, first, last = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(repo / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402

spec = spec_from_file_location("method", method)
mod = module_from_spec(spec)
sys.modules["method"] = mod
spec.loader.exec_module(mod)
paths: dict[str, int] = {}
worst = 0.0
slowest = 0.0
for seed in range(first, last + 1):
    case = json.loads(make_instance(seed)["payload"])
    started = time.monotonic()
    out = mod.allocate(case)
    slowest = max(slowest, time.monotonic() - started)
    paths[mod.LAST_PATH] = paths.get(mod.LAST_PATH, 0) + 1
    worst = max(worst, max(out["certificate"].values()))
print(method.name, paths, "largest certificate field", worst, "slowest call s", round(slowest, 3))
