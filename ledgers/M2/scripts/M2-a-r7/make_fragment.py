import json, sys
sys.path.insert(0, "tools")
C6 = "Carried from round 6 (cited lines not in the 44f1eb6..7aa909e delta hunks, so byte-identical): "
rows = []
def row(i, check, loc, ev, status="PASS"):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})

row("M2a-R6-01", "check_pages unit gate", "tools/check_pages.py --unit M2",
    "Fresh, round 7 at 7aa909e: stdout 'check_pages M2: PASS', exit 0.")
row("M2a-R6-02", "check_dag gate", "tools/check_dag.py --all",
    "Fresh: 'check_dag <unit>: PASS' for every unit; grep for non-PASS lines returned nothing.")
row("M2a-R6-03", "run_labs for the unit", "tools/run_labs.py --unit M2",
    "Fresh: 'run_labs M2: PASS (27/27)', exit 0.")
row("M2a-R6-04", "Twins alone under python -I -W error; page code and expected block byte-equal",
    "tests/labs/M2/lab-M2-L01-1.py..L06-1.py; course/modules/M/M2/L01..L06.html lab sections",
    "Fresh: ledgers/M2/scripts/M2-a-r7/twin_compare.py. All six twins exit 0 with empty stderr; page code==twin True and expected==output True for L01-L06 (L05 re-run after the delta).")
row("M2a-R6-05", "page_smoke in Chromium", "tools/page_smoke.py --unit M2 --pages index L01..L06",
    "Fresh: 'page_smoke M2: PASS'; each of modules/M/M2/L03..L06 PASS (tail of output shown; index and L01/L02 lines in same run).")
row("M2a-R6-06", "Lab pytest", "tests/test_labs.py -k M2",
    "Fresh: python -m pytest tests/test_labs.py -k M2 -q printed 27 dots and no failure line.")
row("M2a-R6-07", "ruff on the twins", "tests/labs/M2",
    "Fresh: ruff check tests/labs/M2 'All checks passed!'; ruff format --check '27 files already formatted'.")
row("M2a-R6-08", "Registry integrity for cited keys", "tools/verify_refs.py --offline",
    "Fresh: 'offline integrity: 560 entries, 0 problems'.")
row("M2a-R6-09", "Independent re-derivation of every printed or claimed number in scope",
    "ledgers/M2/scripts/M2-a-r7/l05_exact.py; l06_grid.py",
    "Fresh for the changed numbers. L05 exact Fraction arithmetic at x=3/2, h=1/10000: product err 2.350000001e-07 (prints 2.35e-07), quotient err 3.3319e-10 (prints 3.33e-10; 3 digits agree with exact value), composite err 8.550000009e-07 (prints 8.55e-07). p'''(1.5)=141 and h^2 p'''/6=2.35e-07. L06 exact grid: 8 of 16 intervals increase, 16 of 16 midpoint agreements, f(-1)=2, f(1)=-2. Numbers in L01-L04 lines not in the delta are carried from round 6 (" + "lines byte-identical; changed L02-L04 hunks are notation-only, \\mathbb{R} to \\R, verified by notation.json macro \\R = \\mathbb{R}).")
row("M2a-R6-10", "Hub hours arithmetic", "course/modules/M/M2/index.html:29,42 and the 24 lesson files",
    C6 + "index.html delta is line 151 only (card title); hours lines not touched. check_pages PASS fresh.")
row("M2a-R6-11", "Hub placement diagnostic arithmetic and skill keys", "course/modules/M/M2/index.html:71,127,132",
    C6 + "index.html hunks do not touch lines 71, 127, 132.")
row("M2a-R6-12", "Hub and page anchors and navigation", "course/modules/M/M2/index.html links; L01-L06 prev/next and cross-links",
    "Fresh: check_pages M2 PASS and page_smoke PASS after the delta. Only change in index.html is the L11 card title text.")
row("M2a-R6-13", "Hub lesson-card descriptions for L01-L24 against lesson titles", "course/modules/M/M2/index.html:144-167",
    "Re-verified fresh: index.html:151 now reads 'Integration by Parts and Substitution'; course/modules/M/M2/L11.html:36 h1 is 'Integration by Parts and Substitution' (exact match). Previous FAIL R6-31 resolved. Other card titles and descriptions not in the delta (carried).")
