"""Per-seed checks: collect count, product count, and whether the two lower-margin products have equal margins."""
import json, subprocess, sys, pathlib, shutil, os
ROOT = pathlib.Path(sys.argv[1]).resolve()
SCR = pathlib.Path(sys.argv[2]).resolve()
G = ROOT / "course/modules/AC/AC4/grader"
PY = str(ROOT / ".venv/bin/python")
sys.path.insert(0, str(G))
from instance import make_instance  # noqa: E402  (grader file, read-only import)
counts = {}
eq = []
nprod = {}
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    rows = case["products"]
    nprod[len(rows)] = nprod.get(len(rows), 0) + 1
    m = [r["budget_price_cents"] - r["standard_inputs_per_unit"] * case["input_price_cents"] for r in rows[:2]]
    if m[0] == m[1]:
        eq.append(seed)
    allm = [r["budget_price_cents"] - r["standard_inputs_per_unit"] * case["input_price_cents"] for r in rows]
    if len(set(allm)) == 1:
        eq.append(("all3", seed))
print("products per seed:", nprod)
print("seeds where first two budgeted margins are equal:", eq)
d = SCR / "collect"
d.mkdir(parents=True, exist_ok=True)
for f in ("instance.py", "test_project.py", "starter.py"):
    shutil.copy(G / f, d / f)
for seed in range(50):
    env = dict(os.environ, QF_SEED=str(seed))
    p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--collect-only", "test_project.py"],
                       cwd=d, env=env, capture_output=True, text=True)
    counts[p.stdout.strip().splitlines()[-1]] = counts.get(p.stdout.strip().splitlines()[-1], 0) + 1
print("collect outcomes over seeds 0-49:", counts)
