# Example 5.1 and Lab 3 floor values, recomputed independently (scratch).
import numpy as np
pr = np.array([0.25, 0.5, 0.25]); m = np.array([1.2, 0.9, 0.8]); z = np.array([3.0, 1.0, -1.0])
price = pr @ (m * z); Ez2 = pr @ z**2; c = price / Ez2
print("price", round(price, 6), "E[z2]", Ez2, "c", round(c, 6), "x*", np.round(c*z, 6).tolist(), "E[x*^2]", round(float(pr @ (c*z)**2), 6), "E[m^2]", round(float(pr @ m**2), 6))
print("E[x* e3]", round(float(pr[2] * c * z[2]), 6))
# Lab 3 floor 0 closed form: m_s = max(lam z_s, floor); solve E[m z] = price by bisection
for floor in (0.0, 0.1, 0.5):
    lo, hi = 0.0, 10.0
    for _ in range(200):
        lam = (lo + hi) / 2
        if pr @ (np.maximum(lam * z, floor) * z) < price: lo = lam
        else: hi = lam
    mm = np.maximum(lam * z, floor)
    print("floor", floor, "m", np.round(mm, 4).tolist(), "E[m^2]", round(float(pr @ mm**2), 4))
