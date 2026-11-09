"""Writes the round-4 verifier fragment for M2 slice c (L13-L18) to ledgers/M2/M2-c.json.

Every row's evidence names the script or output that backs it (repository paths under
ledgers/M2/scripts/M2-c-r4/ or, for carried rows, ledgers/M2/scripts/M2-c-r3/ and the delta output).
"""
import json
import subprocess
import sys

ROOT = sys.argv[1]
PIN = subprocess.run(["git", "-C", ROOT, "rev-parse", "edbb7aa8"], capture_output=True, text=True, check=True).stdout.strip()
BASE = "8196077d5f56c3919d33e69888176d197d378ad4"
S = "ledgers/M2/scripts/M2-c-r4/"
R3 = "ledgers/M2/scripts/M2-c-r3/"
CARRY = "Carried from round 3 (files byte-identical since the previous pin 8196077d: L13.html, L16.html, lab-M2-L13-1.py to lab-M2-L18-1.py; delta hunks listed in S01 do not touch the cited locators): "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (fresh at pin edbb7aa8)
row("M2c-gate-check-pages", "2.9-structure", "tools/check_pages.py --unit M2", "PASS",
    S + "g01_check_pages_M2.out: 'check_pages M2: PASS', rc=0 (run this round).")
row("M2c-gate-check-dag", "2.9-dag", "tools/check_dag.py --unit M2", "PASS",
    S + "g02_check_dag_M2.out: 'check_dag M2: PASS', rc=0 (run this round).")
row("M2c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M2 --page L13..L18", "PASS",
    S + "g04_run_labs_L13.out .. g04_run_labs_L18.out: each 'run_labs M2: PASS (1/1)', rc=0 (run this round, one call per page).")
row("M2c-gate-check-projects", "2.6-projects-gate", "tools/check_projects.py --unit M2", "PASS",
    S + "g03_check_projects_M2.out: 'check_projects M2: PASS', rc=0 (run as a gate; project slice is owned elsewhere).")
row("M2c-gate-page-smoke", "2.9-page-smoke", "tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18", "PASS",
    S + "g05_page_smoke_L13_L18.out: each page 'page_smoke ...: PASS', 'page_smoke M2: PASS', rc=0, 15 s (run this round).")
row("M2c-gate-pytest", "2.5-labs-pytest", "pytest tests/test_labs.py -k M2", "PASS",
    S + "g09_pytest_labs_M2.out: 27 passed, rc=0; collect-only count 27 (run this round).")
row("M2c-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2", "PASS",
    S + "g10_verify_refs_offline.out '560 entries, 0 problems' rc=0; " + S + "g11_verify_refs_unit_M2_live.out 'live re-verification of M2: 2 of 560 entries, 0 problems' rc=0 (both run this round). references/ byte-identical since the previous pin (git diff).")
row("M2c-labs-lint", "2.5-labs-lint", "tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py", "PASS",
    S + "g07_ruff_mypy_twins.out: ruff check 'All checks passed!', ruff format --check '6 files already formatted', mypy --no-incremental 'Success: no issues found in 6 source files' (run this round).")
row("M2c-labs-data", "2.8-data", "six twins; L13-L18 lab sections", "PASS",
    S + "s02_banned_and_process.out: twin file/network tokens [] for all six twins; data-files, data-chart, figure, svg markup 0 on all six pages. " + CARRY + R3 + "g06_twins_isolated_L13_L18.out.")

# ---- attribution, grades, data/figures, notation, banned, process, DAG, terms, hours, structure
row("M2c-attribution", "2.1-attribution", "L13-L18 References sections and body text", "PASS",
    S + "s04_attribution_registry.out: data-cite 0 and data-locator 0 on all six pages; Spivak/Hubbard/Velleman occur only in the References sections, which state no passage locator. The delta adds no citation (git diff of the six pages).")
row("M2c-grades", "2.3-grades", "L13-L18 claim titles, grade spans, Key results", "PASS",
    S + "s01_mechanical_delta.out: claim_titles and grades IDENTICAL for all six pages between 8196077d and edbb7aa8 (counts L13 4/14, L14 2/12, L15 6/14, L16 2/11, L17 2/11, L18 3/13). Delta hunks (S01 header list) contain no data-grade change, so the round-3 grade re-grading stands; round-3 re-grade output " + R3 + "grades_scan.out.")
row("M2c-data-figures", "2.8-figures", "L13-L18 (no data-files, no chart or figure markup)", "PASS",
    S + "s02_banned_and_process.out: 'data/figure markup: 0' on L13 to L18. No dataset is read and no figure is drawn, so no MANIFEST row or figure controls apply.")
