import sys, math, json
exec(open("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/ledgers/E3/scripts/E3-d-r8/reverse_order.py").read().split("fwd = lambda")[0])
for h in (1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6, 3e-7, 1e-7):
    C = inv3(info(h, lambda p: p))
    print(f"h={h:g} se_lambda={l*math.sqrt(C[1][1]):.3f} se_gamma={g*(1-g)*math.sqrt(C[0][0]):.5f} se_kappa={k*math.sqrt(C[2][2]):.4f}")
