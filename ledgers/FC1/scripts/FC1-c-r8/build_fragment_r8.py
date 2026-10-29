import json, sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC8-FC1-c")
S = "ledgers/FC1/scripts/FC1-c-r8"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/C-FC1-c.round7.json").read_text())
CARRY_CARDS = "Carried from round 7 (cards.json FC1-c017 and L01.html byte-identical since the previous pin 0d2d0f3):"
CARRY = "Carried from round 7 (project.html and tests/labs/FC1 byte-identical since the previous pin 0d2d0f3):"

reverified = {
 "proj-run-graders": ("PASS", f"run_graders FC1 --seeds 0-49 this round: 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.1 s)' ({S}/run_graders.out). test_project.py changed this delta, so re-run."),
 "proj-collect-count-55": ("PASS", f"Collect on the scratch copy (instruments.py = reference.py): '59 tests collected' ({S}/collect.out). Page line 171 says 59 checks. Seeds 0-4 each '59 passed' ({S}/ref_seeds_0-4.out)."),
 "proj-browser-suite": ("PASS", f"page_smoke.py --unit FC1 --pages project.html --skip-sweep: 'page_smoke FC1: PASS' ({S}/page_smoke_project.out). Pyodide suite not driven by hand."),
 "proj-local-command": ("PASS", f"Command at project.html line 307 run verbatim in a scratch copy (instruments.py = reference.py): '59 passed in 0.02s' ({S}/local_pytest_seed0.out). Starter: '57 failed, 2 passed' (same run)."),
 "proj-alternatives-five": ("PASS", f"a1..a5 against the current test_project.py, seeds 0-49, each failing_seeds=0 ({S}/alts_r8.out, script {S}/alts_r8.sh)."),
 "proj-instances-50": ("PASS", f"run_graders FC1 50/50 seeds PASS ({S}/run_graders.out); instance.py unchanged since 0d2d0f3 (git diff empty)."),
 "proj-starter-vs-spec": ("PASS", f"starter.py unchanged; starter run on the current suite, seed 0: '57 failed, 2 passed' ({S}/local_pytest_seed0.out, starter run in the same scratch dir)."),
 "proj-lab1-twin": ("PASS", f"run_labs FC1: PASS (8/8) this round ({S}/run_labs.out). Lab twin project-1 is in that run; project.html and tests/labs/FC1 unchanged since 0d2d0f3."),
 "proj-lab2-completion": ("PASS", f"run_labs FC1: PASS (8/8) this round ({S}/run_labs.out), which runs the project-2 twin and page code."),
 "proj-lab2-docstring": ("PASS", f"run_labs FC1: PASS (8/8) this round ({S}/run_labs.out): page code equals twin, so the docstring at project.html line 107 equals the twin line 1."),
 "proj-lab3-fixtures": ("PASS", f"run_labs FC1: PASS (8/8) this round ({S}/run_labs.out); project-3 twin in that run."),
 "proj-check-pages-dag": ("PASS", f"check_pages --unit FC1: PASS ({S}/check_pages.out); check_dag --all: 'check_dag FC1: PASS' ({S}/check_dag_all.out)."),
 "proj-failure-messages": ("PASS", "Read grader/test_project.py lines 464-480 this round: the silence test's assertion is 'assert captured.out == \"\" and captured.err == \"\", f\"{label}: a valid input must print nothing\"', which names the input and the property and does not show a value. Lines 12 and 527-550 unchanged."),
 "proj-test-docstring": ("PASS", "Read grader/test_project.py lines 464-466 this round: the docstring's list (negative yield, zero yield, zero coupon, zero price, sell side, quantity 1, settlement period 1, one cent of face, one period, twelve periods) matches the ten boundary runs in the body (lines 470-480) one for one."),
 "proj-mutants-killed": ("PASS", f"mutate_graders.py --unit FC1 --seeds 0-49: 'mutate_graders FC1: PASS (58/58 killed)' ({S}/mutate_s0-49.out). Seeds 0-9: 58/58 ({S}/mutate_s0-9_r8.out). Round-7 survivors r7n01 and r7n02 now killed by test_the_module_prints_nothing."),
 "proj-silence-coverage": ("PASS", f"Round-7 survivors r7n01 (price_cents = 0) and r7n02 (yield_bps = 0) are KILLED by test_the_module_prints_nothing at seed 0 and at seeds 0-49 ({S}/mutate_s0-49.out). The test now has the zero price and zero yield runs (test_project.py lines 470, 474)."),
 "proj-new-mutants-r7": ("PASS", f"ledgers/FC1/mutants/r7n03_prints_on_one_period_bond.py KILLED by test_the_module_prints_nothing (seed 0), {S}/mutate_s0-49.out."),
 "proj-new-mutants": ("PASS", f"Round-5 mutants c5n01..c5n05 are in the 58/58 kill set ({S}/mutate_s0-49.out)."),
 "proj-new-mutants-r6": ("PASS", f"Round-6 mutants c6n01..c6n05 are in the 58/58 kill set ({S}/mutate_s0-49.out)."),
 "mutant-d-set": ("PASS", f"d01..d07 are in the 58/58 kill set ({S}/mutate_s0-49.out)."),
 "proj-lint-types": ("PASS", f"ruff check and ruff format --check on course/modules/FC/FC1/grader and tests/labs/FC1: 'All checks passed!' and '12 files already formatted' ({S}/ruff.out). mypy --no-incremental on reference.py, instance.py, starter.py: 'Success: no issues found in 3 source files' ({S}/mypy_grader.out)."),
 "proj-banned-phrases": ("PASS", "Grep for BUILDER_RULES §1.3 strings (TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'obviously', 'clearly', 'simply', 'it can be shown') over grader/test_project.py, reference.py, starter.py returned no hit (this round). project.html and the lab twins are unchanged since 0d2d0f3."),
 "proj-named-conditions": ("PASS", "test_project.py changed this delta only at lines 464-480 (silence test, verified by git diff 0d2d0f3..HEAD). The named-condition refusal and accepted-boundary tests lie outside that hunk and are byte-identical. Carried for those lines; project.html Constraints lines 163-167 unchanged."),
 "proj-fixture-claims": ("PASS", "test_project.py changed only at lines 464-480 this delta; fixture tests at lines 173 and onward are byte-identical, and the project.html line 275 fixture text is unchanged. Carried for the unchanged subject. Re-run values: run_graders and seeds 0-4 PASS this round."),
 "proj-notation": ("PASS", "The only new text in test_project.py this delta is the silence test (lines 464-480) and its docstring. It uses no math symbols. project.html, reference.py, instance.py and the project labs are byte-identical. Carried."),
 "proj-prose-numbers": (None, None),
 "proj-hours-arithmetic": (None, None),
 "proj-dag-closure": (None, None),
 "proj-reading-list": (None, None),
 "proj-spec-questions": (None, None),
 "proj-ladder": (None, None),
 "proj-stretch-scope": (None, None),
 "proj-privacy-claim": (None, None),
 "cards-misconception-refs": (None, None),
 "cards-scan-98": ("PASS", f"All 111 cards read this round (flattened by python -I; full dump {S}/cards_dump.txt). No duplicate ids, fronts or backs. Ten changed cards (c014, c029, c036, c039, c042, c091-c093, c095, c096) were read against the lesson text; the other 101 are byte-identical by id to 0d2d0f3 ({S}/cards_changed.txt)."),
 "cards-numbers": ("PASS", "Numbers on changed cards re-derived: c010 1000*(1-0.9^11)/0.1 = 6861.8940391 -> 686189 cents; c011 1000/(1-0.5*0.9) = 1818.18 -> 181818 cents, 18.18% of 10000; c014 multiplier 6.8619 is Lab 1 Part A stage 10 output; c092 limits 181818 and 1000000 printed by Lab 1 Part C; c093 -50 dollars printed; c029, c095, c096 counts printed by Lab 2 Part B (equities 3, rates 3, credit 2, fx 2, commodities 2; cash 6, derivative 6; exchange 4, otc 8). Lab output in " + S + "/twin_L01-1.out and twin_L02-1.out. Every number on a changed card appears in its lesson or lab output."),
 "cards-labels-and-hypotheses": ("PASS", "Cited labels exist in L01-L03: Definition 1.2 (L03 line 61), Definition 2.1 and Remark 2.2 (L03 lines 87, 92), Corollary 2.4 (L03 line 109), Proposition 3.1, 3.5, 4.1, 2.2 (L01 lines 89, 103, 131, 155), Remark 4.2 (L01 line 165). Hypothesis of c036 present (see cards-hypothesis-c036)."),
 "cards-hypothesis-c036": ("PASS", "c036 back now reads 'where m and h are whole numbers of cents (the lesson's convention), the quoted spread is even: s = 2h (Definition 1.2)'. This carries the hypothesis of L03 Definition 1.2 (line 61: 'm and h whole numbers of cents')."),
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in reverified and reverified[rid][0] is not None:
        st, ev = reverified[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
        continue
    if rid == "proj-silence-coverage":
        pass
    if rid == "cards-grades-and-basis":
        rows.append({
          "id": rid, "check": r["check"], "location": "cards.json FC1-c014, c029, c091, c092, c093, c095, c096 (grade C); L01.html grade table row (line 460, T); L02.html grade table row (line 408, T)",
          "status": "FAIL",
          "evidence": "Round 7 said the lab-printed claims were graded T. The builder regraded them C, but cards must agree with the CURRENT lesson text, and the lesson tables still grade the same claims T. L01.html line 460: 'The exact-arithmetic checks in Lab 1 agree with Propositions 2.2, 3.1, 3.5 and 4.1 ... T'. L02.html line 408: 'The counts on each axis of the typed-in register reconcile to 12 (exposure 3, 3, 2, 2, 2; form 6, 6; venue 4, 8) ... T'. Cards c014, c091, c092, c093 (Lab 1) and c029, c095, c096 (Lab 2) grade C for the same claims. BLUEPRINT §3 grades T as 'proved on the page' (the Propositions cited) and C as working paper, practitioner research or single-sample evidence, so C is also the wrong grade for an exact deterministic check. Cards c034 and c033 (C) are a separate question.",
          "fix": "Pick one grade for these claims and apply it to the cards and the lesson tables together. Under BLUEPRINT §3, the claims that restate a proposition on typed-in parameters are T with the proposition cited, and the card basis names the lab output. Then re-run this row."
        })
        continue
    if rid == "cards-lesson-agreement":
        rows.append({
          "id": rid, "check": r["check"], "location": "cards.json FC1-c039 back, FC1-c042 back; L03.html Remark 2.2 (line 93) and Corollary 2.4 (line 110)",
          "status": "FAIL",
          "evidence": "c039 back now reads 'V = 2V_b, where V_b is the volume that customers buy'. c042 back reads 'P = C = s V_b'. The current L03 text says 'V = 2Q' (Remark 2.2, line 93: 'The volume Q is therefore the shares bought by customers ... V = 2Q') and 'P = C = sQ' (Corollary 2.4, line 110). V_b appears nowhere in L03.html and nowhere in notation/notation.json (grep: no 'V_b' or 'V_{b}'). So both cards use a symbol the cited lesson does not define. Other cited agreements hold: c010, c014, c017, c029, c056, c058, c060, c093 (see round 7), c036 now matches Definition 1.2.",
          "fix": "Make the card and the lesson use one symbol. Either the lesson defines V_b once (L03 builder, with a Remark naming it) and Remark 2.2 and Corollary 2.4 use it, or the cards use the lesson's symbol. Either way the card text must match the lesson text at the locator above."
        })
        continue
    if rid == "cards-notation-Q":
        rows.append({
          "id": rid, "check": r["check"], "location": "cards.json FC1-c039 back, FC1-c042 back; plans/FC1-build-plan.md section 9.2 (Never use Q for a quantity or quote on an FC1 page)",
          "status": "FAIL",
          "evidence": "Round 7 flagged Q as a volume on c039 and c042. The cards now avoid Q, but use V_b, a new symbol not registered in notation/notation.json and not defined in L03.html. The notation rule (plan §9.2) forbids Q for a quantity, and the lesson's own use of Q (L03.html lines 93, 110, 115, 340) is a cross-slice defect for the L03 slice. A registered or lesson-defined symbol is required. Checked with: grep -c 'V_b' notation/notation.json and course/modules/FC/FC1/L03.html (both 0).",
          "fix": "Define the volume symbol once in L03.html (an allowed letter defined on first use) and use it in the card and in the lesson's Remark 2.2 and Corollary 2.4, removing Q from them. Notation requests go to NOTATION_REQUESTS if the symbol is program-wide."
        })
        continue
    if rid == "proj-reference-deployment":
        rows.append({
          "id": rid, "check": r["check"], "location": "course/modules/FC/FC1/grader/reference.py (git-tracked, 4327 bytes); BLUEPRINT.md §7 line 400-401; .github/workflows/ci.yml; tools/build_site.py",
          "status": "FAIL",
          "evidence": "BLUEPRINT §7: 'Deployment publishes course/ ... and excludes every grader/reference.py'. reference.py is tracked under course/ (git ls-files lists it). No exclusion exists: grep over tools/, .github/workflows/ci.yml, .gitignore and config files finds no rule that removes grader/reference.py from the published course/ tree. The only mentions are tools that read it (run_graders, page_smoke, check_projects). So the full solution is published. Checked with git ls-files and grep (this round).",
          "fix": "Add the exclusion to the deploy step (the step that publishes course/) for course/**/grader/reference.py, and move the file out of the published tree or add the exclusion test. Then re-run this row."
        })
        continue
    if rid == "proj-new-mutants-r8":
        continue
    # carry everything else (subject byte-identical or re-verified above)
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                 "evidence": ((CARRY_CARDS if rid.startswith("cards-") else CARRY) + " " + r["evidence"]) if r["status"] == "PASS" else r["evidence"]})

