# Probe L08 lab implied_volatility on prices strictly between the bounds but close to the spot.
import importlib.util, math, sys
spec = importlib.util.spec_from_file_location("labL08", "/tmp/verifyC1-FC2-c/tests/labs/FC2/lab-FC2-L08-1.py")
src = open("/tmp/verifyC1-FC2-c/tests/labs/FC2/lab-FC2-L08-1.py").read().replace("\nmain()", "\n")
ns = {"__name__": "probe"}
exec(compile(src, "lab", "exec"), ns)
bs_call, implied, lb = ns["bs_call"], ns["implied_volatility"], ns["lower_bound"]
for K in (80.0, 100.0, 120.0):
    cHi = bs_call(100.0, K, 0.05, 1.0, 10.0)
    print("K", K, "C(sigma=10)", repr(cHi), "lower bound", lb(100.0, K, 0.05, 1.0))
    # a price strictly between bound and spot but above C(10)
    p = (cHi + 100.0) / 2
    p2 = 100.0 - 1e-9
    for price in (p, p2):
        if not (lb(100.0,K,0.05,1.0) < price < 100.0):
            print("  price not in bounds", price); continue
        try:
            print("  price", repr(price), "->", implied(price, K))
        except ValueError as e:
            print("  price", repr(price), "-> ValueError:", e)
# true implied vol for a price just under spot, computed by a bracket that contains the root
def bs_rootable(price, K):
    lo, hi = 1e-6, 1.0
    while bs_call(100.0,K,0.05,1.0,hi) < price: hi *= 2
    for _ in range(200):
        m=(lo+hi)/2
        if bs_call(100.0,K,0.05,1.0,m) < price: lo=m
        else: hi=m
    return (lo+hi)/2
print("K=80 price 99.9999 true sigma (bracket expanded)", bs_rootable(99.9999, 80.0))
print("lab on 99.9999 K=80:", end=" ")
try: print(implied(99.9999, 80.0))
except ValueError as e: print("ValueError:", e)
