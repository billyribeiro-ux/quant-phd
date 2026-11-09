"""Writes the round-5 fragment for M5-b (delta verification, pin dde0486b). Rows keep every round-4 id."""
import json

CK = "/Users/billyribeiro/.fanout/wt/verifyS5-M5-b"
S = "ledgers/M5/scripts/M5-b-r5/out/"
PFX = ("Carried from round 4 (L05.html, L06.html, L07.html and the three slice twins are byte-identical at the cited "
       "lines; the only changed lines in these files since edbb7aa8 are L05.html:134, L06.html:289, L07.html:67, "
       "L07.html:528 and tests/labs/M5/lab-M5-L05-1.py:48, per git diff --unified=0): ")
CPFX = ("Carried from round 4 (card objects byte-identical since edbb7aa8; cards.json changed objects are c055, c064, "
        "c067, c084, c105, c135, c173, c175, c222, c223, c229, c242, c243): ")

R = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

# ---- gates, all re-run on dde0486b (ledgers/M5/scripts/M5-b-r5/gates.sh; out/_rc.txt all rc=0)
row("gate-check-pages", "2.9 structure (check_pages --unit M5, and per page L05/L06/L07)",
    "course/modules/M/M5/L05.html, L06.html, L07.html, cards.json", "PASS",
    "Re-run on dde0486b: 'check_pages M5: PASS' (out/check_pages_M5.out); per page rc=0 (check_pages_L05/L06/L07.out).")
row("gate-check-dag", "2.9 DAG (check_dag --unit M5)", "course/modules/M/M5/L05.html, L06.html, L07.html", "PASS",
    "Re-run: 'check_dag M5: PASS' (out/check_dag_M5.out). The new L07 Definition 1.2 cites L04 Definition 3.2 in plain text, with no concept link, so no new DAG edge is created.")
row("gate-check-projects", "2.9 unit gate (check_projects --unit M5)", "unit M5 (project outside this slice)", "PASS",
    "Re-run: 'check_projects M5: PASS' (out/check_projects_M5.out). Project not verified in this slice.")
row("gate-run-labs", "2.5 labs (run_labs --unit M5 --page L05/L06/L07)", "course/modules/M/M5 (labs of L05, L06, L07)", "PASS",
    "Re-run: 'run_labs M5: PASS (1/1)' for each page (out/run_labs_L05.out, run_labs_L06.out, run_labs_L07.out).")
row("lab-L05-twin", "2.5 labs (twin alone under python -I -W error; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L05-1.py:45-49 (docstring changed this round); course/modules/M/M5/L05.html:84-173", "PASS",
    "out/twin_check.out: 'L05 ... rc=0 stderr_len=0 page_code==twin(rstrip)=True expected==stdout=True'. The docstring line (twin line 48, page L05.html:134) changed in dde0486b and the page copy still equals the twin.")
row("lab-L06-twin", "2.5 labs (twin alone; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L06-1.py; course/modules/M/M5/L06.html section#lab-M5-L06-1", "PASS",
    "out/twin_check.out: 'L06 ... rc=0 stderr_len=0 page_code==twin(rstrip)=True expected==stdout=True'. Twin unchanged since edbb7aa8.")
row("lab-L07-twin", "2.5 labs (twin alone; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L07-1.py; course/modules/M/M5/L07.html section#lab-M5-L07-1", "PASS",
    "out/twin_check.out: 'L07 ... rc=0 stderr_len=0 page_code==twin(rstrip)=True expected==stdout=True'. Twin unchanged since edbb7aa8.")
row("gate-page-smoke", "2.9 page_smoke (console errors, math rendered, 360 px, no external requests; labs in Pyodide)",
    "course/modules/M/M5/L05.html, L06.html, L07.html", "PASS",
    "Re-run per page (--pages L05 / L06 / L07): 'page_smoke M5: PASS' (out/page_smoke_L05.out, _L06, _L07); each lab ran (0.0-0.1 s).")
row("gate-ruff-mypy-twins", "2.5 lint and types (twins); mypy strict over the repository",
    "tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py", "PASS",
    "out/ruff_check_twins.out 'All checks passed!'; out/ruff_format_twins.out '3 files already formatted'; out/mypy_full.out 'Success: no issues found in 385 source files' (mypy --no-incremental).")
row("gate-pytest-labs-M5", "2.5 labs (CI test)", "tests/test_labs.py -k M5", "PASS",
    "out/pytest_labs_M5.out: 13 dots, rc=0; out/pytest_collect_M5.out: 'tests/test_labs.py: 13' (13 M5 labs collected).")
row("gate-verify-refs-offline", "2.1 citations (offline integrity)", "references/references.json; slice pages", "PASS",
    "out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Slice pages cite no registry key (no data-cite).")
