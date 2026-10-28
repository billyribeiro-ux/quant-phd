import random, sys, types
src = open("/tmp/verify23-AC1-b/tests/labs/AC1/lab-AC1-L06-1.py").read().replace("\nmain()\n", "\n")
mod = types.ModuleType("L6"); sys.modules["L6"] = mod
exec(compile(src, "lab", "exec"), mod.__dict__)
Lease = mod.Lease; pv = mod.present_value_cents; rf = mod.roll_forward
hits = []
rng = random.Random(1)
for trial in range(20000):
    term = rng.randint(4, 7); pay = rng.randint(120_000_00, 300_000_00); rate = rng.randint(400, 800)
    L = Lease(term, pay, rate)
    years, adj = rf(L, pv(L))
    for t, y in enumerate(years, 1):
        if y.interest + y.amortization == y.payment:
            hits.append((term, pay, rate, t)); break
print("hits in 20000 random leases:", len(hits), hits[:5])
