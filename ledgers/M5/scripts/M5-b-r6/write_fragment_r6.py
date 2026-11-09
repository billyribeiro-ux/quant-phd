"""Write the round-6 delta fragment for M5-b (lessons L05-L07, twins, slice cards)."""
import json

CARRY5 = "Carried from round 5 ({what} byte-identical since the previous pin dde0486b): "
RE6 = "Re-verified in round 6 (pin e896b7a4): "
CARDS = "course/modules/M/M5/cards.json slice blocks (66 cards, L05-L07) byte-identical; out/cards_bytes.out"
L05_NOCHG = "L05.html lines outside the delta hunks"
TREE = "html_tree_compare.out (markup token stream identical; text differs only in the listed chunks)"

rows = []


def row(rid, check, location, status, evidence):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


# Gates, re-run on the pin
row("gate-check-pages", "2.9 structure (check_pages --unit M5, and per page L05/L06/L07)",
    "course/modules/M/M5/L05.html, L06.html, L07.html, cards.json", "PASS",
    RE6 + "`tools/check_pages.py --unit M5`: 'check_pages M5: PASS'; `--page L05`, `--page L06`, `--page L07` each PASS (out/check_pages_M5.out, out/check_pages_L05.out, out/check_pages_L06.out, out/check_pages_L07.out; rc=0).")
row("gate-check-dag", "2.9 DAG (check_dag --unit M5)", "course/modules/M/M5/L05.html, L06.html, L07.html", "PASS",
    RE6 + "`tools/check_dag.py --unit M5`: 'check_dag M5: PASS' (out/check_dag_M5.out, rc=0). The L07 Definition 1.2 cross-reference is plain text (L07.html:67), so no new DAG edge.")
row("gate-check-projects", "2.9 unit gate (check_projects --unit M5)", "unit M5 (project outside this slice)", "PASS",
    RE6 + "`tools/check_projects.py --unit M5`: 'check_projects M5: PASS' (out/check_projects_M5.out). Project not verified in this slice.")
row("gate-run-labs", "2.5 labs (run_labs --unit M5 --page L05/L06/L07)", "course/modules/M/M5 (labs of L05, L06, L07)", "PASS",
    RE6 + "`tools/run_labs.py --unit M5`: 'run_labs M5: PASS (13/13)'; per page L05, L06, L07: 'PASS (1/1)' (out/run_labs_M5.out, out/run_labs_L05.out, out/run_labs_L06.out, out/run_labs_L07.out).")
row("lab-L05-twin", "2.5 labs (twin alone under python -I -W error; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L05-1.py (line 1 docstring changed this delta); course/modules/M/M5/L05.html section#lab-M5-L05-1", "PASS",
    RE6 + "`python -I -W error tests/labs/M5/lab-M5-L05-1.py` from /tmp: rc=0, stderr 0 bytes (out/twin_L05.rc, out/twin_L05.stderr). Stdout (out/twin_L05.stdout) read in full: Part B prints 'sup_distance 1/2, 1/4, 1/32, 1/1024, 1/1125899906842624' and 'equals_half_power True' for orders 1, 2, 5, 10, 50; 'least_order_with_half_power_below_1_over_1000 10' ((1/2)^9=1/512 > 1/1000, (1/2)^10=1/1024 < 1/1000); Part C 0.99^10=0.9043820750, 0.99^100=0.3660323413, 0.99^1000=0.0000431712 (checked by Fraction arithmetic). run_labs PASS: page code byte-identical to twin and expected block equal to stdout. Docstring line 1 ('[0, 1/2]'), line 9 ('the function 0 on [0, 1]', defect 6 of Builder F resolved) and line 48 ('exact fraction, integer, boolean, or float with ten decimals') read against stdout: each sentence is supported.")
row("lab-L06-twin", "2.5 labs (twin alone; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L06-1.py (unchanged); course/modules/M/M5/L06.html section#lab-M5-L06-1", "PASS",
    RE6 + "twin unchanged between pins (git diff name-only); `python -I -W error` rc=0, stderr 0 bytes (out/twin_L06.rc); run_labs PASS (out/run_labs_L06.out).")
row("lab-L07-twin", "2.5 labs (twin alone; page code equals twin; expected equals output)",
    "tests/labs/M5/lab-M5-L07-1.py (unchanged); course/modules/M/M5/L07.html section#lab-M5-L07-1", "PASS",
    RE6 + "twin unchanged between pins; `python -I -W error` rc=0, stderr 0 bytes (out/twin_L07.rc); run_labs PASS (out/run_labs_L07.out).")
