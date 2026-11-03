import sys
sys.path.insert(0, '/tmp/M4-d-r2')
import inst_check_instance as I
bad = []
nus = set(); ns = set(); npos = {}
for s in range(2000):
    inst = I.make_instance(s)
    pos = inst["positions_cents"]
    npos[len(pos)] = npos.get(len(pos), 0) + 1
    if not all(type(w) is int and w > 0 for w in pos):
        bad.append(("nonpositive", s, pos))
    if not all(100000 <= w <= 5000000 for w in pos):
        bad.append(("range", s, pos))
    nus.add(inst["nu"]); ns.add(inst["n_draws"])
    if inst["label"] != "SIMULATED":
        bad.append(("label", s))
print("instances 0..1999; bad:", len(bad), bad[:3])
print("position counts:", npos, "nu set:", sorted(nus), "n_draws set size:", len(ns), "max n_draws:", max(ns))
print("n_draws multiple of 100:", sum(1 for n in ns if n % 100 == 0))