row("pages-raw-angle-brackets", "2.9 structure (HTML validity; raw '<' in math and prose)",
    "L05.html lines 60, 65, 75, 76, 81, 86, 186, 188, 200, 210, 220, 233, 256, 264, 281, 283, 290, 291, 297, 299, 300, 383 (29 occurrences); L06.html lines 258, 308, 330, 331, 332 (8 occurrences); L07.html lines 52, 165, 195 (3 occurrences)",
    "FAIL",
    "Round-4 row said no raw '<' followed by a letter or digit exists outside tags; that is wrong for digits and backslashes. Script ledgers/M5/scripts/M5-b-r5/out (run inline; regex <(?=[0-9\\\\]) over each page) finds 40 raw '<' in text nodes, e.g. L05.html:60 '<\\varepsilon', L05.html:81 '<1', L06.html:330 '<1', L07.html:52 '<1'. HTML5 parses these as text (no tag opens on '<' followed by a non-letter), and page_smoke renders the math, so there is no visible defect. The builder's own convention is visible elsewhere (L05.html:215 '0&lt;a&lt;1', L06.html:56 'n_{1}&lt;n_{2}'), so the escaping is applied inconsistently. LOW, presentation/markup hygiene; not a ruling-26 blocking kind.",
    "Replace every raw '<' in math or prose on L05, L06 and L07 with '&lt;' (40 occurrences at the lines listed in location). Then re-run check_pages --unit M5 and page_smoke for L05, L06 and L07.")
row("pages-banned-strings", "2.9 banned strings and process words", "L05.html, L06.html, L07.html, cards.json (slice cards)", "PASS",
    "grep -i over the three pages and the 66 slice cards for todo, tbd, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, verifier, builder, fixer, ledger, plan, architect: no hits in the slice. Hits only at cards.json line 425 ('the plane is complete', L04) and line 892 ('best plan', L08), both outside the slice.")
row("notation-registry", "2.4 notation (every symbol vs notation/notation.json; no reuse of a registered symbol)",
    "L05.html, L06.html, L07.html", "PASS",
    "Counts re-run: \\mathbb 0, \\Phi 0, \\gamma 0, \\Prob 0, \\E 0, R^{\\ast} and R^{e\\ast} 0, R_f 0, bare Q 0 on all three pages. \\R 16/12/25 and \\N 0/9/0 (L05/L06/L07). Local symbols are defined where used; \\mathbf{1} in L05 Research 2 is the KaTeX built-in (no reuse of the registered \\indic meaning).")
row("hours-split", "2.9 hours arithmetic", "L05.html, L06.html line 2 data-hours=10; L07.html line 2 data-hours=11; L10.html data-hours=11; index.html data-hours-lessons=104; project.html data-hours-project=26; curriculum/01-foundations.yaml:231-235 hours 130", "PASS",
    "grep re-run: L01-L06 data-hours=10 (six pages), L07-L10 =11 (four pages): 6*10+4*11 = 104 = index data-hours-lessons; 104+26 = 130 = curriculum M5 hours (curriculum/01-foundations.yaml:235 'hours: 130').")
row("problems-tiers", "2.9 problem set (four tiers, worked solutions)",
    "L05.html #problems; L06.html #problems; L07.html #problems", "PASS",
    "Re-counted this round: details class=solution count 12 on each of the three pages (one solution per problem); twelve problems, three per tier (as round 4). Problem sections are outside every changed line.")
row("structure-order", "2.9 structure (section order, BUILDER_RULES 4.2)", "L05.html, L06.html, L07.html", "PASS",
    "Re-counted this round: misconception items 3 per page; data-grade claims 20/22/20 (L05/L06/L07); details.solution 12 per page. Section order carried from round 4 (no changed line moves a section).")
row("forward-reference-L07-roadmap", "2.9 forward reference (BUILDER_RULES 4.1: no link to a later lesson)",
    "course/modules/M/M5/L07.html:52 (why-it-matters)", "PASS",
    "L07.html:52 re-read: 'Lesson 8 applies Theorem 2.1 to the operator of its Definition 1.1.' Plain text; zero '<a ' tags on that line, so no link to a later lesson.")
row("open-items-status", "2.9 open items for slice b (Builder F defects 1, 2, 6 as listed in round 4)",
    "L05.html, L06.html, L07.html; tests/labs/M5/lab-M5-L05-1.py", "FAIL",
    "Defect 2 (ratio wording): PASS, L07.html:327 and L07.html:493 both read 'tends to one/1 for pairs of fixed separation far from the origin'. Defect 6 (L05 twin docstring): PASS as a sentence (twin line 48 now lists 'an exact fraction, an integer, a boolean, or a float with ten decimals', which matches stdout in out/twin_check.out). Defect 1 (raw '<'): FAIL (residue). The named escapes (L05.html:215, L06.html:56) are present, but 40 raw '<' remain (row pages-raw-angle-brackets). The Builder F open-items file is not in the pinned checkout; defects were checked as recorded in the round-4 fragment.",
    "Finish the defect-1 escaping (see pages-raw-angle-brackets), then re-run check_pages and page_smoke for L05-L07.")

