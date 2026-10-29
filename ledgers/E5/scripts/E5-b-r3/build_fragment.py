import json, sys
root = "/Users/billyribeiro/.fanout/wt/verifyC3-E5-b"
S = "ledgers/E5/scripts/E5-b-r3/"
rows = []
def R(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

R("E5b-inventory", "2.9 structure", "course/modules/E/E5/L04.html, L05.html, L06.html; tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py",
  "PASS", "Read in full, line by line (L04 1-579, L05 1-498, L06 1-538; twins 81-154 lines each). Prior round fragment C-E5-b.round2.json is absent at the given path (/Users/billyribeiro/.fanout/frags/), so no PASS row is carried; every row was re-verified from the pin ccfdf4c.")
R("E5b-cmd-check_pages", "2.9 structure", "tools/check_pages.py --unit E5", "PASS",
  "Run at ccfdf4c: output 'check_pages E5: PASS'. Covers hub, lesson minimum counts, hours split, banned strings and lab ids for L04-L06.")
R("E5b-cmd-check_dag", "2.9 DAG", "tools/check_dag.py --unit E5", "PASS",
  "Run at ccfdf4c: output 'check_dag E5: PASS'. Concept links in L04-L06 resolve: #def-business-cycle, #def-is-lm-model, L04.html#def-is-lm-model, L05.html#def-ad-as-model, #def-phillips-curve, #def-natural-rate-of-unemployment (anchor checks in the round-3 inline script, all True). Concepts linked from outside the lesson set are comparative-statics and competitive-equilibrium (E1, inside the closure {E1, M1, M2, P0.1}).")
R("E5b-cmd-run_labs", "2.5 labs", "tools/run_labs.py --unit E5 --page L04 / --page L05 / --page L06", "PASS",
  "Each run: 'run_labs E5: PASS (1/1)'. Page code is byte-identical to its twin and the expected block matches stdout under the page rule.")
R("E5b-lab-twin-isolated", "2.5 labs", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS",
  "Each twin run alone: python -I -W error <twin>, cwd /tmp, exit 0, stderr 0 bytes. Script " + S + "check_labs_b.py output: 'L04 ... page_code_equals_twin=True expected_equals_output=True', same for L05 and L06, 'ALL_OK'.")
R("E5b-lab-lint-types", "2.5 labs", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS",
  "ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental: 'Success: no issues found in 3 source files'.")
R("E5b-lab-pytest", "2.5 labs", "tests/test_labs.py -k E5", "PASS", "pytest tests/test_labs.py -q -k E5: 11 passed (lab harness over every E5 lab).")
R("E5b-lab-page_smoke", "2.9 page smoke", "tools/page_smoke.py --unit E5 --pages L04 L05 L06", "PASS",
  "Run at ccfdf4c (alone): 'page_smoke modules/E/E5/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke E5: PASS'. Zero console errors, no unrendered math, no horizontal scroll at 360 px, figures sweep (none on these pages).")
R("E5b-cit-hicks", "2.1 citations", "course/modules/E/E5/L04.html:566 (References), key hicks1937mr", "PASS",
  "Paper-level mention only; the page attributes no result to it and says the lesson has not read it (L04.html:566). Live: tools/verify_refs.py --unit E5 -> 'live re-verification of E5: 4 of 560 entries, 0 problems' (run at ccfdf4c). Plan §7.1 permits paper level.")
R("E5b-cit-L05-L06-none", "2.1 citations", "course/modules/E/E5/L05.html:485; L06.html:525", "PASS",
  "No outside result is attributed on L05 or L06; both References sections say so (grep of data-cite in E5 lesson pages: 0 hits).")
R("E5b-cit-phelps-plan", "2.1 citations / plan §3 L06 and §7.1", "course/modules/E/E5/L06.html:525", "FAIL",
  "plans/E5-build-plan.md §3 (L06) and §7.1 require phelps1968money 'cited at paper level for the expectations-augmented construction'. L06.html:525 says the key is not cited, because the lesson has not read the paper. L04 names hicks1937mr at paper level on the same basis, so the two lessons are inconsistent. No data-cite on L06.",
  "Either name phelps1968money at paper level in L06 References (no locator, no result attributed; plan §7.1 'Use in E5' wording) or record an architect decision in the plan that L06 cites nothing.")
R("E5b-num-L04", "2.2 numbers", "course/modules/E/E5/L04.html prose and Lab 1 expected block", "PASS",
  "Re-derived by " + S + "rederive_b.py (Fraction arithmetic, independent of the twin): A=3, D=5/4, Y*=28/5, i*=4/5, IS and LM residuals 0, h/D=4/5, b/D=8/5, -(1-c)/D=-1/5, dY=2/25 and di=1/25 for G 1->11/10, di=2/5 for G 1->2, benchmark 4, b=0 multiplier 4, E1 ratio 1/2, E3 share 1/5, M1 D=3 Y=14/3 i=5/6, M2 2/3 and 1/3, M3 2/3 and -1/6. All 'ALL_OK'.")
R("E5b-num-L05", "2.2 numbers", "course/modules/E/E5/L05.html prose and Lab 1 expected block", "PASS",
  "rederive_b.py: P*=6/5, Y*=1040, dP=1/10, dY=20, long-run prices 8/5 and 19/10, Part D shares 1/3,1/2,2/3,4/5,8/9 with dY 10,15,20,24,80/3, E1 4/5 and 24, E2 increment 8/3, R2 P*=3/2 Y*=1040, M1 P*=21/20 Y*=995, M2 3/4 and 1/5, M3 7/5, misconception 1060 and demand 1000 at P=1.6. All 'ALL_OK'. Expected block values 1.200000, 1040.000000, 0.666667, 0.003333 match the exact fractions rounded half-even.")
R("E5b-num-L06", "2.2 numbers", "course/modules/E/E5/L06.html prose and Lab 1 expected block", "PASS",
  "rederive_b.py: beta=5/6, Part A P1=613/500 and pi=13/600=0.021667 (both forms), 4% change 1/120=0.008333, 3% change 1/60=0.016667, R1 ratio 6/5, R2 u=31/500 (6.2%), M1 beta 1/2 pi 3/100, M2 beta 4/5 pi 0.048, M3 pi 1/200 (fall 0.015), E3 period-1 change -29/6000=-0.004833 and 5.5% row -1/240=-0.004167, Part B t=1 pi=151/6000 (0.025167). Part B path: I recomputed sign counts from the printed table (9 positive gaps: periods 1,2,3,4,5,7,8,11,12; 3 negative: 6,9,10) and they match E2. All 'ALL_OK'.")
R("E5b-prose-scope", "2.9 scope words", "L04-L06 'every', 'all', 'only', 'exactly', 'same', 'any'", "PASS",
  "Each scope word checked against a derivation or a lab line: L04 'exactly one equilibrium' (Prop 3.2), 'only interest rate' (A3 model), 'every value is an exact Fraction' (lab code), L05 'every positive shift' (Prop 2.2, sign of Δa/(η+ν)), 'every value of a' (Prop 3.1), L06 'exactly when' (Cor 3.2), 'no period' (Part B counts). The 'vacuously' sentence (L06 interpretation) is stated honestly.")
R("E5b-math-L04", "2.4 mathematics", "L04.html Derivation 2.2, Prop 3.2, Prop 4.2, Prop 4.3, Remark 4.4-4.5, P2", "PASS",
  "Derivation 2.2 re-derived by hand: (1-c)Y+bi=A. Prop 3.2 determinant -D, Cramer formulas, direct check of both relations (each bracket simplifies to A and mbar, verified by the rederive script). Prop 4.2 derivatives: h/D, b/D, -ch/D, d/D, -(1-c)/D. Prop 4.3: h/D <= 1/(1-c) iff bd >= 0 (h(1-c) <= D). Assumptions A1-A4 are stated before each result. Hypotheses complete.")
R("E5b-math-L05", "2.4 mathematics", "L05.html Prop 2.1, Prop 2.2, Remark 2.3, Prop 3.1, Remark 3.2, Canon-break 2 (A3 counterfactual)", "PASS",
  "Prop 2.1 solved: (η+ν)P = a-Ȳ+νP^e, unique since η+ν>0. Prop 2.2: ΔP=Δa/(η+ν), ΔY=νΔa/(η+ν), bounds via η>0, ν>0. Prop 3.1 fixed-point argument re-derived. Non-linear extension L05-R1 proof checked: H strictly decreasing, limits at 0+ and infinity, IVT, uniqueness. Assumptions A1-A3 stated.")
R("E5b-math-L06", "2.4 mathematics", "L06.html Prop 2.1, Prop 3.1, Cor 3.2, Remark 2.2, Remark 3.3, L06-R2", "PASS",
  "Prop 2.1: from A1 P_t-P^e_t=(Y_t-Ȳ)/ν and A2, pi_t = pi^e_t - (κ/(νP_{t-1}))(u_t-u^n) re-derived with (P^e_t-P_{t-1})/P_{t-1}=pi^e_t. Prop 3.1 and Cor 3.2 follow (β>0). L06-R2 extension: u=u^n+v/β=0.062 re-derived. Hypotheses (ν>0, κ>0, P_{t-1}>0) stated.")
R("E5b-notation", "2.4 notation", "L04-L06 symbols vs notation/notation.json (8 symbols, 26 macros)", "PASS",
  "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and the macros \\E, \\R, etc. L04-L06 use none of the registered symbols with another meaning: no bare T (grade badges only), no R_f or R^*, no Phi, no gamma. Letters D, A, c, b, d, h, G, Tax, m-bar, a, eta, nu, kappa, beta, pi, u, v are local and defined on first use.")
R("E5b-define-L06-natural-rate", "2.9 define-before-use", "course/modules/E/E5/L06.html:68-70 (Assumption A2) vs Definition 1.2 at :83-85", "FAIL",
  "A2 uses the term 'natural rate of unemployment' and 'u^n' before Definition 1.2 defines it ('the natural rate of unemployment defined in Definition 1.2'). Ordering defect (plan §2.1 item 5: each concept defined where it is first used). Definition 1.2 depends on A2, so the definition cannot simply move up.",
  "In A2 say only 'u^n is a parameter of the model (Definition 1.2 below gives its meaning)' and do not name the 'natural rate' term until Definition 1.2, or define the term in one plain <dfn> at the first use in A2.")
R("E5b-title-L04", "2.9 hub titles (plan §2.2 'Hub lesson titles match each lesson's <h1>')", "course/modules/E/E5/index.html:149 vs L04.html:36", "FAIL",
  "Hub card title 'Business Cycles and IS–LM' differs from L04 h1 'Business cycles and the IS–LM model' (L04.html:36). The L05 and L06 hub titles match their h1s (index.html:150-151). check_pages does not compare these strings, so the gate does not catch it.",
  "Set index.html:149 card-title to 'Business cycles and the IS–LM model' (the hub is slice a's file; reported, not edited).")
R("E5b-nav", "2.9 structure", "L03.html -> L04.html -> L05.html -> L06.html -> L07.html lesson-nav labels", "PASS",
  "Each Previous/Next label equals the target h1: L04 prev 'L03 · The Solow growth model' (L03 h1 match), L04 next 'L05 · Aggregate Demand and Aggregate Supply', L05 prev 'L04 · Business cycles and the IS–LM model', L05 next 'L06 · The Phillips Curve and the Natural Rate', L06 next 'L07 · Central-Bank Policy and the Taylor Rule' (L07 h1 match).")
R("E5b-struct-L04-L06", "2.9 structure (BUILDER_RULES §4.2)", "L04-L06 section order, minimum counts", "PASS",
  "Per page: why-it-matters 91/105/103 words (limit 120); §1-§4 content, canon-breaks, misconceptions (3 each), problem set with 3 problems in each of Mechanics, Proof, Empirical and Research (counted per tier), key-results table, 10-item retrieval quiz with an explanation on each item, references section; data-hours=10.")
R("E5b-banned-process", "2.9 banned phrases and process words", "L04-L06 full text", "PASS",
  "grep for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', ellipsis, 'builder', 'verifier', 'round', 'REQUESTS': zero hits in learner text (the 'rounded' hits are the rounding convention). 'registry' appears in learner text, which AC1 pages also do (precedent).")
R("E5b-grades", "2.3 grades", "L04 Prop 3.2, 4.2, 4.3; L05 Prop 2.1, 2.2, 3.1; L06 Prop 2.1, 3.1, Cor 3.2; key-results tables", "PASS",
  "Every theorem block is data-grade T and is a derivation on the page with its assumptions. The one non-T row (L06 key result, grade C) is the seeded SIMULATED path, labelled as one generated path with no claim about an economy. No B or C claim about an empirical slope or multiplier appears on these pages.")
R("E5b-labs-simulated", "2.5 / BUILDER §1.7 SIMULATED label", "lab-E5-L06-1 hypothesis and docstring; L04/L05 labs", "PASS",
  "lab-E5-L06-1 carries the SIMULATED label in its hypothesis and docstring (seed 20261028, random.Random). L04 and L05 are exact closed-form labs on illustrative inputs; each states 'not data' and no data-files attribute is used.")
R("E5b-problems-quiz", "2.6-style problem and quiz checks", "L04-L06 problem sets, retrieval quiz explanations", "PASS",
  "Solutions re-derived line by line (L04 M1-M3, P1-P3, E1-E3, R1-R3; L05 M1-M3, P1-P3, E1-E3, R1-R3; L06 M1-M3, P1-P3, E1-E3, R1-R3). Quiz numeric answers 5.6, 0.8, 4, -0.2 (L04); 1040, 20, 0.1, 0.3, 1.2 (L05 checked); 1, 0.008333, 0.021667, 0.048, 1 (L06). Each explanation agrees with its lesson and lab line.")
R("E5b-interp-labs", "2.2 lab statements vs output", "L04/L05/L06 'interpretation' paragraphs and hypotheses", "PASS",
  "Each printed value quoted in prose matches the expected block exactly (e.g. L04 'multiplier_below_cross True', L05 'exact_match True', L06 'identity_every_period True', 'no_change_only_at_natural_rate True' with the vacuity caveat stated).")

frag = {
  "unit": "E5",
  "slice": "E5-b",
  "round": 3,
  "verifier": "Haiku independent verifier, E5 slice b round 3 (did not build E5)",
  "pin": "ccfdf4c",
  "base": "none readable: round-2 fragment absent at /Users/billyribeiro/.fanout/frags/C-E5-b.round2.json; all rows re-verified",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-E5-b (detached at ccfdf4c, .venv symlinked)",
  "scratch": "/tmp (E5b_*.out, E5b_smoke.out, E5b_refs.out)",
  "verified_at": "2026-10-28",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [
    "phelps1968money: plan §3/§7.1 asks for paper-level citation in L06; page does not cite it (E5b-cit-phelps-plan). Registry record itself was not re-read here; live verify_refs --unit E5 reported 0 problems over 4 entries."
  ],
  "freshness_flags": [],
  "notes": [
    "Slice is lessons only (rubric unit, no autograder): no mutants required; mutate_graders is not run for E5 (plan §10).",
    "Non-PASS rows: E5b-cit-phelps-plan (plan conformance, L06 citation), E5b-define-L06-natural-rate (term used before definition, L06 A2), E5b-title-L04 (hub card title in slice a's file index.html:149; reported, not edited).",
    "Not checked: the hub, cards.json, the project and the L01-L03 / L07-L08 pages are other slices. Pages were not compared against the Pyodide runtime version beyond page_smoke's runs; no network other than the Crossref/verify_refs live run.",
    "Scripts kept under ledgers/E5/scripts/E5-b-r3/: check_labs_b.py (page code vs twin, expected vs output), rederive_b.py (all prose numbers in L04-L06 re-derived in Fraction), build_fragment.py (writes this fragment)."
  ],
  "summary": {}
}
frag["summary"] = {
  "rows_total": len(rows),
  "pass": sum(r["status"] == "PASS" for r in rows),
  "fail": sum(r["status"] == "FAIL" for r in rows),
  "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
  "mutants_killed": "0/0 (lesson slice, rubric unit)"
}
out = f"{root}/ledgers/E5/E5-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, frag["summary"])
