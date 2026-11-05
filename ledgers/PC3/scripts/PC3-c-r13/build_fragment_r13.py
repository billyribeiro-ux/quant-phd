"""Builds ledgers/PC3/PC3-c.json (round 13) from the round-12 fragment: carried rows (cited subjects byte-identical since
5db69a9b), fresh rows (re-verified this round), and new rows. Writes only the fragment."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-c")
OUT = ROOT / "ledgers/PC3/scripts/PC3-c-r13/out"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round12.json"))
changed = set(subprocess.run(["git", "diff", "--name-only", "5db69a9b", "e919577b"], capture_output=True, text=True,
                             cwd=ROOT).stdout.split())
FRESH = json.load(open(Path(__file__).parent / "fresh_evidence.json"))  # id -> [status, evidence, optional fix]
NEW = json.load(open(Path(__file__).parent / "new_rows.json"))
TOKENS = ["project.html", "test_project", "plans/", "starter", "engine.py", "instance.py", "reference.py", "mutant",
          "alt", "labs", "lab-", "run_", "page", "tools/", "pytest", "mypy", "ruff", "verify", "check_", "collect",
          "L05", "L06", "cards", "grader"]
rows = []
for r in prev["rows"]:
    rid = r["id"]
    text = r["location"] + " " + r["check"]
    if rid in FRESH:
        status, evidence, *rest = FRESH[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = rest[0] if rest else ""
    elif not any(t in text for t in TOKENS) and r["status"] == "PASS":
        cited = sorted(set(re.findall(r"[A-Za-z0-9_./\-]+\.(?:html|py|json|md|yaml|out)", text)))
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": "Carried from round 12 (" + (", ".join(cited) or "cited subject") +
                           " byte-identical since the previous pin 5db69a9b): " + r["evidence"]}
    else:
        raise SystemExit(f"row {rid} has no fresh evidence entry")
    rows.append(row)
rows += NEW
mutants = []
for line in (OUT / "mutate_new_r13_0-49.txt").read_text().splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(2), "description": m.group(3),
                        "killed_by": m.group(4) if m.group(1) == "KILLED" else None})
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "PC3", "slice": "c", "round": 13,
    "verifier": "independent verifier (Haiku 5.5), round 13, slice c; did not build PC3",
    "pin": "e919577", "base": "round 12 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round12.json (pin 5db69a9b). "
    "Delta 5db69a9b..e919577 for slice c: project.html (14 lines), grader/test_project.py (68 lines), plans/PC3-build-plan.md "
    "(2 lines), ledgers/PC3/mutants v47-v49. Not slice c: L05, L06, cards.json. Engine, instance, reference, starter and the "
    "project labs are byte-identical to the round-12 pin.",
    "checkout": str(ROOT), "scratch": "ledgers/PC3/scripts/PC3-c-r13/ (every script and output); /tmp/pc3c-r13* scratch copies",
    "verified_at": "2026-11-05T00:00:00+00:00", "verdict": verdict, "rows": rows, "mutants": mutants,
    "registry_flags": [], "freshness_flags": [],
    "notes": json.load(open(Path(__file__).parent / "notes.json")),
    "summary": f"PC3-c round 13: verdict {verdict}. Rows {len(rows)}: PASS {sum(r['status']=='PASS' for r in rows)}, "
               f"FAIL {sum(r['status']=='FAIL' for r in rows)}, UNVERIFIABLE {sum(r['status']=='UNVERIFIABLE' for r in rows)}. "
               f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed.",
}
dest = ROOT / "ledgers/PC3/PC3-c.json"
dest.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "verdict", verdict)