row("gate-page-smoke", "2.9 page_smoke (console errors, math rendered, 360 px, no external requests; labs in Pyodide)",
    "course/modules/M/M5/L05.html, L06.html, L07.html", "PASS",
    RE6 + "`tools/page_smoke.py --unit M5 --pages L05 L06 L07`: each page PASS, 'page_smoke M5: PASS' (out/page_smoke_L05_L07.out, rc=0).")
row("gate-ruff-mypy-twins", "2.5 lint and types (twins); mypy strict over the repository",
    "tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py", "PASS",
    RE6 + "`ruff check tests/` 'All checks passed!' (out/ruff_check.out); `ruff format --check tests/labs/M5/` '13 files already formatted' (out/ruff_format.out); `mypy --no-incremental` on the three twins 'Success: no issues found in 3 source files' (out/mypy_twins.out). Repository-wide mypy not re-run (no .py outside the three twins changed in the slice).")
row("gate-pytest-labs-M5", "2.5 labs (CI test)", "tests/test_labs.py -k M5", "PASS",
    RE6 + "`pytest tests/test_labs.py -k M5 -q`: 13 tests, all passed, rc=0 (out/pytest_labs_M5.out).")
row("gate-verify-refs-offline", "2.1 citations (offline integrity)", "references/references.json; slice pages", "PASS",
    RE6 + "`tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems', rc=0 (out/verify_refs_offline.out). No slice page changed a citation key.")

# Content rows
row("pages-raw-angle-brackets", "2.9 structure (HTML validity; raw '<' in math and prose)",
    "L05.html, L06.html, L07.html (round-5 residue lines 60-383, 258-332, 52-195)", "PASS",
    RE6 + "Round-5 FAIL resolved. ledgers/M5/scripts/M5-b-r6/raw_lt.py: 0 raw '<' not starting markup in L05, L06, L07 (out/raw_lt.out); grep -c '<[^A-Za-z/!?]' gives 0 lines per page. Every '<' in math/text is now '&lt;' (for example L05.html:215 '0&lt;a&lt;1', L07.html:52 '\\(\\beta&lt;1\\)'). html_tree_compare.out: markup token streams identical across pins (812/806/861 tokens), so no tag was changed by the escaping.")
row("pages-banned-strings", "2.9 banned strings and process words", "L05.html, L06.html, L07.html, cards.json (slice cards)", "PASS",
    RE6 + "check_pages M5 PASS (banned strings are a check_pages item, out/check_pages_M5.out). Changed prose (L05.html:52; L06.html:290, 308, 310) re-read: no process words, no banned strings.")
row("notation-registry", "2.4 notation (every symbol vs notation/notation.json; no reuse of a registered symbol)",
    "L05.html, L06.html, L07.html", "PASS",
    RE6 + "checks_misc.py (out/checks_misc.out, line (d)): the set of LaTeX commands (\\\\[A-Za-z]+) in each slice page is identical across pins (no new command). The changed substantive sentences add no symbol: L05.html:52 and the L05 docstring use none; L06.html:290, 308, 310 use p, f and maximum, which occur in the unchanged text (L06.html:290 and :308 before the edit).")
row("hours-split", "2.9 hours arithmetic", "L05.html, L06.html line 2 data-hours=10; L07.html line 2 data-hours=11; L10.html data-hours=11; course/index.html data-hours-lessons; project.html data-hours-project; curriculum/01-foundations.yaml hours", "PASS",
    CARRY5.format(what="course/index.html, course/modules/M/M5/project.html, curriculum/01-foundations.yaml and the data-hours lines of L05, L06, L07, L10") +
    "git diff: none of these files changed between dde0486b and e896b7a4 (checks_misc.out (e)); data-hours values re-read: L05 10, L06 10, L07 11, L10 11.")
row("problems-tiers", "2.9 problem set (four tiers, worked solutions)", "L05.html #problems; L06.html #problems; L07.html #problems", "PASS",
    RE6 + "problem count per page unchanged (12/12/12 old/new, out/checks_misc.out (d)). Changed solution text: L05.html:290-300 escape only (html_tree_compare.out); L06.html:308 and :310 reviewed (f(x)=x^3-3x on [-2,2]: f(-2)=-2, f(-1)=2, f(1)=-2, f(2)=2, f'=3x^2-3 zeros at -1, 1; maximum 2 at -1 and 2, minimum -2 at -2 and 1, checked in checks_misc.out (b)).")
