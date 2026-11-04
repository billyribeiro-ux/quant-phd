"""Recompute the box bounds stated on project.html (Inputs paragraph, line 313) and in grader/instance.py (verifier, round 2).

Usage: python -I ledgers/E4/scripts/E4-d-r2/box_bounds.py <repo-root>
"""

import math

A, TV, TE = 2.0, 1.0, 1.0
tau_bar = lambda c: (TV + TE) * math.exp(-2 * A * c) - TV  # noqa: E731
tau_y1 = lambda sd: TE * TE / (TE + A * A * sd * sd)  # noqa: E731
print("tau_bar(0.120) =", f"{tau_bar(0.120):.6f}", "-> stated 0.2376")
print("tau_bar(0.150) =", f"{tau_bar(0.150):.6f}", "-> stated 0.0976")
print("min tau_y(1) over sd in [0.5, 0.75] =", f"{tau_y1(0.75):.6f}", "-> stated 0.3077")
print("max tau_bar over box =", f"{max(tau_bar(0.120 + 0.030 * k / 200) for k in range(201)):.6f}", "-> stated 0.2376 (bound 0.2377)")
print("interior condition tau_bar < tau_y(1) at worst corner:", tau_bar(0.120) < tau_y1(0.75))
