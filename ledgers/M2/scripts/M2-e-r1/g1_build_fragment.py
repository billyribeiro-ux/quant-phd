import json, re, sys
from datetime import datetime, timezone
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyG1-M2-e/tools")
import ledger  # noqa: E402

CHK = "/Users/billyribeiro/.fanout/wt/verifyG1-M2-e"
S = f"{CHK}/ledgers/M2/scripts/M2-e-r1"
base = json.load(open("/Users/billyribeiro/.fanout/frags/F2-M2-e.round1.json"))
base_rows = {r["id"]: r for r in base["rows"]}

V = {
 "e2-check-pages": "check_pages.py --unit M2 -> 'check_pages M2: PASS', exit 0 (ledgers/M2/scripts/M2-e-r1/g1_check_pages.out); re-run because cards.json changed; covers banned strings, ids, lesson, grade and keys of 395 cards.",
 "e2-check-dag": "check_dag.py --unit M2 -> 'check_dag M2: PASS', exit 0 (g1_check_dag.out).",
 "e2-check-projects": "check_projects.py --unit M2 -> 'check_projects M2: PASS', exit 0 (g1_check_projects.out).",
 "e2-run-graders": "run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.6 s)', exit 0 (g1_run_graders.out).",
 "e2-run-labs-project": "run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)', exit 0 (g1_run_labs_M2.out); the three project labs are among the 27.",
 "e2-page-smoke-project": "page_smoke.py --unit M2 -> 'page_smoke M2: PASS', exit 0 (g1_page_smoke_M2.out), which includes project.html.",
 "e2-pytest-local-and-count": "Suite staged as tools/run_graders.py stages it (test_project.py, instance.py, reference.py as sensitivity_engine.py) in a scratch dir: collect-only '89 tests collected' for seeds 0, 7, 23, and '89 passed' under -W error for each seed (ledgers/M2/scripts/M2-e-r1/g1_grader_staged.out). project.html line 211 states 89 tests: equal to the collected count.",
 "e2-ruff": "ruff check tests/labs/M2 course/modules/M/M2/grader -> 'All checks passed!', exit 0 (g1_ruff_labs.out); ruff format --check -> '31 files already formatted', exit 0 (g1_ruff_format.out).",
 "e2-mypy-labs": "mypy tests/labs/M2 --no-incremental -> 'Success: no issues found in 27 source files', exit 0 (g1_mypy_labs.out).",
 "e2-mypy-grader-command": "mypy --strict --no-incremental on the staged test_project.py, instance.py and sensitivity_engine.py -> 'Success: no issues found in 3 source files', exit 0 (g1_mypy_grader_strict.out).",
 "e2-pytest-labs-tests": "pytest -q tests/test_labs.py tests/test_run_labs.py -k M2 -> 27 passed, exit 0 (g1_pytest_labs.out).",
 "e2-verify-refs": "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (g1_verify_refs_offline.out). references/ is not changed by the delta (git diff). The live run was not repeated (see notes).",
 "e2-grader-reference": "run_graders.py --unit M2 --seeds 0-49 -> reference 50/50 seeds (g1_run_graders.out); the staged reference passes 89/89 for seeds 0, 7, 23 (g1_grader_staged.out).",
 "e2-mutants-existing": "tools/mutate_graders.py --unit M2 -> 'mutate_graders M2: PASS (175/175 killed)', exit 0 (g1_mutate_graders_M2.out): 175 KILLED lines, 0 SURVIVED. The standing set is byte-identical to the base (git diff ledgers/M2/mutants: empty).",
 "e2-project-notation": "Changed cards (28 changed, 3 removed) scanned for the registered symbols of notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}): none present (python scan this round). project.html is byte-identical (carried part).",
 "e2-banned-phrases": "check_pages.py --unit M2 -> PASS (g1_check_pages.out) over the 395 cards of cards.json at this pin, including the changed ones; project.html, grader/ and labs byte-identical since the base (carried part).",
 "e2-scope-words": "Scope words in the changed cards (always, only, every, any, same, exactly, never, none) each checked against the sentence it restates: M2-c064 (L06 line 30, 'Every result in Sections 2 and 3 ... begins its statement with Assuming Assumption 2.1'), c096 (L07 Misconception 3), c111 and c422 (Example 2.4 bound at x = 1/2; Proposition 2.3 for every n and x not 1), c113 and c161 (Misconceptions 2 and 1 of L08 and L11), c143 (L10 Section 5), c177 (L12 Misconception 1). No unsupported scope word found.",
 "e2-cards-count": "cards.json has 395 cards at pin 2a805c83 (python count this round), 398 at the base pin 95f3f8cb: removed M2-c417, M2-c428, M2-c429; none added. Per lesson: L08 20 -> 18, L10 17 -> 16, others unchanged. Ids unique. No M2 page states a card count (grep for card counts in course/modules/M/M2/*.html: none).",
 "e2-cards-dup-ids-fronts": "python scan of 395 cards (this round): exact duplicate fronts 0, exact duplicate backs 0, ids unique. Semantic duplicates are row e10-cards-c412-duplicates-c065 (PASS at this pin).",
 "e2-cards-numbers": "Every numeric token of the 395 cards' fronts and backs (2855 tokens) occurs in its lesson's extracted text (python this round, /tmp/m2e_r1b/numcheck.py): 0 missing. Lab outputs the changed cards quote (c107: 8.10000000 and 0.535841; c422: 3/10 and n 0 to 10) appear in L08.html and L07.html.",
 "e2-cards-locators": "Every changed card's locator checked by hand against the lesson text (rows e2-cards-L06 to e2-cards-L24 below); the 24 lesson pages exist for every card (python). Unchanged cards are byte-identical to the base.",
 "e2-cards-grades": "Grades (python this round): T 235, C 76 (each with a basis), no grade 84; no basis without a grade; no C without a basis. M2-c422 changed C -> T with its basis removed: the new basis is Proposition 2.3, which the L07 key-results table grades T (the L07 key-results table, text extraction).",
 "e2-cards-L06": "Changed card M2-c064 re-read against L06 Assumption 2.1 (text line 30: continuous at each point of [a,b], a<b, attains max and min; no grade; every result in Sections 2 and 3 begins 'Assuming Assumption 2.1') and against L08 Assumption 1.1 (L08 text line 26: continuous on [p,q], p<q; attains max and min; no grade given): the added sentence 'Lesson 8 states the same assumption as its Assumption 1.1 (Section 1), with no grade' is accurate. M2-c065 (Rolle, T) and c066 (MVT, T) match Theorem 2.2 and 2.3 of L06. The other L06 cards are byte-identical to the base.",
 "e2-cards-L07": "Changed M2-c096 re-read against L07 Misconception 3 (text: 'at x = 3/10 it shrinks with the degree, but at x = 2 its absolute value doubles at each degree: at degree 10 the error is -2048 (Lab 1, part C)') and the Lab 1 part C output (n = 10 error -2048; errors -2, -4, ... -2048 doubling). Changed M2-c422 (now T) re-read against Proposition 2.3 (every n >= 0, x != 1) and the twin's part B (X_B = Fraction(3,10), N_MAX = 10, exact equality check, lab lines 205-206 and the remainder check).",
 "e2-cards-L08": "Changed cards re-read against the L08 text (extraction /tmp/m2e_r1b/text/L08.txt): M2-c099 (Rolle applied repeatedly under Assumption 1.1, Theorem 2.1 proof, y_(j+1)), c102 (Example 2.3, xi = 1-(1-x)^(1/(n+2))), c104 (Example 2.4: ratio 2^(n+2)(1-x) in [2^(n+1), 2^(n+2))), c107 (part C row 0.90 1 0.535841 8.10000000; xi = 1 - 0.1^(1/3)), c111 (bound 2 at x = 1/2; remainder (1/2)^n; Problem L08-R3), c112 (Misconception 1), c113 (Misconception 2), c114 (Misconception 3; x = 0.6 bound 8.4375 vs remainder 0.54). Removed M2-c417 and c428 (see e10 row and e6-card-M2-c408-c409 note). Lesson statements unchanged.",
 "e2-cards-L09": "Changed M2-c423 re-read against L09 Misconception 2 (text line 166): both endpoint sums 1/8, the integral 1/6 is a forward reference to L10 Theorem 2.1, the bracket uses suprema and infima. M2-c425 re-read against L09 Remark 1.4 and Theorem 2.2 and Corollary 2.3 (monotone hypotheses), and the L09 text that cites L11 Lemma 1.1 with Theorem 2.2 for x and x^2 (integrability of x - x^2). Numbers 1/8, 1/6 checked by hand (f(0)=0, f(1/2)=1/4, f(1)=0).",
 "e2-cards-L10": "Changed M2-c134, c143, c145, c146, c147 re-read against the L10 text: Theorem 1.2 (MVT, Assumption 2.1), Theorem 2.1 proof (MVT on each subinterval [x_(i-1), x_i]), Section 5 (closed-interval continuity; open-interval counterexample), Misconception 1 (integrability of f), Misconception 2 (G(x) = x/(1+x) + 5; G(1) = 11/2, G(1)-G(0) = 1/2), Misconception 3 (Example 2.2, non-polynomial). Removed M2-c429 (see e10 row). The MVT card M2-c418 is unchanged.",
 "e2-cards-L11": "Changed M2-c152, c161, c162, c163 re-read against the L11 text: Example 2.2 (boundary term 0 because v(1)=0 and u(0)=0), Example 2.3 (boundary term 1; 2*integral of x = 1, so 1/2), Misconception 1 (dropped boundary term forces the integral to 0), Misconception 2 and Theorem 3.1 with Example 3.2 (8/3 with limits 0 and 2; 1/3 with limits 0 and 1, lab part C), Misconception 3 (Theorem 2.1 lists integrability as a hypothesis; polynomials by Corollary 1.2).",
 "e2-cards-L12": "Changed M2-c169, c177, c178, c180 re-read against the L12 text: Theorem 2.2 (p >= 2, Assumption 2.1), Example 2.3 (p = 2: 1; p = 3: 1/2), Theorem 3.3 (p = 1 diverges), Misconception 1 (truncation error exactly 1/b), Misconception 3 (p > 0 belief fails; nothing for 0 < p < 1), Section 4 (p <= 0 not treated; non-integer powers not established). Arithmetic: 1/(p-1) at p = 2 and 3 gives 1 and 1/2.",
 "e2-cards-L18": "Changed M2-c265 is a front wording change only: 'F = (F_1, F_2, and so on up to F_m)' matches L18 Definition 2.1 ('F = (F_1, ..., F_m)', L18 text line 25). Back unchanged (byte-identical).",
 "e2-cards-L24": "Changed M2-c430 re-read against L24 Section 1 (text line 22): D+ and D- and D0 defined; the derivative exists => the central quotient converges to it, because D0 is the average of D+ and D- and both tend to f'(x) as h -> 0+. Identity checked: (D+ + D-)/2 = (f(x+h) - f(x-h))/(2h).",
 "e3-cards-whole-set-mechanical": "Whole-set mechanical checks on 395 cards at pin 2a805c83 (python this round): numeric tokens 0 missing (2855); exact duplicate fronts and backs 0; ids unique; all 24 lesson pages exist; grades and bases consistent; check_pages PASS (g1_check_pages.out). Semantic duplicates: row e10-cards-c412-duplicates-c065.",
 "e6-instances-50": "run_graders.py --unit M2 --seeds 0-49 -> PASS (g1_run_graders.out); instance.py is byte-identical to the base.",
 "e5-fragment-gate-set": "Gate set run this round: ledgers/M2/scripts/M2-e-r1/g1_run_gates.sh (check_pages, check_dag, check_projects, run_graders, run_labs, build_site --check, render_curriculum + git diff, fetch_data --check, verify_refs --offline, ruff, mypy, pytest labs, page_smoke M2) and the staged grader and mutant runs; all exit 0 (outputs g1_*.out).",
 "e9-delta-read": "Full read of this round's delta: git diff --name-only 95f3f8cb..2a805c83 over course/modules/M/M2 and tests/labs/M2 lists only course/modules/M/M2/cards.json (28 changed cards, 3 removed: M2-c417, c428, c429; none added; read per id, old vs new). Global delta (53 non-ledger files) read by name: no other M2 page, twin, grader or tool changed; plans/FINAL-ARCHITECT-RULINGS.md rulings 38-39 are E3-only.",
 "e10-cards-c412-duplicates-c065": "Re-verified from scratch at 2a805c83. The three semantic duplicates of the base row are gone: M2-c417 (Rolle restatement, duplicate of M2-c065) and M2-c429 (MVT restatement, duplicate of M2-c066) are removed, and M2-c428 (EVT restatement, near-duplicate of M2-c064) is removed with its content folded into M2-c064 (diff of cards.json). A python scan of all 395 fronts for Rolle, mean value, extreme value and Assumption 1.1 finds only statements (c064, c065, c066, c404), questions about the MVT's point (c072, c073) and applications or uses (c099, c134, c418). No card restates Rolle's or the MVT's statement a second time. Remaining near-overlap, recorded only: c134 and c418 both say the MVT is used on each subinterval of the proof of Theorem 2.1 (different questions); card style, LOW, not a ruling-26 kind.",
 "e10-cards-changed-c027-c047-c177-c352": "c177 re-read against the L12 text (Misconception 1: the truncation error of x^(-2) from 1 to b is exactly 1/b, positive at every finite b, reached only in the limit): agrees. c027, c047 and c352 are byte-identical to the base (per-id diff), so their base re-reads stand (carried): c027 (L03 Definition 1.1), c047 (L04 lab number 3.000001 = 3h + h^2 at h = 1e-6), c352 (L23 Misconception 1). Only c177 is re-read this round.",
 "e11-cards-deleted-c408-c411": "M2-c408 and M2-c411 are absent at 2a805c83 (python id check). The three cards removed in this delta: M2-c428's claim is carried by the new sentence of M2-c064; M2-c417 and M2-c429 restated the Rolle and MVT statements that M2-c065 (L06 Theorem 2.2) and M2-c066 (L06 Theorem 2.3) carry. Lesson L08 Theorem 1.2 and L10 Theorem 1.2 are cited results, not rows of those lessons' key-results tables (L08.html section 6; L10.html section 6), so no graded claim lost its card.",
 "e11-build-site-check": "build_site.py --check -> 'site data current: 6 outputs', exit 0 (g1_build_site_check.out).",
 "e7-L22-L24-lesson-numbers": "course/modules/M/M2/L22.html, L23.html and L24.html are byte-identical to 95f3f8cb (git diff empty), so the lab numbers in their prose are unchanged. The cards of L22-L24 changed only in M2-c430 (no numbers in it) and were scanned this round: every numeric token of all 395 cards occurs in its lesson text (python, 0 missing). Lab 1 outputs quoted by L23 and L24 cards re-checked against the printed twin outputs (see e2-cards-L23 and e2-cards-L24, carried).",
 "e11-curriculum-regeneration-out-of-slice": "render_curriculum.py -> 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)', then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json -> clean, exit 0 (g1_render_curriculum_check.out).",
}
V_ids = set(V)
for k in ("e2-mutants-existing",):
    assert k in base_rows

