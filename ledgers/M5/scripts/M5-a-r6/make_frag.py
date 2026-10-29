import json
P = "course/modules/M/M5/"
rows = []
def row(id, check, location, status, evidence, fix=None):
    r = {"id": id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# mechanical gates
row("M5a-gate-check-pages", "2.9-structure", "course/modules/M/M5 (unit)", "PASS",
    "`.venv/bin/python tools/check_pages.py --unit M5` printed 'check_pages M5: PASS', rc=0 (hub and L01-L04 covered). Note: `--page index` is not a valid selector; the hub is checked by the unit run.")
row("M5a-gate-check-dag", "2.9-dag", "course/modules/M/M5 (unit)", "PASS",
    "`tools/check_dag.py --unit M5` -> 'check_dag M5: PASS'. Every concept link in index/L01-L04 is own-definition or M1/M2/P0.1 closure (grep of data-concept).")
row("M5a-gate-check-projects", "2.6-projects-gate", "course/modules/M/M5/project.html", "PASS",
    "`tools/check_projects.py --unit M5` -> 'check_projects M5: PASS' (run for completeness; project is outside this slice).")
row("M5a-gate-run-labs", "2.5-labs", "tests/labs/M5/lab-M5-L01-1.py .. L04-1.py", "PASS",
    "`tools/run_labs.py --unit M5 --page L0n` -> 'run_labs M5: PASS (1/1)' for L01, L02, L03, L04. Page code equals twin; expected block equals twin output.")
row("M5a-twins-isolated", "2.5-labs", "tests/labs/M5/lab-M5-L0{1,2,3,4}-1.py", "PASS",
    "Each twin run as `python -I -W error <abs path>`: rc=0, stderr empty, stdout 17/7/5/11 lines (recorded in ledgers/M5/scripts/M5-a-r6/twin-L0n.out) matching the page expected blocks.")
row("M5a-gate-page-smoke", "2.5-2.9-render", "index.html, L01-L04", "PASS",
    "`tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04` -> PASS for all five pages, zero console errors reported, labs run in Pyodide (recorded in ledgers/M5/scripts/M5-a-r6/page_smoke.out).")
row("M5a-gate-ruff-mypy-pytest", "tooling", "tests/labs/M5/lab-M5-L0{1,2,3,4}-1.py", "PASS",
    "ruff check: All checks passed; ruff format --check: 4 files already formatted; mypy --no-incremental: Success, no issues in 4 files; pytest -k M5 (tests/test_labs.py): 13 passed.")
row("M5a-gate-verify-refs-offline", "2.1-citations", "references/references.json (keys cited by index/L01-L04: abbott2015understanding, rudin1976principles)", "PASS",
    "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'. The live Crossref run for M5 was not executed (see notes).")

# hub
row("M5a-hub-numbers", "2.2-numbers", P + "index.html:71,97,101,106,111,116,121", "PASS",
    "Recomputed: 7/9=77.78%, 8/9=88.89% (line 71); 1/1.05=0.9523809 vs 0.952381 diff 4.8e-8 < 0.001 (line 97); sum 2^k k=0..3 = 15; sum (1/2)^n n=0..4 = 31/16 = 1.9375; rung-2 bound 1/2*4=2. All match.")
row("M5a-hub-hours", "2.9-hours", P + "index.html:29,31,40,42,131", "PASS",
    "data-hours-lessons=104, data-hours-project=26; 26/130=20.0% (hours-split 80/20). Lesson data-hours: L01-L06 = 10, L07-L10 = 11 (grep over L01..L10): 6*10+4*11=104; 104+26=130=curriculum hours.")
row("M5a-hub-placement-crossrefs", "2.2-numbers/2.9-prose", P + "index.html:80,89,94,99,104,109,114,119,124", "PASS",
    "Each '(M1, Lesson n)' citation matches a real M1 lesson title: L01 negation of quantifiers; L02 contradiction and irrationality; L03 logarithm; L05 discount factor; L06 geometric sums (M1/L0n.html titles). M2 limit and derivative concepts exist (M2/L01, L02).")
row("M5a-hub-data-claims", "2.8-data", P + "index.html:37,159", "PASS",
    "No data-files attribute, no <svg>, no figures-L*.js and no currency or cents text in any M5 page (grep). 'SIMULATED' label appears where generated parameters are used (project.html:227; labs L08/L09 header 'Generated model parameters'), consistent with the hub's 'Data: none' claim.")
row("M5a-hub-prose-objectives-cards", "2.9-prose", P + "index.html:49-55,133-142", "PASS",
    "Each objective names a lesson whose content matches (L01 Cauchy/completeness; L02 series criterion; L03 delta and uniform continuity; L04 metric axioms; L07-L10 deferred to other slices). Card titles and descriptions match the L01-L04 h1s and section headings.")
row("M5a-hub-theorems-proved-L1-4", "2.4-mathematics", P + "index.html:168", "PASS",
    "Hub claim 'Every theorem in Lessons 1 to 4 is proved on its page' checked against each Theorem/Proposition/Lemma/Corollary block in L01-L04 (every block has a proof div; cited prior results exist).")
row("M5a-hub-P0.1-links", "2.9-dag", P + "index.html:35,64", "PASS",
    "evidence-grade and project-ladder ids exist in course/concepts.html (ids present); 'not yet released' text present in concepts.html (928 occurrences of the sentinel string, the P0.1 placeholder).")
row("M5a-hub-grade-legend-cosmetic", "2.9-prose", P + "L04.html:44-49 vs L01.html:43-48", "PASS",
    "Grade-legend wording differs (L04 'single study' = template text; L01-L03 'single study or lab result'). BLUEPRINT s3 C = 'single-sample evidence'; no rule fixes the legend wording. Recorded as an observation, not a defect.")

# L01
row("L01-M1-cor-2.6-citation", "2.4-citations", P + "L01.html:51,254,273,370,483", "PASS",
    "'M1, Lesson 2, Corollary 2.6' = 'no rational number has square 2' (course/modules/M/M1/L02.html:132), proved from Theorem 2.5 by contradiction (M1 L02 section on irrationality).")
row("L01-lab-1", "2.5-labs", P + "L01.html:144-231", "PASS",
    "run_labs and isolated twin run: output 13 of 13 (both counts), width 2/2^n exact, first step below 1/1000 = 11, step-12 bracket [181/128, 2897/2048]; predicted hypothesis text (line 146) matches output. Recomputed independently (numcheck_r6.py).")
row("L01-theorems-1.2-1.6-cor1.4-lemma1.5", "2.4-mathematics", P + "L01.html:66-135", "PASS",
    "Re-derived each proof: Archimedean by contradiction with sup; nested intervals via sup of left endpoints; Cor 1.4 via |s-t| <= b_n-a_n; Lemma 1.5 both cases; Thm 1.6 induction (width formula, midpoint in [a_n,b_n] so H3 applies). Hypotheses listed for each. No gap found.")
row("L01-prop-1.7", "2.4-mathematics", P + "L01.html:233-246", "PASS",
    "Case s^2<2: eps=min{1,(2-s^2)/(2s+2)} gives (s+eps)^2<2, contradicting upper bound. Case s^2>2: delta=(s^2-2)/(4s), t=s-delta satisfies t^2>=(s^2+2)/2>2, so t is a smaller upper bound. Both algebraic steps checked.")
row("L01-E1-E2-E3", "2.2-numbers", P + "L01.html:336-352", "PASS",
    "181^2=32761 < 32768=2*128^2; 2897^2=8392609 >= 8388608=2*2048^2; width 2897/2048-181/128=1/2048; first n with 2^(1-n)<1/1000 is 11; nesting at steps 4,5 ([11/8,3/2] contains [11/8,23/16]). All recomputed.")
row("L01-problems-mech-proof-research", "2.4-mathematics", P + "L01.html:284-380", "PASS",
    "M1 sup of (0,1)=1 verified; M2 max=sup and sup{1-1/n}=1; M3 two bisection steps match lab steps 1-2; P1 Cor 1.4; P2; P3 iff argument; R1 cube analogue (2^3=8 bound); R2; R3 infimum via -B. No error.")
row("L01-quiz", "2.7-quiz", P + "L01.html:400-479", "PASS",
    "Each keyed answer re-checked: Def 1.1 phrasing; S has no largest element; width after 3 steps = 0.25; first step 11; 3/2 upper bound and 7/5 in S; least n > 1000.5 is 1001; no rational lub; s^2=2; N unbounded by Thm 1.2; step-bracket relation. Distractors are false.")
row("L01-canon-misconceptions", "2.9-prose", P + "L01.html:250-276", "PASS",
    "Canon breaks: rational sup fails (proof of Prop 1.7 transported to Q); sup need not be in S; N unbounded. Misconceptions 1-3 consistent with Lemma 1.5, Prop 1.7 and Thm 1.6. Reasoning checked.")
row("L01-key-results-and-statements", "2.9-prose", P + "L01.html:383-398", "PASS",
    "Each key-results row matches its theorem number and grade T; the S_rat row's source wording (Prop 1.7 plus irrationality of sqrt2 from M1) matches the canon-break proof.")

# L02
row("L02-lab-1", "2.5-labs", P + "L02.html:209-292", "PASS",
    "Output: 200 of 200 gaps >= 1/2; min gap 1/2 at N=1 (recomputed H_2-H_1); 200 of 200 failing N; identity 1830 of 1830 (= sum_{j=1}^{60} j); first N=10; failing N = 0..9. Independent exact recomputation matches. Hypothesis text and interpretation claims match output and code.")
row("L02-prop-3.3-lemma-3.4-prop-3.5", "2.4-mathematics", P + "L02.html:168-207", "PASS",
    "Prop 3.3: each of the N terms 1/(N+1)..1/(2N) >= 1/(2N), sum >= 1/2. Lemma 3.4 telescopes; 0 < G_m-G_n < 1/2^n. Prop 3.5 both directions: N>=10 via 1/2^n<=1/2^10; N<=9 via pair (N,10) with difference >= 1/2^10.")
row("L02-thm-2.5-and-remark-2.6", "2.4-mathematics", P + "L02.html:124-145", "PASS",
    "Cauchy => bounded (Lemma 2.3); b_k decreasing with b_k >= -C; L = glb (Lemma 2.4); upper and lower estimates on s_n with eps/3 are correct; conclusion |s_n-L|<eps for n>=max(N,K). Remark 2.6 accurately says H2 is used through Lemma 2.4 and the suprema b_k.")
row("L02-R3-geometric-decay", "2.4-mathematics", P + "L02.html:418-421", "PASS",
    "Cites M1 Lesson 6 Theorem 2.2 (course/modules/M/M1/L06.html:97, closed form for q != 1): the hypothesis beta != 1 is stated and satisfied; (1+h)^N >= 1+Nh bound and N > c/(h(1-beta)eps) are correct.")
row("L02-canon-misconceptions-problems", "2.4-mathematics", P + "L02.html:294-391", "PASS",
    "Canon 1 (Cauchy rational bisection sequence with limit sup S) re-derived; canon 2 (1/n terms, harmonic); canon 3 (alternating sequence). Misconceptions 1-3 correct (sqrt n example checked). Problems M1-M3, P1-P3, E1-E3, R1-R3 re-derived.")
row("L02-quiz-and-key-results", "2.7-quiz", P + "L02.html:427-534", "PASS",
    "Keyed answers re-checked: H2-H1=1/2; G3=7/8; 1830; N=10; sqrt-n example unbounded; sup S rational-limit; Lesson 1 completeness hypothesis used by Thm 2.5. Key-results grades T with matching source numbers.")

# L03
row("L03-lab-1", "2.5-labs", P + "L03.html:106-167", "PASS",
    "Output: 401 of 401 bound holds; delta=1/50 admits 7 points (k=-3..3, recomputed); 7 of 7 good; first failing grid point 381/200 with |x^2-4|=14839/40000=0.370975; 29 failing points with |x-2|<1/10 (recomputed exactly). Hypothesis numbers match output.")
row("L03-prop-1.4-lemma-1.3-prop-1.5", "2.4-mathematics", P + "L03.html:66-104", "PASS",
    "Lemma 1.3: |x+2|<=|x-2|+4<=5 and |x^2-4|<=5|x-2| (checked). Prop 1.4 with delta=min{1,eps/5}: 5|x-2|<5delta<=eps (checked). Prop 1.5 uses min of deltas (checked). Prop 1.4's conclusion matches the Lab 1 check.")
row("L03-line-64-proof-description", "2.9-prose", P + "L03.html:64", "FAIL",
    "Sentence: 'The proof uses a bound on the factor |x+2|, proved first.' The proof of Proposition 1.4 (L03.html:87-89) invokes Lemma 1.3, a bound on |x^2-4|; the |x+2| <= 5 bound is an internal step of Lemma 1.3's proof (L03.html:76), not something Prop 1.4's proof uses directly.",
    "Replace with: 'The proof uses Lemma 1.3, a bound on |x^2 - 4| near 2, which is proved first.'")
row("L03-prop-2.1-2.2-3.1", "2.4-mathematics", P + "L03.html:171-213", "PASS",
    "Prop 2.1 both directions checked (sequence 1/n-type construction; negation gives delta=1/n sequence). Prop 2.2 threshold min{1,eps/5}. Prop 3.1: x=1/delta, y=x+delta/2 gives f(y)-f(x)>=1 (recomputed).")
row("L03-E1-E2-E3", "2.2-numbers", P + "L03.html:299-317", "PASS",
    "E1: 5|x-2|=0.475 and |x^2-4|=0.370975 (recomputed). E2: k=-3..3 gives the 7 points listed (recomputed). E3: positive side k=5..19 (15 values, k=4 gives 16.08 and k=5 gives 20.125), negative side j=6..19 (14 values, j=5 gives 19.875, j=6 gives 23.82); total 29 (recomputed by script).")
row("L03-R1-R2-R3", "2.4-mathematics", P + "L03.html:323-343", "PASS",
    "R1: x=3 gives |x^2-4|=5 with |x-2|=1, so 5 is sharp. R2: x=2+h with 0<h<1/200 is off-grid, g(x)=x^2+1 gives |g(x)-g(2)|>=1 (checked). R3: |max{a,b}-max{c,d}| <= max{|a-c|,|b-d|} proved case by case; continuity via min of deltas.")
row("L03-canon-misconceptions", "2.4-mathematics", P + "L03.html:215-240", "PASS",
    "Canon 1: point 2 delta cannot serve all points. Canon 2: f(1)=5 example with x=1+min{delta,1}/2 gives |x-5|>=3.5 (checked). Misconception 1 numbers 10.1 (|x^2-100|=2.01, delta=1/5) checked. Misconception 3: y_n=2/(2n+1) argument and Prop 2.1 use correct.")
row("L03-quiz", "2.7-quiz", P + "L03.html:364-443", "PASS",
    "Keyed answers re-checked: eps-delta form; delta=1/50=0.02; delta depends on eps; f(1)=5 not continuous; c=5; sequential needs every sequence; x^2 not uniformly continuous; 29; 401; Lemma 1.3 |x+2|<=5.")

# L04
row("L04-lab-1", "2.5-labs", P + "L04.html:103-210", "PASS",
    "run_labs and isolated twin: Part A euclidean 25/625/15625, all failures 0; Part B sup 27/729/19683, all failures 0; Part C squared 3/9/27, triangle failures 2 at (0,1,2) and (2,1,0); d(0,2)=4, d(0,1)+d(1,2)=2. Hypothesis (line 105) matches output. Enumeration re-checked.")
row("L04-quiz-q5-distractor", "2.7-quiz", P + "L04.html:425", "FAIL",
    "Option 1 of the 'Which triple of points shows (x-y)^2 violates the triangle inequality?' question reads '0 and 1, with z=2, because d(0,1) is small'. That names the triple (x,y,z)=(0,1,2), which is the correct option's triple (option 2 at L04.html:426, d(0,2)=4 > d(0,1)+d(1,2)=2). Two options name the same violating triple, so the item has no single answer.",
    "Replace option 1 with a triple that does not violate M3, for example '(x,y,z)=(0,2,1): d(0,1)=1 <= d(0,2)+d(2,1)=5'.")
row("L04-prop-1.4-lagrange", "2.4-mathematics", P + "L04.html:79-96", "PASS",
    "Lagrange identity expansion checked: (u1^2+u2^2)(v1^2+v2^2)-(u1v1+u2v2)^2 = (u1v2-u2v1)^2. Cauchy-Schwarz step and square-root steps are valid.")
row("L04-example-1.5-prop-1.7", "2.4-mathematics", P + "L04.html:98-236", "PASS",
    "Discrete metric M3 cases exhaustive (x=z; y=x or y=z; y distinct). Prop 1.7: finiteness via 2M bound; M1 from nonnegativity of sup; M3 via sup of each term. Checked.")
row("L04-remark-2.2-prop-2.1", "2.4-mathematics", P + "L04.html:238-255", "PASS",
    "Remark 2.2: (0,1] not open at 1 (point 1+r/2); discrete metric makes every subset open (balls B(x,1/2)={x}). Prop 2.1 triangle argument with s=r-d(x,y) checked.")
row("L04-section-3-props", "2.4-mathematics", P + "L04.html:257-297", "PASS",
    "Prop 3.3 (eps/2 argument), Prop 3.4 (coordinate Cauchy, d_2^2 < eps^2/4+eps^2/4 < eps^2), Example 3.6 via F4-F6 (|x| <= |x-1/n|+|1/n| -> 0 forces x=0 not in (0,1]). Each step checked.")
row("L04-section-4-props", "2.4-mathematics", P + "L04.html:299-320", "PASS",
    "Prop 4.2 both directions (negation gives z_n with d(x,z_n)<1/n and d(f(x),f(z_n))>=eps). Example 4.3 |phi(x)-phi(z)|<=d(x,z) via M2 and M3, then delta=eps.")
row("L04-F-facts-section-1", "2.4-mathematics", P + "L04.html:56", "PASS",
    "F1-F6 are true (F5 cites L02 Problem P2, which exists at L02.html:361-366; F6 argument: c<=t_n, t_n<eps, c=0 via F3). Problem M1 cited for 1/n->0 exists (L02.html:328-333).")
row("L04-canon-misconceptions", "2.9-prose", P + "L04.html:322-338", "PASS",
    "Canon breaks 1-4 and misconceptions 1-3 checked: |x^2-y^2| has d(1,-1)=0 (pseudometric); unbounded f excluded from B(R); (0,1] neither open nor closed (min(r/2,1) argument). Statements agree with examples and lab Part C.")
row("L04-problems", "2.4-mathematics", P + "L04.html:340-374", "PASS",
    "Mechanics 1-3 (d_2=5; finite metric six cases; sup=1/4 at x=1/2); Proofs 1-3 (pseudometric, min(|x-y|,1), pointwise from uniform); Empirical 1-3 (15625 triples; the 2 failing triples in Part C enumerated; 19683 and d_inf=2); Research 1-3 (phi subadditive, closed in complete, constants complete). All re-derived.")
row("L04-key-results", "2.9-prose", P + "L04.html:376-391", "PASS",
    "Each key-results row matches the corresponding proposition or lab part; grades T.")

fragment = {
    "unit": "M5",
    "slice": "a",
    "round": 6,
    "verifier": "independent Haiku verifier (round 6); not the builder",
    "pin": "44f1eb6a417ce687a9b88c7ee917e72566b29892",
    "base": "none: /Users/billyribeiro/.fanout/frags/B-M5-a.round5.json does not exist, so no carried PASS rows; every row re-verified from the pin",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB6-M5-a",
    "scratch": "/tmp/m5a-r6",
    "verified_at": "2026-10-29T00:49:13Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/M/M5/index.html, L01.html, L02.html, L03.html, L04.html and tests/labs/M5/lab-M5-L01-1.py..L04-1.py (pin 44f1eb6).",
        "Read in full: index.html (174 lines), L01 (495), L02 (551), L03 (460), L04 (480), and the four twins; the plan plans/M5-build-plan.md and VERIFIER_RULES consulted.",
        "Not checked: cards.json entries for L01-L04 (outside this slice; the quiz data-cards link is taken as given); the live Crossref/verify_refs run for M5 (only --offline was run); run_graders and mutate_graders (project slice, not in this slice); page_smoke visual look at 360px beyond the tool's own checks.",
        "Delta: no round-5 fragment exists at the stated path, so the delta from the previous pin was not computed; the whole slice was read instead of a hunk diff.",
        "Equivalent-mutant and alternative-implementation rows do not apply to lab-only slices.",
        "Observation only (not a row): L04 quiz line 425 is the only quiz defect found; L01-L03 grade-legend wording differs from the lesson template (cosmetic)."
    ],
    "summary": "M5-a round 6: 2 FAIL rows (L03-line-64 wording; L04 quiz distractor duplicates a valid violating triple); all mechanical gates PASS; all lab outputs and lesson mathematics re-derived."
}
json.dump(fragment, open("ledgers/M5/M5-a.json", "w"), indent=2, ensure_ascii=False)
print("rows", len(rows), "fail", sum(r["status"] != "PASS" for r in rows))
