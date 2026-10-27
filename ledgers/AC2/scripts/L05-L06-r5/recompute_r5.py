import math
from statistics import NormalDist
N = NormalDist()
T = 120
sigma = 0.08
# L05 E2
sd_theory_unrounded = sigma * math.sqrt(2/100)
print('sd_theory exact', sd_theory_unrounded, 'printed-form 0.08*0.1414 =', round(0.08*0.1414, 6))
planted = -0.0008 * -2.7937
print('planted spread from -2.7937', planted)
print('E2 t with displayed SD 0.01131:', 0.0022350/(0.01131/math.sqrt(T)))
print('E2 t with SD 0.011314 :', 0.0022350/(0.011314/math.sqrt(T)))
print('E2 t with exact SD    :', 0.0022350/(sd_theory_unrounded/math.sqrt(T)))
print('E2 t with exact SD and planted=beta*gap(-2.79962)',  -0.0008*-2.79962/(sd_theory_unrounded/math.sqrt(T)))
print('E2 t with exact SD and planted=beta*gap(-2.7937)',  -0.0008*-2.7937/(sd_theory_unrounded/math.sqrt(T)))
# analytic gap
q = N.inv_cdf(0.2); phi = math.exp(-q*q/2)/math.sqrt(2*math.pi)
gap = -2*phi/0.2
print('analytic gap', gap, 'low-quintile mean', -phi/0.2)
for name, v in [('50',-2.7437),('100',-2.7728),('500',-2.7912),('5000',-2.7991),('200seed',-2.7937)]:
    print('distance', name, round(-2.7996 - v, 4), 'vs analytic exact', round(gap - v, 5))
# E3 L05
print('E3 seed0 distance rounded inputs / exact SE', (0.00075-0.00223)/(sd_theory_unrounded/math.sqrt(T)))
print('E3 seed0 rounded inputs / SE 0.011314/sqrt120', (0.00075-0.00223)/(0.011314/math.sqrt(T)))
print('E3 with displayed SE 0.00103', (0.00075-0.00223)/0.00103)
print('E3 with 0.0010328', (0.00075-0.00223)/0.0010328)
print('SE 0.011314/sqrt120', 0.011314/math.sqrt(T))
print('SE with exact sd/sqrt120', sd_theory_unrounded/math.sqrt(T))
# L06
print('z a2 displayed', 0.003076/0.001467, 'tail 2(1-Phi(2.096))', 2*(1-N.cdf(2.096)), 'tail 2.067', 2*(1-N.cdf(2.067)))
print('z rounded 0.0031/0.0015', 0.0031/0.0015)
print('a1 SE ratio', 0.2824/0.05, 0.2781/0.05)
print('R1 rows', 1800*(0.2781/0.05)**2, 1800*(0.2781/0.05)**2/0.9)
print('sqrt rule', 0.2781*math.sqrt(1800/57600))
print('decomp', 0.1425+0.1965-0.1306, 0.3891-0.1806, 0.2084/0.2824)
print('E3 L06 two-sided tail 2.096', 2*(1-N.cdf(2.096)))
