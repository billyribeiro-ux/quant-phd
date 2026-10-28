"""Verifier round 1 (CS2-b): does the lab's pruned brute_min_hops (tests/labs/CS2/lab-CS2-L06-1.py) ever differ
from an unpruned enumeration of all simple paths? Random graphs with 3 to 8 vertices, every source.
Runtime: about 2 to 4 minutes. Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/prune_search_L06.py
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "check_L06_brute.py"), encoding="utf8").read().split("rng = random.Random(SEED)")[0]
ns = {"__name__": "helpers"}
exec(src, ns)
rng = random.Random(1)
found = 0
tested = 0
for _ in range(200000):
    n = rng.randint(3, 8)
    adj = ns["random_graph"](rng, n, rng.random())
    for s in adj:
        tested += 1
        if ns["pruned_min_hops"](adj, s) != ns["unpruned_min_hops"](adj, s):
            found += 1
            print("witness", n, s, adj)
            break
    if found >= 3:
        break
print("tested sources", tested, "differences found", found)
