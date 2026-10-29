"""Writes ledgers/E1/E1-b.json (round 7, slice b) from the rows verified in this round."""

import datetime
import json

R = []


def row(rid, check, location, evidence, status="PASS"):
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


row("E1-b-run-labs", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py",
    "tools/run_labs.py --unit E1 -> 'run_labs E1: PASS (12/12)', rc=0 (run by me, round 7; output /tmp/e1b7/labs.out).")
row("E1-b-twin-isolated", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py",
    "python -I -W error on each twin: rc=0; 18, 12 and 25 output lines (/tmp/e1b7/twin04.out, twin05.out, twin06.out).")
row("E1-b-page-twin-identical", "2.5-labs", "course/modules/E/E1/L04.html, L05.html, L06.html lab sections",
    "python -I ledgers/E1/scripts/E1-b-r7 ... page_twin_check.py (round-6 script re-run on this checkout): 'ALL OK'; "
    "page_code_eq_twin=True and expected_eq_output=True for L04 (code_len 4102, 18 lines), L05 (4513, 12), L06 (7284, 25).")
row("E1-b-lint-types", "2.5-labs", "tests/labs/E1/lab-E1-L04-1.py, lab-E1-L05-1.py, lab-E1-L06-1.py",
    "ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; "
    "mypy --no-incremental on the 3 twins: 'Success: no issues found in 3 source files'.")
row("E1-b-page-smoke", "2.5-labs, 2.9-structure", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "tools/page_smoke.py --unit E1 --pages L04 L05 L06 -> 'page_smoke E1: PASS' (each page PASS; rc=0; /tmp/e1b7/smoke.out).")
row("E1-b-check-pages", "2.9-structure", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "tools/check_pages.py --unit E1 -> 'check_pages E1: PASS' (rc=0). Quiz: 10 items per page, one data-correct per MC item (checked by script).")
row("E1-b-check-dag", "2.9-structure, 2.9-DAG", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "tools/check_dag.py --unit E1 -> 'check_dag E1: PASS' (rc=0). E1 prereqs [M2] (curriculum/02-economics-finance-core.yaml:22); "
    "'proof by induction' is M1's mathematical-induction (curriculum/01-foundations.yaml:110), in the closure via M2.")
row("E1-b-dag-convexity-name", "2.9-DAG (Architect decision 3)", "course/modules/E/E1/L05.html:313-316 (P3)",
    "Round-6 FAIL is fixed on pin 7aa909e. P3 title is now 'Strict concavity of the profit' (L05.html:313) and the solution "
    "no longer says 'needs no convexity theory' (L05.html:316). grep -i convex over L04, L05, L06 pages, their lab text and "
    "cards.json returns no match. Concavity (second derivative -2b) is allowed by the decision.")
row("E1-b-pytest-labs", "2.5-labs", "tests/test_labs.py -k 'E1 and (L04 or L05 or L06)'",
    "pytest -q: 3 passed (output '...  [100%]'). Other units' lab tests not run (outside slice).")

# Numbers: re-derived by ledgers/E1/scripts/E1-b-r7/l04_numbers.py (Decimal, 60 digits)
row("E1-b-numbers-L04", "2.1-numbers",
    "course/modules/E/E1/L04.html prose: Example 1.3 (l.83), Example 2.4 (l.134), Example 3.2 (l.277), Remark 3.3 (l.282), "
    "Section 4 (l.288), Problems E1-E3, R1-R3, quiz (l.441-512), Lab 1 prose (l.249, l.309, l.374)",
    "Re-derived: eps(10)=-0.2, eps(40)=-2; p*(120)=10, dp/da=1/22, dQ/da=10/11 (1-2/22 = 10/11); (a/p)dp/da=6/11; "
    "p''(120)=-1/5324, p'''(120)=3/1288408; fwd ratios 9.99628 and 9.99963 (printed 9.9963, 9.99963); cen ratios 100.00296, "
    "100.0000296, 100.0000003 (prose 100.003, 100.00003, 100.0000003); fwd/cen at h=0.01 = 24198.99998 (prose 24,199 / 24198.99998); "
    "leading fwd 0.99999587 and cen 1+2.99e-11 ratios; h=1 cen 1.0000299 and fwd 0.99589 times leading terms; "
    "exact 1% rise p(121.2)=10.0544108843 -> 0.5441088% (prose 0.5441088%); M1 eps=-2/3; M2 eta=3; M3 eps(20)=-2; "
    "R1 dp/da=-1/2; R2 dp/da=1/(2 sqrt a); R3 a/(2p(1+p))=6/11 at a=120. Every stated figure matches.")
