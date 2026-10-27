"""Round-28 part C: run the 83 distinct killing test ids named in the part-A tooling mutants (killed_by) at c9beb92.
Reads ledgers/S7/data-tooling-A.json (mutants[].killed_by) and runs pytest on the ids. Run: python -I run_killers_C.py <checkout>"""
import json
import re
import subprocess
import sys

CK = sys.argv[1]
d = json.load(open(f"{CK}/ledgers/S7/data-tooling-A.json", encoding="utf-8"))
ids = sorted({m["killed_by"].strip() for m in d["mutants"] if m.get("killed_by")})
print("mutants:", len(d["mutants"]), "distinct killer ids:", len(ids))
r = subprocess.run([f"{CK}/.venv/bin/python", "-m", "pytest", "-q", "-p", "no:cacheprovider", *ids], cwd=CK, capture_output=True, text=True)
tail = [l for l in r.stdout.splitlines() if l.strip()][-1:]
print("pytest exit", r.returncode, tail)
