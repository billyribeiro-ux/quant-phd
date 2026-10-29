"""Recover the integer totals behind the L02 printed averages by importing the twin's functions (main() removed)."""
import random
import sys

sys.path.insert(0, sys.argv[1])

import types
src = open(sys.argv[2], encoding="utf-8").read().replace("\nmain()", "\n")
mod = types.ModuleType("l02")
exec(compile(src, sys.argv[2], "exec"), mod.__dict__)
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored_all = set(keys)
absent = [x for x in rng.sample(range(10**9), 2000) if x not in stored_all][:500]
for n in (16, 32, 64, 128, 256):
    t = mod.ChainedHashTable(mod.BUCKETS)
    for k in keys[:n]:
        t.insert(k)
    s = sum(t.lookup(k)[1] for k in keys[:n])
    u = sum(t.lookup(k)[1] for k in absent)
    print(n, "successful_total", s, "unsuccessful_total", u, "longest", max(len(c) for c in t.chains))
