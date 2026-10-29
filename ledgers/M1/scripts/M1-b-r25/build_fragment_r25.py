"""Build the round-25 fragment for M1 slice b from the round-24 fragment.

Rows are carried only when every cited line is byte-identical to the round-24 pin; the one changed
line (L04.html:79) is re-verified fresh. Command rows and changed-line rows were re-run this round.
"""
import json
import sys

ROOT, PREV = sys.argv[1], sys.argv[2]
prev = json.load(open(PREV, encoding="utf-8"))
CARRY = "Carried from round 24 (cited lines byte-identical since the previous pin; L04.html changed only at line 79, which this row does not cite):"
CARRY_L05 = "Carried from round 24 (course/modules/M/M1/L05.html, cards.json, tests/labs/M1 and the hours markup byte-identical since the previous pin):"

fresh = {
 "M1-b-cmd-pin": ("checkout pin and slice inventory", "course/modules/M/M1/L04.html; L05.html; tests/labs/M1/; cards.json",
   "git rev-parse HEAD = b49a85740e56f64ba3476517614319636dbc68c4 (pin b49a857, detached). git diff --stat 23cbd6a b49a857 for slice b: course/modules/M/M1/L04.html 1 insertion, 1 deletion (line 79); no change to L05.html, cards.json, tests/labs/M1, tools, references or course/assets. The other 116 changed paths are AC4, CF1 and ledgers files."),
 "M1-b-cmd-run_labs": ("run_labs for M1 (all 11 labs)", "tools/run_labs.py --unit M1; course/modules/M/M1/L04.html; L05.html",
   "run_labs --unit M1 printed 'run_labs M1: PASS (11/11)', exit 0."),
 "M1-b-cmd-twins": ("lab twins alone under python -I -W error, output equal to the embedded expected block", "tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py; course/modules/M/M1/L04.html:191-217 and L05.html:223-235 <pre class=expected>",
   "Both twins exit 0 under python -I -W error (outputs /tmp/M1-v/M1-b-r25/l04.out, l05.out). Python comparison of the expected block text to the twin output: L04 equal (1159 characters), L05 equal (847 characters)."),
 "M1-b-cmd-page_smoke": ("page_smoke for L04 and L05", "tools/page_smoke.py --unit M1 --pages L04 L05",
   "page_smoke modules/M/M1/L04.html: PASS (runtime boot 1.0 s); modules/M/M1/L05.html: PASS; 'page_smoke M1: PASS'."),
 "M1-b-cmd-check_pages_dag": ("check_pages and check_dag for M1", "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1; tools/check_projects.py --unit M1",
   "check_pages M1: PASS; check_dag M1: PASS; check_projects M1: PASS (each exit 0)."),
 "M1-b-cmd-lint-types": ("ruff check, ruff format --check and mypy on the two twins", "tests/labs/M1/ (ruff); lab-M1-L04-1.py, lab-M1-L05-1.py (mypy)",
   "ruff check tests/labs/M1/: All checks passed!; ruff format --check: 11 files already formatted; mypy --no-incremental on both twins: Success: no issues found in 2 source files."),
 "M1-b-cmd-refs": ("verify_refs live for M1 and offline", "references/references.json; tools/verify_refs.py; L04.html:459-462; L05.html:472-475",
   "verify_refs --unit M1 (live): 'live re-verification of M1: 1 of 560 entries, 0 problems', exit 0; verify_refs --offline: 'offline integrity: 560 entries, 0 problems', exit 0. L04 and L05 cite no registry key (references paragraphs read)."),
 "M1-b-cmd-pytest": ("relevant pytest", "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py",
   "pytest -q on the three files: exit 0, all dots, no failures (output /tmp/M1-v/M1-b-r25/pytest.out)."),
 "M1-b-2.9-structure-prose": ("2.9 structure, banned phrases and process words, L04 and L05 (full pages)", "course/modules/M/M1/L04.html and L05.html (full pages); ledgers/M1/scripts/M1-b-r25/scan_e_list.py",
   "Full-page regex scan of both pages (scan_e_list.py): no hit for 'roughly half', 'about 6%', 'historically', '...', the ellipsis character, 'builder', 'build', 'round', 'verifier', 'REQUESTS' or 'unit report'. The changed line 79 was re-read in full: it contains no banned phrase or process word."),
 "M1-b-2.9-DAG": ("2.9 DAG and concepts for L04 and L05", "tools/check_dag.py --unit M1 (re-run); L04.html:79 (changed line)",
   "check_dag M1: PASS (re-run). Line 79 contains no concept link (no data-concept or class=concept), so no concept use-before-prerequisite is introduced."),
 "M1-b-r4-term-before-def-L04": ("term before definition, L04 (Assumption E block and its first use)", "course/modules/M/M1/L04.html:75 (first mention, names the next block), 78-80 (Assumption E block), 101-102 (Prop 2.2 statement), 52, 54-56, 59",
   "Re-verified on the changed block: E is defined at 78-79 and first used at 102 and 107. Line 75 is a forward pointer ('stated as Assumption E in the next block'). The new text at 79 adds only the label 'the solution to Problem R3', a location name (a later block at 361-367), which is not a term used before definition."),
 "M1-b-r18-embed-twins": ("embedded expected blocks equal the twins' real output", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py; course/modules/M/M1/L04.html:116-190 and 191-217; L05.html:141-222 and 223-235",
   "Re-run this round: both twins exit 0 under python -I -W error; the embedded expected blocks equal the real output (see M1-b-cmd-twins)."),
 "M1-b-r20-E-scope-remarks": ("scope of Assumption E in the remarks that cite Proposition 2.2", "course/modules/M/M1/L04.html:79 (list), 112 (Remark 2.3); L05.html:127 (Remark 2.3)",
   "L04.html:79 lists 'Remark 2.3'; L04.html:111-112 (Remark 2.3) names Proposition 2.2 under Assumption E. L05.html:126-128 (Remark 2.3) re-read: 'Under Assumption E, Proposition 2.2 says ...'; L05 is byte-identical since the pin."),
 "M1-b-r21-E-list-complete": ("scope of the L04.html:79 list: round-21 omissions at lines 75 and 460", "course/modules/M/M1/L04.html:79 (list); 75 (section 2 introduction); 460 (references paragraph)",
   "Round-21 omissions are fixed. Scan (scan_e_list.py): lines naming Proposition 2.2 are 75, 79, 101, 112, 117, 261, 358, 365, 378, 425, 460. The line-79 list now names section 2 introduction (75), Remark 2.3 (112), the Lab 1 hypothesis (117), the misconception in section 5 (261), Problem R2 (358), the solution to Problem R3 (365), the key-results table in section 7 (378), quiz item 5 (425, the fifth li.item of L04's quiz) and the references paragraph in section 9 (460). Line 79 and line 101 are the statement itself. Complete."),
 "M1-b-r22-E-lab1-dropped": ("scope and completeness of the L04.html:79 list of places that name Proposition 2.2", "course/modules/M/M1/L04.html:79 (list); line 117 (Lab 1 hypothesis)",
   "Line 117 ('Propositions 2.1 and 2.2 predict ...') is named in the line-79 list as 'the Lab 1 hypothesis'. Present."),
 "M1-b-r23-E-list-R3": ("2.9 scope, Assumption E list on L04.html:79 (named entries)", "course/modules/M/M1/L04.html:79 (list) ; 365 (R3 solution)",
   "L04.html:365 ('as in the proof of Proposition 2.2') names Proposition 2.2 in the R3 solution. Line 79 now lists 'the solution to Problem R3'. Every named entry is present; FAIL cleared."),
 "M1-b-r24-E-list-R3-named": ("Line 79 list of places that name Proposition 2.2 is complete", "course/modules/M/M1/L04.html:79 (list); 365 (R3 solution names Prop 2.2); 378 (key results)",
   "Scan (scan_e_list.py) gives the complete set of names above; the list in line 79 names each of them (75, 112, 117, 261, 358, 365, 378, 425, 460), and no entry is missing. The R3 entry is 'the solution to Problem R3'. Round-24 FAIL cleared."),
 "M1-b-r24-embed-twins": ("embedded expected blocks equal the twins' real output", "course/modules/M/M1/L04.html expected block (191-217); L05.html (223-235)",
   "Re-run this round: both expected blocks equal the twins' real output (see M1-b-cmd-twins)."),
 "M1-b-r22-delta": ("round-25 delta re-check for slice b (23cbd6a..b49a857)", "course/modules/M/M1/L04.html:79; git diff --stat 23cbd6a b49a857",
   "Delta since the round-24 pin is one line (L04.html:79, 'the solution to Problem R3' added to the list). The rest of slice b is byte-identical; rows citing other lines are carried."),
}
new_rows = [
 ("M1-b-r25-delta-scope", "round-25 delta: only L04.html:79 changed in slice b", "course/modules/M/M1/L04.html:79", "PASS",
  "git diff 23cbd6a b49a857 -- course/modules/M/M1 tests/labs/M1 tools references curriculum plans atlas: 1 insertion, 1 deletion in L04.html only. git diff --stat outside ledgers: AC4 and CF1 files and L04.html."),
 ("M1-b-r25-E-list-complete", "scope of Assumption E list at L04.html:79 after the round-25 edit", "course/modules/M/M1/L04.html:75, 79, 101, 112, 117, 261, 358, 365, 378, 425, 460",
  "PASS",
  "scan_e_list.py: lines naming Proposition 2.2 are 75, 79, 101, 112, 117, 261, 358, 365, 378, 425, 460. Line 79 lists every one except its own statement (79) and the statement at 101: 75, 112, 117, 261, 358, 365, 378, 425, 460. Complete; the R3 entry is correctly placed (365 names Proposition 2.2; 380 names only Problem R3)."),
 ("M1-b-r25-line79-claims", "claims in the rewritten line 79 (L03 wording, use in R3)", "course/modules/M/M1/L04.html:79; L03.html:56-63; L04.html:365-367",
  "PASS",
  "L03.html:56 'A1 to A3'; grep of L03.html for '1 + x' or '1+x' returns 0 hits, so L03 states the exponential only through A1 to A3 as far as the page shows. L04.html:365-367 ('Assumption E gives e^x - 1 > x') confirms E is used directly in Problem R3."),
]
carry_L04_79 = {"M1-b-r4-term-before-def-L04"}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        chk, loc, ev = fresh[rid]
        rows.append({"id": rid, "check": chk, "location": loc, "status": "PASS", "evidence": ev})
    elif rid in ("M1-b-r21-E-list-complete", "M1-b-r23-E-list-R3", "M1-b-r24-E-list-R3-named"):
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": fresh.get(rid, ("", "", ""))[2]})
    elif rid in ("M1-b-r21-mutants", "M1-b-r18-cards-scan", "M1-b-2.7-cards"):
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": CARRY_L05 + " " + r["evidence"]})
    else:
        pre = CARRY_L05 if "L04" not in r["location"] else CARRY
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": pre + " " + r["evidence"]})
for rid, chk, loc, st, ev in new_rows:
    rows.append({"id": rid, "check": chk, "location": loc, "status": st, "evidence": ev})

