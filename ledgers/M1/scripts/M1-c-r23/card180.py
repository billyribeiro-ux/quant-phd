from fractions import Fraction as F
C, r, n = F(100), F(1, 10), 3
v = 1 / (1 + r)
ordinary = sum(C * v**t for t in range(1, n + 1))
due = sum(C * v**t for t in range(0, n))
print("ordinary", float(ordinary), "due", float(due), "gap", float(due - ordinary), "gap/ordinary", float((due - ordinary) / ordinary))
print("gap exact", due - ordinary, "== r*ordinary", (due - ordinary) == r * ordinary, "due/ordinary", due / ordinary)
