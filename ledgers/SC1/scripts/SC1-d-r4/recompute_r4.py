"""Verifier r4: re-derive every prose number in project.html from the unrounded values, with independent code."""
import itertools, math, random, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE4-SC1-d/course/modules/SC/SC1/grader")
import instance as I
import reference as R

inst = I.make_instance(0)
H, a, N, seed = inst["H"], inst["a"], inst["n_paths"], inst["seed"]
print("instance", inst)
tail = math.erfc(a / math.sqrt(2 * H))
print("tail unrounded", repr(tail), "round6", f"{tail:.6f}")
# one step, independent of reference: path-major draws
rng = random.Random(seed)
ind = [1.0 if rng.gauss(0.0, math.sqrt(H)) >= a else 0.0 for _ in range(N)]
hits = sum(ind)
p = hits / N
var = sum((x - p) ** 2 for x in ind) / (N - 1)
se = math.sqrt(var) / math.sqrt(N)
target = tail / 2
tse = math.sqrt(target * (1 - target) / N)
print("one-step hits", hits, "p", repr(p), "sample se", repr(se), f"{se:.6f}")
print("target", repr(target), f"{target:.6f}", "target se", repr(tse), f"{tse:.6f}", "band", f"{5*tse+1/N:.6f}")
print("tail - p", repr(tail - p), f"{tail-p:.6f}", "p - target", repr(p - target), f"{p-target:.6f}")
print("(p-target)/se(sample)", (p - target) / se, " (p-target)/tse", (p - target) / tse)
print("ratio printed 0.016300/0.010735", 0.016300 / 0.010735, " 0.0163/0.0107", 0.0163 / 0.0107)
print("0.001799/0.012870 (grid 64)")
# reference-module check of the same one-step numbers
est, rse = R.discrete_max_exceedance(inst, 1)
print("reference one-step", repr(est), repr(rse), "equal to independent:", est == p, rse == se)
for n in (1, 4, 16, 64, 256):
    e, s = R.discrete_max_exceedance(inst, n)
    print("grid", n, "est", f"{e:.6f}", "se", f"{s:.6f}", "tail-est", f"{tail-e:.6f}", "hits", round(e * N), "tail-est unrounded", repr(tail - e))
    print("   tail-est in SE units", (tail - e) / s)
# nested counts, independent
def path_max_stride(n_fine, strides):
    rng = random.Random(seed)
    sd = math.sqrt(H / n_fine)
    out = {s: [] for s in strides}
    for _ in range(N):
        pos = 0.0
        best = {s: -math.inf for s in strides}
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            for s in strides:
                if k % s == 0 and pos > best[s]:
                    best[s] = pos
        for s in strides:
            out[s].append(best[s])
    return out
nest = path_max_stride(256, (1, 4, 16, 64, 256))
fine = sum(1 for m in nest[1] if m >= a)
print("nested fine", fine, [(c, sum(1 for m in nest[s] if m >= a)) for c, s in ((64, 4), (16, 16), (4, 64), (1, 256))])
# walks
def walk(n, lvl):
    mx = en = 0
    for steps in itertools.product((1, -1), repeat=n):
        sums = list(itertools.accumulate(steps))
        mx += max(sums) >= lvl
        en += sums[-1] >= lvl
    return mx, en
print("walk 12,3", walk(12, 3), "2**12", 2**12)
print("walk 6,2", walk(6, 2), "walk 6,3", walk(6, 3))
# simpson diff
def simpson(level, horizon, intervals=4000):
    top = level + 12 * math.sqrt(horizon); step = (top - level) / intervals
    d = lambda x: math.exp(-x*x/(2*horizon)) / math.sqrt(2*math.pi*horizon)
    tot = d(level) + d(top)
    for k in range(1, intervals):
        tot += (4 if k % 2 else 2) * d(level + k*step)
    return 2 * tot * step / 3
print("simpson diff", f"{abs(simpson(a,H)-tail):.2e}", repr(abs(simpson(a,H)-tail)))
# exemplar-A/B checks
print("erfc(2.474/sqrt(2*2.083))", f"{math.erfc(2.474/math.sqrt(2*2.083)):.6f}", "half tail", f"{tail/2:.4f}")
print("0.0595 - 0.0432 =", round(0.0595-0.0432,4), " 0.059548-0.043248 =", round(0.059548-0.043248,6))
print("1-step sd of target p(1-p)", target*(1-target))
