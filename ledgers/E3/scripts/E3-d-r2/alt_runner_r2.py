"""Run one alternative (alt1..alt5) of run_alternatives.py on the given seeds, same pytest flags.

Usage: python3 run_alt_one.py <alt> <seeds>   (seeds like 0-9)
Used to run the five alternatives in parallel; the build and the pytest invocation are the ones in
ledgers/E3/scripts/run_alternatives.py, imported from that file.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_alternatives", SCRIPTS / "run_alternatives.py")
assert spec is not None and spec.loader is not None
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

name, seed_text = sys.argv[1], sys.argv[2]
seeds = ra.seeds_of(seed_text)
work = Path(tempfile.mkdtemp(prefix=f"e3-{name}-"))
failed: list[int] = []
try:
    for f in ("test_project.py", "instance.py"):
        shutil.copy(ra.GRADER / f, work / f)
    (work / "elicit.py").write_text(ra.build(name), encoding="utf-8")
    for seed in seeds:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        )
        print(f"seed {seed}: rc={result.returncode} {result.stdout.strip().splitlines()[-1:]}", flush=True)
        if result.returncode != 0:
            failed.append(seed)
            print(result.stdout[-1500:], flush=True)
finally:
    shutil.rmtree(work, ignore_errors=True)
verdict = "PASS" if not failed else "FAIL"
print(f"{name}: {verdict} ({len(seeds) - len(failed)}/{len(seeds)} seeds" + ("" if not failed else f"; failing {failed}") + ")", flush=True)