row("E1-b-numbers-L05", "2.1-numbers",
    "course/modules/E/E1/L05.html: Lab 1 prose (l.127, l.234), Misconceptions (l.254, l.258, l.262), M1-M3, P1-P3, E1-E3, R1-R3 (l.350-366), quiz (l.395-462)",
    "Re-derived in closed form: Lab cases (120,1,20),(90,3,10),(200,4,5): p_m=70,20,27.5; Q_m=50,30,90; pi_m=2500,300,2025; "
    "Lerner 5/7, 1/2, 9/11; p_m-a/(2b)=10,5,2.5=c/2; second difference -2b = -2,-6,-8; |eps(70)|=1.4; "
    "M1 p=30,Q=40,pi=800; M2 p=12,Lerner 2/3; M3 p=25; E2 Lerner 9/11, eps=-11/9; R1 p_m=beta c/(beta-1), Lerner 1/beta; "
    "R2 midpoint; R3. Quiz keys 30, 40, 5/7=0.7142857, 2500, 20, 11/9=1.2222222 all consistent.")
row("E1-b-numbers-L06", "2.1-numbers",
    "course/modules/E/E1/L06.html: Example 1.5 (l.92), Example 2.7 (l.142), Prop 2.8 (l.147-158), Lab 1 prose (l.385), Table (l.406-410), "
    "Problems M1-M3, E1-E3 (l.503-517), quiz (l.571-638)",
    "Re-derived: monopoly (120,1,20): Q=50, fee 70, profit 2500; Cournot each d/3=100/3, total 200/3, fee 160/3, each 10000/9=1111.11 "
    "(1111 cents); Bertrand fee c=20, volume 100; Prop 4.1 differences d/6, d/3, d/(6b), d/(3b), d^2/(36b) (checked by algebra); "
    "lab iteration first within 1e-6 at step 25 (d=100), 25 (d=60), 26 (d=180); gap -25/805306368 = -(100/3)/2^30; "
    "grid fees 1001 of 1201 (E2); E3 sharing 937.5 vs undercut ~1875 (lab 1874.949999); M1 R(24)=18, R(70)=0; "
    "M2 q=20, fee 50/3, profit 400/3; quiz x_2=25, fee 160/3=53.33, volume 200/3=66.67, 20000/9=2222.22.")
row("E1-b-lab-L04", "2.5-labs (sentences about prints)", "course/modules/E/E1/L04.html Lab 1 section; tests/labs/E1/lab-E1-L04-1.py",
    "Stated predictions (l.139): dp/da=1/22=0.0454545455; forward error falls x10, central x100 per tenfold fall in h (observed ratios 9.996, 100.00003). "
    "Printed Parts A-D match the twin's output line for line (page expected block equals twin output, page_twin_check).")
row("E1-b-lab-L05", "2.5-labs (sentences about prints)", "course/modules/E/E1/L05.html Lab 1 section; tests/labs/E1/lab-E1-L05-1.py",
    "Lab docstring and prose match the code: Part A grid of 1/10 cent (grid_prices), Part B Lerner vs 1/|e| with exact Fractions, Part C "
    "central-difference slope (0) and second difference normalised by step^2 (-2b). Printed values match prose.")
row("E1-b-lab-L06", "2.5-labs (sentences about prints)", "course/modules/E/E1/L06.html Lab 1 section; tests/labs/E1/lab-E1-L06-1.py",
    "Docstring vs code: Part A asserts closed form on grid (assert in part_a), Part B asserts iterate equals closed form at 30 steps, "
    "Part C fee grid 1/10 cent and sharing = h(r)/2. Prose claims (1001 of 1201; four rival fees; undercut about twice sharing; "
    "steps 25, 25, 26) match the printed output.")
