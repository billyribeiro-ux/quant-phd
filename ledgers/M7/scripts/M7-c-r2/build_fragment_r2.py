"""Builds the round-2 fragment ledgers/M7/M7-c.json for M7 slice c (L07, L08, their twins and their cards).

Every evidence string names the command, script or line range that produced it. Run from the checkout:
python3 -I ledgers/M7/scripts/M7-c-r2/build_fragment_r2.py
"""
import json
from pathlib import Path

SCR = "ledgers/M7/scripts/M7-c-r2"
ROOT = Path.cwd()
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gate commands (run by this verifier at 9294b914; output in SCR/commands_output.txt) ----
row("M7c-r1-cmd-check_pages", "gate: check_pages --unit M7", "index, L01-L08, project, cards", "PASS",
    f"Run at 9294b914: `.venv/bin/python tools/check_pages.py --unit M7` -> 'check_pages M7: PASS', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-cmd-check_dag", "gate: check_dag --unit M7", "DAG of M7", "PASS",
    f"Run at 9294b914: `.venv/bin/python tools/check_dag.py --unit M7` -> 'check_dag M7: PASS', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-cmd-run_labs-L07", "gate: run_labs --unit M7 --page L07", "course/modules/M/M7/L07.html, lab-M7-L07-1", "PASS",
    f"`.venv/bin/python tools/run_labs.py --unit M7 --page L07` -> 'run_labs M7: PASS (1/1)', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-cmd-run_labs-L08", "gate: run_labs --unit M7 --page L08", "course/modules/M/M7/L08.html, lab-M7-L08-1", "PASS",
    f"`.venv/bin/python tools/run_labs.py --unit M7 --page L08` -> 'run_labs M7: PASS (1/1)', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-twins-alone-python-I-W-error", "twin run alone: python -I -W error", "tests/labs/M7/lab-M7-L07-1.py, tests/labs/M7/lab-M7-L08-1.py", "PASS",
    f"Each twin run alone with `python -I -W error`: exit 0 (`## twin L07`, `## twin L08` in {SCR}/commands_output.txt). Stdout saved to {SCR}/twin_L07.stdout and {SCR}/twin_L08.stdout.")
row("M7c-r1-page-code-equals-twin", "page embedded code equals twin", "course/modules/M/M7/L07.html:150-298, L08.html:150-284 vs twins", "PASS",
    f"{SCR}/cmp_twin_page.py ({SCR}/cmp_twin_page_output.txt): 'page code == twin' is False only because the twin ends with one extra newline; 'equal after stripping the twin's final newline: True' for L07 and L08.")
row("M7c-r1-expected-equals-output", "expected block equals twin output", "course/modules/M/M7/L07.html:299-318, L08.html:285-310", "PASS",
    f"{SCR}/cmp_twin_page_output.txt: 'expected == twin stdout: True' for L07 and L08. Also a shell diff of each page's expected block against twin_L0x.stdout is empty.")
row("M7c-r1-cmd-ruff", "gate: ruff check and ruff format --check on the twins", "tests/labs/M7", "PASS",
    f"`.venv/bin/ruff check tests/labs/M7` -> 'All checks passed!', exit 0; `.venv/bin/ruff format --check tests/labs/M7` -> '11 files already formatted', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-cmd-mypy-strict", "gate: mypy strict on the twins; repo mypy", "tests/labs/M7/lab-M7-L07-1.py, lab-M7-L08-1.py", "PASS",
    f"`.venv/bin/mypy --no-incremental --strict tests/labs/M7/lab-M7-L07-1.py tests/labs/M7/lab-M7-L08-1.py` -> 'Success: no issues found in 2 source files', exit 0. Repo-wide `.venv/bin/mypy --no-incremental` -> 'Success: no issues found in 385 source files', exit 0 ({SCR}/commands_output.txt).")
row("M7c-r1-cmd-pytest-lab-cases", "relevant pytest: lab twin cases", "tests (test_labs parametrization for M7 L07 and L08)", "PASS",
    f"`.venv/bin/python -m pytest -q tests -k \"lab-M7-L07-1 or lab-M7-L08-1\"` -> '..' (2 passed), exit 0 ({SCR}/pytest_output.txt). The full pytest suite was not run (see what_not_checked in the notes).")
