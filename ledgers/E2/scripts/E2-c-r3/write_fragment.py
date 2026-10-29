"""Writes the E2 slice c round 3 verifier fragment (rows, verdict computed from statuses)."""
import datetime
import json
import pathlib

D = "ledgers/E2/scripts/E2-c-r3"
S = "ledgers/E2/scripts/E2-c-r3"
rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates and commands (run on pin ccfdf4c)
row("E2c-gate-check-pages", "2.9-structure", "course/modules/E/E2/L07.html, L08.html, L09.html", "PASS",
    f"tools/check_pages.py --unit E2 --page L07 / L08 / L09 each printed 'check_pages E2 Lnn: PASS' (logs {D}/out/check_pages_L0*.out).")
row("E2c-gate-check-dag", "2.9-dag", "course/modules/E/E2/L07-L09.html; tools/check_dag.py", "PASS",
    f"tools/check_dag.py --unit E2 -> 'check_dag E2: PASS', exit 0 ({D}/out/check_dag.out). Concept links on L07-L09 resolve to dfn ids L01 nash-equilibrium, L02 bayesian-nash-equilibrium, L04 signaling, L05 screening, L07 mechanism-design and revelation-principle, L08 bid-shading, common-value-auction, winners-curse; all defined before use.")
row("E2c-gate-run-labs", "2.5-labs", "tests/labs/E2/lab-E2-L07-1.py, lab-E2-L08-1.py, lab-E2-L09-1.py", "PASS",
    f"tools/run_labs.py --unit E2 --page L07/L08/L09 -> 'run_labs E2: PASS (1/1)' each, exit 0 ({D}/out/run_labs_L0*.out).")
row("E2c-gate-page-smoke", "2.9-smoke", "course/modules/E/E2/L07.html, L08.html, L09.html", "PASS",
    f"tools/page_smoke.py --unit E2 --pages L07 L08 L09 (run alone, quiet machine) -> 'page_smoke modules/E/E2/Lnn.html: PASS' x3 and 'page_smoke E2: PASS' ({D}/out/page_smoke.out). Lab runtimes in Pyodide 0.0 s and 0.2 s.")
row("E2c-twins-isolated", "2.5-labs", "tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py", "PASS",
    f"{D}/check_twins.py run as python -I -W error: exit 0 and empty stderr for each twin; each ends with an unconditional main() and has no __main__ guard ({D}/out/check_twins.out).")
row("E2c-page-code-equals-twin", "2.5-labs", "L07.html:164-306, L08.html:138-263, L09.html:91-214 (data-run code blocks)", "PASS",
    f"Unescaped <pre><code data-run> text equals the twin file byte-for-byte except one trailing newline on the twin (embed artifact); {D}/compare_page_twin.py, {D}/out/compare_page_twin.out.")
row("E2c-expected-equals-output", "2.5-labs", "L07.html expected block (line ~307), L08.html (line ~261), L09.html (line ~216 region)", "PASS",
    f"Unescaped <pre class=expected> text equals the stdout of the twin run under -I -W error, except one trailing newline ({D}/out/compare_page_twin.out).")
row("E2c-ruff-mypy-pytest", "2.5-labs", "tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py; tests/test_labs.py; tests/test_run_labs.py", "PASS",
    f"ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files'; pytest tests/test_labs.py tests/test_run_labs.py: all passed ({D}/out/ruff.out, mypy.out, pytest_labs.out).")

