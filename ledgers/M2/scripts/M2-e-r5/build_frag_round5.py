"""Build the round-5 fragment for M2 slice e from the verifier's own gate outputs and card verdicts (no carried PASS
without the byte-identity statement in its evidence)."""

import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M2-e")
S = "ledgers/M2/scripts/M2-e-r5"
verdicts = json.loads((ROOT / S / "card_verdicts_r5.json").read_text(encoding="utf-8"))
rows = []


def row(rid, check, location, evidence, status="PASS"):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


CARRY_ALL = ("Carried from round 4 (course/modules/M/M2/project.html, grader/*.py, tests/labs/M2/*.py, "
             "plans/M2-build-plan.md, index.html and the lessons L19-L21 and L24 are byte-identical between the round-4 "
             "pin 4eb6788f and the pin 440ed3c8, per git diff --stat 4eb6788f 440ed3c8): ")

row("e2-check-pages", "2.9 structure", "course/modules/M/M2/",
    f"Re-run this round: .venv/bin/python tools/check_pages.py --unit M2 -> 'check_pages M2: PASS', rc=0 ({S}/check_pages.out).")
row("e2-check-dag", "2.9 DAG", "course/modules/M/M2/",
    f"Re-run this round: tools/check_dag.py --unit M2 -> 'check_dag M2: PASS', rc=0 ({S}/check_dag.out).")
row("e2-check-projects", "2.6 spec, ladder, hours, rubric", "course/modules/M/M2/project.html",
    f"Re-run this round: tools/check_projects.py --unit M2 -> 'check_projects M2: PASS', rc=0 ({S}/check_projects.out).")
row("e2-run-graders", "2.6 autograder 1", "course/modules/M/M2/grader/reference.py",
    f"Re-run this round: tools/run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds)', rc=0 ({S}/run_graders.out).")
row("e2-run-labs-project", "2.5 labs", "course/modules/M/M2/project.html lab-M2-project-1..3",
    f"Re-run this round: tools/run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)', rc=0, covering the 24 lesson labs and project labs 1-3 ({S}/run_labs_M2.out).")
row("e2-lab-page-code-equals-twin", "2.5 labs: page code equals twin", "project.html lab blocks 1-3; tests/labs/M2/lab-M2-project-1..3.py",
    CARRY_ALL + "page code equals twin as established in round 4 (ledgers/M2/scripts/M2-e-r4/lab-M2-project-*.out); "
    "run_labs re-run this round passes all three project labs.")
row("e2-lab-twin-clean-and-expected", "2.5 labs: twin under python -I -W error; expected block equals output",
    "tests/labs/M2/lab-M2-*.py (27 twins)",
    f"Re-run this round: each of the 27 twins run alone as .venv/bin/python -I -W error FILE: rc=0 and empty stderr for all 27 ({S}/twins_r5.out). "
    "The expected-block equality for the three project labs is carried from round 4 (project.html byte-identical).")
row("e2-page-smoke-project", "2.9 page_smoke", "course/modules/M/M2/project.html",
    f"Re-run this round: tools/page_smoke.py --unit M2 -> 'page_smoke M2: PASS', rc=0, project labs and in-browser grader '87 tests pass' ({S}/page_smoke_M2.out).")
row("e2-pytest-local-and-count", "2.6 autograder 5 and page test count", "course/modules/M/M2/grader/test_project.py",
    "Re-run this round: pytest --collect-only -q -> '87 tests collected'; project.html line states 'runs 87 tests'; "
    "pytest -W error with QF_SEED 0, 7 and 49 -> '87 passed' each (run in /tmp/m2e_r5 copy of the grader).")
row("e2-ruff", "gate: ruff", "tests/labs/M2, course/modules/M/M2/grader",
    f"Re-run this round: ruff check and ruff format --check on both paths -> 'All checks passed!', '31 files already formatted' ({S}/ruff_check.out, {S}/ruff_format.out).")