row("M2c-notation", "2.4-notation", "L13-L18 math; notation/notation.json", "PASS",
    "Fresh scan this round (command output in the transcript, script " + S + "s06_notation_hours_hub.py, output s06_notation_hours_hub.out): no \\Phi, \\gamma, \\ast, \\mathbb{Q}, R_f, R^{e}, \\SR, and no \\mathbb on any slice page (T used only as prose). Notation registry 'about' says letters conventionally local are defined per lesson; the new local letters are psi, omega, rho, k, C (L17 E2, L18 Theorem 4.1, L14 Prop 3.1, L18 Prop 3.2); \\varphi in L17 P2 is an angle, so psi in E2 avoids a collision (L17 lines 266-268 vs 293).")
row("M2c-banned-scan", "2.9-banned", "L13-L18 HTML, six twins, slice cards", "PASS",
    S + "s02_banned_and_process.out: 0 hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, the ellipsis character, on all six pages, all six twins and the 103 slice cards. One three-dot sequence ellipsis appears in a displayed docstring (L15 line 193 and twin line 34: 'angles 0, 2 pi/count, 4 pi/count, ...'); it is a sequence pattern whose every term the code computes, not omitted content, so it is not a banned placeholder (recorded in notes).")
row("M2c-process-words", "2.9-process-words", "L13-L18 learner text; slice cards", "PASS",
    S + "s02_banned_and_process.out: 0 hits for architect, builder, verifier, planner, ledger, fanout, round N, page_smoke, run_labs, check_pages, check_dag, embed_labs, MCP, fixer, slice, pin, Ruling, KNOWN, blind on the six pages, six twins and slice cards.")
row("M2c-dag-forward-mentions", "2.9-dag", "L13-L18 concept links and names", "PASS",
    S + "s01_mechanical_delta.out: concept_links IDENTICAL for all six pages. Links: L13 {derivative, exponential-and-logarithm, finite-difference-derivative, limit, taylor-theorem}; L14 {automatic-differentiation (own, dfn at L14), derivative, finite-difference-derivative (L13)}; L15 {limit}; L16 {derivative, finite-difference-derivative, partial-derivative}; L17 {gradient, partial-derivative}; L18 {jacobian (own)}. Every link is to a prerequisite or an earlier lesson; check_dag PASS (g02). Prose-only names in the delta (chain rule in L18 R2, value part and tangent in L14 Section 2) are not concepts in the registry for M2 or are defined in the same block.")
row("M2c-terms-before-definition", "2.9-order", "L14.html:73 vs :80 (Assumption 1 paragraph); L18.html:340 (R2 solution)", "PASS",
    CARRY + "L14 line 73 (Definition 2.1) still cites Assumption 1, whose paragraph moved from line 79 to line 80 by the one-line insertion at line 75 (text byte-identical). L18 R2 (line 340, now changed) uses only Definition 2.1 (line 61), Definition 3.1 (line 72), Problem P2 (line 287) and terms defined in its own solution (K); it is not used before definition.")
row("M2c-hours", "2.9-hours", "course/modules/M/M2/index.html line 29; L13-L18 data-hours", "PASS",
    S + "s01_mechanical_delta.out and grep: index.html line 29 data-hours-lessons=240, data-hours-project=60 (240+60=300 = curriculum); L13..L18 data-hours=10 each (24 lessons x 10 h = 240). The delta changes the hub's skill-check items and L21 card text only (git diff hunks at index.html lines 124 and 161), not the hours.")
row("M2c-structure", "2.9-structure", "L13-L18 HTML", "PASS",
    S + "s05_structure_and_cards.out: why-it-matters words 106, 102, 89, 95, 83, 107 (limit 120); 3 misconceptions each; 12 problems each (M1-M3, P1-P3, E1-E3, R1-R3); quiz items 10, 10, 10, 10, 10, 9 (8-15); key-results rows 8, 6, 8, 5, 5, 7. Counts identical to the previous pin (s01).")
row("M2c-quiz-keys", "2.9-quiz", "L14 quiz item 7; L15 quiz item 7; other items", "PASS",
    "Re-checked this round: L14 quiz item 7 (line 494-500) keys '-1' for 'x if x.val > 0 else -x' at 0+1eps; s03_changed_hunks_numbers.out shows tangent -1 for that program. L15 quiz item 7 (line 438-442) keys the single option 'Each point of the set has a ball of some radius inside the set'. Other items unchanged (s01 quiz_items counts identical; the delta changes only items 7).")