row("M7c-r1-cmd-page_smoke", "gate: page_smoke for L07 and L08, each run alone", "course/modules/M/M7/L07.html, L08.html", "PASS",
    f"`.venv/bin/python tools/page_smoke.py --unit M7 --pages L07` -> 'page_smoke modules/M/M7/L07.html: PASS', exit 0; `--pages L08` -> 'page_smoke modules/M/M7/L08.html: PASS', exit 0 ({SCR}/page_smoke_L07_output.txt, {SCR}/page_smoke_L08_output.txt). Lab runtime 0.0 s each (Pyodide timing lines in those files).")
row("M7c-r1-cmd-verify_refs-offline", "gate: verify_refs --offline (registry)", "references/references.json", "PASS",
    f"`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({SCR}/commands_output.txt). The slice cites no registry key: `<ol data-references></ol>` at L07.html:556 and L08.html:539.")
row("M7c-r2-cmd-check_projects", "gate: check_projects --unit M7 (project slice not judged here)", "course/modules/M/M7/project.html", "PASS",
    f"`.venv/bin/python tools/check_projects.py --unit M7` -> 'check_projects M7: PASS', exit 0 ({SCR}/commands_output.txt). Recorded because it is a gate command; the project itself belongs to another slice.")

# ---- numbers, mathematics, labs, grades ----
row("M7c-r1-numbers-L07-prose", "numbers in prose (computed, quoted, or derived)",
    "L07.html:52, 56, 149, 153, 300-318, 319, 342, 346, 350, 415-422, 429, 489-548 (quiz), 492, 506, 517-534", "PASS",
    f"Independent re-derivation in {SCR}/indep_L07_L08_r2.py ({SCR}/indep_L07_L08_r2_output.txt), no lab import: Part A table equals L07.html:300-304 (True); W400 column 240, 220, 200, 130, 4 (E1 L07.html:415); differences 20, 20, 70, 126; 130/240 = 13/24 = 0.5417 (E2 L07.html:422); brute-force count from (0,400) = 70 = C(8,4) (E3 L07.html:429); brute force equals recursion at all 20 pairs (True); optimal plan 100 100 100 100 total 240; greedy total 130; greedy tails from t=1,2,3 optimal True; greedy plan optimal False; V_1(400)=220 (quiz L07.html:532-534 with plan 200, 100, 100); V_0(400)-V_3(400)=110 (quiz L07.html:546-548).")
row("M7c-r1-numbers-L08-prose", "numbers in prose (computed, quoted, or derived)",
    "L08.html:52, 149, 286-292, 311, 353, 360, 367, 403, 410, 417, 442, 480, 517, 531", "PASS",
    f"{SCR}/indep_L07_L08_r2_output.txt (Fraction arithmetic): V_0(0)=1394889/100000 = 13.94889 (exact denominator 10^5, so the E1 claim 'at most five decimal places' at L08.html:403 holds); V_1(0)=13.3584; V_4(0)=9.6; V_5=(6,4,1); V_4(0) by running 6+0.9*4=9.6 and repair -4+0.9*6=1.4 (M1 L08.html:353); M2 V_1=(2,3), V_0(x)=3.5, V_0(y)=4.5; M3 plan (a,d) total 3.5; E1 0.59049 and 3.6; E2 ratios 0.6, 0.761111 (printed 0.7611), 0.9, 0.9, 0.9; Part C changes exact 6, 18/5, 137/50, 1233/500, 11097/5000, 99873/50000 which display as 6.0000000000 ... 1.9974600000; E3 3*(2^6+...+2^1)=378; quiz values 9.6, 2.74, 0.590490 confirmed.")
row("M7c-r1-math-L07-theorems", "mathematics: theorems, proofs, formulas",
    "L07.html:58-80 (Defs 1.1-1.4), 74 (Remark 1.3), 86-145 (Thms 2.1-2.3, Cor 2.4 and proofs), 322-325 (Remark 2.5)", "PASS",
    f"Every proof line re-read and re-derived. Random checks in {SCR}/indep_L07_L08_r2.py: Theorem 2.1 recursion on 1469 (t,s) instances of 300 random finite problems; Theorem 2.2 (continuations of optimal plans optimal) and Corollary 2.4 (forward maximizing choice optimal) on all 300; Theorem 2.3 iff on 7477 (plan, t, s) triples. Remark 1.3 (sup 1, not attained) re-derived. Remark 2.5 counterexample: V_1(y)=0, V_0(x)=1 via b, plan (a,c) total 0.")