row("M2a-R6-14", "Concept definitions and links in scope", "course/modules/M/M2/L01.html:61; L04.html:57; L05.html:91",
    C6 + "L01.html and L04.html dfn lines not in hunks. L05.html:91 central-difference dfn read in full and defined before Assumption 1.4 (line 93).")
row("M2a-R6-15", "DAG: later-module names in scope", "course/modules/M/M2/index.html and L01-L06",
    "Fresh: check_dag --all PASS for all units including M2.")
row("M2a-R6-16", "Cross-module references", "index.html:80; L01.html:37; L04.html:154; L13.html:115; M1/L01.html:92-93; M1/L03.html:68; M1/L06.html:36-39",
    C6 + "none of these lines is in the delta; L06 'Lesson 4, Problem R3' (line 83) and 'Lesson 4, Example 1.2' (L05 P3) read fresh and unchanged in meaning.")
row("M2a-R6-17", "Proofs of every T claim in scope",
    "L01 Props 2.2, 3.1, 4.2; L02 Prop 1.1 (i)-(iii), Cor 2.2; L03 Prop 1.3, Cor 1.4, Prop 2.2; L04 Prop 2.1; L05 Lemma 1.1, Props 1.2, 1.3, 2.1; L06 Prop 1.1, Thms 2.2, 2.3, Cor 3.1",
    "Fresh for L06 Thm 2.2 (L06.html:78-84), Thm 2.3 (L06.html:88-96), Cor 3.1 (L06.html:103-111), P1-P3 (L06.html:243-257), R3 (L06.html:307): proofs re-read; Rolle via max/min argument and MVT via g(x)=f(x)-f(a)-s(x-a) are valid; Cor 3.1 (iii) follows from MVT. L05 P3 chain-rule proof re-read: valid. Other proofs' lines not in the delta (carried): " + "L01-L04 and L05 Lemma 1.1, Props 1.2, 1.3, 2.1 lines not in hunks.")
row("M2a-R6-18", "Quiz keyed answers (MCQ) in scope", "course/modules/M/M2/L01..L06 quiz sections",
    "Fresh for changed items: L01 q9 (L01.html:402-407): key 'Nothing follows from boundedness alone about convergence' is the only true option ('It converges' and 'limit equal to largest term' are false; (-1)^n is bounded and does not converge). L06 q5 (key 'increasing') unchanged in key. Other keys carried.")
row("M2a-R6-19", "Quiz numeric answers and tolerances", "course/modules/M/M2/L01..L06 quiz sections",
    "Fresh for L06 numeric item: data-answer 1.1547, tolerance 1e-4, 2/sqrt(3)=1.1547005; key unchanged. Other numeric items carried (lines not in hunks).")
row("M2a-R6-20", "Misconceptions: counterexamples", "course/modules/M/M2/L01..L06 misconception sections",
    "Fresh for changed items: L05 misconception 3 (L05.html:219): (1+h)^3-(1-h)^3 over 2h = 3+h^2 verified; 2.35e-07 etc. match Lab output. L06 misconceptions (L06.html:198-205): x^3 strictly increasing with f'(0)=0; c=1/sqrt(3)~0.577 for x^3 on [0,1] (3c^2=1) verified. Other misconceptions carried.")
row("M2a-R6-21", "Problem sets: worked solutions", "course/modules/M/M2/L01..L06 problem sets (72 problems)",
    "Fresh for changed L05 P3/E1 and L06 M1-M3, P1-P3, R3: M1 f=x^2-4x+1 critical point 2, f(2)=-3 verified; M2 c=2/sqrt(3) verified; M3 f'=3(x-1)(x+1)>0 on (-2,-1), f(-2)=-2<2=f(-1) verified. Unchanged problems carried.")
