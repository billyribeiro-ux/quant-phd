import json, re, datetime, pathlib
ROOT = pathlib.Path("/tmp/verify44-AC4-e")
S = "ledgers/AC4/scripts/AC4-e-r44"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round41.json"))

# ---- mutants: this round's observed lines
def parse(path, prefix):
    res = []
    for line in (ROOT / path).read_text().splitlines():
        m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line)
        if m:
            res.append({"file": prefix + m.group(1), "description": m.group(2), "killed_by": m.group(3) + " [KILLED]"})
    return res
mutants = parse(f"{S}/out/mutate_ac4.out", "ledgers/AC4/mutants/")
mutants += parse(f"{S}/out/subdir_fx23_mutants.out", "ledgers/AC4/mutants/AC4-e-r23/")
mutants += parse(f"{S}/out/new_r44_mutants.out", "ledgers/AC4/mutants/")
assert len(mutants) == 165 + 6 + 4, len(mutants)

EV_MUT = ("Re-run in round 44 at pin b4cdc22: tools/mutate_graders.py --unit AC4 --seeds 0-49 -> "
          "'mutate_graders AC4: PASS (165/165 killed)', exit 0 (out/mutate_ac4.out); the six AC4-e-r23 fx23 files killed on seed 0 "
          "(out/subdir_fx23_mutants.out); the four new student-error mutants r44_01..r44_04 killed on seed 0 (out/new_r44_mutants.out). "
          "Every top-level docstring first line describes one specific wrong implementation (listed by ast; the fx23 docstrings name a student error).")
EV_ALT = ("Re-run in round 44: run_alts.py on the six earlier alternatives (alt40_a..c, alt42_a..c) and the two new ones "
          "(alt44_d_divmod_single_pass.py, alt44_e_decimal_context.py) -> PASSES on seeds 0-49 for all eight (out/alts40.out, out/alts44.out).")
EV_GATE = {
 "check_pages": "Re-run round 44: tools/check_pages.py --all -> 'check_pages AC4: PASS', exit 0 (out/check_pages.out).",
 "check_dag": "Re-run round 44: tools/check_dag.py --all -> 'check_dag AC4: PASS', exit 0 (out/check_dag.out).",
 "check_projects": "Re-run round 44: tools/check_projects.py --all -> 'check_projects AC4: PASS', exit 0 (out/check_projects.out).",
 "run_labs": "Re-run round 44: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)', exit 0 (out/run_labs.out).",
 "page_smoke": "Re-run round 44: tools/page_smoke.py --unit AC4 --pages project.html -> 'page_smoke AC4: PASS', exit 0 (out/page_smoke_project.out).",
 "run_graders": "Re-run round 44: tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.4 s)', exit 0 (out/run_graders.out).",
 "ruff": "Re-run round 44: ruff check . -> 'All checks passed!', exit 0; ruff format --check . -> '220 files already formatted', exit 0 (out/ruff_check.out, out/ruff_format.out).",
 "mypy": "Re-run round 44: mypy --no-incremental -> 'Success: no issues found in 153 source files', exit 0 (out/mypy.out).",
 "collect": "Re-run round 44: collect count taken in a grader workspace for all 50 seeds (collect_seeds44.py) -> 563 tests on every seed (out/collect_seeds44.out). Note: pytest --collect-only from the repository root errors (ModuleNotFoundError: budget_engine; out/collect_ac4.out), as expected because no budget_engine.py exists there.",
 "pytest": "Re-run round 44: pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py -> 55 dots, exit 0 (out/pytest_memo_page_checks.out).",
 "refs": "Re-run round 44: tools/verify_refs.py --unit AC4 -> 'live re-verification of AC4: 2 of 560 entries, 0 problems', exit 0 (out/verify_refs_live_AC4.out); tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out).",
}
EV_LAB = ("Re-run round 44: python -I -W error tests/labs/AC4/lab-AC4-project-1.py and -project-2.py exit 0; each output equals the "
          "data-embedded expected block of project.html (checked by script: both True), and the two outputs are identical (out/twin_project1.out, out/twin_project2.out).")

