import itertools, sys
N, a = 12, 3
cnt_M_S2 = cnt_S4 = cnt_M = cnt_S2 = 0
for steps in itertools.product((1, -1), repeat=N):
    s = 0; m = 0
    for x in steps:
        s += x; m = max(m, s)
    if m >= a: cnt_M += 1
    if m >= a and s == 2: cnt_M_S2 += 1
    if s == 4: cnt_S4 += 1
print("paths", 2**N, "M>=3:", cnt_M, "M>=3&S=2:", cnt_M_S2, "S=4:", cnt_S4)
# Part A-style check for N=6, a=2 (index.html rung-2 claim not here) and P(S12>=3), nu_3 check for c241 is L08 (not slice b)
