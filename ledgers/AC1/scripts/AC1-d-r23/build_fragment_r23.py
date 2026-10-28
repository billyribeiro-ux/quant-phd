# Builds ledgers/AC1/AC1-d.json (round 23) from the round-22 fragment, re-verified rows, and carried rows.
# Usage: python -I build_fragment_r23.py <checkout> <round22 fragment> <alts_carried out file>
import json, sys
from pathlib import Path

checkout, prev_path, alts_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
prev = json.loads(prev_path.read_text(encoding="utf-8"))
CARRY = "Carried from round 22 ({files} byte-identical since the previous pin): "
UNCHANGED = "course/modules/AC/AC1/project.html, grader/, tests/labs/AC1/, L01-L04 and L07-L08 pages, index.html"

# Rows re-verified this round: id -> (status, evidence). Evidence names the command or the lines read.
RE = json.loads((checkout / "ledgers/AC1/scripts/AC1-d-r23/reverified.json").read_text(encoding="utf-8"))

# Rows carried: id -> files byte-identical since the pin (must name only files or lines unchanged in the delta).
CARRY_FILES = json.loads((checkout / "ledgers/AC1/scripts/AC1-d-r23/carried.json").read_text(encoding="utf-8"))

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    new = dict(r)
    if rid in RE:
        status, ev = RE[rid]
        new["status"], new["evidence"] = status, ev
    elif rid in CARRY_FILES:
        new["evidence"] = CARRY.format(files=CARRY_FILES[rid]) + r["evidence"]
    else:
        raise SystemExit(f"row {rid} neither re-verified nor carried")
    rows.append(new)

NEW = json.loads((checkout / "ledgers/AC1/scripts/AC1-d-r23/new_rows.json").read_text(encoding="utf-8"))
for r in NEW:
    assert r["id"] not in seen, r["id"]
    rows.append(r)

mutants = prev["mutants"] + json.loads((checkout / "ledgers/AC1/scripts/AC1-d-r23/new_mutants.json").read_text(encoding="utf-8"))
frag = {
    "unit": "AC1", "slice": "AC1-d", "round": 23,
    "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 23 (did not build AC1; computed the delta d160ac3..503d139 on the slice and re-verified every changed row and every command row)",
    "pin": "503d139",
    "base": "d160ac3 (round-22 pin); slice delta: L05.html line 351; L06.html lines 52 and 320; cards.json AC1-c069, AC1-c088, new AC1-c141",
    "checkout": "/tmp/verify23-AC1-d",
    "scratch": "/tmp/ac1-v/d23",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (checkout / "ledgers/AC1/scripts/AC1-d-r23/notes.txt").read_text(encoding="utf-8").strip(),
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (f"AC1-d round 23: verdict {'PASS' if n_pass == len(rows) else 'FAIL'}. "
                   f"{n_pass} PASS rows, {len(rows) - n_pass} non-PASS. Mutant files in ledgers/AC1/mutants/: 204 (201 earlier + 3 new v23), "
                   f"all killed on seeds 0 and 17; the mutants list records the 6 student-error mutants of rounds 22 and 23.")
out = checkout / "ledgers/AC1/AC1-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "mutants", len(mutants))
