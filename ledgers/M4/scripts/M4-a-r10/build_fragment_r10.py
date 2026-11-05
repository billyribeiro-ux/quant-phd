# Round 10 slice a fragment builder (rows and evidence written by hand from this round's observations).
import json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1])
S = "ledgers/M4/scripts/M4-a-r10"
CARRY = "Carried from round 9 (course/modules/M/M4/index.html and L03.html byte-identical since the previous pin 1e272e5): "
rows = []
def R(id, check, location, status, evidence):
    rows.append({"id": id, "check": check, "location": location, "status": status, "evidence": evidence})

# Gates, all run this round at pin 47a36d8 (logs under gates/)
R("A-G01", "Gate: check_pages --unit M4", "tools/check_pages.py; course/modules/M/M4/index.html, L01-L04.html", "PASS",
  f"{S}/gates/check_pages.log: 'check_pages M4: PASS'; exit 0 (_exit_codes.log).")
R("A-G02", "Gate: check_dag --unit M4", "tools/check_dag.py; M4 pages", "PASS",
  f"{S}/gates/check_dag.log: 'check_dag M4: PASS'; exit 0.")
R("A-G03", "Gate: check_projects --unit M4", "tools/check_projects.py; course/modules/M/M4/project.html", "PASS",
  f"{S}/gates/check_projects.log: 'check_projects M4: PASS'; exit 0. The project page is not in this slice; its line 42 is cited under A-H11.")
R("A-G04", "Gate: run_labs --unit M4 (13 labs)", "tools/run_labs.py; tests/labs/M4/*.py", "PASS",
  f"{S}/gates/run_labs_M4.log: 'run_labs M4: PASS (13/13)'; exit 0.")
R("A-G05", "Twins L01-L04 alone under python -I -W error; page code equals twin; expected block equals stdout", "tests/labs/M4/lab-M4-L01-1.py..L04-1.py vs course/modules/M/M4/L01..L04.html", "PASS",
  f"Each twin run alone: exit 0, stderr 0 bytes (outputs in {S}/out_L0n.txt). {S}/twin_vs_page.log: page code == twin (trailing newline stripped) True and expected == stdout True for L01, L02, L03, L04.")
R("A-G06", "Gate: page_smoke --unit M4 --pages index L01 L02 L03 L04 (alone)", "tools/page_smoke.py; index.html, L01-L04.html", "PASS",
  f"{S}/gates/page_smoke_slice.log: each page PASS, 'page_smoke M4: PASS'; exit 0.")
R("A-G07", "Gate: ruff check on slice paths", "tests/labs/M4, course/modules/M/M4", "PASS",
  f"{S}/gates/ruff_check.log: 'All checks passed!'; exit 0.")
R("A-G08", "Gate: ruff format --check on slice paths", "tests/labs/M4, course/modules/M/M4", "PASS",
  f"{S}/gates/ruff_format.log: '17 files already formatted'; exit 0.")
R("A-G09", "Gate: mypy --no-incremental (strict)", "repository", "PASS",
  f"{S}/gates/mypy.log: 'Success: no issues found in 385 source files'; exit 0.")
R("A-G10", "Gate: relevant pytest (labs, run_labs, page checks, docs figures, page smoke, curriculum)", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py", "PASS",
  f"{S}/gates/pytest_relevant.log: all dots, no failures; exit 0. The log has no pass count line (quiet mode).")
R("A-G11", "Gate: verify_refs --offline (whole registry) and --unit M4 (live)", "references/references.json", "PASS",
  f"{S}/gates/verify_refs_offline.log: 'offline integrity: 560 entries, 0 problems'; {S}/gates/verify_refs_unit_M4.log: 'live re-verification of M4: 1 of 560 entries, 0 problems'; exit 0.")
R("A-G12", "Round delta: every hunk in the slice and in its shared inputs read (1e272e5a to 47a36d8c)", "course/modules/M/M4/L01.html:270; L02.html:51, :270; L04.html:52, :70, :99; cards.json (M4-c067, M4-c165, c185, c233-c236); project.html; glossary.json; program.json; curriculum/01-foundations.yaml:175; curriculum/curriculum.json:3510, :6405", "PASS",
  "git diff -U0 1e272e5a 47a36d8c read for every slice file. index.html and L03.html are not in the diff (byte-identical). Changed slice hunks are re-verified under their own rows below. Shared-input hunks (glossary/program/curriculum rename of level-slope-curvature) are M3 entries, not M4; A-G13 covers their consistency.")
R("A-G13", "Gate: build_site --check (generated site data current)", "tools/build_site.py; course/assets/data/glossary.json", "PASS",
  f"{S}/gates/build_site_check.log: 'site data current: 6 outputs'; exit 0. Round 9 FAIL (stale glossary entry for level-slope-curvature, M3/L08) is resolved at this pin: glossary.json:1095-1096 now matches the regenerated entry.")