# ---- L13 (byte-identical lesson and twin: carried)
row("M2c-L13-numbers", "2.2-numbers", "L13.html Example 2.3, Lab 1 prose, Sections 2-5, Problems, Key results, Misconceptions 1-2", "PASS",
    CARRY + R3 + "numbers_L13.py / numbers_L13.out and numbers_L13b.py / numbers_L13b.out; tie_check_L13.out. Printed-value agreement re-checked this round in the lab output (" + S + "twin_L13.stdout).")
row("M2c-L13-theorems", "2.4-mathematics", "L13.html Thm 2.1, 2.2, Prop 3.2, Cor 4.1, Problems M1-M3, P1-P3, Section 5, Assumption 1", "PASS",
    CARRY + "round-3 hand re-derivation of Theorem 2.1, 2.2 (Lagrange remainders), Prop 3.2 and Corollary 4.1 (r3 notes); file byte-identical.")
row("M2c-L13-lab1", "2.5-labs", "L13.html Lab 1 (lab-M2-L13-1)", "PASS",
    CARRY + "twin run alone under python -I -W error this round: " + S + "twin_L13.stdout (rc 0, stderr empty) reproduces the page's expected block; run_labs PASS (g04).")
row("M2c-L13-prose", "2.9-prose", "L13.html Assumption 1 (line 98), Section 5, Misconceptions, Key results, quiz", "PASS",
    CARRY + "file byte-identical; banned, process and notation scans re-run this round (s02) with 0 hits.")
row("M2c-L13-lab-embed", "2.5-labs-embed", "L13.html lab-M2-L13-1 vs tests/labs/M2/lab-M2-L13-1.py", "PASS",
    CARRY + R3 + "lab_embed_check_r3.out (code_equals_twin=True, expected_equals_output=True); run_labs PASS this round (g04_run_labs_L13.out).")

# ---- L14
row("M2c-L14-numbers", "2.2-numbers", "L14.html Example 4.1, Example 5.1, Lab 1 prose, E1, Key results rows 1-4", "PASS",
    CARRY + "cited locators are outside the L14 delta lines (75, 95-97, 289, 413-415, 494, 500); " + R3 + "numbers_L14.py / numbers_L14.out; Key results row 4 at line 434 unchanged.")
row("M2c-L14-theorems", "2.4-mathematics", "L14.html Def 2.1, Prop 3.1, Prop 5.2, P1-P3, R1-R3, Section 6 branch examples", "PASS",
    S + "s03_changed_hunks_numbers.out: sum, product and quotient of Definition 2.1 agree with the lab Dual class on 500 random exact rationals; quotient tangent (g'k - gk')/k^2 checked. Prop 3.1 proof (lines 95-97, renamed H to k) re-derived: sum rule, product rule, quotient rule, all with k(a) nonzero. R3 (413-415) and Section 6 bullet 1 (289) re-derived with the twin's Dual class. Prop 5.2, P1-P3, R1-R2 and Example 4.1/5.1 unchanged (carry).")
row("M2c-L14-assumption1-order", "2.9-order", "L14.html:73 vs the Assumption 1 paragraph (now line 80)", "PASS",
    CARRY + "text byte-identical; line 73 still reads 'The exponential and sine rules hold under Assumption 1'. The forward mention of a numbered Assumption is not a defined term; kept PASS as in rounds 2 and 3.")
row("M2c-L14-lab1", "2.5-labs", "L14.html Lab 1 (lab-M2-L14-1)", "PASS",
    S + "twin_L14.stdout (rc 0, stderr empty): 'grid points: 251', both max-error lines True, f1(2)=15.2327609113, f1'(2)=21.7317705218 by dual numbers and by closed form, f2'(1)=2.5067615350; run_labs PASS (g04). Page Lab 1 lines unchanged (carry).")
row("M2c-L14-keyresult-grade", "2.3-grades", "L14.html:434 (Key results row 4)", "PASS",
    CARRY + "row 4 at line 434 unchanged; round-2 fix stays. Row 5 (line 436, branch tangent, grade T) re-checked: the branch convention is now stated in Definition 2.1 (line 75), so the T claim is derived on the page from Definition 2.1 (basis stated in the row).")
row("M2c-L14-lab-embed", "2.5-labs-embed", "L14.html lab-M2-L14-1 vs tests/labs/M2/lab-M2-L14-1.py", "PASS",
    S + "g04_run_labs_L14.out PASS (run_labs compares the page code with the twin byte for byte and the expected block with the printed output); " + R3 + "lab_embed_check_r3.out.")
