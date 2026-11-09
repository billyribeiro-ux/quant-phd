"""Parse the closing standing-mutant run into fragment mutant entries (read-only check against ledgers/M3/mutants)."""
import json
import os
import re
import sys

ROOT = sys.argv[1]
out_path = sys.argv[2]
lines = open(f"{ROOT}/ledgers/M3/scripts/M3-d-r1/out/closing_mutate_M3_seeds0-9.out", encoding="utf-8").read().splitlines()
pat = re.compile(r"^KILLED (\S+\.py): (.*) -> (.*)$")
killed = {}
for ln in lines:
    m = pat.match(ln)
    if m:
        killed[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
files = sorted(f for f in os.listdir(f"{ROOT}/ledgers/M3/mutants") if f.endswith(".py"))
missing = [f for f in files if f not in killed]
extra = [f for f in killed if f not in files]
print("mutant files:", len(files), "KILLED lines:", len(killed), "files without KILLED line:", missing, "KILLED lines without file:", extra)
entries = []
for f in files:
    if f in killed:
        desc, kb = killed[f]
        entries.append({"id": f[:-3], "description": desc, "killed_by": kb, "file": f"ledgers/M3/mutants/{f}"})
json.dump(entries, open(out_path, "w", encoding="utf-8"), indent=1)
print("entries written:", len(entries))