R("A-G14", "Gate: fetch_data --check (market data matches MANIFEST, offline)", "tools/fetch_data.py; course/assets/data/market/", "PASS",
  f"{S}/gates/fetch_data_check.log: 'fetch_data: 3 datasets, 0 problems'; exit 0.")
R("A-G15", "Gate: render_curriculum.py regenerates CURRICULUM.md and curriculum.json with no diff", "tools/render_curriculum.py; CURRICULUM.md; curriculum/curriculum.json", "PASS",
  f"{S}/gates/render_curriculum_diff.log: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json` exit 0; git status shows no tracked-file change in the checkout.")

# Hub index.html (byte-identical since the previous pin; carried rows)
R("A-H01", "Hub structure: header, objectives, prerequisites, placement, lesson map, ladder, data statement", "course/modules/M/M4/index.html:1-189", "PASS",
  CARRY + "round 9 row A-H01 evidence (index.html:1-189 read in full this round).")
R("A-H02", "Hub hours split and lesson hours arithmetic", "index.html:29, :40, :42, :147; L01..L04.html eyebrow and data-hours", "PASS",
  CARRY + "90 lesson hours = 10 x 9 h (data-hours 9 on L01-L04 re-read this round; L05-L10 are other slices); 30 h project; 25% of 120 h; widths 75%/25%.")
R("A-H03", "Hub objectives: 4-8, measurable verbs, each tied to a lesson", "index.html:49-54", "PASS", CARRY + "six objectives, verbs Compute/Derive/State/Decide/Show, each tied to Lessons 1-10.")
R("A-H04", "Hub prerequisites: M2 and M1 only; concept links usable", "index.html:35, :60-64", "PASS",
  CARRY + "curriculum M4 prereqs ['M2'] and M2 prereqs ['M1'] (curriculum.json), so 'through M2, M1' holds.")
R("A-H05", "Hub: M4 uses no M3 concept; matrix results proved from the quadratic form", "index.html:62, :64", "PASS", CARRY + "no M3 link in index.html.")
R("A-H06", "Hub placement: 10 items, 8 on M1/M2, 2 data-skill items, mastery 0.8", "index.html:68-141", "PASS", CARRY + "ten items; data-skill at :132 and :137; data-mastery 0.8 at :68.")
R("A-H07", "Hub citation of M1 Theorem 3.1 (negating a quantifier)", "index.html:79; course/modules/M/M1/L01.html", "PASS", CARRY + "M1 L01 carries the theorem (round 9 read).")
R("A-H08", "Hub numeric claims recomputed from unrounded values", "index.html:75-140", "PASS", CARRY + "re-derived this round: 0.5, 3, 1.875, 5/6, 15/8 for the placement answers; 0.6 = 3/5 for the rung 2 blank; 0.5 for item 3.")
R("A-H09", "Hub scale-rule hypothesis and its citations (L02 Prop 2.3, L06 Prop 2.6, L06 Assumption 1)", "index.html:140; L02.html:115-122; L06.html", "PASS",
  CARRY + "L02 Proposition 2.3 (scale and shift) is still at L02.html:114-116; the round 10 edit at L02.html:51 adds the same cross-reference in the why-it-matters paragraph.")
R("A-H10", "Hub card titles and lesson links match the lesson h1 titles", "index.html:149-158; L01-L04.html h1", "PASS",
  CARRY + "L01-L04 h1 titles re-read this round equal the card titles (L01 'Random Variables, Distributions and Quantiles', L02 'Expectation and Variance', L03 'Skewness and Kurtosis', L04 'Independence and Conditional Expectation (Elementary)').")
R("A-H11", "Hub skip rule agrees with BUILDER_RULES 5.1 and the project page", "course/modules/M/M4/index.html:70, :164; course/modules/M/M4/project.html:42; BUILDER_RULES.md:190-193", "FAIL",
  "Re-verified from scratch. BUILDER_RULES.md:190-193: 'A placement pass means meeting the hub quiz's data-mastery bar and answering every item marked data-skill.' Hub index.html:70 and :164 state the same two-part rule. project.html:42 reads: 'If you met the placement bar on the module page, skip rungs 1 and 2 and start at rung 3.' It omits the data-skill condition. project.html:42 is unchanged in the round 10 delta (the delta hunks are at :61, :109, :206, :215, :228). Fix (project.html, outside this slice): 'If you met the placement bar and answered both skill checks on the module page, skip rungs 1 and 2 ...'.")
R("A-H12", "No lab reads data; no data-files attribute in slice", "index.html:37, :175, :187; tests/labs/M4/lab-M4-L01-1..L04-1.py", "PASS",
  CARRY + "grep of the four twins for open/read/data shows no data file; page code blocks equal the twins (A-G05).")