row("M2c-L14-branch-comparison", "2.4-mathematics", "L14.html:75 (convention), :289 (Section 6), :413-415 (R3), :436 (key row 5), :494-500 (quiz 7); cards.json M2-c212, M2-c218", "PASS",
    "Round-3 FAIL fixed. Definition 2.1 now states the convention (line 75): a branch test reads the value part a and ignores the tangent b; code writes x.val > 0. The lab Dual class defines .val (lab-M2-L14-1.py lines 21-24). s03_changed_hunks_numbers.out: 'x if x.val > 0 else -x' at 0+1eps gives tangent -1, 'x if x.val >= 0 else -x' gives +1, 'x if x.val > 0 else 0' gives 0, 'x if x.val >= 0 else 0' gives 1; max(x,0) equal to the first program at 2000 random points. All five locators agree with these values.")
row("M2c-L14-prose", "2.9-prose", "L14.html Section 6 bullet 1 (289), Misconceptions (300-310), Remark (423), problem sets", "PASS",
    "Round-3 FAIL fixed. Section 6 bullet 1 now reads x.val, tests the value part 0 > 0 (false), takes the else branch -x and returns 0 - 1eps, tangent -1; matches s03 output. Misconception 3 (line 310) says the branch example gives -1 and +1 for |x| at 0, consistent. R3 solution (415) and quiz 7 explain (500) consistent. Remark (423) and other sections unchanged (carry).")

# ---- L15
row("M2c-L15-numbers", "2.2-numbers", "L15.html Prop 3.5, E1, E3, R3, Lab 1 interpretation (230), Section 4 bullet 2", "PASS",
    CARRY + R3 + "numbers_L15.py / numbers_L15.out (exact max |cos^2 sin| = 2/(3 sqrt 3) = 0.3849001795); delta hunks at lines 438, 442 only.")
row("M2c-L15-theorems", "2.4-mathematics", "L15.html Prop 2.1, 2.2, Def 2.3, Ex 2.4, Prop 3.1, Cor 3.2, Ex 3.3, Ex 3.4, Prop 3.5, Prop 3.6, Problems", "PASS",
    CARRY + "Definition 2.3 (lines 88-89) and the other statements unchanged; hunks at 438 and 442 are quiz text only.")
row("M2c-L15-lab1", "2.5-labs", "L15.html Lab 1 (lab-M2-L15-1) and interpretation (230)", "PASS",
    S + "twin_L15.stdout (rc 0, stderr empty) reproduces the sampled-maximum table; run_labs PASS (g04). Page Lab 1 unchanged (carry).")
row("M2c-L15-prose", "2.9-prose", "L15.html Section 4, Section 5 misconceptions, Key results rows 1-8, Remark (360)", "PASS",
    CARRY + "misconceptions 1-3 at lines 247-256 and key results unchanged; s01 blocks and misconceptions identical.")
row("M2c-L15-quiz-q7-two-correct", "2.9-quiz", "L15.html:436-442 (quiz item 7); Definition 2.3 (lines 88-89)", "PASS",
    "Round-3 FAIL fixed. The distractor now reads 'Every point of R^n is the centre of a ball lying inside the set'. Only the keyed option is a correct reading for every open set: the distractor holds only for U = R^n (any ball about x not in U contains x, which is outside U, so 'every point of R^n' forces U = R^n), and 'U has no boundary points' fails for U = (0,1). The explanation (line 442) states exactly this. Verified by reading Definition 2.3 (line 89) and the option text.")
row("M2c-L15-lab-embed", "2.5-labs-embed", "L15.html lab-M2-L15-1 vs tests/labs/M2/lab-M2-L15-1.py", "PASS",
    S + "g04_run_labs_L15.out PASS; " + R3 + "lab_embed_check_r3.out.")

# ---- L16 (byte-identical, carried)
row("M2c-L16-numbers", "2.2-numbers", "L16.html Example 1.3, Prop 2.1 prose, Lab 1, E1, E3, R3, Key results", "PASS",
    CARRY + R3 + "numbers_L16_L17_L18.py / .out (F_x(1,2)=4+2e^2=18.778112198, F_y(1,2)=1+e^2=8.389056099).")
row("M2c-L16-theorems", "2.4-mathematics", "L16.html Remark 1.2, Prop 2.1, Prop 3.1, Problems P1-P3, R1-R2, Assumption 1", "PASS",
    CARRY + "file byte-identical (s01 and git diff).")
row("M2c-L16-lab1", "2.5-labs", "L16.html Lab 1 (lab-M2-L16-1)", "PASS",
    S + "twin_L16.stdout (rc 0, stderr empty); run_labs PASS (g04). File byte-identical.")
