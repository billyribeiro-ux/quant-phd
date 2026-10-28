"""Independent recomputation of every displayed number in CF1 L05 and L06 (slice c, round 8)."""
import math
import random
import statistics

R = 0.10


def pb(flows):
    if flows[0] >= 0:
        return 0.0
    total = float(flows[0])
    for t in range(1, len(flows)):
        prev = total
        total += flows[t]
        if total >= 0:
            return (t - 1) + (-prev) / flows[t]
    return None


def disc(flows, r):
    return [f / (1 + r) ** t for t, f in enumerate(flows)]


def npv(flows, r):
    return math.fsum(disc(flows, r))


A = (-1_000_000, 300_000, 400_000, 400_000, 300_000, 200_000, 100_000)
B = (-1_000_000, 300_000, 400_000, 400_000, 0, 0, 0)
D = (-1_000_000, 500_000, 500_000, 0, 0, 0, 0)
print("A simple", round(pb(A), 3), "disc", round(pb(disc(A, R)), 3), "npv", f"{npv(A, R):.2f}")
print("B simple", round(pb(B), 3), "disc", pb(disc(B, R)), "npv", f"{npv(B, R):.2f}")
print("D simple", round(pb(D), 3), "npv", f"{npv(D, R):.2f}")
gap = npv(A, R) - npv(B, R)
pv46 = 300000 / 1.1**4 + 200000 / 1.1**5 + 100000 / 1.1**6
print("gap", f"{gap:.2f}", "pv_years_4_to_6", f"{pv46:.2f}", "gap/npvA", f"{gap / npv(A, R):.5f}", "pct", f"{100 * gap / npv(A, R):.2f}")
print("A-B check", f"{npv(A, R) + abs(npv(B, R)):.2f}", "|B|", f"{abs(npv(B, R)):.2f}")
print("sec3 flows1", f"{-1000 + 1 / 1.1**4 + 1 / 1.1**5:.4f}", "sec3 flows2", f"{-1000 + 1000 / 1.1**4:.4f}")
print("pb flows1", pb((-1000, 0, 0, 0, 1, 1)), "pb flows2", pb((-1000, 0, 0, 0, 1000, 0)))
print("M1 pb", pb((-1000, 400, 400, 400)))
M2 = (-1000, 400, 400, 400, 400)
M2_no = (-1000, 400, 400, 400)
dM2 = disc(M2, R)
print("M2 terms", [round(400 / 1.1**t, 2) for t in (1, 2, 3, 4)], "sum3 unrounded", f"{sum(400 / 1.1**t for t in (1, 2, 3)):.4f}", "cum3", f"{-1000 + sum(400 / 1.1**t for t in (1, 2, 3)):.4f}", "pb", f"{pb(dM2):.4f}", "pb_no", pb(disc(M2_no, R)))
print("cum after 4", f"{-1000 + sum(400 / 1.1**t for t in (1, 2, 3, 4)):.4f}", "5.26/273.21", f"{5.259/273.205:.5f}")
print("M3 pb", f"{pb((-500, 100, 200, 300)):.6f}")
print("E1 range", f"{693692.91 - 121251.71:.2f}", f"{(693692.91 - 121251.71) / 100:.2f}")
print("E2 1.3323", f"{385535.69 / 289367.40:.5f}", "A-B", f"{289367.40 + 96168.29:.2f}")
print("E3 fine")
# normal reading in E1 of L06
z = 5464.72 / 4400.22
print("L06 E1 z", f"{z:.5f}", "two-sided tail", f"{2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))):.5f}")

# L06 closed forms
LOW, HIGH, INV, RATE, YEARS = 50000, 150000, 300000, 0.10, 5
m = HIGH - LOW + 1
annuity = (1 - (1 + RATE) ** -YEARS) / RATE
exp_npv = -INV + (LOW + HIGH) / 2 * annuity
var_one = (m * m - 1) / 12
sd_exact = math.sqrt(sum(var_one / (1 + RATE) ** (2 * t) for t in range(1, YEARS + 1)))
print("expected", f"{exp_npv:.4f}", "sd_exact", f"{sd_exact:.4f}")
rng = random.Random(6)
npvs = [-INV + math.fsum(x / (1 + RATE) ** (t + 1) for t, x in enumerate([rng.randint(LOW, HIGH) for _ in range(YEARS)])) for _ in range(50000)]
for n in (100, 1000, 10000, 50000):
    s = npvs[:n]
    mean = math.fsum(s) / n
    se = statistics.stdev(s) / math.sqrt(n)
    print("n", n, f"{mean:.4f}", f"{se:.4f}", f"{(mean - exp_npv) / se:+.4f}")
sd_all = statistics.stdev(npvs)
print("sd sample", f"{sd_all:.4f}", f"ratio {sd_all / sd_exact:.5f}")
o = sorted(npvs)
q = lambda p: o[max(1, math.ceil(p * len(o))) - 1]
print("q10", q(0.1), "q50", q(0.5), "q90", q(0.9), "width", f"{q(0.9) - q(0.1):.2f}")
neg = sum(1 for x in npvs if x < 0) / 50000
print("share", neg, "se", f"{math.sqrt(neg * (1 - neg) / 50000):.6f}", "band", f"{neg - 1.96 * 0.0010:.5f}", f"{neg + 1.96 * 0.0010:.5f}")
print("ratio se 100/50000", f"{(statistics.stdev(npvs[:100]) / 10):.4f}/{statistics.stdev(npvs) / math.sqrt(50000):.4f}", f"{(statistics.stdev(npvs[:100]) / 10) / (statistics.stdev(npvs) / math.sqrt(50000)):.4f}")
print("sqrt500", f"{math.sqrt(500):.4f}")
# M2, M3 L06
print("L06 M2 var die", 35 / 12, "sd", math.sqrt(35 / 12))
ann2 = 1 / 1.1 + 1 / 1.21
print("L06 M3", f"{ann2:.6f}", f"{-100 + 50 * ann2:.4f}")
print("L06 E2 band", f"{0.0552 - 1.96 * 0.001:.5f}", f"{0.0552 + 1.96 * 0.001:.5f}")
print("L06 E3 width /100", f"{(143406.13 - 14896.62) / 100:.4f}")
print("L06 remark 3.1 fine")
print("L06 deviation in SEs at 1000", f"{(77963.35 - 79078.68)/1544.09:+.3f}")