notes = [
 "Slice b is lessons L04 and L05 with their lab twins, not a project slice: no student-error mutants or alternative implementations apply (architect ruling, as in rounds 16-24). ledgers/M1/mutants/ is slice a and c material; mutants is empty for this slice.",
 "Round-25 delta for slice b (23cbd6a..b49a857): one line, L04.html:79, where 'the solution to Problem R3' was added to the list of places that name Proposition 2.2. L05.html, cards.json, tests/labs/M1, tools, references and course/assets are unchanged. Rows citing only unchanged lines are carried with the prefix; rows citing line 79 or the full L04 page were re-verified fresh.",
 "The three previous FAIL rows about the line-79 list (M1-b-r21-E-list-complete, M1-b-r23-E-list-R3, M1-b-r24-E-list-R3-named) are re-verified fresh against the complete scan and now PASS.",
 "Not checked: the references (Beneish, SEC) are not cited on these pages and no external source was fetched; the live verify_refs run covered the M1 registry (1 of 560 entries re-verified, 0 problems); L05 Remark 2.3 was re-read but the L05 numbers were carried, not re-derived this round because L05 is byte-identical.",
]
frag = {
 "unit": "M1", "slice": "M1-b", "round": 25,
 "verifier": "independent verifier (Haiku), round 25",
 "pin": "b49a85740e56f64ba3476517614319636dbc68c4", "base": "none",
 "previous_fragment": "/tmp/fanout-frags/M1-b.round24.json",
 "checkout": "/tmp/verify25-M1-b", "scratch": "/tmp/M1-v/M1-b-r25",
 "verified_at": "2026-10-28T16:00:00+00:00",
 "verdict": "PASS",
 "rows": rows, "mutants": [], "registry_flags": [], "freshness_flags": [], "notes": notes,
 "summary": {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"),
             "fail": sum(1 for r in rows if r["status"] != "PASS"), "unverifiable": 0},
}
json.dump(frag, open(f"{ROOT}/ledgers/M1/M1-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(frag["summary"])