# ---- numbers (re-derived with own scripts)
row("E2c-l07-numbers", "2.2-numbers", "L07.html: §1 (v_L, v_H, p_H, Delta), Example 3.3 (c = -1000, revenue 7000, 6000), Lab 1 Part A-C printed values, Problems M1-M3, P3, E1-E3, R1, R3, quiz numerics", "PASS",
    f"{D}/recompute.py output: c(7/10) = -1000; exclusion 7000; pooling 6000; grid pairs with q_L<=q_H = 15, all pass, best (0,1) = 7000; decline tie-break revenue 4200 (0.7*6000); low-price tie-break 6000; M3 revenue 6500 = formula 7000 + (-1000)(1/2); M2 c = 1000 at p_H=1/2; R3 c = 6000 - 10000 p_H, zero at 3/5 ({D}/out/recompute.out). Printed Lab 1 values checked in the run_labs and expected-block comparison. Quiz numeric answers 7000, 4200, 6000 match.")
row("E2c-l08-numbers", "2.2-numbers", "L08.html: Example 2.4 (4/9), Remark 2.3 (4000/3, 1333.33, 1333.66656253, 0.3332292, 1.34), Remark 3.2 (1334, -0.67), Lab 1 interpretation (-26620718, -26673331, 79810, 0.66 SE, -1333.67, -1331.04, 59282, 6669, 52613, 26680000), Problems E1-E3, R1, R3", "PASS",
    f"{D}/recompute.py: E[M](2,1)=4/9, E[M](3,1)=2/3, E[M](5,2000)=85418692002000/64048012001 = 1333.6665625260 (claimed 1333.66656253); 4000/3 = 1333.3333; difference 0.3332292; exact naive total -26673331.2505 -> -26673331; exact shaded 6668.749 -> 6669; 1334-E[M]=0.33343747; 1333-E[M]=-0.6665625; {D}/recompute_l08_sim.py re-implements the seeded simulation independently: naive total -26620718, shaded 59282, SE 79810, shaded minus naive = 26680000 = 1334*20000, (naive - exact)/SE = 0.659 ({D}/out/recompute_l08_sim.out). Brute-force enumeration for n=2,3 (a=1) agrees with the Prop 2.2 sum.")
row("E2c-l09-numbers", "2.2-numbers", "L09.html: Part A (14000, 17500, 16000, 7/8, 25%), Part B (228, 28, 0, 256), Part C (256 of 256), Remark 3.3, Problems M1-M3, E1-E3, R1, quiz numerics", "PASS",
    f"{D}/recompute_l09.py: revenues 14000 and 17500, gap 3500 = 1/4 of 14000, efficiency 14000/16000 = 7/8; 256 profiles: 228 above, 28 equal, 0 below; equal set = profiles whose top three bids are equal (checked profile by profile, no mismatch); k=1 identity 256/256; R1 counts 4v+1 = 1,5,9,13 sum 28; 228/256 = 0.890625 = 89.06%; M2 12000 vs 15000 diff 3000 ({D}/out/recompute_l09.out).")
row("E2c-l08-simulation-reproduction", "2.5-labs", "tests/labs/E2/lab-E2-L08-1.py (SIMULATED seed 20261028)", "PASS",
    f"Independent re-implementation in {D}/recompute_l08_sim.py reproduces every printed simulated total and SE exactly; the lab is labelled SIMULATED in the hypothesis, the docstring, the interpretation and key-results row.")

# ---- mathematics
row("E2c-l07-prop2.2", "2.4-math", "L07.html Assumption 3, Definition 2.1, Proposition 2.2 and proof (lines ~85-111)", "PASS",
    "Re-derived the proof: x*(theta') = x(s(theta')); the equilibrium condition for type theta against message s(theta') gives the truthful-report inequality; outcomes equal per type so expected payments and trades coincide. Assumptions complete for the one-agent claim; the page does not claim the several-agent case (canon-breaks, quiz L07q9).")
row("E2c-l07-lemma3.1", "2.4-math", "L07.html Assumption 4, Lemma 3.1 and proof (lines ~127-135)", "PASS",
    "Re-derived: IC of H against L gives U_H >= U_L + Delta q_L; IC of L against H gives U_H <= U_L + Delta q_H; IR reduces to U_L >= 0 since U_H >= U_L + Delta q_L >= 0; the two bounds are compatible iff Delta q_L <= Delta q_H, i.e. q_L <= q_H for Delta > 0; converse holds. Statement with Delta > 0 is complete.")