row("e2-mypy-labs", "gate: mypy strict on labs", "tests/labs/M2",
    f"Re-run this round: .venv/bin/mypy --no-incremental tests/labs/M2 -> 'Success: no issues found in 27 source files' ({S}/mypy_labs.out).")
row("e2-mypy-grader-command", "plan section 8 grader mypy command", "plans/M2-build-plan.md section 8; grader/test_project.py",
    f"Re-run this round: the plan's grader mypy --strict --no-incremental command on the three grader files -> 'Success: no issues found in 3 source files', rc=0 ({S}/mypy_grader_r5.out).")
row("e2-pytest-labs-tests", "gate: pytest for lab tests", "tests/test_labs.py, tests/test_run_labs.py -k M2",
    f"Re-run this round: pytest -q tests/test_labs.py tests/test_run_labs.py -k M2 -> 27 passed, rc=0 ({S}/pytest_labs_M2.out).")
row("e2-verify-refs", "2.1 citations: keys cited by project.html", "references/references.json; course/modules/M/M2/project.html",
    f"Re-run this round: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', rc=0 ({S}/verify_refs_offline.out). Live Crossref run not performed (offline gate only).")
row("e2-hours-arithmetic", "hours arithmetic: hub split vs lesson hours", "course/modules/M/M2/index.html; project.html time budget",
    CARRY_ALL + "hub split and project time budget; no hour figure in any changed file (L22, L23 and cards.json changed only in prose and card text).")
for rid, label in [
    ("e2-project-lab1-numbers", "numbers in prose vs unrounded values (Lab 1)"),
    ("e2-project-lab2-numbers", "numbers in prose vs unrounded values (Lab 2)"),
    ("e2-project-lab3-numbers", "numbers in prose vs unrounded values (Lab 3)"),
]:
    row(rid, label, "course/modules/M/M2/project.html",
        CARRY_ALL + "project lab prose numbers; the lab outputs were re-run this round in run_labs (PASS).")
row("e2-project-exemplar-numbers", "numbers in exemplars A and B", "project.html Exemplars A and B",
    CARRY_ALL + "exemplar numbers.")
row("e2-project-spec-signatures", "spec signatures vs starter and reference", "project.html Rung 3; grader/starter.py; grader/reference.py",
    CARRY_ALL + "signatures; the fd_derivative, ad_derivative, hessian_fd, bond_price_cents and sensitivities signatures "
    "are exercised by all 87 tests and by the two new alternative engines (see e5-alternatives).")
row("e2-project-tolerances-conventions", "tolerances and conventions", "project.html Conventions and Tolerances; grader/test_project.py",
    CARRY_ALL + "tolerances; the test suite re-run this round passes at seeds 0, 7, 49 and 0-49 for the reference.")
row("e2-project-rubric-calibration", "rubric calibration (blind scoring)", "project.html rubric table and Exemplars A and B",
    CARRY_ALL + "rubric and exemplar annotations.")
row("e2-project-rubric-observable", "rubric levels are observable", "project.html rubric table",
    CARRY_ALL + "rubric descriptors.")
row("e2-project-adversarial-atlas-studio", "adversarial question bank / atlas / studio", "project.html; plan sections 0, 7",
    CARRY_ALL + "project.html question bank, atlas and studio paragraphs.")
row("e2-project-notation", "notation registry: no symbol reused with another meaning", "project.html math; cards.json; L19-L24",
    "notation/notation.json registers T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f and Q. grep over course/modules/M/M2 "
    "(project.html, L22.html, L23.html and all lessons) shows none of these symbols used as a math symbol; the only 'T' is the grade letter "
    "T (Theorem) in the grade legend. The new L22 and L23 text introduces K, J, I, G, V and x-tilde with local meanings only. PASS.")