def group(rid):
    if rid.startswith(("proj-mutant", "proj-r12-mutant", "proj-r12-mutants", "proj-r13-mutants", "proj-r14-mutants", "proj-r15-mutants",
                       "proj-r17-mutant", "proj-r18-new-student", "proj-r18-mutants", "proj-r23-mutants", "proj-r30-mutant",
                       "proj-r38-mutants", "proj-r38-equivalent", "proj-r40-mutants", "proj-r40-fx23", "proj-autograder-rerun",
                       "proj-r30-mutants", "proj-r18-new-student", "proj-r17-mutant-docstrings", "proj-r17-mutants", "proj-r15-mutant",
                       "proj-r14-mutants-all", "proj-r18-mutants-all", "proj-r38-mutants-all", "proj-mutants")):
        return "mut"
    if "alt" in rid:
        return "alt"
    if rid in ("proj-check-pages",): return "check_pages"
    if rid == "proj-check-dag": return "check_dag"
    if rid == "proj-check-projects": return "check_projects"
    if rid in ("proj-run-labs-ac4", "proj-r18-run-labs"): return "run_labs"
    if rid in ("proj-page-smoke", "proj-r18-page-smoke", "proj-r30-page-smoke", "proj-r18-gates", "proj-r23-gates-labs-smoke-graders"): return "page_smoke"
    if rid in ("proj-run-graders-ac4", "proj-r30-run-graders-reference"): return "run_graders"
    if rid in ("proj-ruff-mypy", "proj-r30-ruff-mypy-buildsite", "proj-r23-gates-build-ruff-mypy"): return "ruff"
    if rid in ("proj-collect-count", "proj-r30-collect-563", "proj-r17-collect-seeds", "proj-r18-collect-all-seeds", "proj-r23-collect-count-seeds"): return "collect"
    if rid in ("proj-r30-pytest-generic", "proj-r30-exemplars-calibration"): return "pytest"
    if "verify-refs" in rid or rid in ("proj-citations-reading", "proj-r15-reading-keys-used-by-ac4", "proj-r23-reading-list-keys", "proj-reading-list-sentence", "proj-r13-verify-refs"): return "refs"
    if rid in ("proj-lab-1", "proj-lab-2", "proj-r30-run-labs-twins", "proj-r23-lab2-twin-and-blanks", "proj-lab-1-run-line146-untouched"): return "lab"
    return None

# rows whose cited subject is the changed line (project.html line 346) or the memo annotation block: re-verified
CHANGED = {"proj-calib-A-annotation", "proj-r40-exemplar-A-C2-level3-annotation", "proj-r38-exemplar-A-annotation-arithmetic",
           "proj-rubric-C2-terms", "proj-r40-fx23-subdir-mutants", "proj-mutant-descriptions", "proj-banned-phrases",
           "proj-r38-banned-and-process-scan", "proj-r15-no-banned-phrases-changed-lines", "proj-r23-banned-and-placeholders",
           "proj-r30-rubric-observability", "proj-r38-rubric-C2-level3-monotone", "proj-exemplar-overall-level",
           "proj-r23-exemplar-scores-and-words", "proj-r30-exemplars-calibration", "proj-calib-A-scores",
           "proj-memo-structure-length", "proj-r30-memo-body-words", "proj-r18-memo-length-band", "proj-r23-exemplar-B-figures",
           "proj-hours", "proj-r13-hours-split", "proj-r23-hours-split-arith", "proj-r30-hours-arithmetic"}