row("E2c-l07-prop3.2", "2.4-math", "L07.html Proposition 3.2 statement and proof, lines 139-153", "FAIL",
    "The statement says the maximiser is q_L = 0 when c < 0 and q_L = 1 when c > 0, and gives the maximum for c < 0 and c > 0 only. The proof closes with the same two cases and never addresses c = 0. At c = 0 both endpoints give p_H v_H = v_L (recompute.py: at p_H = 3/5 the value is 6000 for both menus) so the claim is true but unstated; R3 and key-results row 3 rely on it without the case.",
    "In Proposition 3.2 and its proof add the case c = 0: both q_L = 0 and q_L = 1 attain the maximum, which equals p_H v_H = v_L. Then state in key-results row 3 that c = 0 gives both menus.")
row("E2c-l07-prop-3.1-example", "2.4-math", "L07.html Example 3.3 (lines ~158)", "PASS",
    "Recomputed: c = (3/10)(6000) - (7/10)(4000) = -1000; optimal menu q_L=0, q_H=1, tau_H=10000, tau_L=0 satisfies Lemma 3.1 (U_H = 0); revenue 7000; both-type pooling at 6000 gives 6000.")
row("E2c-l07-remark2.4-signaling", "2.9-prose", "L07.html Remark 2.4 (line ~ 'the special cases of L04 and L05')", "PASS",
    "L04.html line 60 defines signaling with the informed worker choosing the observable signal first and the firm, which sees the signal and not the type, setting the wage; this matches the Remark's description. L05 menu-as-direct-mechanism claim is consistent with Definition 1.2.")
row("E2c-l08-prop2.1", "2.4-math", "L08.html Proposition 2.1 statement and proof, lines 89-95", "FAIL",
    "Statement and sign argument check out (M >= eps_1, M - eps_1 >= (eps_2 - eps_1)^+, P(eps_2=a, eps_1=-a) = (2a+1)^-2, so E[M] > 0). But the first paragraph of the proof, line 94, says the largest bid V+M is the winner's bid 'because a tie between bids means the same value'. That is not the reason: the bid equality follows from every bid being V + eps_i, so the largest bid is V + max eps_i = V + M. The sentence as written does not justify the step.",
    "On L08.html line 94 replace 'because a tie between bids means the same value' with 'because every bid is V + eps_i, so the largest bid is V + M'.")
row("E2c-l08-prop2.2", "2.4-math", "L08.html Proposition 2.2 statement and proof (lines ~102-110)", "PASS",
    "Re-derived: Prob(M<=x) = F(x)^n with F(x)=(x+a+1)/(2a+1); M + a = sum over x=-a..a-1 of 1{M > x}; E[M] = -a + sum (1 - F(x)^n). Brute-force enumeration (recompute.py) agrees for (n,a)=(2,1) and (3,1); the closed form for (5,2000) is 85418692002000/64048012001.")
row("E2c-l08-remark2.3-grade", "2.3-grades", "L08.html Remark 2.3 (line 113), key-results row (line 413), references paragraph (section 9)", "FAIL",
    "The discrete E[M] for n=5, a=2000 is graded C (single-sample evidence per BLUEPRINT §3) and the remark says it 'is not a derivation on this page'. It is the exact evaluation of Proposition 2.2, which the page proves (grade T); recompute.py gives the exact fraction with no simulation. The grade and the sentence contradict the page.",
    "Grade the discrete value T with source 'Proposition 2.2 evaluated exactly (Lab 1 Part B prints the exact total)'; delete 'it is not a derivation on this page'; update key-results row (line 413) and the section 9 sentence 'except the discrete value of Remark 2.3, which is grade C'.")