R("A-H13", "Blitzstein registry record and the hub's description of it", "references/references.json (blitzstein2019introduction); index.html:181-183", "PASS",
  CARRY + "verify_refs --unit M4 live, 1 of 560 entries, 0 problems (A-G11). The registry record's edition field is absent; index.html:183 says so.")
R("A-H14", "Curriculum M4 entry matches the hub (tier, hours, prerequisites, introduces)", "curriculum/curriculum.json (M4 entry); curriculum/01-foundations.yaml:190-", "PASS",
  "Re-verified this round: M4 entry tier F, hours 120, prereqs ['M2'], introduces 19 concepts including random-variable, expectation, variance, independence, skewness, kurtosis, quantile-function, conditional-expectation-elementary (all used on L01-L04). The round 10 curriculum hunks (yaml:175, curriculum.json:3510, :6405) are the M3 level-slope-curvature rename, not M4.")
R("A-H15", "Hub footer and data statement", "index.html:175, :187", "PASS", CARRY + "footer states that seeded samples are SIMULATED and no real data is used.")

# L01 (changed this round at :270; re-verified in full)
R("L01-PROSE", "L01 prose: definitions, caveats, misconceptions, scope words, process words", "course/modules/M/M4/L01.html:51, :55-99, :114-119, :273-300", "PASS",
  "Read L01.html 1-512 in full this round. Definitions 1.1-1.2, 2.1, 3.1 and Example 1.3 match their uses. Section 4 'Where the canon breaks' has four bullets; misconceptions (3) at :288-297 each check against Example 3.6 and Lab 1 (F(Q(1/2))=3/5 not 1/2; Q(3/5)=0; 148/150=74/75=0.987 at :278).")
R("L01-MATH", "L01 mathematics: Prop 2.2, Def 3.1, Prop 3.2, Remark 3.3, Prop 3.4, Examples 3.5-3.6", "course/modules/M/M4/L01.html:80-135", "PASS",
  "Proof of Prop 2.2 (a)-(d), Prop 3.2 (infimum argument), Remark 3.3 (jumps; left-continuity), Prop 3.4 (ceiling index) re-read; the Example 3.6 values F = 1/10, 3/10, 3/5, 4/5, 9/10, 1 and Q(1/2)=0, Q(3/5)=0, Q(61/100)=1 re-derived with Fraction in python (see lab output at out_L01.txt).")
R("L01-PROBLEMS", "L01 problem set: 3 per tier (mechanics, proof, empirical, research), worked solutions correct", "course/modules/M/M4/L01.html:302-405", "PASS",
  "12 problems (mech-1..3, proof-1..3, emp-1..3, res-1..3). Re-derived: M1 F and Q(1/2)=0; M2 F(5)=7/10, Q(7/10)=5, Q(71/100)=7; M3 ceil(36.04)=37; E1 F(2)=9/10 < 99/100; E2 F(0)+eps gives 1; R1 Q^s(3/5)=1 (F(1)=4/5>3/5). All correct.")
R("L01-QUIZ", "L01 retrieval quiz: 9 items, keys correct, explanations accurate", "course/modules/M/M4/L01.html:424-494", "PASS",
  "9 items. Keys re-derived: Q(1/2)=1 for (1/4,1/2,1/4); Q(61/100)=1; Prop 2.2(d) jump; index 198 (pn=198); index 149 (pn=148.5); Q(F_k)=x_k; P(X<=1)=5/6=0.833; X:Omega->R; Q(1)=x_m.")
R("L01-GRADES", "L01 grades: T on proved claims; C/D on labs; no unproved claim graded T", "course/modules/M/M4/L01.html:43-48, :103, :119, :413-418", "PASS",
  "Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4 carry data-grade T and are proved on the page (:86-91, :109, :115, :125). Key-results rows (:413-418) cite proofs or exact computations on the page. The lab (:138-271) carries no theorem grade.")
R("L01-FWD", "L01 forward links and terms: no later lesson used; forward pointers only to same-lesson definitions", "course/modules/M/M4/L01.html:37, :51, :95", "PASS",
  "Only M1/M2 concepts are linked (quantifiers, limit-free). 'quantile' is named in why-it-matters (:51) before Definition 3.1 and points to it ('defined in Definition 3.1 below'). The infimum is defined at :95 before use in Definition 3.1.")
R("L01-LAB", "L01 lab: twin, page code, expected block, hypothesis and interpretation (changed sentence at :270)", "course/modules/M/M4/L01.html:138-271; tests/labs/M4/lab-M4-L01-1.py", "PASS",
  "Round 10 edit at :270 ('the printed value of Q(F(x)+eps) ... is the quantile at one level p just above F(x), which is the next support value; it is one checked level'). Output (out_L01.txt): x=-2 gives Q(F+eps)=-1, x=-1 gives 0, x=0 gives 1, x=1 gives 2, x=2 gives 3, i.e. the next support value; the lab tests the grid of 100 levels and the 5 printed levels, not a limit. Interpretation now matches the output. Twin == page code and expected == stdout (A-G05). Hypothesis at :139-146 matches the output (Q at 1/20, 1/10 is -2; 11/100 is -1; 9/10 is 2; 91/100 is 3).")

