"""Verifier round 4: seeded L07 facts that the lab prints (first LCS pair, count of impossible coin cases).

Loads the twin's definitions (without its trailing main() call) and recomputes with its generators.
Usage: python3 -I l07_seeded_facts_r4.py <path-to-L07-twin>
"""
import sys

src = open(sys.argv[1], encoding="utf-8").read().rsplit("\nmain()", 1)[0]
ns: dict = {"__name__": "twin"}
exec(compile(src, sys.argv[1], "exec"), ns)
gen = ns["Lcg"](ns["SEED"])
pairs = ns["make_lcs_instances"](gen)
cases = ns["make_coin_instances"](gen)
x, y = pairs[0]
print("first LCS pair:", x, y, "length (table):", ns["lcs_table"](x, y)[0], "length (memo):", ns["lcs_memo"](x, y)[0])
print("LCS pairs:", len(pairs), "coin cases:", len(cases))
print("coin cases with no combination:", sum(1 for d, a in cases if ns["coins_table"](d, a)[0] is None), "of", len(cases))
print("coins (1,3,4) amount 6 greedy:", ns["greedy_count"]((1, 3, 4), 6), "optimum:", ns["coins_table"]((1, 3, 4), 6)[0])