# ---- lab claims (carried: prose lines and twin unchanged; docstring part handled by lab-docstring-types-L05)
row("lab-claims-L05", "2.5 labs: sentences about what the lab prints, checks, contains (hypothesis, interpretation)",
    "L05.html:86 (hypothesis), :174 (interpretation); twin lab-M5-L05-1.py", "PASS",
    PFX + "L05.html:86 and :174 re-read this round. Hypothesis: sup distance 1 for every printed order on k/100 (out/twin_check.out L05 stdout, 'sup_distance 1' for orders 1,2,5,10,50); least order 10 with 1/1024 < 1/1000 (stdout 'least_order_with_half_power_below_1_over_1000 10'); x^n at 0.99 decays (0.9043820750, 0.3660323413, 0.0000431712). Interpretation: the grid contains 1, so the printed sup is exact (twin docstring, verified). The program does not compute distance to f (Part C prints the pointwise limit as text only). The docstring type sentence is row lab-docstring-types-L05.")
row("lab-claims-L06", "2.5 labs: sentences about what the lab prints, checks, contains",
    "L06.html:101 (hypothesis), :222 (interpretation); twin lab-M5-L06-1.py", "PASS",
    PFX + "L06.html:222 re-read this round: 'x(1-x)=1/4-(x-1/2)^2 <= 1/4' (algebra checked), 12/49 at 3/7 below 1/4 (rederive.out), e_i of the lab is e_{i+1} of Example 3.3 (checked against Example 3.3 indexing). Lab output (out/twin_check.out L06): 'grid_sevenths argmax 3/7 maximum 12/49', 'pairs 45 min_distance 1 max_distance 1'.")
row("lab-claims-L07", "2.5 labs: sentences about what the lab prints, checks, contains",
    "L07.html:200 (hypothesis), :310 (interpretation); twin lab-M5-L07-1.py", "PASS",
    PFX + "Output lines (out/twin_check.out L07) match L07.html:310 and the hypothesis: 'part C: window [-50, 50]: largest sampled ratio = 0.999798'; 'f(x) - x is positive at every grid point on either window'; 'the error is at most the a priori bound for n = 0 to 30'. Grid of 201 points (rederive.out: adjacent-pair and all-pair maxima agree).")

# ---- numbers (re-derived this round: ledgers/M5/scripts/M5-b-r5/rederive.py, out/rederive.out)
row("num-L05-lab1", "2.6 numbers in prose vs printed/unrounded values (Lab 1 expected block)",
    "L05.html:156-173 (expected block); :174 interpretation", "PASS",
    "out/rederive.out: 2^50 = 1125899906842624; 0.99^10 = 0.9043820750, 0.99^100 = 0.3660323413, 0.99^1000 = 0.0000431712 (10 decimals); least n with (1/2)^n < 1/1000 is 10 ((1/2)^9 = 1/512, (1/2)^10 = 1/1024). Expected block equals stdout (twin_check.out).")
row("num-L05-prose", "2.6 numbers in prose (Empirical 2 and 3; quiz numeric items; Example 1.4 and Proposition 2.5 numbers)",
    "L05.html:290-293; :334-340; :360-362; :280-283", "PASS",
    "out/rederive.out: ln 0.99 = -0.01005034; 100 ln 0.99 = -1.005034; exp = 0.36603 (0.3660323); (1/2)^9 = 1/512 > 1/1000 and (1/2)^10 = 1/1024 < 1/1000; (1/2)^3 = 1/8 = 0.125.")
row("num-L06-lab1", "2.6 numbers in prose (Lab 1 expected block; Empirical items; quiz)",
    "L06.html:205-221 (expected block); :321-330; :415-416", "PASS",
    "out/rederive.out: 1/4 - 12/49 = 1/196 = 0.0051020408 (prose 'about 0.0051'); C(10,2) = 45; width after step 8 = 1/256 = 0.00390625; sevenths maximum 12/49 first attained at 3/7; tenths maximum 1/4 at 1/2.")
row("num-L07-lab-A", "2.6 numbers in prose (Lab 1 Part A expected block)",
    "L07.html:296-304 (Part A block); :310 interpretation; quiz L07.html:510-512", "PASS",
    "out/rederive.out: sin 1 = 0.8414709848; error and bound for n = 0, 1, 2, 5, 10, 20, 30 match the expected block to printed digits (n=5: bound/err = 48.92447); all 31 rows satisfy error <= bound; cos 1 = 0.540302.")
