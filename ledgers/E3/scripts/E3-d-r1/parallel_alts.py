"""Round-1 E3-d: the same alternative build and the same pytest command as run_alternatives.py, one seed per process.

Used to get alt4 and alt5 results sooner than the sequential run; each seed runs in its own scratch directory.
Usage: parallel_alts.py alt4 alt5 ... (seeds 0-9)
"""
import concurrent.futures as cf, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD1-E3-d")
sys.path.insert(0, str(ROOT / "ledgers/E3/scripts"))
import run_alternatives as ra  # the same module the sequential run uses

def run_one(name: str, seed: int) -> tuple[str, int, int]:
    work = Path(tempfile.mkdtemp(prefix=f"e3d1-{name}-s{seed}-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(ra.GRADER / f, work / f)
        (work / "elicit.py").write_text(ra.build(name), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, capture_output=True, text=True, check=False,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        return name, seed, r.returncode
    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == "__main__":
    names = sys.argv[1:]
    jobs = [(n, s) for n in names for s in range(10)]
    with cf.ThreadPoolExecutor(max_workers=20) as ex:
        results = list(ex.map(lambda j: run_one(*j), jobs))
    for name in names:
        rcs = {s: rc for n, s, rc in results if n == name}
        failed = sorted(s for s, rc in rcs.items() if rc != 0)
        print(f"{name}: {'PASS' if not failed else 'FAIL'} ({10 - len(failed)}/10 seeds" + ("" if not failed else f"; failing seeds {failed}") + ")", flush=True)