# L02 (changed at :51 and :270; re-verified)
R("L02-PROSE", "L02 prose: why-it-matters, scope of §1-§2, definitions", "course/modules/M/M4/L02.html:51, :55-101", "PASS",
  "Read in full. :51 now adds '(Proposition 2.3)' after the scale rule; Proposition 2.3 is at :114-116. Definitions 1.1, 1.6 (continuous case, 'no result of this lesson uses this definition'), 2.1 match the proofs.")
R("L02-MATH", "L02 mathematics: Props 1.2, 1.3, 2.2, 2.3, 2.4; Examples 1.4, 1.5, 2.5, 2.6", "course/modules/M/M4/L02.html:63-142", "PASS",
  "Re-derived: die E=7/2, E[X^2]=91/6, Var=35/12, sd sqrt(35/12)=1.7078 ('about 1.708'); loss E=12500, E[L^2]=3125000000, Var=2968750000, sd sqrt(2968750000)=54486.237 ('about 54486.24'); Var(2X)=35/3=4*35/12; Prop 2.4 proof direction correct.")
R("L02-LAB", "L02 lab: twin, page code, expected block, hypothesis and interpretation", "course/modules/M/M4/L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
  "Twin == page code; expected == stdout (out_L02.txt, 10 lines). Seeded samples labelled SIMULATED. Die sample mean 3.469 for seed 2026, minus 7/2 = -0.031; loss losses 489, total 122250000, mean 12225.0 cents (489*250000/10000). Sample variance uses divisor n, documented in the twin's docstring.")
R("L02-PROBLEMS", "L02 problem set: 3 per tier, worked solutions correct", "course/modules/M/M4/L02.html:298-401", "PASS",
  "12 problems. Re-derived: M1 Var=21/100; M2 E=5000, Var=2.25e8, sd=15000; M3 Var(3X-2)=36, Var(X+10)=4; P2 identity; P3 Var(U+V)=0 vs 2; R2 Var(D)=296875; R3 E=3/10, Q(1/2)=0; E2 expected count 500, 489 is 11 below.")
R("L02-QUIZ", "L02 retrieval quiz: 10 items, keys correct", "course/modules/M/M4/L02.html:421-492", "PASS",
  "10 items: 3.5; Var=5-4=1; Var(2X)=12; Definition 2.1; 5000; 2.25e8; 21/100; c=E[X]; 15000; E[3X-1]=5. All keys re-derived.")
R("L02-CANON", "L02 'where the canon breaks': every stated claim true under the stated hypotheses", "course/modules/M/M4/L02.html:270", "FAIL",
  "Line 270 says: 'For a law with E[X^2] = infinity, the variance is infinite and Proposition 2.2 does not apply.' Definition 2.1 needs the mean mu = E[X] to exist, and Definition 1.6 needs integral |x| f finite. Counterexample: the standard Cauchy law has E[X^2] = infinity and no mean, so under Definition 2.1 its variance is undefined, not 'infinite'. The bullet is also unproved. The round 10 edit to :270 did not touch this sentence (the edit is the first sentence of the bullet). Fix: 'For a law with a finite mean and E[X^2] = infinity, the variance is infinite (since X^2 <= 2(X - mu)^2 + 2 mu^2); a law with no finite mean has no variance under Definition 2.1.'")
R("L02-MISC", "L02 misconceptions: each claim checked", "course/modules/M/M4/L02.html:279-296", "PASS",
  "Four misconceptions. The die E[X^2]=91/6 ~ 15.17 and Var=35/12 ~ 2.92 (:289) check. The +/-1 example gives 1 = 1 (:289). Scaling by a gives a^2 (:285). Seed-2026 mean 3.469 (:293).")
R("L02-FWD-COVARIANCE", "L02 does not claim a general variance-of-sum formula", "course/modules/M/M4/L02.html:347 (P3)", "PASS",
  "P3 states 'This lesson does not derive a general formula for Var(U + V)' and gives the counterexample U = -V (Var(U+V)=0 vs 2).")
R("L02-FOOTER-SCOPE", "L02 references and footer scope statements", "course/modules/M/M4/L02.html:494-507", "PASS",
  "References (:496) cite no registry key beyond the curriculum's Blitzstein name; footer (:507) states seeded samples are SIMULATED and not proofs.")