row("num-L07-lab-B", "2.6 numbers in prose (Lab 1 Part B; E3 and its unrounded difference)",
    "L07.html:305 (block); :310; :411-414 (E3)", "PASS",
    "out/rederive.out: largest quotient over all 201-grid pairs = 0.840116725732564 (adjacent pairs give the same); sin 1 - (cos 0.995 - cos 1)/0.005 = 0.0013542591 (E3).")
row("num-L07-lab-C", "2.6 numbers in prose (Lab 1 Part C block)",
    "L07.html:307-309 (block); :310; card M5-c203", "PASS",
    "out/rederive.out: W=5 max ratio 0.980390 (all pairs and adjacent), min f(x)-x 0.099020 = sqrt26 - 5; W=50 max 0.999798, min 0.009999 = sqrt2501 - 50; f'(5) = 0.9805807 and f'(50) = 0.9998001 bound the printed maxima.")
row("num-L07-prose", "2.6 numbers in prose (Examples, Problems, quiz)",
    "L07.html:340-345 (M2), :350 (M3), :391-395 (E1), :398-404 (E2), :406-409 (E3), :424-427 (R2), :473-507 (quiz)", "PASS",
    "out/rederive.out: M2 bound 3/3^13 = 1.8817e-6 and 3/3^14 = 6.2723e-7, smallest n 14; R2 threshold 90.7126, beta^90/(1-beta) = 1.13e-6 > 1e-6, beta^91/(1-beta) = 9.52e-7 <= 1e-6, so n = 91; E1 ratio 48.92447 (prose 48.92); Ex 2.3 bound equals error at every n (checked to 1e-15).")
row("num-L07-misc3", "2.6 numbers in prose (Misconception 3)", "L07.html:335", "PASS",
    "out/rederive.out: 2.661258 / 0.05439523 = 48.92447; prose 'about 48.9 times' is consistent with the unrounded ratio.")

# ---- mathematics (carried unless noted)
row("math-L05-props", "2.2 mathematics (Props 1.3, 2.1, 2.4, 2.5, Ex 2.3, Ex 1.4)", "L05.html:65-76, :179-221; Proof 2.5 :218-220; Ex 2.3 :199-201", "PASS",
    PFX + "Re-read this round: Ex 1.4 (l.81), Ex 2.3 proof (l.200: |x^n-y^n| <= n|x-y| from the geometric sum, verified), Prop 2.4 (l.205), Prop 2.5 (l.214-221). Hypotheses listed for every T item.")
row("math-L05-props-2", "2.2 mathematics (Props 3.1, 3.2; Remark 3.3; canon-breaks; misconceptions)", "L05.html:223-267", "PASS",
    PFX + "Prop 3.1 and 3.2 proofs and canon item 3 unchanged; checked on the page this round (Prop 3.2 hypothesis (1) metric space implies nonempty by L04 Definition 1.1).")
row("math-L06-props", "2.2 mathematics (Lemma 1.2, Props 1.3, 1.4, Ex 1.5, Prop 2.1, Cor 2.2, Prop 3.1, Cor 3.2, Prop 3.4)",
    "L06.html:56-96, :226-268, :276-282, :285-299", "PASS",
    "Re-verified this round for the changed line L06.html:289 (Prop 3.4 proof at l.278-283: the closed unit ball contains e_n with no convergent subsequence, bounded by 2 via the triangle inequality; canon sentence now matches). Prop 1.3 proof (l.80-81): the choice n_k > n_{k-1} with x_{n_k} in I_k is justified by infinitely many indices. Remaining cited lines byte-identical since edbb7aa8.")
row("math-L07-core", "2.2 mathematics (Defs 1.1-1.2, Props 1.4, 1.5, Thm 2.1, Lemma 2.2, Ex 2.3, Prop 2.4, Prop 3.1, Cor 3.2, Ex 3.3)",
    "L07.html:56-197", "PASS",
    "Re-read this round in full (plain text of l.52-197): Def 1.2 (l.67, new cross-reference to L04 Definition 3.2, same definition as L04 l.265-266); Prop 1.4 proof (l.83: beta d <= d < eps); Prop 1.5 (l.87-94); Thm 2.1 Step 1 (l.132: beta^N c/(1-beta) < eps and monotonicity in n), Steps 3-5 (l.134-136); Lemma 2.2 (l.117-128); Ex 2.3 (l.141); Prop 2.4 statement and proof reference (l.145-151); Prop 3.1 and Cor 3.2 (l.170-190); Ex 3.3 uses Assumption 2(a),(b),(c),(d) (l.156-166, verified text). No gap found.")