row("M2c-L16-prose", "2.9-prose", "L16.html Sections 3-4, Misconceptions 1-3, Key results, quiz 1-10", "PASS",
    CARRY + "file byte-identical; s02 scans 0 hits.")
row("M2c-L16-lab-embed", "2.5-labs-embed", "L16.html lab-M2-L16-1 vs tests/labs/M2/lab-M2-L16-1.py", "PASS",
    S + "g04_run_labs_L16.out PASS; " + R3 + "lab_embed_check_r3.out.")

# ---- L17
row("M2c-L17-numbers", "2.2-numbers", "L17.html E2 (changed), Example 1.2, Example 2.3, Lab 1, E3, R1, Section 4 bullet 4", "PASS",
    S + "s03_changed_hunks_numbers.out: psi''' = 6u1^2 u2 - u2^3 cos y matches a 7-point difference (relative error 2.4e-5 at step 1e-2); |psi'''| <= 7 on 200 unit directions; truncation (t^2/6)*7 = 1.1667e-12 (lesson: about 1.2e-12); 2^-53 = 1.110e-16 and delta/t = 1.110e-10 (lesson: order 1e-10); measured central-difference error over 200 directions at t=1e-6 is 8.7e-10, below 1e-6. Twin prints 'below 1e-6: True' (twin_L17.stdout). Other L17 numbers unchanged: " + R3 + "numbers_L16_L17_L18.py / .out.")
row("M2c-L17-theorems", "2.4-mathematics", "L17.html Def 1.1, Def 2.1, Thm 2.2, Example 2.3, Thm 3.1, Section 4, Problems M1-M3, P1-P3, R2, R3", "PASS",
    CARRY + "the delta touches only E2 (line 293) of L17, which is not among the cited statements; s01 blocks and claim titles identical.")
row("M2c-L17-lab1", "2.5-labs", "L17.html Lab 1 (lab-M2-L17-1)", "PASS",
    S + "twin_L17.stdout (rc 0, stderr empty): 360 directions, 'below 1e-6: True', gradient (1.000000, 1.877583), magnitude 2.127279, angle 61.96 degrees, 'agrees with the magnitude to 1e-4: True'; run_labs PASS (g04).")
row("M2c-L17-prose", "2.9-prose", "L17.html Section 4 bullets 1-4, Misconceptions 1-3, Key results, quiz 1-10", "PASS",
    CARRY + "unchanged (s01 identical counts; delta line 293 only).")
row("M2c-L17-lab-embed", "2.5-labs-embed", "L17.html lab-M2-L17-1 vs tests/labs/M2/lab-M2-L17-1.py", "PASS",
    S + "g04_run_labs_L17.out PASS; " + R3 + "lab_embed_check_r3.out.")

# ---- L18
row("M2c-L18-numbers", "2.2-numbers", "L18.html Example 4.2, Lab 1 prose, E1-E3, Key results, Section 5 R1 partial formula", "PASS",
    CARRY + R3 + "numbers_L16_L17_L18.py / .out (remainder identity at s=(0.3,-0.2) gives (0.05,-0.12)); delta hunks at lines 87, 113, 340 only. Lab output re-run: " + S + "twin_L18.stdout (25 grid points, error below 1e-6 True, Jacobian rows 2 -4 / 4 2, remainders 1e-1..1e-4).")
row("M2c-L18-theorems", "2.4-mathematics", "L18.html Prop 3.2 (proof, line 87), Prop 3.3 (proof, 91-97), Theorem 4.1 (proof, 113)", "PASS",
    S + "s03_changed_hunks_numbers.out: |Ah| <= K|h| with K = sum |A_ij| on 2000 random matrices; uniqueness identity (A-C)tv = [F(a+tv)-F(a)-Ctv] - [F(a+tv)-F(a)-Atv] checked. Prop 3.2 (line 87) now uses C for the second matrix; the argument is correct: dividing by t and letting t -> 0 gives |(A-C)v| = 0 for every unit v. Prop 3.3 re-derived. Theorem 4.1 proof (line 113): MVT on s -> F_i(p_{k-1}+s e_k) on [0,h_k] (partial exists on the whole ball B(a,r)); q_k within |h| of a; telescoping identity; omega(rho) = supremum over |x-a| <= rho, finite for small rho because each partial is continuous at a; omega(rho) -> 0; bound sqrt(m) n omega(|h|)|h| gives ratio -> 0. The round-3 'largest' wording is now 'supremum' with the finiteness sentence; the theorem's statement (line 105-107) and the Key results row (361) match.")
