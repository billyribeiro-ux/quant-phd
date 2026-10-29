import json, sys
sys.path.insert(0, "tools")
import ledger

PREV = "44f1eb6a417ce687a9b88c7ee917e72566b29892"
SLICE_FILES = ("course/modules/M/M4/L05.html, L06.html, L07.html, tests/labs/M4/lab-M4-L05-1.py, lab-M4-L06-1.py, lab-M4-L07-1.py, notation/notation.json")
def carry(files, text):
    return f"Carried from round 6 ({files} byte-identical since the previous pin {PREV[:7]}): {text}"

rows = []
def add(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)

add("B6-01", "Pin and slice inventory", "git rev-parse HEAD; course/modules/M/M4/L05-L07 pages; tests/labs/M4/lab-M4-L05/06/07-1.py", "PASS",
    "git rev-parse HEAD = 7aa909e95b757b1abf7b75186d5fa1ed7d1945a4. git diff 44f1eb6 HEAD: L05.html, L06.html, L07.html, lab-M4-L05-1.py, lab-M4-L06-1.py, lab-M4-L07-1.py, notation/notation.json all reported identical (git diff --quiet). Delta inside M4 touches only L02, L03, L10, cards.json, project.html, project grader, lab-M4-L10-1.py.")
add("B6-02", "check_pages for unit M4", "tools/check_pages.py --unit M4", "PASS",
    "Re-run this round; log ledgers/M4/scripts/M4-b-r7/logs/check_pages.out: 'check_pages M4: PASS', exit 0.")
add("B6-03", "Concept DAG check for unit M4", "tools/check_dag.py --unit M4", "PASS",
    "Re-run this round; logs/check_dag.out: 'check_dag M4: PASS', exit 0 (L10 changed, so re-run rather than carried).")
add("B6-04", "check_projects for unit M4", "tools/check_projects.py --unit M4", "PASS",
    "Re-run this round; logs/check_projects.out: 'check_projects M4: PASS', exit 0.")
add("B6-05", "run_labs for unit M4", "tools/run_labs.py --unit M4", "PASS",
    "Re-run this round; logs/run_labs.out: 'run_labs M4: PASS (13/13)', exit 0.")
add("B6-06", "page_smoke for L05 L06 L07 alone", "tools/page_smoke.py --unit M4 --pages L05 L06 L07", "PASS",
    "Re-run this round; logs/smoke.out: page_smoke L05, L06, L07 PASS; 'page_smoke M4: PASS', exit 0.")
add("B6-07", "Lab page code equals twin; twin under python -I -W error; expected equals stdout", "course/modules/M/M4/L05.html, L06.html, L07.html; tests/labs/M4/lab-M4-L05-1.py, L06, L07; ledgers/M4/scripts/M4-b-r7/labcheck2_r7.py",
    "PASS", "Re-run this round: each twin exit 0 with empty stderr under python -I -W error (logs/twin_L0x.err 0 bytes); each page has one code block equal to its twin and one expected block equal to the twin stdout (labcheck2_r7.py: True for L05, L06, L07).")
add("B6-08", "ruff, ruff format, mypy strict on the three lab twins", "tests/labs/M4/lab-M4-L05-1.py, L06, L07", "PASS",
    "Re-run this round: 'All checks passed!'; '3 files already formatted'; mypy --no-incremental: 'Success: no issues found in 3 source files'.")
add("B6-09", "L05 prose numbers against unrounded values", "course/modules/M/M4/L05.html interpretation paragraphs and E1-E3 solutions", "PASS",
    carry("L05.html", "round-6 recheck_numbers.py output; this round logs/run_labs and twin_L05.out reproduce every printed value (0.00002223, 0.00016257, 0.592936, -0.007064, 4.817275 max/min, 0.0004 entries)."))
add("B6-10", "L05 mathematics, Props 1.1-1.6, Example 1.7, Remark 1.8, Props 2.3-2.4, problems and quiz", "course/modules/M/M4/L05.html sections 1-5 and quiz", "PASS",
    carry("L05.html", "round-6 hand re-derivation. Re-checked this round for the card-cited items: Var(Y)=2/9 (Remark 1.8), |[[1,2],[2,1]]| bound 4<=1 false (Prop 2.4), Cov(100X,100Y)=10^4 Cov (Prop 1.2)."))