row("structure-order", "2.9 structure (section order, BUILDER_RULES 4.2)", "L05.html, L06.html, L07.html", "PASS",
    RE6 + "check_pages per page PASS (out/check_pages_L05/L06/L07.out); markup token streams identical across pins (html_tree_compare.out), so section order and element structure are unchanged.")
row("forward-reference-L07-roadmap", "2.9 forward reference (BUILDER_RULES 4.1: no link to a later lesson)", "course/modules/M/M5/L07.html:52 (why-it-matters)", "PASS",
    RE6 + "L07.html:52 changed only by HTML escaping (text chunk identical; html_tree_compare.out, L07 shows 0 differing text chunks). 'Lesson 8 applies Theorem 2.1' is plain text, not a link (markup identical).")
row("open-items-status", "2.9 open items for slice b (Builder F defects 1, 2, 6 as listed in plans/M5-open-items.md)",
    "L05.html, L06.html, L07.html; tests/labs/M5/lab-M5-L05-1.py", "PASS",
    RE6 + "Round-5 FAIL resolved. Defect 1 (raw '<'): no raw '<' remains in L05/L06/L07 (raw_lt.out); the listed lines now carry escapes (L05.html:215 '0&lt;a&lt;1', L05.html:220 '0&lt;a^{n}', L06.html:70 'for \\(j&lt;k\\)'). Defect 2 (ratio wording): L07.html:327 and :493 now read 'tends to 1 for pairs of fixed separation far from the origin'; checked against the algebra |phi x - phi y|/|x - y| = |x+y|/(phi x + phi y) with x = y + h, y -> infinity, ratio -> 1 for fixed h (the pair is far from the origin). Defect 6 (twin docstring): twin line 9 now reads 'the function 0 on [0, 1]', matching the code (max of x^n over the grid). plans/M5-open-items.md Builder F section is unchanged between pins (the delta changes only decision 3).")
row("lab-claims-L05", "2.5 labs: sentences about what the lab prints, checks, contains (hypothesis, interpretation; twin)",
    "L05.html:86 (hypothesis, changed by escape and the [0,1/2] grid wording), :174 (interpretation); twin lab-M5-L05-1.py", "PASS",
    RE6 + "L05.html:86 re-read against out/twin_L05.stdout: 'on the grid k/100 of [0,1] the sup distance from x^n to 0 is 1 for every printed order n' (all five orders print 1); 'on the grid of [0,1/2] the sup distance is (1/2)^n' (Part B prints 1/2, 1/4, 1/32, 1/1024, 1/1125899906842624); 'least order ... is 10' (stdout line 'least_order_with_half_power_below_1_over_1000 10'); 'values of x^n at 0.99 decay' (0.9043820750, 0.3660323413, 0.0000431712); 'exact (fractions) except the printed floats in Part C' (the twin uses Fraction throughout; float() only in Part C). L05.html:174 unchanged in text.")
row("lab-claims-L06", "2.5 labs: sentences about what the lab prints, checks, contains", "L06.html:101 (hypothesis), :222 (interpretation); twin lab-M5-L06-1.py", "PASS",
    CARRY5.format(what="L06.html:101 and :222 and tests/labs/M5/lab-M5-L06-1.py") + "none of those lines is in the delta hunks (L06 hunks: 258, 290, 308, 310, 330-332); run_labs PASS re-run (out/run_labs_L06.out).")
row("lab-claims-L07", "2.5 labs: sentences about what the lab prints, checks, contains", "L07.html:200 (hypothesis), :310 (interpretation); twin lab-M5-L07-1.py", "PASS",
    CARRY5.format(what="L07.html:200 and :310 and tests/labs/M5/lab-M5-L07-1.py") + "neither line is in the delta hunks (L07 hunks: 52, 60, 77, 83, 103, 127, 132, 165, 170, 182, 187, 195, 317, 326-327, 375, 389, 414, 423, 437, 439, 490); run_labs PASS re-run (out/run_labs_L07.out).")
row("num-L05-lab1", "2.6 numbers in prose vs printed/unrounded values (Lab 1 expected block)", "L05.html:156-173 (expected block); :174 interpretation", "PASS",
    CARRY5.format(what="L05.html:156-174") + "the expected block is outside every delta hunk; run_labs PASS (expected equals the twin's stdout, out/twin_L05.stdout).")