row("math-L07-canon", "2.2 mathematics (canon-breaks items 1-3; misconceptions 1-3)", "L07.html:316-337", "PASS",
    PFX + "Item 1: phi x = x/2 on (0,1] has only candidate 0 not in X. Item 2 (l.327): ratio tends to 1 for x = y+h, y to infinity; sqrt(x^2+1) > x, so no fixed point. Misconceptions unchanged.")
row("math-L07-assumptions", "2.2 named assumptions (Assumption 1, 2; uses)", "L07.html:156-170 (Assumptions 1, 2); uses at :172, :177, :182, :195", "PASS",
    PFX + "Assumption 2 (l.165) read in full: (a) sin strictly increasing on [0,1], sin 0 = 0; (b) 0 < cos t <= 1 on [0,1]; (c) derivatives; (d) sin 1 < 1. Every result that uses them names them (Prop 3.1, Cor 3.2 'Assuming Assumption 1'; Ex 3.3 'Assuming Assumptions 1 and 2').")
row("math-L07-problems", "2.2 problems (M1-M3, P1-P3, E1-E3, R1-R3)", "L07.html:346-440 (problem set)", "PASS",
    PFX + "Solutions unchanged; values re-derived this round (out/rederive.out): M2 n=14, E1 48.92, E3 0.0013542591, R2 n=91, R1 bound equals error (Ex 2.3 check).")
row("math-L05-L06-problems", "2.2 problems (L05 and L06 tiers)", "L05.html:271-302; L06.html:304-334", "PASS",
    PFX + "Problem sections byte-identical; solutions re-checked on the page: L05 Empirical 1 (1), 2 (1/512 vs 1/1024), 3 (0.366); L06 Empirical 1 (1/196), 2 (45).")
row("math-grades-T", "2.3 grades (T only where proved on the page or by a cited proved result; key-results rows)",
    "L05.html key results l.305-321; L06.html l.338-354; L07.html l.445-461", "PASS",
    PFX + "Block-title grades counted this round: data-grade 20 (L05), 22 (L06), 20 (L07), unchanged except the new L07 Definition 1.2 (no grade; a definition). No over-grade found in the changed claims (L06 canon sentence is an assertion proved by Prop 3.4; L07 Def 1.2 carries no claim grade).")

# ---- cards
row("cards-count-and-basis", "2.7 cards (count and basis per slice lesson)", "course/modules/M/M5/cards.json (slice L05 17, L06 19, L07 30 = 66)", "PASS",
    "Re-run this round: total 233 cards, ids unique; slice counts L05 17, L06 19, L07 30 (66). Graded cards without basis: none; basis without grade: none.")
row("cards-L05-read", "2.7 cards (L05 cards read in full against the current text)",
    "cards.json M5-c069..c084, c221 (c222 removed)", "PASS",
    CPFX + "All 17 L05 slice cards read this round. Changed: M5-c084 now 'What is the pointwise limit of f_n(x) = x^n on [0,1]?' (grade T, basis Example 1.4); checked against L05.html:81 ('f(x)=0 for x<1 and f(1)=1'). Removed c222 (boolean print). The other 16 cards are byte-identical and unchanged.")
row("cards-L06-read", "2.7 cards (L06 cards read in full against the current text)", "cards.json M5-c085..c100, c194, c223, c240", "PASS",
    CPFX + "Changed: M5-c223 now 'In the proof of Proposition 1.3, why must each chosen index n_k exceed n_(k-1)?' (T). Checked against L06.html:80: 'pick n_k > n_{k-1} with x_{n_k} in I_k, which is possible because infinitely many indices give such terms'. Matches. Other 18 cards byte-identical.")
row("cards-L07-read", "2.7 cards (L07 cards read in full against the current text)",
    "cards.json M5-c101..c120, c196, c197, c198, c203, c210, c211, c224, c225, c241, c242", "PASS",
    CPFX + "Changed: M5-c105 (Theorem 2.1(c)) now without the 'known once x1 is computed' gloss; checked against L07.html:105-113 (the bound, for every n >= 0). Added: M5-c242 'What is a complete metric space (Lesson 7, Definition 1.2)?' answer 'A metric space in which every Cauchy sequence converges to a point of the space. This is the definition of Lesson 4, Definition 3.2.' checked against L04.html:265-266 (same definition). Other 27 cards byte-identical.")
row("cards-duplicate-c078-c107", "2.7 cards (no duplicate cards; round-1 FAIL re-verified)", "cards.json M5-c078, M5-c107", "PASS",
    CPFX + "Fronts differ (c078 statement of Prop 3.2; c107 location of the proof of L07 Prop 2.4). Not duplicates.")
row("cards-duplicate-c074-c079", "2.7 cards (no duplicate cards; round-1 FAIL re-verified)", "cards.json M5-c074, M5-c079", "PASS",
    CPFX + "c074 asks whether the pointwise limit of x^n is continuous; c079 asks which hypothesis Prop 2.1 needs. Different facts.")
