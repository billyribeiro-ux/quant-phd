import json, sys
sys.path.insert(0, "tools")
import ledger

CARRY_L04 = "Carried from round 5 (course/modules/E/E2/L04.html and tests/labs/E2/lab-E2-L04-1.py byte-identical since 04626e9; git diff empty): "
CARRY_REG = "Carried from round 5 (references/references.json byte-identical since ccfdf4c; git diff empty; offline verify_refs this round: 'offline integrity: 560 entries, 0 problems'): "
RECHK = "Round 6 (pin 9fd6aed, delta from 04626e9 read in full): re-derived with ledgers/E2/scripts/E2-b-r6/recompute_E2b_r6.out ('TOTAL 59 FAILED 0', 'ALL True') and the lab output below: "
ids = [
 ("E2b-cite-spence1973job","2.1-citation","course/modules/E/E2/L04.html:229","PASS", CARRY_L04+"Spence (1973) cited by title, year, venue only; registry spence1973job unchanged."),
 ("E2b-cite-rothschild1976equilibrium","2.1-citation","course/modules/E/E2/L05.html:254; L05.html:296","PASS", RECHK+"L05.html:254 read in full, title/year/venue only, no result used; registry rothschild1976equilibrium unchanged (CARRY_REG)."),
 ("E2b-cite-holmstrom1979moral","2.1-citation","course/modules/E/E2/L06.html:247; L06.html:290","PASS", RECHK+"L06.html:247 read, title/venue/year only, no result; L06.html:290 (L06-r3) quotes title word 'observability', matching 'Moral Hazard and Observability'."),
 ("E2b-cite-live-registry","2.1-citation","references/references.json (8 E2 keys)","PASS", CARRY_REG+"Live run not repeated this round (no registry change)."),
 ("E2b-cite-attribution-abstract","2.1-citation","L04.html:229; L05.html:254; L06.html:247","PASS", RECHK+"each sentence attributes title, year, venue only; no claim depends on the abstracts (not read)."),
 ("E2b-numbers-L04","2.2-numbers","L04.html:56, 79-100, 218-219, 235-237, 245-273, 261-265, 299-316, 328-329","PASS", CARRY_L04+"round-5 recomputation re-run on this pin: TOTAL 59 FAILED 0."),
 ("E2b-numbers-L05","2.2-numbers","L05.html:56, 97, 124-125, 249, 254, 260-262, 270-274, 286-290, 305-310, 324-354","PASS", RECHK+"Remark 2.1 (L05.html:249) numbers re-derived: 3000*(4.5M-4.0M)*3/4=375,000; 0.25*6,000,000=1,500,000; sum 1,875,000; 750=750 (3/4*1000 = 1/4*3000). Lab L05 Part D prints 7875000, 6000000, 1875000."),
 ("E2b-numbers-L06","2.2-numbers","L06.html:56-63, 99-107, 113, 229, 234, 241, 252-253, 262-266, 270-282, 298-301, 316-346","PASS", RECHK+"lab 1 output (run_labs_L06.out): best share 0.20, principal profit 600000, first-best 650000, agency cost 50000; Part A rows 0.00/250000, 0.10/225000, 0.20/600000, 0.30/525000, 1.00/0; Remark 2.1 identity 600,000+50,000=650,000."),
 ("E2b-numbers-printed-digits","2.2-numbers","L04.html:192-211; L05.html:222-241; L06.html:209-228","PASS", RECHK+"twin output re-run under python -I -W error (twin_L06.out, twin_L05.out) and run_labs PASS: printed digits equal the expected blocks."),
 ("E2b-grades-L04","2.3-grades","L04.html:84 (T), 98-101, 217-225, 282-284","PASS", CARRY_L04),
 ("E2b-grades-L05","2.3-grades","L05.html:101 (Lemma 1.3 T), 111 (Prop 1.4 T), 307-309","PASS", RECHK+"grades unchanged on those lines; Remark 2.1 is a remark (no grade claim)."),
 ("E2b-grades-L06","2.3-grades","L06.html:86 (Lemma 1.2 T), 98 (Prop 1.3 T), 299-302 (Key results)","FAIL", "Key-results row at L06.html:302 reads 'Without limited liability the first best of 650,000 cents is attained, and the agency cost is 50,000 cents', graded T. Remark 1.4 (L06.html:233-236) and Remark 2.1 (L06.html:241-243) make the agency cost 0 without limited liability (first best 650,000 attained) and 50,000 with it. The sentence attributes the 50,000 to the wrong regime. Round 5 PASSed this row without catching it."),
 ("E2b-grades-citation-claims","2.3-grades","L04.html:229; L05.html:254; L06.html:247","PASS", RECHK+"claims graded C with citation only; no result attributed."),
 ("E2b-math-L04-prop13","2.4-mathematics","L04.html:83-96","PASS", CARRY_L04),
 ("E2b-math-L04-remark22","2.4-mathematics","L04.html:223-225","PASS", CARRY_L04),
 ("E2b-math-L05-lemma13","2.4-mathematics","L05.html:101-107","PASS", RECHK+"lemma text on unchanged lines; Lemma 1.3 cited by Remark 2.1 for 'each unit removed lowers rent by 3000' (rent = (theta_H-theta_L) q_L when U_L=0): verified."),
 ("E2b-math-L05-prop14","2.4-mathematics","L05.html:111-119","PASS", RECHK+"Step 3 (L05.html:119) unchanged; FOC 750=750 re-derived."),
 ("E2b-math-L05-p3-concavity","2.4-mathematics","L05.html:119 (Step 3) and L05.html:281-282 (L05-p3)","PASS", CARRY_L04+"L05-p3 solution unchanged; Hessian sign re-checked in recompute output."),
 ("E2b-math-L06-lemma12","2.4-mathematics","L06.html:86-93","PASS", RECHK+"Lemma 1.2 proof re-read: alpha+beta*Xbar=w(Xbar); expected payment weights 3/4, 1/4 match E_a. Statement 'every contract ... is affine in output' is the two-point interpolation, valid."),
 ("E2b-math-L06-prop13","2.4-mathematics","L06.html:98-109","PASS", RECHK+"beta>=1/5 from 750000*beta>=150000 (IC); profit <= E_H(1-beta) <= 600000; Remark 1.4 threshold 150,000>c_H=100,000."),
 ("E2b-math-L06-remark14-21","2.4-mathematics","L06.html:233-241","PASS", RECHK+"Remark 1.4 alpha=c_H-beta E_H <0 for beta>=1/5 (150,000>100,000). Remark 2.1 identity re-derived."),
 ("E2b-math-L06-remark21-scope","2.4-mathematics","L06.html:241-243 (Remark 2.1)","PASS", RECHK+"agency cost defined as first best minus optimum under model constraints = 50,000 WITH limited liability; this scope is what the Key results row (L06.html:302) misstates, see E2b-grades-L06."),
 ("E2b-notation","2.4-notation","L04.html, L05.html, L06.html (math spans); notation/notation.json","PASS", RECHK+"no new symbols introduced this delta except the word 'affine' (not a symbol); alpha, beta, c_H, E_H, X-bar used as before."),
 ("E2b-labs-run","2.5-labs","tests/labs/E2/lab-E2-L04-1.py, lab-E2-L05-1.py, lab-E2-L06-1.py","PASS", "run_labs_L04.out, run_labs_L05.out, run_labs_L06.out: 'run_labs E2: PASS (1/1)' each; twins under python -I -W error exit 0 with empty stderr (twin_L05.err, twin_L06.err)."),
 ("E2b-labs-page-twin","2.5-labs","course/modules/E/E2/L04.html:106-191; L05.html:130-221; L06.html:114-208","PASS", "run_labs PASS on all three pages: page code equals twin and expected block equals output."),
 ("E2b-labs-L04-claims","2.5-labs","L04.html:105 (hypothesis), 212 (interpretation), 92-96","PASS", CARRY_L04),
 ("E2b-labs-L05-claims","2.5-labs","L05.html:129 (hypothesis), 242 (interpretation)","PASS", RECHK+"Part A now prints the four constraints; interpretation (L05.html:242) claims low PC bind 0>=0, high IC slack 0, low IC slack 12,000,000, best grid points 2000 and 6000: all in twin_L05.out."),
 ("E2b-labs-L06-claims","2.5-labs","L06.html:113 (hypothesis), 229 (interpretation)","PASS", RECHK+"hypothesis now promises agency cost printed in Part B: twin_L06.out line 'agency cost ... 50000' present; Part C reaches 650000 at 0.20/0.50/1.00 as the interpretation says."),
 ("E2b-labs-seed-network","2.5-labs","tests/labs/E2/lab-E2-L04-1.py, lab-E2-L05-1.py, lab-E2-L06-1.py","PASS", "No random draws and no network imports in the three twins (read in full; twin runs under -I with no network)."),
 ("E2b-labs-L05-docstring","2.5-labs","tests/labs/E2/lab-E2-L05-1.py:8-13 (module docstring, Part A)","PASS", "Round-5 FAIL fixed: docstring now says Part A prints the four constraints with an explicit participation check for the low type only, the high type's utility and two incentive slacks printed as values; twin_L05.out shows 'low type utility, participation: 0 >= 0 holds: True', 'high type utility: 6000000', slacks 0 and 12000000."),
 ("E2b-dag","2.9-dag","L04.html:38-39; L05.html:38-39; L06.html:38-39","PASS", "check_dag E2: PASS (ledgers/E2/scripts/E2-b-r6/check_dag.out)."),
 ("E2b-terms-before-definition","2.9-terms","L04.html:105 (lab hypothesis) with forward pointer to Remark 2.1 at L04.html:218","PASS", CARRY_L04),
 ("E2b-terms-agency-cost-before-definition","2.9-terms","L06.html:113 (lab hypothesis); L06.html:241 (Remark 2.1)","PASS", "Round-5 FAIL fixed: L06.html:113 now says 'agency cost, first best minus best profit (defined in Remark 2.1 below)', a forward pointer; Remark 2.1 defines it at L06.html:241."),
 ("E2b-terms-linear-vs-affine","2.9-terms","course/modules/E/E2/L06.html:7 (meta description); course/modules/E/E2/cards.json E2-c067 (front, line 453); L06.html:86, 95, 114, 286","FAIL", "Round 6 renamed the form to 'affine' in Lemma 1.2 (L06.html:86, 95), the lab title and docstring (L06.html:114) and problem L06-r1 (L06.html:286), but the meta description at L06.html:7 still says 'The linear contract', and card E2-c067 (lesson L06, cards.json:453) still asks 'what linear form does every contract take'. Same object, two names in one lesson. Fix: change 'linear form' to 'affine form' in cards.json E2-c067 (regenerate via build_site.py, do not hand-edit generated output per CLAUDE.md rule 1 if the card file is generated; else edit the source) and change L06.html:7 meta to 'The affine contract'. Severity low."),
 ("E2b-process-words","2.9-prose","L04.html, L05.html, L06.html; tests/labs/E2/lab-E2-L0[456]-1.py","PASS", "Changed prose (L05.html:249, L06.html:52, 95, 113, 241) read: no process words ('this round', 'changed', 'was fixed')."),
 ("E2b-structure-hours","2.9-structure","L04.html:2, L05.html:2, L06.html:2 (data-hours=10); index.html:28-29, 113-115","PASS", "No hours change in delta; index.html not in the 04626e9..9fd6aed delta for E2 (carried)."),
 ("E2b-structure-page-smoke","2.9-structure","L04.html, L05.html, L06.html","PASS", "page_smoke E2: PASS (page_smoke_L05.out, page_smoke_L04.out, page_smoke_L06.out); check_pages E2 L04/L05/L06: PASS."),
 ("E2b-hub-titles","2.9-structure","course/modules/E/E2/index.html:112-115 vs L04.html:36, L05.html:36, L06.html:36","PASS", "index.html unchanged since 04626e9 (not in delta). L05 h2 renamed at L05.html:~247 is a section heading, not a hub title; L06 titles unchanged."),
 ("E2b-quiz-explanations","2.9-structure","L04.html:292-349; L05.html:316-374; L06.html:308-366","PASS", "Quiz blocks not in the delta hunks (carried, byte-identical spans)."),
 ("E2b-gates-tests","2.9-gates","tests/test_labs.py -k E2; tests/test_page_checks.py; tests/test_page_smoke.py","PASS", "pytest -k E2 on test_labs.py: 15 dots, no failures; test_page_checks.py + test_page_smoke.py: 17 dots, no failures."),
 ("E2b-gates-lint-type","2.9-gates","tests/labs/E2/lab-E2-L04-1.py, lab-E2-L05-1.py, lab-E2-L06-1.py","PASS", "ruff check tests/labs/E2: 'All checks passed!'; ruff format --check: '12 files already formatted' (ruff_E2_labs.out). mypy not run (only the three twins changed and mypy is not in the required gate list for a twin-only delta; not verified)."),
 ("E2b-problems-solutions","2.6-problems","course/modules/E/E2/L06.html:279-280 (L06-e2)","PASS", "Round-4 FAIL remains fixed: L06-e2 solution (agency cost 75,000 and first best 700,000 re-derived in recompute output) unchanged in delta."),
 ("E2b-problems-other","2.9-problems","L04.html:244-273; L05.html:269-298; L06.html:261-291","PASS", "L06-r1 (L06.html:286-287) rewritten to 'affine form': two outcomes give two free values, any two values define an affine function; the three-outcome remark is correct. Other solutions unchanged."),
]
FIX = {
 "E2b-grades-L06": "Rewrite L06.html:302 row to: 'Without limited liability the first best of 650,000 cents is attained (agency cost 0, Remark 1.4); with limited liability the agency cost is 50,000 cents (Remark 2.1)', keep grade T.",
 "E2b-terms-linear-vs-affine": "Use 'affine' in cards.json E2-c067 front (source of the generated card file; regenerate) and change L06.html:7 meta to 'The affine contract'.",
}
rows = [{"id": i, "check": c, "location": l, "status": s, "evidence": e, **({"fix": FIX[i]} if i in FIX else {})} for i, c, l, s, e in ids]
d = {
 "unit": "E2", "slice": "b", "round": 6,
 "verifier": "Claude Haiku 5.5, independent verifier for E2-b (did not build E2; no context shared with builders)",
 "pin": "9fd6aed", "base": "04626e9 (round-5 pin)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-E2-b",
 "scratch": "none (all scripts under ledgers/E2/scripts/E2-b-r6/)",
 "verified_at": "2026-10-29T12:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [{"id": "M-L06-agency-sign", "description": "L06 lab 1 twin: agency cost sign flipped (principal_profit(best) - FIRST_BEST); ledgers/E2/mutants/L06-lab1-agency-sign.py", "killed_by": "run_labs / expected block: printed -50000 vs page expected 50000 (ledgers/E2/scripts/E2-b-r6/ ran the mutant; output 'agency cost ... -50000')"}],
 "registry_flags": ["holmstrom1979moral: author family 'Holmstrom' vs prose 'Holmström' (carried from round 5; observation, not a citation failure)."],
 "freshness_flags": [],
 "notes": "Delta 04626e9..9fd6aed for the slice: L05.html (Part A lab text, Remark 2.1 rewritten, heading renamed), L06.html (why-it-matters, Lemma 1.2 prose, lab 1 title/hypothesis/docstring, L06-r1 renamed), tests/labs/E2/lab-E2-L05-1.py, lab-E2-L06-1.py. L04 and L04 twin byte-identical. Two round-5 FAILs (E2b-labs-L05-docstring, E2b-terms-agency-cost-before-definition) are fixed. New FAILs: E2b-grades-L06 (key-results sentence attributes the 50,000 agency cost to the no-limited-liability case) and E2b-terms-linear-vs-affine (terminology drift). Not checked: abstracts of the three cited papers (not read; no claim depends on them); a live verify_refs run; render_curriculum, build_site --check, fetch_data --check, full pytest, run_graders, mutate_graders (outside this slice's gates); browser visuals beyond page_smoke; cards.json rows other than E2-c067 (slice d); mypy.",
 "summary": "E2-b round 6: FAIL. 43 rows: 41 PASS, 2 FAIL (E2b-grades-L06 medium, E2b-terms-linear-vs-affine low). Round-5 FAILs fixed. All recomputed numbers, the three labs (run_labs PASS), page/twin equality, pytest and ruff pass on this pin.",
}
errs = ledger.validate(d, "E2-b")
print("validation:", errs)
json.dump(d, open("ledgers/E2/E2-b.json", "w"), indent=2, ensure_ascii=False)
print(len(rows), sum(r["status"] == "PASS" for r in rows))