row("e2-banned-phrases", "banned phrases", "project.html; cards.json; grader/*.py; labs; L22, L23",
    "Re-scan this round against BUILDER_RULES 1.3-1.4 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, "
    "left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, "
    "clearly, it can be shown that, roughly half, historically, ellipsis): cards.json, L22.html, L23.html, project.html and the grader "
    "and labs: no hit. The only three-dot sequences are Python annotations tuple[float, ...] in L22.html lines 119-120 and L23.html line 120.")
row("e2-scope-words", "scope words", "project.html intro, Labs 1-3 prose; instance.py docstring; L22, L23 changed text",
    CARRY_ALL + "project.html, labs and instance.py. The changed L22 and L23 text was read in full this round (Remark 1.4, "
    "Proposition 2.1, Lab prose): no unqualified 'always' or 'every' without a computation or a stated hypothesis.")
row("e2-project-data-simulated", "simulated data labelled", "project.html; grader/instance.py; L22, L23 labs",
    CARRY_ALL + "project data labels; L22 lab docstring says SIMULATED test functions and L23 lab says the bond is SIMULATED (read this round).")
row("e2-project-process-words", "no process words in learner text", "project.html; cards.json; grader/test_project.py messages; L19-L24",
    "Re-scan this round: grep -i for round, verifier, builder, audit, this round, previous round over cards.json, L22.html and L23.html: no hit. "
    "project.html, grader and labs carried from round 4 (byte-identical).")
row("e2-grader-instances", "instance validity over seeds 0-49", "course/modules/M/M2/grader/instance.py",
    CARRY_ALL + "instance.py; the reference passes 50/50 seeds re-run this round (e2-run-graders).")
row("e2-grader-instance-claims", "instance.py docstring ranges", "instance.py lines 1-20 docstring",
    CARRY_ALL + "instance.py docstring.")
row("e2-grader-reference", "reference solution passes the suite", "course/modules/M/M2/grader/reference.py",
    f"Re-run this round: run_graders reference 50/50 (e2-run-graders) and pytest 87 passed at seeds 0, 7, 49 with the reference as sensitivity_engine.py.")
row("e2-grader-alternatives", "five alternative correct implementations pass", "ledgers/M2/scripts/M2-e-r3/alts/*.py and ledgers/M2/scripts/M2-e-r5/alts_r5/*.py",
    f"Re-run this round over seeds 0-49 ({S}/run_alts_r5.out): reference 50/50; r3 alt1 Richardson central 50/50; r3 alt2 complex step 50/50; "
    "r3 alt3 reverse mode 50/50; r3 alt4 exact rational 50/50; r3 alt5 numpy 50/50; round-5 alt A (decimal half-even rounding, fsum) 50/50 "
    f"after its own precision defect was fixed ({S}/run_alt_a_patched.out); round-5 alt B (iterative discounting, Python round) 50/50. See e5-alternatives.")
row("e2-grader-messages", "failure messages name a property and a hint", "course/modules/M/M2/grader/test_project.py (884 lines)",
    CARRY_ALL + "test_project.py messages (file unchanged). Not re-read this round beyond the failing-test messages printed by the alternative runs.")
row("e2-grader-valueerror-scope", "exception type demanded only for conditions the page names", "test_project.py must_raise call sites",
    CARRY_ALL + "must_raise call sites (file unchanged). Checked this round against the alternative runs: the one failure seen (test_yield_just_above_minus_one_is_accepted, yield -9999 bps, for the first draft of alternative A) came from the alternative (a 28-digit Decimal context raised InvalidOperation on a price with 38 integer digits), not from an over-constrained test; after the alternative was fixed it passes.")
row("e2-grader-no-print", "module prints nothing and warns nothing", "test_project.py autouse fixture; purity test",
    CARRY_ALL + "autouse fixture; the suite runs with -W error at all seeds re-run this round.")
row("e2-mutants-existing", "every existing mutant killed", "ledgers/M2/mutants/ (147 files this round)",
    f"Re-run this round: tools/mutate_graders.py --unit M2 --seeds 0-9 -> 'mutate_graders M2: PASS (147/147 killed)', rc=0 ({S}/mutate_M2_r5.out). The 143 pre-existing and 4 new mutants are all killed.")