add("B6-11", "L05 Example 2.5 states its assumption and does not claim it is proved", "course/modules/M/M4/L05.html line 159-162 (Example 2.5 block)", "PASS",
    carry("L05.html", "Raw HTML at L05.html line 160 reads 'The variables Z1 and Z2 are not finitely valued, so this example uses the rules of Proposition 1.1 for them without proving them here. It assumes that those rules hold, with Var(Zi)=1 and Cov(Z1,Z2)=0.' (re-read this round). The grade issue is recorded on the cards row B6-22."))
add("B6-12", "L06 prose numbers against unrounded values", "course/modules/M/M4/L06.html Part A/B interpretation and solutions", "PASS",
    carry("L06.html", "round-6 recheck. Re-read this round: twin_L06.out prints sample_variance 1.669114 (nu=5), 1.240325 (nu=10), relative_error 0.001469 and -0.007740; twin code (lab-M4-L06-1.py lines 52-56) computes the relative error from unrounded variance, as stated."))
add("B6-13", "L06 Props 1.2-1.5 proofs", "course/modules/M/M4/L06.html Section 1", "PASS",
    carry("L06.html", "round-6 proofs check; this round re-read Prop 1.5 proof (L06.html lines 103-116)."))
add("B6-14", "L06 Prop 1.5 second claim (E[X]=mu, Var(X)=sigma^2 for X ~ N(mu, sigma^2)) proved", "course/modules/M/M4/L06.html lines 103-115 (Proposition 1.5 and its Proof)", "PASS",
    "Re-verified from scratch (round 6 FAIL not reproduced). The Proof block at L06.html lines 108-115 is one paragraph that continues after the display: 'For X = mu + sigma Z, which has the law N(mu, sigma^2) by Proposition 1.4, linearity gives E[X] = mu + sigma E[Z] = mu, and Var(X) = E[(sigma Z)^2] = sigma^2 E[Z^2] = sigma^2.' The round-6 reader stopped at the display. The step is proved; no fix needed. Also checked the numeric bound sqrt(2) e^(-1/2) = 0.85788 < 0.86 and the integration by parts boundary term.")
add("B6-15", "L06 Lemma 2.3, Props 2.4, 2.6", "course/modules/M/M4/L06.html Section 2", "PASS",
    carry("L06.html", "round-6 proof check. Subject unchanged this round."))
add("B6-16", "L06 Remark 2.7, misconceptions, problems, quiz values", "course/modules/M/M4/L06.html sections 3-7", "PASS",
    carry("L06.html", "round-6 values check (5/3, 0.7978846, 1/2, 5); quiz value 1/(nu-2) = 1/2 at nu=4 re-read at L06.txt line 276."))
add("B6-17", "L07 Defs 1.1, Props 1.2-1.4", "course/modules/M/M4/L07.html Section 1", "PASS",
    carry("L07.html", "round-6 proof check; subject unchanged."))
add("B6-18", "L07 Props 2.3-2.5 and cosine modulus formula", "course/modules/M/M4/L07.html Section 2", "PASS",
    carry("L07.html", "round-6 check; the two-point modulus formula re-derived this round: |p e^{ita}+(1-p)e^{itb}|^2 = p^2+(1-p)^2+2p(1-p)cos(t(a-b)) (card M4-c107 agrees)."))
add("B6-19", "L07 prose numbers against unrounded values", "course/modules/M/M4/L07.html Part A/B/C interpretation and solutions", "PASS",
    carry("L07.html", "Printed values re-checked this round against twin_L07.out: abs difference 7.11e-13 at t=2, closed form 244.69193226; cos mean -0.062124 vs real part -0.062110."))
add("B6-20", "L07 problem and quiz values", "course/modules/M/M4/L07.html sections 5 and 7", "PASS",
    carry("L07.html", "round-6 check; subject unchanged."))
