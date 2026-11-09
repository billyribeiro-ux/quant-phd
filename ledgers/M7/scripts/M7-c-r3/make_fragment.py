"""Assemble the round-3 verifier fragment for M7 slice c from the evidence recorded under ledgers/M7/scripts/M7-c-r3/."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS3-M7-c")
S = "ledgers/M7/scripts/M7-c-r3/"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


P = "PASS"
# ---- carried ids from round 1 and round 2, all re-run or re-derived at 8196077d
row("M7c-r1-cmd-check_pages", "tools/check_pages.py --unit M7", "index, L01-L08, project, cards", P,
    f"Run at 8196077d: `.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 ({S}commands_output.txt). check_cards (tools/check_pages.py:366-399) passes for the 199 cards.")
row("M7c-r1-cmd-check_dag", "tools/check_dag.py --unit M7", "DAG of M7", P,
    f"Run at 8196077d -> 'check_dag M7: PASS', exit 0 ({S}commands_output.txt).")
row("M7c-r1-cmd-run_labs-L07", "tools/run_labs.py --unit M7 --page L07", "course/modules/M/M7/L07.html, lab-M7-L07-1", P,
    f"Run at 8196077d -> 'run_labs M7: PASS (1/1)', exit 0 ({S}labs_output.txt). Whole unit `--unit M7` -> 'PASS (11/11)', exit 0 (same file).")
row("M7c-r1-cmd-run_labs-L08", "tools/run_labs.py --unit M7 --page L08", "course/modules/M/M7/L08.html, lab-M7-L08-1", P,
    f"Run at 8196077d -> 'run_labs M7: PASS (1/1)', exit 0 ({S}labs_output.txt).")
row("M7c-r1-twins-alone-python-I-W-error", "each twin run alone under python -I -W error", "tests/labs/M7/lab-M7-L07-1.py, tests/labs/M7/lab-M7-L08-1.py", P,
    f"`python -I -W error <twin>` exit 0 for both; stderr 0 bytes; stdout saved to {S}twin_L07.stdout (798 bytes) and {S}twin_L08.stdout (903 bytes) ({S}labs_output.txt).")
row("M7c-r1-page-code-equals-twin", "HTML-unescaped page code block vs twin source", "course/modules/M/M7/L07.html:150-298, L08.html:150-284 vs twins", P,
    f"{S}cmp_page_twin.py / {S}cmp_page_twin_output.txt: page code == twin.rstrip('\\n') True for L07 and L08. The exact-equality difference is the single trailing newline, which tools/embed_labs.py:117 and tools/run_labs.py:74-75 strip by convention, so the page and twin are equal under the repo's own comparison.")
row("M7c-r1-expected-equals-output", "page expected block vs twin stdout", "course/modules/M/M7/L07.html:299-318, L08.html:285-310", P,
    f"{S}cmp_page_twin_output.txt: expected == twin stdout after rstrip('\\n') True for both pages; the twin stdout files are {S}twin_L07.stdout and {S}twin_L08.stdout.")
row("M7c-r1-cmd-ruff", "ruff check and ruff format --check", "tests/labs/M7 (repo-wide too)", P,
    f"`ruff check tests/labs/M7/lab-M7-L07-1.py tests/labs/M7/lab-M7-L08-1.py` All checks passed; `ruff format --check` 2 files already formatted ({S}gates_output.txt). Repo-wide `ruff check .` All checks passed and `ruff format --check .` 553 files already formatted ({S}ruff_check_repo.txt, {S}ruff_format_repo.txt).")
row("M7c-r1-cmd-mypy-strict", "mypy --no-incremental --strict on the twins; repo-wide mypy", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", P,
    f"Strict mypy on the two twins: 'Success: no issues found in 2 source files' ({S}gates_output.txt). Repo-wide `.venv/bin/mypy --no-incremental`: 'Success: no issues found in 385 source files', exit 0 ({S}mypy_repo.txt).")
row("M7c-r1-cmd-pytest-lab-cases", "pytest lab cases for L07 and L08", "tests/test_labs.py (parametrized)", P,
    f"`pytest -q tests/test_labs.py -k \"lab-M7-L07-1 or lab-M7-L08-1\"` -> '..', exit 0 ({S}pytest_labs_output.txt). Collect-only lists 11 M7 lab cases in tests/test_labs.py.")
row("M7c-r1-cmd-page_smoke", "tools/page_smoke.py --unit M7 --pages L07 / L08 (run alone)", "course/modules/M/M7/L07.html, L08.html", P,
    f"`--pages L07` -> 'page_smoke modules/M/M7/L07.html: PASS', exit 0; `--pages L08` -> 'page_smoke modules/M/M7/L08.html: PASS', exit 0 ({S}page_smoke_L07.txt, {S}page_smoke_L08.txt). Lab timing 0.0 s each (runtime boot 1.1 s).")
row("M7c-r1-cmd-verify_refs-offline", "tools/verify_refs.py --offline", "references/references.json", P,
    f"'offline integrity: 560 entries, 0 problems', exit 0 ({S}commands_output.txt). The slice cites no registry key: data-references is empty (L07.html:556, L08.html:539) and no slice card has a cite field.")
row("M7c-r1-numbers-L07-prose", "re-derive every number in L07 prose, lab claims and problems", "L07.html:52, 56, 149, 300-318, 319, 342-350, 415-422, 429, 466-470, 490-549", P,
    f"{S}indep_L07_L08.py (plain Python, no lab import; output {S}indep_L07_output.txt). Recomputed: Part A table equal to L07.html:300-304; W400 column 240, 220, 200, 130, 4; plans 70 = C(8,4) (E3); greedy 130 vs optimal 240; 130/240 = 13/24 = 0.541666 -> 0.5417 (E2); differences 20, 20, 70, 126 (E1); V0-V3 at 400 = 110 (quiz); plan (200,100,100) from (1,400) totals 220 = V1(400) (quiz); Remark 2.5 V0(x)=1; M1-M3 values as in L07.html:365-379.")
row("M7c-r1-numbers-L08-prose", "re-derive every number in L08 prose, lab claims and problems (Fraction arithmetic)", "L08.html:52, 149, 286-292, 311, 353, 360, 367, 403, 410, 417, 442, 480, 514-531", P,
    f"{S}indep_L08.py / {S}indep_L08_output.txt (no lab import): V0(0)=1394889/100000 = 13.94889 (denominator 10^5, so the five-place claim at L08.html:403 holds); V0(0)-V1(0) = 59049/100000 = 0.590490; V4(0)=48/5=9.6; V5=(6,4,1); 378 = 3(2^6+...+2^1); changes exact 6, 18/5, 137/50, 1233/500, 11097/5000, 99873/50000 = printed 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746; ratios 3/5, 137/180=0.7611, then 9/10 three times (E2); policy rows L08.html:293-298 equal recomputation; repair at V4(0): 7/5=1.4 (M1); M2 values 2, 3, 7/2, 9/2; M3 = 7/2.")
row("M7c-r1-math-L07-theorems", "Definitions 1.1-1.4, Remark 1.3, Theorems 2.1-2.3, Corollary 2.4, Remark 2.5", "L07.html:58-145, 322-325", P,
    f"All proof lines re-read. Random-instance check {S}math_random_check.py (output {S}math_random_check_output.txt, seed fixed): Theorem 2.1 formula and recursion vs brute force 2033 checks; Theorem 2.2 1585 optimal plans x all continuations; Theorem 2.3 iff 99647 (plan, first action, continuation) triples; Corollary 2.4 2033 checks; 0 failures. Remark 2.5 example: V1(y)=0, V0(x)=1 attained only by b, plan (a,c) total 0 < 1. Remark 1.3: totals from (0,s) are a with 0<a<1, supremum 1 not attained.")
row("M7c-r1-math-L08-theorems", "Definitions 1.1-2.1, Theorems 1.3-1.4, Remark 1.5, Lemma 2.2, Proposition 2.3, Remark 2.4", "L08.html:58-145", P,
    f"All proof lines re-read. {S}math_random_check.py (beta in {{0, 1/2, 1, 2}}): Theorem 1.3 vs brute force 5804 (t,s) checks, 0 failures; Theorem 1.4 uniqueness 3600 checks; Lemma 2.2 time shift 17348 checks; Proposition 2.3 11640 checks; 0 failures. Section 3 beta = -1 example: four plan totals (0, -1, 1, 0), V0=1, U1=1, U0=0 ({S}math_random_check_output.txt). Remark 1.5: (1+c, c) solves the t=0 equation for every c.")
row("M7c-r1-math-problem-sets-L07", "problems M1-M3, P1-P3, E1-E3, R1-R3", "L07.html:361-456", P,
    f"Each solution recomputed: M1-M3 ({S}indep_L07_output.txt: V1(x)=5, V1(y)=3, V0(x)=10; plans (u,w)=6, (v,u)=9, (v,v)=10, (u,v) infeasible); E1-E3 as in the numbers row; R2 objective example recomputed in {S}math_random_check_output.txt (V1(x)=5, plans (a0,c) and (a0,b) both 10 = V0(s), (c) with objective 3 < 5); R1 sup 1, no attaining plan; R3 counts m^(H-t) and H|S|m. P1 (induction-free last step), P2 (cancellation of r(s,a)), P3 (Theorem 2.3 chain) re-checked line by line.")
row("M7c-r1-math-problem-sets-L08", "problems M1-M3, P1-P3, E1-E3, R1-R3", "L08.html:349-446", P,
    f"Recomputed in {S}indep_L08_output.txt and {S}math_random_check_output.txt: M1 V5=(6,4,1), V4(0)=9.6 (run) vs -4+0.9*6=1.4 (repair); M2 (2, 3, 7/2, 9/2); M3 7/2; P1 H=1 unique solution; P2 time shift (two identical sets of totals); P3 beta=1 family; E1-E3 as above; R1 sign step (beta<0 example); R2 U^2 as maximum over length-2 sequences (consistent with Proposition 2.3 checks); R3 u_n=1/n for n>=1: distance/change = n+1 for n=1..5 ({S}math_random_check_output.txt).")
row("M7c-r1-lab-L07-claims", "every printed-claim sentence in the L07 lab text", "L07.html:149, 161-165, 300-318, 319, 342-350", P,
    f"Each named printed line matches the expected block and the independent computation: V0(400)=240 (line 300-304), plans_checked_from_0_400 70 (306), recursion_matches_brute_force True (307), greedy 400 0 0 0 total 130 (313-314), tails from t=1,2,3 True (315-317), greedy_plan_optimal False (318).")
row("M7c-r1-lab-L08-claims", "every printed-claim sentence in the L08 lab text", "L08.html:149, 158-164, 286-310, 311", P,
    f"V0(0)=13.948890 (286); policy lines show repair in state 2 for t=0..3 and run for t=4,5 (293-298); tied_pairs_t0_to_5 0 (299); plans_enumerated 378 (301); changes 6.0..1.99746 (304-309); iterate_equals_n_period_recursion True (310). All equal {S}indep_L08_output.txt.")
row("M7c-r1-lab-L07-check-probe", "student-error probe of the L07 twin (labs are demonstrations; the ruling applies)", "tests/labs/M7/lab-M7-L07-1.py", P,
    f"{S}lab_probe.py (output {S}lab_probe_output.txt, survivor classification {S}lab_probe_survivors.txt): 6 mutants: min-for-max (recursion False, tail False: killed); strict feasibility (ValueError crash: loud); brute force ignores bequest (identical stdout: survivor); optimal plan uses period t instead of t+1 (plan 0,100,100,100; tail False: killed); tail check against values[0] (identical stdout: survivor); greedy uses min (greedy_total 4: differs from page expected: killed by run_labs). The two survivors print identical lines because the bequest is never the binding term on this instance and V_t(w)=V_0(w) along the optimal path; no lesson sentence claims the lab detects a bequest or time-index error, so neither is a finding (ruling: labs are demonstrations).")
row("M7c-r1-lab-L08-check-probe", "student-error probe of the L08 twin", "tests/labs/M7/lab-M7-L08-1.py", P,
    f"Same probe ({S}lab_probe_output.txt, {S}lab_probe_survivors.txt): min for max in the Bellman step (recursion False: killed); brute force drops the discount (recursion False: killed); brute force misses the terminal term (recursion False: killed); value iteration applies the operator to beta*U (iterate_equals False: killed); repair moves to state 1 (values change, so run_labs fails against the page expected block: killed); repair cost sign (tied_pairs 1 and changed values: killed). No survivor with identical output.")
row("M7c-r1-lab-seeded-no-network", "no randomness, no network, SIMULATED label", "tests/labs/M7/lab-M7-L07-1.py:3, lab-M7-L08-1.py:3; L07.html:149; L08.html:149", P,
    "Twins import only __future__, fractions and itertools (no random, socket or urllib; grep); both twins and both hypothesis paragraphs say SIMULATED; page_smoke runtime 0.0 s per lab.")
row("M7c-r1-grades-L07", "grade audit, L07", "L07.html:87, 109, 124, 138, 466-470", P,
    "Theorems 2.1-2.3 and Corollary 2.4 and Remark 2.5 graded T; their proofs are on the page and were re-read (rows above). Lab-read numbers are not graded T in the lesson; the cards grade them C naming Lab 1 (c130-c137).")
row("M7c-r1-grades-L08", "grade audit, L08", "L08.html:77, 91, 122-123, 133, 454-458", P,
    "Theorem 1.3, Theorem 1.4, Lemma 2.2, Proposition 2.3 and Remark 1.5 graded T; proofs on the page and re-read. Lab-read numbers are C naming Lab 1 (c150-c154, c175, c215).")
row("M7c-r1-dag-concept-links", "concept links and definitions vs check_dag and the prerequisite closure", "L07.html:38-39, 79; L08.html:38-39, 69; course/concepts.html", P,
    f"check_dag PASS ({S}commands_output.txt). L07 links mathematical-induction (M1, in closure); defines principle-of-optimality once (L07.html:79). L08 links principle-of-optimality to L07.html#def-principle-of-optimality (earlier, anchor exists), mathematical-induction, and defines bellman-equation once (L08.html:69). No link to a concept outside the closure. Prose names outside the closure are noted in M7c-r3-value-iteration-prose.")
row("M7c-r1-forward-reference-bellman", "forward mention of the Bellman equation before L08", "L07.html:52, 84", P,
    "Both mentions are explicit pointers to L08 Definition 1.2 (\"Lesson L08 calls that recursion the Bellman equation (its Definition 1.2)\"; \"Lesson L08 calls the equation in Theorem 2.1 the Bellman equation\"). No link and no use of its content before the definition. Lines unchanged since round 2; re-read.")
row("M7c-r1-notation", "notation registry collisions", "L07.html and L08.html math", P,
    f"{S}notation_scan.py / {S}notation_scan_output.txt: no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q) occurs in either page. The registered macro \\R is used with its meaning (real numbers). Lesson-local symbols, each defined in the lesson: beta (L08.html:56), S, A, H, m (L07.html:333, R3), Sigma (L07.html:116), C (L08.html:124), U, W^(n), G (L08.html:115-119).")
row("M7c-r1-banned-process-words", "BUILDER_RULES 1.3-1.4 phrases and process words", "L07.html, L08.html, slice cards", P,
    f"check_pages PASS; grep (banned phrases plus builder, verifier, architect, planner, round N, ruling, fixer, B1/B2, Q-numbers, open item) over both pages and the 40 slice cards: no hits ({S}banned_process_grep.txt, {S}commands_output.txt). The only Q1/Q2 hits are in other units' cards.")
row("M7c-r1-scope-words", "scope words need a computation or a proof", "L07.html, L08.html", P,
    "All occurrences of every|all|always|never|any|exactly|only|none|whenever in both pages read in context. Each is a definitional quantifier, a claim proved on the page (Theorems 1.3-1.4, 2.1-2.3, Corollary 2.4, Lemma 2.2, Proposition 2.3), a count the lab prints (20 pairs, 18 pairs, 70, 378), or a distractor option. 'Every problem has a full worked solution' (L07.html:357, L08.html:345) holds: all 12 problems in each lesson have a details.solution block.")
row("M7c-r1-attribution", "attribution: nothing cited from memory", "L07.html:555, L08.html:538; cards", P,
    "No author, year, DOI, page or locator string in either page (grep for years, et al, Boyd, Stokey, Lucas, Prescott, doi). Both pages state they cite no outside source; data-references empty. No slice card has a cite field.")
row("M7c-r1-structure-counts", "template sections, counts and quiz/problem minimums", "L07.html:52, 337-353, 355-458, 476-551; L08.html:52, 325-341, 343-446, 464-534", P,
    f"Counted from the pages: L07 why-it-matters 118 words (<=120); 10 quiz items (8-15); 3 misconceptions; 12 problems (3 per tier, M1-M3, P1-P3, E1-E3, R1-R3), each solution >= 35 words. L08 why-it-matters 120 words; 9 quiz items; 3 misconceptions; 12 problems, solutions >= 50 words. Every quiz answer and explanation checked against the lab (L07 240, 70, 130, 220, 110; L08 9.6, 378, 2.74, 0.590490). check_pages PASS covers section order and minimum counts.")
row("M7c-r1-hours", "hours arithmetic", "L07.html:2, 35; L08.html:2, 35; index.html:29 (data-hours-lessons=77), 141, 149-150", P,
    "data-hours L07=9, L08=10; eyebrows 9 and 10 study hours; hub cards 'L07 · 9 h' (index.html:149) and 'L08 · 10 h' (index.html:150). Lesson sum 9+9+10+10+10+10+9+10 = 77 equals the hub's data-hours-lessons=77. The project's 33 h is outside this slice.")
row("M7c-r1-B2-infinite-horizon", "infinite-horizon result is not stated", "L08.html:52, 144, 311, 317, 538", P,
    "L08 says the infinite-horizon case is not treated (52, 538), that Proposition 2.3 says nothing about it (144), that the lab shows no value for a problem with no fixed horizon (311), and that no infinite-horizon result is stated (317). No infinite-horizon claim found.")
row("M7c-r1-figures-data", "figures, datasets and external requests", "L07.html, L08.html", P,
    "grep for <svg, <img, data-files, MANIFEST and http in both pages: 0 hits. page_smoke reports no external requests (page_smoke_L07.txt, page_smoke_L08.txt).")
row("M7c-r1-cards-L07-theorems", "L07 definition, theorem and corollary cards", "course/modules/M/M7/cards.json: M7-c121..c128, c211, c212, c224", "FAIL",
    f"All 11 cards read in full ({S}cards_L07_L08_dump.txt) and matched to their lesson text. Ten match. M7-c123 does not: its back says 'the value is the supremum 1', which the current Remark 1.3 and R1 do not say (see M7c-r3-card-M7-c123).",
    "Fix M7-c123 as specified in row M7c-r3-card-M7-c123; the other ten cards need no change.")
row("M7c-r1-cards-L07-lab-and-misconceptions", "L07 lab, Remark 2.5 and misconception cards", "cards.json: M7-c129, c130-c133, c135-c137", P,
    "Each card matched to L07.html:149, 300-318, 319, 324, 342-350: c129 V_0(x)=1 (Remark 2.5); c130 240, 220, 200, 130, 4 (W400 column); c131 20 pairs; c132 70 = C(8,4) with basis; c133 optimal plan 100 x4, total 240, every continuation optimal; c135-c137 misconceptions. c134 is absent from the file; the id sequence need not be contiguous and check_pages has no contiguity rule.")
row("M7c-r1-cards-L08-theorems", "L08 definition, theorem, lemma and proposition cards", "cards.json: M7-c142-c145, c147-c149, c155, c156, c162, c186, c214", P,
    "Each matched to its lesson statement and hypotheses: c144, c145, c149 carry beta >= 0 and the finite-problem hypotheses; c148 states Lemma 2.2 with the same terminal reward C; c186 matches Section 3; c214 and c162 match Remark 2.4 and Problem R3; c155 and c156 match misconceptions 1 and 2.")
row("M7c-r1-cards-L08-lab", "L08 lab and misconception cards", "cards.json: M7-c150-c154, c157, c175, c199, c215", P,
    f"Each matched to L08.html:149, 286-310, 311, 293-299, 353, 360 and to {S}indep_L08_output.txt: c150 (U^n equals V_(H-n), i.e. the n-period value with terminal reward U^0=0, which is what the lab checks); c151 13.948890; c152 no ties; c153 378 = 3*(2^6+...+2^1); c154 changes; c157 policy; c175 18 pairs; c199 V5=(6,4,1); c215 0.9 pattern from n=3 on, labelled as an instance-only observation. Lab-read values are C with basis.")
row("M7c-r1-cards-duplicates-and-numbers", "full scan for duplicate cards and card numbers in lesson text", "course/modules/M/M7/cards.json (199 cards)", P,
    f"{S}cards_scan.py / {S}cards_scan_output.txt: 199 cards; 0 duplicate ids, fronts or backs; 0 near-duplicate fronts; grades valid; every non-T card has a basis; every number in the 40 slice cards appears in its lesson text (the one flagged token '00' is an artefact of the regex on '400').")
row("M7c-r1-hub-L08-card-error-claim", "hub card for L08 restates the lab output", "course/modules/M/M7/index.html:150", P,
    "Round-2 FAIL fixed. index.html:150 now reads 'value iteration on a finite-state problem with the change between successive iterates reported', which matches Part C (changes printed at L08.html:304-309). The 'error reported' promise is gone (git diff 9294b914..8196077d, index.html:150). index.html:149 (L07 card, 'checked against an enumeration of all plans') matches Part B.")
row("M7c-r2-cmd-check_projects", "tools/check_projects.py --unit M7", "course/modules/M/M7/project.html", P,
    f"'check_projects M7: PASS', exit 0 ({S}commands_output.txt). Recorded as a gate command; the project itself is outside this slice.")
row("M7c-r2-delta-L07-L08-hunks", "delta 9294b914..8196077d for this slice", "L07.html:74, 440; L08.html:442, 483; index.html:150", P,
    "git diff 9294b914 8196077d read hunk by hunk for L07.html (Remark 1.3 at line 74; R1 solution at 440), L08.html (R3 solution at 442; quiz item 3 prompt at 483), index.html:150 (hub card) and cards.json (M7-c123 and, outside the slice, M7-c174). tests/labs/M7, notation/, curriculum/, tools/ and references/ show no changed hunks in this range. The reading is complete; the consequence of the M7-c123 hunk is recorded in its own row.")
row("M7c-r2-delta-cards", "delta on cards.json for this slice", "course/modules/M/M7/cards.json", P,
    "git diff 9294b914 8196077d on cards.json: two entries changed. M7-c123 (L07, slice) is re-verified and FAILs (row M7c-r3-card-M7-c123). M7-c174 (L06, outside the slice) changed wording only; it was read and is not graded here.")

# ---- round-3 new rows
row("M7c-r3-card-M7-c123", "card agrees with the CURRENT lesson text", "course/modules/M/M7/cards.json, id M7-c123 (back)", "FAIL",
    "Back reads: 'Yes. For H = 1, one state, A(s) = {a : 0 < a < 1}, r(s, a) = a, f(s, a) = s and B = 0, the value is the supremum 1 and no plan attains it (Remark 1.3).' The current lesson does not call the supremum the value: Remark 1.3 (L07.html:74) says 'The supremum of the totals from (0,s) is 1, and no plan attains it'; Definition 1.2 (L07.html:69) defines V as a maximum, which does not exist here; the R1 solution (L07.html:440) says 'A value defined as this supremum would be 1 here. The page proves nothing about such a definition.' The card asserts what the lesson declines to assert, and it is graded T.",
    "Change the back of M7-c123 to: 'Yes. For H = 1, one state, A(s) = {a : 0 < a < 1}, r(s, a) = a, f(s, a) = s and B = 0, the totals from (0, s) have supremum 1 and no plan attains it, so the maximum in Definition 1.2 does not exist (Remark 1.3).' Keep grade T.")
row("M7c-r3-L08-keyresult-lemma22-hypothesis", "key-results row restates Lemma 2.2 with its hypotheses", "course/modules/M/M7/L08.html:457 (key-results table, grade T)", "FAIL",
    "Row reads: 'The value at time 1 of a horizon-H problem equals the value at time 0 of a horizon-(H-1) problem (Lemma 2.2, one shift)'. Lemma 2.2 (L08.html:124) requires the same data and the same terminal reward C; the row omits it, so as written it is false. Counterexample: H = 1, B = 0 gives V_1 = 0, and a horizon-0 problem with terminal reward C = 1 gives value 1 at time 0. The lemma itself (L08.html:124-129) is correct and random checks passed (math_random_check_output.txt: 17348 Lemma 2.2 checks, 0 failures).",
    "Replace the row text with: 'The value at time 1 of a horizon-H problem equals the value at time 0 of a horizon-(H-1) problem with the same data and terminal reward (Lemma 2.2, one shift)'.")
row("M7c-r3-cmd-build_site-check", "tools/build_site.py --check", "course/concepts.html, site data", P,
    f"'site data current: 6 outputs', exit 0 ({S}build_site_check.txt). Relevant because the pages' dfn and link structure feeds the concept index.")
row("M7c-r3-cmd-pytest-docs-refs", "pytest tests/test_docs_figures.py tests/test_refs.py", "tests/", P,
    f"Both files pass, exit 0 ({S}pytest_docs_refs.txt). Covers the docs-figure and reference integrity tests that could be affected by the slice's prose.")
row("M7c-r3-value-iteration-prose", "prose use of a concept owned outside the closure", "L08.html Definition 2.1 title (line 114) and text (119); L08.html:52, 311; index.html:150", P,
    "'value iteration' is named in prose, not linked and not declared with a dfn. The concept value-function-iteration (M5, 'Value-function iteration with a certified error bound', curriculum/01-foundations.yaml) is outside M7's closure. The page does not claim a certified error bound (L08.html:311, 52, 317). Plan section 3 B2 option (a), approved by the architect, has L08 run value iteration. PASS on the plan's rule (section 8.2(5): undeclared terms are plain prose). Architect to confirm, because Q12 does not list this term.")
row("M7c-r3-full-read", "entire slice read", "L07.html (568 lines), L08.html (551 lines), lab-M7-L07-1.py (149), lab-M7-L08-1.py (135), cards (40 slice cards)", P,
    "Both pages read in full with cat -n in windows that cover every line (longest line 1147 characters, nothing truncated). Both twins read in full. All 40 slice cards read in full (cards_L07_L08_dump.txt). Plan M7-build-plan.md read in full, and the verifier rules file read in full.")

fragment = {
    "unit": "M7",
    "slice": "c",
    "round": 3,
    "verifier": "independent verifier (Haiku), unit M7 slice c, round 3 (final full verification, binding rulings file)",
    "pin": "8196077d",
    "base": "round-2 fragment /Users/billyribeiro/.fanout/frags/S-M7-c.round2.json (pin 9294b914). Delta 9294b914..8196077d for this slice: L07.html:74 and :440, L08.html:442 and :483, index.html:150, cards.json M7-c123 (and M7-c174, outside the slice). No change in tests/labs/M7, notation/, curriculum/, tools/ or references/. Every row was re-run or re-derived at 8196077d; no row is carried. Every round-1 and round-2 row id is kept.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M7-c",
    "scratch": "ledgers/M7/scripts/M7-c-r3/",
    "verified_at": "2026-11-09T06:30:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none registered. Ruling: labs are demonstrations and mutation testing applies to project graders only. The lab probe (ledgers/M7/scripts/M7-c-r3/lab_probe.py, 12 mutants: 6 per twin) is reported in rows M7c-r1-lab-L07-check-probe and M7c-r1-lab-L08-check-probe. Its two identical-output survivors (L07 brute force without the bequest; L07 tail check against values[0]) are power limits of this instance, not findings: no lesson sentence claims the lab detects them.",
        "Non-blocking wording (not a row): card M7-c124 reads 'a plan p = (a_t, a_{t+1}, up to a_{H-1})'; 'up to' inside the tuple should be an ellipsis, e.g. (a_t, a_{t+1}, ..., a_{H-1}). Content is correct.",
        "Round-2 non-blocking items are resolved: L08 quiz item 3 now asks 'Which equation is the terminal condition' (L08.html:483), and R3 now defines u_n = 1/n for n >= 1 (L08.html:442).",
        "Architect question (no FAIL): 'value iteration' is used in prose in L08 without a link (see M7c-r3-value-iteration-prose). Q12 lists six undeclared terms and does not list this one; B2 option (a) implies it is allowed.",
        "The page's code block equals its twin except for the trailing newline that tools/embed_labs.py and tools/run_labs.py strip by convention. This is not a finding.",
        "Lab-read numbers are C grade naming Lab 1 in the cards, as the rules require. No lesson lab-read number is graded T.",
    ],
    "summary": "M7 slice c round 3 (L07, L08, twins, 40 cards) at 8196077d. 50 rows: 47 PASS, 3 FAIL, 0 UNVERIFIABLE. The two round-2 items are fixed: the hub card at index.html:150 and the L08 quiz wording. Two new defects: card M7-c123 says the value is the supremum, which current Remark 1.3 and R1 do not say (FAIL); and the L08 key-results row at L08.html:457 restates Lemma 2.2 without its same-terminal-reward hypothesis (FAIL). The third FAIL row (M7c-r1-cards-L07-theorems) is the card group containing M7-c123. All twins run and match their pages, all printed numbers were re-derived independently, and all gates pass.",
    "what_not_checked": [
        "render_curriculum.py and fetch_data.py --check: the curriculum, notation and data are unchanged in this range, so they were not run.",
        "The full pytest suite: only the M7 lab cases, tests/test_docs_figures.py and tests/test_refs.py were run.",
        "A live verify_refs run: the slice cites no registry key, so offline integrity was run and no network call was made.",
        "run_graders.py, mutate_graders.py and the five alternative project solvers: the project is outside this slice.",
        "Visual inspection beyond page_smoke's geometry, console, and light/dark checks: the slice contains no figures.",
        "Pyodide runtime of the labs beyond page_smoke's reported 0.0 s per lab.",
    ],
}

out = ROOT / "ledgers/M7/M7-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", sum(r["status"] == "FAIL" for r in rows), "pass", sum(r["status"] == "PASS" for r in rows))
