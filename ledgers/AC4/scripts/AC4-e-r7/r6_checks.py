"""Round-6 checks for AC4 slice e: run from the checkout root with .venv/bin/python -I.

1. Reference and collection counts on the learner-facing grader files (per seed, scratch copy).
2. Alternative engines alt_e/alt_f/alt_g (this directory) and alt_a-c (alternatives_r4.py) on seeds 0-9 and 25.
3. Instance payloads of the current instance.py against the 00745fe copy (git show), seeds 0-499.
4. Assertion-message count of test_project.py.
Mutant runs: tools/mutate_graders.py --unit AC4 --seeds 0-9 and scripts/AC4-e-r5/run_mutants.py (copied to AC4-e-r6).
"""
import ast
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
SCR = pathlib.Path(sys.argv[2]).resolve()
PY = str(ROOT / ".venv/bin/python")
GRADER = ROOT / "course/modules/AC/AC4/grader"
HERE = pathlib.Path(__file__).resolve().parent


def suite(engine: pathlib.Path, seed: int) -> str:
    d = SCR / engine.stem / str(seed)
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    for f in ("instance.py", "test_project.py", "starter.py"):
        shutil.copy(GRADER / f, d / f)
    shutil.copy(engine, d / "budget_engine.py")
    p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                        "test_project.py"], cwd=d, env=dict(os.environ, QF_SEED=str(seed)),
                       capture_output=True, text=True)
    return p.stdout.strip().splitlines()[-1]


for engine in sorted(HERE.glob("alt_[efg].py")):
    for seed in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 25):
        print(engine.name, seed, suite(engine, seed))

reference = ROOT / "course/modules/AC/AC4/grader/reference.py"
for seed in (0, 1, 2, 3, 5, 99, 455320725):
    print("reference", seed, suite(reference, seed))

spec = importlib.util.spec_from_file_location("old_instance", SCR / "instance_00745fe.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
new_spec = importlib.util.spec_from_file_location("new_instance", GRADER / "instance.py")
new = importlib.util.module_from_spec(new_spec)
new_spec.loader.exec_module(new)
print("instance payloads equal for seeds 0-499:", all(old.make_instance(s) == new.make_instance(s) for s in range(500)))

tree = ast.parse((GRADER / "test_project.py").read_text(encoding="utf-8"))
asserts = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
print("asserts", len(asserts), "without message", sum(a.msg is None for a in asserts))