add("B6-21", "Lab output and lesson text agree (L05, L06, L07 Lab 1)", "course/modules/M/M4/L05.html, L06.html, L07.html lab interpretation", "PASS",
    carry("L05.html, L06.html, L07.html and their twins", "the printed lines in twin_L05.out, twin_L06.out, twin_L07.out (this round) match the numbers quoted in the lesson interpretation paragraphs."))
add("B6-22", "Cards for L05-L07 (49 cards): numbers appear in lesson, grade matches lesson, no duplicates", "course/modules/M/M4/cards.json entries with lesson L05, L06, L07 (ids M4-c067..c113, M4-c174, M4-c191)",
    "FAIL",
    "Re-verified from scratch (cards.json changed since round 6: 36 hunks touch L05-L07 cards, plus new M4-c191). Checked: 49 cards, no duplicate ids or fronts; every cited Definition/Proposition/Remark/Example/Problem/Assumption label exists in L05-L07 text (cardrefs_r7.py); every number on the cards appears in its lesson; lab-cited numbers match this round's twin outputs (c082 0.00002223/0.00016257, c083 0.592936/-0.007064, c098 1.669114 and 0.001469 from unrounded values, c112 7.11e-13 and 244.69193226, c113 -0.062124/-0.062110); the mathematics of c069-c111, c174 re-derived. DEFECT: M4-c191 (L05, grade T): 'What covariance matrix does the two-asset construction ... have?' It rests on Var(Z_i)=1 and Cov(Z1,Z2)=0, which the lesson does not prove (L05.html line 160: 'without proving them here. It assumes that those rules hold'), and the lesson's own closing paragraph (L05.html line 509) says 'Example 2.5 is a computation under the assumption that the example states'. A card graded T for a conditional computation contradicts the lesson's grading rule (rule 9 and line 509).",
    fix="Change M4-c191 grade from \"T\" to \"C\" with basis \"Example 2.5, under its stated assumption Var(Z_i)=1, Cov(Z1,Z2)=0\", or give the assumption a numbered Assumption in L05 and cite it. Re-run check_pages and check_dag after the edit.")
add("B6-23", "Cross-references into L04 from L05 and L07", "course/modules/M/M4/L05.html lines 22, 50, 56; L07.html Prop 1.5 reference in P3", "PASS",
    carry("L04.html, L05.html, L07.html", "the cited L04 subjects are byte-identical; L04 references re-read in L05.txt line 22 and L07.txt P3 (line 277)."))
add("B6-24", "Cross-reference from L06 to L10 (Student-t(3) fourth moment)", "course/modules/M/M4/L06.html line 284; course/modules/M/M4/L10.html Proposition 2.3 (line 150) and Remark 2.2 (line 145)", "PASS",
    "Re-verified because L10.html changed (hunks at Remark 1.6, Assumption 3 and Lesson-9 references). L10.html still states 'Proposition 2.3 (the fourth moment of the Student-t(3) law is infinite)' at line 150, under 'Assumption 1 (density of the Student-t law with three degrees of freedom)' at line 65; Remark 2.2 (the Student-t(3) variance) at line 145. L06.html line 284 cites 'L10, Proposition 2.3' and 'L10's Assumption 1' correctly.")
add("B6-25", "Notation of L05-L07 against notation/notation.json", "notation/notation.json; L05-L07 visible text", "PASS",
    carry("notation/notation.json, L05.html, L06.html, L07.html", "subject identical; no new symbol introduced in the slice."))
add("B6-26", "Process words and builder/verifier vocabulary in learner text", "course/modules/M/M4/L05.html, L06.html, L07.html", "PASS",
    carry("L05.html, L06.html, L07.html", "subject identical."))
add("B6-27", "Hours: 9 study hours per slice lesson", "course/modules/M/M4/L05-L07 headers; plans/M4-build-plan.md", "PASS",
    carry("L05.html, L06.html, L07.html and plans/M4-build-plan.md", "plan unchanged in the delta (git diff 44f1eb6 HEAD -- plans/M4* empty)."))
add("B6-28", "Registry verification offline", "tools/verify_refs.py --offline", "PASS",
    "Re-run this round: 'offline integrity: 560 entries, 0 problems'.")