row("num-L05-prose", "2.6 numbers in prose (Empirical 2 and 3; quiz numeric items; Example 1.4 and Proposition 2.4)",
    "L05.html:290-293; :334-340; :360-362; :280-283", "PASS",
    RE6 + "L05.html:281, 283, 290-291, 297, 299-300 changed only by escaping (html_tree_compare.out: identical text). Numbers re-derived: (1/2)^9=1/512>1/1000, (1/2)^10=1/1024<1/1000 (least order 10); 0.99^100=0.36603 (0.366 to three places); (1/2)^3=0.125 on [0,1/2]. Lines 334-340 and 360-362 not in the delta.")
row("num-L06-lab1", "2.6 numbers in prose (Lab 1 expected block; Empirical items; quiz)", "L06.html:205-221 (expected block); :321-330; :415-416", "PASS",
    RE6 + "L06.html:330-332 changed only by escaping (html_tree_compare.out: identical text); 205-221 and 415-416 unchanged. run_labs PASS (out/run_labs_L06.out).")
row("num-L07-lab-A", "2.6 numbers in prose (Lab 1 Part A expected block)", "L07.html:296-304 (Part A block); :310 interpretation; quiz L07.html:510-512", "PASS",
    RE6 + "L07 text unchanged in these lines (no L07 text chunk differs, html_tree_compare.out); run_labs PASS (out/run_labs_L07.out).")
row("num-L07-lab-B", "2.6 numbers in prose (Lab 1 Part B; E3 and its unrounded difference)", "L07.html:305 (block); :310; :411-414 (E3)", "PASS",
    RE6 + "L07.html:414 changed only by escaping (html_tree_compare.out: identical text). Difference re-derived: (cos 0.995 - cos 1)/0.005 = 0.8401167..., sin 1 = 0.8414709848..., difference 0.0013542591... (unrounded) (computed in Python float arithmetic in round 6: quotient 0.840116725732564, sin 1 = 0.8414709848078965, gap 0.0013542590753324868).")
row("num-L07-lab-C", "2.6 numbers in prose (Lab 1 Part C block)", "L07.html:307-309 (block); :310; card M5-c203", "PASS",
    RE6 + "L07 text chunks identical across pins (html_tree_compare.out); run_labs PASS (out/run_labs_L07.out).")
row("num-L07-prose", "2.6 numbers in prose (Examples, Problems, quiz)", "L07.html:340-345 (M2), :350 (M3), :391-395 (E1), :398-404 (E2), :406-409 (E3), :424-427 (R2), :473-507 (quiz)", "PASS",
    RE6 + "L07 text chunks identical across pins (html_tree_compare.out, 0 differing chunks); the changed lines 375, 389, 414, 423, 437, 439, 490 are escape-only.")
row("num-L07-misc3", "2.6 numbers in prose (Misconception 3)", "L07.html:335", "PASS",
    RE6 + "L07:335 text identical across pins (html_tree_compare.out).")
row("math-L05-props", "2.2 mathematics (Props 1.3, 2.1, 2.4, 2.5, Ex 2.3, Ex 1.4)", "L05.html:65-76, :179-221; Proof 2.5 :218-220; Ex 2.3 :199-201", "PASS",
    RE6 + "L05.html:65, 75-76, 186, 188, 200, 210, 220 changed only by escaping (html_tree_compare.out: text chunks identical outside the listed chunk 87 at line 52). Proofs re-read on the unescaped text: Prop 2.5 (a^n -> 0 via (1+h)^n >= 1+nh) and Ex 2.3 (x_k = 1 - 1/k) unchanged.")
row("math-L05-props-2", "2.2 mathematics (Props 3.1, 3.2; Remark 3.3; canon-breaks; misconceptions)", "L05.html:223-267", "PASS",
    RE6 + "L05.html:233, 256, 264 changed only by escaping (html_tree_compare.out). Text identical.")
row("math-L06-props", "2.2 mathematics (Lemma 1.2, Props 1.3, 1.4, Ex 1.5, Prop 2.1, Cor 2.2, Prop 3.1, Cor 3.2, ...)", "L06.html:56-96, :226-268, :276-282, :285-299", "PASS",
    RE6 + "L06.html:258 escape-only; L06.html:290 changed substantively ('no point of (0,1) is a maximiser' -> 'attains the maximum'). Re-derived: for f(x)=x on (0,1) and p in (0,1), f((p+1)/2)=(p+1)/2 > p = f(p) with (p+1)/2 in (0,1), so no point of (0,1) attains the supremum 1, and 1 is not in (0,1). Statement and proof unchanged in content.")