row("E2c-l08-continuous-analogue", "2.4-math", "L08.html Remark 2.3 continuous analogue (line 113)", "PASS",
    "Re-derived: M = -a + 2aU, E[U] = n/(n+1), E[M] = a(n-1)/(n+1) = 4000/3 for n=5, a=2000; E[M] = 1 for n=2, a=1 gives 1/3 (R1 value).")
row("E2c-l08-remark3.2", "2.2-numbers", "L08.html Remark 3.2 (line ~135)", "PASS",
    "1334 is the least integer >= 1333.66656253; 1333 - E[M] = -0.66656253, rounds to -0.67 (recompute.py).")
row("E2c-l09-prop2.1", "2.4-math", "L09.html Definition 1.1, Definition 1.2, Proposition 2.1 and proof (lines ~62-84)", "PASS",
    "Re-derived: R_d - R_u = sum over j<=k of (b_(j) - b_(k+1)) >= 0 with equality iff b_(1)=...=b_(k+1); verified exhaustively on 256 profiles (recompute_l09.py: equality set equals the top-three-equal set).")
row("E2c-l09-prop3.2-prop4.1", "2.4-math", "L09.html Proposition 3.2 (efficiency 1 under truthful bids), Definition 3.1, Proposition 4.1 (k=1)", "PASS",
    "Definition 3.1 handles the non-positive denominator explicitly. Proof of 3.2 is complete (ranking by value, ties to lower index, same winners under both formats). Proposition 4.1 follows from Definition 1.1 with k=1; 256/256 identity check.")
row("E2c-l09-grades", "2.3-grades", "L09.html key-results rows 4 and 5 (lines ~423-427)", "PASS",
    "Row 4 (228/28/0 counts over an exhaustive 256-profile grid) graded C with basis Lab 1 Part B, consistent with the plan rule that finite enumerations are C. Row 5 (efficiency 7/8, 25%) graded T with its arithmetic on the page (E1, E3); the inputs are printed by Part A and the arithmetic is written out, so T is accepted here (noted, not failed).")
row("E2c-l07-quiz-items", "2.9-prose", "L07.html quiz items L07q1-L07q9 (line ~500-575)", "PASS",
    "Each correct option is consistent with the lesson and the labs (checked against Lab 1 printed values and Proposition 3.2); numeric answers 7000, 4200, 6000, 0 match the recomputed values; explanations cite the right definitions.")
row("E2c-l08-quiz-items", "2.9-prose", "L08.html quiz items L08q1-L08q9 (line ~425-490)", "PASS",
    "Numeric answers -0.4444 (tol 1e-4), 1334, 0.6667 (tol 1e-4), -250 match recomputed values; L08q5 0.3332 difference matches recomputed 0.3332292; correct options match Prop 2.1 and Remark 3.2.")
row("E2c-l09-quiz-items", "2.9-prose", "L09.html quiz items L09q1-L09q9 (line ~440-500)", "PASS",
    "Numeric answers 14000, 17500, 0.875 (tol 5e-4), 228 match Part A/B printed values; correct options are consistent with Definition 1.1, Proposition 2.1, 3.2, 4.1 and Remark 2.2.")
row("E2c-l07-problem-set", "2.4-math", "L07.html Problems M1-M3, P1-P3, E1-E3, R1-R3 (lines ~376-478)", "PASS",
    "Every worked solution recomputed: M1 utility 4000; M2 c = 1000, revenue 6000 vs exclusion 5000; M3 6500 = formula; P1 sum of IC inequalities gives (v_H - v_L)(q_H - q_L) >= 0 with no IR used; P3 U_H = 0; E1 15 of 15; E2 lists the four menus correctly; E3 gap 1000; R1 decline tie-break revenue 4200 with IC and IR; R2 Delta=0 remark; R3 threshold 3/5.")
