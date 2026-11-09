"""Writes the round-4 fragment for M7 slice c (L07, L08, twins, cards). Evidence strings cite scripts under ledgers/M7/scripts/M7-c-r4/."""
import json
from pathlib import Path

S = "ledgers/M7/scripts/M7-c-r4/"
CARRY3 = "Carried from round 3 (tests/labs/M7/* byte-identical since the previous pin 8196077d, verified by git diff --quiet): "
CARRY3_HUB = "Carried from round 3 (course/modules/M/M7/index.html byte-identical since the previous pin 8196077d, verified by git diff --quiet): "

rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("M7c-r1-cmd-check_pages", "tools/check_pages.py --unit M7", "index, L01-L08, project, cards", "PASS",
    f"Run at edbb7aa8: `.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 ({S}check_pages_output.txt).")
row("M7c-r1-cmd-check_dag", "tools/check_dag.py --unit M7", "DAG of M7", "PASS",
    f"Run at edbb7aa8 -> 'check_dag M7: PASS', exit 0 ({S}check_dag_output.txt).")
row("M7c-r1-cmd-run_labs-L07", "tools/run_labs.py --unit M7 --page L07", "course/modules/M/M7/L07.html, lab-M7-L07-1", "PASS",
    f"Run at edbb7aa8 -> 'run_labs M7: PASS (1/1)', exit 0 ({S}run_labs_L07_output.txt).")
row("M7c-r1-cmd-run_labs-L08", "tools/run_labs.py --unit M7 --page L08", "course/modules/M/M7/L08.html, lab-M7-L08-1", "PASS",
    f"Run at edbb7aa8 -> 'run_labs M7: PASS (1/1)', exit 0 ({S}run_labs_L08_output.txt).")
row("M7c-r1-twins-alone-python-I-W-error", "each twin run alone under python -I -W error", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
    f"{S}extract_compare.py ran each twin as `python -I -W error <twin>`: exit 0 for both, stderr 0 bytes; stdout saved as {S}out/L07-twin.stdout and L08-twin.stdout ({S}extract_compare_output.txt).")
row("M7c-r1-page-code-equals-twin", "HTML-unescaped data-run code block vs twin source", "course/modules/M/M7/L07.html:150-298, L08.html:150-284 vs twins", "PASS",
    f"{S}extract_compare_output.txt: page code == twin after rstrip('\\n') for L07 and L08. Exact string equality is False only by the single trailing newline, which tools/run_labs.py and tools/embed_labs.py strip by convention.")
row("M7c-r1-expected-equals-output", "page pre.expected block vs twin stdout", "course/modules/M/M7/L07.html:299-318, L08.html:285-310", "PASS",
    f"{S}extract_compare_output.txt: expected.rstrip == twin stdout.rstrip for both pages; the page code run standalone under python -I -W error prints the identical stdout.")
row("M7c-r1-cmd-ruff", "ruff check and ruff format --check (twins and repo)", "tests/labs/M7 and repo", "PASS",
    f"{S}ruff_output.txt: twins 'All checks passed!' and '2 files already formatted'. {S}ruff_check_repo_output.txt: 'All checks passed!', exit 0. {S}ruff_format_repo_output.txt: '553 files already formatted', exit 0.")
row("M7c-r1-cmd-mypy-strict", "mypy --strict on the twins; mypy --no-incremental on the repo", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
    f"{S}mypy_twins_output.txt: 'Success: no issues found in 2 source files'. {S}mypy_repo_output.txt: 'Success: no issues found in 385 source files', exit 0.")
row("M7c-r1-cmd-pytest-lab-cases", "pytest lab cases for L07 and L08; collect count", "tests/test_labs.py", "PASS",
    f"{S}pytest_labs_output.txt: `pytest -q tests/test_labs.py -k \"lab-M7-L07-1 or lab-M7-L08-1\"` -> '..' exit 0. {S}pytest_collect_M7_output.txt: 11 M7 cases collected.")
