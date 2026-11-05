"""Run run_candidates_r10.py over every grader mutant (seeds given), six at a time, one output file per mutant."""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d")
seeds = sys.argv[1]
outdir = ROOT / sys.argv[2]
outdir.mkdir(parents=True, exist_ok=True)
mutants = sorted(p for p in (ROOT / "ledgers/SC1/mutants").glob("*.py") if "SC1a" not in p.name)


def run(path: Path) -> None:
    with open(outdir / (path.stem + ".txt"), "w", encoding="utf-8") as fh:
        subprocess.run([str(ROOT / ".venv/bin/python"), "-I", str(ROOT / "ledgers/SC1/scripts/SC1-d-r10/run_candidates_r10.py"),
                        seeds, str(path)], stdout=fh, stderr=subprocess.STDOUT, cwd=ROOT, check=False)


with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(run, mutants))
(outdir / "_done.txt").write_text(f"done {len(mutants)} mutants\n", encoding="utf-8")