row("cards-grade-c115", "2.7 cards (grade and basis mirror the key-results row; round-1 FAIL re-verified)", "cards.json M5-c115; L07.html:457 (key-results row)", "PASS",
    CPFX + "c115 grade T, basis 'Canon-breaks, item 2'; L07.html:457 unchanged, grade T, source 'Canon-breaks, items 1 and 2'. Matching.")
row("L05-sup-norm-before-definition", "2.8 terms used before definition (round-1 FAIL re-verified)", "course/modules/M/M5/L05.html:52 (why-it-matters)", "PASS",
    PFX + "No sup-norm term precedes its definition; 'uniform convergence' and 'pointwise convergence' carry explicit Definition references.")
row("L07-thm21-step3-uncited-continuity", "2.2 citations for steps (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:134 (Theorem 2.1 proof, Step 3)", "PASS",
    PFX + "Step 3 cites Definition 1.1 for the contraction inequality, the uniqueness-of-limits argument, and phi x_n = x_{n+1}.")
row("L07-thm21-step1-geometric-uncited", "2.2 citations for steps (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:132 (Step 1); L05.html:214-221", "PASS",
    PFX + "Step 1 cites Lesson 5, Proposition 2.5 for beta^n -> 0 and Lemma 2.2 for the geometric bound; L05.html:219-221 proves a^n -> 0 by Bernoulli.")
row("L07-def12-ungraded-T-claim", "2.3 grades (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:66-68 (Definition 1.2), :86-94 (Prop 1.5), :181-182 (Cor 3.2)", "PASS",
    "Re-verified this round against the changed text: Definition 1.2 block (l.66-68) has no data-grade (definition, not a claim). Prop 1.5 (T) proved on the page from hypothesis (2), which cites L02 Theorem 2.5 (listed in References). Cor 3.2 (T) proved on the page.")
row("cards-coverage-slice", "2.7 cards: coverage of definitions, claims, misconceptions (BUILDER_RULES 7: one card per definition)",
    "course/modules/M/M5/L07.html:66-68 (Definition 1.2); cards.json M5-c242", "PASS",
    "Round-4 gap closed: M5-c242 covers Definition 1.2 (complete metric space). Every slice definition (L05 1.1, 1.2; L06 1.1, subsequence, bounded; L07 1.1, 1.2, named theorems) has a card; slice misconceptions (3 per page) and key-results rows have cards.")
row("cards-duplicate-scan", "2.7 cards (no duplicate cards across the file)", "cards.json (233 cards)", "PASS",
    "Re-run this round (difflib front similarity over all pairs): no exact duplicate fronts; ids unique. Highest pairs (c166/c167 0.98, c170/c233 0.96, c127/c128 0.94, slice c106/c211 0.88, c104/c210 0.87, c069/c070 0.87) test different facts (conclusion of different results or different definitions). New c242 and changed c084, c105, c223 do not duplicate any card above 0.75.")
row("card-label-refs", "2.7 cards agree with the lesson text (every card number appears in its lesson)", "cards.json slice cards vs L05/L06/L07 text", "PASS",
    CPFX + "Labels on changed or added cards checked: 'Example 1.4' (L05.html:80), 'Proposition 1.3' (L06.html:74), 'Lesson 7, Definition 1.2' (L07.html:66), 'Lesson 4, Definition 3.2' (L04.html:265), 'Theorem 2.1(c)' (L07.html:98-114). Unchanged cards carried.")
row("cards-hypotheses-carried", "2.7 cards carry a proposition's hypotheses (rule 10)", "cards.json M5-c072, c105, c106, c109, c211, c241 and other proposition cards", "PASS",
    CPFX + "c105 (changed) carries the Theorem 2.1 hypotheses (complete, nonempty, contraction, x0 and recursion) matching L07.html:100-106. Other proposition cards carried.")
row("lemma-2-2-grade", "2.3 grade on the title of a proved lemma", "course/modules/M/M5/L07.html:117; cards M5-c106, M5-c211", "PASS",
    PFX + "L07.html:117 block-title data-grade=T; proof on the page; c106 and c211 T with basis 'Proof in Section 2 (Lemma 2.2)'.")
row("figures", "2.8 figures (no chart in L05-L07)", "L05.html, L06.html, L07.html", "PASS",
    "Re-run this round: grep for data-chart, <figure, <svg, data-figures returns 0 on all three pages.")
row("L07-why-it-matters-locators", "2.9 forward references and locators in the lesson preview", "course/modules/M/M5/L07.html:52", "PASS",
    PFX + "Theorem 2.1 reference (l.98-114) accurate; Lesson 8 mention is plain text.")