# new row
rows.append({"id": "proj-new-mutants-r8", "check": "2.6-autograder",
  "location": "ledgers/FC1/mutants/r8n01_prints_on_quantity_one.py, r8n02_prints_on_zero_yield.py, r8n03_prints_on_settlement_day_one.py, r8n04_prints_on_face_one_cent.py",
  "status": "PASS",
  "evidence": f"Four new student-error silence mutants (each prints one line on a valid input the page allows). mutate_graders.py --unit FC1 --seeds 0-49 kills all four at seed 0 by test_the_module_prints_nothing ({S}/mutate_s0-49.out, 58/58). Generator: {S}/make_mutants.py."})

# fix field for non-PASS rows
for r in rows:
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = "See evidence."

mutants = [
 {"id": "r7n01_prints_on_zero_price", "description": "Student error: CashTrade.events prints a line when the price is zero, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0 and seeds 0-49)"},
 {"id": "r7n02_prints_on_zero_yield", "description": "Student error: bond_price_cents prints a line at a zero yield, a valid input, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0 and seeds 0-49)"},
 {"id": "r7n03_prints_on_one_period_bond", "description": "Student error: Bond.__init__ prints a note when the bond has one period, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0)"},
 {"id": "r8n01_prints_on_quantity_one", "description": "Student error: CashTrade.events prints a line when the quantity is 1, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0)"},
 {"id": "r8n02_prints_on_zero_yield", "description": "Student error: bond_price_cents prints a line when the yield is zero, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0)"},
 {"id": "r8n03_prints_on_settlement_day_one", "description": "Student error: CashTrade.events prints a line when the settlement day is 1, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0)"},
 {"id": "r8n04_prints_on_face_one_cent", "description": "Student error: Bond.events prints a line when the face is one cent, a valid input the page allows, which the page's silence rule forbids.", "killed_by": "KILLED by test_the_module_prints_nothing (seed 0)"},
]

