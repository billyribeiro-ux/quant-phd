import sys
from decimal import Decimal
# Constants and indices as printed on L08 §3 (course/modules/AC/AC2/L08.html lines 431-437)
c = {"DSRI": (0.920, 1.5), "GMI": (0.528, 1.1429), "AQI": (0.404, 1.0833), "SGI": (0.892, 1.2),
     "DEPI": (0.115, 1.0909), "SGAI": (-0.172, 1.0), "LVGI": (-0.327, 0.9792), "TATA": (4.679, 0.0333)}
intercept = -4.84
M_disp_terms = sum(round(w*x, 4) for w, x in c.values())
M_unrounded = intercept + sum(w*x for w, x in c.values())
print("sum of 4dp terms:", round(M_disp_terms, 4), "+ intercept =", round(intercept + M_disp_terms, 4))
print("M from displayed indices:", round(M_unrounded, 4))
# Lab 1 output E1: medians
print("E1 gap:", round(-1.5067 - (-2.4747), 4))