row("M2a-R6-22", "Empirical items against lab output", "course/modules/M/M2/L01..L06 empirical sections",
    "Fresh for L05 E1 (L05.html:282-284): 2.35e-07 = 1e-8*141/6 verified; matches printed 2.35e-07. L04/L01-L03 empirical items carried.")
row("M2a-R6-23", "Lab hypotheses (predictions) against output", "course/modules/M/M2/L01..L06 lab sections, class 'hypothesis'",
    "Fresh for L05 hypothesis (L05.html:99): 32.0625, 29/49~0.591837, 95.0625 verified; h=1e-4 magnitude claim consistent with 2.35e-07, 3.33e-10, 8.55e-07. Other hypotheses lines carried.")
row("M2a-R6-24", "Lab interpretations and docstrings against code (excluding the q value)",
    "course/modules/M/M2/L01..L06 interpretation paragraphs; twins' docstrings",
    "Fresh for L05 docstring (tests/labs/M2/lab-M2-L05-1.py:3-10; output format now .2e so 'three significant digits' holds) and L05 interpretation (L05.html:172); L06 interpretation (L06.html:179) and L06 twin docstring (lines 1-12, 'under Assumption 2.1' as stated). Remaining lab docstrings carried.")
row("M2a-R6-25", "Lab determinism, network and stdlib", "tests/labs/M2/lab-M2-L01-1.py..L06-1.py",
    "Fresh: all six twins import only __future__, fractions, collections.abc or stdlib; run under python -I -W error with exit 0 and identical outputs to page expected blocks.")
row("M2a-R6-26", "Lesson structure per BUILDER_RULES and check_pages minima", "course/modules/M/M2/L01..L06",
    "Fresh: check_pages --unit M2 PASS after the delta.")
row("M2a-R6-27", "Cards for L01-L06 (76 cards, of 380 in cards.json)", "course/modules/M/M2/cards.json",
    "Fresh: counts by lesson L01 14, L02 13, L03 13, L04 11, L05 12, L06 13 = 76 (was 75 in round 6; the added card is M2-c379, L05). No duplicate ids or fronts. Changed cards re-checked against current text: M2-c018 (L02 Remark 3.1, Prop 1.1(iii) b!=0, Misconception 1 at L02.html:199-202) OK; M2-c047 (L04.html:119-121 output '3.000001e-06') OK; M2-c056 (2.35e-07) OK; M2-c057 (3.33e-10, exact 3.3319e-10) OK; M2-c058 (8.55e-07) OK; M2-c067 (L06 Cor 3.1 hypotheses, L06.html:103) OK; M2-c379 (central difference defined at L05.html:91 before Assumption 1.4 at :93) OK. Unchanged cards carried.")
row("M2a-R6-28", "Banned words, process words and data", "course/modules/M/M2/index.html and L01-L06",
    "Fresh: grep for can-be-shown/clearly/obviously/trivially/TODO/TBD/lorem/builder/verifier over index, L01-L06 and cards.json returned no banned or process word in the slice. Only 'fixed' hits are 'held fixed' in cards.json outside this slice.")
row("M2a-R6-29", "Grade legend letters against BLUEPRINT section 3", "course/modules/M/M2/L01..L06 grade-legend block",
    "Fresh: legend at L0x.html:46 defines C as 'single study or lab result'; grade-C spans name the lab (for example L05.html:172 'Lab 1, one point and one step'). Grade-C lab results therefore satisfy the page legend.")
row("M2a-R6-30", "Number printed as an error equals its exact value to 3 digits",
    "course/modules/M/M2/L05.html:170,172,219; cards.json M2-c056..c058; tests/labs/M2/lab-M2-L05-1.py",
    "Re-verified fresh: exact rational computation (l05_exact.py) gives 2.35e-07, 3.3319e-10, 8.55e-07. Printed table (L05.html:170-172 and twin output) now 2.35e-07, 3.33e-10, 8.55e-07, agreeing with exact values to 3 digits. Previous 3.328e-10 is fixed. Prose and cards agree with the table.")
row("M2a-R6-31", "Hub card title matches lesson h1", "course/modules/M/M2/index.html:151; course/modules/M/M2/L11.html:36",
    "Re-verified fresh: index.html:151 title 'Integration by Parts and Substitution' equals L11.html:36 h1 exactly.")