row("e2-mutants-written", "verifier-written mutants from round 3", "ledgers/M2/mutants/r3_01..r3_04",
    "Included in the 147/147 mutate_graders re-run of this round (killed).")
row("e2-mut-v2-01", "round-2 survivor: dprice_dy numerical", "course/modules/M/M2/grader/test_project.py",
    "Round-2 survivor mutant still present in ledgers/M2/mutants and killed in the 147/147 re-run this round.")
row("e2-mut-v2-02", "round-2 survivor: d2price_dy2 numerical", "course/modules/M/M2/grader/test_project.py",
    "Round-2 survivor mutant still present and killed in the 147/147 re-run this round.")
row("e2-mut-v2-03", "round-2 survivor: forward step floored at 1e-8", "course/modules/M/M2/grader/test_project.py",
    "Round-2 survivor mutant still present and killed in the 147/147 re-run this round.")
row("e4-mutants-new-r4", "three new student-error mutants written by round-4 verifier", "ledgers/M2/mutants/r4_01..r4_03",
    "The three round-4 mutants are included in the 147/147 re-run this round (killed).")
row("e2-cards-count", "card count and id format", "course/modules/M/M2/cards.json",
    f"Re-run this round: 391 cards, 391 unique ids, all ids match M2-cNNN ({S}/cards_mech_r5.py). Round 4 had 394 (c388, c389, c396 removed; no card added).")
row("e2-cards-dup-ids-fronts", "no duplicate cards", "course/modules/M/M2/cards.json",
    "No duplicate id. One normalised-front collision ('In Lab 1, what is P(y0) ... y0 = 0.04') is two distinct questions: P'(y0) (c342) and P''(y0) (c343), "
    "differing by the prime. No duplicate card.")
row("e2-cards-numbers", "every card number appears in its own lesson", "cards.json vs L01-L24",
    "Round 5: every number and label (Proposition, Lemma, Theorem, Corollary, Definition, Example, Remark, Assumption, Problem) of the 332 cards "
    "re-verified this round is read in its own lesson (per-card evidence in " + S + "/card_verdicts_r5.json). Cards of L19-L21 and L24 "
    "(other than c358) carried below. Mechanical re-scan (cards_mech_r5.py) flags only Misconception labels, which are unnumbered paragraphs, and cross-lesson 'Definition 1.3 of Lesson 9' references, both checked by hand.")
row("e2-cards-locators", "every card locator resolves in its lesson", "cards.json vs L01-L24",
    "Round 5: locators (Section, Remark, Example, Misconception, Problem, Lab part) of the re-read cards checked against the lesson text; see " + S + "/card_verdicts_r5.json. Locators of the carried cards of L19-L21 and L24 carried.")
row("e2-cards-grades", "grade and basis fields", "course/modules/M/M2/cards.json",
    f"Re-run this round ({S}/cards_mech_r5.py): grade values only None, T, C; no C without basis; no T with basis; C grades are the lab-result cards with a basis string.")