row("E2c-l08-problem-set", "2.4-math", "L08.html Problems M1-M3, P1-P3, E1-E3, R1-R3 (lines ~300-400)", "PASS",
    "Recomputed: M1 -4/9; M2 2/3 (27ths check); M3 5/9, 1 cent enough; P2 product formula; P3 a>=1 needed; E1 52613, 0.66 SE, 3.99 per auction, 0.25 cent rounding effect; E2 26680000; E3 0.33343747 and -0.66656253; R1 1/3 vs 4/9, difference 1/9; R3 nonnegative set starts at 1334.")
row("E2c-l09-problem-set", "2.4-math", "L09.html Problems M1-M3, P1-P3, E1-E3, R1-R3 (lines ~318-410)", "PASS",
    "Recomputed: M1 ranking 1,3,2,0 and clearing 6000; M2 12000 vs 15000 diff 3000; M3 7000 vs 8000; P1 winners exactly k; P2 efficiency 1; P3 format-independence; E1 7/8; E2 228/256 = 0.890625; E3 25%; R1 4v+1 sum 28; R3 Proposition 4.1 proof.")

# ---- DAG, prose, notation, attribution, hours
row("E2c-dag-outside-closure", "2.9-dag", "L07.html line ~92 ('expected utility of a type'); L08, L09 full text", "PASS",
    "grep over L07-L09 for E3/M7/S1/E4/FC2 concept names: 'expected utility' (L07 line ~92) is plain prose with no link and no dfn, which the architect defaults permit; no Lagrangian, KKT, convexity, Bayes' rule as a named concept, risk-aversion or welfare-theorem term appears. Nothing outside the prerequisite closure is linked.")
row("E2c-banned-and-process-words", "2.9-prose", "L07.html, L08.html, L09.html visible prose and code comments", "PASS",
    "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, '...', widely claimed, builder, verifier, REQUESTS, unit report, ledger: no hits. The word 'agent' is the mechanism-design term (one agent), not a process word.")
row("E2c-notation-registry", "2.4-notation", "L07.html, L08.html, L09.html; notation/notation.json", "PASS",
    "Macros used are the registered ones (\\E, \\Prob, \\indic) and no hand-typed \\mathcal{N}, \\mathbb{E}, \\mathbb{P}, \\Phi or T appears; the letters R (revenue), tau, U, c, M, F, a, n, V, S, v, b, k, q, x, Theta are local and defined in each lesson. The one collision is x^{*} (row FAIL E2c-l07-notation-xstar).")
row("E2c-l07-notation-xstar", "2.4-notation", "L07.html lines 101, 106, 111, 415, 417, 486 (x^{*} for the direct-mechanism map)", "FAIL",
    "notation/notation.json symbol row 'R^\\ast' has the meaning '... defined in AP1 Lesson 4, where it is written x^\\ast ...', so x^\\ast is the registered AP1 payoff-space SDF notation. L07 reuses x^{*} for the direct-mechanism map x*(theta) = x(s(theta)) in Proposition 2.2, its proof, Problem P2, and key-results row 1. Plan §2.3 requires registered AP1 symbols not to take another meaning.",
    "Rename the direct-mechanism map on every line listed (for example to \\hat{x}) in L07.html; no other change is needed.")
row("E2c-attributions", "2.1-citations", "L08.html §9 references paragraph (names two registry titles); L07.html §9; L09.html §10", "PASS",
    "Crossref via plain curl (no personal data): doi 10.2307/1911865 = 'A Theory of Auctions and Competitive Bidding', Econometrica 50(5), 1982; doi 10.1111/j.1540-6261.1961.tb02789.x = 'COUNTERSPECULATION, AUCTIONS, AND COMPETITIVE SEALED TENDERS', Journal of Finance 16(1), 1961 (ledgers/E2/scripts/E2-c-r3/out/crossref.out). The L08 text names them by title and year and attributes no result, matching the registry string. No other attribution appears in L07-L09. Abstracts were not read; no result is attributed to either paper.")
