import math
from math import sqrt, erf
def tail(z):
    return 2.0 * (1.0 - 0.5 * (1.0 + erf(abs(z) / sqrt(2.0))))
# L05 numbers (displayed and full-precision)
SIG=0.08; Q=100; T=120; BETA=-0.0008
sd_exact = SIG*sqrt(2.0/Q)
print('sd_exact', sd_exact, '7dp', round(sd_exact,7), '5dp', round(sd_exact,5))
se_exact = sd_exact/sqrt(T)
print('se_exact', se_exact, '7dp', round(se_exact,7))
gap_disp = -2.7937
print('planted from displayed gap', -BETA*0+(-0.0008)*(-2.7937))
planted_disp = 0.0008*2.7937
print('planted_disp 0.0022350?', round(planted_disp,7), planted_disp)
planted_lab = 0.00223495
print('E2 displayed-SD t (0.0022350/(0.01131/sqrt120))', 0.0022350/(0.01131/sqrt(T)))
print('E2 full-precision t (0.00223495/(0.0113137/sqrt120))', 0.00223495/(0.0113137/sqrt(T)))
print('c123 same quotient w/ displayed SD 0.01131 and planted 0.00223495', 0.00223495/(0.01131/sqrt(T)))
print('exact t with exact sd and planted 0.00223495', 0.00223495/se_exact)
print('exact t with planted 0.0008*2.7937', planted_disp/se_exact)
print('seed0 quotient rounded inputs, SE 0.0010328', (0.00075-0.00223)/0.0010328)
print('seed0 quotient displayed SE 0.00103', (0.00075-0.00223)/0.00103)
print('R1 sqrtT', (1.959964+0.841621)*sd_exact/0.00223495, 'T', ((1.959964+0.841621)*sd_exact/0.00223495)**2)
print('R1 with 0.0113137', (1.96+0.8416)*0.0113137/0.0022350, ((1.96+0.8416)*0.0113137/0.0022350)**2)
print('R1 with 0.00223495 and 0.0113137 approx T', (2.8016*0.0113137/0.00223495)**2)
# L06 numbers
print('--- L06')
print('z_a2 6dp', 0.003076/0.001467, 'tail', tail(0.003076/0.001467))
print('z rounded both', 0.0031/0.0015, tail(0.0031/0.0015))
print('z rounded SE only', 0.003076/0.0015, tail(0.003076/0.0015))
print('z rounded diff only', 0.0031/0.001467, tail(0.0031/0.001467))
print('diff 0.3891-0.1806', 0.3891-0.1806)
print('M3 0.2084/0.2824', 0.2084/0.2824)
print('0.1425+0.1965-0.1306', 0.1425+0.1965-0.1306)
print('tail 2.096', tail(2.096), 'tail 2.097', tail(2.097))
