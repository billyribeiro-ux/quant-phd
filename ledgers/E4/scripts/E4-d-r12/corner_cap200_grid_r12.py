"""Re-run the round-11 corner grid (linear sd and cost, 300 x 300) with the 200-halving cap to check the logged 11598 count."""
import math
src = open("ledgers/E4/scripts/E4-d-r12/rederive_r12.py").read().split('print("== tau_bar on the box")')[0]
ns = {}
exec(compile(src, "rd_defs", "exec"), ns)
bisect = ns["bisect"]
c_edge = -math.log(1.01 / 2.0) / 4.0
for cap in (200, 240):
    n = over = 0
    worst = (0.0, None)
    for i in range(300):
        sd = 1e-50 * (1 + 0.002 * i)
        for j in range(300):
            c = c_edge - 0.0005 + 0.0005 * j / 299
            t = 2 * math.exp(-4 * c) - 1
            if t < 1e-2:
                continue
            ex = 2.0 * sd * math.sqrt(t / (1.0 - t))
            if ex >= 1.0 or ex <= 0:
                continue
            n += 1
            rel = abs(bisect(sd, c, cap=cap) - ex) / ex
            if rel > 1e-10:
                over += 1
            if rel > worst[0]:
                worst = (rel, (sd, c, ex))
    print(f"cap {cap}: cases {n}, over 1e-10: {over}, max rel {worst[0]:.4e} at {worst[1]}")
