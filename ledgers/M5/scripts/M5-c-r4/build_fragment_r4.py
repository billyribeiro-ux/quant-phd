"""Writes the round-4 fragment ledgers/M5/M5-c.json (slice c, M5 L08-L10 with twins and cards)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M5/scripts/M5-c-r4"
O = f"{S}/out"
SEV = "Severity (ruling 26): LOW (wording, presentation or card style); no blocking kind. "

rows = [
    # ---- gates and labs (all re-run this round) ----
    dict(id="M5c-gate-check-pages", check="2.9 structure (check_pages)", location="course/modules/M/M5 (L08-L10, cards.json)", status="PASS",
         evidence=f"{S}/gates.sh: .venv/bin/python tools/check_pages.py --unit M5 -> 'check_pages M5: PASS', exit 0 ({O}/check_pages.out)."),
    dict(id="M5c-gate-check-dag", check="2.9 DAG (check_dag)", location="course/modules/M/M5 pages", status="PASS",
         evidence=f"tools/check_dag.py --unit M5 -> 'check_dag M5: PASS', exit 0 ({O}/check_dag.out). Prerequisite closure checked by hand: M5 prereqs [M2] (curriculum/01-foundations.yaml:235), M2 prereqs [M1], so discount-factor (M1) is in closure."),
    dict(id="M5c-gate-check-projects", check="2.6 projects (check_projects, unit-level, recorded for completeness)", location="course/modules/M/M5/project.html (outside slice)", status="PASS",
         evidence=f"tools/check_projects.py --unit M5 -> 'check_projects M5: PASS', exit 0 ({O}/check_projects.out)."),
    dict(id="M5c-gate-run-labs", check="2.5 labs (run_labs, unit and per page)", location="tests/labs/M5/lab-M5-L08-1.py, L09-1.py, L10-1.py", status="PASS",
         evidence=f"tools/run_labs.py --unit M5 -> 'run_labs M5: PASS (13/13)' ({O}/run_labs_unit.out); --page L08, L09, L10 -> 'PASS (1/1)' each ({O}/run_labs_L08.out, _L09.out, _L10.out)."),
    dict(id="M5c-twins-isolated", check="2.5 twins alone under python -I -W error", location="tests/labs/M5/lab-M5-L08-1.py, lab-M5-L09-1.py, lab-M5-L10-1.py", status="PASS",
         evidence=f"python -I -W error <twin>: exit 0 each ({O}/twin_L08.out, twin_L09.out, twin_L10.out). {S}/page_twin_compare.py ({O}/page_twin_compare.out): stderr 0 bytes, page data-run code equals the twin file, page expected block equals stdout, RESULT PASS."),
    dict(id="M5c-gate-page-smoke", check="2.9 page_smoke for the slice pages, alone", location="course/modules/M/M5/L08.html, L09.html, L10.html", status="PASS",
         evidence=f"tools/page_smoke.py --unit M5 --pages L08 (and L09, L10) -> 'page_smoke M5: PASS', exit 0 ({O}/page_smoke_L08.out, _L09.out, _L10.out)."),
    dict(id="M5c-gate-ruff-mypy", check="2.5 twins: ruff and mypy", location="tests/labs/M5/lab-M5-L08-1.py, L09-1.py, L10-1.py", status="PASS",
         evidence=f"ruff check on the three twins -> 'All checks passed!' ({O}/ruff_check_twins.out); ruff format --check -> '3 files already formatted' ({O}/ruff_format_twins.out); .venv/bin/python -m mypy --no-incremental -> 'Success: no issues found in 385 source files' ({O}/mypy_no_incremental.out)."),
    dict(id="M5c-gate-pytest-labs", check="2.5 relevant pytest", location="tests/test_labs.py -k M5", status="PASS",
         evidence=f"python -m pytest tests/test_labs.py -q -k M5 -> 13 dots, exit 0 ({O}/pytest_labs_M5.out)."),
    dict(id="M5c-gate-verify-refs-offline", check="2.1 citations (verify_refs --offline)", location="references/references.json; slice pages", status="PASS",
         evidence=f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({O}/verify_refs_offline.out). Slice pages: grep for data-cite, data-locator, references.json returns 0 hits in L08-L10 (round-4 scan, output recorded in the notes); slice cards have no source keys (cards_r4.py)."),
    dict(id="M5c-lab-L08-1", check="2.5 lab L08-1 (demonstration; rung not applicable)", location="course/modules/M/M5/L08.html:136-271; tests/labs/M5/lab-M5-L08-1.py", status="PASS",
         evidence=f"{S}/page_twin_compare.py: page code equals twin, expected block equals stdout ({O}/page_twin_compare.out). {S}/numbers_r4.py ({O}/numbers_r4.out): V* = 5.000000, 5.176097, 5.284873, 5.366025; residual 8.695e-13 (lab output); worst sampled ratio 0.9000000000000006 (excess 5.55e-16 over beta, which supports the page's 'computed in floating point' rationale at L08.html:271); BETA=0.5 gives 40 iterations and BETA=0.95 gives 527 in copies (numbers_r4.out)."),
    dict(id="M5c-lab-L09-1", check="2.5 lab L09-1 (demonstration; rung not applicable)", location="course/modules/M/M5/L09.html:130-274; tests/labs/M5/lab-M5-L09-1.py", status="PASS",
         evidence=f"{S}/page_twin_compare.py (page code equals twin; expected equals stdout). {S}/numbers_r4.py: reference 278 iterations, cert 9.5124e-13; stops n=59/103/147 with cert=actual to 1e-12 (actual minus cert about -9.5e-13); fixed count 10 cert 1.7433922005; naive stop n=126, step 9.5341874e-07, actual - 9*step = -9.5e-13; step spread exactly 0.0 at each stop ({O}/numbers_r4.out)."),
    dict(id="M5c-lab-L10-1", check="2.5 lab L10-1 (demonstration; rung not applicable)", location="course/modules/M/M5/L10.html:175-353; tests/labs/M5/lab-M5-L10-1.py", status="PASS",
         evidence=f"{S}/page_twin_compare.py (page code equals twin; expected equals stdout). {S}/numbers_r4.py: exact right/left sums and error formulas True for n=4,10,100,1000; Part B largest error/mesh 0.491631 (lab output); Part C sums 0 and 1 at n=10,100; Part D 0.500500000000 and 0.499500000000 ({O}/numbers_r4.out)."),
    # ---- numbers ----
    dict(id="M5c-num-L08-worked", check="2.2 numbers (worked values, one row per span)", location="L08.html:74, :133, :278, :319, :326, :369, :483", status="PASS",
         evidence=f"{S}/numbers_r4.py ({O}/numbers_r4.out): Example 1.2 sqrt(0.75)=0.866025; M1 (BV)(0.25)=0.5; M2 V*=0.5/0.05=10; M3 feasible sets (0.707107 and 0.866025 comparisons); E2 sqrt(0.457107)=0.676097 and 0.676097+0.9*5=5.176097; Example 2.3 V*=5 at beta=0.9."),
    dict(id="M5c-num-L08-counts", check="2.2 numbers (iteration counts and a priori counts)", location="L08.html:293, :362, :455, :490", status="PASS",
         evidence=f"{S}/numbers_r4.py: solver counts 40 (beta 0.5), 257 (0.9, also printed by the lab), 527 (0.95); a priori thresholds 40.66, 282.74, 594.29 and least n 41, 283, 595 (numbers_r4.out). Counts at 0.5 and 0.95 are C naming the modified copies, which the page states (L08.html:293, :362)."),
    dict(id="M5c-num-L08-ratio-unrounded", check="2.2 numbers (unrounded contraction excess) - round-3 FAIL re-verified", location="L08.html:271; cards.json (former M5-c205)", status="PASS",
         evidence=f"Round 3 FAIL (unsourced 0.9+5.6e-16 quoted on L08.html:271 and card M5-c205) is fixed: the sentence now says only that the check allows 1e-12 above beta because the ratio is computed in floating point, and card M5-c205 is removed (cards_r4.py: 235 unique ids). The rationale is supported by {S}/numbers_r4.py: unrounded worst ratio 0.9000000000000006, excess 5.55e-16 (numbers_r4.out)."),
    dict(id="M5c-num-L09-apriori-R2", check="2.2 numbers (a priori count, Problem R2)", location="L09.html:392-399 (R2 statement and solution)", status="PASS",
         evidence=f"{S}/numbers_r4.py: ||V1-V0|| = 0.8660254 = sqrt(3)/2; bound at n=151 is 1.066963e-6 (prints as 1.067e-6), at n=152 is 9.602671e-7 (prints as 9.60e-7); least n with bound <= 1e-6 is 152 (numbers_r4.out). Card M5-c154 agrees."),
    dict(id="M5c-num-L09-problems-quiz", check="2.2 numbers (problem solutions and quiz keys)", location="L09.html:311-327, :363, :436-492", status="PASS",
         evidence=f"{S}/numbers_r4.py: M1 1, 9, 99; M2 cert_2 = 4*0.016 = 0.064; M3 step 1/9000 = 1.1111e-4; E1 n=103 cert 0.0000968163; E3 1.7433922005 and 147 steps; quiz keys 0.02, 3.486784 (0.9^10/0.1 = 3.4867844), 147, 99 (numbers_r4.out)."),
    dict(id="M5c-num-L09-E2-ratio", check="2.2 numbers (printed ratio)", location="L09.html:290, :370", status="PASS",
         evidence=f"0.0000085808/0.0000009534 = 9.000209775 (numbers_r4.out), i.e. 9 to the precision of the printed step; actual error minus 9 times the unrounded step is -9.5e-13, so 'nine times the unrounded last step' holds to the printed digits (numbers_r4.out)."),
    dict(id="M5c-num-L10-example33", check="2.2 numbers and 2.4 mathematics (Example 3.3 closed forms)", location="L10.html:147, :471, :485, :580", status="PASS",
         evidence=f"{S}/numbers_r4.py: closed forms (n+1)(4n-1)/(6n^2) and (4n^2-3n-1)/(6n^2) equal the exact Fraction sums for n=1..60 (no failures, numbers_r4.out); n=4,10,100,1000 errors match the printed lab values; E1 errors 29/600 and -31/600, gap 1/300; quiz 0.6671665 = 1001*3999/(6*10^6). The 1/n bound is not written on the page: see M5c4-L10-ex33-bound-step."),
    dict(id="M5c-num-L10-partB-P2", check="2.2 numbers (Part B ratio and Problem P2)", location="L10.html:352, :451-453, :478", status="PASS",
         evidence=f"Printed largest_error_over_mesh 0.491631 is the lab output (twin_L10.out). {S}/numbers_r4.py: over 3000 random tagged partitions the worst |S-2/3|/mesh is 0.601879 (<= 1, as P2 proves; numbers_r4.out)."),
    dict(id="M5c-num-L10-prop42-R2-R3", check="2.2 numbers and 2.4 mathematics (Prop 4.2, Problem R2, Problem R3)", location="L10.html:376-381, :502-503, :508-510", status="PASS",
         evidence=f"{S}/numbers_r4.py: Prop 4.2 worst |S-1/2|/mesh = 0.982976 <= 1 over 3000 random tagged partitions; R2 step at c: tagged sums equal f(c) to 9 dp for c=0.3, 0.77 at n=100, 1000 (numbers_r4.out); R3 telescoping argument checked by hand."),
    # ---- mathematics ----
    dict(id="M5c-math-L08", check="2.4 mathematics (Prop 1.3, Remark, Thm 2.2 (a)-(c), Ex 1.2, Ex 2.3, Problems M1-M3, P1-P3, E1-E3, R1-R3)", location="L08.html:77-130, 131-134, 317-400", status="PASS",
         evidence="Read in full. Proof of Thm 2.2(a) checked line by line (maximisers a and b, one-sided bounds, beta >= 0 used). Proof of (c) via Theorem 2.1 of Lesson 7 (L07.html:99-111, hypotheses (1)-(3) hold). E1 threshold ln(tau(1-beta)/d)/ln(beta) recomputed (numbers_r4.out). R2 divergence argument checked. R3 nonemptiness for grids in (0,1] checked. Canon-breaks items 1-4 and misconceptions 1-3 checked against the code and proofs."),
    dict(id="M5c-math-L09", check="2.4 mathematics (Lemmas 1.1, 1.2, 2.3; Thm 1.3, 2.4; Remark 2.5; problems)", location="L09.html:52-130; P3 solution L09.html:352", status="PASS",
         evidence="Read in full. Lemma 1.1 (Cauchy in R^G converges, letting l to infinity), Lemma 1.2 (new proof: maximiser for W is feasible for V, bound by beta*delta), Lemma 2.3(a),(b),(c) and Theorem 2.4 (Bernoulli bound on beta^n, Archimedean step) rechecked. P1 and P3 (induction) and R2 (telescoping; 152) rechecked. Canon-breaks items 1-3 (X=(0,1], Psi=x+1, Psi=beta x+1 with equality) rechecked (V1=1, xi*=1/(1-beta))."),
    dict(id="M5c-math-L10", check="2.4 mathematics (Sections 1-4, Lemmas, Theorems, Props, problems)", location="L10.html:69-172, 364-381, 418-510", status="PASS",
         evidence="Read in full. Lemma 1.3 (uniqueness), Lemma 2.1 (i),(ii) (Bolzano-Weierstrass subsequence arguments), Lemma 2.2 (U-L <= eps(b-a)), Lemma 2.4 (a),(b),(c) (common refinement, splitting at e, both inequalities), Theorem 3.1 (eta = eps/(M(b-a)+1) bound), Corollary 3.2 (2*(1/3)=2/3), Theorem 3.5 (Steps 1-3, I defined before eps), Prop 4.1 (two tags, eps=1/2), Prop 4.2 (|S-1/2| <= |P|), Remark 4.2, all problems. Gap in R1's answer and the 1/n step are separate rows."),
    dict(id="M5c-math-cross-refs", check="2.4 cross-references and 2.1 locators (M2, M5 L01/L02/L06/L07/L08)", location="L08: L07 Thm 2.1; L09: L01 Thm 1.2, L02 Thm 2.5, L06 Prop 1.3, L08 Thm 2.2(a); L10: M2 L09 Def 1.3, Lemmas 1.1/1.2, Ex 3.2; M2 L10 Thm 2.1; M2 L11 Lemma 1.1; M2 L06 Assumption 2.1; L02 Thm 2.5; L06 Prop 1.3", status="PASS",
         evidence="Located in the checkout: L01.html:67 (Theorem 1.2 Archimedean); L02.html:127 (Theorem 2.5 Cauchy criterion); L06.html:74 (Proposition 1.3 Bolzano-Weierstrass); L07.html:99 and :131-136 (Theorem 2.1 and its Step 1, beta^n -> 0); M2/L09.html:65, :75, :85, :136 (Lemma 1.1, Lemma 1.2, Definition 1.3, Example 3.2); M2/L10.html:76 (Theorem 2.1 FTC); M2/L11.html:57 (Lemma 1.1 linearity); M2/L06.html:72 (Assumption 2.1, EVT). All cited locators exist with the stated content."),
    dict(id="M5c-math-grades", check="2.3 grades (theorem titles, key-results rows)", location="L08.html:413-419; L09.html:414-419; L10.html:522-530; theorem titles", status="PASS",
         evidence="Every Lemma, Theorem, Proposition and Corollary title in L08-L10 carries data-grade T (L08 2, L09 5, L10 9; grep). Key-results rows: L08 7, L09 6, L10 9, all T, each with a proof or named source in the row. Conditional results (Theorem 3.1, Corollary 3.2) are T with Assumption 1 named on the page, as the convention allows. Example 3.3 display gap is a separate row."),
    # ---- structure and prose ----
    dict(id="M5c-struct-L08", check="2.9 structure (template sections in order)", location="course/modules/M/M5/L08.html", status="PASS",
         evidence="Header, grade legend, why-it-matters, sections s1-s8 (s1 model, s2 contraction, s3 canon breaks, s4 misconceptions, s5 problem set, s6 key results, s7 quiz, s8 references), nav. data-hours=11 matches eyebrow. check_pages PASS."),
    dict(id="M5c-struct-L09", check="2.9 structure (template sections in order)", location="course/modules/M/M5/L09.html", status="PASS",
         evidence="Same template order s1-s8; data-hours=11; check_pages PASS."),
    dict(id="M5c-struct-L10", check="2.9 structure (template sections in order)", location="course/modules/M/M5/L10.html", status="PASS",
         evidence="Same template order s1-s10 (s5 canon breaks, s6 misconceptions, s7 problems, s8 key results, s9 quiz, s10 references); data-hours=11; check_pages PASS."),
    dict(id="M5c-prose-banned", check="2.9 banned phrases (BUILDER_RULES 1.3-1.4)", location="L08.html, L09.html, L10.html; cards.json (slice cards)", status="PASS",
         evidence="check_pages M5 PASS (includes the banned-phrase rule) ({O}/check_pages.out)."),
    dict(id="M5c-prose-process-words", check="2.9 process words in learner text", location="L08.html, L09.html, L10.html", status="PASS",
         evidence="grep (case-insensitive) for verif, builder, ledger, fixer, round, slice, TODO, draft, placeholder, architect, we will, let us: no hits in learner text. 'planner' is the domain word for the economic agent; 'Stated before running' is the program's lab convention."),
    dict(id="M5c-prose-html", check="2.9 HTML validity (raw < in math)", location="L08.html, L09.html, L10.html", status="PASS",
         evidence="html.parser-style scan of start tags (round-4 script inline): every tag name is in the program vocabulary (a, body, button, code, details, dfn, div, em, fieldset, footer, h1-h3, header, input, label, legend, li, link, main, meta, nav, ol, p, pre, script, section, span, strong, summary, table, tbody, td, th, thead, title, tr, ul); no '\\\\(...<letter' pattern in math."),
    dict(id="M5c-prose-stock-L09", check="2.9 prose (undefined term 'stock')", location="L09.html:272, :485", status="PASS",
         evidence="grep -c '\\\\bstock' on L09.html = 0 (round-4 scan). The page uses 'state' (L09.html:56, :127) and the lab docstring uses 'state k' (L09.html:135)."),
    dict(id="M5c-prose-L09-nav", check="2.9 navigation", location="L09.html:505", status="PASS",
         evidence="L09.html nav: Previous -> L08.html, Next -> L10.html (L09.html:505-506); L08 and L10 nav links point back and forward correctly."),
    dict(id="M5c-thm-L09-1.3-hypotheses", check="2.4 hypotheses (Theorem 1.3 as the Banach theorem)", location="L09.html:86 (Theorem 1.3)", status="PASS",
         evidence="Hypotheses (1) complete, (2) contraction of modulus beta in (0,1), (3) nonempty match L07.html:99-103 (Theorem 2.1 hypotheses (1)-(3)); application to R^G uses Lemma 1.1 and Lemma 1.2 as stated."),
    dict(id="M5c-quiz-L10-q7", check="2.5/2.4 quiz key (L10q7)", location="L10.html:585 (correct option of quiz item L10q7)", status="PASS",
         evidence="Correct option 'Yes, under Assumption 1, and it equals int f G' dx (Theorem 3.1)' is supported by Theorem 3.1 (L10.html:122-125); the explanation names the two function hypotheses. The option's qualifier 'under Assumption 1' is the page's conditional convention."),
    dict(id="M5c-quiz-numeric-answers", check="2.2 quiz numeric keys and tolerances", location="L08.html:438-483; L09.html:438-489; L10.html:549-603", status="PASS",
         evidence="Keys and tolerances rechecked: L08 0.866025 (1e-6; true 0.8660254), 10, 2001 (0.5), 0.676097 (1e-6; true 0.6760973); L09 0.02, 3.486784 (1e-6; true 3.4867844), 99, 147 (0.5); L10 0.666667 (5e-7; true 0.6666667), 0.5, 0.6671665 (1e-7), 0.75. MC keys: L08q1, q4, q6, q7; L09q1, q3, q5, q7, q8; L10q1, q3, q5, q7, q8 match the text."),
    dict(id="M5c-dag", check="2.9 DAG and concept links", location="L08.html:38-39; L09.html:38-39; L10.html:38-39", status="PASS",
         evidence="check_dag M5 PASS ({O}/check_dag.out). Links used before definition: L08 uses L01, L04, L07 concepts; L09 uses L07, L08, L02, L01; L10 uses M2 definite-integral and limit, L03, L06. Each dfn id is defined once (bellman-operator-contraction L08, value-function-iteration L09, riemann-stieltjes-integral L10)."),
    dict(id="M5c-notation", check="2.4 notation (notation.json)", location="L08.html, L09.html, L10.html math segments", status="PASS",
         evidence="Macros used in slice pages: \\R (registered, notation.json macros) and \\mathcal{B} (local, defined in L08 Definition 1.1 per the architect's Q1/notation decision). No \\mathbb. Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used in the slice (grep). Local letters (G, F, V, I, c, xi, eta) are defined in each lesson."),
    dict(id="M5c-hours", check="2.9 hours arithmetic", location="L08.html:2, L09.html:2, L10.html:2; index.html data-hours-lessons, data-hours-project", status="PASS",
         evidence="data-hours: L08=11, L09=11, L10=11; index.html:29 data-hours-lessons=104 (6 x 10 + 4 x 11 = 104) and data-hours-project=26; 104 + 26 = 130 = curriculum hours (curriculum/01-foundations.yaml:234); 26/130 = 20.0% inside the 10-40% band."),
    # ---- cards ----
    dict(id="M5c-cards-schema", check="2.7 cards schema, ids and grade/basis", location="course/modules/M/M5/cards.json (235 cards; 88 in L08-L10)", status="PASS",
         evidence=f"{S}/cards_r4.py ({O}/cards_r4.out): 235 cards, 235 unique ids, no duplicate ids; every graded card (T or C) carries a basis; ungraded cards carry no basis; slice cards 29 (L08), 26 (L09), 33 (L10)."),
    dict(id="M5c-cards-L08", check="2.7 cards L08 (29 cards, each against the lesson text)", location="cards.json M5-c121..c139, c186, c199, c200, c204..c206 (removed), c212, c226..c229", status="PASS",
         evidence="Each of the 29 L08 cards read against L08.html and checked: definitions (c121-c124), Prop 1.3, Remark, Theorem 2.2(a),(b),(c) hypotheses and conclusions (c125-c129), Example 2.3 (c130, c226), R1, R2 (c131, c132), Misconceptions 1-3 (c133-c135), lab cards c136-c139, c204, c206, c227-c229 (each number checked in numbers_r4.out and the twin output). Former M5-c205 is removed; no remaining card cites the unrounded excess."),
    dict(id="M5c-cards-L09", check="2.7 cards L09 (26 cards)", location="cards.json M5-c140..c161, c202, c207, c208, c230..c232, c235", status="PASS",
         evidence="Each of the 26 L09 cards read against L09.html: c154 (152; 1.067e-6 and 9.60e-7, numbers_r4.out), c155-c158 and c230-c232 (lab numbers in the twin output), c159-c161 (misconceptions; c160 and c161 updated text agrees with L09.html:294, :298), c152 (canon item 3), c202 and c235 (Lemma 1.2 of L09 is part (a) of Theorem 2.2 of L08, L09.html:76). Duplicate question is tracked in M5c3-cards-duplicate-fact."),
    dict(id="M5c-cards-L10", check="2.7 cards L10 (33 cards)", location="cards.json M5-c162..c189, c209, c233, c234, c236..c239", status="PASS",
         evidence="Each of the 33 L10 cards read against L10.html: definitions c162-c164, Lemmas c165-c167 and c187, Theorem 3.1 and Corollary 3.2 (c168, c169, c177, c178 with Assumption 1 stated), Example 3.3 (c170, c171, c233, c234; formulas verified exactly), P2 (c172), Props 4.1-4.2 (c173, c174, c176 with R2), Remark 4.2 (c175), misconceptions c179-c181, lab numbers c182, c183, c185, c209 (twin output), Theorem 3.5 (c189), Def 3.4 (c188, c237, c238), c236, c239. c184 is removed (it duplicated c180)."),
    dict(id="M5c-cards-numbers", check="2.7 card numbers appear in their lesson", location="cards.json (slice cards) vs L08-L10 and lab outputs", status="PASS",
         evidence=f"Every number on a slice card is in the lesson text or in the lab output block: e.g. 0.900000 (L08 lab output), 1.7433922005 and 9.512e-13 (L09 lab output), 0.667166500000 and 0.000499833333 (L10 lab output), 0.491631 (L10 lab output), 1.067e-6 and 9.60e-7 (L09.html:392-399). Checked by reading each card against its lesson ({S}/cards_r4.py)."),
    dict(id="M5c-cards-coverage", check="2.7 card coverage (Builder F rule: every named example with a claim has a card)", location="L08.html:73-75 (Example 1.2); L08.html:56, :63; L09.html; L10.html:120; cards.json", status="FAIL",
         evidence="Coverage checked against the Builder F standard in plans/M5-open-items.md (every dfn, definition, proposition, lemma, theorem, corollary, named example with a claim, all 9 misconceptions in L08-L10, all 22 key-results rows). All of those are carded except L08 Example 1.2 ('one step on a two-point grid', L08.html:73-75, claim (BV)(1.0)=0.866025), which has no card (grep 'Example 1.2' in cards.json: 0 hits). "+SEV,
         fix="Add one card for Example 1.2: lesson L08, front 'On G = (0.25, 1.0), alpha = 1/2 and V = 0, what is (BV)(1.0)?', back '0.866025, the maximum of sqrt(0.75) at k'=0.25 and 0 at k'=1.0 (Example 1.2)', grade T, basis 'Example 1.2 (computed on the page)'. Id: next free id."),
    dict(id="M5c-cards-atomic", check="2.7 atomic cards", location="cards.json M5-c143, M5-c162, M5-c188, M5-c171", status="PASS",
         evidence="Each card asks one question with one answer: c143 (Lemma 1.2 hypotheses and conclusion), c162 (tagged partition), c188 (total variation), c171 (bound from the proof of Theorem 3.1, one quantity)."),
    # ---- round-3 rows carried with a new status ----
    dict(id="M5c3-cards-duplicate-fact", check="2.7 duplicate cards (full scan)", location="cards.json: M5-c173 and M5-c175; M5-c229 and M5-c231; M5-c135 (L08) and M5-c160 (L09); former M5-c180 and M5-c184", status="FAIL",
         evidence=f"Round-3 defect (M5-c180 and M5-c184 both test the Lab 1 Part C result) is fixed: M5-c184 is removed. A full token-overlap scan ({S}/cards_r4.py, {O}/cards_r4.out) and reading finds three remaining duplicated facts: (1) M5-c173 and M5-c175 both state Proposition 4.1 (f = 0 below 1/2, 1 from 1/2, step G at 1/2: no Riemann-Stieltjes integral), c175 only adds that G is nondecreasing (Remark 4.2); (2) M5-c229 ('the policy chooses 0.25 at k = 0.5') is a subset of M5-c231 ('0.25 at every grid point'); (3) M5-c135 (L08) and M5-c160 (L09) both state that the grid fixed point or certificate is not the continuous problem's value (discretization error). "+SEV,
         fix="(1) Merge M5-c175 into M5-c173 or reword c175 to ask only about nondecreasing G with its own answer; (2) delete M5-c229; (3) keep one card for the discretization point and reword the other to ask about the certificate's coverage only (c160 already does that)."),
    dict(id="M5c3-L08-note-docstring", check="2.5 lab docstring vs code (L08 twin)", location="tests/labs/M5/lab-M5-L08-1.py docstring line 147 ('the fixed point is u / (1 - BETA) = 5 at BETA = 0.9')", status="FAIL",
         evidence="The docstring writes u as a number but never defines it: the docstring names u(c) = sqrt(c) as the utility function, and the value u(1/4) = 1/2 that makes u/(1-BETA) = 5 is not stated. The code checks 5 (part_c, abs(values[0] - 5.0) <= 1e-9), so the claim is true with u = 1/2 (numbers_r4.out: V*=5.000000000000001). "+SEV,
         fix="In the twin docstring, write 'the fixed point is u / (1 - BETA) with u = u(1/4) = 1/2, which is 5 at BETA = 0.9' (a lab-file change; not made by this verifier)."),
    dict(id="M5c-prose-footer", check="2.3 grades and 2.9 footer statements", location="course/modules/M/M5/L08.html:501; L09.html:510; L10.html:620", status="PASS",
         evidence="Round-3 FAIL (the footer said every claim carries an evidence grade, which L09 Remark 2.5 and the misconception bodies contradict) is fixed: the footer now reads 'Each graded result carries a grade; this page cites no registry source.' Every Lemma, Theorem, Proposition and Corollary block carries data-grade (grep); the page cites no registry key (grep data-cite, data-locator: 0). The statement is true. The Example 3.3 display gap is a separate row."),
    dict(id="M5c3-L09-misc2-heading", check="2.9 misconception heading vs body (L09 Misconception 2)", location="course/modules/M/M5/L09.html:293-294", status="PASS",
         evidence="Round-3 FAIL resolved. The heading is now 'The certified bound applies to the continuous savings problem.' and the body (L09.html:294) says the lab measures the error against the grid fixed point only and does not measure the discretization error. The body now corrects the stated belief."),
    dict(id="M5c3-L09-misc3-fixed-count", check="2.4 misconception claim (L09 Misconception 3)", location="course/modules/M/M5/L09.html:298", status="PASS",
         evidence="Round-3 FAIL resolved. The body now says a count certifies a tolerance tau when cert_N <= tau (Theorem 2.4), so a fixed count has no tolerance attached until its certificate is compared with one; the 10-step count (cert 1.7433922005) is valid but above 1e-6. Checked against numbers_r4.out: cert_10 = 1.7433922005 > 1e-6 and cert_147 = 9.389e-7 <= 1e-6, so no universal claim remains."),
    # ---- new round-4 LOW rows ----
    dict(id="M5c4-L10-ex33-bound-step", check="2.4 mathematics (Example 3.3, the 1/n bound is not shown)", location="course/modules/M/M5/L10.html:147 (Example 3.3: 'Both differ from 2/3 by at most 1/n.')", status="FAIL",
         evidence="The claim is true and follows from the displayed closed forms (numbers_r4.out): right minus 2/3 = (3n-1)/(6n^2) <= 1/(2n); left minus 2/3 = -(3n+1)/(6n^2), with absolute value <= 2/(3n) <= 1/n. The page writes the bound before the derivation and gives no step that subtracts 2/3. "+SEV+"If the architect reads 'unproved' strictly under ruling 26, this row is blocking.",
         fix="Add one line after the closed forms: 'Subtracting 2/3, the right error is (3n-1)/(6n^2) <= 1/(2n) and the left error is -(3n+1)/(6n^2), whose absolute value is at most 2/(3n); both are at most 1/n.'"),
    dict(id="M5c4-L10-R1-weakest-hypothesis", check="2.4 mathematics (Problem R1 asks for the weakest hypothesis)", location="course/modules/M/M5/L10.html:494-496 (Problem R1 and its solution)", status="FAIL",
         evidence="R1 asks to 'state the weakest hypothesis on G' that the proof, as written, needs'. The solution lists the three uses of continuity of G' (M finite via Lemma 2.1(i); G' integrable on each I_i for (Q3); f G' integrable via Lemma 2.2) and says the proof establishes the theorem under continuity, but it does not state the hypothesis the question asks for. The three uses are correctly identified (L10.html:129-132). "+SEV,
         fix="State what the proof as written uses: G' bounded on [a,b], G' Riemann-integrable on each I_i (for Assumption 1), and f G' integrable on [a,b]; note that Lemma 2.2 supplies the last one only when G' is continuous, so the answer is continuity of G' as the sufficient condition the proof checks."),
    dict(id="M5c4-L10-ex33-grade-display", check="2.3 grades (Example 3.3 carded T but not graded on the page)", location="course/modules/M/M5/L10.html:146 (Example 3.3 block); cards.json M5-c170, M5-c233, M5-c234, M5-c171", status="FAIL",
         evidence="The closed forms of Example 3.3 are derived on the page (L10.html:147), and the cards grade them T with basis 'Example 3.3 (proved on the page)', which ruling 13 allows. The block itself carries no data-grade and no key-results row lists it, so the page shows no grade for a result the cards grade T. "+SEV,
         fix="Give the Example 3.3 block a T grade with basis 'Example 3.3' and add a key-results row for the two closed forms, or, if the owner prefers, change the four cards to match the page's ungraded display. Either way the card and the page must agree."),
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
prev_ids = [r["id"] for r in json.loads(Path("/Users/billyribeiro/.fanout/frags/S-M5-c.round3.json").read_text())["rows"]]
missing = [i for i in prev_ids if i not in ids]
print("round-3 ids missing:", missing)

fragment = {
    "unit": "M5",
    "slice": "c",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for M5-c (L08-L10 pages, lab twins and cards), round 4, final full verification under FINAL-ARCHITECT-RULINGS 1-26 (ruling 26 severity rule applied). No build-side context; the round-3 fragment was read as context only and every row was re-derived this round.",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin). Delta for slice c from git diff 8196077d edbb7aa8: course/modules/M/M5/L08.html (why-it-matters, interpretation, Problem R2 solution, footer), L09.html (Lemma 1.2 wording, Misconception 2 heading and body, Misconception 3 body, footer), L10.html (why-it-matters, Remark 3.6, lab hypothesis, M2 solution, footer), cards.json (M5-c160, c161, c184 removed, c205 removed, c241 added in L07). tests/labs/M5 and notation/ unchanged in the delta.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-M5-c",
    "scratch": "ledgers/M5/scripts/M5-c-r4/out (all outputs); scripts ledgers/M5/scripts/M5-c-r4/{gates.sh,page_twin_compare.py,numbers_r4.py,cards_r4.py,build_fragment_r4.py}",
    "verified_at": "2026-11-09T07:37:15Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Not a project slice: lab twins are demonstrations and ruling 9 applies to project graders, so no mutant was written or run. "
        "Ruling 26 acceptance: all six non-PASS rows are LOW (wording, presentation or card style), and none is a blocking kind "
        "(false or unproved math, missing hypothesis, wrong number, over-grade, failing gate, surviving non-equivalent mutant, lab statement the code does not support). "
        "Under ruling 26 the slice is accepted when these LOW rows are listed in plans/KNOWN-ISSUES.md with their ids; the ledger verdict stays FAIL until they are fixed, per VERIFIER_RULES section 3. "
        "Row M5c4-L10-ex33-bound-step is borderline: an unwritten one-line inequality, which the verifier classes LOW; a strict reading of 'unproved' makes it blocking. "
        "Round-3 FAIL rows M5c-num-L08-ratio-unrounded, M5c-cards-L08, M5c-prose-footer, M5c3-L09-misc2-heading and M5c3-L09-misc3-fixed-count are re-verified PASS. "
        "Every other round-3 PASS row was re-run or re-derived this round (none carried). "
        "Not checked: the repository-wide gates outside the slice (check_pages --all, check_dag --all, build_site --check, render_curriculum, fetch_data --check, run_graders and mutate_graders for M5, verify_refs live run); the rendered pages were not screenshotted; the L07 Proposition 2.4 card (M5-c241) is outside the slice; the notation macros beyond those used in the slice were not audited; tools/ledger.py merge was not run (it would merge M5-a/b/d fragments)."
    ),
    "summary": (
        "M5-c round 4 on edbb7aa8: verdict FAIL by the ledger rule, but no blocking row. All gates, twins, page smoke, mypy and pytest pass; "
        "every number, proof and quiz key in L08-L10 re-derived; the round-3 blocking defects (unsourced L08 ratio, false L09 universal claim, misconception heading, footer over-claim, duplicate Lab 1 Part C card) are fixed. "
        "Six LOW rows remain: one card gap (Example 1.2), three card duplicates, one lab docstring symbol, and three L10 presentation items (unwritten 1/n step in Example 3.3, Problem R1 answer, Example 3.3 grade display)."
    ),
    "counts": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0},
}

out = Path(ROOT / "ledgers/M5/M5-c.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", fragment["counts"]["pass"], "fail", fragment["counts"]["fail"])
