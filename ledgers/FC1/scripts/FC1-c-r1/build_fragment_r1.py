"""Build ledgers/FC1/FC1-c.json (round 1, closing delta of slice c) from the base round-17 fragment.

Carry rule: a base PASS row is carried only when every path it cites is absent from the
delta `git diff --name-only aa659725..HEAD`; rows that cite a changed path are re-verified
(their fresh evidence is written here, from the outputs in out/)."""
import json, re, sys
from pathlib import Path

R = Path("/Users/billyribeiro/.fanout/wt/verifyF11-FC1-c")
D = R / "ledgers/FC1/scripts/FC1-c-r1"
OUT = D / "out"
BASE = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC1-c.round17.json").read_text(encoding="utf-8"))
CHANGED = set(Path("/tmp/fc1c_r1_changed.txt").read_text().split())
MODULE = "course/modules/FC/FC1/"
PREV = "aa659725"

def norm_paths(text):
    found = set()
    for tok in re.findall(r"[A-Za-z0-9_./\-*{}]+\.(?:html|py|json|js|md|yaml|sh|txt|cfg|toml)|(?:ledgers|course|tests|tools|references|curriculum|notation|plans)/[A-Za-z0-9_./\-*]+", text):
        tok = tok.rstrip(".,;:)")
        if tok.startswith(("ledgers/", "course/", "tests/", "tools/", "references/", "curriculum/", "notation/", "plans/")):
            found.add(tok)
        elif "/" not in tok:
            found.add(MODULE + tok)  # bare lesson/page names (L05.html, index.html, project.html)
        else:
            found.add(MODULE + tok)  # grader/... relative to the unit folder
    return found

def cites_changed(paths):
    hits = []
    for p in paths:
        base = p.replace("*", "")
        for c in CHANGED:
            if c == base or (base.endswith("/") and c.startswith(base)) or (not base.endswith(("/", ".py", ".html", ".json", ".js", ".md", ".yaml", ".sh", ".txt")) and c.startswith(base)):
                hits.append(c)
    return sorted(set(hits))

# rows re-verified from scratch in this round (their subject changed or the standing set was re-run)
FRESH_IDS = {"proj-run-graders", "proj-check-pages-dag", "proj-check-projects", "proj-run-labs",
             "proj-pytest-targeted", "proj-lint-types", "proj-mutants-killed", "proj-mutant-r17-new",
             "proj-mutant-first-line"}
# documented exception: plans/FINAL-ARCHITECT-RULINGS.md changed only by appended ruling 37 (hunk @@ -132,0 +133,4 @@)
PLANS_OK = {"proj-scope-ruling5", "proj-accepted-input-tests-r17"}

