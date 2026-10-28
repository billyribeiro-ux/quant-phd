import sys
sys.path.insert(0, '/tmp/M5-v/d3/alt/w_altR3b')
import reference_r3 as ref
p = {"beta": 0.5, "alpha": 0.5}; grid = [0.75, 1.0]; b = 0.5
V0 = [0.0, 0.0]
V1 = ref._sweep(0.5, 0.5, grid, V0)
V2 = ref._sweep(0.5, 0.5, grid, V1)
d12 = max(abs(x - y) for x, y in zip(V2, V1))
print("V1", V1, "V2", V2)
print("residual-after-sweep certificate at n=1: ||B V1 - V1||/(1-beta) =", d12 / (1 - b), " (formula certificate = 0.5)")
# a valid solver using the residual certificate with value V_1:
cert1 = d12 / (1 - b)
print("tol = nextafter(0.5,0) =", repr(__import__('math').nextafter(0.5, 0.0)), " stops at sweep 1?", cert1 <= __import__('math').nextafter(0.5, 0.0))
# validity: true distance to fixed point V* (reference, 1e-12)
v = [0.0, 0.0]
for _ in range(10000):
    nxt = ref._sweep(0.5, 0.5, grid, v); v = nxt
Vstar = v
print("true ||V1 - V*|| =", max(abs(a - c) for a, c in zip(V1, Vstar)), " <= cert1?", max(abs(a - c) for a, c in zip(V1, Vstar)) <= cert1)