# L03 (byte-identical since the previous pin; carried, except rows whose cited subject includes cards.json, which were re-verified)
for id_, chk, loc in [
    ("L03-PROSE", "L03 prose: why-it-matters, moment definition inline, Def 2.1-2.2", "course/modules/M/M4/L03.html:51, :55-76"),
    ("L03-MATH", "L03 mathematics: Props 1.1, 2.3, 2.4, 2.5; Example 2.6; Section 3 moment sums", "course/modules/M/M4/L03.html:57-134"),
    ("L03-LAB", "L03 lab: twin, page code, expected block, hypothesis and interpretation", "course/modules/M/M4/L03.html:120-239; tests/labs/M4/lab-M4-L03-1.py"),
    ("L03-NUMBERING", "L03 numbering: each Definition/Proposition/Example number once, in order", "course/modules/M/M4/L03.html:53-110"),
    ("L03-STD-NORMAL-DUP", "L03 does not define the normal density (defined once in L06)", "course/modules/M/M4/L03.html (whole page)"),
    ("L03-CANON", "L03 canon: zero skewness not symmetry; kurtosis not peakedness; finiteness; sample", "course/modules/M/M4/L03.html:241-250"),
    ("L03-MISC", "L03 misconceptions: each claim checked", "course/modules/M/M4/L03.html:252-268"),
    ("L03-PROBLEMS", "L03 problem set: 3 per tier, worked solutions correct", "course/modules/M/M4/L03.html:270-373"),
    ("L03-QUIZ", "L03 retrieval quiz: 9 items, keys correct", "course/modules/M/M4/L03.html:392-462"),
    ("L03-GRADES", "L03 grades: T on proofs and exact computations; C on seeded sample", "course/modules/M/M4/L03.html:42-49, :381-388, :401-407"),
    ("L03-FOOTER-SCOPE", "L03 references and footer scope statements", "course/modules/M/M4/L03.html:464-477"),
]:
    R(id_, chk, loc, "PASS", CARRY + "round 9 PASS row for this id (same locator). The numbers the card and lab outputs depend on were re-checked this round: m_2=163/16, m_3=2157/32, m_4=149461/256, mu=7/4 (recomputed with Fraction), kurtosis 149461/26569 = 5.62539, skewness 2.07300, Bernoulli 73/9 and 64/9, law (-2,1,3) kurtosis 5/3. Lab output out_L03.txt matches.")
R("L03-PROP28-SCOPE", "L03 has no Proposition 2.8 or Assumption 2.7 left in the page, cards or quiz", "course/modules/M/M4/L03.html; cards.json (L03 cards c034-c048, c183, c200, c212-c229); project.html", "PASS",
  "Re-verified this round (cards.json changed in the delta, though no L03 card changed): grep of L03.html and the 28 L03 cards finds no 'Proposition 2.8' or 'Assumption 2.7'.")

# L04 (changed at :52, :70, :99; re-verified)
R("L04-PROSE", "L04 prose: why-it-matters, joint table, independence definitions", "course/modules/M/M4/L04.html:52-70, :137-145", "PASS",
  "Read in full. :52 now says 'developed in Lesson 5' (correlation and covariance matrix are the L05 concepts per curriculum); :70 says 'verdict for each table' (Part A two tables, Part B one table: three verdicts, matching the output). Definitions 1.1, 1.2, 2.1 and Remark 2.2 match the proofs.")
R("L04-TERM-ORDER", "L04 terms used after definition", "course/modules/M/M4/L04.html:52 vs :59, :65, :98, :131", "PASS",
  "Joint table (Def 1.1), independence (Def 1.2), covariance (Def 1.6), conditional expectation (Def 2.1) each used after definition or only forward-pointed in prose.")
R("L04-REMARK-1-3", "L04 Remark 1.3 claim: 'Lab 1 applies the test to every cell of three tables (Parts A and B) and prints the verdict for each table'", "course/modules/M/M4/L04.html:70; tests/labs/M4/lab-M4-L04-1.py:is_independent", "PASS",
  "The twin's is_independent (line 45-48) checks all(p == px[x]*py[y] for every cell). Part A prints a verdict for product and dependent tables (lines 73-76); Part B prints independent False (line 89). Three verdicts, every cell tested. Output out_L04.txt matches.")
R("L04-MATH", "L04 mathematics: Props 1.4, 1.5, 1.7, 1.8, 2.3, 2.4; Examples 1.9, 2.5", "course/modules/M/M4/L04.html:73-169", "PASS",
  "Re-derived: Example 1.9 (E[X]=0, E[Y]=2/3, E[XY]=0, Cov=0, p(0,0)=1/3 vs 1/9); Example 2.5 (marginals 2/5, 3/5; E[X]=4/5; E[X|Y=0]=1; E[X|Y=1]=2/3; total expectation 4/5). Prop 1.4 proof, 1.5 factorisation, 1.7 expansion, 2.3 regrouping and 2.4 all correct.")
R("L04-PROBLEMS", "L04 problem set: M1-M3, P1-P3, E1-E3, R1-R3 correct", "course/modules/M/M4/L04.html:331-434", "PASS",
  "12 problems. Re-derived: M1 marginals 0.3/0.7/0.4/0.6, cell 0.12 vs 0.1; M2 E[X|Y=1]=2/3; M3 cells 1/8,1/8,3/8,3/8; P3 Cov=-ab; E2 ratio 3; E3 ratio 5/8; R1 Cov=0; R3 conditional expectations 0.")