row("M2c-L18-lab1", "2.5-labs", "L18.html Lab 1 (lab-M2-L18-1)", "PASS",
    S + "twin_L18.stdout (rc 0, stderr empty): 'grid points: 25', 'max entry error ... below 1e-6: True', Jacobian rows, remainder lines; run_labs PASS (g04). File byte-identical.")
row("M2c-L18-R2-result-named", "2.9-prose", "L18.html:340 (Problem R2 solution)", "PASS",
    "Round-3 FAIL fixed. The solution now says 'The candidate is the chain rule ...', 'This lesson does not prove the chain rule', and 'The chain rule is not proved on this page'. The earlier 'The result is the chain rule' next to 'does not state' is gone, so the statement is not self-contradictory. The proof sketch is labelled as a sketch ('A proof sketch would apply Definition 3.1 ...') and is not presented as a proof.")
row("M2c-L18-R2-solution-numbers", "2.2-numbers", "L18.html Problem R2 solution (line 340); Problem P2 (287-289)", "PASS",
    S + "s03_changed_hunks_numbers.out: |Ah| <= K|h| with K = sum |A_ij| (2000 random cases); P2 solution (line 289) proves the same bound with |v| <= sum |v_i|. The solution contains no other numerical claim.")
row("M2c-L18-prose", "2.9-prose", "L18.html Section 5 bullets 1-4, Misconceptions 1-3, Assumption 1 (line 250), Key results, quiz 1-9", "PASS",
    CARRY + "unchanged (s01 identical counts; delta lines 87, 113, 340 only).")
row("M2c-L18-lab-embed", "2.5-labs-embed", "L18.html lab-M2-L18-1 vs tests/labs/M2/lab-M2-L18-1.py", "PASS",
    S + "g04_run_labs_L18.out PASS; " + R3 + "lab_embed_check_r3.out.")

# ---- cards
row("M2c-cards-sample-01", "2.7-cards", "cards.json M2-c181 .. M2-c190 (L13)", "PASS",
    CARRY + "the card objects are byte-identical between the pins (s01 'cards changed' lists only c058, c068, c069, c212, c225, c417, c418 unit-wide).")
row("M2c-cards-sample-02", "2.7-cards", "cards.json M2-c191 .. M2-c200 (L13)", "PASS",
    CARRY + "identical card objects (s01). Numbers rechecked by " + R3 + "cards_check_r3.out.")
row("M2c-cards-sample-03", "2.7-cards", "cards.json M2-c201, M2-c380, M2-c381, M2-c202 .. M2-c208 (L13-L14)", "PASS",
    CARRY + "identical card objects (s01).")
row("M2c-cards-sample-04", "2.7-cards", "cards.json M2-c209 .. M2-c218 (L14); M2-c212 and M2-c218", "PASS",
    "Round-3 FAIL fixed. M2-c212 now reads 'x.val > 0' and 'x.val >= 0' with tangents 0 and 1 (s03 output); matches R3 and quiz 7. M2-c218 states the branch example gives -1 or +1 for |x| at 0 (Misconception 3, line 310), which the convention in line 75 makes true. Cards c209-c211, c213-c217 are identical JSON objects (s01) and their statements (Prop 3.1, Section 6 jumps, Misconception 1) are unchanged.")
row("M2c-cards-sample-05", "2.7-cards", "cards.json M2-c219 .. M2-c228 (L14-L15); M2-c225 (cards.json lines 1586 and 1589)", "PASS",
    "Round-3 FAIL fixed. M2-c225 locator now reads 'the paragraph after Example 2.4; Misconception 3': L15.html line 97 is the paragraph after Example 2.4 (line 93 title), and the misconception 'The closed disc ... is open' is the third misconception (lines 254-256). The card's statement is true (checked against line 97 and Example 2.4). Cards c219-c224 and c226-c228 are identical objects (s01); c228 is T and its statement (|f| <= |y| <= |(x,y)|) is correct.")
row("M2c-cards-sample-06", "2.7-cards", "cards.json M2-c229 .. M2-c238 (L15); M2-c234", "PASS",
    CARRY + "identical card objects (s01): c234 'f(1/n,1/n)=1/(2n)' and c229 'g along (1/k,1/k) gives 1/2' re-derived this round (exact arithmetic: x^2 y/(x^2+y^2) at (1/n,1/n) = 1/(2n); xy/(x^2+y^2) = 1/2).")
row("M2c-cards-sample-07", "2.7-cards", "cards.json M2-c239 .. M2-c249 (L16)", "PASS",
    CARRY + "identical card objects (s01).")
