# Independent recheck of L04 hand-derived numbers (Example 4.2, M1-M3, E1-E3, Lab 4 header mapping).
import numpy as np
probs = np.array([0.25, 0.5, 0.25])
X = np.array([[1.0, 1.4], [1.0, 1.1], [1.0, 0.6]])
p = np.array([0.96, 0.976])
S = X.T @ (probs[:, None] * X)
print("E[xx']", S.round(6).tolist())
b = np.linalg.solve(S, p)
print("b", b.round(6).tolist())
xs = X @ b
print("x*", xs.round(6).tolist(), "E[x*]", round(float(probs @ xs), 9), "E[x*x_stock]", round(float(probs @ (xs * X[:, 1])), 9))
print("E[x*^2]", round(float(probs @ xs**2), 9), "b.p", round(float(b @ p), 9))
# tau on the segment
a, c = np.array([0.5, 0, 0.46]), np.array([0, 0.8, 0.16])
d = c - a
tau = np.linalg.lstsq(d[:, None], (xs * probs) - a, rcond=None)[0][0]
print("tau", round(float(tau), 6), "check state prices", (a + tau * d).round(6).tolist(), "pi*x*", (probs * xs).round(6).tolist())
# M1
print("M1 m", (0.448/0.6), (0.522/0.4), "E[m]", 0.6*0.448/0.6+0.4*0.522/0.4, "Rf", 1/0.97, "price stock", 0.6*(0.448/0.6)*1.3+0.4*(0.522/0.4)*0.8)
# M2
z = np.array([2.0, 1.0, 0.0]); Ez2 = z @ z / 3; c2 = 0.9 / Ez2
print("M2 c", c2, "x*", (c2*z).round(6).tolist(), "E[x*^2]", c2*c2*Ez2)
# M3
xs3 = np.array([0.824242, 0.940606, 1.134545]); pr = np.array([0.25, 0.5, 0.25])
print("M3 E[x* stock]", round(float(pr @ (xs3 * np.array([1.4, 1.1, 0.6]))), 6), "E[x*^2]", round(float(pr @ xs3**2), 6))
print("M3 terms", round(0.25*0.824242*1.4,6), round(0.5*0.940606*1.1,6), round(0.25*1.134545*0.6,6))
print("M3 E[x*^2] terms", round(0.25*0.824242**2,6), round(0.5*0.940606**2,6), round(0.25*1.134545**2,6))
print("M3 b.p", round(1.367273*0.96 - 0.387879*0.976, 6))
# E1, E2, E3 values
print("E1 ratio", round(1.004012/1.133251, 4), "1-ratio", round(1-1.004012/1.133251, 4))
print("E2 1/1.003", round(1/1.003, 6))
for k in (0, 1, 6.75, 7):
    price = 0.25*3*1.2 + 0.5*1*0.9 - 0.25*k*0.8
    print("E3 k", k, "price", round(price, 6), "formula 1.35-0.2k", round(1.35-0.2*k, 6))
# Lab 4 weights: which currency is index 2?
