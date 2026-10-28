# Recomputes the L06 Lab 1 quantiles unrounded and the Section 3 differences (run with python -I).
import math, random, statistics, sys
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {}
exec(compile(src, "lab", "exec"), ns)
rng = random.Random(ns["SEED"])
npvs = [ns["npv_of"]([rng.randint(ns["LOW"], ns["HIGH"]) for _ in range(ns["YEARS"])]) for _ in range(ns["N_MAX"])]
ordered = sorted(npvs)
q = {p: ns["quantile"](ordered, p) for p in (0.10, 0.50, 0.90)}
for p, v in q.items():
    print(f"q{p:.2f} unrounded {v:.6f}")
d = q[0.90] - q[0.10]
print(f"diff_unrounded {d:.6f} rounds2 {d:.2f}")
print(f"printed_diff 143406.13-14896.62 = {143406.13-14896.62:.2f}")
print(f"gap printed_diff - unrounded_diff = {(143406.13-14896.62)-d:.4f}")
print(f"unrounded minus printed q10 {q[0.10]-14896.62:+.6f} q90 {q[0.90]-143406.13:+.6f}")
sd = statistics.stdev(npvs)
print(f"sd_all {sd:.6f} se_at_50000 {sd/math.sqrt(50000):.4f} sqrt500 {math.sqrt(500):.4f} ratio_se {4400.22/221.01:.4f}")
print(f"mean_check share_below {sum(1 for x in npvs if x<0)/50000:.6f} se {math.sqrt(0.0552*(1-0.0552)/50000):.6f}")