row("M2c-cards-sample-08", "2.7-cards", "cards.json M2-c251 .. M2-c260 (L17)", "PASS",
    CARRY + "identical card objects (s01).")
row("M2c-cards-sample-09", "2.7-cards", "cards.json M2-c261 .. M2-c270 (L17-L18)", "PASS",
    CARRY + "identical card objects (s01).")
row("M2c-cards-sample-10", "2.7-cards", "cards.json M2-c271 .. M2-c279 (L18)", "PASS",
    CARRY + "identical card objects (s01).")
row("M2c-cards-sample-11", "2.7-cards", "cards.json M2-c406, M2-c413, M2-c415, M2-c419 (L14, L15)", "PASS",
    CARRY + "identical card objects (s01). M2-c419 (g(1/n,1/n)=1/2) is a different fact from M2-c234 (f(1/n,1/n)=1/(2n)); the 0.96 surface similarity is a different function, not a duplicate.")
row("M2c-cards-duplicates", "2.7-duplicates", "cards.json unit-wide (394 cards)", "PASS",
    S + "s05_structure_and_cards.out: 0 exact duplicate fronts unit-wide; 0 duplicate ids (s01). Near-duplicate slice fronts (ratio >= 0.80): c182/c183, c188/c189, c191/c192, c194/c195, c228/c229, c232/c233, c234/c419 are distinct facts (theorem errors for forward vs central quotient; two lab values; two functions); none is a repeated card.")
row("M2c-cards-numbers", "2.7-numbers", "cards.json slice backs vs lesson text", "PASS",
    S + "s05_structure_and_cards.out: M2-c212 and M2-c225 carry no number with three or more decimals or scientific notation. The other slice cards are identical objects (carried), and their numbers were checked against the lesson text in " + R3 + "cards_check_r3.out.")
row("M2c-cards-grades", "2.7-grades", "cards.json slice cards (103: T 66, C 22, no grade 15)", "PASS",
    S + "s05_structure_and_cards.out: grades T 66, C 22, none 15; no C card lacks a basis; no T card carries a basis field.")
row("M2c-cards-coverage", "2.7-coverage", "cards.json slice cards vs lesson definitions, theorems, examples, labs, misconceptions", "PASS",
    S + "s01_mechanical_delta.out: blocks (definition/theorem/proposition/corollary/example/remark/proof), misconception count and problem count identical for all six pages, so no definition, theorem or misconception was added or removed. The new branch convention (L14 line 75) is covered by M2-c212 and M2-c218; the hunks in L15, L17, L18 change no statement that had a card other than M2-c225 (re-checked above). Carried otherwise.")

# ---- changed hunks (explicit delta rows)
row("M2c-delta-L14-section2", "2.4-mathematics", "L14.html:75 (new branch paragraph inside Definition 2.1)", "PASS",
    S + "s03_changed_hunks_numbers.out: the x.val convention and the value/tangent reading match the lab Dual class (.val, .dot) and the four program outputs.")
row("M2c-delta-L14-prop31-proof", "2.4-mathematics", "L14.html:95-97 (Prop 3.1 sum, product, quotient)", "PASS",
    S + "s03_changed_hunks_numbers.out: sum, product, quotient formulas and tangents match Definition 2.1 on 500 random cases; the renaming H -> k is consistent within each sentence (checked by reading lines 95-97).")
row("M2c-delta-L14-section6-R3-quiz", "2.9-prose", "L14.html:289, 413-415, 494, 500", "PASS",
    S + "s03_changed_hunks_numbers.out (branch tangents -1, +1, 0, +1; max(x,0) identity). Each changed sentence agrees with these values.")
row("M2c-delta-L15-quiz7", "2.9-quiz", "L15.html:438, 442", "PASS", "See M2c-L15-quiz-q7-two-correct (the distractor and explanation are correct and exact).")
row("M2c-delta-L17-E2", "2.2-numbers", "L17.html:293 (E2 solution)", "PASS", "See M2c-L17-numbers: psi''' formula, bound 7, error estimates 1.2e-12 and 1e-10 re-derived (" + S + "s03_changed_hunks_numbers.out).")
row("M2c-delta-L18-proofs-R2", "2.4-mathematics", "L18.html:87, 113, 340", "PASS", "See M2c-L18-theorems and M2c-L18-R2-result-named (both re-derived this round).")
row("M2c-delta-cards-slice", "2.7-cards", "cards.json M2-c212, M2-c225 (the only slice cards changed)", "PASS", "See M2c-cards-sample-04 and -05 (re-derived this round). Unit-wide changes outside the slice (c058, c068, c069, c416 removed, c417, c418, c421 added; lessons L05, L06, L08, L10) are not in this slice and are not verified here.")

