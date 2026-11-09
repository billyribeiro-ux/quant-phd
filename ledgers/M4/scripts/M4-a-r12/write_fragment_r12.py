"""Writes the round-12 slice-a fragment ledgers/M4/M4-a.json (rows, verdict and notes from the M4-a-r12 checks)."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/M4/scripts/M4-a-r12/"
rows = []

def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates and commands
row("A-G01", "2.9 structure gate", "tools/check_pages.py --unit M4", "PASS", f"'check_pages M4: PASS' ({S}check_pages.out)")
row("A-G02", "2.9 DAG gate", "tools/check_dag.py --unit M4", "PASS", f"'check_dag M4: PASS' ({S}check_dag.out)")
row("A-G03", "2.6 projects gate (command row; project.html is outside slice a)", "tools/check_projects.py --unit M4", "PASS", f"'check_projects M4: PASS' ({S}check_projects.out)")
row("A-G04", "2.5 labs", "tools/run_labs.py --unit M4", "PASS", f"'run_labs M4: PASS (13/13)' ({S}run_labs.out)")
row("A-G05", "2.5 twins alone; page code equals twin; expected equals output", "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py vs course/modules/M/M4/L01..L04.html", "PASS",
    f"Each twin run alone from /tmp as python -I -W error: exit 0 ({S}twin_L01..L04.out). {S}twin_compare.py: page code equals twin except the final newline the page omits (True for all four); expected block equals stdout (True for all four).")
row("A-G06", "2.9 page_smoke (pages alone)", "tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04", "PASS",
    f"'page_smoke M4: PASS'; every page and every lab PASS; lab runtimes 0.0 s ({S}page_smoke.out)")
row("A-G07", "ruff", "ruff check tests/labs/M4 course/modules/M/M4; ruff format --check tests/labs/M4", "PASS",
    f"'All checks passed!' and '13 files already formatted' ({S}ruff_check.out, {S}ruff_format.out)")
row("A-G08", "mypy strict", "mypy --no-incremental", "PASS", f"'Success: no issues found in 385 source files' ({S}mypy.out)")
row("A-G09", "repository state", "git status after all gate runs", "PASS",
    "No tracked file is modified by any gate; render_curriculum rewrote its generated files byte-identically (git diff exit 0)")
row("A-G10", "relevant pytest", "tests/test_labs.py test_run_labs.py test_page_checks.py test_docs_figures.py test_page_smoke.py test_curriculum.py", "PASS",
    f"All tests passed, exit 0 ({S}pytest_relevant.out)")
row("A-G11", "2.1 registry", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M4 (live Crossref)", "PASS",
    f"Offline: '560 entries, 0 problems'. Live for M4: '1 of 560 entries, 0 problems' ({S}verify_refs_offline.out, {S}verify_refs_live_M4.out)")
row("A-G12", "2.7 card numbers; no dangling card ids", "course/modules/M/M4/cards.json vs L01..L04.html; grep for removed ids", "PASS",
    f"{S}card_numbers.py: 142 numbers in the backs of the 90 slice cards (6 or more, and fractions) occur verbatim in their lesson HTML. No page or twin mentions M4-c014, c046, c124, c219 or c244 (grep).")
row("A-G13", "2.8 generated site data (not edited)", "tools/build_site.py --check", "PASS", f"'site data current: 6 outputs' ({S}build_site_check.out)")
row("A-G14", "2.8 data manifest", "tools/fetch_data.py --check", "PASS", f"'fetch_data: 3 datasets, 0 problems' ({S}fetch_data_check.out)")
row("A-G15", "generated curriculum current", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
    f"'curriculum valid: 25 parts, 134 modules, 157 projects'; diff exit 0 ({S}render_curriculum.out, {S}render_curriculum_diff.out)")

# ---- hub
row("A-H01", "2.9 structure: hub", "course/modules/M/M4/index.html:29-184", "PASS",
    "Sections present in order: objectives (line 45, six items), prerequisites (58), placement quiz (68, ten items), lessons (145, ten cards), project ladder (162, four rungs), data status (173), core reading (178).")
row("A-H02", "hours arithmetic", "index.html:29 data-hours-lessons=90 data-hours-project=30; L01..L10 data-hours=9", "PASS",
    "10 x 9 = 90 lesson hours; project 30 h; 30/120 = 25% (index.html:42 text); bar widths 75%/25% (index.html:39-40). Curriculum hours 120 at curriculum/01-foundations.yaml:193.")
row("A-H03", "2.9 objectives", "index.html:48-56", "PASS", "Six objectives (4 to 8 allowed) each opening with a measurable verb (Compute, Derive, Compute, Decide, Derive, State).")
row("A-H04", "prerequisites and links", "index.html:58-66; curriculum/01-foundations.yaml:88, :123, :190-194", "PASS",
    "M1 title 'Precalculus & Mathematical Reasoning' (yaml:88) and M2 'Single & Multivariable Calculus' (yaml:123) match the hub text; M4 prereqs [M2] (yaml:194). All 82 internal links in index and L01..L04 resolve to existing files and anchors (link_check.py: 0 problems).")
row("A-H05", "DAG: no M3 concept by name", "index.html; L01..L04.html", "PASS",
    "grep for eigen, semidefinite, projection, singular value, vector space: no hits in L01..L04; hub hits are prose saying M4 does not use M3 (index.html:64).")
row("A-H06", "placement structure", "index.html:68-143; M1 course/modules/M/M1/L01.html:79", "PASS",
    "section.quiz id=placement, data-mastery 0.8; ten items: eight M1/M2 items and two data-skill items. The M1 Theorem 3.1 cited in the first item's explanation exists (M1 L01.html:79, 'negating one quantifier').")
row("A-H07", "placement keys (M1/M2 items)", "index.html:73-131", "PASS",
    f"Recomputed (recompute_numbers.py): lim 1/n = 0; int_0^1 x dx = 1/2; ln(e^3) = 3; 1+1/2+1/4+1/8 = 15/8 = 1.875; discount 1/(1+r); d/dx(x^2 y) = 2xy. Options marked correct match.")
row("A-H08", "placement skill check 2 (rung 2)", "index.html:140; course/modules/M/M4/L06.html:59 (Assumption 1), :158 (Proposition 2.6)", "PASS",
    "Key 0.6 = 3/5 = (nu-2)/nu at nu = 5 = 1/Var(t_5), Var(t_5) = 5/3 from L06 Proposition 2.6 (L06.html:158); scale-rule hypothesis stated as not proved (L02 Proposition 2.3 covers finite laws only, L02.html:115).")
row("A-H09", "placement skill check 1 (rung 1) key", "index.html:133-135", "PASS",
    "Key 1: F(0) = 1/4 < 1/2 and F(1) = 3/4 >= 1/2, so Q(1/2) = 1 (recompute_numbers.py L01 quiz line). The explanation's claim is judged separately in A-H16.")
row("A-H10", "lesson-card descriptions L01-L04", "index.html:147-160 vs L01..L04.html headings and content", "PASS",
    "L01 (quantile with left-endpoint convention), L02 (shortcut and scale rule checked on die and loss), L03 (affine maps, Bernoulli exact values, kurtosis floor 1), L04 (independence on a joint table, zero covariance without independence, conditional expectation) each match the lesson's headings and labs.")
row("A-H11", "project cross-reference (round 11 FAIL)", "index.html:70, :164; course/modules/M/M4/project.html:42", "PASS",
    "project.html:42 now reads 'answered both skill checks', matching the hub's placement and ladder text. Round-11 row A-H11 resolved.")
row("A-H12", "data labelling", "index.html:37, :175, :187 (footer); L02.html:146; L03.html:122", "PASS",
    "Seeded samples are labelled SIMULATED on the labs that print them (L02, L03); the hub states no real data is used.")
row("A-H13", "reference: blitzstein2019introduction", "index.html:181-183; references/references.json (key blitzstein2019introduction)", "PASS",
    "Record: DOI 10.1201/9780429428357, isbn [9780429428357], publisher Chapman and Hall/CRC, year 2019, no edition field, source string 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)'. The hub says the edition is not checked against the book, which matches the record. Registry flag below.")
row("A-H14", "curriculum entry for M4", "curriculum/01-foundations.yaml:190-194", "PASS", "id M4, title 'Probability', tier F, hours 120, prereqs [M2], as the hub meta states (index.html:31, :35).")
row("A-H15", "project ladder", "index.html:162-170; course/modules/M/M4/project.html:42-47", "PASS",
    "Four rung-title items in order; project.html names rungs 1 to 4 the same way; rung 2 is graded instantly (check_projects PASS). Rungs 1-2 skip rule matches project.html:42.")
row("A-H16", "hub claim: rung 1 worked example", "course/modules/M/M4/index.html:135 ('This is the worked example of rung 1.')", "FAIL",
    "Rung 1 (project.html:56-58, lab-M4-project-1) is a seeded two-asset portfolio 99% loss by the rank ceil(0.99 n) of sorted losses. The item asks for the 0.5 quantile of a three-value law. The convention is the same (Lesson 1 Proposition 3.4), but the item is not the worked example.",
    "In index.html:135 replace 'This is the worked example of rung 1.' with 'The same convention as rung 1 applies: the quantile is the least value whose distribution function reaches the level (Lesson 1, Proposition 3.2), and rung 1 uses the rank ceil(0.99 n) of equally likely losses (Lesson 1, Proposition 3.4).'")

# ---- lessons L01
row("L01-PROSE", "2.9 prose and definitions", "course/modules/M/M4/L01.html:51-99", "PASS",
    "Definitions 1.1, 1.2, 2.1, 3.1 and the why-it-matters paragraph read in full; the infimum is defined (line 95) before its use in Definition 3.1 (line 99); quantifier logic cross-link to M1 concept.")
row("L01-MATH", "2.4 mathematics", "L01.html:80-135 (Props 2.2, 3.2, Remark 3.3, Prop 3.4, Examples 3.5, 3.6)", "PASS",
    "Each proof re-read. Left-continuity and jump claims re-derived; Example 3.5 gives 149 for n=150 (pn=148.5) and 198 for n=200; 148/150 = 74/75 = 0.98667 (recompute_numbers.py). Q values of Example 3.6 recomputed: Q(1/2)=0, Q(3/5)=0, Q(61/100)=1.")
row("L01-DELTA-86", "delta hunk: Proposition 2.2(d) wording", "L01.html:85-86 (changed in 5db69a9b/e919577b)", "PASS",
    "New text: 'F is right-continuous at each x_k, meaning that F(x) -> F(x_k) as x decreases to x_k, and it jumps ...'. Checked: F is constant on [x_k, x_{k+1}) (Prop 2.2(b)), so the right limit is F(x_k); the left limit at x_k is F_{k-1}, the jump p_k > 0. Correct.")
row("L01-PROBLEMS", "2.4 worked solutions", "L01.html:302-404", "PASS",
    "M1 (F and Q(1/2) of a parity variable: 0), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (indices 36 and 37), P1-P3 proofs, E1-E3 match Lab 1 output (Q(99/100)=3, 'Q(F(0)+eps)=1', '100 of 100'), R1 strict-rule argument (Q^s(3/5)=1 and agreement elsewhere) re-proved, R2 left-continuity, R3 grid check scope. All numbers recomputed.")
row("L01-QUIZ", "retrieval quiz", "L01.html:424-494", "PASS",
    "Nine items; keys recomputed: Q(1/2)=1 for (1/4,1/2,1/4); Q(61/100)=1; index 198 and 149; P(X<=1)=5/6=0.833 (tolerance 0.0005); Q(F_k)=x_k; Q(1)=x_m; answers 'No' and 'A function' marked correctly.")
row("L01-GRADES", "2.3 grades", "L01.html:43-48, :103, :113, :119, :413-418", "PASS",
    "Every proposition and remark carries data-grade T; key-results table grades T with 'Proved in' sources; lab output is labelled exact computation, not graded as evidence.")
row("L01-FWD", "2.9 forward references", "L01.html:37-38, :95, :505", "PASS", "Uses only quantifiers (M1) and the infimum (defined in §3, the place where first used); next-lesson link to L02.html.")
row("L01-LAB", "2.5 lab statements", "L01.html:138-271; tests/labs/M4/lab-M4-L01-1.py", "PASS",
    "Hypothesis (line 140) predicts exactly the printed quantiles, the 100-of-100 agreement and the jump; interpretation (line 270) states one-checked-level for eps = 1e-9. Output lines 252-269 equal the twin's stdout (twin_L01.out).")

# ---- lessons L02
row("L02-PROSE", "2.9 prose and definitions", "L02.html:51-101", "PASS", "Why-it-matters, Definitions 1.1, 1.6 and 2.1 read; 'Lesson 3 uses both in the standardized variable of its Definition 2.1' is correct (L03.html:70-71).")
row("L02-MATH", "2.4 mathematics", "L02.html:63-142", "PASS",
    "Props 1.2, 1.3, 2.2, 2.3, 2.4 and Examples 1.4, 1.5, 2.5, 2.6 re-derived. Die: E=7/2, E[X^2]=91/6, Var=35/12=2.9167, sd=1.7078 (about 1.708). Loss: E=12500, E[L^2]=3125000000, Var=2968750000, sd=54486.24. Recomputed by recompute_numbers.py.")
row("L02-LAB", "2.5 lab statements", "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
    "Hypothesis (line 146) lists the exact values and says the printed difference is for the die only; line 262 interpretation (3.469, -0.031, 489 losses, 12225.0 cents) equals output (twin_L02.out). Seeds 2026/2027 stated.")
row("L02-PROBLEMS", "2.4 worked solutions", "L02.html:298-401", "PASS",
    "M1 (21/100), M2 (2.25e8 cents squared, sd 15000), M3 (36, 4), P1-P3 proofs (P2 identity and P3 counterexample U+V=0 with Var 0 vs 2), E1-E3 match output, R1 divisor-n identity, R2 (Var(D)=296875; sd 544.8624 = 54486.24/100), R3 (3/10 expectation vs Q(1/2)=0). Numbers recomputed.")
row("L02-QUIZ", "retrieval quiz", "L02.html:421-492", "PASS", "Ten items; keys 3.5, 1, 12, 5000, 225000000, 21/100, c=E[X], 15000, 5 recomputed and correct.")
row("L02-CANON", "2.4 canon-breaks", "L02.html:269-272", "PASS",
    "The inequality X^2 <= 2(X-mu)^2 + 2 mu^2 gives E[X^2] <= 2 Var + 2 mu^2 (verified algebraically), so infinite E[X^2] forces infinite variance. The example mean 3/10 = (-2 - 2 + 0 + 2 + 2 + 3)/10 and Q(1/2) = 0 are correct.")
row("L02-MISC", "misconceptions", "L02.html:279-296", "PASS",
    "91/6 is about 15.17 and 35/12 about 2.92 (recomputed). 'The two agree only when E[X]=0' follows from Var = E[X^2] - mu^2. Die sample mean 3.469 for seed 2026 matches output.")
row("L02-FWD-COVARIANCE", "forward reference", "L02.html:345-347 (P3)", "PASS", "P3 states that the lesson does not derive a general formula for Var(U+V); there is no forward dependence on L05.")
row("L02-FOOTER-SCOPE", "scope and footer", "L02.html:494-507", "PASS", "Reference section says no passage from Blitzstein was read and attributes nothing to it; footer says the seeded samples are SIMULATED and not proofs.")

# ---- lessons L03
row("L03-PROSE", "2.9 prose and definitions", "L03.html:51-76", "PASS",
    "Definition 2.1 (standardized variable), Definition 2.2 (gamma_3 = E[Z^3], gamma_4 = E[Z^4], no subtraction of 3) read; 'every kurtosis computed on this page is E[Z^4]' holds (Props 2.3-2.5, Example 2.6).")
row("L03-MATH", "2.4 mathematics", "L03.html:57-134", "PASS",
    "Props 1.1, 2.3, 2.4, 2.5 and Example 2.6 re-derived. Bernoulli: m3 = pq(1-2p), m4 = pq(1-3pq); gamma_3 = (1-2p)/sqrt(pq); gamma_4 = (1-3pq)/(pq). p=1/10: gamma_3 = 8/3, gamma_4 = 73/9 = 8.11, gamma_3^2 = 64/9. p=1/4: gamma_4 = 7/3, gamma_3 = 2/sqrt 3 = 1.155. Props 2.5 proof (W = Z^2, Var(W) = gamma_4 - 1) re-derived.")
row("L03-LAB", "2.5 lab statements and numbers", "L03.html:120-239; tests/labs/M4/lab-M4-L03-1.py", "PASS",
    "Printed exact values: m2 = 163/16, m3 = 2157/32, m4 = 149461/256, squared skewness 18610596/4330747 = 4.29732, skewness 2.0730, kurtosis 149461/26569 = 5.6254. Recomputed independently (recompute_numbers.py). Sample line (2.065, 5.580) equals output; gaps 0.008 and 0.045 and the 0.001 rounding bound are arithmetic-correct.")
row("L03-NUMBERING", "numbering and cross-references", "L03.html:53-110 and cross-refs at :64, :71, :86, :96, :106", "PASS",
    "Definitions 2.1-2.2, Props 1.1, 2.3-2.5, Example 2.6 are numbered consecutively; cross-references to L02 Definition 2.1, Proposition 1.3, 2.2, 2.3, 2.4 point to the right results (L02.html:51-101, :63-142).")
row("L03-STD-NORMAL-DUP", "normal law and kurtosis claims (round 11 open item)", "L03.html (whole page)", "PASS",
    "grep 'normal' in L01..L04: no hits. No normal-kurtosis claim and no forward pointer to L06 remains; the round-11 open item (Builder A item 1) is no longer an issue on this page.")
row("L03-CANON", "2.4 canon-breaks", "L03.html:241-250", "PASS",
    "Law on -2, 1, 3 with probabilities 2/5, 1/2, 1/10: mean 0, m2 = 3, m3 = 0, m4 = 15, gamma_4 = 5/3, not symmetric (value 2 has probability 0). Recomputed.")
row("L03-MISC", "misconceptions", "L03.html:252-268", "PASS",
    "Bernoulli p = (1 - 1/sqrt 3)/2 gives pq = 1/6 and gamma_4 = 3 (recomputed 3.000000000000002). Sign-reversal claim follows from Prop 2.4.")
row("L03-PROBLEMS", "2.4 worked solutions", "L03.html:270-373", "PASS",
    "M1 (sigma = sqrt3/4, gamma_3 = 2/sqrt3, gamma_4 = 7/3), M2 (mu=1, gamma_4=1), M3 (m3 = 2157/32; the four terms -1372/512, -54/512, 1/512, 35937/512 re-added), P1-P3 proofs, E1-E3 (gap 0.008 and 0.045; Bernoulli checks; integer weights 4,2,1,1 sum to 8), R1 (kurtosis exactly one only for the symmetric two-point law), R2 (the 73/9 law has no tail), R3 (symmetric implies zero skewness, converse fails by §4). Numbers recomputed.")
row("L03-QUIZ", "retrieval quiz", "L03.html:392-462", "PASS", "Nine items; keys 0, 1, 1.6667 (5/3), 2.6667 (8/3), options for sign change, affine kurtosis invariance and symmetry checked against Props 2.4 and §4.")
row("L03-GRADES", "2.3 grades", "L03.html:42-49, :381-388, :401-407", "PASS", "Propositions and Example 2.6 carry T; key-results table T; sample values are labelled SIMULATED single-run estimates and are not graded as theorems.")
row("L03-FOOTER-SCOPE", "scope and footer", "L03.html:464-477", "PASS", "Reference and footer say the sample is SIMULATED and not a proof; no source attributed.")
row("L03-PROP28-SCOPE", "hypotheses of Props 2.4 and 2.5", "L03.html:89-101", "PASS",
    "Props 2.4 and 2.5 state 'at least two values' and positive weights (Prop 2.4 also a nonzero a); the proof of Prop 2.5 uses these (Var(W)=0 needs a single value for W).")

# ---- lessons L04
row("L04-PROSE", "2.9 prose and definitions", "L04.html:52-70, :137-145", "PASS", "Definitions 1.1, 1.2, 1.6 and 2.1, Remark 1.3 and Remark 2.2 read in full; the scope limits (finite tables only) match the canon-breaks section.")
row("L04-TERM-ORDER", "terms before definition", "L04.html:52 vs :59, :65, :98, :131, :139", "PASS", "'joint table' is used at line 52 with the explicit pointer 'Definition 1.1 below' and defined at line 59; 'covariance' is defined in Definition 1.6 (line 98) before Proposition 1.7.")
row("L04-REMARK-1-3", "Remark 1.3 claim", "L04.html:70; tests/labs/M4/lab-M4-L04-1.py main()", "PASS", "'applies the test to every cell of three tables (Parts A and B)': Part A has product and dependent tables, Part B the uniform table; the code applies is_independent to each (all() over cells).")
row("L04-MATH", "2.4 mathematics", "L04.html:73-169", "PASS",
    "Props 1.4, 1.5, 1.7, 1.8, 2.3, 2.4 and Examples 1.9, 2.5 re-derived. Example 1.9: E[X]=0, E[Y]=2/3, E[XY]=0, Cov=0, p(0,0)=1/3 vs 1/9. Example 2.5: E[X|Y=0]=1, E[X|Y=1]=2/3, E[X]=4/5, total-expectation sum 4/5.")
row("L04-DELTA-53", "delta hunk: why-it-matters wording", "L04.html:52-53 (changed in 5db69a9b/e919577b)", "PASS",
    "New text: 'Example 1.9 gives a pair that is not independent but still has E[XY] = E[X]E[Y]'. Checked: E[XY]=0=E[X]E[Y]; p(0,0)=1/3 != 1/9 = P(X=0)P(Y=0). Correct; Lab 1 Part B prints both.")
row("L04-PROBLEMS", "2.4 worked solutions", "L04.html:331-434", "PASS",
    "M1 (product 0.12 vs 0.1, dependent), M2 (2/3), M3 (1/8 two ways), P1-P3, E1 (sum 4/5), E2 (ratio 3), E3 (ratio 5/8 = 0.625), R1 (Cov 0, dependent), R2, R3 (conditional expectations all 0). Numbers recomputed.")
row("L04-QUIZ", "retrieval quiz", "L04.html:453-527", "PASS", "Ten items; keys 1, 0.8, 0, 0.6, 0.06 (3/50) recomputed; options and explanations correct.")
row("L04-CANON-MISC", "canon-breaks and misconceptions", "L04.html:303-329", "PASS",
    "Marginals example (p(0,0)=1/2 vs 1/4), E[XY]=1 vs 0 for Y=X, zero covariance counterexample, and misconception on disjoint events all recomputed and correct.")
row("L04-FOOTER", "footer and references", "L04.html:530-543", "PASS", "No outside source cited; footer says no registry source is cited, matching the page.")
row("L04-FWD", "forward reference to L05", "L04.html:52, :99, :539", "PASS", "L05 is named as the place where correlation and the covariance matrix are developed; no L04 result depends on it.")
row("L04-LAB", "2.5 lab statements", "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
    "Hypothesis (line 174) and interpretation (line 300) match output lines 283-299 (3/50 both sides; 1/10 vs 4/25; 1/3 vs 1/9; covariance 0; 4/5; 1; 2/3). Expected block tolerance 1e-9 is harmless for exact fractions; output identical.")

# ---- cards
row("CARDS-DUP", "2.7 duplicate cards (full scan of the 90 slice cards)", "course/modules/M/M4/cards.json: M4-c028 vs M4-c023; M4-c065 vs M4-c061", "FAIL",
    f"M4-c023 'How does variance change under X to aX + b?' -> Var(aX+b)=a^2 Var(X); M4-c028 'Does scaling X by a multiply its variance by a?' -> No, Var(aX)=a^2 Var(X): same fact, same answer. M4-c061 'Under independence, does E[X|Y=y] equal E[X]?' -> Yes; M4-c065 'Is E[X|Y=y] always the same as E[X]?' -> No, equality holds under independence: same fact, same answer. Pairwise scan in {S}card_dups_pairs.txt. Other similar pairs (c022/c029, c008/c009) test different facts and are not counted.",
    "Delete M4-c028 and M4-c065 from cards.json (or reword each to a fact no other card covers), then rerun check_pages --unit M4.")
row("CARDS-L01", "2.7 cards L01", "cards.json: M4-c001..c016, c173, c192..c195, c197, c198, c245 (23 cards)", "PASS",
    "Each back checked against the lesson text and its hypotheses; grades T; no cite needed for T; numbers verbatim (A-G12).")
row("CARDS-L02", "2.7 cards L02", "cards.json: M4-c017..c033, c181, c182, c199, c243 (21 cards)", "PASS",
    f"Backs checked; grade C cards c030 and c033 carry basis 'Lab 1 (SIMULATED), seed 2026/2027' and match the printed lines (3.469; 489 vs 500). c028's content is correct; its duplication is CARDS-DUP.")
row("CARDS-L03", "2.7 cards L03", "cards.json: M4-c034..c048, c183, c200, c212, c214, c215, c222..c229 (27 cards)", "PASS",
    "Backs checked; grade C cards c047 (2.065 vs 2.073) and c183 (5.580 vs 5.625) carry basis 'Lab 1 (SIMULATED), seed 2026' and match output.")
row("CARDS-L04", "2.7 cards L04", "cards.json: M4-c049..c065, c201, c204 (19 cards)", "PASS",
    "Backs checked against L04 definitions, propositions and examples; c065's content is correct; its duplication is CARDS-DUP.")
row("CARDS-DELTA", "delta: cards changed or added in slice a", "cards.json: M4-c192 (hypotheses added), c244 deleted, c245 added", "PASS",
    "c192 now carries 'Hypotheses: positive weights and distinct values' and the answer (0<p<=1 range (3/5,4/5]) is correct. c244 (L02 'Does adding a constant change variance?') is absent and no card or page refers to it. c245 'For the table of Example 3.6, what is Q(3/5)?' -> 0 is correct (F(0)=3/5 reaches 3/5). Deltas in cards at other lessons (L05, L08) are outside slice a.")
row("CARDS-NUMBERS", "2.7 card numbers appear in lesson", "cards.json (90 slice cards) vs L01..L04.html", "PASS", "card_numbers.py: 142 checked numbers, all verbatim in the lesson text.")
row("CARD-M4-c219", "round-11 row kept by id", "cards.json (no M4-c219 at pin 329c1d7)", "PASS",
    "Python id lookup: M4-c219 is not in cards.json at this pin, and no page or twin refers to it (grep). Nothing dangling.")

# ---- notation, process, scope, data, structure, numbers, grades, assumptions, DAG
row("NOTATION-A", "2.4 / notation registry", "notation/notation.json vs index.html, L01..L04.html", "PASS",
    "Registered symbols used in slice a: \\gamma_3 and \\gamma_4 (L03.html:76, :81, :86) with the registry meanings (E[Z^3], E[Z^4] of the standardized variable, not excess). Registered \\Phi, T, R^*, R^{e*}, R_f and \\mathbb{Q} are not used in slice a. Local letters mu, sigma, alpha, beta, delta and m_k are allowed by the registry's 'about' text. Plain P and E are not registered macros and collide with nothing registered. Observation (not a failure): p denotes a weight p(omega) (L01 §1), a quantile level (L01 §3), a Bernoulli parameter (L03) and a joint probability (L04); each section fixes its meaning.")
row("NOTATION-REG", "registry entries for gamma", "L03.html:75-86 vs notation.json (\\gamma_3, \\gamma_4 entries)", "PASS", "Registry gamma_4 says 'not excess; 3 under normality'. L03 never asserts the normal value, so nothing conflicts.")
row("NOTATION-MACRO", "registered macros only", "index.html, L01..L04.html", "PASS", "Macros used: \\R, \\tfrac, \\operatorname, \\varepsilon, \\lceil, \\varnothing, \\mid and standard LaTeX; no unregistered custom macro (page_smoke strict-math check PASS).")
row("PROCESS-A", "2.9 process words in learner text", "index.html; L01..L04.html visible text; cards.json (slice)", "PASS",
    "grep for builder, verifier, round, ledger, TODO, placeholder, draft, fragment, architect, open item, Q-numbers: no learner-text hits. 'Predicted before running' and 'Stated before running' are the BUILDER_RULES §5 lab-hypothesis template (BUILDER_RULES.md:279), not process words.")
row("SCOPE-A", "scope words", "L01..L04.html; index.html (every, all, only, always, any, same, exactly)", "PASS",
    "Each scope word was reviewed: 'every point' statements are backed by Prop 3.2 or by a grid stated as finite (L01.html:270, :376); 'no tail beyond them' for the two-point law (L03.html:362) is about the two-value law only; 'only' claims are proved (L03.html:355 R1, L03.html:246). No unbacked 'always' or 'every' found.")
row("DATA-A", "2.8 data", "index.html:37, :175, :187 (footer); L02.html:146, :507; L03.html:122, :477; no data-files attribute", "PASS",
    "No real data; no data-files; labs use exact tables or seeded draws; SIMULATED labelling present where samples are printed.")
row("STRUCT-A", "2.9 lesson structure", "course/modules/M/M4/L01..L04.html", "PASS",
    "Sections in the order of LESSON_SECTIONS (why-it-matters, numbered sections, canon-breaks, misconceptions, problems, key-results, quiz, references); data-hours 9; lab ids lab-M4-L0n-1; check_pages PASS.")
row("NUM-A", "2.2 numbers in prose", "index.html; L01..L04.html", "PASS",
    f"Every prose number in slice a recomputed by {S}recompute_numbers.py (exact fractions and float). Mismatches found: none. Checked: F and Q tables; 74/75 = 0.987; index 149 and 198; 40p = 36.04; 54486.24; 1.708; 15.17; 2.92; 544.8624; 2.0730; 5.6254; 8.11; 1.155; 0.008, 0.045 gaps; 0.031; 489 vs 500; 0.833; 0.625; 0.6; 0.6667.")
row("GRADE-A", "2.3 grades (re-graded)", "index.html; L01..L04.html; cards.json (slice)", "PASS",
    "Re-grading against BLUEPRINT §3: proved results T (correct); lab-observed seeded numbers are single-run estimates and are labelled SIMULATED in prose, which BLUEPRINT §3 accepts for computed-live numbers; exact labs are computations on a stated table. Observation for the architect: seeded sample values are not carried with a C grade in the prose (open item 20 in M4-open-items.md, unchanged).")
row("ASSUMP-A", "2.4 hypotheses and numbered assumptions", "index.html:138-140; L01..L04.html", "PASS",
    "No numbered Assumption in L01..L04. Every statement lists its hypotheses (finite space, positive weights, distinct values, at least two values, finitely many values). The hub's use of L06 Assumption 1 is explicit (index.html:140).")
row("DAG-A", "2.9 DAG and definitions once", "check_dag.py; L01..L04.html dfn tags (grep); link_check.py", "PASS",
    "Each of the eight dfn concepts in slice a is defined once: random-variable, quantile-function (L01); expectation, variance (L02); skewness, kurtosis (L03); independence, conditional-expectation-elementary (L04). 82 internal links resolve. Covariance is defined inline in L04 Definition 1.6 without dfn, as the plan allows.")
row("DAG-HUB-PREVIEW", "hub previews of L01-L04", "index.html:147-160", "PASS", "Previews match the lesson headings and content (see A-H10).")
row("DAG-L02-L04-USES", "uses before definition across L01-L04", "L02..L04.html meta lines 37-39", "PASS",
    "L02 uses L01 random-variable; L03 uses L01 random variable and L02 expectation, variance; L04 uses L01 random variable and L02 expectation; links point to earlier lessons only; no M3 or M5+ concept used.")
row("DAG-SD-TWICE", "round-11 FAIL: standard deviation defined twice (L02 vs L05, outside slice a)", "course/modules/M/M4/L05.html:79-80; L02.html:100-101", "PASS",
    "Re-verified at the pin: L05.html:79-80 is now 'Remark 1.3 (notation for the standard deviation)' pointing to L02 Definition 2.1. L05's dfn tags are only correlation (line 85) and covariance-matrix (line 126). Round-11 FAIL resolved.")

# ---- flags
registry_flags = [
    "blitzstein2019introduction: record has no edition field; the curriculum and source string say '2nd ed. (2019)'; the edition is unverified and no locator was read. The hub and lessons say so."
]
freshness_flags = []
mutants = []

fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] == "FAIL")
unv_n = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
summary = (f"Slice a round 12 at 329c1d7 (base ccaeeaf4): {len(rows)} rows; {pass_n} PASS, {fail_n} FAIL, {unv_n} UNVERIFIABLE. "
           "FAIL rows: A-H16 (index.html:135 says the rung-1 skill item is the rung-1 worked example; it is not) and CARDS-DUP "
           "(cards M4-c028 and M4-c065 repeat the fact and answer of M4-c023 and M4-c061). All L01-L04 numbers, proofs, labs and card numbers "
           "re-verified; round-11 FAIL rows A-H11 and DAG-SD-TWICE are now PASS. Mutants: none (lessons, hub and lab twins; no grader in slice a).")

notes = (
    "Round 12 at pin 329c1d7 (round-11 pin ccaeeaf4). Delta in slice a: L01.html:85-86 (Prop 2.2(d) wording), L04.html:52-53 (why-it-matters wording), "
    "cards.json (M4-c192 hypotheses added, M4-c244 deleted, M4-c245 added). Changes in L05 and project.html and in L08 cards are outside slice a and "
    "were not re-verified beyond cross-references. Full slice read this round: index.html (189 lines), L01.html (511), L02.html (509), L03.html (479), "
    "L04.html (545), the four twins and their output, and all 90 L01-L04 cards. No row carried forward: every row was re-verified at this pin. "
    "Not checked: the Blitzstein book (not read; no locator is claimed); visual rendering (slice a has no figures; page_smoke geometry only); "
    "L05-L10 and project.html except for cross-references; run_graders (no grader in slice a); mutation testing (rulings: lab twins are demonstrations). "
    "Judgment call: CARDS-DUP counts only same-fact, same-answer pairs; other restatement pairs (c022/c029, c008/c009) are not counted."
)

verifier = "Claude Haiku 5.5 independent verifier (verifyD12-M4-a)"
frag = {
    "unit": "M4",
    "slice": "a",
    "round": 12,
    "verifier": verifier,
    "pin": "329c1d7feac5479403c351e64587c867278452cc",
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD12-M4-a",
    "scratch": S,
    "verified_at": "2026-11-05T14:00:00+00:00",
    "verdict": "FAIL" if fail_n or unv_n else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary,
}
out = root / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", pass_n, "fail", fail_n, "verdict", frag["verdict"])