R("L04-QUIZ", "L04 retrieval quiz: 10 items, keys correct", "course/modules/M/M4/L04.html:453-527", "PASS",
  "10 items. Keys re-derived: L04q1 No; q2 E[X|Y=0]=1; q4 E[X]=0.8; q6 Cov=0; q8 P(Y=1)=0.6; q10 product-table cell (0,0) = (1/5)(3/10)=3/50=0.06 (PX and PY in the twin, lines 30-31).")
R("L04-CANON-MISC", "L04 'where the canon breaks' and misconceptions", "course/modules/M/M4/L04.html:303-329", "PASS",
  "Canon 2: p(0,0)=1/2 vs 1/4 correct. Canon 3: X=Y=+/-1 gives E[XY]=1 vs 0 correct. Misconception 2 (disjoint events) correct; misconception 3 values 1, 2/3, 4/5 correct.")
R("L04-FOOTER", "L04 footer and references", "course/modules/M/M4/L04.html:530-543", "PASS",
  "References: no outside source cited, every result derived on the page; footer says each exact result is proved or an exact computation on a stated table.")
R("L04-FWD", "L04 forward references", "course/modules/M/M4/L04.html:52, :99, :539", "PASS",
  "Correlation and the covariance matrix are named as Lesson 5 content in prose (:52, :99). Correlation is not used as a result anywhere in L04 (no formula, no link), so this is a pointer, not a use. Next link is L05.html.")
R("L04-LAB", "L04 lab: twin, page code, expected block, hypothesis and interpretation", "course/modules/M/M4/L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
  "Twin == page code; expected == stdout (out_L04.txt, 18 lines). Interpretation at :300 matches: product table cell 3/50 both sides; dependent table 1/10 vs 4/25; Part B covariance 0, cell 1/3 vs 1/9; Part C 1, 2/3, 4/5 and equals_E[X] True.")

# Cards (cards.json changed: M4-c067 (L05), c165/c185/c233-c236 (L09), outside this slice; all 92 L01-L04 cards re-read)
R("CARDS-DUP", "Full scan: no duplicate fronts or ids in cards.json (230 cards)", "course/modules/M/M4/cards.json", "PASS",
  f"{S}/dump: python check of cards.json this round: 230 cards, 0 duplicate fronts, 0 duplicate ids; grades 205 T and 25 C.")
R("CARDS-L01", "L01 cards (23): atomic, correct against the current lesson text (all read)", "course/modules/M/M4/cards.json (M4-c001..c016, c173, c192..c195, c197, c198)", "PASS",
  "All 23 read and checked against L01.html. c011 (198), c012 (Q(1/2)=0), c014 (Q(3/5)=0), c015 (149), c016 (grid check) match the page. Only card-to-page difference: cards cite 'Hypotheses: ...' on the Prop 3.2 family, which the page states.")
R("CARDS-L02", "L02 cards (22): atomic, correct against the current lesson text (all read)", "course/modules/M/M4/cards.json (M4-c017..c033, c181, c182, c199, c243, c244)", "PASS",
  "All 22 read. c030 (3.469) and c033 (489) are grade C and match Lab 1 output. c031 and c182 (2968750000; 54486.24) and c181 (sqrt(35/12) ~ 1.708) match Example 2.5-2.6. c021 says 'never negative' (Definition 2.1). No card cites the L02 :270 claim.")
R("CARDS-L03", "L03 cards (28): atomic, correct against the current lesson text (all read)", "course/modules/M/M4/cards.json (M4-c034..c048, c183, c200, c212, c214, c215, c222..c229)", "PASS",
  "All 28 read. Numbers re-derived: c200 m3=2157/32 (67.40625); c228 m4=149461/256 (583.83203); c043 kurtosis 5/3 (m2=3, m4=15); c045 73/9 and 7/3; c048 64/9; c047 and c183 (2.065, 5.580 vs exact 2.073 and 5.625) match the Lab 1 printed sample lines. c183 writes 'exact kurtosis 5.625' for 149461/26569 = 5.62539: the 3-decimal display; the page (L03.html:330) states the three-decimal rule. Accepted.")
R("CARDS-L04", "L04 cards (19): atomic, correct against the current lesson text (all read)", "course/modules/M/M4/cards.json (M4-c049..c065, c201, c204)", "PASS",
  "All 19 read. c062 (1), c064 (-ab), c065 (2/3 vs 4/5), c063 (marginals example) match the page. M4-c066 is absent (removed in round 9); no card references it.")