row("E1-b-math-L04", "2.2-math", "course/modules/E/E1/L04.html Sections 1-3 (Def 1.1, Remark 1.2, Example 1.3, Prop 1.4, Remark 1.5, Def 2.1, Remark 2.2, Prop 2.3, Example 2.4, Prop 3.1, Example 3.2, Remark 3.3)",
    "Proof steps re-read: Prop 1.4 equivalences valid for 0<p<a/b; Remark 1.2 chain rule; Prop 2.3 F_p=D_p-S'<0 and dp/da=D_a/(S'-D_p); "
    "Prop 3.1 expansions (plus-sign and even/odd cancellation; central h^2/6 p''') correct; p'' and p''' formulas correct.")
row("E1-b-math-L05", "2.2-math", "course/modules/E/E1/L05.html Sections 1 (Def 5.1, Assumption M, Prop 5.2, Remark 5.3, Prop 5.4, Corollary 5.5), Problems M1-M3, P1-P3, E1-E3, R1-R3",
    "Prop 5.2 completed square and constant bp_m^2-ac=(a-bc)^2/(4b) verified; p_m<a/b since bc<a; Prop 5.4 first-order condition and sign of eps "
    "verified; Corollary 5.5 |eps(p_m)|=(a+bc)/(a-bc); R1 sign of pi' verified; R2 midpoint; R3 uses Prop 1.4 with 0<p_m<a/b.")
row("E1-b-math-L06", "2.2-math", "course/modules/E/E1/L06.html Sections 1-4 (Lemma 1.3, Prop 1.4, Lemma 2.4, Thm 2.5, Remark 2.6, Prop 2.8, Lemma 3.2, Thm 3.3, Remark 3.4, Prop 4.1), Problems M1-M3, P1-P3, R1-R2",
    "Lemma 2.4 cases D<=0 and D>0; Thm 2.5 uniqueness argument (q1=0 gives R(d/2)=d/4>0 contradiction); Prop 2.8 induction (r^t in [-1/2,1], x_t in [0,d/2]); "
    "Thm 3.3 Steps 1-4 (Step 2 move to c, Step 3 Case A/B with continuity of h, Step 4) checked; R1 n-exchange q=d/(n+1) verified; "
    "R2 tie-rule argument checked.")
row("E1-b-quiz-keys", "2.2-quiz", "course/modules/E/E1/L04.html, L05.html, L06.html quiz sections",
    "Each MC item has exactly one data-correct option (script). Numeric answers re-derived: L04 -0.2, -2, 1/22=0.0454545, 6/11; "
    "L05 30, 40, 5/7=0.7142857, 2500, 11/9=1.2222222, 20; L06 30, 160/3=53.33, 200/3=66.67, 25, 20000/9=2222.22, 2500 vs 2222.22.")
row("E1-b-cards", "2.6-cards", "course/modules/E/E1/cards.json (55 cards with lesson L04, L05 or L06, including E1-c038..c053, c054..c066, c067..c091, c133)",
    "All 55 read. Each card matches its lesson statement (Definition 1.1 hypotheses carried by c069/c070/c075/c076; Assumption M by c055-c059; "
    "lab cards grade C naming the lab). Every card number appearing in a card appears in its lesson (Proposition, Remark, Problem and Example numbers checked). "
    "No duplicate fronts or ids in the whole cards.json. Changed in this round: c041, c048-c050, c056, c057, c060, c062-c064, c069, c070, c075, c087, c077 wording only.")
row("E1-b-notation", "2.4-notation", "notation/notation.json (8 registered symbols); symbols in L04-L06",
    "Registered: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} plus macros. Math tokens in L04-L06 (script): none of these used. "
    "Local letters (beta in L05 R1, d and k in L04, d in L06, Pi/pi for profit) are defined where used.")
