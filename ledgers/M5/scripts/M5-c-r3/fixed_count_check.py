"""Round-3 check of L09 Misconception 3: does some fixed count N certify tolerance 1e-6 (cert_N <= 1e-6)?

Independent of the lab: iterate V_{n+1} = B V_n on GRID with beta = 0.9 from 0 and print cert_N for selected N.
"""

import math

GRID = (0.25, 0.5, 0.75, 1.0)
BETA = 0.9


def B(V):
    out_vals = []
    for k in GRID:
        out = k**0.5
        best = max(math.sqrt(out - kp) + BETA * V[j] for j, kp in enumerate(GRID) if kp <= out)
        out_vals.append(best)
    return out_vals


V_prev = [0.0] * 4
V = B(V_prev)
first = None
for n in range(1, 400):
    cert = BETA / (1 - BETA) * max(abs(a - b) for a, b in zip(V, V_prev))
    if n in (10, 100, 147, 151, 152, 200, 300):
        print(f"N={n} cert_N={cert:.6e}")
    if first is None and cert <= 1e-6:
        first = n
    V_prev, V = V, B(V)
print("first fixed N with cert_N <= 1e-6:", first)