row("math-L07-core", "2.2 mathematics (Defs 1.1-1.2, Props 1.4, 1.5, Thm 2.1, Lemma 2.2, Ex 2.3, Prop 2.4, Prop 3.1 ...)", "L07.html:56-197", "PASS",
    RE6 + "every L07 changed line (60, 77, 83, 103, 127, 132, 165, 170, 182, 187, 195) is escape-only (html_tree_compare.out: 0 differing text chunks in L07, markup identical). Mathematics unchanged; read on the unescaped text.")
row("math-L07-canon", "2.2 mathematics (canon-breaks items 1-3; misconceptions 1-3)", "L07.html:316-337", "PASS",
    RE6 + "L07.html:317, 326-327 escape-only. Re-derived: phi x = sqrt(x^2+1); (phi x - phi y)(phi x + phi y) = (x-y)(x+y) and phi x + phi y > |x|+|y| >= |x+y| give |phi x - phi y| < |x-y|; phi has no fixed point since sqrt(x^2+1) > |x| >= x; ratio |x+y|/(phi x + phi y) -> 1 along x = y+h, y -> infinity.")
row("math-L07-assumptions", "2.2 named assumptions (Assumption 1, 2; uses)", "L07.html:156-170 (Assumptions 1, 2); uses at :172, :177, :182, :195", "PASS",
    RE6 + "L07.html:165, 170 escape-only (html_tree_compare.out). Assumption 2(d) sin 1 < 1 and 2(a) sin increasing on [0,1] read unchanged.")
row("math-L07-problems", "2.2 problems (M1-M3, P1-P3, E1-E3, R1-R3)", "L07.html:346-440 (problem set)", "PASS",
    RE6 + "L07.html:375, 389, 414, 423, 437, 439 escape-only (html_tree_compare.out).")
row("math-L05-L06-problems", "2.2 problems (L05 and L06 tiers)", "L05.html:271-302; L06.html:304-334", "PASS",
    RE6 + "L06.html:308 and :310 changed (solution wording: 'a point where the maximum is attained', 'a point where the minimum is attained'). Re-derived: f(x)=x^3-3x on [-2,2]; f(-2)=-2, f(-1)=2, f(1)=-2, f(2)=2; f'=3x^2-3 vanishes at -1 and 1; maximum 2 at x=-1 and 2, minimum -2 at x=-2 and 1 (checks_misc.out (b)). Logic (interior extremum has f'=0) unchanged. L05.html:290-300 and L06.html:330-332 escape-only.")
row("math-grades-T", "2.3 grades (T only where proved on the page or by a cited proved result; key-results rows)",
    "L05.html key results l.305-321; L06.html l.338-354; L07.html l.445-461", "PASS",
    RE6 + "key-results rows: L05.html:315 escape-only; no grade attribute changed in the slice pages (html_tree_compare.out markup identical).")
row("cards-count-and-basis", "2.7 cards (count and basis per slice lesson)", "course/modules/M/M5/cards.json (slice L05 17, L06 19, L07 30 = 66)", "PASS",
    CARRY5.format(what=CARDS) + "re-counted: L05 17, L06 19, L07 30 = 66 (out/cards_delta.out). Delta cards are L01 (c008, c245, c246), L04 (c193, c244), L08 (c135), L09 (c208), L10 (c187, c247, c248), none in L05-L07.")
row("cards-L05-read", "2.7 cards (L05 cards read in full against the current text)", "cards.json M5-c069..c084, c221 (c222 removed)", "PASS",
    CARRY5.format(what="the L05 card blocks M5-c069..c084 and c221 (out/cards_bytes.out)") + "lesson text these cards cite re-read on the current pin: c082, c083 against L05 Lab 1 output (out/twin_L05.stdout); c074/c075/c076/c080 against L05.html text (escape-only changes).")
row("cards-L06-read", "2.7 cards (L06 cards read in full against the current text)", "cards.json M5-c085..c100, c194, c223, c240", "PASS",
    CARRY5.format(what="the L06 card blocks (out/cards_bytes.out)") + "c097 ('f(x)=x on (0,1) ... has no maximum') re-read against the changed L06.html:290 ('attains the maximum'): consistent.")
row("cards-L07-read", "2.7 cards (L07 cards read in full against the current text)", "cards.json M5-c101..c120, c196, c197, c198, c203, c210, c211, c224, c225, c241, c242", "PASS",
    CARRY5.format(what="the L07 card blocks (out/cards_bytes.out)") + "L07 lines cited by the cards are escape-only or unchanged (html_tree_compare.out: 0 differing L07 text chunks).")