# ---- per-lesson card rows for L01-L18 (re-read this round, every card) and L22, L23, L24 c358 (re-read this round)
import collections
cards = json.loads((ROOT / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
by_lesson = collections.defaultdict(list)
for c in cards:
    by_lesson[c["lesson"]].append(c["id"])
for L in [f"L{n:02d}" for n in range(1, 19)] + ["L22", "L23"]:
    ids = by_lesson[L]
    assert all(verdicts[i]["status"] == "PASS" for i in ids), L
    row(f"e2-cards-{L}", "card check vs lesson (every card read this round)", f"cards.json {L}; course/modules/M/M2/{L}.html",
        f"Round 5 full re-read: all {len(ids)} cards of {L} ({ids[0]}..{ids[-1]}) read against the cleaned text of {L}.html "
        f"(clean.py, {S}/lesson_text/{L}.txt) including the lesson's Lab output blocks, misconceptions and problem set where cited. "
        f"Per-card evidence: {S}/card_verdicts_r5.json. Lesson text unchanged except L22 and L23, both re-read.")
# L24: c358 re-read this round; the other 16 entries and L24.html carried
l24 = by_lesson["L24"]
row("e2-cards-L24", "card check vs lesson", "cards.json L24; course/modules/M/M2/L24.html",
    f"Mixed: M2-c358 (changed) re-read this round against L24 Section 1 (PASS, {S}/card_verdicts_r5.json). The other {len(l24) - 1} L24 "
    "entries and L24.html are byte-identical to the round-4 pin (git diff --stat 4eb6788f 440ed3c8; cards.json entries compared by id). "
    "Carried from round 4: " + ", ".join(i for i in l24 if i != "M2-c358") + " (round 4 PASS on the same bytes).")
for L in ["L19", "L20", "L21"]:
    row(f"e2-cards-{L}", "card check vs lesson", f"cards.json {L}; course/modules/M/M2/{L}.html",
        f"Carried from round 4 (course/modules/M/M2/{L}.html and its {len(by_lesson[L])} cards.json entries are byte-identical between pins 4eb6788f and 440ed3c8; checked by a per-id comparison of cards.json this round). Round-4 PASS on these bytes.")
row("e2-cards-L19-L21-untouched-proof", "subject byte-identity for carried card rows", "cards.json; L19.html, L20.html, L21.html, L24.html",
    "git diff --stat 4eb6788f 440ed3c8 lists only L22.html, L23.html and cards.json for M2 course files. A per-id comparison of cards.json between the two commits shows changed entries only for M2-c358 (L24), c326 (L22), c379 and c068 and c072 (L05, L06), c230 (L15), and the removed c388, c389, c396. All L19-L21 entries are identical.", "PASS")

# ---- round-5 rows (new work)
row("e3-cards-whole-set-mechanical", "whole-set card checks", "cards.json (391 cards) vs L01-L24 cleaned text",
    f"Re-run this round ({S}/cards_mech_r5.py): 391 cards, unique ids, grade fields valid; label citations resolved in their own lesson except (a) 'Misconception n' labels, which are unnumbered paragraphs in the lesson (each checked by hand this round against the Misconceptions section) and (b) cross-lesson references 'Definition 1.3 of Lesson 9' (c135, c137), checked against L10 text.")
row("e5-alternatives", "alternative correct implementations over seeds 0-49", f"{S}/alts_r5/ and ledgers/M2/scripts/M2-e-r3/alts/",
    "Two new alternatives written by this verifier: alt A (Decimal half-even rounding with a 400-digit context, fsum sums, a plain forward-mode class), 50/50 after fixing its own 28-digit precision defect; alt B (iterative discounting, Python round for half-even, hand-written dual numbers and per-entry second differences), 50/50. Alternatives r3 alt1-alt5 re-run: 50/50 each.")
row("e5-mutants-new-r5", "three or more new student-error mutants, all killed", "ledgers/M2/mutants/r5_01..r5_04",
    "Four new student-error mutants written by this verifier, each a complete solution module with the error named on the first docstring line: r5_01 central difference with endpoints swapped (returns minus the derivative); r5_02 convexity not divided by the unrounded price; r5_03 mixed Hessian entries left at zero; r5_04 bond price with simple interest discounting. All four killed by seed 0 (mutate_graders output in " + S + "/mutate_M2_r5.out).")
row("e5-twins-alone", "lab twins run alone under python -I -W error", "tests/labs/M2/lab-M2-*.py",
    f"27 twins, each rc=0 with empty stderr ({S}/twins_r5.out).")
row("e5-fragment-gate-set", "gate set run this round on pin 440ed3c8", "course/modules/M/M2",
    "check_pages, check_dag, check_projects, run_labs (27/27), run_graders (50/50), page_smoke, ruff check and format, mypy labs, mypy grader command, pytest labs (27), verify_refs --offline (560/0), mutate_graders (147/147), collect-only (87), pytest seeds 0, 7, 49, and 27 twins alone. All PASS.")

# ---- validate the row set against the round-4 row ids (every round-4 id kept)
round4_ids = ["e2-check-pages","e2-check-dag","e2-check-projects","e2-run-graders","e2-run-labs-project","e2-lab-page-code-equals-twin","e2-lab-twin-clean-and-expected","e2-page-smoke-project","e2-pytest-local-and-count","e2-ruff","e2-mypy-labs","e2-mypy-grader-command","e2-pytest-labs-tests","e2-verify-refs","e2-hours-arithmetic","e2-project-lab1-numbers","e2-project-lab2-numbers","e2-project-lab3-numbers","e2-project-exemplar-numbers","e2-project-spec-signatures","e2-project-tolerances-conventions","e2-project-rubric-calibration","e2-project-rubric-observable","e2-project-adversarial-atlas-studio","e2-project-notation","e2-banned-phrases","e2-scope-words","e2-project-data-simulated","e2-project-process-words","e2-grader-instances","e2-grader-instance-claims","e2-grader-reference","e2-grader-alternatives","e2-grader-messages","e2-grader-valueerror-scope","e2-grader-no-print","e2-mutants-existing","e2-mutants-written","e2-mut-v2-01","e2-mut-v2-02","e2-mut-v2-03","e4-mutants-new-r4","e2-cards-count","e2-cards-dup-ids-fronts","e2-cards-numbers","e2-cards-locators","e2-cards-grades"] + [f"e2-cards-L{n:02d}" for n in range(1, 25)] + ["e3-cards-whole-set-mechanical"]
have = {r["id"] for r in rows}
missing_ids = [i for i in round4_ids if i not in have]
print("round-4 ids missing from the round-5 rows:", missing_ids)
assert not missing_ids, missing_ids
assert all(r["status"] == "PASS" for r in rows)

mutants = [
    {"id": "r5_01_central_difference_sign_swapped", "description": "The central estimate is written with its endpoints swapped, so it returns minus the derivative.",
     "killed_by": "test_central_difference_matches_the_analytic_derivative[inst0] (seed 0)"},
    {"id": "r5_02_convexity_not_divided_by_the_price", "description": "Convexity is returned as the second sensitivity in cents, without dividing by the unrounded price.",
     "killed_by": "test_named_ratios_are_the_stated_formulas[inst0] (seed 0)"},
    {"id": "r5_03_hessian_mixed_entries_left_at_zero", "description": "The mixed second partials are never filled in, so every off-diagonal Hessian entry stays at zero.",
     "killed_by": "test_hessian_matches_the_analytic_hessian[inst0] (seed 0)"},
    {"id": "r5_04_bond_price_uses_simple_interest", "description": "The bond price discounts each cash flow with simple interest, 1 / (1 + rate * t), not compound discounting.",
     "killed_by": "test_price_is_the_half_even_rounding_of_the_exact_price[inst0] (seed 0)"},
    {"id": "pre-existing-143", "description": "The 143 mutants already in ledgers/M2/mutants before this round (e01..x14, r3_*, r4_*, r6..r15, s01..s10, v01..v2_03), re-run this round.",
     "killed_by": "tools/mutate_graders.py --unit M2 --seeds 0-9: 147/147 killed in total (" + S + "/mutate_M2_r5.out)"},
]

frag = {
    "unit": "M2",
    "slice": "e",
    "round": 5,
    "verifier": "independent verifier (Haiku 5.5), slice e, verifyD5-M2-e",
    "pin": "440ed3c8",
    "base": "round-4 fragment /Users/billyribeiro/.fanout/frags/D-M2-e.round4.json (pin 4eb6788f). Delta 4eb6788f..440ed3c8 for M2 course files: L22.html, L23.html and cards.json (cards c379, c068, c072, c230, c326, c358 changed; c388, c389, c396 removed). project.html, grader/, tests/labs/M2, plans/M2-build-plan.md, index.html, L19-L21, L24.html unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M2-e",
    "scratch": "/tmp/m2e_r5 and ledgers/M2/scripts/M2-e-r5",
    "verified_at": "2026-11-03T20:12:15Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-4 scope gap closed: every card of L01-L18 (292 cards) and of L22, L23 and the changed card c358 of L24 (39 + 1 cards) was read this round against the cleaned text of its lesson, including the lab output blocks, misconceptions and problem sets it cites (per-card evidence in " + S + "/card_verdicts_r5.json; 332 verdicts, all PASS). Cards of L19-L21 and the other 16 entries of L24 are carried from round 4 by the byte-identity rule (per-id comparison of cards.json with 4eb6788f: only c358 among L19-L24 changed).",
        "Changed-card checks: c379 (L05, central difference uses values only, Section 1), c068 and c072 (L06, Assumption 2.1 and Misconception 2/3), c230 (L15, Proposition 3.5 with both signs of sin theta), c326 (L22, Remark 1.4 with L21 Theorem 1.3 uniqueness), c358 (L24, backward quotient). All PASS. Removed cards c388, c389, c396 (L10 and L08 Theorem and Assumption restatements) no longer exist; no remaining card depends on them (checked by grep for their ids).",
        "L09 forward references (Lesson 10 Theorem 2.1 for the value 1/6 in Misconception 2, Lesson 11 Lemma 1.1 for integrability) are prose cross-references, graded T in card c129, and the lesson states that they are forward references not derived there. check_dag PASS. Not a finding.",
        "Alternative A of this verifier failed at first (39/50 seeds) because its 28-digit Decimal context raised InvalidOperation on prices above 10^28 cents at yield -0.9999; the grader's test_yield_just_above_minus_one_is_accepted caught that correctly. After fixing the alternative (400-digit context) it passes 50/50. No grader over-constraint was found.",
        "Scratch directory ledgers/M2/scripts/M2-e-r5 already held 29 files tracked by commit 44f1eb6a (alts/, build_fragment_r5.py, outputs/, probe/, report_sim/, run_r5.sh, quick_checks.py, reveal_check.py, showcards.py, showlesson.py, totext.py, twin_and_alt_runs.py, ratio_check.py). This verifier did not read or use them as evidence; its own files there carry the names listed in the fragment.",
        "Lab twins: 27/27 run alone under python -I -W error, rc=0, empty stderr. Project labs 1-3 page code equals twin and expected blocks: carried (project.html byte-identical), and run_labs passes them this round.",
        "Card-level observations (not failures): c370 (round-4 note) asks the reader to assume M_2 = M_3 = e; the card answer uses the lesson's approximate wording and remains C with basis. c357 repeats the lesson's exactness qualification. Card id gaps (c243, c333) are allowed by ruling.",
    ],
    "summary": "Slice e round 5 (pin 440ed3c8): PASS on the re-verified scope. Every card of L01-L18 (292), L22 (15), L23 (24) and the changed card c358 (L24) re-read against its lesson this round (332 verdicts, all PASS). Gates re-run fresh and PASS: check_pages, check_dag, check_projects, run_labs (27/27), run_graders (50/50), page_smoke, pytest collect 87 and seeds 0/7/49, ruff, mypy labs, plan mypy grader command, pytest labs, verify_refs --offline (560/0), 27 twins alone, mutate_graders 147/147 (4 new student-error mutants, all killed), alternatives 50/50 each (5 r3 alternatives, 2 new). L19-L21 and the other 16 L24 entries carried from round 4 by byte-identity; project.html, grader, project labs and plan carried (byte-identical). Disclosed: online verify_refs not run; project prose rows carried rather than re-read.",
}

out = ROOT / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "wrote", out)