R("CARDS-NUMBERS", "Every numeric token in the L01-L04 card backs appears on its lesson page (fractions as \\tfrac in HTML)", "course/modules/M/M4/cards.json (92 cards) vs L01-L04.html", "PASS",
  f"{S}/card_refs_r10.log: 92 cards checked. Flags: c043 '5/3' and c044 '2/5' appear as \\tfrac{{5}}{{3}} and \\tfrac25 on L03.html (:436, :245); 'Problem P3' in c064 is the page's own label for the item (L04.html:378 'P3 · ...' within the Problem set). No missing numbers.")
R("CARD-M4-c219", "No card M4-c219 (carried check; the id is absent)", "course/modules/M/M4/cards.json", "PASS", "Checked this round: 'M4-c219' not among the 230 ids.")

# Notation and scope/process/data/structure
R("NOTATION-A", "Notation: no symbol in the slice contradicts notation/notation.json", "notation/notation.json (8 symbols, 4 macros); index.html, L01..L04.html", "PASS",
  "grep this round: the slice uses \\R (registry macro \\mathbb{R}, real numbers) only; it does not use T, Phi, R^*, R_f, \\mathbb{Q} (the registry's AP1 Q is a measure; M4's plain Q is the quantile function, not that symbol). Observation, not a FAIL: plain Q and the letter p are used for the quantile function and quantile level, and also for weights p(omega) (L01) and joint probabilities p(x,y) (L04); none of these is a registry symbol.")
R("NOTATION-REG", "gamma_3 and gamma_4 in L03 match the registry meaning (not excess kurtosis)", "course/modules/M/M4/L03.html:76-86; notation/notation.json (M4 gamma_3, gamma_4)", "PASS",
  "Registry: gamma_3 = E[(r-mu)^3]/sigma^3; gamma_4 = E[(r-mu)^4]/sigma^4, not excess. L03 defines gamma_4 = E[Z^4] with 'no subtraction of 3' (card c224); Bernoulli gamma_4 = (1-3pq)/(pq) (L03 Example 2.6). Consistent.")
R("NOTATION-MACRO", "Macros used in the slice are defined (page_smoke renders KaTeX in strict mode)", "index.html, L01..L04.html", "PASS",
  f"{S}/gates/page_smoke_slice.log: no unrendered math, no katex-error on index, L01-L04, light and dark, 360 px and desktop.")
R("PROCESS-A", "No process words in learner text (builder, verifier, round, TODO, ledger, fragment, checkout, pin, slice, ruling)", "index.html, L01..L04.html (visible text), cards.json (slice cards)", "PASS",
  f"{S}/struct_r10.log: zero hits in visible text of index, L01, L02, L03, L04; zero hits in any of the 230 cards.")
R("SCOPE-A", "Scope words backed by a computation or limited to quoted wrong claims", "index.html:37, :175; L01.html:270, :288; L02.html:270, :347; L04.html:300, :306", "PASS",
  "Words checked: 'every' (every cell, every variance computed here), 'only' (Proposition 1.8 forward only; interpretation at L04:300), 'all' (L01:270 'not a limit taken over all p' is scoped). The one scope claim that is wrong is recorded as its own FAIL (L02-CANON).")
R("DATA-A", "No real data; SIMULATED labels on seeded samples", "index.html:37, :175, :187; L02.html:146, :262, :507; L03.html (lab hypothesis)", "PASS",
  "Every seeded sample on L02 and L03 is labelled SIMULATED at its hypothesis or footer. No twin reads a file. Index states 'No real data is used in M4'.")
R("STRUCT-A", "Lesson structure: why-it-matters <= 120 words; misconceptions >= 3; 3 problems per tier; quiz items", "course/modules/M/M4/L01..L04.html", "PASS",
  f"{S}/struct_r10.log: why-it-matters words L01 118, L02 105, L03 97, L04 103 (all <= 120). Misconceptions 3, 4, 3, 3 (>= 3). Problems 12 each (3 per tier). Quiz items 9, 10, 9, 10. Eyebrow '9 study hours' on each.")
R("NUM-A", "Every displayed number in the slice recomputed from unrounded values", "index.html; L01..L04.html", "PASS",
  "L01 (1/10, 3/10, 3/5, 4/5, 9/10, 74/75 = 0.987, 5/6 = 0.833, 0.99 * 150 = 148.5, 40*0.901 = 36.04); L02 (1.708, 54486.24, 3.469, 0.031, 489, 122250000, 12225.0, 15.17, 2.92); L04 (3/50, 1/10 vs 4/25, 5/8 = 0.625, 2/3, 4/5, 0.8, 0.6) re-derived with Fraction/python. L03 numbers re-checked this round through the card and lab lines (CARDS-L03).")
R("GRADE-A", "Grade attributes match BLUEPRINT evidence grades (T theorems; C labs; no A/B/D claims without evidence)", "index.html; L01..L04.html; cards.json (slice)", "PASS",
  "Every block-title claim with data-grade T is a proposition or remark with a proof on the page. Lab-based claims in the slice cards are C (c030, c033, c047, c183). No A, B or D claim in the slice.")