row("cards-duplicate-c078-c107", "2.7 cards (no duplicate cards; round-1 FAIL re-verified)", "cards.json M5-c078, M5-c107", "PASS",
    CARRY5.format(what="the two card blocks") + "and the whole-file duplicate scan (row cards-duplicate-scan) finds 0 duplicate fronts across 238 cards.")
row("cards-duplicate-c074-c079", "2.7 cards (no duplicate cards; round-1 FAIL re-verified)", "cards.json M5-c074, M5-c079", "PASS",
    CARRY5.format(what="the two card blocks") + "and the whole-file duplicate scan (row cards-duplicate-scan) finds 0 duplicate fronts.")
row("cards-grade-c115", "2.7 cards (grade and basis mirror the key-results row; round-1 FAIL re-verified)", "cards.json M5-c115; L07.html:457 (key-results row)", "PASS",
    CARRY5.format(what="the M5-c115 block and L07.html:457 (not in the L07 delta hunks)") + "row still T with the same basis.")
row("L05-sup-norm-before-definition", "2.8 terms used before definition (round-1 FAIL re-verified)", "course/modules/M/M5/L05.html:52 (why-it-matters)", "PASS",
    RE6 + "L05.html:52 changed (the sentence now says pointwise convergence 'does not guarantee' continuity). The terms used are unchanged: 'uniform convergence', 'Definition 1.2', 'the sup distance of L04, Example 1.6'; no 'sup norm' term is introduced before its definition.")
row("L07-thm21-step3-uncited-continuity", "2.2 citations for steps (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:134 (Theorem 2.1 proof, Step 3)", "PASS",
    CARRY5.format(what="L07.html:134") + "line 134 is outside every L07 delta hunk.")
row("L07-thm21-step1-geometric-uncited", "2.2 citations for steps (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:132 (Step 1); L05.html:214-221", "PASS",
    RE6 + "L07.html:132 escape-only (html_tree_compare.out). Step 1 cites 'Lesson 5, Proposition 2.5' for beta^n -> 0 and the citation is present in the text.")
row("L07-def12-ungraded-T-claim", "2.3 grades (round-1 FAIL re-verified)", "course/modules/M/M5/L07.html:66-68 (Definition 1.2), :86-94 (Prop 1.5), :181-182 (Cor 3.2)", "PASS",
    RE6 + "L07.html:182 escape-only; :66-68 and :86-94 unchanged. Definition 1.2 carries no grade; Prop 1.5 and Cor 3.2 keep their grades and proofs (text identical).")
row("cards-coverage-slice", "2.7 cards: coverage of definitions, claims, misconceptions (BUILDER_RULES 7: one card per definition)", "course/modules/M/M5/L07.html:66-68 (Definition 1.2); cards.json M5-c242", "PASS",
    CARRY5.format(what="the M5-c242 block and L07.html:66-68") + "both byte-identical (out/cards_bytes.out; L07 hunks do not include 66-68).")
row("cards-duplicate-scan", "2.7 cards (no duplicate cards across the file)", "cards.json (238 cards)", "PASS",
    RE6 + "checks_misc.py (c): 238 cards, 238 unique ids, 0 duplicate fronts (out/checks_misc.out). The delta added M5-c244..c248 and edited c008, c135, c187, c193, c208 (out/cards_delta.out); none duplicates a front.")
row("card-label-refs", "2.7 cards agree with the lesson text (every card number appears in its lesson)", "cards.json slice cards vs L05/L06/L07 text", "PASS",
    RE6 + "slice card blocks byte-identical (out/cards_bytes.out). Card-to-lesson agreement re-read for every card whose cited sentence changed: c082, c083 (L05 Lab 1 output), c097 (L06 'no maximum'), c221 (x^n at 1/2 from Part A). Lesson number references unchanged.")
row("cards-hypotheses-carried", "2.7 cards carry a proposition's hypotheses (rule 10)", "cards.json M5-c072, c105, c106, c109, c211, c241 and other proposition cards", "PASS",
    RE6 + "those card blocks are byte-identical (out/cards_bytes.out). Their cited propositions: L05 Prop 1.3 (L05.html:75-76 escape-only), L07 Prop 1.5/Lemma 2.2/Cor 3.2 (escape-only or unchanged). Hypotheses stated on the cards match the text (html_tree_compare.out: text identical there).")
row("lemma-2-2-grade", "2.3 grade on the title of a proved lemma", "course/modules/M/M5/L07.html:117; cards M5-c106, M5-c211", "PASS",
    CARRY5.format(what="L07.html:117 and the M5-c106, M5-c211 blocks") + "L07:117 is outside every L07 delta hunk.")