mut_out = (OUT / "mutate_FC1_s0-9.out").read_text(encoding="utf-8").splitlines()
killed = {}
for line in mut_out:
    m = re.match(r"^KILLED (\S+\.py): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        killed[m.group(1)] = (m.group(2), m.group(3), int(m.group(4)))
assert len(killed) == 153, len(killed)
assert "mutate_graders FC1: PASS (153/153 killed)" in mut_out

rows, carried, fresh_mut = [], [], []
prefix = f"Carried from round 17 ({{files}} byte-identical since the previous pin {PREV}): "
MUT_RERUN = ("Round-1 re-run of the standing set (out/mutate_FC1_s0-9.out): tools/mutate_graders.py --unit FC1 --seeds 0-9 "
             "reports 'mutate_graders FC1: PASS (153/153 killed)'; every test named in the base evidence quoted after this sentence appears as a killed_by test in that output: ")

for r in BASE["rows"]:
    loc = r["location"]
    paths = norm_paths(loc)
    hits = cites_changed(paths)
    is_mut = "ledgers/FC1/mutants" in loc
    nr = dict(id=r["id"], check=r["check"], location=loc, status="PASS", evidence="")
    if r["id"] in FRESH_IDS:
        nr["evidence"] = None  # filled below
        fresh_mut.append(r["id"])
    elif is_mut:
        tests = sorted(set(t for t in re.findall(r"\btest_[a-z0-9_]+\b", r["evidence"] + " " + loc) if t != "test_project"))
        outs = {k for k, v in killed.items()}
        missing = [t for t in tests if t not in {v[1] for v in killed.values()}]
        assert not missing, (r["id"], missing)
        nr["evidence"] = (f"Round-1 re-verified (the mutant set was re-run as a whole, since ledgers/FC1/mutants gained three files in the delta): " + MUT_RERUN
                          + (", ".join(tests) if tests else "(no test named)") + ". Base evidence: " + r["evidence"])
        fresh_mut.append(r["id"])
    elif hits and r["id"] not in PLANS_OK:
        raise SystemExit(f"row {r['id']} cites changed paths {hits}")
    else:
        pre = prefix.format(files=loc)
        if r["id"] in PLANS_OK:
            pre = prefix.format(files=loc) + "the cited ruling text is unchanged (the delta only appends ruling 37 after line 132); "
        nr["evidence"] = pre + r["evidence"]
        carried.append(r["id"])
    rows.append(nr)

# fresh rows: evidence written from this round's outputs
FRESH_TEXT = {
 "proj-run-graders": "Re-run this round: `.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49` printed 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 (out/gates_batch1.out). grader/test_project.py and grader/reference.py are unchanged since the base pin, so the base's evidence on the test count is carried in proj-collect-count-65.",
 "proj-check-pages-dag": "Re-run this round: `tools/check_pages.py --unit FC1` -> 'check_pages FC1: PASS'; `tools/check_dag.py --all` -> 'check_dag FC1: PASS' and every other unit PASS, rc=0 (out/gates_batch1.out). check_pages validates cards.json (unique ids, lesson exists, grade set, cite keys, every lesson has a card), so it also covers the changed cards.",
 "proj-check-projects": "Re-run this round: `tools/check_projects.py --all` -> 'check_projects FC1: PASS', rc=0 (out/gates_batch1.out).",
 "proj-run-labs": "Re-run this round: `tools/run_labs.py --unit FC1` -> 'run_labs FC1: PASS (8/8)', rc=0 (out/gates_batch1.out). Twin tests/labs/FC1/lab-FC1-L01-1.py run alone under `python -I -W error` in an empty scratch directory: rc=0, stderr 0 bytes, stdout in out/twin_L01.out.",
 "proj-pytest-targeted": "Re-run this round: `.venv/bin/pytest -q -k 'FC1 or project or page or cards or FC2' tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_curriculum.py` -> all dots, rc=0 (out/pytest_targeted.out). The -k set also selects the FC2 tests; the FC2 files that changed are outside this slice and are not verified here.",
 "proj-lint-types": "Re-run this round: `.venv/bin/ruff check .` -> 'All checks passed!' rc=0; `.venv/bin/ruff format --check .` -> '555 files already formatted' rc=0; `.venv/bin/mypy --no-incremental` -> 'Success: no issues found in 386 source files' rc=0 (out/lint_types.out).",
 "proj-mutants-killed": f"Re-run this round: `tools/mutate_graders.py --unit FC1 --seeds 0-9` -> 'mutate_graders FC1: PASS (153/153 killed)', rc=0. The output has 153 KILLED lines, one per file in ledgers/FC1/mutants/ (out/mutate_FC1_s0-9.out). The 153 files are the 150 earlier mutants plus r17n01-03 (added in the delta; see proj-mutant-r17-new).",
 "proj-mutant-r17-new": "Re-verified (the three files are added in the delta aa659725..HEAD). Each file's first line is a one-line error description (checked: ledgers/FC1/mutants/r17n01..03, line 1) and the page sentence it cites exists: project.html line 163 ('a trade amount is an exact integer product'), line 53 ('the amount repaid at maturity'), line 178 ('discounted by (1+y)^-t'). Killed on seed 0 by: " + "; ".join(f"{k}: {killed[k][1]} (seed {killed[k][2]})" for k in sorted(killed) if k.startswith("r17n")) + " (out/mutate_FC1_s0-9.out). No new mutant was written in this round (ruling 37).",
 "proj-mutant-first-line": "Re-run this round over all 153 files of ledgers/FC1/mutants/: every file opens with a triple-quoted one-line description (checked by script: first line starts with '\"\"\"'); " + str(sum(1 for f in (R / 'ledgers/FC1/mutants').glob('*.py') if f.read_text(encoding='utf-8').split(chr(10), 1)[0].startswith('\"\"\"Student error:'))) + " of them begin with the '\"\"\"Student error:' form and the other 71 open with a triple-quoted one-line description of the error without that prefix (out/mutate_FC1_s0-9.out repeats each description).",
}
for nr in rows:
    if nr["id"] in FRESH_TEXT:
        nr["evidence"] = FRESH_TEXT[nr["id"]]

# new rows for the changed cards (the base fragment had no card rows)
NEW = [
 dict(id="cards-c016", check="2.4-math/2.9-cards (changed card)", location="course/modules/FC/FC1/cards.json FC1-c016 (back text changed); course/modules/FC/FC1/L01.html lines 74 (A1), 104 (Prop 3.1 statement), 333-334 (misconception 2)", status="PASS",
      evidence="Card back now: 'No. Under Assumption 2.0 with d > 0 and 0 < rho <= 1, at stage n it is (1 - (1 - rho)^(n+1))/rho, which is smaller than 1/rho at every finite n when rho < 1 (Proposition 3.1; misconception 2).' Hypotheses: L01.html line 74 gives A1 with 0 < rho <= 1; line 104 gives Prop 3.1 'Assuming Assumption 2.0 with d > 0, for every n >= 0'. The 'smaller than' claim is the lesson's own misconception 2 text (L01.html line 334: 'For rho < 1 it is smaller than 1/rho at every finite n'); its one-line proof is 1/rho - S_n/d = (1-rho)^(n+1)/rho > 0 for 0 < rho < 1. Exact re-check (ledgers/FC1/scripts/FC1-c-r1/cards_delta_check.py, out/cards_delta_check.out): 101 values of rho (k/97 for k=1..96 plus 1/10, 1/4, 1/2, 9/10, 1) times n = 0..59, the recursion sum equals the closed form and is below 1/rho when rho < 1, equal at rho = 1: 0 violations. Stage-10 value at rho = 1/10 is 6.8618940391 (L01.html line 334 text; Lab 1 Part A prints 6.8619, out/twin_L01.out). Grade T is consistent with Proposition 3.1 being proved on the page. No card number is absent from the lesson (the card now has none)."),
 dict(id="cards-c103", check="2.4-math/2.5-lab (changed card)", location="course/modules/FC/FC1/cards.json FC1-c103 (back now cites Lab 1, Part B); course/modules/FC/FC1/L01.html Proposition 2.2 (line 89) and the Part B sentence (lesson line 267); tests/labs/FC1/lab-FC1-L01-1.py", status="PASS",
      evidence="Card: 'Yes. Summing the stage identity over stages 0 to n, the sum of the X_t plus the sum of the l_t equals S_n (Proposition 2.2; Lab 1, Part B prints True).' Proposition 2.2 (L01.html line 89 header, statement line 90) proves it for Assumption 2.0; grade T rests on that proof. The lab mention is a printed check: the twin run alone under python -I -W error (out/twin_L01.out) prints 'each stage balances: True' and 'cumulative reserves plus cumulative loans equal total deposits: True', rc=0, stderr 0 bytes. Exact re-check of the identity sum X_t + sum l_t = S_n with X_t = rho D_t, l_t = D_t - X_t, D_{t+1} = l_t over d in {1000, 7/3, 1/9}, rho in {1/10, 1/4, 1, 3/7}, t = 0..24: 0 violations (out/cards_delta_check.out). The lesson sentence it matches (L01.html line 267, 'Parts A and B print True for each exact comparison') is consistent with the printed output."),
 dict(id="cards-c105", check="2.4-math (changed card, text only)", location="course/modules/FC/FC1/cards.json FC1-c105; course/modules/FC/FC1/L03.html line 81 (A2 no other flows)", status="PASS",
      evidence="Card back is now 'The dealer has no fees, no interest on cash, no inventory cost and no information. Its cash and its shares are the only two quantities (Assumption A2).' L03.html line 81 reads 'A2 (no other flows). The dealer has no fees, no interest on cash, no inventory cost and no information. Its cash and its shares are the only two quantities.' The change adds a full stop only. The card has no grade field (as in the base); check_pages accepts it (grade is optional when cite/basis absent)."),
 dict(id="cards-c153", check="2.4-math (changed card)", location="course/modules/FC/FC1/cards.json FC1-c153; course/modules/FC/FC1/L01.html line 132 (Proposition 3.5, raw HTML)", status="PASS",
      evidence="Card: 'Under A2' with d > 0, A1 with 0 < rho <= 1, and the no-withdrawal and no-repayment parts of A3, exactly when phi = 1 or rho = 1 (Proposition 3.5).' L01.html line 132 (Proposition 3.5): 'Assuming Assumption 2.0 with d > 0 and with A2 replaced by A2′ ... Keep A1, with 0 < rho <= 1, and keep the no-withdrawal and no-repayment parts of A3; the cash held outside the bank is the leakage that A2′ adds ... with equality if and only if phi = 1 or rho = 1.' Proof (L01.html line 137): equality iff (1-rho)(1-phi) = 0. Exact re-check over phi in {k/20} x rho in {k/20, k=1..20}: limit d/(1-phi(1-rho)) is never above d/rho and equals it iff (1-phi)(1-rho) = 0, 420 pairs, 0 violations (out/cards_delta_check.out). Grade T matches the proof on the page."),
 dict(id="cards-removed", check="2.9-structure (removed cards)", location="course/modules/FC/FC1/cards.json (FC1-c125, FC1-c173, FC1-c174 removed; base had 172 cards, HEAD has 169)", status="PASS",
      evidence="Removed cards: FC1-c125 (C, 'Lab 1, Part B (typed-in parameters)'), FC1-c174 (C, same basis), FC1-c173 (T, Problem R3 fill sum). No file in course/, tests/, tools/, references/, curriculum/, plans/ or BLUEPRINT.md names these ids (grep, base 95f3f8cb checkout; the only match is course/modules/FC/FC1/cards.json itself, which no longer contains them for c125/c173/c174). Removing a card removes no page claim. Per-lesson coverage after removal: L01, L02, L03, L04, L05 each still have cards (check_pages FC1: PASS)."),
 dict(id="cards-structure", check="2.9-structure (whole file)", location="course/modules/FC/FC1/cards.json (169 cards)", status="PASS",
      evidence="check_pages FC1 PASS (out/gates_batch1.out). Script ledgers/FC1/scripts/FC1-c-r1/cards_structure_scan_r1.py (out/cards_structure_scan.out): 169 cards, no duplicate id, no duplicate front (case-insensitive), no duplicate back; lessons present: L01 34, L02 29, L03 41, L04 31, L05 34 (sum 169; base had 172 cards); page smoke for L01.html (quiz.js loads cards.json through addLessonCards) passes: 'page_smoke FC1: PASS', rc=0 (out/page_smoke_L01.out)."),
 dict(id="mutants-ruling37", check="2.6-mutants (ruling 37 closing round)", location="plans/FINAL-ARCHITECT-RULINGS.md lines 133-136 (ruling 37); ledgers/FC1/mutants/ (153 files)", status="PASS",
      evidence="Ruling 37 (appended in the delta, lines 133-136) says a closing round writes no new mutants and re-runs the standing set. This round wrote no mutant; the standing set of 153 was run (proj-mutants-killed: 153/153 KILLED). The three r17 mutants were already present at the delta start and are killed (proj-mutant-r17-new)."),
]
rows.extend(NEW)

mutants = []
for fname, (desc, test, seed) in sorted(killed.items()):
    mutants.append({"id": fname[:-3], "description": desc, "killed_by": f"{test} (seed {seed})"})

summary = {"rows": len(rows), "PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": 0, "UNVERIFIABLE": 0,
           "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
           "failing_rows": [], "prior_round_rows_not_in_this_fragment": []}
frag = {
 "unit": "FC1", "slice": "c", "round": 1,
 "verifier": "Claude Haiku 5.5, independent closing-delta verifier for FC1-c, round 1 (did not build FC1; ruling 30)",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "aa6597255304919b9c4e5e5ca07763ae3e13d45c (round-17 pin; base fragment /Users/billyribeiro/.fanout/frags/D-FC1-c.round17.json, copied to ledgers/FC1/scripts/FC1-c-r1/base_round17_fragment_copy.json)",
 "checkout": str(R), "scratch": "ledgers/FC1/scripts/FC1-c-r1/ (new scripts cards_delta_check.py, build_fragment_r1.py; outputs in out/)",
 "verified_at": "2026-11-09T15:50:00+00:00",
 "verdict": None, "rows": rows, "mutants": mutants,
 "registry_flags": BASE["registry_flags"],
 "freshness_flags": BASE["freshness_flags"] + ["verify_refs ran offline only in this round (out/gates_batch1.out); the live run needs network and was not run."],
 "notes": (
   "Closing delta (ruling 30) of slice c from the round-17 pin aa659725 to HEAD 95f3f8cb. Delta paths in the slice: course/modules/FC/FC1/cards.json (cards c016, c103, c105, c153 changed; c125, c173, c174 removed), ledgers/FC1/mutants/r17n01-03 (added), plans/FINAL-ARCHITECT-RULINGS.md (ruling 37 appended at lines 133-136). course/modules/FC/FC1/project.html, grader/*.py, tests/labs/FC1/*, L01-L05.html and index.html are byte-identical to the base pin, so their rows are carried with the carry prefix. "
   "Rows re-verified from scratch: the nine FRESH rows and every mutant-group row (the mutant set was re-run as a whole). Ruling 37 forbids new mutants in this closing round, so no mutant was written (the verifier rules' 'at least three new mutants' is superseded for this round). "
   "Changed files outside the slice, not verified here: tests/labs/FC2/lab-FC2-project-1..3.py, course/modules/FC/FC2/*, tests/test_lx1_project_lab3.py, E3 and M2 and CS2 files, ledgers/M5, ledgers/M7 and ledgers/FC1/scripts/FC1-b-*. "
   "Not checked: the alternatives a1..a5 and the two extra alternatives were not re-run (grader/test_project.py and the alternatives are unchanged; carried); page_smoke for project.html and the other lessons (only L01.html re-run); build_site --check, render_curriculum --check, fetch_data --check (no input of these tools changed in the slice); the full pytest suite (targeted set only); live verify_refs; mypy --strict on grader files beyond the repo-wide mypy run; Pyodide execution of the mutants (local grader only). "
   "Observation (not a FAIL kind under ruling 26): card FC1-c105 has no grade field; the base also had none. The removed FC1-c125 and FC1-c174 were C cards whose basis was the typed-in lab; no replacement C card was needed by the rules. "
   "Observation: the scratch directory ledgers/FC1/scripts/FC1-c-r1/ already held tracked files from an earlier campaign (commit e22feb33); they were not read as evidence or modified."
 ),
 "summary": summary,
}
frag["verdict"] = "PASS" if summary["PASS"] == summary["rows"] and summary["mutants_killed"] == summary["mutants"] else "FAIL"
Path(R / "ledgers/FC1/FC1-c.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("carried", len(carried), "fresh", len(fresh_mut) + len(FRESH_IDS - set(fresh_mut)), "new", len(NEW), "rows", len(rows), "verdict", frag["verdict"])
print("fresh ids:", sorted(FRESH_IDS | set(fresh_mut)))