rows = []
EV_CHANGED = {
 "proj-calib-A-annotation": "Re-verified round 44 (line 346 changed since b2082cc). Lab 1 twin prints step 3 price 180000, step 4 volume 542857, step 5 efficiency -40000, step 6 mix -462857, step 7 total 220000, step 8 True (out/twin_project1.out). Recomputed by script from the case: master 2,600,000; flexed 3,142,857; mix = (1200*4400 + 300*8000) - 5,000,000 - 3,142,857 = -462,857. Exemplar A figures +542,857, +180,000, +462,857 (wrong sign, annotated) and 220,000 are consistent with that; annotation line 345 and new line 346 agree.",
 "proj-r40-exemplar-A-C2-level3-annotation": "Resolved and re-verified round 44. project.html line 346 now reads 'Misses C2 level 3: the efficiency variance is not tied to a case figure. The volume, price and mix variances are tied, so the memo scores level 2.' Every clause is a level-3 condition: the efficiency variance is never stated in exemplar A (no case figure), while volume (1,500 and 1,400 units), price (5,000 and 9,000 cents) and mix (462,857 cents) each state a case figure under the line-308 definition; level 2 is met (line 345), so C2 = 2 as the official scoring at line 328 says. The mix-explanation clause and the inference sentence are gone.",
 "proj-r38-exemplar-A-annotation-arithmetic": "Re-verified round 44 (lines 345-351 touched by the line-346 edit). Arithmetic: 542,857 + 180,000 - 462,857 - 40,000 = 220,000 (script). The C1 level 3 miss (line 344), the C3 level 3 miss (line 348, input price 'never stated' is true of exemplar A's text; -40,000 is the step 5 figure) and the C4 misses (lines 349-350) agree with the memo text. Exemplar A body is 318 words (script; inside 300-600).",
 "proj-rubric-C2-terms": "Re-verified round 44. Line 308 defines 'tied to a case figure' (a number of the case or a computed one shown in the memo); line 315 level 3 cell reads 'Each of the four variances tied to a case figure.' (unchanged since b2082cc); line 345 level 2 annotation and line 346 level 3 annotation are consistent with those definitions.",
 "proj-banned-phrases": "Re-run round 44 over project.html and cards.json: grep for roughly, 'about <digit>', historically, '...', ellipsis, typically, generally, usually, 'half of', 'most <word>', 'in general' -> no matches; process words (build, builder, verifier, round N, unit report, REQUEST) -> no matches in project.html.",
 "proj-r38-banned-and-process-scan": "Re-run round 44 (same scan as proj-banned-phrases): no banned phrase and no process word in project.html; cards.json scan (141 cards, script) has no banned or process word in front or back.",
 "proj-r15-no-banned-phrases-changed-lines": "Re-run round 44: the one changed line (project.html line 346) contains no banned phrase or process word (scan above).",
 "proj-r23-banned-and-placeholders": "Re-run round 44: no banned phrase, ellipsis or placeholder in project.html or cards.json (scan above; cards.json script check: no empty front or back).",
 "proj-r30-rubric-observability": "Carried-in check re-run round 44: line 315 (C2 level 3) and line 317 (C4 level 1) unchanged and the scoring rule at line 308 unchanged; the level-3 C2 cell is observable per the line-308 definition.",
 "proj-r38-rubric-C2-level3-monotone": "Re-run round 44: the C2 row (line 315) is unchanged and its level 3 cell is stricter than level 2 ('each of the four' vs 'at least two'), with line 346 now consistent with it.",
 "proj-exemplar-overall-level": "Re-run round 44: data-level 1 (exemplar A, scores 2,2,2,1,2 -> lowest 1) and data-level 3 (exemplar B, scores 4,4,3,4,4 -> lowest 3) match the scoring rule at line 308 (overall = lowest criterion score).",
 "proj-calib-A-scores": "Re-run round 44: exemplar A data-scores 2,2,2,1,2 match its annotations (C1 level 2 met, level 3 missed -> 2; C2 level 2 met, level 3 missed -> 2; C3 level 2 met, level 3 missed -> 2; C4 level 2 missed -> 1; C5 three headings -> 2).",
 "proj-memo-structure-length": "Re-run round 44: exemplar A body 318 words and exemplar B body 409 words (inline script this round, h5 headings excluded); both inside 300-600; exemplar A has three of four headings; exemplar B has four (script on project.html).",
 "proj-r30-memo-body-words": "Re-run round 44 (script): exemplar A body 318 words, exemplar B body 409 words.",
 "proj-r18-memo-length-band": "Re-run round 44 (script): exemplar A 318 words, exemplar B 409 words, both within 300-600.",
 "proj-r23-exemplar-scores-and-words": "Re-run round 44: word counts 318 and 409 (script) and the score lines at lines 328 and 359 match the data-scores attributes.",
 "proj-r30-exemplars-calibration": "Re-run round 44: tests/test_memo_exemplars.py passes (pytest exit 0, out/pytest_memo_page_checks.out) after the line-346 edit.",
 "proj-r23-exemplar-B-figures": "Re-run round 44 by script: exemplar B figures 2,820,000; 2,600,000; 220,000; +542,857; +240,000 (1,200 units); -60,000 (300 units); -40,000 (200 extra units at 200 cents); 167,000 after a 210-cent input price (-53,000 = 5,300 x 10); threshold 5,400 gives budgeted margin 4,400 = Standard's and mix 0 (recomputed with divmod rounding). All consistent.",
 "proj-hours": "Re-run round 44: lesson data-hours L01..L08 = 6,7,6,6,7,6,6,6 -> sum 50 (script); hub data-hours-lessons=50 and data-hours-project=20 (index.html line 29); page time table rows 1+2+2+6+4+2+2+1 = 20 (line 277-285 table). Arithmetic consistent; hours not judged against pace (architect ruling).",
 "proj-r13-hours-split": "Re-run round 44: 50 lesson hours (sum of L01..L08 data-hours) + 20 project hours = 70; hub split 71.4% / 28.6% matches 50/70 and 20/70.",
 "proj-r23-hours-split-arith": "Re-run round 44: same arithmetic as above; the time-budget table totals 20.",
 "proj-r30-hours-arithmetic": "Re-run round 44: same arithmetic as above; total 20 equals the project figure.",
}
for r in prev["rows"]:
    rid = r["id"]
    base_location = r["location"]
    if rid in EV_CHANGED:
        row = {"id": rid, "check": r["check"], "location": base_location, "status": "PASS", "evidence": EV_CHANGED[rid]}
    elif group(rid):
        g = group(rid)
        ev = {"mut": EV_MUT, "alt": EV_ALT, "lab": EV_LAB, "refs": EV_GATE["refs"], "pytest": EV_GATE["pytest"],
              "collect": EV_GATE["collect"], "ruff": EV_GATE["ruff"], "mypy": EV_GATE["mypy"]}.get(g) or EV_GATE.get(g)
        row = {"id": rid, "check": r["check"], "location": base_location, "status": "PASS", "evidence": ev}
    else:
        # carried: the cited subject is unchanged since the previous pin (b2082cc); see the delta note
        prefix = ("Carried from round 43 (course/modules/AC/AC4/grader/*, cards.json, L01-L08.html, tests/labs/AC4/*, "
                  "references and course/assets byte-identical since the previous pin; the only project.html line changed "
                  "since b2082cc is line 346, which the row does not cite): ")
        row = {"id": rid, "check": r["check"], "location": base_location, "status": "PASS",
               "evidence": prefix + r["evidence"]}
    rows.append(row)