R("ASSUMP-A", "Unproved statements are named Assumptions or hypotheses", "index.html:138-140; L01..L04.html", "PASS",
  "Index Q (rung 2) names the Student-t scale rule as a hypothesis, not proved on the page; L02 Prop 2.2 hypotheses (finite, positive weights) and the Def 1.6 integral condition are stated.")
R("DAG-A", "Standard normal and Gaussian are not used in L03 before L06 defines them", "course/modules/M/M4/L03.html (whole page)", "PASS",
  CARRY + "round 9 evidence; re-checked this round by grep of L03.html for 'normal' (no definition of the normal density).")
R("DAG-HUB-PREVIEW", "Hub preview of later lessons is not a lesson-node link", "index.html:138-140, :147-160", "PASS",
  CARRY + "check_dag M4 PASS (A-G02).")
R("DAG-L02-L04-USES", "Lessons L01-L04 use only earlier definitions (L01, L02 for L04) and M1/M2 concepts", "course/modules/M/M4/L01.html..L04.html", "PASS",
  "Re-verified this round for L01, L02 and L04 (changed pages). L02 uses L01 (random variable, distribution) and M2 limit/definite integral. L04 uses L01 (random variable) and L02 (expectation, E[X^2]-(EX)^2 at L04:421). Forward mention of Lesson 5 correlation at L04:52/:99 is a pointer (see L04-FWD).")
R("DAG-SD-TWICE", "Each term defined once: standard deviation is defined in L02 and again in L05 (BUILDER_RULES.md:71-72, rule 10 'No concept defined twice')", "course/modules/M/M4/L02.html:100-101 (Definition 2.1); course/modules/M/M4/L05.html:79-80 (Definition 1.3)", "FAIL",
  "Re-verified this round. L02.html:100-101 'Definition 2.1 (variance and standard deviation)' defines sigma = sqrt(Var(X)). L05.html:79-80 'Definition 1.3 (standard deviation)': 'The standard deviation of X is sigma_X = sqrt(Var(X)), the nonnegative square root of the variance.' Still present at pin 47a36d8 (L05.html is not in the delta). L05 is a cross-slice file; the FAIL is recorded here as in round 9. Fix (L05, other slice): delete Definition 1.3 and cite L02 Definition 2.1 (the round 10 cards.json edit at M4-c067 already does this for the card back).")

fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "M4", "slice": "a", "round": 10,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD10-M4-a)",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "1e272e5a641f18412703b37778a44db6f7391a69",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-M4-a",
    "scratch": "ledgers/M4/scripts/M4-a-r10/",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "blitzstein2019introduction: the registry record carries no edition field; the '2nd ed. (2019)' string comes from the curriculum and the registry source string and is not checked against the book (index.html:183 says so). Unchanged from round 9; verify_refs --unit M4 live, 1 of 560, 0 problems."
    ],
    "freshness_flags": [],
    "notes": (
        "Round 10 at pin 47a36d8 (base 1e272e5, the round 9 pin). Delta for the slice: L01.html:270 (interpretation), L02.html:51 (Proposition 2.3 cross-reference) and :270 (canon bullet), L04.html:52, :70, :99 (wording: 'Lesson 5', 'each table'), cards.json (M4-c067 back in L05; L09 grades c165/c185/c233-c236 in L09; neither in this slice, both read). index.html and L03.html are byte-identical since 1e272e5 and are carried from round 9 (CARRY prefix). Round 9 FAILs: A-G13 (glossary) is PASS now (build_site --check exit 0); A-H11 (project.html:42) and DAG-SD-TWICE (L05.html:79-80) are still FAIL at this pin; L02-CANON-VAR is a new FAIL found in the re-read of L02.html:270. Gates were run at this pin (gates/ logs, _exit_codes.log). Mutation testing does not apply (lessons, hub and lab twins). Tracked files unchanged by the gates (git diff exit 0). Cross-slice items for other owners: project.html:42 (A-H11), L05.html:79-80 (DAG-SD-TWICE), L05 Definition 1.3 vs the cards.json M4-c067 edit (done), L09 card grades (not checked by this slice)."
    ),
    "summary": (
        f"Slice a round 10 at 47a36d8: {len(rows)} rows; {len(rows)-len(fails)} PASS, {len(fails)} FAIL, 0 UNVERIFIABLE. "
        "FAIL rows: A-H11 (project.html:42 omits the data-skill condition of BUILDER_RULES.md:190-193), DAG-SD-TWICE (L05.html:79-80 redefines the standard deviation of L02 Definition 2.1), L02-CANON (L02.html:270 says the variance is infinite whenever E[X^2] is infinite; the Cauchy law has no mean, so its variance is undefined under Definition 2.1). Round 9 A-G13 is PASS now. Labs: all four twins and their page blocks are identical and the expected blocks equal the output."
    ),
}
out = ROOT / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fails", [r["id"] for r in fails])