row("E1-b-structure-prose", "2.9-structure", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "check_pages PASS; section order and key-results and quiz present; 'Lesson 4 of 9', 'Lesson 5 of 9', 'Lesson 6 of 9'.")
row("E1-b-process-words", "2.2-prose", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "grep for builder, verifier, round, draft, pending, TODO, fix, plan, architect, audit, grader, mutat over learner text: no process words. "
    "Only 'unrounded' (a value term, used with its meaning).")
row("E1-b-hours", "2.9-hours", "course/modules/E/E1/L04.html, L05.html, L06.html (data-hours); course/modules/E/E1/index.html; plans/E1-build-plan.md lesson table",
    "data-hours=10 on each of the three pages. Hub: 9 lessons x 10 = 90 (data-hours-lessons=90) + 30 project = 120 (Tier F 120 hours). Plan table: L04, L05, L06 = 10.")
row("E1-b-refs", "2.7-references", "course/modules/E/E1/L04.html, L05.html, L06.html References sections; references/references.json",
    "Each page's References says 'This lesson cites no outside source'; no URL or citation key in the three pages (grep). "
    "Architect decision 7 (cite only varian2014intermediate; no historical attribution) respected: no Cournot/Bertrand year, no Nash name (Architect decision 2).")
row("E1-b-figures", "2.9-figures", "course/modules/E/E1/L04.html, L05.html, L06.html",
    "No figure, svg or figures-*.js script in the three pages (grep: 0 <figure>/<svg>; only katex and site.js scripts). "
    "No external http(s) request target in the pages. data-files attribute absent.")
row("E1-b-cross-lesson", "2.9-DAG / cross-references", "L04 (Lesson L05 Definition 5.1); L05 (Proposition 1.4 of L04; Lesson L07); L06 (Lesson 3 cost with k>0; Lesson 7)",
    "L04 line 52 cites L05 Definition 5.1 (exists, l.58). L05 cites L04 Prop 1.4 (exists) and L07 (exists). L06 'Lesson 3' setting: L03 Setting C(q)=F+cq+kq^2 with k>0 "
    "(curriculum-page L03.html, Setting); L06 Lesson 7 exists (NextL07). Prop/Remark/Problem numbers cited in each lesson exist on that page.")

summary = ("E1-b round 7 (pin 7aa909e): 26 PASS rows, 0 non-PASS. The round-6 FAIL (E1-b-dag-convexity-name) is fixed; "
           "every number, proof, lab, quiz key and card re-derived this round.")
notes = ("Scope: L04, L05, L06 and lab-E1-L04-1, lab-E1-L05-1, lab-E1-L06-1 (plus their cards). Delta since pin 44f1eb6: "
         "L05 P3 title and solution; L06 'Proposition 4.1' wording and fieldset style; cards c041, c048-c050, c056, c057, c060, c062-c064, c069, c070, c075, c077, c087 (wording). "
         "L04 page and all three twins unchanged in the delta. Lab twins are demonstrations, so no mutation testing (ruling). "
         "Not checked: (1) live verify_refs (only --offline run, 560 entries, 0 problems); (2) browser visual diff beyond page_smoke's own checks; "
         "(3) raw HTML markup line by line (text read via a tag-stripping extractor, ledgers/E1/scripts/E1-b-r7/extract.py); "
         "(4) hub index.html, build_site --check, and the other E1 lessons (other slices); (5) E3 test_labs failures noted earlier are outside this slice; "
         "(6) the pinned checkout has no round-6 or round-5 carry-forward rows used: all rows re-derived, none carried.")

out = {
    "unit": "E1",
    "slice": "b",
    "round": 7,
    "verifier": "independent verifier, Haiku 5.5 (claude-haiku-5-5), fresh checkout; no build context",
    "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
    "base": "44f1eb6a417ce687a9b88c7ee917e72566b29892 (round-6 pin); no carry-forward rows, every row re-derived this round",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-E1-b",
    "scratch": "/tmp/e1b7",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "PASS",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
with open("/Users/billyribeiro/.fanout/wt/verifyB7-E1-b/ledgers/E1/E1-b.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("rows", len(R), "non-PASS", sum(1 for r in R if r["status"] != "PASS"))