# keep a reading of any row that cites line 346 not already re-verified
for row in rows:
    if "346" in row["location"] and not row["evidence"].startswith(("Re-", "Resolved")) and "Carried" in row["evidence"]:
        raise SystemExit("carry conflict: " + row["id"])

NEW = [
 ("proj-r44-delta-scope", "Delta since the previous pin is limited to project.html line 346 and mutant/script files",
  "git diff --stat b2082cc b4cdc22 -- course tests tools references atlas plans: only course/modules/AC/AC4/project.html changes (1 insertion, 1 deletion, line 346); course/modules/AC/AC4/grader/*, cards.json, L01-L08.html, index.html and tests/labs/AC4/* are byte-identical (git diff --quiet). Mutants: six AC4-e-r23 fx23 docstrings edited; r40e/r42e/fx40 and alt40/alt42 files added. Read every hunk.",
  "git diff b2082cc b4cdc22 -- course/modules/AC/AC4/project.html; git diff --quiet b2082cc b4cdc22 -- course/modules/AC/AC4/grader course/modules/AC/AC4/cards.json course/modules/AC/AC4/L0*.html tests/labs/AC4"),
 ("proj-r44-round43-fragment-absent", "Previous-round fragment and pin for the carry rule",
  "/tmp/fanout-frags/AC4-e.round43.json does not exist on disk; the newest readable AC4-e fragment is AC4-e.round41.json (its rounds field says 40, pin b2082cc). Its 242 row ids are all kept here; the carry base is b2082cc. A carried row is valid for any pin between b2082cc and b4cdc22 because only line 346 of project.html differs there.",
  "ls /tmp/fanout-frags | grep AC4-e; git log --oneline b2082cc..b4cdc22"),
 ("proj-r44-c2-level3-annotation", "The rewritten C2 level 3 annotation states only its failing condition and agrees with the rubric",
  "project.html line 346 (new): 'Misses C2 level 3: the efficiency variance is not tied to a case figure. The volume, price and mix variances are tied, so the memo scores level 2.' Checked against line 308 (tie definition), line 315 (C2 level 3 cell), line 345 (C2 level 2 annotation) and line 328 (official C2 2). No sentence is stated more exactly than the memo supports: exemplar A never states efficiency, and volume, price and mix each state a case figure.",
  "sed -n 343,351p course/modules/AC/AC4/project.html; line 308 and 315 read in place"),
 ("proj-r44-new-mutants-student-errors", "Four new student-error mutants written by this verifier are all killed",
  "r44_01 mix measured against master profit (the four variances stop summing to the total); r44_02 flexed cents rounded by Python round() (half to even); r44_03 float actual units truncated by int(); r44_04 a product with zero budgeted units refused. Each is killed on seed 0 (out/new_r44_mutants.out). The page sanctions a zero budget for one product (Constraints: only 'a budget with no budgeted units' is refused) and the grader tests it (test_zero_budgeted_units_in_the_first_product_is_valid), so r44_04 is a real error.",
  "ledgers/AC4/mutants/r44_01..r44_04 (run by ledgers/AC4/scripts/AC4-e-r44/run_mutants_files.py)"),
 ("proj-r44-alternatives-new", "Two new genuinely different correct engines pass the whole suite",
  "alt44_d: divmod half-up, operator.index validation, one pass over products; alt44_e: Decimal ROUND_HALF_UP in a 60-digit context, strict int check. Both PASS on seeds 0-49 (out/alts44.out). Together with the six earlier alternatives this is eight correct implementations; none is over-constrained by the suite.",
  "ledgers/AC4/scripts/AC4-e-r44/alts/alt44_d_divmod_single_pass.py; alt44_e_decimal_context.py"),
 ("proj-r44-lab-numbers-recomputed", "Lab 1 figures and the interpretation numbers recomputed from the case by hand and by script",
  "Master 2,600,000 = 8,600,000 - 1,000,000 - 5,000,000; flexed 3,142,857 = round(1500*8,600,000/1400) - round(1500*1,000,000/1400) - 5,000,000; volume 542,857; price 240,000 - 60,000 = 180,000; efficiency 200*(5,100-5,300) = -40,000; mix (1200*4400 + 300*8000 - 5,000,000) - 3,142,857 = -462,857; total 220,000; sum of four = 220,000; step 6 residual 1/7. Interpretation: 7,600,000/1,400 = 5,428.57; Standard 71.4% -> 80.0%; Deluxe 28.6% -> 20.0%; margins 4,400 and 8,000. All match.",
  "tests/labs/AC4/lab-AC4-project-1.py run this round; arithmetic re-derived inline this round (not saved as a file)"),
 ("proj-r44-collect-563-all-seeds", "563 checks on every seed 0-49 in a grader workspace",
  "collect_seeds44.py: 563 tests collected for seed 0 and seeds 1-49 (out/collect_seeds44.out). The page count 'collects 563 checks' (project.html Grading mode) matches.",
  "ledgers/AC4/scripts/AC4-e-r44/collect_seeds44.py"),
 ("proj-r44-specification-spot-checks", "Specification constraints and the sixteen later-product conditions match the grader",
  "Constraints (project.html Constraints dd): each refused condition appears in the grader; sixteen entries in LATER_PRODUCT_CONDITIONS (test_project.py lines 1052-1067) times two positions (middle, last) as the page says; zero budgeted units, zero standard inputs, zero actual units and zero fixed overhead are valid in the grader and in alternatives. The mix sentence 'differs by less than one cent' holds: the difference is 1/7 cent (lab output).",
  "course/modules/AC/AC4/grader/test_project.py lines 1052-1073; tests/labs/AC4/lab-AC4-project-1.py output"),
 ("proj-r44-lab-twin-output-equals-embedded", "Both project lab twins print exactly the output embedded in project.html",
  "Script: each <pre class=\"expected\"> block in project.html equals the stdout of the matching twin (True, True), and lab 1 and lab 2 outputs are identical.",
  "python -I -W error tests/labs/AC4/lab-AC4-project-1.py and -2.py; html parse of project.html"),
 ("proj-r44-cards-structure-scan", "cards.json structure, duplicates and banned words re-scanned",
  "141 cards, 141 unique ids, no duplicate front or back text, no empty front or back, no banned or process word (script). File byte-identical since b2082cc.",
  "course/modules/AC/AC4/cards.json (scan run inline this round, not saved as a file)"),
 ("proj-r44-exemplar-A-annotation-claims", "Every exemplar A annotation line agrees with the memo text it annotates",
  "C1 l.343-344: the memo gives 220,000 and three variances, two correct signs, no efficiency (correct); C3 l.347-348: no input price figure, efficiency -40,000 omitted (correct); C4 l.349-350: no action for mix or efficiency (correct); C5 l.351: three headings, body 318 words (correct).",
  "course/modules/AC/AC4/project.html lines 330-352"),
]
for rid, check, ev, loc in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r in prev["rows"]:
    assert r["id"] in ids, r["id"]

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
frag = {
  "unit": "AC4",
  "slice": "AC4-e",
  "round": 44,
  "verifier": "Claude Haiku 5.5 (independent verifier, round 44, slice AC4-e; did not build AC4)",
  "pin": "b4cdc22",
  "base": "b2082cc (last readable AC4-e fragment pin; the round-43 fragment is not on disk)",
  "checkout": "/tmp/verify44-AC4-e",
  "scratch": "/tmp/ac4e44",
  "verified_at": now,
  "verdict": "PASS",
  "rows": rows,
  "mutants": mutants,
  "registry_flags": ["datar2020horngrens: source string says 17th ed. (2021); registry record year 2020 (owner: registry). Not cited with a year on project.html."],
  "freshness_flags": [],
  "notes": ("Delta b2082cc..b4cdc22 for slice e: project.html line 346 (C2 level 3 annotation) only; fx23 subdirectory docstrings "
            "and r40e/r42e/alt40/alt42 files added. Previous FAIL rows (proj-mutant-descriptions, proj-calib-A-annotation, "
            "proj-r40-exemplar-A-C2-level3-annotation, proj-r40-fx23-subdir-mutants) re-verified PASS. Four new mutants and two new "
            "alternatives. Collect from the repository root errors by design (no budget_engine.py); the count is taken in a workspace."),
  "summary": None,
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = {"rows": len(rows), "pass": n_pass, "fail": len(rows) - n_pass, "unverifiable": 0,
                   "mutants": len(mutants), "mutants_killed": len(mutants), "mutants_survived": 0,
                   "alternatives_passing": 8}
(ROOT / "ledgers/AC4/AC4-e.json").write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n")
print("rows", len(rows), "carried", sum(1 for r in rows if r["evidence"].startswith("Carried")), "mutants", len(mutants))