CARRY_PREFIX = ("Carried from round 1 (F2-M2-e.round1.json, pin 95f3f8cb): the subject is byte-identical since that pin "
                "(git diff 95f3f8cb..2a805c83 over the slice paths changes only course/modules/M/M2/cards.json, and in that file "
                "only the cards named under the e2-cards and e10/e11 rows; this row's cards and lesson are not among them): ")


COUNTS = {"L01": 18, "L02": 13, "L03": 14, "L04": 10, "L05": 14, "L06": 15, "L07": 24, "L08": 18, "L09": 19, "L10": 16,
          "L11": 15, "L12": 17, "L13": 23, "L14": 18, "L15": 21, "L16": 10, "L17": 14, "L18": 15, "L19": 13, "L20": 14,
          "L21": 16, "L22": 15, "L23": 24, "L24": 19}
def fix_location(loc):
    return re.sub(r"\((L\d\d): \d+ cards\)", lambda m: f"({m.group(1)}: {COUNTS[m.group(1)]} cards)", loc)

rows = []
for rid, br in base_rows.items():
    if rid in V:
        rows.append({"id": rid, "check": br["check"], "location": fix_location(br["location"]), "status": "PASS", "evidence": V[rid]})
    else:
        ev = br["evidence"]
        rows.append({"id": rid, "check": br["check"], "location": fix_location(br["location"]), "status": "PASS",
                     "evidence": CARRY_PREFIX + ev})
