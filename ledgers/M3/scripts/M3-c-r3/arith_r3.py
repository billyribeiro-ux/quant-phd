import math
import numpy as np
# L08 E1 bound from printed inputs (page line 284 and 377)
m11, t0 = 13.6818, 88.2028
print("E1 bound from printed inputs:", round(100 * m11 / (t0 + 99 * m11), 4), 100 * m11 / (t0 + 99 * m11))
print("shares sum of printed top three (percent):", 75.9 + 18.1 + 5.2)
# L09 E2: C0 vs R (R off-diagonal 0.5, 0.5, -0.5)
c0 = np.array([[1, .9, .9], [.9, 1, -.9], [.9, -.9, 1.]])
r = np.array([[1, .5, .5], [.5, 1, -.5], [.5, -.5, 1.]])
print("||C0-R||_F^2:", round(float(np.sum((c0 - r) ** 2)), 12), " sqrt:", round(math.sqrt(0.96), 4))
# L09 C0 clipped squared distance and eigenvalues
w, v = np.linalg.eigh(c0)
print("C0 eigenvalues:", np.round(w, 6), " sum of squared negative eigenvalues:", float(np.sum(np.minimum(w, 0) ** 2)))
# L09 Example 2.3 witness
x = np.array([1, -1, -1.])
print("x^T C0 x:", float(x @ c0 @ x))
