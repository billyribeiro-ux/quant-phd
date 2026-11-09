"""Reads the round-15 verifier run outputs and prints the facts the fragment cites. Usage: summarize_runs.py <verifier-dir>."""
import json
import re
import sys
from collections import defaultdict

D = sys.argv[1]
out = {}

# alternatives: alt_vN seed=S EXIT=E ... passed/failed
alts = defaultdict(dict)
for line in open(f"{D}/alternatives_seeds_0-9.raw", encoding="utf-8"):
    m = re.match(r"alt_v(\d) seed=(\d+) EXIT=(\d)\s+(.*)", line)
    if m:
        alts[int(m.group(1))][int(m.group(2))] = (int(m.group(3)), m.group(4).strip()[:60])
out["alternatives"] = {f"alt_v{k}": {"seeds_run": sorted(v), "all_pass": all(e == 0 for e, _ in v.values()), "n_pass": sum(e == 0 for e, _ in v.values())} for k, v in sorted(alts.items())}

# equivalents
eq = defaultdict(dict)
for line in open(f"{D}/equivalent_seeds_0-9.raw", encoding="utf-8"):
    m = re.match(r"(\S+) ledgers/E3/equivalent/\S+ seed=(\d+) EXIT=(\d)", line) or re.match(r"ledgers/E3/equivalent/(\S+) seed=(\d+) EXIT=(\d)", line)
    if m:
        eq[m.group(1)][int(m.group(2))] = int(m.group(3))
out["equivalent_all_pass"] = {k: (len(v), all(e == 0 for e in v.values())) for k, v in sorted(eq.items())}

# new verifier mutants
nm = defaultdict(dict)
for line in open(f"{D}/new_mutants_seeds_0-9.raw", encoding="utf-8"):
    m = re.match(r"ledgers/E3/mutants/(\S+) seed=(\d+) EXIT=(\d)\s+(.*)", line)
    if m:
        nm[m.group(1)][int(m.group(2))] = (int(m.group(3)), m.group(4))
out["new_mutants"] = {k: {"seeds": len(v), "killed_seeds": sum(e != 0 for e, _ in v.values()), "first_failing": next((t for e, t in v.values() if e != 0), None)} for k, v in sorted(nm.items())}
print(json.dumps(out, indent=1)[:6000])