row("delta-hunks-read", "2.2 every hunk of the delta read (edbb7aa8..dde0486b) on slice files and cards", "git diff edbb7aa8 dde0486b (slice files, twins, cards.json, plans/FINAL-ARCHITECT-RULINGS.md, plans/KNOWN-ISSUES.md)", "PASS",
    "All slice hunks read in full: L05.html:134 (docstring; checked against stdout); L06.html:289 (Boundedness sentence; checked against Prop 3.4); L07.html:67 (Def 1.2 cross-reference; checked against L04.html:265-266); L07.html:528 (References; checked, row scope-words); tests/labs/M5/lab-M5-L05-1.py:48 (docstring; checked). cards.json slice hunks: c084, c105, c222 (removed), c223, c242 (added). Other cards.json hunks (c055, c064, c067, c135, c173, c175, c229, c243) belong to L04, L08 and L10 and are outside this slice. plans/FINAL-ARCHITECT-RULINGS.md rulings 27-29 are E3-only; plans/KNOWN-ISSUES.md is E3-only.")
row("L06-lab1-keep-rule", "2.5 labs: the Part A selection rule as stated (L06 Lab 1 hypothesis)", "L06.html:101 (hypothesis); tests/labs/M5/lab-M5-L06-1.py (Part A selection code)", "PASS",
    PFX + "Hypothesis text and twin unchanged. Rule and output (out/twin_check.out L06 'subsequence_indices 1 2 3 4 5 32 45 55') consistent with the stated rule.")
row("L07-thm21-step1-cross-lesson-citation", "2.4 mathematics: a proof step that cites another lesson", "course/modules/M/M5/L07.html:132; course/modules/M/M5/L05.html:214-221", "PASS",
    PFX + "L05 Proposition 2.5 is an earlier-lesson result proving a^n -> 0 for 0 < a < 1; the citation locator is correct.")
row("ruling-13-grades", "Ruling 13 (T versus C for worked values) and ruling 26 scope", "cards.json (lab-only values graded C: c082, c083, c098, c099, c100, c117, c118, c119, c120, c203, c221, c224; page-derived values graded T: c074, c084, c110)", "PASS",
    "Re-checked after this round's changes. c084 (T) is a value derived in a numbered Example (Example 1.4) and no longer a lab print; c223 (T) is a proof step; c222 (lab boolean) removed. Remaining C cards are lab-output values named with their lab, as ruling 13 allows. Note (not a row): C cards c098 (index 55 of a 4096-term prefix) and c082 are construction-level lab prints; they name the lab and their basis says 'illustrates the construction only' for c098.")
row("scope-words", "2.2 scope words (all, every, always, only, exactly, same) and the References claim", "course/modules/M/M5/L07.html:528 (References); :132; :151", "PASS",
    "Round-4 FAIL resolved. L07.html:528 now says 'except for three imported results': (1) the completeness of R (Lesson 2, Theorem 2.5), a hypothesis of Propositions 1.5 and 2.4 (l.88, l.146); (2) Lesson 5, Proposition 3.2 with X = S, the whole proof of Proposition 2.4 (l.151); (3) Lesson 5, Proposition 2.5, used by Step 1 of Theorem 2.1 (l.132). Checked against every theorem-like block on the page (Props 1.4, 1.5, Thm 2.1, Lemma 2.2, Prop 2.4, Props 3.1, Cor 3.2): all others are proved on the page. Assumptions 1 and 2 named where used (l.170, l.182, l.195). The count of three is correct.")
row("lab-docstring-types-L05", "2.5 labs: docstring sentences about what the lab prints (rule 2 includes docstrings)", "tests/labs/M5/lab-M5-L05-1.py:48; course/modules/M/M5/L05.html:134", "PASS",
    "Round-4 FAIL resolved: docstring now reads 'Every value is an exact fraction, an integer, a boolean, or a float with ten decimals.' out/twin_check.out shows booleans (equals_half_power True; value_at_one_for_every_order True), integers (order labels; least order 10), exact fractions (1/2, 1/1024) and ten-decimal floats (0.9043820750). Sentence supported by output.")
row("defined-twice-complete-metric-space", "BUILDER_RULES 1.10 (no concept defined twice): complete metric space", "course/modules/M/M5/L07.html:66-68 vs course/modules/M/M5/L04.html:265-266", "PASS",
    "Round-4 FAIL resolved: L07 Definition 1.2 now reads 'complete in the sense of Lesson 4, Definition 3.2' (L07.html:67), the only definition of completeness on the page; L04 Definition 3.2 (l.265-266) is unchanged. L06.html:263 uses the same cross-reference form.")
row("cards-trivia-lab-prints", "2.7 cards are not trivia (BUILDER_RULES 7; verifier 2.7)", "cards.json M5-c084, M5-c222 (removed), M5-c223", "PASS",
    "Round-4 FAIL resolved: c084 is now the pointwise limit (T); c222 is removed; c223 is now a proof step (T). The mathematical content of the removed prints is carried by c070, c074, c083, c099, c221, c224 (unchanged).")