row("E2c-hours", "2.9-structure", "L07.html, L08.html, L09.html eyebrow and data-hours", "PASS",
    "data-hours=10 on each of the three lessons; check_pages.py accepts 6-12 h; hub split is outside this slice.")
row("E2c-lab-claims-match-output", "2.5-labs", "L07 Lab 1 interpretation (line ~344), L08 Lab 1 interpretation (line ~266), L09 Lab 1 interpretation (line ~243)", "PASS",
    "Every sentence about printed values matches the expected block: L07 Parts A (7000, 6000, 10000 IC-only, 1800 IC-fail), B (15 of 15, grid optimum 7000), C (6000 and 4200); L08 Parts A (4/9 both), B (-26620718, -26673331, 79810, 0.66 SE, -1331.04 per auction), C (59282, 6669); L09 Part A (7/8, 14000, 17500), Part B (228/28/0), Part C (256 of 256). The labs make no claim about markets, equilibria or real bidders beyond what the text says.")
row("E2c-lab-docstring-claims", "2.5-labs", "Docstrings of tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py", "PASS",
    "Docstrings match the code: L07 Part A 'two feasible menus, one fails IR, one fails IC' (the code's show() list); L08 'nine noise pairs', exact totals rounded half up, SE formula matches standard_error_of_total; L09 'the ratio is not defined when that sum is not positive' matches efficiency code path (Part A has positive sum).")
row("E2c-html-structure", "2.9-structure", "L09.html lines ~ 213-215 (h2 id=s3 not wrapped in a section element)", "PASS",
    "Cosmetic: section 3-5 headings of L09 are not wrapped in <section> elements. check_pages.py and page_smoke.py pass; noted, not a verification failure.")

mutants = []
fragment = {
    "unit": "E2",
    "slice": "E2-c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-c round 3 (did not build E2; no context shared with the builders)",
    "pin": "ccfdf4c",
    "base": "none: no round-2 fragment exists at /Users/billyribeiro/.fanout/frags/C-E2-c.round2.json (directory empty); every row re-verified from scratch",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-E2-c",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyC3-E2-c (scripts kept under ledgers/E2/scripts/E2-c-r3/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice E2-c = L07-L09 and their lab twins, pinned at ccfdf4c. Mutants: none, because the slice holds lessons and lab twins only "
        "(VERIFIER §2.6 mutants apply to project graders, which are slice d). Labs are demonstrations (ruling), so no lab mutants were written. "
        "Not checked by this verifier: cards.json entries for L07-L09 (slice d scope in the slices file); the hub; the project; "
        "tools/verify_refs.py run (only the two auction DOIs were confirmed by plain curl to Crossref); page_smoke for the other E2 pages; "
        "the full pytest suite; the repo-wide gates. Lessons L07-L09 were read in full (HTML body, quiz, references), and every "
        "numeric claim was recomputed; hub and cards not read. Non-PASS rows: E2c-l07-prop3.2, E2c-l07-notation-xstar, E2c-l08-prop2.1, E2c-l08-remark2.3-grade."
    ),
    "summary": "",
}
n = len(rows)
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = n - pass_n
fragment["summary"] = (f"E2 slice c (L07-L09 and twins) round 3 at ccfdf4c: verdict {fragment['verdict']}. {n} rows: {pass_n} PASS, "
                       f"{fail_n} non-PASS (FAIL), 0 UNVERIFIABLE. Non-PASS: E2c-l07-prop3.2 (c=0 case omitted), E2c-l07-notation-xstar "
                       f"(x^* reuses the registered AP1 notation), E2c-l08-prop2.1 (invalid reason in the tie sentence), "
                       f"E2c-l08-remark2.3-grade (grade C contradicts the page's Proposition 2.2).")
out = pathlib.Path("ledgers/E2/E2-c.json")
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", n, "pass", pass_n, "fail", fail_n, "verdict", fragment["verdict"])
