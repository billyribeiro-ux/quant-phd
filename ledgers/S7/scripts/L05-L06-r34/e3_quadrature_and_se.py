"""Round-34 quadrature and seeded-simulation checks for L06 Problem E3 and L05 Problem E3.

(a) L06 E3 (page line 437): P(|N(3,1)| > 1.96) by scipy.integrate.quad over the density (page: 0.851 via Phi terms);
    the truly-null share among published findings for pi1 = 0.1, 0.3, 0.6; Holm's Bonferroni comparison
    Phi^-1(1 - 0.05/800) = 3.836 (page line 470).
(b) L06 E3 seeded simulation (sol-S7-L06-E3, seed 64): re-run with a per-replication standard error added, so that the
    page's claim 'agree within Monte Carlo error' is judged with the simulation's own SE.
(c) L05 E3 (page lines 1082-1123): derived quantities 1 - Phi(5.224), Phi(1.045), P(N(0,1) > 1.9545), P(1.6449 < N(3,1)
    < 1.9545), P(N(3,1) > 1.6449), and the StepM and step-down derived values, by quadrature and scipy.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/e3_quadrature_and_se.py <scratch-dir>
"""

from __future__ import annotations

import contextlib
import io
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy import integrate
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[4]
TWIN = ROOT / "tests" / "labs" / "S7" / "sol-S7-L06-E3.py"
scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
scratch.mkdir(parents=True, exist_ok=True)

# (a)
def density(x: float) -> float:
    return float(norm.pdf(x, loc=3.0, scale=1.0))

p_pub_real, _ = integrate.quad(density, 1.96, math.inf)
p_pub_real += integrate.quad(density, -math.inf, -1.96)[0]
p_pub_null = 2 * norm.sf(1.96)
print(f"P(|N(3,1)|>1.96) by quad = {p_pub_real:.6f} (page 0.851); P(|N(0,1)|>1.96) = {p_pub_null:.6f}")
for pi1 in (0.1, 0.3, 0.6):
    share = (1 - pi1) * p_pub_null / ((1 - pi1) * p_pub_null + pi1 * p_pub_real)
    print(f"truly-null share among published, pi1={pi1}: {share:.6f} -> {share:.3f} (page {{0.346, 0.121, 0.038}})")
print(f"Phi^-1(1-0.05/800) = {norm.ppf(1 - 0.05 / 800):.6f} (page 3.836)")

# (b) seeded simulation with per-replication SE: the twin's code, with the printing replaced
src = TWIN.read_text(encoding="utf-8")
old = 'print(f"{pi1} {np.mean(null_share):.3f} {np.mean(unrejected):.3f} {np.mean(hurdle):.2f}")'
assert src.count(old) == 1
new = (
    'se_null = np.std(null_share, ddof=1) / np.sqrt(reps)\n'
    '    print(f"{pi1} {np.mean(null_share):.3f} {np.mean(unrejected):.3f} {np.mean(hurdle):.2f} '
    'null_share_SE {se_null:.4f} derived_null_share {(1 - pi1) * p_pub_null / ((1 - pi1) * p_pub_null + pi1 * p_pub_real):.4f}")'
)
variant = scratch / "sol_L06_E3_with_se.py"
variant.write_text(src.replace(old, new).replace("from statistics import NormalDist",
                    "from statistics import NormalDist\nfrom scipy.integrate import quad\nfrom scipy.stats import norm as _norm\n"
                    "p_pub_real = quad(lambda x: _norm.pdf(x, 3.0, 1.0), 1.96, float('inf'))[0] + quad(lambda x: _norm.pdf(x, 3.0, 1.0), float('-inf'), -1.96)[0]\n"
                    "p_pub_null = 2 * _norm.sf(1.96)", 1), encoding="utf-8")
import subprocess  # noqa: E402

res = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(variant)], cwd=scratch,
                     capture_output=True, text=True, check=False)
print("sol-S7-L06-E3 with per-replication SE: rc", res.returncode, "stderr bytes", len(res.stderr))
print(res.stdout + res.stderr)

# (c) L05 E3 derived values
c_unstud = 8.224268135  # solves Phi(c) Phi(c/5) = 0.95 (checked in derive_numbers.py)
c_stud = float(norm.ppf(0.95 ** 0.5))
print(f"c_studentized = {c_stud:.6f} (page 1.955)")
print(f"1 - Phi(5.224) = {norm.sf(5.224):.4e} (page 9e-8)")
print(f"Phi(3 - 1.955) = Phi(1.045) = {norm.cdf(3 - 1.955):.6f} (page 0.852)")
print(f"Phi(1.045492...) with c = {c_stud:.6f}: {norm.cdf(3 - c_stud):.6f}")
a = float(norm.sf(c_stud))
b = float(norm.cdf(1.6448536269514722 - 3) - norm.cdf(c_stud - 3 * 0 - 3))  # placeholder kept out of use
b = float(norm.cdf(c_stud - 3) - norm.cdf(1.6448536269514722 - 3))
print(f"P(N(0,1) > c_stud) = {a:.6f} (page 0.0253)")
print(f"P(1.6449 < N(3,1) < c_stud) = {b:.6f} (page 0.0602)")
print(f"StepM studentized derived 0.8521 + 0.0253 x 0.0602 = {0.8521 + 0.0253 * 0.0602:.6f} (page 0.8536)")
print(f"unstudentized step-2 derived: P(null strategy 2 clears 8.224 with sd 5) = {norm.sf(c_unstud / 5):.6f}; "
      f"P(N(3,1) > 1.6449) = {norm.sf(1.6448536269514722 - 3):.6f}; product = {norm.sf(c_unstud / 5) * norm.sf(1.6448536269514722 - 3):.6f} (page 0.046 from 0.050 x 0.912)")
print(f"MC SE of 0.85 over 20000 = {math.sqrt(0.85 * 0.15 / 20000):.5f} (page 0.0025)")
