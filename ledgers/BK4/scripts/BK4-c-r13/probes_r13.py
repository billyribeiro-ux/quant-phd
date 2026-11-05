"""Round-13 BK4-c probes, run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-c-r13/probes_r13.py

1. Cap probes: the capital layer and the margin layer capped at the survivors' pool (not in ledgers/BK4/mutants,
   so they are probes, not counted mutants). Each is run on seeds 0-49 with the suite.
2. The r13d mutant (fund layer capped at the survivors' pool, ledgers/BK4/mutants/r13d_*.py) on seeds 0-49.
3. The starter: the suite on starter.py must fail with named messages (count of 'has no implementation for').
"""

import os
import shutil
import subprocess

ROOT = os.getcwd()
PY = os.path.join(ROOT, ".venv", "bin", "python")
GRADER = os.path.join(ROOT, "course", "modules", "BK", "BK4", "grader")
REF = open(os.path.join(GRADER, "reference.py"), encoding="utf-8").read()
SCRATCH = "/tmp/bk4c_r13/probes"


def suite_on(name, source, seeds=range(50)):
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    with open(os.path.join(d, "clearing_house.py"), "w", encoding="utf-8") as handle:
        handle.write(source)
    for f in ("test_project.py", "instance.py"):
        shutil.copy(os.path.join(GRADER, f), d)
    failed = []
    for s in seeds:
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=d, env=dict(os.environ, QF_SEED=str(s)),
                           capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(s)
    return failed, d


probes = {
    "capital_capped_at_pool": (
        "    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)\n",
        "    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents, "
        "sum(v for m, v in default_fund_cents.items() if m != defaulter_id))\n"),
    "margin_capped_at_pool": (
        "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])\n",
        "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id], "
        "sum(v for m, v in default_fund_cents.items() if m != defaulter_id))\n"),
}
for name, (old, new) in probes.items():
    assert REF.count(old) == 1, name
    failed, _ = suite_on(name, REF.replace(old, new, 1))
    print(f"probe {name}: killed on {len(failed)} of 50 seeds; killing seeds {failed[:12]}")

mutant = open(os.path.join(ROOT, "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py"),
              encoding="utf-8").read()
failed, _ = suite_on("r13d_seeds_0-49", mutant)
print(f"mutant r13d (ledgers/BK4/mutants): killed on {len(failed)} of 50 seeds")

# Starter: the suite must fail on every seed, with named messages.
starter = open(os.path.join(GRADER, "starter.py"), encoding="utf-8").read()
failed, d = suite_on("starter", starter, seeds=[0])
out = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                      "test_project.py"], cwd=d, env=dict(os.environ, QF_SEED="0"), capture_output=True, text=True).stdout
print("starter on seed 0: failing tests named 'has no implementation for':", out.count("has no implementation for"),
      "| summary line:", out.strip().splitlines()[-1])