row("figures", "2.8 figures (no chart in L05-L07)", "L05.html, L06.html, L07.html", "PASS",
    RE6 + "no <svg> element in L05, L06 or L07 at either pin (checks_misc.out (d): svg 0/0); check_pages M5 PASS.")
row("L07-why-it-matters-locators", "2.9 forward references and locators in the lesson preview", "course/modules/M/M5/L07.html:52", "PASS",
    RE6 + "L07.html:52 escape-only (html_tree_compare.out: identical text).")
row("delta-hunks-read", "2.2 every hunk of the delta read (dde0486b..e896b7a4) on slice files and cards", "git diff dde0486b e896b7a4 (L05, L06, L07, twins, cards.json, plans); L08/L10 hunks read for context only", "PASS",
    RE6 + "every hunk read with `git diff -U0`: L05 (18 escape hunks, substantive 52, 86-87), L06 (290, 308, 310 substantive; 258, 330-332 escape), L07 (21 escape hunks), twin L05 line 1, cards.json (slice blocks byte-identical; changed non-slice blocks c008, c135, c187, c193, c208; new c244-c248), plans M5-build-plan.md, M5-open-items.md (decision 3), FINAL-ARCHITECT-RULINGS.md (rulings 30-34 appended), KNOWN-ISSUES.md (appended). Out of slice, read for context only: L08.html:73 (Example 1.2 now data-grade T), L10.html:389, :510.")
row("ruling-13-grades", "Ruling 13 (T versus C for worked values) and ruling 26 scope", "cards.json (lab-only values graded C: c082, c083, c098, c099, c100, c117, c118, c119, c120, c203, c221, c224; page-derived T: c074, c084, c110)", "PASS",
    CARRY5.format(what="the slice card blocks listed (out/cards_bytes.out)") + "lab-derived values remain C with a lab basis; page-derived values remain T.")
row("scope-words", "2.2 scope words (all, every, always, only, exactly, same) and the References claim", "course/modules/M/M5/L07.html:528 (References); :132; :151", "PASS",
    RE6 + "L07.html:528 and :151 unchanged; :132 escape-only. Changed sentences checked: L05.html:52 (no scope word added); L05 hypothesis 'for every printed order n' (L05.html:86) backed by stdout (all five orders print 1); L06.html:290 'no point of (0,1) attains the maximum' backed by the proof; L06.html:308 'a point where the maximum is attained' backed by Corollary 2.2 (stated just before).")
row("lab-docstring-types-L05", "2.5 labs: docstring sentences about what the lab prints (rule 2 includes docstrings)", "tests/labs/M5/lab-M5-L05-1.py:48; course/modules/M/M5/L05.html:134 (page copy)", "PASS",
    CARRY5.format(what="tests/labs/M5/lab-M5-L05-1.py line 48 and L05.html:134") + "line 48 ('an exact fraction, an integer, a boolean, or a float with ten decimals') matches out/twin_L05.stdout (Fractions, integers, booleans, 10-decimal floats). Only twin line 1 changed in the delta.")
row("defined-twice-complete-metric-space", "BUILDER_RULES 1.10 (no concept defined twice): complete metric space",
    "course/modules/M/M5/L07.html:66-68 vs course/modules/M/M5/L04.html:265-266", "PASS",
    CARRY5.format(what="L07.html:66-68 and L04.html:265-266") + "neither range is in the delta hunks (L04 is not in the delta).")
row("cards-trivia-lab-prints", "2.7 cards are not trivia (BUILDER_RULES 7; verifier 2.7)", "cards.json M5-c084, M5-c222 (removed), M5-c223", "PASS",
    CARRY5.format(what="the M5-c084 and M5-c223 blocks") + "c222 remains removed (no M5-c222 in the file). c084 asks a mathematical value (the pointwise limit), not a printed string.")
row("L07-rulings-check", "Architect rulings 1-29 applied to slice b", "plans/FINAL-ARCHITECT-RULINGS.md (rulings 1-29 and new 30-34); slice files", "PASS",
    RE6 + "the diff of FINAL-ARCHITECT-RULINGS.md only appends at line 97 (hunk @@ -96,0 +97,24 @@), so rulings 1-29 are byte-identical. Rulings 30-34 read: 30 is this delta protocol; 31 concerns the M5 project (not slice b); 32 and 33 concern E3; 34 concerns FC2. None changes a slice-b lesson.")
