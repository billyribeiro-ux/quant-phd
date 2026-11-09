"""Writes the round-2 M5 slice-c fragment (ledgers/M5/M5-c.json) from the rows the verifier recorded."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
O = "ledgers/M5/scripts/M5-c-r2/out/"
CARRY = "Carried from round 1 (course/modules/M/M5/{f}.html byte-identical since the previous pin aeb512b6): "

def P(i, check, loc, ev):
    return {"id": i, "check": check, "location": loc, "status": "PASS", "evidence": ev}

def F(i, check, loc, ev, fix):
    return {"id": i, "check": check, "location": loc, "status": "FAIL", "evidence": ev, "fix": fix}

rows = [
    P("M5c-gate-check-pages", "2.9 structure (check_pages)", "course/modules/M/M5 (L08-L10, cards.json)",
      "Command: .venv/bin/python tools/check_pages.py --unit M5 -> 'check_pages M5: PASS', exit 0 (" + O + "check_pages.out)."),
    P("M5c-gate-check-dag", "2.9 DAG (check_dag)", "course/modules/M/M5 pages",
      "Command: .venv/bin/python tools/check_dag.py --unit M5 -> 'check_dag M5: PASS', exit 0 (" + O + "check_dag.out). Prerequisite closure of M5 is M2 and M1; every concept used on L08-L10 is in it (see M5c-dag)."),
    P("M5c-gate-check-projects", "2.6 projects (check_projects, unit-level command row)", "course/modules/M/M5/project.html (outside slice)",
      "Command: .venv/bin/python tools/check_projects.py --unit M5 -> 'check_projects M5: PASS', exit 0 (" + O + "check_projects.out). Recorded for completeness; the project slice is verified elsewhere."),
    P("M5c-gate-run-labs", "2.5 labs (run_labs, unit-level)", "tests/labs/M5/* incl. lab-M5-L08-1, L09-1, L10-1",
      "Command: .venv/bin/python tools/run_labs.py --unit M5 -> 'run_labs M5: PASS (13/13)', exit 0 (" + O + "run_labs.out)."),
    P("M5c-twins-isolated", "2.5 twins alone under python -I -W error", "tests/labs/M5/lab-M5-L08-1.py, lab-M5-L09-1.py, lab-M5-L10-1.py",
      "Command: .venv/bin/python -I -W error <twin>; exit 0 and empty stderr for L08, L09, L10 (" + O + "twin-L0*.stderr). Stdout equals the expected block exactly (" + O + "page_twin_check.out)."),
    P("M5c-gate-page-smoke", "2.9 page_smoke for the slice pages, alone", "course/modules/M/M5/L08.html, L09.html, L10.html",
      "Command: .venv/bin/python tools/page_smoke.py --unit M5 --pages L0x for each page -> 'page_smoke modules/M/M5/L0x.html: PASS', exit 0; lab runtime 0.0 s for each (" + O + "page_smoke-L08.out, -L09.out, -L10.out)."),
    P("M5c-gate-ruff-mypy", "2.5 twins: ruff and mypy", "tests/labs/M5/lab-M5-L08-1.py, L09-1, L10-1",
      "Commands: .venv/bin/ruff check and ruff format --check on the three twins -> exit 0, '3 files already formatted' (" + O + "ruff.out); .venv/bin/mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files', exit 0 (" + O + "mypy.out)."),
    P("M5c-gate-pytest-labs", "2.5 relevant pytest", "tests/test_labs.py -k M5",
      "Command: .venv/bin/pytest tests/test_labs.py -q -k M5 -> 13 passed, exit 0 (" + O + "pytest_labs_M5.out)."),
    P("M5c-gate-verify-refs-offline", "2.1 citations (verify_refs --offline)", "references/references.json; slice pages",
      "Command: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + O + "verify_refs_offline.out). The slice cites no registry key: L08.html:490, L09.html:499, L10.html:610 say so."),
    P("M5c-lab-L08-1", "2.5 lab L08-1 (demonstration; rung not applicable)", "course/modules/M/M5/L08.html:136-271; tests/labs/M5/lab-M5-L08-1.py",
      "Page code block equals the twin after strip (" + O + "page_twin_check.out); printed lines equal the expected block L08.html:259-270 exactly. Independent recomputation (" + O + "independent_numbers.out): 257 iterations to gap 1e-12, V* = 5.000000, 5.176097, 5.284873, 5.366025, residual 8.695e-13, counts 40/257/527, one-point fixed point 5."),
    P("M5c-lab-L09-1", "2.5 lab L09-1 (demonstration)", "course/modules/M/M5/L09.html:130-274; tests/labs/M5/lab-M5-L09-1.py",
      "Page code equals the twin after strip; expected block L09.html:264-272 equals the output exactly (" + O + "page_twin_check.out). The changed docstring (twin lines 14-18, L09.html:146-150) states Lemma 2.3(c) with distance at most 1e-12 for the reference, which is correct since cert_n <= 1e-12. Independent recomputation (" + O + "independent_numbers.out): reference 278 iterations, certified 9.512e-13, stops 59/103/147 with actual error equal to certified, fixed count 10 gives 1.7433922005, naive stop n 126, step 9.534e-7, error 8.5808e-6."),
    P("M5c-lab-L10-1", "2.5 lab L10-1 (demonstration)", "course/modules/M/M5/L10.html:175-353; tests/labs/M5/lab-M5-L10-1.py",
      "Page code equals the twin after strip; expected block L10.html:340-351 equals the output exactly (" + O + "page_twin_check.out). Independent recomputation with Fractions (" + O + "independent_numbers.out): right and left errors equal (3n-1)/(6n^2) and -(3n+1)/(6n^2) for n = 4, 10, 100, 1000; Part B worst error/mesh 0.491631 and largest mesh 0.992962 with the lab's draw order; Part C and D reproduced in the twin output."),
    P("M5c-num-L08-worked", "2.2 numbers (c) derived", "L08.html:74, :133, :278, :319, :326, :369, :483",
      CARRY.format(f="L08") + "Re-checked this round in " + O + "independent_numbers.out: sqrt(0.75)=0.866025; V*=(1/2)/(1-beta)=10 at beta=0.95, u=1/2; E2 sqrt(0.707107-0.25)+0.9*5 = 5.176097; F(k) sets in M3 follow from k^(1/2)."),
    P("M5c-num-L08-counts", "2.2 numbers (a) computed; misc. E1 thresholds", "L08.html:293, :362, :455, :490",
      CARRY.format(f="L08") + "Re-derived in " + O + "independent_numbers.out: solver counts 40 (beta 0.5), 257 (0.9), 527 (0.95); a priori thresholds 40.6556, 282.7413, 594.2865 with least n 41, 283, 595 (the threshold formula and inputs d = sqrt(3)/2, tau = 1e-12 are shown at L08.html:362). Note for the architect: 40 and 527 are not printed by the lab; the page states that they come from a copy with BETA changed (L08.html:293, :490)."),
    P("M5c-num-L08-ratio-unrounded", "2.2 numbers (c) and 2.5 interpretation", "L08.html:271 (interpretation)",
      CARRY.format(f="L08") + "Re-computed in " + O + "independent_numbers.out with the lab's draw order (random.Random(20261028), 2000 pairs, 4 uniforms each for V and W): largest ratio 0.9000000000000006, i.e. 0.9 + 5.55e-16, about five units in the last place above beta. Matches the page. The lab does not print this value (page says so)."),
    P("M5c-num-L09-apriori-R2", "2.2 numbers (c) derived; Problem R2", "L09.html:395",
      "Re-derived in " + O + "independent_numbers.out: 0.9^n <= 1.1547e-7 first holds at n = 152; the bound 0.9^n sqrt(3)/2 / 0.1 is 1.0670e-6 at n = 151 and 9.6027e-7 at n = 152; V_1 maximum over GRID is sqrt(0.75) = sqrt(3)/2 at k = 1.0 (L09.html:395). Quoted values match."),
    P("M5c-num-L09-problems-quiz", "2.2 numbers (c); 2.6 quiz data-answer", "L09.html:311-327, 363, 436-492",
      "Re-computed in " + O + "independent_numbers.out and by hand: M1 values 1, 9, 99; M2 0.8/0.2 * 0.016 = 0.064; M3 1e-3*(1-beta)/beta = 1/9000; quiz 0.9^10/0.1 = 3.4867844 (answer 3.486784, tolerance 1e-6); quiz 0.02, 99, and 147 (printed certified_stop n 147) match."),
    P("M5c-num-L09-E2-ratio", "2.2 numbers (c); E2 and Misconception 1", "L09.html:290, :370",
      "0.0000085808 / 0.0000009534 = 9.000210 (" + O + "independent_numbers.out), which the page reports as 9.0002 and as nine to the printed step's precision. Printed naive_factor_times_step equals 9 times the unrounded step (8.999999 ratio)."),
    P("M5c-num-L10-example33", "2.2 numbers (c); Example 3.3 closed forms", "L10.html:147, :471, :485, :580",
      "Exact Fractions (" + O + "independent_numbers.out): right error 11/96, 29/600, 299/60000, 2999/6000000 equal (3n-1)/(6n^2) and left error -13/96, -31/600, -301/60000, -3001/6000000 equal -(3n+1)/(6n^2) for n = 4, 10, 100, 1000. E1 gap 31/600 - 29/600 = 1/300. L10q6 (1001)(3999)/(6e6) = 0.6671665 exactly."),
    P("M5c-num-L10-partB-P2", "2.2 numbers; Problem P2 bound (proved bound used in E2)", "L10.html:352, :451-453, :478",
      "Part B recomputed with the lab's draw order (" + O + "independent_numbers.out): largest mesh 0.992962, largest error/mesh 0.491631, all within 2 mesh. E2 states 0.491631 below 1 and below one half, consistent with P2 (ratio <= 1). The P2 bound |S - 2/3| <= m is proved on the page (L10.html:453) and its algebra checked."),
    P("M5c-num-L10-prop42-R2-R3", "2.4 mathematics spot-checks (Prop 4.2, R2, R3)", "L10.html:376-381, :502-503, :508-510",
      "Prop 4.2 proof algebra checked: S = xi_k and |xi_k - 1/2| <= Delta x_k <= |P|. R2 proof checked (same argument, continuity of f at c). R3: the increments of G + c equal those of G, so the sums coincide; the check value 2/3 equals Corollary 3.2."),
    P("M5c-math-L08", "2.4 mathematics (Prop 1.3, Def 1.1, Thm 2.2, Ex 2.3, Problems R1-R3, P1-P3, E1-E3)", "L08.html:77-130, 131-134, 317-400",
      CARRY.format(f="L08") + "L07 Theorem 2.1 hypotheses unchanged in the delta (complete, nonempty; L07.html Theorem 2.1 block). Re-read in full this round: proof of (a) (maximisers a, b; inequality chain) and Problems P1-P3, R1-R3 checked; E1 thresholds and E2 arithmetic re-derived (" + O + "independent_numbers.out)."),
    F("M5c-math-L09", "2.4 mathematics (Lemmas 1.1, 1.2, 2.3, Thm 2.4, Remark 2.5, P1-P3, R1-R3)", "course/modules/M/M5/L09.html:352 (Problem P3 proof)",
      "Re-derived from scratch. Lemma 1.1, Lemma 1.2 (both directions), Theorem 1.3 (now with hypothesis (3) nonempty), Lemma 2.3(a),(b),(c), Theorem 2.4 (Bernoulli argument) and R1, R2, R3 are correct. Defect in P3 proof: the induction step ends 'Multiplying the step bound by beta/(1 - beta) gives the claim for n.' The step bound is for ||V_{n+1} - V_n||, so multiplying gives cert_{n+1} <= beta^{n+1}/(1 - beta) ||V_1 - V_0||, which is the claim for n + 1, not n.",
      "L09.html:352: change 'gives the claim for n.' to 'gives the claim for n + 1.'"),
    P("M5c-math-L10", "2.4 mathematics (Lemmas 1.3, 2.1, 2.2, 2.4, Thm 3.1, Cor 3.2, Thm 3.5, Prop 4.1, 4.2, Problems P1-P3, R1-R3)", "L10.html:69-172, 364-381, 418-510",
      "Re-derived in full: Lemma 1.3 (uniqueness); Lemma 2.1 (Bolzano-Weierstrass proofs of (i),(ii)); Lemma 2.2 (gap argument); Lemma 2.4 (a)-(c); Theorem 3.1 (eta = eps/(M(b-a)+1), error bound (b-a)M eta < eps; uses Q3 exactly as M2 L10 Theorem 2.1 states it); Corollary 3.2; Theorem 3.5 Steps 1-3 (refinement estimate, Cauchy estimate with 2 eta V, limit); Proposition 4.1 (eps = 1/2, even n, two tagged partitions); Proposition 4.2 (|S - 1/2| <= |P|); P1-P3; R1 (solution names the three uses of continuity of G'; accepted as stating the hypothesis the proof as written needs, which is continuity); R2; R3; M1-M3; E1 (31/600 - 29/600 = 1/300), E2, E3. Ran by hand and by " + O + "independent_numbers.out."),
    P("M5c-math-cross-refs", "2.4 cross-lesson and M1/M2/L01/L02/L06/L07 statements read", "L08:38, :59, :128; L09:38, :75, :85, :122; L10:80, :89, :91, :114, :124, :142",
      "Read the cited statements: L07 Theorem 2.1 (complete, nonempty); L01 Theorem 1.2 Archimedean; L02 Theorem 2.5 Cauchy criterion; L06 Proposition 1.3 Bolzano-Weierstrass; M2 L09 Definition 1.3, Lemma 1.1 (refinement), Lemma 1.2 (lower below upper), Example 3.2 (x^2 on [0,1]); M2 L10 Theorem 2.1 with hypotheses equal to the Q3 wording and M2 Assumption 2.1 (M2 L06); M2 L11 Lemma 1.1 (linearity) and Example 3.2 (8/3). M2 L09, L10 and L11 changed in the delta, but none of the cited statements changed (git diff aeb512b6 9294b914 -- course/modules/M/M2)."),
    P("M5c-math-grades", "2.3 grades re-graded against BLUEPRINT 3", "L08.html:413-419; L09.html:414-419; L10.html:522-530; claim blocks",
      "Re-graded every claim block and key-results row: L08 Prop 1.3, Thm 2.2, Example 2.3 (T, proofs on page); L09 Lemmas 1.1, 1.2, 2.3, Thm 1.3, Thm 2.4 (T); L10 Lemmas 1.3, 2.1, 2.2, 2.4, Thm 3.1, Cor 3.2, Thm 3.5, Props 4.1, 4.2 (T; Thm 3.1 and Cor 3.2 are stated under the named Assumption 1 of L10 Section 2). Lab-printed values on the cards are C with a lab basis. Example 3.3 on L10 is a remark with its derivation shown, not a claim block."),
    P("M5c-struct-L08", "2.9 structure and template (BUILDER 4.2)", "L08.html",
      "Order: why-it-matters (120 words, limit 120), s1, s2, lab, canon-breaks, misconceptions (3), problem set (3 per tier, 12 problems), key results, quiz (8 items, one data-correct per MC item), references. Scan output " + O + "structure_checks.out."),
    P("M5c-struct-L09", "2.9 structure and template (BUILDER 4.2)", "L09.html",
      "Order as BUILDER 4.2 (why-it-matters 112 words; misconceptions 3; 12 problems; key results; quiz 9 items; references). " + O + "structure_checks.out."),
    P("M5c-struct-L10", "2.9 structure and template (BUILDER 4.2)", "L10.html",
      "Order as BUILDER 4.2 with the lab inline in Section 3 (L10.html:175), canon-breaks, misconceptions (3), problem set (3 per tier), key results, quiz (9 items), references. Why-it-matters 120 words. " + O + "structure_checks.out."),
    P("M5c-prose-banned", "2.9 banned phrases (BUILDER 1.3-1.4)", "L08.html, L09.html, L10.html",
      "Scan (" + O + "structure_checks.out) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly, roughly, historically, ellipsis characters and entities: 0 hits in prose. The only '...' are Python type annotations (tuple[float, ...]) inside lab code."),
    P("M5c-prose-process-words", "2.9 process words in learner text (ruling 12)", "L08.html, L09.html, L10.html",
      "Scan for builder, verifier, round, ledger, fragment, checkout, agent, placeholder: the only substring hits are 'unrounded' and 'rounding' (learner text about float values). No process words."),
    P("M5c-prose-html", "2.9 HTML integrity (raw '<' breaking markup)", "L08.html, L09.html, L10.html",
      "Start-tag scan outside pre blocks: every tag name is in the HTML vocabulary (" + O + "structure_checks.out). A stricter scan for '<' followed directly by a letter outside code returned 0 in each page. The round-1 raw '<' defects were in L04-L06, not in these pages."),
    P("M5c-prose-stock-L09", "2.9 term used without definition (ruling 13 wording / open item 7)", "L09.html:272, :485",
      "'stock' no longer appears in L08-L10 prose (" + O + "structure_checks.out). L09.html:485 now reads 'It keeps the capital positive'; L09.html:272 uses capital or state."),
    P("M5c-prose-L09-nav", "2.9 cross-link text matches target title", "L09.html:505",
      "Previous link text 'L08 · The Discounted Bellman Operator Is a Contraction' equals the L08 h1 (L08.html:36). L08 next link equals the L09 h1, and L09 next link 'L10 · The Riemann–Stieltjes integral' equals the L10 h1."),
    P("M5c-thm-L09-1.3-hypotheses", "2.4 assumptions complete (BUILDER 1.10 / VERIFIER 2.4); BUILDER 3.3", "L09.html:86 (Theorem 1.3)",
      "Theorem 1.3 now lists (1) complete, (2) contraction with modulus beta in (0,1), (3) X nonempty, and the application sentence checks (3) via the zero function in R^G. L07.html Theorem 2.1 hypothesis (1) reads 'complete metric space, and X is nonempty', so the hypotheses match the cited theorem."),
    P("M5c-quiz-L10-q7", "2.4 statement of a T result without its named Assumption; 2.9 quiz", "L10.html:585 (correct option of quiz item L10q7)",
      "Correct option now reads 'Yes, under Assumption 1, and it equals int f G' dx (Theorem 3.1)'. Explanation L10.html:589 is consistent. Theorem 3.1 is stated under Assumption 1 (L10.html:124)."),
    P("M5c-quiz-numeric-answers", "2.6/2.9 quiz data-answer values", "L08.html:438-483; L09.html:438-489; L10.html:549-603",
      "Each numeric answer re-derived: L08 0.866025, 10, 2001, 0.676097; L09 0.02, 3.486784 (3.4867844), 147; L10 0.666667 (|0.666667 - 2/3| = 3.3e-7 < 5e-7), 0.5, 0.6671665 (exact (1001)(3999)/6e6), 0.75. Every MC item has exactly one data-correct option."),
    P("M5c-dag", "2.9 DAG; concept introduction", "L08.html:38-39; L09.html:38-39; L10.html:38-39",
      "check_dag PASS. Concepts used: completeness, metric space, contraction, Banach, discount factor (M1), Cauchy sequence, Archimedean and Cauchy criterion (L01, L02), epsilon-delta continuity (L03), compactness and Bolzano-Weierstrass (L06), definite integral and Darboux sums (M2). All are in the M5 prerequisite closure (M2, M1). No concept is defined twice in the slice."),
    P("M5c-notation", "2.9 / ruling 13 notation vs notation/notation.json", "L08.html, L09.html, L10.html math segments",
      "Scan (" + O + "notation_scan.out): registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and \\mathbb{Q} do not occur in the slice math. Registered macro \\R is used correctly. Local letters (G, F, V, B, W, K on L08-L09; P, Q, R, S, I, J, L, U, M, N, V on L10; xi, zeta, eta, Delta) are defined on use and not registered. Plain Q (a partition, L10) is not \\mathbb{Q}, so there is no collision."),
    P("M5c-hours", "2.2/2.9 hours arithmetic (ruling: hours are design targets)", "L08.html:2, L09.html:2, L10.html:2; index.html data-hours-lessons/project",
      "Hub data-hours-lessons = 104 and data-hours-project = 26, total 130 (index.html:29). 104 = 6 lessons at 10 h plus 4 at 11 h (index.html:131); each slice page declares data-hours 11 (L08.html:2, L09.html:2, L10.html:2), and the lesson cards show 11 h."),
    P("M5c-cards-schema", "2.7 cards schema, duplicates (full scan)", "course/modules/M/M5/cards.json (236 cards)",
      "236 cards, ids unique, every card has id, lesson, front, back; no two cards have identical backs; within the 90 slice cards no two fronts are duplicates (only similar pairs c166/c167 and c170/c233, which are different lemmas and different sums). Numbering skips c144, c149, c150, c195 (no card references them). Output " + O + "structure_checks.out."),
    P("M5c-cards-L08", "2.7 cards correctness vs lesson (30 cards, all read)", "cards.json: M5-c121..c139, c186, c199, c200, c204..c206, c212, c226..c229 vs L08.html",
      "Every card read against L08.html and checked: definitions c121-c124, Prop 1.3 c125, remark c126, Thm 2.2 c127-c129, Example 2.3 c130 and c226, R2 c131, R1 c132, misconceptions c133-c135, Lab 1 cards c136-c139, c204-c206, c227-c229, canon item c212, P3 c186. c199 (policy) and c200 (sup norm) now sit in L08 and match L08.html:56 and :63."),
    P("M5c-cards-L09", "2.7 cards correctness vs lesson (26 cards, all read)", "cards.json: M5-c140..c161, c202, c207, c208, c230..c232, c235 vs L09.html",
      "Every card read against L09.html: Def 2.1 c140, Def 2.2 c141, Lemma 1.1 c142, Lemma 1.2 c143 (statement only) and c235 (matches Theorem 2.2(a) of L08), Lemma 2.3 c145-c147, Theorem 2.4 c148, canon items c151-c152, Problems M1 c153, R2 c154, R3 (via c152), misconceptions c159-c161, Lab 1 c155-c158, c207, c208, c230-c232, Theorem 1.3 c202 (now lists nonempty). Each number matches the lesson."),
    P("M5c-cards-L10", "2.7 cards correctness vs lesson (34 cards, all read)", "cards.json: M5-c162..c189, c209, c233, c234, c236..c239 vs L10.html",
      "Every card read against L10.html: Defs 1.1-1.2 c163-c164, mesh c236, tagged partition c162, Lemma 1.3 c165, Lemmas 2.1, 2.2, 2.4 c166, c167, c187, Thm 3.1 c168, Cor 3.2 c169, Example 3.3 c170, c233, c234, c171, P2 c172, Props 4.1, 4.2 c173-c175, R2 c176, M3 c178, Thm 3.5 c189, Definition 3.4 c188, c237, c238, continuously differentiable c239, misconceptions c179-c181, Lab 1 c180, c182-c185, c209, numeric P3 c177. Each number matches the lesson."),
    P("M5c-cards-numbers", "2.7 every card number appears in its lesson", "cards.json (slice cards) vs L08-L10",
      "Check in " + O + "structure_checks.out: every decimal or two-or-more-digit number on the 90 slice cards appears verbatim in its own lesson page (e.g. 0.491631 in L10, 1.7433922005 in L09, 0.9 + 5.6 x 10^-16 in L08)."),
    P("M5c-cards-coverage", "BUILDER 7 coverage (definitions, theorems, misconceptions)", "L08.html:56, :63; L10.html:120; cards.json",
      "Round-1 gaps closed: policy card M5-c199 (L08.html:56), sup norm card M5-c200 (L08.html:63), continuously differentiable card M5-c239 (L10.html:120). Each definition, dfn, theorem, lemma, proposition, corollary and misconception in L08-L10 has at least one card; Example 1.2 and the canon items beyond those cited are not required by BUILDER 7."),
    P("M5c-cards-atomic", "BUILDER 7 'each card tests one fact'", "cards.json: M5-c143, M5-c162, M5-c188",
      "c143 asks only for Lemma 1.2's statement; c162 defines only a tagged partition (mesh on c236); c188 defines only V(G) (bounded variation on c237, telescoping on c238). Other multi-quantity cards (c182, c204, c205, c208) each report one printed value with its direct comparison and were accepted."),
    F("M5c-prose-footer", "2.9 prose: scope claim without support (defect class 4)", "L08.html:501, L09.html:510, L10.html:620 (site footer)",
      "Each page's footer reads 'M5 · Real Analysis · Every claim carries an evidence grade and a registry citation.' The claim is false for these pages: L08.html:490 says 'This page cites no source', L09.html:499 says 'cites no outside source', and L10.html:610 says 'cites no outside source'. No claim on L08-L10 carries a registry key. The same footer sentence is in other units' pages (86 files, shared template text).",
      "On L08.html:501, L09.html:510 and L10.html:620 replace the footer sentence with a true one, for example 'Each claim carries an evidence grade; this page cites no registry source.' The shared template owner must decide the wording for the other units; the M5 pages must not claim registry citations they do not contain."),
]

frag = {
    "unit": "M5",
    "slice": "c",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for M5-c (L08-L10, lab twins and cards), round 2, final full verification against the binding rulings; no build-side context; the round-1 fragment was read as context only and its PASS rows were not trusted",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f (round-1 pin). Delta for slice c: course/modules/M/M5/L07.html (not slice; cited statements read), L09.html (36 lines), L10.html (26 lines), cards.json (94 lines; c143, c162, c168, c169, c171, c172, c177, c188, c199, c200, c202 changed; c235-c240 added; c199 and c200 relabelled L08), tests/labs/M5/lab-M5-L09-1.py (docstring), tests/labs/M5/lab-M5-L02-1.py (not slice), index.html (hub, hours split re-checked), references/references.json (FC2 key added; no M5 key changed), M2 L09-L11 (cited statements unchanged). L08.html, lab-M5-L08-1.py and lab-M5-L10-1.py are byte-identical to the round-1 pin for L08 only; L10 changed and was fully re-verified.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M5-c",
    "scratch": "/tmp/m5c-r2-gates.log (empty gate log; outputs are in ledgers/M5/scripts/M5-c-r2/out), /tmp/m5c_cards_r1.json (round-1 cards copy used only for the delta)",
    "verified_at": "2026-11-09T04:31:32Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutation testing does not apply to lab twins (ruling: mutants are for project graders only), so mutants is empty. "
        "Scripts backing rows: ledgers/M5/scripts/M5-c-r2/run_gates.sh (gate rows; outputs in out/), m5c_page_twin_check.py, m5c_independent_numbers.py, m5c_notation_scan.py, m5c_structure_checks.py (writes out/structure_checks.out), build_fragment_r2.py. "
        "Files that were already tracked in ledgers/M5/scripts/M5-c-r2/ at the pin (l08_check.py, l09l10_check.py, lab-M5-L08-1.out, lab-M5-L09-1.out, lab-M5-L10-1.out) were not created by this round, were not modified and were not used as evidence. "
        "Two numbers are not printed by the lab and are stated on the page from a modified copy (40 and 527 iterations, L08.html:293, :362, :490) or recomputed outside the lab (0.9 + 5.6e-16, L08.html:271; card M5-c205). The procedure is stated, and I reproduced both independently, so they are carried as PASS under BUILDER 1.2(c); the architect may prefer the lab to print them. "
        "Could not check: run_graders for M5 (project grader, outside slice c); page_smoke for the whole unit; a Pyodide run beyond page_smoke; verify_refs without --offline (the slice cites no registry key, so there is nothing to resolve); the full text of L01, L02, L06, L07 and M2 (only the statements cited from the slice were read, with their hunks in the delta). "
        "The pre-existing ledgers/M5/M5-c.json (round 7, pin 7aa909e) was overwritten by this fragment as instructed."
    ),
    "summary": "M5-c round 2 on 9294b914: verdict FAIL. 48 rows: 46 PASS, 2 FAIL. Both FAILs are real and minor. (1) L09 Problem P3 induction ends with 'gives the claim for n' where n+1 is meant (L09.html:352). (2) The shared footer on L08, L09 and L10 says every claim carries a registry citation, which these pages do not do (L08.html:501, L09.html:510, L10.html:620). All round-1 FAIL rows (stock, L09 nav, L09 Theorem 1.3 hypotheses, L10 quiz q7, card coverage, card atomicity) are fixed and re-verified. All gates pass: check_pages, check_dag, check_projects, run_labs, twins under -I -W error, page_smoke on the three pages, ruff, mypy, pytest -k M5, verify_refs --offline.",
}

path = ROOT / "ledgers/M5/M5-c.json"
path.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", path, "rows", len(rows), "fail", sum(r["status"] == "FAIL" for r in rows))
