"""Round 15 candidate runner (verifier scratch). Usage: run_cand_r15.py SOLUTION.py SEEDS [--collect]
Builds the same workspace as tools/run_graders.py and runs the suite on each seed."""
import sys, subprocess, os, shutil, tempfile
from pathlib import Path
REPO = Path("/Users/billyribeiro/.fanout/wt/verifyE15-PC3-c")
sys.path.insert(0, str(REPO / "tools"))
GRADER = REPO / "course/modules/PC/PC3/grader"
def workspace(solution: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="pc3c-r15-"))
    for name in ["test_project.py", "engine.py", "instance.py"]:
        shutil.copy(GRADER / name, work / name)
    shutil.copy(solution, work / "market_maker.py")
    return work
def run(work: Path, seed: int, collect: bool) -> tuple[int, str]:
    args = [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
    if collect:
        args.append("--collect-only")
    args.append("test_project.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    r = subprocess.run(args, cwd=work, capture_output=True, text=True, env=env, timeout=600)
    return r.returncode, (r.stdout[-1500:] + r.stderr[-800:])
if __name__ == "__main__":
    sol = Path(sys.argv[1]).resolve()
    seeds = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] != "range" else list(range(50))
    collect = "--collect" in sys.argv
    work = workspace(sol)
    try:
        for s in seeds:
            code, out = run(work, s, collect)
            last = [ln for ln in out.strip().splitlines() if ln.strip()][-1:] if out.strip() else [""]
            failed = sorted({ln.split("::")[1].split(" ")[0] for ln in out.splitlines() if ln.startswith("FAILED ")})
            print(f"seed={s} exit={code} last={last[0][:160]} failed={failed[:3]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