# ---- verdict
status_counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if status_counts["PASS"] == len(rows) else "FAIL"

fragment = {
    "unit": "M2",
    "slice": "c",
    "round": 4,
    "verifier": "Haiku 5.5 independent verifier (fanout S4 slice c, round 4, final full verification under ruling 26)",
    "pin": PIN,
    "base": "round 3 fragment /Users/billyribeiro/.fanout/frags/S-M2-c.round3.json at pin " + BASE + " (context; PASS rows carried only where cited subjects are byte-identical; FAIL rows re-verified from scratch). Delta " + BASE[:8] + ".." + PIN[:8] + ": L14, L15, L17, L18 hunks (S01 header), cards.json (c212, c225 in slice), index.html hub (not slice).",
    "checkout": ROOT,
    "scratch": "/tmp/m2c_r4_cards_old.json, /tmp/m2c_r4_cards_new.json (cards snapshots only; all scripts kept under " + S + ")",
    "verified_at": "2026-11-09T07:35:34Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none required. Slice c is lesson pages and lab twins; VERIFIER_RULES 2.6 mutation testing applies to project graders (rulings: lab twins are demonstrations). The twins were run alone under python -I -W error (twin_L13..L18.stdout).",
        "Ruling 26 (round 4 is the last full verification for tag S): every row is PASS, so no row of the blocking kinds (false or unproved statement, missing hypothesis, wrong number, over-grade, failing gate, surviving non-equivalent mutant, lab statement the code does not support) is open in this slice. No LOW row is open either.",
        "Out-of-slice observation for the hub verifier (not a row of slice c): course/modules/M/M2/index.html (rung 2 skill check, data-answer 12.02) says 'Lesson 13 builds' the central second difference (f(x+h)-2f(x)+f(x-h))/h^2 from the expansions. L13 gives the two Taylor expansions (lines 91-92) and subtracts them for the first difference (line 93); it never adds them or states the second difference, so the attribution to L13 is not supported by L13's text. The arithmetic (1.1^4+0.9^4-2)/0.01 = 12.02 is correct. Suggested fix for the hub: say the second difference follows from adding the two expansions of Lesson 13, or cite the step the lesson omits.",
        "Observation, not a banned placeholder: the three-dot sequence in the L15 docstring and twin (angles 0, 2 pi/count, 4 pi/count, ...) continues a pattern the code computes in full.",
        "Observation: the central-difference bound in L17 E2 says 'for y near a' although |cos y| <= 1 holds everywhere; the bound is correct globally, so the hedge is harmless.",
        "Observation: Assumption 1 is cited in Definition 2.1 (L14 line 73) before its paragraph (line 80); carried PASS as in rounds 2 and 3.",
        "Cards outside this slice changed in the delta (M2-c058, c068, c069, c416 removed, c417, c418, c421 added; lessons L05, L06, L08, L10); not verified in this slice.",
        "Not run: run_graders (project slice), check_pages/check_dag for other units, build_site --check, render_curriculum, full pytest suite, the full repository ruff/mypy gate (only the six twins were linted and type-checked), and visual screenshots of the lab figures (the pages carry no figures). page_smoke was run for the six slice pages only.",
        "Live reference check run this round: verify_refs --unit M2 (2 of 560 entries, 0 problems). Other registry keys not cited by M2 body text were not re-resolved beyond the offline integrity pass."
    ],
    "summary": "PASS: %d rows (all PASS; fail=0, unverifiable=0). Round-3 FAILs (M2c-L14-branch-comparison, M2c-L14-prose, M2c-cards-sample-04, M2c-L15-quiz-q7-two-correct, M2c-cards-sample-05, M2c-L18-theorems, M2c-L18-R2-result-named) re-verified from scratch at edbb7aa8 and PASS. All gates pass (check_pages, check_dag, check_projects, run_labs x6, page_smoke x6, pytest -k M2 27/27, ruff, mypy on twins, verify_refs offline and live M2)." % len(rows),
}

import importlib.util
spec = importlib.util.spec_from_file_location("ledger", f"{ROOT}/tools/ledger.py")
mod = importlib.util.module_from_spec(spec)
sys.path.insert(0, f"{ROOT}/tools")
spec.loader.exec_module(mod)
problems = mod.validate(fragment, "M2-c")
print("validate:", problems)
print("status counts:", status_counts, "verdict:", verdict)
with open(f"{ROOT}/ledgers/M2/M2-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", f"{ROOT}/ledgers/M2/M2-c.json", "rows", len(rows))
