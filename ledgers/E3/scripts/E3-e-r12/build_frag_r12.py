"""Round-12 slice e fragment builder. Starts from the round-11 rows (every id kept), applies the round-12 outcomes
recorded in this file, carries prior PASS rows whose cited passage no round-12 hunk touches (stated per row), adds
new rows, and writes ledgers/E3/E3-e.json. Validation is done by tools/ledger.py's validate()."""
import datetime
import json
import sys
from pathlib import Path

CHECK = Path("/Users/billyribeiro/.fanout/wt/verifyD12-E3-e")
sys.path.insert(0, str(CHECK / "tools"))
import ledger  # noqa: E402

prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-e.round11.json", encoding="utf-8"))
rows_prev = {r["id"]: r for r in prev["rows"]}
OUT = {}  # id -> (status, check, location, evidence, fix)

CARRY = "Carried from round 11 (cited passage not touched by any round-12 hunk ccaeeaf4..329c1d7f; file changed elsewhere): "
for rid, r in rows_prev.items():
    if r["status"] == "PASS":
        OUT[rid] = ("PASS", r["check"], r["location"], CARRY + r["evidence"], "")
    else:
        OUT[rid] = (None, r["check"], r["location"], "", "")  # must be re-verified in this round (set below)

def setrow(rid, status, evidence, fix="", check=None, location=None):
    old = OUT.get(rid, (None, "", "", "", ""))
    OUT[rid] = (status, check or old[1] or rid, location or old[2] or "", evidence, fix)

exec(open(CHECK / "ledgers/E3/scripts/E3-e-r12/rows_r12.py", encoding="utf-8").read())

missing = [rid for rid, v in OUT.items() if v[0] is None]
assert not missing, f"rows without a round-12 outcome: {missing}"
rows = []
for rid, (status, check, location, evidence, fix) in OUT.items():
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}
    rows.append(row)
for rid in rows_prev:
    assert any(r["id"] == rid for r in rows), rid
mutants = json.load(open(CHECK / "ledgers/E3/scripts/E3-e-r12/mutants_r12.json", encoding="utf-8"))
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m.get("killed_by") for m in mutants) else "FAIL"
frag = {
    "unit": "E3",
    "slice": "e",
    "round": 12,
    "verifier": "Haiku independent verifier, unit E3 slice e, round 12",
    "pin": "329c1d7f",
    "base": "ccaeeaf4 (round-11 pin); round-11 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round11.json",
    "checkout": str(CHECK),
    "scratch": "/tmp/e3e_r12",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "plans/FINAL-ARCHITECT-RULINGS.md item 7 quotes exemplar word counts 103 and 375; the page has 117 and 450 "
        "(recounted this round with the stated method). The ruling text is stale; the page count is right."
    ],
    "notes": NOTES,
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = (f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
                   f"Mutants: {len(mutants)} listed, {sum(1 for m in mutants if m.get('killed_by'))} killed.")
problems = ledger.validate(frag, "E3-e")
print("validate:", problems)
out = CHECK / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"], "verdict", verdict)