row("L07-rulings-check", "Architect rulings 1-29 applied to slice b", "plans/FINAL-ARCHITECT-RULINGS.md (rulings 1-29); slice files", "PASS",
    "Rulings 27-29 are E3-only (checked). Ruling 13 applied (ruling-13-grades). Ruling 26 classification of this round: no blocking kind found (no false or unproved mathematical statement, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, or lab statement the code does not support). LOW rows open: pages-raw-angle-brackets and open-items-status (defect 1 residue).")

# ---- new rows this round
row("def12-cross-reference", "2.9 cross-lesson reference (L07 Definition 1.2 to L04 Definition 3.2): same definition, lesson order, DAG",
    "course/modules/M/M5/L07.html:67; course/modules/M/M5/L04.html:265-266", "PASS",
    "L04 Definition 3.2 reads 'The space (X,d) is complete when every Cauchy sequence in X converges to a point of X.' L07 Definition 1.2 says the same definition by reference. L04 precedes L07 in the unit and is in L07's prerequisite closure (check_dag M5 PASS). No new concept use before definition.")
row("L06-boundedness-sentence", "2.6 prose claim (L06 canon-breaks 'Boundedness is not enough', changed this round)",
    "course/modules/M/M5/L06.html:289; L06.html:278-283 (Prop 3.4)", "PASS",
    "Sentence now says the closed unit ball 'contains a sequence with no convergent subsequence'. Prop 3.4 proof (l.282-283) shows each e_n lies in the ball and no subsequence of (e_n) converges. Claim is true and proved on the page.")

rows_out = R
ids = [r["id"] for r in rows_out]
n_pass = sum(1 for r in rows_out if r["status"] == "PASS")
n_fail = sum(1 for r in rows_out if r["status"] == "FAIL")
frag = {
    "unit": "M5",
    "slice": "b",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for M5-b (lessons L05-L07, their lab twins and their retrieval cards), round 5 (delta verification); did not build M5 and shares no context with the builders or earlier verifiers",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-M5-b.round4.json)",
    "checkout": CK + " (detached at dde0486b; .venv symlinked)",
    "scratch": "ledgers/M5/scripts/M5-b-r5/ (gates.sh, twin_check.py, rederive.py, write_fragment_r5.py; outputs in ledgers/M5/scripts/M5-b-r5/out/)",
    "verified_at": "2026-11-09T08:30:00Z",
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta edbb7aa8..dde0486b for the slice: L05.html:134 (docstring), L06.html:289 (Boundedness sentence), L07.html:67 (Def 1.2 cross-reference to L04 Def 3.2), L07.html:528 (References), tests/labs/M5/lab-M5-L05-1.py:48 (docstring); cards.json: c084 changed to T, c105 changed, c222 removed, c223 changed to T, c242 added (c243 is L08, outside). L06 and L07 twins unchanged.",
        "All four round-4 blocking/low findings are resolved and re-verified: scope-words (count now three, listed), lab-docstring-types-L05, defined-twice-complete-metric-space, cards-coverage-slice (c242), cards-trivia-lab-prints.",
        "New LOW finding: raw '<' in math text (40 occurrences in 30 lines). Round-4 row pages-raw-angle-brackets was PASS on a grep that does not match digits or backslashes; corrected to FAIL. HTML5 renders these correctly; the fix is escaping to &lt; (LOW; ruling 26 non-blocking).",
        "Ruling 26 blocking kinds: none found in this round. The verdict is FAIL only because of the two LOW rows (pages-raw-angle-brackets, open-items-status).",
        "Builder F open-items file (plans/M5-open-items.md as cited in round 4) is not the Builder D file in the pinned checkout; defects 1, 2 and 6 were checked as recorded in the round-4 fragment.",
        "Carried rows use the prefix 'Carried from round 4 (...)' only where the cited lines are outside every changed hunk (git diff --unified=0 edbb7aa8 dde0486b).",
        "Gate runs: all gate commands re-run on dde0486b; each rc=0 (out/_rc.txt). Full M5 unit gates (check_pages, check_dag, check_projects, page_smoke for the three slice pages, run_labs) pass.",
        "The committed ledgers/M5/M5-b.json at dde0486b (round 9 of a different lineage, pin b6865c7d) was overwritten with this round-5 fragment as instructed.",
    ],
    "summary": "M5-b round 5 (delta): %d rows, %d PASS, %d FAIL (both LOW, raw '<' residue); no blocking ruling-26 kind; mutants none (slice has no project grader)." % (len(rows_out), n_pass, n_fail),
}
json.dump(frag, open(CK + "/ledgers/M5/M5-b.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows_out), "pass", n_pass, "fail", n_fail)
