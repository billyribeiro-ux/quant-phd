"""Learner answer whose inequality multipliers are all positive (every one raised by EPS), checked with and without the floor.

Builds constrained_allocator.py as reference.py with allocate() replaced by a wrapper that adds EPS to every inequality
multiplier and reports the four certificate fields as the suite recomputes them. MODE 'floored' reports max(0, -min m);
MODE 'unfloored' reports -min m. Runs test_project.py on seeds given on the command line, in scratch directories only.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD5-M7-d")
G = ROOT / "course/modules/M/M7/grader"
PY = str(ROOT / ".venv/bin/python")
EPS = 2e-9
WRAPPER = '''

def allocate(instance):
    out = _reference_allocate(instance)
    mult = out["multipliers"]
    for key in ("lower", "upper", "sector", "turnover_plus", "turnover_minus"):
        mult[key] = [v + EPS for v in mult[key]]
    mult["turnover_total"] = mult["turnover_total"] + EPS
    w = out["weights"]
    n = len(w)
    gamma, mu, sigma = instance["gamma"], instance["mu"], instance["sigma"]
    w0, lo, up = instance["w0"], instance["lower"], instance["upper"]
    sec, caps, tau = instance["sector"], instance["sector_caps"], instance["turnover_limit"]
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    ssum = [sum(w[i] for i in range(n) if sec[i] == k) for k in range(len(caps))]
    pairs = []
    pairs += [(mult["lower"][i], lo[i] - w[i]) for i in range(n)]
    pairs += [(mult["upper"][i], w[i] - up[i]) for i in range(n)]
    pairs += [(mult["sector"][k], ssum[k] - caps[k]) for k in range(len(caps))]
    pairs += [(mult["turnover_plus"][i], d[i] - t[i]) for i in range(n)]
    pairs += [(mult["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
    pairs += [(mult["turnover_total"], sum(t) - tau)]
    primal = max([0.0, abs(sum(w) - 1.0), *[g for _, g in pairs]])
    floored = max(0.0, -min(m for m, _ in pairs))
    unfloored = -min(m for m, _ in pairs)
    cs = max(abs(m * g) for m, g in pairs)
    rw, rt = [], []
    for i in range(n):
        grad = gamma * sum(sigma[i][j] * w[j] for j in range(n)) - mu[i]
        rw.append(grad + mult["budget"] - mult["lower"][i] + mult["upper"][i] + mult["sector"][sec[i]]
                  + mult["turnover_plus"][i] - mult["turnover_minus"][i])
        rt.append(mult["turnover_total"] - mult["turnover_plus"][i] - mult["turnover_minus"][i])
    stat = max(max(abs(v) for v in rw), max(abs(v) for v in rt))
    out["certificate"] = {
        "primal_residual": primal,
        "stationarity_residual": stat,
        "dual_residual": FLOORED_OR_NOT,
        "complementary_slackness": cs,
    }
    return out
'''


def build(mode: str, seed: int) -> Path:
    src = (G / "reference.py").read_text(encoding="utf-8")
    src = src.replace("def allocate(instance: dict[str, Any]) -> dict[str, Any]:",
                      "def _reference_allocate(instance: dict[str, Any]) -> dict[str, Any]:", 1)
    wrapper = WRAPPER.replace("FLOORED_OR_NOT", "floored" if mode == "floored" else "unfloored")
    wrapper = f"EPS = {EPS!r}\n" + wrapper
    d = Path(f"/tmp/m7d-r5-floor/{mode}/{seed}")
    d.mkdir(parents=True, exist_ok=True)
    for name in ("test_project.py", "instance.py"):
        (d / name).write_text((G / name).read_text(encoding="utf-8"), encoding="utf-8")
    (d / "constrained_allocator.py").write_text(src + wrapper, encoding="utf-8")
    return d


if __name__ == "__main__":
    mode = sys.argv[1]
    seeds = [int(s) for s in sys.argv[2:]]
    for seed in seeds:
        d = build(mode, seed)
        env = dict(os.environ, QF_SEED=str(seed), PYTHONHASHSEED="0")
        res = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                              "test_project.py"], cwd=d, env=env, capture_output=True, text=True)
        failed = [line.split(" - ")[0] for line in res.stdout.splitlines() if line.startswith("FAILED")]
        print(f"{mode} seed {seed}: exit {res.returncode}; last line: {res.stdout.strip().splitlines()[-1]}")
        for f in failed[:6]:
            print("   ", f)