row("def12-cross-reference", "2.9 cross-lesson reference (L07 Definition 1.2 to L04 Definition 3.2): same definition, linked or restated",
    "course/modules/M/M5/L07.html:67; course/modules/M/M5/L04.html:265-266", "PASS",
    CARRY5.format(what="L07.html:67 and L04.html:265-266") + "neither line is in the delta hunks.")
row("L06-boundedness-sentence", "2.6 prose claim (L06 canon-breaks 'Boundedness is not enough')", "course/modules/M/M5/L06.html:289; L06.html:278-283 (Prop 3.4)", "PASS",
    CARRY5.format(what="L06.html:278-289") + "no L06 delta hunk falls in 278-289 (hunks at 258, 290, 308, 310, 330-332).")
row("L06-lab1-keep-rule", "2.5 labs: the Part A selection rule as stated (L06 Lab 1 hypothesis)", "course/modules/M/M5/L06.html:101 (hypothesis); tests/labs/M5/lab-M5-L06-1.py (Part A selection code)", "PASS",
    CARRY5.format(what="L06.html:101 and tests/labs/M5/lab-M5-L06-1.py") + "neither changed in the delta.")
row("L07-thm21-step1-cross-lesson-citation", "2.4 mathematics: a proof step that cites another lesson", "course/modules/M/M5/L07.html:132; course/modules/M/M5/L05.html:214-221", "PASS",
    RE6 + "L07.html:132 and L05.html:220 escape-only (html_tree_compare.out: identical text). The cited Lesson 5 Proposition 2.5 is the proof that a^n -> 0 for 0 < a < 1; its text is present at L05.html:220.")

doc = {
    "unit": "M5",
    "slice": "b",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for M5-b (lessons L05-L07, their lab twins and their retrieval cards), round 6 (delta verification); did not build M5 and shares no context with the builders or earlier verifiers",
    "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
    "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-M5-b.round5.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-M5-b (detached at e896b7a4; .venv symlinked)",
    "scratch": "ledgers/M5/scripts/M5-b-r6/ (classify_delta.py, cards_delta.py, cards_bytes.py, raw_lt.py, html_tree_compare.py, checks_misc.py, write_fragment_r6.py; outputs in ledgers/M5/scripts/M5-b-r6/out/)",
    "verified_at": "2026-11-09T11:44:33Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta dde0486b..e896b7a4 for the slice: L05.html (escape-only except line 52 why-it-matters and the lab docstring/hypothesis at 86-87), L06.html (escape-only at 258, 330-332; substantive at 290, 308, 310), L07.html (escape-only at all 21 hunks), tests/labs/M5/lab-M5-L05-1.py line 1 (docstring). cards.json slice blocks are byte-identical; no slice card changed.",
        "Escape-only proof: html_tree_compare.out shows markup token streams identical across pins for L05, L06 and L07, and text chunks identical except the five substantive chunks (L05 lines 52 and the twin docstring; L06 lines 290, 308, 310).",
        "Round-5 non-PASS rows re-verified: pages-raw-angle-brackets (40 raw '<' now 0) and open-items-status (defects 1, 2, 6 for slice b) are PASS.",
        "Carry rule: rows marked 'Carried from round 5' cite only lines or blocks outside the delta hunks (lines and card blocks byte-identical). Rows marked 'Re-verified in round 6' cite lines changed only by HTML escaping, verified by the markup/text token comparison, or the substantive sentences re-derived here.",
        "Out of slice, observed and not verified: L08.html:73 Example 1.2 now carries data-grade T (L08 is outside slice b); L10.html:389 and :510 text changes; cards c008, c135, c187, c193, c208 changed and c244-c248 added (L01, L04, L08, L09, L10). Owner slices should verify these.",
        "Plans: plans/M5-build-plan.md lines 304-312 and plans/M5-open-items.md decision 3 changed (in-place sweep and residual stop declared not valid alternatives; ruling 31). Project, not slice b.",
        "Nothing could not be checked for slice b that the protocol requires. Repository-wide mypy was not re-run (only the three twins changed in the slice); the twin-level mypy and ruff runs are the slice-relevant gates.",
    ],
    "summary": "M5-b round 6 (delta dde0486b..e896b7a4): 68 rows, 68 PASS, 0 FAIL. Both round-5 FAILs (pages-raw-angle-brackets, open-items-status) are resolved. The slice has no project grader, so mutants are none. Verdict PASS.",
}

with open("ledgers/M5/M5-b.json", "w", encoding="utf-8") as fh:
    json.dump(doc, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "ids unique", len({r['id'] for r in rows}))
