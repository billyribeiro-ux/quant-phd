"""Classify collected PC3 tests: nine per-seed checks, seed-only checks, and the three seed-free checks."""
import re, sys, collections
names = [l.strip() for l in open(sys.argv[1]) if "::" in l]
per_seed = collections.Counter()
for n in names:
    base = n.split("::")[1].split("[")[0]
    if "[" in n and re.search(r"\[(\d+)\]$", n) and base in SEED_FUNCS if False else False:
        pass
fn = collections.Counter(n.split("::")[1].split("[")[0] for n in names)
print("distinct functions", len(fn), "tests", len(names))
for k, v in sorted(fn.items()):
    print(f"{v:4d} {k}")