n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag = {
 "unit": "FC1", "slice": "FC1-c", "round": 8,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1 slice c (project.html, grader, project labs, cards.json), round 8; did not build FC1",
 "pin": "f618cf1",
 "base": "round 7 fragment /Users/billyribeiro/.fanout/frags/C-FC1-c.round7.json (pin 0d2d0f3), context only. Delta 0d2d0f3..f618cf1 in this slice: grader/test_project.py (silence test, lines 464-480) and cards.json (FC1-c014, c029, c036, c039, c042, c091-c093, c095, c096). project.html, reference.py, instance.py, starter.py and tests/labs/FC1 are byte-identical to 0d2d0f3 (git diff empty).",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC8-FC1-c",
 "scratch": "/tmp/fc1c8",
 "verified_at": "2026-10-29T07:38:48+00:00",
 "verdict": "FAIL" if n_fail else "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  f"Rows: {len(rows)} total, {n_fail} non-PASS (cards-grades-and-basis, cards-lesson-agreement, cards-notation-Q, proj-reference-deployment). Round-7 FAILs proj-silence-coverage, proj-mutants-killed and cards-hypothesis-c036 are PASS now with evidence.",
  "Mutants: 58 on disk (54 pre-round incl. r7n01-03, plus r8n01-04 added this round). mutate_graders FC1 seeds 0-9: 58/58; seeds 0-49: 58/58 killed.",
  "Alternatives a1-a5 pass seeds 0-49 against the current test_project.py (alts_r8.out). Local command run verbatim: 59 passed (QF_SEED=0 and seeds 0-4); starter 57 failed, 2 passed.",
  "Gates this round: check_pages --unit FC1 PASS; check_dag --all FC1 PASS; check_projects --all FC1 PASS; run_graders FC1 PASS; run_labs FC1 8/8 PASS; page_smoke FC1 project.html (--skip-sweep) PASS; ruff check and format on grader and labs PASS; mypy --no-incremental on reference, instance, starter: no issues.",
  "Lesson twins run alone under python -I -W error: lab-FC1-L01-1 exit 0, lab-FC1-L02-1 exit 0, lab-FC1-L03-1 exit 0 (outputs under " + S + ").",
  "Not checked: (1) the Pyodide suite in a real browser beyond page_smoke; (2) the full text of project.html was not re-read this round since it is byte-identical to 0d2d0f3 and its rows are carried; (3) verify_refs.py was not run this round (no reference or citation in the changed files; project.html reading list carried); (4) pytest over tests/ beyond the labs and the grader was not run; (5) cards' grade basis for c033 and c034 (C) was not re-graded in this round; (6) the L03 defect (Q used as a volume in L03.html lines 93, 110, 115) is a cross-slice finding, not checked row by row here.",
  "Grade judgement: BLUEPRINT §3 T means proved on the page; C means working paper, practitioner research or single-sample evidence. The lesson tables (L01 line 460, L02 line 408) and the cards disagree on the same claims, which is the row that fails, whichever grade is chosen.",
 ],
 "summary": f"FC1-c round 8: verdict {'FAIL' if n_fail else 'PASS'}. {len(rows)} rows, {n_fail} FAIL: cards-grades-and-basis (cards C vs lesson T), cards-lesson-agreement and cards-notation-Q (V_b on c039/c042 is not defined in L03), proj-reference-deployment (grader/reference.py not excluded from course/). Mutants 58/58 killed; alternatives a1-a5 pass; reference 50/50 seeds."
}
out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, len(rows), n_fail)