add("B6-29", "Project grader mutation status for unit M4 (grader changed since round 6)", "tools/mutate_graders.py --unit M4; course/modules/M/M4/grader/test_project.py; course/modules/M/M4/project.html", "FAIL",
    "Re-run this round (logs/mutate_M4.out): 'mutate_graders M4: FAIL (82/86 killed)'. Survivors: m11_loss_sign_flipped.py (loss sign reversed); m17_student_t_second_seed.py (Student-t uses seed+1); n02_one_chi_square_per_asset.py (one chi-square per asset); v4_m02_matched_factor_skipped_for_small_nu.py (matched factor only for nu>4). Each violates a sentence on the project page: the lab code on project.html states 'The loss is minus the position-weighted return' (step 4 comment) and 'from the same seed' for both families (line 85 of the embedded code); it states 'W is the chi-square draw' (single W, lab code lines 62-63); and the matched factor (nu-2)/nu is stated for nu greater than 2 (matched_factor docstring, lab code line 161) with instance nu from 3 to 8 (project.html line 200). The grader does not kill these. Scope: project grader, not lesson slice b; reported because B6-29 was a round-6 row.",
    fix="Add autograder tests that fail each survivor: a loss-sign check against a seeded reference loss quantile; a same-seed check across families; a shared-W check with two assets; a Student-t variance test at nu=3 and nu=4. Then re-run tools/mutate_graders.py --unit M4 until 86/86 killed (or each survivor is shown to violate no stated behaviour).")
add("B7-30", "pytest tests/test_labs.py for M4 cases; curriculum and site currency", "tests/test_labs.py -k M4; tools/render_curriculum.py; tools/build_site.py --check", "PASS",
    "Re-run this round: M4 cases 13 passed (pytest -k M4). Curriculum regenerated and git diff --exit-code empty; 'site data current: 6 outputs'. Out of scope and not an M4 finding: test_labs.py fails for unit E3 cases ('missing twin tests/labs/E3/lab-E3-L05-1.py'; tests/labs/E3 absent at 7aa909e).")

frag = {
    "unit": "M4",
    "slice": "b",
    "round": 7,
    "verifier": "Haiku verifier, independent of the builders (verifyB7-M4-b)",
    "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
    "base": "44f1eb6a417ce687a9b88c7ee917e72566b29892 (round-6 pin, from /Users/billyribeiro/.fanout/frags/B-M4-b.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M4-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB7-M4-b/ledgers/M4/scripts/M4-b-r7/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "cards.json changed in the delta (L05-L07 card hunks and M4-c191); cards row re-verified (B6-22)",
        "L10.html changed; L06-to-L10 cross-reference re-verified (B6-24)",
        "project grader, project.html and lab-M4-L10-1.py changed; B6-29 re-run",
    ],
    "notes": (
        "Delta: L05.html, L06.html, L07.html, their three twins, notation/notation.json and L04.html are byte-identical to the round-6 pin, so the lesson rows B6-09..B6-21, B6-23, B6-25..B6-27 are carried, not re-derived line by line this round. "
        "Round-6 row B6-14 (FAIL) was not reproduced: the Proposition 1.5 proof continues after its display and proves E[X]=mu and Var(X)=sigma^2 for X = mu + sigma Z (L06.html lines 108-115). "
        "Mutants: this is a lesson slice, so no new grader mutants were written; the existing 86 M4 grader mutants were re-run (mutate_graders). "
        "Not checked: the full re-read of L05-L07 text this round (carried by byte-identity; the round-6 reader read every line); L08-L10 prose beyond the cross-references the slice uses; alternative correct grader implementations (project scope, not this slice); live browser rendering beyond page_smoke."
    ),
    "summary": "Slice b (L05-L07 and twins), round 7: 31 rows; FAIL 2 (B6-22 card M4-c191 graded T for a conditional computation; B6-29 four surviving project-grader mutants that violate stated behaviour). B6-14 from round 6 is PASS on re-verification. All gates (check_pages, check_dag, check_projects, run_labs 13/13, page_smoke L05-L07, twins, ruff, mypy, verify_refs) PASS.",
}

problems = ledger.validate(frag, "M4-b")
print("validate:", problems)
out = "ledgers/M4/M4-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, len(rows), "rows")
