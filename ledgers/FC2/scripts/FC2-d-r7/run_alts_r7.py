"""Run each alternative implementation through the FC2 suite on seeds 0..49, and compare scan output with reference.py.

Usage: python -I run_alts_r5.py <grader_dir> <alts_dir> <reference_file>
"""

import importlib.util
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

grader = Path(sys.argv[1]).resolve()
alts = Path(sys.argv[2]).resolve()
reference = Path(sys.argv[3]).resolve()
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def suite(solution: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="fc2-alt-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(grader / name, work / name)
    shutil.copy(solution, work / "scanner.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run([sys.executable, "-m", "pytest", *FLAGS, "test_project.py"], cwd=work,
                         capture_output=True, text=True, env=env, check=False, timeout=300)
    shutil.rmtree(work)
    failed = sorted({line.split("::")[-1].split(" ")[0] for line in res.stdout.splitlines() if line.startswith("FAILED")})
    summary = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else res.stderr[-200:]
    return res.returncode == 0, summary + (" failing: " + ",".join(failed[:6]) if failed else "")


for path in sorted(alts.glob("alt*.py")):
    passed = 0
    first_fail = None
    for seed in range(50):
        ok, info = suite(path, seed)
        passed += ok
        if not ok and first_fail is None:
            first_fail = (seed, info)
    print(f"{path.name}: {passed}/50 seeds pass the suite")
    if first_fail:
        print(f"  first failure seed {first_fail[0]}: {first_fail[1]}")

# agreement with the reference on random chains (includes unequal spacing, ties and zero costs)
spec = importlib.util.spec_from_file_location("reference_mod", reference)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)  # type: ignore[union-attr]
for path in sorted(alts.glob("alt*.py")):
    mod_spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)  # type: ignore[union-attr]
    rng = random.Random(12345)
    disagree = 0
    checked = 0
    for _ in range(3000):
        n = rng.randint(1, 7)
        strikes = sorted(rng.sample(range(1, 400), n))
        spot = rng.randint(1, 400)
        df = rng.choice([1, 1_000_000, 990_000, 580_000, 500_000, rng.randint(1, 1_000_000)])
        calls = [rng.randint(0, 300) for _ in range(n)]
        puts = [rng.randint(0, 300) for _ in range(n)]
        chain = {"spot_cents": spot, "df_ppm": df, "strikes_cents": strikes, "call_cents": calls, "put_cents": puts,
                 "cost": {"fee_cents_per_contract": rng.randint(0, 5), "half_spread_cents": rng.randint(0, 5)}}
        try:
            want = [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in ref.scan(chain)]
            want_conv = ref.convexity_violations(strikes, calls, df)
        except ValueError:
            continue
        checked += 1
        got = [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in mod.scan(chain)]
        if got != want or mod.convexity_violations(strikes, calls, df) != want_conv:
            disagree += 1
    print(f"{path.name}: agreement with reference.py on random chains: {checked - disagree}/{checked} agree")
