# For argv[1] (an elicit.py candidate path) and seeds 0-9: the estimate's lambda score (central difference in log lambda,
# step 1e-5, oracle log-likelihood) and the largest log-likelihood gain from a 0.1 percent move in lambda, up or down.
import os, subprocess, sys, shutil, tempfile
from pathlib import Path
cand = Path(sys.argv[1]).resolve()
G = Path("course/modules/E/E3/grader").resolve()
probe = r'''
import math, sys
import test_project as tp
lam_s = tp.est()["lambda_hat"]; g = tp.est()["gamma_hat"]; k = tp.est()["kappa_hat"]
h = 1e-5
score = (tp.oracle_loglik(tp.PARSED, g, lam_s*math.exp(h), k) - tp.oracle_loglik(tp.PARSED, g, lam_s*math.exp(-h), k)) / (2*h)
here = tp.oracle_loglik(tp.PARSED, g, lam_s, k)
gain = max(tp.oracle_loglik(tp.PARSED, g, lam_s*(1+s), k) - here for s in (1e-3, -1e-3))
print(f"lambda_hat={lam_s:.10g} lambda_score={score:.3e} max_gain_lambda_move_0.1pct={gain:.3e}")
'''
for seed in range(10):
    work = Path(tempfile.mkdtemp(prefix="r9score-"))
    try:
        for f in ("instance.py", "test_project.py"):
            shutil.copy(G / f, work / f)
        shutil.copy(cand, work / "elicit.py")
        (work / "probe.py").write_text(probe, encoding="utf-8")
        r = subprocess.run([sys.executable, "probe.py"], cwd=work, capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        print("seed", seed, (r.stdout.strip() or r.stderr.strip()[-300:]))
    finally:
        shutil.rmtree(work, ignore_errors=True)
