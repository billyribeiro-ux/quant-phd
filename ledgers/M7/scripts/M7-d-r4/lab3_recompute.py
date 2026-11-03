"""Independent exact recomputation of Lab 3's stationarity residuals and of the Lab 1 answer's KKT residuals."""
from fractions import Fraction as F
G = F(2)
S = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]
nu = F(-21, 1100)
lo = [F(0), F(0), F(9, 1100)]
w = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
r = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + nu - lo[i] for i in range(3)]
print("check C stationarity residuals", [str(x) for x in r], "max abs", str(max(abs(x) for x in r)))
w = [F(9, 11), F(2, 11), F(0)]
r = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + nu - lo[i] for i in range(3)]
print("check A stationarity residuals", [str(x) for x in r])
lo2 = [F(0), F(0), -F(9, 1100)]
r = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + nu - lo2[i] for i in range(3)]
print("check B stationarity residuals", [str(x) for x in r], "max abs", str(max(abs(x) for x in r)))
obj = F(1, 2) * G * sum(S[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(MU[i] * w[i] for i in range(3))
print("Lab 1 objective at (9/11, 2/11, 0):", str(obj))
