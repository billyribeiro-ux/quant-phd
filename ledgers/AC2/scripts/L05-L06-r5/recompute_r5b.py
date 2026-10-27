import math
from statistics import NormalDist
N = NormalDist()
b, se = 0.003076, 0.001467  # b here is the difference from 0.10 (0.103076 - 0.10)
# exact (unrounded) difference is 0.0030760..., SE 0.001467...
print('z unrounded inputs (printed)', round(b/se, 4))
print('z rounded b only (0.0031, SE 0.001467)', round(0.0031/se, 4), 'tail', round(2*(1-N.cdf(0.0031/se)), 4))
print('z rounded SE only (b 0.003076, SE 0.0015)', round(b/0.0015, 4), 'tail', round(2*(1-N.cdf(b/0.0015)), 4))
print('z both rounded (0.0031, 0.0015)', round(0.0031/0.0015, 4), 'tail', round(2*(1-N.cdf(0.0031/0.0015)), 4))
print('tail at 2.096', round(2*(1-N.cdf(2.096)), 4), ' at 2.067', round(2*(1-N.cdf(2.067)), 4))
# L05 unrounded SD label check
sd_exact = 0.08*math.sqrt(2/100)
print('exact SD', sd_exact, 'rounded to 6 dp', round(sd_exact, 6), 'label 0.011314 is rounded by', round(0.011314 - sd_exact, 9))
print('E2 t exact SD', 0.0022350/(sd_exact/math.sqrt(120)), ' with 0.011314', 0.0022350/(0.011314/math.sqrt(120)))
print('E3 SE exact', sd_exact/math.sqrt(120), ' with 0.011314', 0.011314/math.sqrt(120))
