"""Writes the round-2 fragment for E2 slice b (L04-L06). Rows carry evidence read on pin e22feb3."""
import json
import sys

S = "PASS"; X = "FAIL"
R = []
def row(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

SCRIPT = "ledgers/E2/scripts/E2-b-r2/recompute_slice_b_r2.py"
TWIN_RUN = "tools/run_labs.py --unit E2 --page L04/L05/L06 -> 'run_labs E2: PASS (1/1)' each"

row("E2-b-cmd-check-pages", "2.9-structure", "course/modules/E/E2/index.html; L04.html; L05.html; L06.html",
    S, "cd /tmp/verifyC2-E2-b && .venv/bin/python tools/check_pages.py --unit E2 -> 'check_pages E2: PASS' (run this round on e22feb3).")
row("E2-b-cmd-check-dag", "DAG", "course/modules/E/E2/L04.html; L05.html; L06.html; curriculum/curriculum.json",
    S, "tools/check_dag.py --unit E2 -> 'check_dag E2: PASS'. Link owners on the three pages: L04 adverse-selection (L03 anchor), signaling (own); L05 adverse-selection, signaling (L04), screening (own); L06 expectation (M4, in closure), moral-hazard (own), screening (L05). Plain-prose uses of outside-closure words (concave, expected utility, risk neutral) are unlinked, as the Architect decisions default allows.")
row("E2-b-cmd-run-labs", "2.5-labs", "tests/labs/E2/lab-E2-L04-1.py; lab-E2-L05-1.py; lab-E2-L06-1.py",
    S, TWIN_RUN + " (this round).")
row("E2-b-cmd-twins-isolated", "2.5-labs", "tests/labs/E2/lab-E2-L04-1.py; lab-E2-L05-1.py; lab-E2-L06-1.py; course/modules/E/E2/L04.html; L05.html; L06.html",
    S, "python -I -W error on each twin: rc 0, stderr 0 bytes, 20 stdout lines each. Stdout equals the page's <pre class=\"expected\"> block exactly (checked by script-free comparison, recorded in the run). The code in each page's <code data-run> block equals the twin file (strip-and-compare: True for all three). Twin has no __main__ guard and ends with main().")
row("E2-b-cmd-page-smoke", "2.5-labs", "course/modules/E/E2/L04.html; L05.html; L06.html",
    S, ".venv/bin/python tools/page_smoke.py --unit E2 --pages L04 L05 L06 -> 'page_smoke modules/E/E2/L04.html: PASS', L05 PASS, L06 PASS; lab timings 0.0 s, 0.1 s, 0.0 s; 'page_smoke E2: PASS' (exit 0).")
row("E2-b-cmd-ruff-mypy-pytest", "2.5-tooling", "tests/labs/E2/lab-E2-L04-1.py; lab-E2-L05-1.py; lab-E2-L06-1.py; tests/test_labs.py",
    S, "ruff check on the three twins: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files'; .venv/bin/pytest tests/test_labs.py -q -k E2: 15 passed.")
row("E2-b-ref-live", "2.1-citations", "references/references.json (keys spence1973job, rothschild1976equilibrium, holmstrom1979moral among the E2 keys)",
    S, ".venv/bin/python tools/verify_refs.py --unit E2 -> 'live re-verification of E2: 8 of 560 entries, 0 problems'.")
row("E2-b-ref-offline", "2.1-citations", "references/references.json", S,
    ".venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'. references/ unchanged between 55b5634 and e22feb3 (git diff --stat empty).")
row("E2-b-cit-spence-topic", "2.1-citations", "course/modules/E/E2/L04.html section 4 (span data-cite=spence1973job)",
    S, "Registry read: title 'Job Market Signaling', Spence, QJE 87(3), year 1973, DOI 10.2307/1882010. Page: cited 'for the topic of signaling by its title, year and venue only; no page or result of that paper is used'. Title matches topic. Source not read (JSTOR); the claim is limited to the title.")
row("E2-b-cit-spence-result", "2.1-citations", "course/modules/E/E2/L04.html key-results (3 rows, all T); course/modules/E/E2/cards.json E2-c048",
    S, "The round-1 C row sourced to Spence is gone: key-results rows 1-3 are all T and cite Proposition 1.3 and Lab 1. Card E2-c048 now says 'cited by title, year and venue only. No page or result of that paper is used.' Agrees with section 4.")
row("E2-b-cit-rothschild", "2.1-citations", "course/modules/E/E2/cards.json E2-c060 (front); course/modules/E/E2/L05.html section 4",
    X, "Registry: 'Equilibrium in Competitive Insurance Markets: An Essay on the Economics of Imperfect Information', QJE 90(4), 1976. Section 4 of L05 (current) says the paper is cited 'by its title, year and venue only, for competitive insurance markets under imperfect information', which the registry title supports; the short title drops the subtitle without an ellipsis, a presentation point that is not a factual error. Card E2-c060 front still reads 'Which source does the lesson cite for screening in a competitive market', attributing screening to the paper. 'screening' is not in the title and not in section 4; the card's attribution is unread.",
    "Change the front of E2-c060 to 'Which source does the lesson cite for competitive insurance markets under imperfect information, and what does it attribute to it?' (matching L05 section 4), and give the full registry title or add the subtitle in section 4.")
row("E2-b-cit-holmstrom-topic", "2.1-citations", "course/modules/E/E2/L06.html section 4; key-results; card E2-c072",
    S, "Registry: 'Moral Hazard and Observability', Holmstrom, Bell Journal of Economics 10(1), 1979, DOI 10.2307/3003320. Page cites title, year and venue only; card E2-c072 says no result or page used. Consistent.")
row("E2-b-num-L04", "2.2-numbers", "course/modules/E/E2/L04.html Remark 1.4, Remark 2.1, Lab 1 Part B table, Misconceptions 3, Problems L04-m1..m3, e1..e3, quiz",
    S, "Recomputed exactly in " + SCRIPT + ": Delta = 2,000,000; bounds 2 and 4; enumerated separating thresholds [2,3,4]; high utility 5,000,000 at t=2, 4,000,000 at t=4; low utility 5,000,000 at e=1 under t=1; m1 upper bound 8; p1 bounds 3/2 and 3; e1 upper bound 5; e2 bounds 1 and 2. All whole-cent values are exact integers (no rounding).")
row("E2-b-num-L05-base", "2.2-numbers", "course/modules/E/E2/L05.html Remark 1.5, Remark 2.1, Misconceptions 1-3, key-results row 3, quiz",
    S, "Recomputed exactly in " + SCRIPT + ": q_L* = 2000, q_H = 6000, m_L = 6,000,000, m_H = 30,000,000, U_H = 6,000,000; menu profit 6,000,000; first best 7,875,000; gap 1,875,000; grid argmax 2000 (low, q_H=6000); 2-D grid optimum (2000, 6000).")
row("E2-b-num-L05-percent", "2.2-numbers", "course/modules/E/E2/L05.html problem L05-e3",
    S, "1,875,000 / 7,875,000 = 23.8095..% -> displayed 23.81% with base stated as first-best profit (recomputed, round(,2)=23.81). 7,875,000 / 6,000,000 - 1 = 31.25% with base the menu profit (stated). Both display bases are stated.")
row("E2-b-num-L05-variant-e1", "2.2-numbers", "course/modules/E/E2/L05.html problem L05-e1 (solution)",
    S, "Variant run: copy of tests/labs/E2/lab-E2-L05-1.py with P_LOW=2/3, P_HIGH=1/3 prints Part B best low quantity 1500, profit 6750000; Part D (menu fixed at 2000) prints menu profit 6666667 and gap 2333333. The solution says the menu values are at q_L=2,000 and gives the best-menu profit 6,750,000 and gap 2,250,000 at q_L=1,500 (recomputed exactly; 2000 gap = 7,000,000/3 = 2,333,333.33). Agrees with the printed output.")
row("E2-b-num-L05-remark-1.5-numbers", "2.2-numbers", "course/modules/E/E2/L05.html Remark 1.5 (line ~118 in the text render)",
    S, "Recomputed in " + SCRIPT + ": transfers, U_H = 6,000,000 cents, low-type rent 0, first-best low quantity 3000 units. Lab 1 Part A prints m_L = 6000000, m_H = 30000000, information rent 6000000.")
row("E2-b-num-L06", "2.2-numbers", "course/modules/E/E2/L06.html Proposition 1.3, Remark 1.4, Remark 2.1, Misconceptions, problems m1-m3, e1-e3, quiz",
    S, "Recomputed in " + SCRIPT + ": E_H 750,000; E_L 250,000; first best 650,000; best grid share 1/5 with profit 600,000; profit at 0.30 = 525,000; agency cost 50,000; profit + agent utility = E_H - c_H; m1 utilities 87,500 and 62,500, profit 562,500; m2 utility 0 at 2/15; m3 profit 590,000; p1 witness utilities -725,000 and -875,000; e1 threshold 3/10 and profit 525,000; e2 threshold 1/6, profit 2,000,000/3 (rounds to 666,667), first best 700,000. Remark 1.4 profit 650,000 at beta = 1/5, 1/2, 1.")
row("E2-b-grade-L04", "2.3-grades", "course/modules/E/E2/L04.html Proposition 1.3 (T); Remark 2.1; key-results rows 1-3 (T)",
    S, "Proposition 1.3 is a complete iff proof: (IC-L) iff c_L t >= Delta (low-type proof, both directions), (IC-H) iff y_H - c_H t >= y_L (high-type proof, sup over e<t attained at e=0), combined with t>=1 for separation. Remark 2.2 (on-path comparisons) supports 'under any off-path wages'. Grade T is correct; the enumeration rows in Lab 1 are cited as 'checks', not as the proof.")
row("E2-b-grade-L05", "2.3-grades", "course/modules/E/E2/L05.html Lemma 1.3 (T), Proposition 1.4 (T), key-results rows 1-3 (T)",
    S, "Proposition 1.4 now states Assumptions 1 to 6 and the hypothesis theta_L - (p_H/p_L)(theta_H - theta_L) >= 0. Step 1 uses Lemma 1.3 and Assumption 6; Step 2 uses q_L >= 0 (Assumption 6); Step 3 checks feasibility incl. both participation constraints and IC-L. Grade T is supported by the stated hypotheses. Research problem L05-r1 is ungraded and separately FAILs (E2-b-math-L05-ex-r1).")
row("E2-b-grade-L06", "2.3-grades", "course/modules/E/E2/L06.html Lemma 1.2 (T), Proposition 1.3 (T), key-results rows 1-3",
    S, "Lemma 1.2 proof is an identity (alpha + beta x at x=0 and X-bar, expected payment alpha + beta E_a). Proposition 1.3 is T: its incentive, bound, attainment, low-effort and refusal cases are all re-derived; it uses Assumptions 1 to 4, all of which are listed in the statement.")
row("E2-b-math-L04-prop1.3", "2.4-math", "course/modules/E/E2/L04.html Proposition 1.3 and proof (~lines 44-50 of the text render)",
    S, "Re-derived by hand and in " + SCRIPT + ": (IC-L) iff c_L t >= Delta; (IC-H) iff y_H - c_H t >= y_L iff t <= Delta/c_H; t >= 1 makes the signals differ. Statement and proof agree.")
row("E2-b-math-L04-off-path", "2.4-math", "course/modules/E/E2/L04.html Assumption 3, Remark 2.2, quiz item (explanation)",
    S, "Round-1 defect fixed: Assumption 3 now says e=0 is on path (the low type's choice), off-path levels are 0<e<t and e>t, and Remark 2.2 argues the necessary part under any off-path wages using only on-path wages at e=0 and e=t. Re-derived: IC-H uses the wage at 0 (y_L, on path) and IC-L uses the wage at t (y_H, on path); so the bound [Delta/c_L, Delta/c_H] holds under any off-path rule. Quiz explanation agrees.")
row("E2-b-math-L05-lemma1.3", "2.4-math", "course/modules/E/E2/L05.html Lemma 1.3 and proof",
    S, "Adding (IC-L) and (IC-H) gives (theta_H - theta_L)(q_H - q_L) >= 0; (IC-H) gives U_H >= U_L + (theta_H - theta_L) q_L. Re-derived; uses Assumptions 1 and 3 only (as stated).")
row("E2-b-math-L05-prop1.4", "2.4-math", "course/modules/E/E2/L05.html Proposition 1.4 statement and proof Steps 1-3",
    S, "Round-1 defect fixed: the statement adds Assumption 6 (q_L, q_H >= 0). Step 1 (raise both transfers by U_L; new U_H = U_H - U_L >= (theta_H - theta_L) q_L >= 0 by Lemma 1.3 and Assumption 6), Step 2 (raise m_H by delta; IC-L holds because theta_L q_H - m_H' = (theta_H - theta_L)(q_L - q_H) <= 0 = U_L), Step 3 (Hessian diag(-p_L, -p_H); FOC gives q_H = theta_H, q_L = theta_L - (p_H/p_L)(theta_H - theta_L); feasibility incl. participation and IC-L; stationary point of concave function is global max). Each step re-derived. Proposition holds as stated.")
row("E2-b-math-L05-P2", "2.4-math", "course/modules/E/E2/L05.html problem L05-p2 (solution)",
    S, "Solution raises both transfers by U_L; IC constraints unchanged; new U_H >= (theta_H - theta_L) q_L >= 0 using Assumption 6. Re-derived; the constraint set is checked, including high-type participation.")
row("E2-b-math-L05-P3", "2.4-math", "course/modules/E/E2/L05.html Step 3 and problem L05-p3 (solution)",
    S, "Pi(q_L,q_H) = p_L(theta_L q_L - C(q_L)) + p_H(theta_H q_H - (theta_H - theta_L) q_L - C(q_H)); Hessian diag(-p_L, -p_H), no cross term; strictly concave. Re-derived.")
row("E2-b-math-L05-gap-decomp", "2.4-math", "course/modules/E/E2/L05.html Remark 2.1",
    S, "Round-1 causal sentence removed. Current text: 375,000 from the low type (p_L x (4,500,000 - 4,000,000)) and 1,500,000 = p_H x 6,000,000 rent. Recomputed in " + SCRIPT + ": 375,000 + 1,500,000 = 1,875,000. The cut condition p_L(theta_L - q_L) = p_H(theta_H - theta_L): 750 = 750 cents per unit; each unit cut lowers rent by 3000 cents. All verified.")
row("E2-b-math-L05-ex-r1", "2.4-math", "course/modules/E/E2/L05.html problem L05-r1 (statement and solution)",
    X, "Statement: 'show that the high type keeps a positive rent at any menu that satisfies both participation constraints and in which the low type takes a positive quantity'. Lemma 1.3 needs the incentive constraints, which the statement omits. Counterexample checked in " + SCRIPT + ": menu (q_L, m_L) = (1000, 0), (q_H, m_H) = (0, 0). U_L = 3,000,000 >= 0 and U_H = 0 >= 0 (both participation hold), q_L = 1000 > 0, but U_H = 0 < theta_H q_L - m_L = 6,000,000, so IC-H fails and the high type's rent is 0.",
    "Add the two incentive constraints to the hypothesis: 'at any menu that satisfies (IC-L), (IC-H) and both participation constraints, in which the low type takes a positive quantity'. The solution's 'Removing the rent would require q_L <= 0' then follows from Lemma 1.3 as written.")
row("E2-b-math-L06-prop1.3", "2.4-math", "course/modules/E/E2/L06.html Proposition 1.3 proof (incentive, bound, attainment, low effort, refusal)",
    S, "Re-derived: IC iff beta Delta_E >= c_H iff beta >= 1/5 (alpha cancels); bound E_H - alpha - beta E_H <= E_H(1-beta) <= 600,000, equality only at alpha = 0, beta = 1/5 (uses alpha >= 0 from Assumption 3 and beta >= 1/5); attainment gives agent 50,000 and principal 600,000; low effort profit <= E_L = 250,000; refusal gives 0. Statement's 'no other contract attains this profit' follows from the equality case.")
row("E2-b-math-L06-P1", "2.4-math", "course/modules/E/E2/L06.html problem L06-p1 (statement and solution)",
    S, "Round-1 defect fixed: the statement is about preference ('the agent prefers high effort ... iff beta >= 1/5, for any alpha'), and the solution separates acceptance: alpha = -1,000,000, beta = 1/2 satisfies IC (250,000 >= 100,000) yet both utilities are below 0 (-725,000 and -875,000), so the agent refuses. Re-derived in " + SCRIPT + ".")
row("E2-b-math-L06-P2-P3", "2.4-math", "course/modules/E/E2/L06.html problems L06-p2 and L06-p3 (solutions)",
    S, "P2: profit E_H - alpha - beta E_H <= E_H(1-beta) (alpha >= 0) <= 600,000 (beta >= 1/5), equality only at alpha = 0, beta = 1/5. P3: low-effort payment is 3/4 w(0) + 1/4 w(X-bar) >= 0, so profit <= E_L = 250,000. Re-derived.")
row("E2-b-math-L06-remarks", "2.4-math", "course/modules/E/E2/L06.html Remark 1.4, Remark 2.1, Lemma 1.2 proof",
    S, "Remark 1.4: alpha = c_H - beta E_H gives expected payment c_H and profit 650,000 for beta >= 1/5 (recomputed; Lab Part C prints 650000 for beta 0.20, 0.50, 1.00). Remark 2.1 identity: (E_H - alpha - beta E_H) + (alpha + beta E_H - c_H) = E_H - c_H = 650,000 = 600,000 + 50,000. Lemma 1.2 proof checked.")
row("E2-b-lab-L04", "2.5-labs", "course/modules/E/E2/L04.html Lab 1 (hypothesis before the block, interpretation after)",
    S, "Lab 1 is deterministic; output (20 lines) read in full. Hypothesis 'Proposition 1.3 predicts ... 2, 3 and 4, and the enumeration should agree' matches Part C. Interpretation: threshold 1 'low type gains' (Part B row: 5,000,000 vs 4,000,000 - correct); thresholds 5 and 6 'high type prefers education 0' (rows: best 4,000,000 at e=0 - correct); 'Lab does not show anything between whole years' (true, grid is integers). Docstring: 'checks each threshold by enumeration', 'the high type's utility at signal t' - matches code.")
row("E2-b-lab-L05", "2.5-labs", "course/modules/E/E2/L05.html Lab 1 hypothesis and interpretation; twin docstring",
    S, "Hypothesis: Part A prints menu and four constraints. Output has participation (low utility 0 >= 0 printed as holds True), high type utility 6,000,000 (its slack, = printed as value), IC slacks 0 and 12,000,000; the printed values support 'bind (slack 0)' and 'slack 12,000,000'. Part B argmax 2000; Part C argmax 6000; Part D 7875000, 6000000, 1875000 match Proposition 1.4 values. 'Covers every menu with nonnegative quantities' matches the corrected Assumption 6 statement. Minor: the high-type participation line prints a utility rather than a labelled slack; equivalent value, not a claim error.")
row("E2-b-lab-L06", "2.5-labs", "course/modules/E/E2/L06.html Lab 1 hypothesis and interpretation",
    S, "Round-1 defect fixed: hypothesis now attributes 'best share 0.20 / profit 600,000' to Proposition 1.3 and 'Part C reaches 650,000' to Remark 1.4. Output read in full: rows 0.00 (-100000, 0, low, 250000), 0.10 (-25000, 25000, low, 225000), 0.20 (50000, 50000, high, 600000), 0.30 (125000, 75000, high, 525000), 1.00 (650000, 250000, high, 0). Interpretation 'Part A shows 50,000 under both actions at 0.20 ... 525,000 at 0.30' matches. Part B 'all 101 grid shares' is computed. Interpretation 'Proposition 1.3 covers every contract that satisfies Assumptions 1 to 4' matches the statement.")
row("E2-b-lab-variant-L04", "2.5-labs", "course/modules/E/E2/L04.html problems L04-e1 and L04-e2",
    S, "Variant run of tests/labs/E2/lab-E2-L04-1.py with COST_HIGH=400_000 (copy in /tmp/e2-v/E2-b-r2/variants/l04_v.py): interval 2 to 5, enumerated [2,3,4,5], 'the two lists agree: True' - matches the solution's predicted thresholds 2,3,4,5. e2 (y_H = 5M): by closed form 1 and 2, as the solution states (recomputed).")
row("E2-b-lab-variant-L06", "2.5-labs", "course/modules/E/E2/L06.html problem L06-e1 and lab Part C",
    S, "Round-1 variant run is valid: with COST_HIGH=150,000 the best share is 0.30 and profit 525,000, first best 600,000, agency cost 75,000 (recomputed in " + SCRIPT + "). Lab Part C under this variant prints 'profit equals first-best' for beta=0.20 although 0.20 < 0.30 violates IC; that is a property of the variant's Part C, which the base case (0.20 = threshold) does not exhibit, and the base-case claims are unaffected.")
row("E2-b-ex-L04", "2.4-math", "course/modules/E/E2/L04.html problems L04-m1..m3, L04-p1..p3, L04-e1..e3, L04-r1..r3 (solutions)",
    S, "All worked solutions re-derived in " + SCRIPT + " or by hand: m1 (2..8), m2 (5,250,000; 4,000,000; 3,000,000 low-type utility at 3 is 3,000,000), m3 (1.5 and 3; whole numbers 2, 3), p1, p2 (single point), p3 (t=0 shared signal), e1 (2..5), e2 (1 and 2; low utility at e=1 equals 4,000,000), e3 (2 gives 5,000,000; 3 gives 4,500,000; 4 gives 4,000,000), r1-r3 (qualitative; no numeric claim beyond the stated closed forms).")
row("E2-b-ex-L05", "2.4-math", "course/modules/E/E2/L05.html problems L05-m1..m3, L05-p1..p4, L05-e1..e3, L05-r1..r3 (solutions)",
    X, "All numbers re-derived (m1 9,000,000; m2 U_H 3,000,000, IC-L -15,000,000; m3 5,625,000; e1 1500 / 6,750,000 / 6,666,667 / 2,333,333; e2 U_H 6,000,000 vs 4,500,000; e3 23.81% and 31.25%). The non-numeric problem L05-r1 is defective: see E2-b-math-L05-ex-r1.",
    "Fix L05-r1 as stated in E2-b-math-L05-ex-r1.")
row("E2-b-ex-L06", "2.4-math", "course/modules/E/E2/L06.html problems L06-m1..m3, L06-p1..p3, L06-e1..e3, L06-r1..r3 (solutions)",
    S, "m1 (87,500; 62,500; high effort; 562,500), m2 (0; 33,333 at 2/15; low effort), m3 (590,000), p1 witness (E2-b-math-L06-P1), e1 (0.30, 525,000), e2 (1/6; 666,666 2/3 -> 666,667; first best 700,000), e3 (surplus 650,000 = 600,000 + 50,000). Recomputed in " + SCRIPT + ".")
row("E2-b-term-L04-offpath", "2.5-terms", "course/modules/E/E2/L04.html Assumption 3 (define-before-use), Remark 2.2",
    X, "Assumption 3 defines off-path as 'no type chooses it in the profile of Proposition 1.3'. 'Profile' is not defined before Assumption 3; Proposition 1.3 (later) fixes the profile (high type e = t, low type e = 0). The term 'off-path' is therefore defined by reference to a later object. The earlier round's defect (use before definition, and the e = 0 misstatement) is otherwise fixed.",
    "In Assumption 3, state the profile first (high type at t, low type at 0), or move the off-path definition after Proposition 1.3 and make Assumption 3 refer to it.")
row("E2-b-term-L05-rent-efficient", "2.5-terms", "course/modules/E/E2/L05.html why-it-matters, Definition 1.2, Lemma 1.3 title, Remarks 1.5 and 2.1",
    S, "Round-1 defect fixed: why-it-matters now says 'utility'; 'rent' and 'first-best quantity' are defined in Definition 1.2 before the Lemma 1.3 title and Remark 1.5; 'efficient quantity' no longer appears in the body (grep). Assumption 4's cross-reference to the participation constraint of Definition 1.2 is a pointer, not a use of an undefined meaning.")
row("E2-b-term-L06-first-best", "2.5-terms", "course/modules/E/E2/L06.html Section 1 (definition), Remark 1.4, Remark 2.1, key-results row 3",
    S, "First-best profit is defined in Section 1 ('the principal's profit when effort is observable and the agent is paid exactly its cost c_H ... = 650,000') before Remark 1.4 and the key-results and quiz uses.")
row("E2-b-notation-L04", "2.5-notation", "course/modules/E/E2/L04.html (all math)", S,
    "Macros used are standard KaTeX plus registered macros only. Symbols t, e, c_L, c_H, y_L, y_H, Delta, theta are local and defined in Section 1. None of the registered symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) appears (grep of the math).")
row("E2-b-notation-L05-T", "2.5-notation", "course/modules/E/E2/L05.html Assumption 1, Definition 1.2, Proposition 1.4, quiz, card E2-c054", S,
    "Round-1 FAIL fixed: payments are m (local letter, allowed by notation/notation.json 'about': m is local). grep of the page math for a plain T used as payment: none. Card E2-c054 uses m_H, m_L. T (S1, number of observations) is not used in L05.")
row("E2-b-notation-L05-raw-macros", "2.5-notation", "course/modules/E/E2/L05.html Problem L05-p3 solution and Proposition text", S,
    "Round-1 FAIL fixed: the page uses \\diag and \\R^2 (registered in notation/notation.json). grep: no \\mathrm{diag}, no \\mathbb in L05.")
row("E2-b-notation-L06", "2.5-notation", "course/modules/E/E2/L06.html Lemma 1.2, Proposition 1.3", S,
    "alpha and beta defined in Lemma 1.2 (local, allowed); \\Prob registered macro used; E_H, E_L, Delta_E local. No registered symbol reused. p_a is defined in Section 1 and is used only in that definition; not a conflict.")
row("E2-b-dag-closure", "2.6-dag", "course/modules/E/E2/L04.html, L05.html, L06.html meta-row and body", S,
    "Prerequisite closure from curriculum YAML (E2 prereqs E1, M4): {E1, M1, M2, M4, P0.1}. Links on the three pages use only own-earlier E2 anchors (adverse-selection L03, signaling L04, screening L05, moral-hazard L06) and concepts.html#expectation (M4). Outside-closure words (expected utility, concave, risk neutral, risk aversion) appear as plain prose with no link and no dfn, as the Architect decisions default allows.")
row("E2-b-struct-lessons", "2.9-structure", "course/modules/E/E2/L04.html, L05.html, L06.html", S,
    "check_pages E2 PASS (template order, lesson hours 10 each, why-it-matters length, key results, quiz, references). Hours: lessons 10 h each (data-hours=\"10\"); hub data-hours-lessons=90 = 9 x 10 and data-hours-project=20; 90 + 20 = 110. Sum agrees with the curriculum 110 h. The pace of each lesson is not failed (architect ruling).")
row("E2-b-banned-phrases", "2.9-prose", "course/modules/E/E2/L04.html, L05.html, L06.html (visible text)", S,
    "tools/check_pages.py E2 PASS (banned strings). Independent scan of the visible-text renders in /tmp/e2-v/E2-b-r2/L04.txt..L06.txt for TODO, TBD, lorem, three-dot ellipsis, for brevity, details omitted, beyond the scope, left as an exercise, you can add, important to note, studies show, experts agree, well known, obviously, clearly, roughly, about <digit>, historically, approximately: no hit.")
row("E2-b-process-words", "2.9-prose", "course/modules/E/E2/L04.html, L05.html, L06.html", S,
    "Scan of visible text for build, builder, verifier, round, REQUEST, unit report: no hit (the only 'round' forms are 'rounded' and a docstring 'Round a non-negative exact amount' in a twin, which is a function description).")
row("E2-b-figures", "2.9-figures", "course/modules/E/E2/L04.html, L05.html, L06.html", S,
    "grep -c '<svg|<figure|figures-' on L04, L05, L06 -> 0 each. No figures to render.")
row("E2-b-cards-sample-1", "2.7-cards", "course/modules/E/E2/cards.json E2-c041..E2-c050", S,
    "Read all 10 against L04 (current text). c043 now says 'For 0 < e < t the wage y_L is an off-path belief' (agrees with Assumption 3). c048 agrees with section 4. c044 lists Assumptions 1 to 4 (agrees with Proposition 1.3). c045, c046, c047, c049, c050 agree with Remark 1.4, Lab 1 and Remark 2.1. Numbers appear in the lesson (1,000,000; 5,000,000; 4,000,000).")
row("E2-b-cards-sample-2", "2.7-cards", "course/modules/E/E2/cards.json E2-c051..E2-c060", X,
    "c051..c059 agree with the current lessons (c052 now matches Remark 2.2; c054 uses m; c057 lists Assumptions 1 to 6 as in Proposition 1.4). c060 front attributes 'screening in a competitive market' to Rothschild and Stiglitz; the paper's registry title does not mention screening and section 4 says 'competitive insurance markets under imperfect information'. Unread attribution (E2-b-cit-rothschild).",
    "Edit the front of E2-c060 to match section 4 (see E2-b-cit-rothschild).")
row("E2-b-cards-sample-3", "2.7-cards", "course/modules/E/E2/cards.json E2-c061..E2-c075", S,
    "Read all 15 against the lessons: c061 (2,000 and 6,000,000; 6,000 and 30,000,000 = Remark 1.5), c062 (rent 6,000,000; Lemma 1.3), c063 (2000 vs 3000; gap 1,875,000), c064 (Lab 1 Parts B and C grid points), c065-c068 (Definition 1.1, Assumption 3, Lemma 1.2, Proposition 1.3), c069 (beta >= 1/5, Assumption 4), c070 (Remark 1.4; 650,000), c071 (50,000; Remark 2.1), c072 (Holmstrom title/year/venue), c073 (525,000 at 0.30 from Lab Part A), c074, c075. All agree with the current text and every number appears in its lesson.")
row("E2-b-cards-dup-scan", "2.7-cards", "course/modules/E/E2/cards.json (all 121 cards of the unit)", S,
    "Script " + SCRIPT + " (difflib): 121 ids, 121 unique; zero back-text pairs with ratio > 0.9; six front pairs between 0.80 and 0.88, all distinct questions (E2-c017/c041, c041/c053, c048/c060, c048/c072, c060/c072, c078/c079). No duplicates.")

nonpass = [r["id"] for r in R if r["status"] != "PASS"]
frag = {
    "unit": "E2",
    "slice": "E2-b",
    "round": 2,
    "verifier": "Haiku independent verifier, round 2, slice E2-b (L04-L06 and lab twins 1-3). Did not build E2; shares no context with the builders.",
    "pin": "e22feb3",
    "base": "55b5634 (round-1 pin; delta since then: L04.html, L05.html, L06.html, cards.json, lab-E2-L05-1.py changed; L04/L06 twins unchanged). Carried rows: none, every row re-run on e22feb3.",
    "previous_ledger": "/tmp/fanout-frags/C-E2-b.round1.json (round 1, pin 55b5634, FAIL, 57 rows)",
    "checkout": "/tmp/verifyC2-E2-b (detached at e22feb3; .venv symlink; vendor present)",
    "scratch": "/tmp/e2-v/E2-b-r2",
    "verified_at": "2026-10-28T23:00:00Z",
    "verdict": "FAIL" if nonpass else "PASS",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: L04, L05, L06 and tests/labs/E2/lab-E2-L04-1.py, L05-1.py, L06-1.py. Project slices and graders are other slices; no mutants written (lesson slice; the mutation ruling applies to project graders only).",
        "Not checked: the three JSTOR-hosted sources (Spence 1973, Rothschild and Stiglitz 1976, Holmstrom 1979) were not read: they are not in reach of plain curl here and the brief forbids bypassing access blocks. Attribution rows are judged on the registry title, year and venue, as the architect ruling allows. The subtitle of Rothschild and Stiglitz is omitted in the short title on the page (not a factual error).",
        "Not run: the full repository pytest and check_projects, run_graders, mutate_graders (other slices); repository-wide mypy (only the three twins); live verify_refs covers 8 E2 entries (the tool's live scope for E2).",
        "Numbers: every number on the three pages was recomputed in exact arithmetic by " + SCRIPT + " (Fractions; a brute-force grid check for L05 Proposition 1.4 and L06 Proposition 1.3; no rounding except where the page displays a rounded value, and the display basis is stated).",
        "Round-1 FAIL rows fixed and re-verified: E2-b-cit-spence-result (row removed), E2-b-math-L04-off-path, E2-b-math-L05-prop1.4, E2-b-math-L05-P2, E2-b-math-L05-gap-decomp, E2-b-math-L06-P1, E2-b-lab-L05, E2-b-lab-L06, E2-b-term-L05-rent-efficient, E2-b-term-L06-first-best, E2-b-notation-L05-T, E2-b-notation-L05-raw-macros, E2-b-num-L05-variant-e1, E2-b-grade-L05, E2-b-cards-sample-1, E2-b-cards-sample-2 (partly: c060 remains FAIL).",
        "Remaining defects: E2-b-math-L05-ex-r1 (IC omitted from a hypothesis; counterexample in the script), E2-b-cit-rothschild and E2-b-cards-sample-2 (card E2-c060 attributes 'screening' to the Rothschild and Stiglitz paper), E2-b-term-L04-offpath (off-path defined by a later profile).",
    ],
    "summary": {
        "rows": len(R),
        "pass": sum(1 for r in R if r["status"] == "PASS"),
        "fail": sum(1 for r in R if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in R if r["status"] == "UNVERIFIABLE"),
        "mutants": 0,
        "fail_ids": nonpass,
    },
}
with open("ledgers/E2/E2-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
print(len(R), frag["verdict"], nonpass)
