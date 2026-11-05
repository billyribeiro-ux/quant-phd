"""Check the L07 E3 claim: closed form at eta = 1 against the identity weighting p, on the 1001-point grid; and the 8dp quotient."""
import math
grid = [i / 1000 for i in range(1001)]
closed = lambda p: math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))
gaps = [(abs(p - closed(p)), p) for p in grid]
g, p = max(gaps)
print(f"eta=1 closed-form gap max = {g:.6e} at p = {p}")
print("closed(0.862) =", closed(0.862), " 0.862 - closed =", 0.862 - closed(0.862))
print("8dp quotient 0.28579088/0.39125077 =", 0.28579088 / 0.39125077)
print("eta=1 general formula p^1/(p+(1-p))^1 equals p; closed-form check gap at 0.862 =", abs(0.862 - closed(0.862)))