row("M2a-R6-32", "Quiz item asks for a 'strongest' claim but keys a weak one", "course/modules/M/M2/L01.html:402-407",
    "Re-verified fresh: prompt now 'Which statement about a bounded sequence is true?'; keyed option 'Nothing follows from boundedness alone about convergence' is the only true option. The 'strongest' wording is gone.")
row("M2a-R6-33", "Grade-C lab results carry a registry key (BLUEPRINT section 3)",
    "Every grade-C span in course/modules/M/M2/L01..L06 (L01.html:149,335; L02.html:151,329; L03.html:172,324; L04.html:122,292; L05.html:172,338; L06.html:179,326); grade-C cards",
    "Re-verified fresh. BLUEPRINT section 3 asks for a registry key on every substantive claim, but the page's own grade legend (L0x.html:46) defines C as 'single study or lab result', and VERIFIER_RULES rule 9 requires 'read off a SIMULATED lab are C naming the lab'. Each C span names its lab (Lab 1). Ruled PASS on that basis; orchestrator may want to reconcile BLUEPRINT section 3 with BUILDER_RULES 'basis' carve-out.")
row("M2a-R6-34", "Assumption openers: 'Assuming Assumption 1.4' rule",
    "tests/labs/M2/lab-M2-L05-1.py:5-8; course/modules/M/M2/L05.html:105,219,282,284",
    "Re-verified fresh: twin docstring now 'Assuming Assumption 1.4, the central difference has error of order h^2. That assumption is stated on the page and not proved there.' L05.html:219 and :282/:284 open with 'Assuming Assumption 1.4'. Residual: none in L05.")
row("M2a-R6-35", "Assumption openers: 'Assuming Assumption 2.1' rule",
    "course/modules/M/M2/L06.html:111,201,218,232,220; L06 twin docstring line 9",
    "Re-verified fresh: L06.html:111 and :201 now begin 'Assuming Assumption 2.1, Corollary 3.1 (ii)...'. Non-blocking note: mid-sentence 'under Assumption 2.1' remains at L06.html:124 (twin docstring), :218, :232 and in the problem text, each naming the assumption; ruled acceptable because the rule as cited in R6 targets uses of Corollary 3.1 with no assumption named. Orchestrator may want to standardise the wording.")
row("M2a-R6-36", "Notation: registered macros only (BUILDER_RULES 3.1, notation.json)",
    "course/modules/M/M2/index.html; L01..L06",
    "Re-verified fresh: grep -n mathbb over index.html and L01-L06 returns no hits. \\R is registered in notation/notation.json (macro \\R, tex \\mathbb{R}).")

frag = {
    "unit": "M2", "slice": "a", "round": 7, "verifier": "independent verifier (Haiku 5.5)",
    "pin": "7aa909e", "base": "44f1eb6a417ce687a9b88c7ee917e72566b29892 (round-6 pin); delta 44f1eb6..7aa909e",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M2-a",
    "scratch": "ledgers/M2/scripts/M2-a-r7/",
    "verified_at": "2026-10-28",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scope: hub index.html, L01-L06, lab twins L01-L06. Delta read in full: index.html:151; L01-L06 hunks; tests/labs/M2/lab-M2-L05-1.py; cards for L02, L04, L05, L06 and new M2-c379. No mutants: lesson slice, mutation rule applies to project graders only (VERIFIER_RULES 2.6). Not checked: L07-L24 and project (other slices); mypy --no-incremental on the full project; pytest full suite; full re-read of unchanged lines of L01-L04 (carried by delta reasoning); freshness of external references (not web-checked). Scripts: twin_compare.py, l05_exact.py, l06_grid.py, make_fragment.py.",
    "summary": "36 rows: 36 PASS, 0 FAIL, 0 UNVERIFIABLE. Round 6 FAIL rows R6-30..R6-36 re-verified and resolved (R6-33 ruled PASS on the page grade legend).",
}
frag["notes"] = frag["notes"]
with open("ledgers/M2/M2-a.json", "w") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
