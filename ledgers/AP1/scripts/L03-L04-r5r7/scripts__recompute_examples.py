"""Round-5 recomputation of the hand-derived (class c) numbers on L03/L04 with exact fractions where possible."""

from fractions import Fraction as F

import numpy as np

# Example 2.3: bond (1,1,1)@0.96, stock (1.4,1.1,0.6)@0.976, fund (2.4,2.1,1.6)@1.95
bond, stock, fund = np.array([1, 1, 1.0]), np.array([1.4, 1.1, 0.6]), np.array([2.4, 2.1, 1.6])
pb, ps, pf = 0.96, 0.976, 1.95
theta = (141, 140, -140)  # bond, stock, fund units
pay = theta[0] * bond + theta[1] * stock + theta[2] * fund
cost = theta[0] * pb + theta[1] * ps + theta[2] * pf
print("Ex2.3 payoff", pay, "today cash flow", -cost, "objective (sum of cash flows)", pay.sum() - cost)
print("Ex2.3 violation cost per (1,1,-1):", pb + ps - pf)

# M1: bond (1,1)@0.95, stock (1.2,0.9)@1.16, theta=(4,-10/3)
pay = 4 * np.array([1, 1.0]) + (-10 / 3) * np.array([1.2, 0.9])
cost = 4 * 0.95 - (10 / 3) * 1.16
print("M1 payoff", pay, "cost", cost, "today cash", -cost, "objective", pay.sum() - cost)

# M2: put on Example 4.3 segment ends; parity 0.976-0.96
print("M2 ends", 0.46 * 0.4, 0.16 * 0.4, "parity", 0.976 - 0.96, "shifted", 0.08 - 0.016, 0.20 - 0.016)
# M3: sum of coordinate upper bounds
print("M3 sum upper", 0.5 + 0.8 + 0.46)
# E3: det and t
X = np.array([[1, 1.4, 0.4], [1, 1.1, 0.1], [1, 0.6, 0]])
print("E3 det", np.linalg.det(X))
# psi(t) = (0.5-0.5t, 0.8t, 0.46-0.3t): check it prices the stock and bond
t = F(1, 2)
psi = [F(1, 2) - F(1, 2) * t, F(4, 5) * t, F(46, 100) - F(3, 10) * t]
print("E3 psi at t=1/2", [float(v) for v in psi], "sum", float(sum(psi)), "stock price", float(psi[0] * F(14, 10) + psi[1] * F(11, 10) + psi[2] * F(6, 10)))
put = psi[2] * F(4, 10)
print("E3 put value", float(put), "check 0.14 - 0.016 =", 0.14 - 0.016)
# R2 lots
print("R2 cash per 100 lots", 100 * 0.014, "fees", 3 * 0.05, "net", 100 * 0.014 - 3 * 0.05, "fees 0.5 per lot ->", 3 * 0.5)

# Example 4.2: pi=(.25,.5,.25); stock (1.4,1.1,.6); bond 1; prices (0.96, 0.976)
pi = np.array([0.25, 0.5, 0.25])
Xm = np.column_stack([np.ones(3), np.array([1.4, 1.1, 0.6])])
p = np.array([0.96, 0.976])
G = Xm.T @ np.diag(pi) @ Xm
b = np.linalg.solve(G, p)
xs = Xm @ b
print("Ex4.2 E[xx']", G.round(6).tolist(), "b", b.round(6), "x*", xs.round(6), "E[x*]", float(pi @ xs), "E[x*^2]", float(pi @ (xs**2)))
psi_tau = lambda tau: (1 - tau) * np.array([0.5, 0, 0.46]) + tau * np.array([0, 0.8, 0.16])  # noqa: E731
print("Ex4.2 pi*x* vs psi(0.587879)", (pi * xs).round(6), psi_tau(0.587879).round(6))

# Example 5.1
pi5 = np.array([0.25, 0.5, 0.25])
z = np.array([3.0, 1.0, -1.0])
m = np.array([1.2, 0.9, 0.8])
print("Ex5.1 E[mz]", float(pi5 @ (m * z)), "E[z^2]", float(pi5 @ (z * z)))
c = float(pi5 @ (m * z)) / float(pi5 @ (z * z))
xs5 = c * z
print("Ex5.1 c", c, "x*", xs5.round(6), "E[x* e3]", float(pi5[2] * xs5[2]))
print("Ex5.1 check E[x* z]", float(pi5 @ (xs5 * z)))

# L04 Problems M1-M3 and E1 ratios, and L03 Example 4.3 portfolio checks
pm = np.array([0.6, 0.4])
m1 = np.array([0.448 / 0.6, 0.522 / 0.4])
x1 = np.array([1.3, 0.8])
print("L04 M1 m", m1.round(6), "E[m]", float(pm @ m1), "Rf", 1 / float(pm @ m1), "E[m x]", float(pm @ (m1 * x1)))
z2 = np.array([2.0, 1.0, 0.0])
c2 = 0.9 / (float(np.mean(z2 * z2)))
print("L04 M2 c", c2, "x*", (c2 * z2).round(6), "E[x*^2]", float(np.mean((c2 * z2) ** 2)))
x3 = np.array([0.824242, 0.940606, 1.134545])
pi3 = np.array([0.25, 0.5, 0.25])
print("L04 M3 E[x* stock]", float(pi3 @ (x3 * np.array([1.4, 1.1, 0.6]))), "E[x*^2]", float(pi3 @ x3**2), "b'p", 1.367273 * 0.96 - 0.387879 * 0.976)
print("L04 E1 ratio", 1.004012 / 1.133251, "eps share", 0.129239 / 1.133251)
print("L03 Ex4.3 upper", 0.5 * 0.976 - 0.3 * 0.96, "payoff", (0.5 * 1.4 - 0.3, 0.5 * 1.1 - 0.3, 0.5 * 0.6 - 0.3))
print("L03 Ex4.3 lower", 0.2 * 0.976 - 0.12 * 0.96, "payoff", (0.2 * 1.4 - 0.12, 0.2 * 1.1 - 0.12, 0.2 * 0.6 - 0.12))
