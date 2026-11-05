"""Round-10: assemble ledgers/E3/E3-e.json from the round-10 runs. Rows are written here with the evidence and the
script or output file each one cites; mutants are parsed from the final mutation run. The fragment is validated by
tools/ledger.py before it is written."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-e-r10/"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

mut_out = (ROOT / S / "mutate_E3_seeds0-9_r10_final.out").read_text(encoding="utf-8").splitlines()
mutants, survivors = [], []
for line in mut_out:
    m = re.match(r"(KILLED|SURVIVED) (\S+?\.py): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    if status == "SURVIVED":
        survivors.append(name)
    mutants.append({
        "id": name[:-3],
        "description": desc,
        "file": f"ledgers/E3/mutants/{name}",
        "killed_by": killer if status == "KILLED" else None,
    })
mut_total = len(mutants)
mut_killed = sum(1 for m in mutants if m["killed_by"])
mut_complete = any(line.startswith("mutate_graders E3:") for line in mut_out)
new_mutants = [m for m in mutants if m["id"].startswith("r10e_")]
print("mutants", mut_total, "killed", mut_killed, "survivors", survivors, "complete", mut_complete,
      "new", [(m["id"], m["killed_by"]) for m in new_mutants])
alt_text = (ROOT / S / "run_alternatives_seeds0-9_r10.out").read_text(encoding="utf-8")
print("alternatives bytes", len(alt_text))
print(alt_text[-800:])