missing_v = [k for k in V if k not in base_rows]
assert not missing_v, missing_v

mutants = []
for line in open(f"{S}/g1_mutate_graders_M2.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+)\.py: (.*?) -> (.*)$", line.strip())
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 175, len(mutants)
base_mut_ids = {m["id"] for m in base["mutants"]}
assert base_mut_ids == {m["id"] for m in mutants}, "mutant id sets differ from base"

notes = [
 "Closing delta over slice e, base fragment ~/.fanout/frags/F2-M2-e.round1.json (pin 95f3f8cb), delta 95f3f8cb..2a805c83 (HEAD). Rulings 30 and 37 applied: every non-PASS base row (e10-cards-c412-duplicates-c065) re-verified from scratch; every row whose subject changed re-verified (cards of L06, L07, L08, L09, L10, L11, L12, L18, L24, the count and grades rows, the whole-set and delta-read rows, e11-cards-deleted); all other rows carried with the carry prefix. No new mutants written (ruling 37); the standing set (175) was re-run.",
 "Delta over slice paths: course/modules/M/M2/cards.json only (28 cards changed: c064, c096, c099, c102, c104, c107, c111, c112, c113, c114, c134, c143, c145, c146, c147, c152, c161, c162, c163, c169, c177, c178, c180, c265, c422, c423, c425, c430; 3 removed: c417, c428, c429). project.html, grader/, tests/labs/M2 and the M2 lesson pages are byte-identical to 95f3f8cb, so the project rows, the lab rows, the grader rows and the page rows are carried.",
 "Outcome of the base non-PASS row: the duplicate pairs (M2-c417/c065, M2-c429/c066, M2-c428/c064) are resolved by deletion and folding, so the row is PASS at this pin. No ruling-26 defect kind was found in the changed subjects: no false or unproved statement, no missing hypothesis, no wrong number (the arithmetic of c107, c422, c423, c430, c161, c169 and c177 was recomputed), no over-grade (c422 C -> T is backed by Proposition 2.3, graded T), no failing gate, no surviving mutant, no lab statement unsupported by the output.",
 "Observations (not ruling-26 kinds, not FAIL): (a) M2-c102 says 'Under Assumption 1.1' for Example 2.3, whose computation does not use the assumption (Theorem 2.1 does); harmless over-hypothesis. (b) M2-c064 now refers to Lesson 8 (a later lesson) from a Lesson 6 card; it is accurate (L08 Assumption 1.1 is the same statement, ungraded), but it is a forward reference in card text. (c) M2-c134 and M2-c418 overlap in content (MVT used on each subinterval of the proof of Theorem 2.1); different questions, card style. (d) The base note that rows cite 'L01: 16 cards, L08: 19 cards, L10: 15 cards' is stale: the counts at pin 2a805c83 are L01 18, L08 18, L10 16 (python count); the 395 total is correct.",
 "Gates re-run at 2a805c83 (ledgers/M2/scripts/M2-e-r1/g1_*.out): check_pages, check_dag, check_projects, run_graders (50 seeds), run_labs (27/27), build_site --check, render_curriculum + clean git diff, fetch_data --check, verify_refs --offline (560 entries), ruff check and format, mypy on labs and mypy --strict on the staged grader, pytest for the M2 lab tests, page_smoke M2, the staged grader (89 collected and passed for seeds 0, 7, 23), and mutate_graders M2 (175/175 killed). All exit 0. Two earlier attempts to collect the grader inside the repo failed because sensitivity_engine.py is staged by run_graders; those outputs were removed and replaced by g1_grader_staged.out.",
 "Not checked: a line-by-line reading of all 24 lesson pages (only the changed lesson text and the cards that cite it; the unchanged lesson pages are byte-identical); the live verify_refs run (no reference record changed); the blind rubric scorers for M2 (none exists in ~/.fanout/blind/, so the base calibration rows are carried); the alternative-implementation runs (grader unchanged; base alternatives carried); the L08/L10/L11/L12 lab twins were not re-executed individually (run_labs M2 covers all 27, and the twins are byte-identical).",
]
freshness = [
 "The base fragment's 'base' field names ccaeeaf4 (its round-11 pin) while its own pin is 95f3f8cb; this round's base is 95f3f8cb as the task states. Files cited by the base as round-11 artefacts (ledgers/M2/mutants/w11e_01..04, ledgers/M2/scripts/M2-e-r11) are present at 2a805c83 and are byte-identical since 95f3f8cb (git diff)."
]
frag = {
 "unit": "M2",
 "slice": "e",
 "round": 1,
 "verifier": "Haiku 5.5 independent verifier (round 1, slice e, closing delta; rulings 30 and 37)",
 "pin": "2a805c83",
 "base": "95f3f8cb (base fragment ~/.fanout/frags/F2-M2-e.round1.json, its pin)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-M2-e",
 "scratch": "/tmp/m2e_r1b (lesson text extraction, card scans, staged grader runs)",
 "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": freshness,
 "notes": notes,
 "summary": f"Slice e closing delta round 1 (pin 2a805c83, base 95f3f8cb): {len(rows)} rows, all PASS. The base FAIL row e10-cards-c412-duplicates-c065 is fixed by deletion (M2-c417, c428, c429) and re-verified PASS. Mutants 175/175 killed (standing set, re-run). Gates: all exit 0.",
}
problems = ledger.validate(frag, "M2-e")
print("validate:", problems)
print("rows", len(rows), "PASS", sum(r["status"] == "PASS" for r in rows), "verified-this-round", len(V), "carried", len(rows) - len(V))
json.dump(frag, open(f"{CHK}/ledgers/M2/M2-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written")