row("M7c-r1-math-L08-theorems", "mathematics: theorems, proofs, formulas",
    "L08.html:58-145 (Defs 1.1-2.1, Thms 1.3-1.4, Remark 1.5, Lemma 2.2, Prop 2.3, Remark 2.4), 430-435 (R1-R2)", "PASS",
    f"Proofs re-read. Random checks in {SCR}/indep_L07_L08_r2.py: Theorem 1.3 (V solves the Bellman system) on 1030 (t,s) pairs against plan enumeration for beta in {{0,1/2,1,2}}; Lemma 2.2 (time shift) and Proposition 2.3 (iterate = n-period value) on 200 random problems (800 iterate checks). Theorem 1.4 uniqueness: the equation for U_t given U_{{t+1}} has a single right-hand side, so downward induction gives U_t = V_t (L08.html:97-101 argument re-read). Remark 1.5 identity re-checked for sampled c. Negative-discount example (L08.html:319): totals 0, -1, 1, 0; V_0=1, V_1=1; U_1=1; U_0=0; U_0 != V_0.")
row("M7c-r1-math-problem-sets-L07", "mathematics: problem sets and solutions",
    "L07.html:361-456 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    f"Each solution recomputed: M1 V_1(x)=5, V_1(y)=3, V_0(x)=10; M2 optimal plan (v,v) total 10; M3 plans (u,w)=6, (v,u)=9, (v,v)=10, (u,v) infeasible; P1-P3 proofs re-checked line by line (P2 cancellation of r(s,a) correct); E1 differences; E2 13/24; E3 C(8,4)=70; R1 sup argument; R2 objective max_k r: plans (a0,b) and (a0,c) both 10, (c) objective 3 not optimal from (1,x) ({SCR}/indep_L07_L08_r2_output.txt); R3 counts m^(H-t) (m=2,H=4,t=0 -> 16; m=3,H=3,t=1 -> 9).")
row("M7c-r1-math-problem-sets-L08", "mathematics: problem sets and solutions",
    "L08.html:349-446 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    f"Each solution recomputed in {SCR}/indep_L07_L08_r2_output.txt: M1 V_5=(6,4,1), V_4(0)=9.6, repair 1.4; M2 (2, 3, 3.5, 4.5); M3 3.5; P1 unique solution at H=1 (proof re-read); P2 totals identical (proof re-read); P3 with beta=1 and c=0 gives U_0=1; E1 0.590490 and 3.6; E2 ratios; E3 378; R1 sign analysis (the step max_q beta J = beta max J needs beta >= 0; -1 example); R2 U^2 as a max over (a_0,a_1) with beta^2 U^0(s_2); R3 u_n=1/n, change 1/(n(n+1)), distance/change = n+1 (n=1,2,3,10 checked).")
row("M7c-r1-lab-L07-claims", "lab claims vs printed output (L07)",
    "L07.html:149 (hypothesis), 161-165 (docstring), 319 (interpretation), 342-350 (misconceptions), expected block 299-318", "PASS",
    "Each printed-line claim matches the expected block: V0(400)=240 (line 300-304 table, Part C optimal_total 240); plans_checked_from_0_400 70 (line 306); recursion_matches_brute_force True (line 307); greedy_consumption 400 0 0 0 and greedy_total 130 (lines 313-314); greedy tails True for t=1,2,3 (lines 315-317); greedy_plan_optimal False (line 318); optimal_plan_every_tail_optimal True (line 312). 'Lab 1 checks the recursion against brute force' (L07.html:52) and 'Part B ... 20 pairs' (L07.html:149) match the embedded code at L07.html:273-279 (page line numbering).")
row("M7c-r1-lab-L08-claims", "lab claims vs printed output (L08)",
    "L08.html:149 (hypothesis), 158-164 (docstring), 311 (interpretation), 321 (ties bullet), 330-338 (misconceptions), expected block 285-310", "PASS",
    "Expected block matches the claims: V_0(0)=13.948890 (line 286); policy lines show repair in state 2 for t=0..3 and run for t=4,5 (lines 293-298); tied_pairs_t0_to_5 0 (line 299); plans_enumerated 378 (line 301); recursion_matches_brute_force True (line 302); n 0..5 changes 6.0, 3.6, 2.74, 2.466, 2.2194, 1.99746 (lines 303-308); iterate_equals_n_period_recursion True (line 309). The embedded checks (matches over n=0..6 against V_(H-n), L08.html:280; tie count over t=0..5, L08.html:254-259) match the embedded docstring at L08.html:158-164.")
row("M7c-r1-lab-L07-check-probe", "lab checks are sensitive to the errors the lesson says they catch (L07)",
    "tests/labs/M7/lab-M7-L07-1.py; probe ledgers/M7/scripts/M7-c-r2/lab_mutants_r2.py", "PASS",
    f"Probe ({SCR}/lab_mutants_r2.py, output {SCR}/lab_mutants_r2_output.txt, 21 mutants over both twins): 18 killed. L07 killed: min-for-max recursion; recursion ignoring the future; recursion reading the same time (values[t] vs values[t+1]); brute force without feasibility check (count 625); optimal plan taking the min; greedy taking the smallest reward; tail check with the wrong index; greedy check inverted. Survivors, none a finding: (a) brute force that drops the bequest still prints True: on this instance the maximum is the same with or without the bequest at all 20 (t, w) pairs, and an optimal plan leaves zero wealth at each of them (ledgers/M7/scripts/M7-c-r2/bequest_check_r2_output.txt); (b) hard-coded 'tail check True' is a rubber stamp, and the real check is live (the wrong-index mutant fails it); (c) V_H = 0 leaves recursion_matches_brute_force True on this instance, but the Part A row t 4 changes, so the expected block detects it. The lesson sentences (L07.html:52, 149, 161-162, 319) claim only that the lab compares the recursion with brute force and that the tail check runs; the probe confirms both. Labs are demonstrations (verifier ruling), so no survivor is a fault.")
row("M7c-r1-lab-L08-check-probe", "lab checks are sensitive to the errors the lesson says they catch (L08)",
    "tests/labs/M7/lab-M7-L08-1.py; probe ledgers/M7/scripts/M7-c-r2/lab_mutants_r2.py", "PASS",
    f"Same probe ({SCR}/lab_mutants_r2_output.txt). L08 killed: Bellman step with min; Bellman step with discount squared; brute force without the discount weight; brute force with weight starting at beta; brute force ignoring the terminal reward; iterate starting from 1; iterate with discount 1; iterate comparing with V_n instead of V_(H-n); undiscounted iterate. Survivor: hard-coded tie count 0 (rubber stamp). The lesson does not claim the lab detects ties: L08.html:321 says 'Lab 1 prints no tie, so it does not illustrate this case'. The true tie count is 0 (independent re-derivation, indep_L07_L08_r2_output.txt 'ties t=0..5 (expect 0): 0').")
row("M7c-r1-lab-seeded-no-network", "lab twins: seeded, no network, runtime",
    "tests/labs/M7/lab-M7-L07-1.py:19-21; lab-M7-L08-1.py:18-21; L07.html:149; L08.html:149", "PASS",
    f"Imports only `__future__`, `itertools` (L07) and `__future__`, `fractions`, `itertools` (L08); no random module, no I/O beyond print; both labs labelled SIMULATED (L07.html:149, L08.html:149); runtime 0.0 s (page_smoke output in {SCR}).")
row("M7c-r1-grades-L07", "grades of claims (BLUEPRINT §3)", "L07.html:466-470 (key results), theorem blocks 87-140", "PASS",
    "Theorems 2.1, 2.2, 2.3, Corollary 2.4 and Remark 2.5 are proved on the page and graded T (L07.html:87, 109, 124, 138; key results 466-470): correct. Lab-read numbers are C naming Lab 1 in the cards (c130-c133, c135-c137); c224 is T and derived on the page. Definitions and Remarks 1.3 are T by proof.")
row("M7c-r1-grades-L08", "grades of claims (BLUEPRINT §3)", "L08.html:454-458 (key results), theorem blocks 77, 91, 123, 133", "PASS",
    "Theorems 1.3, 1.4, Remark 1.5, Lemma 2.2 and Proposition 2.3 are proved on the page and graded T (L08.html:77, 91, 123, 133, key results 454-458): correct. Lab-read numbers are C naming Lab 1 (cards c150-c154, c157, c175, c215). No infinite-horizon claim is graded, because none is stated (architect decision B2).")

# ---- DAG, notation, prose, structure ----
row("M7c-r1-dag-concept-links", "DAG: concept links and definitions", "L07.html:38-39, 79; L08.html:38-39, 69; concepts.html:77", "PASS",
    f"check_dag PASS ({SCR}/commands_output.txt). L07 links mathematical-induction (M1, in closure; anchor concepts.html:77 exists); L07 defines principle-of-optimality (dfn L07.html:79); L08 links principle-of-optimality to L07.html#def-principle-of-optimality and defines bellman-equation (dfn L08.html:69). No link to a concept outside the closure. Prose only, unlinked: 'dynamic programming' (title L07.html:6, 36), 'value iteration' (defined on page, L08.html:114-119), 'Bellman operator' (defined, L08.html:115).")
row("M7c-r1-forward-reference-bellman", "terms used before definition", "L07.html:52, 84; L08.html:68-69", "PASS",
    "L07 uses 'Bellman equation' only as an explicit pointer: 'Lesson L08 calls that recursion the Bellman equation (its Definition 1.2)' (L07.html:52) and 'Lesson L08 calls the equation in Theorem 2.1 the Bellman equation (Definition 1.2 of L08)' (L07.html:84). L08.html:68-69 defines it at Definition 1.2. An explicit pointer, not an undefined use.")
row("M7c-r1-notation", "NOTATION: symbols vs notation/notation.json", "L07.html and L08.html math", "PASS",
    f"{SCR}/static_checks_r2_output.txt: the registry has 8 symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, Q) and 26 macros. Math tokens on L07 (A, B, H, J, S, V, W, a-y, \\Sigma, \\R) and L08 (A, B, C, G, H, J, S, U, V, W, a-y, \\beta, \\mathcal{{G}}, \\R) contain no registered symbol; the only registered macro used is \\R. Local letters (S, H, B, V, J, beta, G, U, C, W^(n)) are defined on their own page (beta at L08.html:56, G at L08.html:115).")
row("M7c-r1-banned-process-words", "banned phrases and process words", "L07.html, L08.html", "PASS",
    f"check_pages PASS; grep (BUILDER_RULES §1.3-1.4 list plus 'builder', 'verifier', 'architect', 'round N', 'ruling', 'planner') -> no hits ({SCR}/commands_output.txt, 'grep banned/process words').")
row("M7c-r1-scope-words", "scope words need a computation or a named set",
    "L07.html and L08.html; occurrences listed in full in " + SCR + "/scope_words_r2_output.txt", "PASS",
    "All scope-word occurrences read (L07 72, L08 61 by the regex in static_checks_r2.py). Each is a definitional quantifier ('for every s in S' in Def 1.1), a claim proved on the page (Theorems 2.1-2.3, 1.3-1.4, Prop 2.3, 'every plan' in the proofs), a computation or enumeration the code performs ('all' over the enumerated plans; 'every value is an integer' with integer code; 'every problem has a full worked solution': 12 solutions present), or a named instance ('every consumption sequence' over the grid, L07.html:271). No unsupported scope word found.")
row("M7c-r1-attribution", "attribution: no unread source or locator", "L07.html:555, L08.html:538; curriculum/01-foundations.yaml:317-319", "PASS",
    "Both pages state they cite no outside source; data-references is empty (L07.html:556, L08.html:539); no author, year or locator appears. The curriculum sources are not cited, so nothing needed a registry check in this slice.")
row("M7c-r1-structure-counts", "structure: template sections, counts, lengths",
    "L07.html:52, 337-353, 355-458, 476-551; L08.html:52, 325-341, 343-446, 464-534", "PASS",
    f"{SCR}/static_checks_r2_output.txt: L07 quiz 10 items, misconceptions 3, problems 12 (3 per tier M, P, E, R), solutions min 37 words, why-it-matters 118 words; L08 quiz 9 items, misconceptions 3, problems 12, solutions min 45 words, why-it-matters 120 words (both within the 120-word cap).")
row("M7c-r1-hours", "hours: data-hours and hub arithmetic",
    "L07.html:2 (data-hours=9), L08.html:2 (data-hours=10); index.html:149-150; index.html data-hours-lessons=77", "PASS",
    "L07 9 h and L08 10 h match the hub cards (index.html:149 'L07 · 9 h', 150 'L08 · 10 h') and the eyebrows (L07.html:35, L08.html:35). Lesson sum 9+9+10+10+10+10+9+10 = 77 equals data-hours-lessons=77; with project 33 this is 110 (plan §5). The other six lessons were read only for their data-hours values.")
row("M7c-r1-B2-infinite-horizon", "B2: no infinite-horizon result stated", "L08.html:52, 144, 317, 319, 538", "PASS",
    "The lesson says the infinite-horizon case is 'not treated here' (L08.html:52), Remark 2.4 explains that Proposition 2.3 says nothing about it (L08.html:144), the canon-breaks bullet says 'This lesson states no infinite-horizon result' (L08.html:317), and the references paragraph says no result is stated (L08.html:538). No contraction argument, no limit and no convergence result appear in L08.")
row("M7c-r1-figures-data", "figures and data", "L07.html, L08.html", "PASS",
    "grep for svg, img, data-files, MANIFEST and http(s) URLs returns 0 hits in both pages (see commands_output.txt). No figure or dataset applies. page_smoke reports no external requests (page_smoke_L07/L08 outputs).")

# ---- cards (cards.json, slice = 40 cards with lesson L07 or L08) ----
row("M7c-r1-cards-L07-theorems", "cards: one per 10 sampled, full read of definitions and theorems (L07)",
    "course/modules/M/M7/cards.json: M7-c121..c128, c211, c212, c224", "PASS",
    "All 11 L07 definition, theorem and corollary cards (c121-c128, c211, c212, c224) read in full and matched to L07 Def 1.1, 1.2, 1.4, Remark 1.3, Thm 2.1, 2.2, 2.3, Cor 2.4 and Remark 2.5. Each is atomic, correct, T, and carries the finiteness hypotheses of Definition 1.1 where Theorems 2.1-2.3 and Corollary 2.4 need them (c125-c128). c224 (rewritten this round) says action a fails condition (i) with r(x,a)+V_1(y)=0 < V_0(x)=1, and b attains it: correct against L07 Remark 2.5 (L07.html:324).")
row("M7c-r1-cards-L07-lab-and-misconceptions", "cards: lab-read numbers, basis, misconceptions (L07)",
    "cards.json: M7-c129, c130-c133, c135-c137 (8 cards; c134 is absent from the file)", "PASS",
    "c129 (V_0(x)=1 via b, Remark 2.5) T and correct. c130 (240, 220, 200, 130, 4) C, basis 'Lab 1 (SIMULATED)', matches L07.html:300-304 (W400 column). c131 (20 pairs) matches Part B and L07.html:149. c132 (70 = C(8,4)) matches E3. c133 (optimal plan 100 x4 total 240, every continuation optimal) matches Part C lines 309-312. c135-c137 (misconceptions) match L07.html:341-349 and Part A/C values. Every C card has a basis naming the lab.")
row("M7c-r1-cards-L08-theorems", "cards: definitions and theorems (L08)",
    "cards.json: M7-c142, c143, c144, c145, c147, c148, c149, c155, c156, c162, c186, c214", "PASS",
    "All read in full. c144, c145, c149 carry beta >= 0 and the finite hypotheses (Thm 1.3, Thm 1.4, Prop 2.3). c148 matches Lemma 2.2. c186 (updated this round) uses actions a (reward 0) and b (reward 1), f(s,a)=s, B=0, beta=-1: V_0=1, U_0=0, correct against L08.html:319 and the re-derivation. c155 (misconception: U^0 dependence, U^1 = 1 + U^0) and c156 are T and correct. c162 and c214 match Remark 2.4 and R3.")
row("M7c-r1-cards-L08-lab", "cards: lab-read numbers and basis (L08)",
    "cards.json: M7-c150, c151, c152, c153, c154, c157, c175, c199, c215", "PASS",
    "c150 (U^n equals the n-period value with terminal reward U^0; lab compares with V_(H-n), which with U^0=0 is that value) C and correct. c151 (13.948890) C, matches line 286 (its 'run as the optimal action' clause was removed this round, correctly). c152 (no tie) C, matches line 299. c153 (378) C, matches E3. c154 (6.0 ... 1.99746) C, matches lines 303-308. c157 (repair t=0..3, run t=4,5) C, matches lines 293-298. c175 (18 pairs) C, matches Part B. c199 (V_5 = 6, 4, 1) now T and derived in M1 (L08.html:353): correct. c215 (ratio 0.9 from n=3) C with 'this instance only' and 'convergence is not shown': matches E2 (L08.html:410).")
row("M7c-r1-cards-duplicates-and-numbers", "cards: full-file duplicate scan and number presence",
    f"course/modules/M/M7/cards.json (199 cards); {SCR}/cards_scan_r2.py", "PASS",
    f"{SCR}/cards_scan_r2_output.txt: 199 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs; 147 T and 52 C; every non-T card carries a basis; every number in the 40 L07/L08 card backs (apart from 0-6) appears in L07.html or L08.html. Both pages contain 'SIMULATED' and 'Lab 1'.")
row("M7c-r1-hub-L08-card-error-claim", "hub card text for L08 vs lesson and lab output", "course/modules/M/M7/index.html:150", "FAIL",
    "index.html:150 (unchanged since aeb512b6, `git diff` empty) says L08 covers 'value iteration on a finite-state problem with the error reported'. The lab prints only the changes between successive iterates (L08.html:299-309 expected block 'n k change ...'; embedded code computes max|U^(n+1)-U^n| at L08.html:277-279), and the lesson says those changes 'are not a bound on the error of the iterates' (L08.html:144), with R3 (L08.html:442) and the quiz explanation (L08.html:517). No error quantity is printed or computed by L08 (grep 'error' in L08.html gives no error bound).",
    "In course/modules/M/M7/index.html line 150, replace 'with the error reported' with 'with the change between successive iterates reported'. The hub owns that line; L08.html and the twin are correct and must not change.")

# ---- round-2 delta ----
row("M7c-r2-delta-L07-L08-hunks", "round-2 delta: every changed hunk of L07.html and L08.html read",
    "L07.html:112-120 (proof, c->g), 437-440 (R1 solution), 566 (footer); L08.html:52, 311, 319-321, 345-367 (M2, M3 use action d), 480 (quiz explanation), 549 (footer)", "PASS",
    f"git diff aeb512b6 9294b914 for both files read hunk by hunk. The renamed symbol g (L07.html:115-120) is consistent within the proof. R1 wording (L07.html:440) fixed. The L08 negative-discount example (L08.html:319) now uses actions a, b with f(s,a)=f(s,b)=s; its numbers were re-derived ({SCR}/indep_L07_L08_r2_output.txt). M2/M3 renamed action c->d in both the problem (L08.html:345) and the solutions (L08.html:360, 365, 367): numbers unchanged (3.5). Quiz explanation (L08.html:480) now shows 6 + 0.9 * V_5(1) = 9.6, correct. Footers changed only in wording. Twins unchanged (git diff empty).")
row("M7c-r2-delta-cards", "round-2 delta: changed card entries of this slice",
    "course/modules/M/M7/cards.json: M7-c133, c151, c186, c199, c224", "PASS",
    "git diff aeb512b6 9294b914 on cards.json: 26 entries changed, of which five are L07/L08 cards (listed here) and one card was added (M7-c225, lesson L02, outside this slice). Each changed slice card was re-checked against the current page: c133 (wealth path removed; still correct), c151 (run clause removed; correct), c186 (actions renamed; correct), c199 (C from Lab 1 changed to T derived in M1; values 6, 4, 1 correct), c224 (rewritten; correct).")

# ---- the rows listed in the round-1 fragment that are not yet re-listed above ----
expected_r1 = [
    "M7c-r1-cmd-check_pages", "M7c-r1-cmd-check_dag", "M7c-r1-cmd-run_labs-L07", "M7c-r1-cmd-run_labs-L08",
    "M7c-r1-twins-alone-python-I-W-error", "M7c-r1-page-code-equals-twin", "M7c-r1-expected-equals-output",
    "M7c-r1-cmd-ruff", "M7c-r1-cmd-mypy-strict", "M7c-r1-cmd-pytest-lab-cases", "M7c-r1-cmd-page_smoke",
    "M7c-r1-cmd-verify_refs-offline", "M7c-r1-numbers-L07-prose", "M7c-r1-numbers-L08-prose",
    "M7c-r1-math-L07-theorems", "M7c-r1-math-L08-theorems", "M7c-r1-math-problem-sets-L07",
    "M7c-r1-math-problem-sets-L08", "M7c-r1-lab-L07-claims", "M7c-r1-lab-L08-claims",
    "M7c-r1-lab-L07-check-probe", "M7c-r1-lab-L08-check-probe", "M7c-r1-lab-seeded-no-network",
    "M7c-r1-grades-L07", "M7c-r1-grades-L08", "M7c-r1-dag-concept-links", "M7c-r1-forward-reference-bellman",
    "M7c-r1-notation", "M7c-r1-banned-process-words", "M7c-r1-scope-words", "M7c-r1-attribution",
    "M7c-r1-structure-counts", "M7c-r1-hours", "M7c-r1-B2-infinite-horizon", "M7c-r1-figures-data",
    "M7c-r1-cards-L07-theorems", "M7c-r1-cards-L07-lab-and-misconceptions", "M7c-r1-cards-L08-theorems",
    "M7c-r1-cards-L08-lab", "M7c-r1-cards-duplicates-and-numbers", "M7c-r1-hub-L08-card-error-claim",
]
got = [r["id"] for r in rows if r["id"].startswith("M7c-r1-")]
assert sorted(got) == sorted(expected_r1), (set(expected_r1) ^ set(got))
assert len(rows) == len(set(r["id"] for r in rows)), "duplicate ids"

non_pass = [r for r in rows if r["status"] != "PASS"]
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if not non_pass else "FAIL"

fragment = {
    "unit": "M7",
    "slice": "c",
    "round": 2,
    "verifier": "independent verifier (Haiku), slice c, round 2 (final full verification, binding rulings file)",
    "pin": "9294b914",
    "base": ("round-1 fragment /Users/billyribeiro/.fanout/frags/S-M7-c.round1.json (pin aeb512b6). Delta aeb512b6..9294b914 "
             "for this slice: L07.html, L08.html and cards.json changed; the twins, index.html, notation, curriculum, tools "
             "and references entries used by M7 are unchanged for this slice (git diff empty). No row was carried: every row "
             "was re-run or re-derived at 9294b914, and every round-1 row id is kept."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M7-c",
    "scratch": f"{SCR}/",
    "verified_at": "2026-11-09T04:45:00Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: the list is empty by design (ruling: labs are demonstrations; mutation testing applies to project graders). The 21 lab-probe mutants are reported in rows M7c-r1-lab-L07-check-probe and M7c-r1-lab-L08-check-probe: 18 killed, 3 survivors, none a finding (see those rows).",
        "Non-blocking wording (no row, not a FAIL): L08.html quiz item 3 asks 'Which pair is the terminal condition' but offers single equations U_H(s)=B(s), U_0(s)=B(s), U_t(s)=0; 'which equation is the terminal condition' would match the options. card M7-c124 writes 'a plan p = (a_t, a_{t+1}, up to a_{H-1})'; 'up to' inside the tuple reads awkwardly and a plain ellipsis would read better. L08 R3 defines u_n=1/n with n>=1 implicitly; u_0 is undefined. The L07 twin and the page code differ only by the twin's trailing newline (page embed convention, accepted in round 1).",
        "Naming note (not a FAIL): the label iterate_equals_n_period_recursion (embedded code at L08.html:280) compares U^n with V_(H-n) of the 6-period recursion. That V_(H-n) is by definition the n-period value with terminal reward B=0 (= U^0 here), so the label and L08.html:311 are accurate.",
        "Round-1 wording fixed and re-verified: L07.html R1 solution no longer repeats the sentence about Theorem 2.2 (L07.html:440). Round-1 card c199 (C, Lab 1 Part A 'Run at every t') was rewritten as T (M1 values); round-1 card c224 was rewritten; both are correct now.",
        "Scope note: the slice is L07, L08, their twins and their 40 cards (lesson L07 or L08 in cards.json). The hub row M7c-r1-hub-L08-card-error-claim is in the slice because it restates L08's claim and is still wrong.",
    ],
    "summary": (
        f"M7 slice c round 2 (L07, L08, twins, 40 cards). {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
        f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Every L07/L08 proof, number, lab claim and card re-derived at 9294b914 with "
        "scripts under ledgers/M7/scripts/M7-c-r2/; all gates run pass. The single FAIL is the hub card line index.html:150, "
        "which still promises an 'error reported' that the L08 lab does not print; the lesson text and the twin are correct."
    ),
    "what_not_checked": [
        "render_curriculum.py, build_site.py --check, fetch_data.py --check: outside this slice (curriculum, tools, site data and MANIFEST unchanged since aeb512b6).",
        "Full pytest suite: only the two M7 lab cases were run (test_labs for lab-M7-L07-1 and lab-M7-L08-1).",
        "run_graders.py, mutate_graders.py and the five alternative implementations: project grader, not in this slice.",
        "Visual inspection of rendered pages in a browser: page_smoke geometry, Pyodide and console checks ran; the pages contain no figures.",
        "Live verify_refs (no network run): the slice cites no registry key.",
    ],
}

out = ROOT / "ledgers/M7/M7-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "verdict", verdict)
