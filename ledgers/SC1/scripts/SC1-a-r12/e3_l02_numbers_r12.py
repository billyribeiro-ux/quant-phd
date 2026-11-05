"""Re-derives L02 E3 (level-1 sup and bound) and the L02 lab numbers from the seed, independently of the lab twin."""
import math
import random

SEED = 20260101
rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
xi11 = rng.gauss(0.0, 1.0)  # first coefficient drawn after xi0 is the level-1 coefficient, as in the lab
print(f"xi0 (unrounded) = {xi0!r}")
print(f"|xi_11| unrounded = {abs(xi11)!r}")
sup1 = abs(xi11) * 2 ** (-1.0)
print(f"level-1 observed sup = |xi_11| * 2^-1 = {sup1!r}  -> 6dp {sup1:.6f}")
print(f"twice the printed value 0.116589 = {2*0.116589:.7f}")
print(f"twice the unrounded sup = {2*sup1:.7f}  -> 6dp {2*sup1:.6f}")
lam1 = math.sqrt(4 * math.log(2))
print(f"lambda_1 = {lam1:.7f}; lambda_1 * 2^-1 = {lam1*0.5:.7f} -> 6dp {lam1*0.5:.6f}")