row("M7c-r1-cmd-page_smoke", "tools/page_smoke.py --unit M7 --pages L07 and --pages L08, each run alone", "course/modules/M/M7/L07.html, L08.html", "PASS",
    f"{S}page_smoke_L07_output.txt: 'page_smoke modules/M/M7/L07.html: PASS', lab 0.0 s, exit 0. {S}page_smoke_L08_output.txt: 'page_smoke modules/M/M7/L08.html: PASS', lab 0.0 s, exit 0.")
row("M7c-r1-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"{S}verify_refs_offline_output.txt: 'offline integrity: 560 entries, 0 problems', exit 0. The two pages cite no registry key, so the live run is not needed for this slice.")
row("M7c-r1-numbers-L07-prose", "every number in L07 prose, lab claims, quiz and problems re-derived", "L07.html:52, 56, 149, 299-318, 319, 342-350, 415-429, 490-548", "PASS",
    f"{S}independent_numbers.py (no lab code imported) -> {S}independent_numbers_output.txt: V_t(W) table 240/220/200/130/4 at W=400; 70 feasible sequences from (0,400) = C(8,4); greedy total 130, optimum 240; greedy tails optimal; differences 20, 20, 70, 126; 130/240 = 13/24 = 0.5417; V_0(400)-V_3(400) = 110. {S}small_examples.py -> {S}small_examples_output.txt: M1 values 5, 3, 10; M3 totals 6, 9, 10. All match the page.")
row("M7c-r1-numbers-L08-prose", "every number in L08 prose, lab claims, quiz and problems re-derived with exact fractions", "L08.html:52, 149, 286-310, 311, 353, 360, 367, 403, 410, 417, 442, 480, 514-531", "PASS",
    f"{S}independent_numbers_output.txt: Part A values exact (at most 5 decimal places, so the 6-place display is exact); policy lines; ties 0; brute force 378 plans and match True; changes exact 6, 18/5, 137/50, 1233/500, 11097/5000, 99873/50000 with display 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746; ratios 3/5, 137/180, 9/10, 9/10, 9/10; V_0(0)-V_1(0) = 0.590490; V_4(0)-V_5(0) = 3.6. {S}small_examples_output.txt: M2 values 2, 3, 7/2, 9/2; M3 total 7/2; negative-discount totals 0, -1, 1, 0 with V_0 = 1, V_1 = 1, U_0 = 0; Remark 1.5 identity; R3 distance/change = n+1. All match the page.")
row("M7c-r1-math-L07-theorems", "Definitions 1.1-1.4, Remark 1.3, Theorems 2.1-2.3, Corollary 2.4, Remark 2.5: read every proof step and re-derive", "L07.html:58-145, 322-325", "PASS",
    f"Read each proof line by line (L07.html:58-145, 322-325). Theorem 2.1 split J_t(a,q)=r+J_{{t+1}}(q) and downward induction; Theorem 2.2 splice p' with Sigma cancellation; Theorem 2.3 chain of two inequalities; Corollary 2.4 induction on H-t. Remark 1.3 supremum 1 with no attaining plan ({S}small_examples_output.txt: finite grids approach 1); Remark 2.5 V_1(y)=0, V_0(x)=1, J((a,c))=0 ({S}small_examples_output.txt). Notation: local H, B, J, V, S, A, f, r, p, q, Sigma; no registered symbol reused.")
row("M7c-r1-math-L08-theorems", "Definitions 1.1-2.1, Theorems 1.3-1.4, Remark 1.5, Lemma 2.2, Proposition 2.3, Remark 2.4: every hypothesis and every case", "L08.html:56, 60, 124-129, 134-139, 457", "FAIL",
    "[BLOCKING: missing hypothesis, undefined horizon-0 case] L07.html:56 fixes 'the horizon H is a whole number with H \\ge 1' and L08.html:56 inherits that Definition 1.1 with no lift. Lemma 2.2 (L08.html:124) states the identity for 0 \\le t \\le H, so its t = H instance is V^{(H)}_H = V^{(0)}_0, a horizon-0 problem. Proposition 2.3 (L08.html:134) quantifies over every whole number n \\ge 0 and asserts W^{(0)}_0 = U^0; its proof (L08.html:139) starts 'For n = 0, the only plan is the empty plan'. No sentence in L07 or L08 defines a horizon-0 problem or allows H = 0, so W^{(0)}_0 and the t = H case are not defined by the page. The statement is true once H = 0 is admitted (the only plan is the empty plan, so the value is the terminal reward), and the other cases (Theorems 1.3, 1.4, Remark 1.5, Lemma 2.2 for t < H, Proposition 2.3 for n \\ge 1) are checked: small_examples_output.txt and the proofs read in full. The same gap reaches the key-results row L08.html:457 at H = 1 (horizon H-1 = 0).",
    "Add one sentence in L08 section 1, after L08.html:56: 'In this lesson H \\ge 0 is allowed: a problem with H = 0 has only the empty plan, so its value at time 0 is its terminal reward B.' Nothing else changes. Re-run check_pages and page_smoke for L08.")
row("M7c-r1-math-problem-sets-L07", "problems M1-M3, P1-P3, E1-E3, R1-R3 (L07)", "L07.html:361-456", "FAIL",
    f"M1-M3 and P1-P3, E1-E3, R2, R3 checked (values and plans in {S}small_examples_output.txt; E3 C(8,4)=70; E1 differences; E2 13/24). [LOW: wording, presentation] R1 (L07.html:437-441) asks 'what Theorem 2.1 then says' when the maximum fails to exist; the worked solution (L07.html:440) explains why a supremum-defined value is not covered and why Theorem 2.2 has no optimal plan, but never says what Theorem 2.1 asserts in that case. Not a false claim.",
    "Rewrite the R1 solution (L07.html:440) to state the conclusion for Theorem 2.1 directly: its maximum is over a set with no maximum, so the formula of Theorem 2.1 is not established on the infinite-action problem, and the page's proof uses finiteness at each max. Keep the grade and the rest of the solution.")
row("M7c-r1-math-problem-sets-L08", "problems M1-M3, P1-P3, E1-E3, R1-R3 (L08)", "L08.html:349-446", "PASS",
    f"M1 (V_5 = 6,4,1; V_4(0) = 9.6 and repair 1.4), M2 (V_1(x)=2, V_1(y)=3, V_0(x)=3.5, V_0(y)=4.5), M3 (3.5), P1 (unique solution for H=1), P2 (identical totals), P3 (c = B = 0, V_0 = 1), E1-E3 (0.590490; 0.6/0.7611/0.9; 378), R1 (sign step), R2 (sum over sequences), R3 (distance/change = n+1) checked by {S}independent_numbers.py and {S}small_examples.py outputs.")
row("M7c-r1-lab-L07-claims", "every printed-claim sentence in the L07 lab text and interpretation", "L07.html:149, 161-165, 299-318, 319, 342-350", "PASS",
    f"Checked against the twin code (lines 262-297) and the expected block: Part B 20 pairs (4 times x 5 wealth states); Part C tail lines 286-295 and greedy tails 292-294; 'optimal_plan_every_tail_optimal True'; 'greedy_plan_optimal False'; the 70 count; 'does not show that the recursion is correct for other problems' is a limit statement, consistent with the code. No printed claim overreaches.")
row("M7c-r1-lab-L08-claims", "every printed-claim sentence in the L08 lab text and interpretation", "L08.html:149, 158-164, 286-310, 311", "PASS",
    f"Checked against the twin (lines 244-281) and expected block: 'no tie' (tied_pairs_t0_to_5 0; ties counted over t=0..5); 18 pairs (6 times x 3 states, loop lines 264-268); 378 enumerated sequences; policy t0-t3 repair and t4-t5 run for state 2; Part C changes for n=0..5; iterate_equals check over n=0..6 (line 280). 'does not show that the iteration converges' is a limit statement consistent with the code.")
row("M7c-r1-lab-L07-check-probe", "student-error probe of the L07 twin (labs are demonstrations; mutation testing applies to project graders only, ruling 9 and the rulings file)", "tests/labs/M7/lab-M7-L07-1.py", "PASS",
    CARRY3 + "round-3 probe (ledgers/M7/scripts/M7-c-r3/lab_probe.py). No lesson sentence claims the lab detects a bequest-free or tail-check error, so the two identical-output survivors are not findings.")
row("M7c-r1-lab-L08-check-probe", "student-error probe of the L08 twin", "tests/labs/M7/lab-M7-L08-1.py", "PASS",
    CARRY3 + "round-3 probe output; no lesson sentence claims the lab detects a tie-breaking or start-function error beyond what Part A and Part C print (L08.html:311, Misconception 1 at L08.html:329-332 says the lab starts only from U^0 = 0).")
row("M7c-r1-lab-seeded-no-network", "no randomness, no network, SIMULATED label", "tests/labs/M7/lab-M7-L07-1.py:3, lab-M7-L08-1.py:3; L07.html:149; L08.html:149", "PASS",
    f"grep over both twins for random, socket, urllib, requests, open(, subprocess, os: no hits (only the docstring phrase 'uses no random draws'). SIMULATED label present on both pages (L07.html:149, L08.html:149) and in each twin docstring.")
row("M7c-r1-grades-L07", "grade audit, L07", "L07.html:87, 109, 124, 138, 466-470", "PASS",
    "Theorem 2.1 (L07.html:87), 2.2 (:109), 2.3 (:124) and Corollary 2.4 (:138) are graded T and each has a complete proof on the page (re-read). Key-results rows 466-470 all T and match. No lab-read value is graded T on the page (the lab-read values in Misconceptions carry no T; the matching cards are C, rows M7c-r1-cards-L07-lab-and-misconceptions).")
row("M7c-r1-grades-L08", "grade audit, L08", "L08.html:77, 91, 122-123, 133, 454-458", "PASS",
    "Theorem 1.3 (L08.html:77), 1.4 (:91), Lemma 2.2 (:122-123), Proposition 2.3 (:133) graded T with complete proofs on the page; key-results rows 454-458 all T and match. Lab-read values are not graded T.")
row("M7c-r1-dag-concept-links", "concept links and definitions vs check_dag and the prerequisite closure", "L07.html:38-39, 79; L08.html:38-39, 69; course/concepts.html", "PASS",
    "tools/check_dag.py --unit M7 PASS. principle-of-optimality defined once (L07.html:79, def-principle-of-optimality); bellman-equation defined once (L08.html:69, def-bellman-equation); no other M7 page defines either (grep over course/modules). mathematical-induction link resolves to course/concepts.html#mathematical-induction. curriculum/01-foundations.yaml M7 introduces both concepts.")
row("M7c-r1-forward-reference-bellman", "forward mention of the Bellman equation (L08) before L08 defines it", "L07.html:52, 84", "PASS",
    "L07.html:52 and :84 name the recursion 'the Bellman equation' with an explicit pointer to L08 Definition 1.2; the term is not used as a step in any L07 proof. Acceptable under BUILDER_RULES 1.10 as a labelled forward pointer.")
row("M7c-r1-policy-term-forward", "forward use of 'policy' before its definition in L08 §3", "L08.html:311, 321", "PASS",
    "L08.html:311 uses 'policy' with the explicit pointer 'defined under Ties in §3'; the definition is at L08.html:321. Explicit forward pointer, not a defect.")
row("M7c-r1-notation", "notation registry collisions (notation/notation.json)", "L07.html and L08.html math", "PASS",
    f"Grep for LaTeX commands on both pages: \\R used (L07.html:56, L08.html:111) as required by ruling 1; no \\mathbb anywhere. No registered program-wide symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}) appears. Letters beta, B, U, V, W, C, H, J, Sigma, G are local and defined in each lesson (beta at L08.html:56; G at L08.html:115), which the registry allows. \\mathcal{{G}} is raw LaTeX for that local operator, not a registered macro collision.")
row("M7c-r1-banned-process-words", "BUILDER_RULES 1.3-1.4 phrases and process words", "L07.html, L08.html, slice cards", "PASS",
    "grep -i over both pages and the 40 slice cards for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly, builder, verifier, ruling, architect, placeholder, pending: no hits. The ellipses are sequence notation (a_t, ..., a_{H-1}), not omitted content.")
row("M7c-r1-scope-words", "scope words (only, all, always, every, any, same, exactly) need a computation or proof", "L07.html, L08.html", "PASS",
    "Each scope word traced: 'every instance of Definition 1.1' is covered by the proofs (finite sets); 'exactly one solution' (L08.html:376-378 P1) is proved; 'the only plan' statements follow from the definitions; 'no tie' is a counted output (tied_pairs 0). No unsupported universal.")
row("M7c-r1-attribution", "attribution: nothing cited from memory", "L07.html:555, L08.html:538; cards", "PASS",
    "Both pages state that they cite no outside source (L07.html:555, L08.html:538) and no registry key appears; the curriculum's two sources (boyd2004convex, stokey1989recursive) are not cited or characterised here. The 40 slice cards make no bibliographic claim.")
row("M7c-r1-structure-counts", "template sections, counts, quiz and problem minimums", "L07.html:52, 337-353, 355-458, 476-551; L08.html:52, 325-341, 343-446, 464-534", "PASS",
    "check_pages M7 PASS. L07: 3 definitions and 3 remarks in sections 1-2 (Definitions 1.1, 1.2, 1.4; Remarks 1.3, 2.5), 3 misconceptions, problem set in four tiers (M1-M3, P1-P3, E1-E3, R1-R3), 10 quiz items. L08: 2 definitions plus Bellman operator (Definitions 1.1, 1.2, 2.1), 2 remarks plus Remark 2.4, 3 misconceptions, problem set in four tiers, 9 quiz items. Section order matches the other merged lessons.")
row("M7c-r1-hours", "hours arithmetic: lesson declared hours, hub card hours, hub split", "L07.html:2, 35; L08.html:2, 35; index.html:29, 141, 149-150", "PASS",
    "L07 data-hours 9 (L07.html:2) = hub card 'L07 · 9 h' (index.html:149). L08 data-hours 10 (L08.html:2) = hub card 'L08 · 10 h' (index.html:150). Lessons: 9+9+10+10+10+10+9+10 = 77 = data-hours-lessons (index.html:29); 77 + 33 = 110 = hub total. Hub prose at index.html:141 agrees.")
row("M7c-r1-B2-infinite-horizon", "infinite-horizon result is not stated", "L08.html:52, 144, 317, 538", "PASS",
    "L08.html:52 and :317 say the infinite-horizon case is not treated; Remark 2.4 (:144) and Problem R3 (:439-443) concern finite-horizon iterates only; no infinite-horizon claim appears on either page.")
row("M7c-r1-figures-data", "figures, datasets and external requests", "L07.html, L08.html", "PASS",
    "grep for http, svg, iframe, img, figures-*.js, data-files over both pages: no hits except assets/ paths; both link targets resolve (checked each href). No figure or dataset in this slice.")
row("M7c-r1-cards-L07-theorems", "L07 definition, theorem, corollary and remark cards read against lesson text", "cards.json: M7-c121..c128, c211, c212, c224 (lines 781-788 for c123, c124)", "PASS",
    "All eleven re-read against L07.html. M7-c123 (line 781) now says 'the totals from (0, s) have supremum 1 and no plan attains it, so the maximum in Definition 1.2 does not exist (Remark 1.3)', which matches Remark 1.3 (L07.html:74) and R1. M7-c124 (line 788) matches Definition 1.4 (L07.html:79). Others match their theorems and carry hypotheses (finite S, finite A(s), deterministic f, finite H). All graded T and correct.")
row("M7c-r1-cards-L07-lab-and-misconceptions", "L07 lab, Remark 2.5, misconception and key-row-mirror cards: text, numbers, grade and basis", "cards.json: M7-c129, c130-c133, c135-c137 (c136 at line 870)", "FAIL",
    f"Numbers and lab claims in all cards check against the lab output ({S}cards_check_output.txt, {S}independent_numbers_output.txt). [LOW: grade consistency, ruling 13] M7-c136 (cards.json:870) is graded C with basis 'Lab 1 (SIMULATED), Part C', but its first claim, that Remark 2.5 gives a two-period plan with an optimal continuation that is not optimal, is the content of Remark 2.5, which the key-results row L07.html:470 grades T. Ruling 13 requires a card and the key-results row it mirrors to carry the same grade and basis. The card also tests two facts (the converse of the principle, and the Lab 1 greedy plan), which BUILDER_RULES 7 ('Each card tests one fact') does not allow. The Lab 1 sentence on its own is correctly C. Under-grading, not over-grading.",
    "Split M7-c136 into two cards: one T card 'Does an optimal continuation of every later time make a plan optimal? No: Remark 2.5 (T)' and one C card 'Lab 1, Part C: greedy plan 400, 0, 0, 0 has optimal tails but is not optimal (basis Lab 1, SIMULATED)'. Alternatively set grade T with basis 'Remark 2.5' and move the lab sentence to a separate card. Make the change in the card source the builder pipeline uses for cards.json, then re-run check_pages --unit M7; the new card text must still agree with L07.html:322-346.")
row("M7c-r1-cards-L08-theorems", "L08 definition, theorem, lemma, proposition and remark cards", "cards.json: M7-c142-c145, c147-c149, c155, c156, c162, c186, c214", "PASS",
    f"Re-read against L08.html: c142/c143 (Definitions 1.1, 1.2), c144/c145 (Theorems 1.3, 1.4, with beta >= 0), c147 (Definition 2.1), c148 (Lemma 2.2), c149 (Proposition 2.3), c155-c156 (Misconception 1; Remark 1.5), c162 and c214 (Remark 2.4), c186 (Section 3; {S}small_examples_output.txt: V_0 = 1 and U_0 = 0 for beta = -1). All graded T, all carry their hypotheses.")
row("M7c-r1-cards-L08-lab", "L08 lab, misconception and instance cards", "cards.json: M7-c150-c154, c157, c175, c199, c215", "PASS",
    f"c150 (edited this round, cards.json:935) is C with basis Lab 1 Part C, consistent with ruling 13; c151 (13.948890), c152 (none tied), c153 (378), c154 (changes), c157 (policy), c175 (18 pairs), c215 (0.9 ratios exact per {S}independent_numbers_output.txt) all match the printed output and are C. c199 (V_5 = 6, 4, 1) is T with Problem M1 as its derivation (L08.html:349-354) and grade T is correct.")
row("M7c-r1-cards-duplicates-and-numbers", "full scan for duplicate cards and card numbers in lesson text", "course/modules/M/M7/cards.json (199 cards; 40 in this slice)", "PASS",
    f"{S}cards_check.py -> {S}cards_check_output.txt: 199 cards, no duplicate id, no duplicate front. All 40 slice cards: every number in the card occurs in the lesson text, and every cited Definition/Theorem/Remark/Lemma/Proposition/Corollary/Problem/Part/Section/Misconception reference exists in the lesson. No two slice cards ask the same question.")
row("M7c-r1-hub-L08-card-error-claim", "hub card for L08 restates the lab output", "course/modules/M/M7/index.html:150", "PASS",
    CARRY3_HUB + "the card at index.html:150 says value iteration with the change between successive iterates reported, and that the infinite-horizon result is not treated: both match L08.html:52 and the lab's printed changes.")
row("M7c-r2-cmd-check_projects", "tools/check_projects.py --unit M7", "course/modules/M/M7/project.html", "PASS",
    f"Run at edbb7aa8 -> 'check_projects M7: PASS', exit 0 ({S}check_projects_output.txt).")
row("M7c-r2-delta-L07-L08-hunks", "delta 8196077d..edbb7aa8 for this slice: every hunk read", "L07.html:52; L08.html:52, 383, 457, 489; cards.json c123, c124, c150", "PASS",
    "git diff 8196077d edbb7aa8 -- course/modules/M/M7 read in full: L07.html:52 (why-it-matters: Definition 1.4, Theorem 2.1 and L08 Definition 1.2 pointers all resolve); L08.html:52 (Definition 1.2, Definition 2.1, Proposition 2.3 resolve); L08.html:383 (P2 now says terminal reward B, which Definition 1.1 supplies); L08.html:457 (key row now carries the terminal-reward hypothesis, see M7c-r1-math-L08-theorems for the H = 0 gap); L08.html:489 (Q3 explanation, correct); cards.json c123, c124, c150 (read, correct). No other M7 file changed; tests/labs/M7, index.html, project.html, grader/, tools/, references/, notation/, curriculum/curriculum.json verified identical by git diff --quiet.")
row("M7c-r2-delta-cards", "delta on cards.json for this slice", "course/modules/M/M7/cards.json", "PASS",
    "The three changed cards (M7-c123 line 781, M7-c124 line 788, M7-c150 line 935) re-verified in full (rows M7c-r1-cards-L07-theorems and M7c-r1-cards-L08-lab). Unchanged cards carry their prior verification by re-reading in this round.")
row("M7c-r3-card-M7-c123", "card agrees with the CURRENT lesson text (round-3 FAIL)", "course/modules/M/M7/cards.json, id M7-c123 (line 781)", "PASS",
    "Round-3 fix applied as specified: back now reads 'the totals from (0, s) have supremum 1 and no plan attains it, so the maximum in Definition 1.2 does not exist (Remark 1.3)'. Matches L07.html:74 and L07.html:440. Grade T retained.")
row("M7c-r3-L08-keyresult-lemma22-hypothesis", "key-results row restates Lemma 2.2 with its hypotheses (round-3 FAIL)", "course/modules/M/M7/L08.html:457", "PASS",
    "Round-3 fix applied: row now reads 'with the same data and terminal reward'. The terminal-reward hypothesis is present. The separate horizon-0 issue (H - 1 = 0 when H = 1) is recorded in M7c-r1-math-L08-theorems.")
row("M7c-r3-cmd-build_site-check", "tools/build_site.py --check", "course/concepts.html, site data", "PASS",
    f"Run at edbb7aa8 -> 'site data current: 6 outputs', exit 0 ({S}build_site_check_output.txt).")
row("M7c-r3-cmd-pytest-docs-refs", "pytest tests/test_docs_figures.py and tests/test_refs.py", "tests/", "PASS",
    f"{S}pytest_docs_output.txt and {S}pytest_refs_output.txt: both exit 0.")
row("M7c-r3-value-iteration-prose", "prose use of 'value iteration' (concept owned outside the closure?)", "L08.html:52, 114, 119, 311; index.html:150", "PASS",
    "'value iteration' is defined in the unit's own text as the title of Definition 2.1 (L08.html:114-119). It is not a concept the curriculum assigns to another unit, so it needs no DAG link, and check_dag passes. Not a defect.")
row("M7c-r3-full-read", "entire slice read", "L07.html (568 lines), L08.html (551 lines), twins, 40 slice cards", "PASS",
    f"Read L07.html and L08.html in full in this round (every line); read every slice card (cards_check.py dump plus manual reading); the twins are compared line by line with the page code by {S}extract_compare.py. Shown and computed: {S}independent_numbers.py, {S}small_examples.py, {S}cards_check.py.")

rows.append({
    "id": "M7c-r4-L08-beta-standing-assumption",
    "check": "scope of the standing assumption on the discount factor",
    "location": "course/modules/M/M7/L08.html:56 vs L08.html:60-64, 320, 426-428",
    "status": "FAIL",
    "evidence": "[LOW: wording] L08.html:56 says 'add a discount factor beta \\ge 0, a real number', so this lesson's beta is nonnegative. Definition 1.1 (L08.html:60-64) is stated for any beta, and Section 3 (L08.html:320) and Problem R1 (L08.html:426-428) analyse beta = -1 and beta < 0 as the lesson's own subject. No false claim: Theorems 1.3, 1.4 and Proposition 2.3 each state beta \\ge 0 explicitly (L08.html:78, 92, 134). The sentence is only inconsistent with the later use.",
    "fix": "Replace L08.html:56 'add a discount factor \\(\\beta \\ge 0\\), a real number' with 'add a discount factor \\(\\beta\\), a real number'. Keep the theorem-level hypotheses unchanged.",
})

fragment = {
    "unit": "M7",
    "slice": "c",
    "round": 4,
    "verifier": "independent verifier (Haiku), unit M7 slice c, round 4 (final full verification, rulings 1-26, ruling 26 severity rule)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "round-3 fragment /Users/billyribeiro/.fanout/frags/S-M7-c.round3.json (pin 8196077d). Delta 8196077d..edbb7aa8 for this slice: L07.html:52, L08.html:52, 383, 457, 489, cards.json c123, c124, c150. tests/labs/M7, index.html, project.html, grader/, tools/, references/, notation/, curriculum/curriculum.json byte-identical (git diff --quiet). Every round-3 row id is kept; rows whose subject changed were re-verified fresh; rows whose subject is byte-identical are marked 'Carried from round 3'.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-M7-c",
    "scratch": "ledgers/M7/scripts/M7-c-r4/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. Ruling: lab twins are demonstrations; mutation testing applies to project graders only (VERIFIER_RULES 2.5, rulings file). No project grader in this slice.",
        "Blocking rows (ruling 26 kinds): M7c-r1-math-L08-theorems (missing hypothesis: horizon-0 case used by Lemma 2.2 at t = H and Proposition 2.3 at n = 0, undefined under the inherited H >= 1). Fix is one sentence. All other FAIL rows are LOW (wording or grade consistency) and may be deferred to plans/KNOWN-ISSUES.md with their ids under ruling 26.",
        "Ruling 26: the slice is accepted only after the blocking row is fixed and a verification round returns no blocking row. M7 is not an S-tag slice, so round 4 is not its last full verification.",
        "Ruling 1 (\\R), ruling 13 (T vs C for lab-read values), ruling 16 (not applicable: no LX1 notation), ruling 26 applied.",
        "Checked and found not defective, recorded for the architect: Remark 1.3 uses an infinite action set but is explicitly a counterexample to finiteness; the forward pointers to L08 (Bellman equation) and L08 section 3 (policy) are explicit; Corollary 2.4 of L07 is stated only for beta = 1, which L08 says.",
        "Lab probes in this round were not re-run beyond the round-3 probe (carried); the twins are byte-identical.",
    ],
    "summary": "M7 slice c round 4 (L07, L08, twins, 40 cards) at edbb7aa8. Every gate re-run fresh and passing (check_pages, check_dag, run_labs L07/L08, twins under python -I -W error, page code == twin, expected == output, ruff, mypy strict and repo, pytest lab cases and refs/docs, page_smoke L07 and L08 alone, verify_refs --offline, build_site --check, check_projects). All numbers in prose, labs, quiz and problems recomputed independently. All 40 cards re-read and checked for numbers and references. Non-PASS rows: one blocking (horizon-0 hypothesis in Lemma 2.2 and Proposition 2.3) and three LOW (R1 solution wording, card M7-c136 grade, beta standing-assumption wording).",
}

out = Path("ledgers/M7/M7-c.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "by status", {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
