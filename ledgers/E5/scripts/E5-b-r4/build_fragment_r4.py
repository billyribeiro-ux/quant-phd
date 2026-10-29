"""Writes ledgers/E5/E5-b.json (round 4). Evidence strings cite the scripts and outputs under ledgers/E5/scripts/E5-b-r4/."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
S = "ledgers/E5/scripts/E5-b-r4/"
PREV = "Carried from round 3 (course/modules/E/E5/L04.html, L05.html, L06.html and tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py byte-identical since ccfdf4c; re-run at b276325): "

def row(i, check, loc, status, ev, fix=""):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("E5b-inventory", "2.9 structure", "course/modules/E/E5/L04.html, L05.html, L06.html; tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS",
     "Read in full, line by line (L04 1-580, L05 1-499, L06 1-539). Every hunk of `git diff ccfdf4c b276325` in these pages and in cards.json, index.html read (/tmp/e5b_r4_diff.txt, 271 lines; scratch, not kept). Twins: `git diff --quiet ccfdf4c b276325 -- <twin>` exit 0 for all three, so twin rows are re-run, not carried. Delta in slice: L04 why-it-matters, A3 dfn, M3 solution; L05 why-it-matters, A2/Def 1.1 notation Y^s, Remark 2.3 title, quiz q7 explain; L06 why-it-matters, A2, Prop 2.1 sentence, Remark 2.2 unchanged, §4 bullets, quiz q10 explain, references; cards E5-c053..c104 for these lessons; index.html L04/L05/L06 card titles."),
 row("E5b-cmd-check_pages", "2.9 structure", "tools/check_pages.py --unit E5", "PASS", S + "out_check_pages.txt: 'check_pages E5: PASS' (run at b276325)."),
 row("E5b-cmd-check_dag", "2.9 DAG", "tools/check_dag.py --unit E5", "PASS", S + "out_check_dag.txt: 'check_dag E5: PASS'. New links: L04 A3 dfn 'expected inflation' has no concept link (plan §3 L06 says no concept link, DAG D1); L06 'natural rate' and 'Phillips curve' links resolve to #def-natural-rate-of-unemployment and #def-phillips-curve (L06.html:84, :79)."),
 row("E5b-cmd-run_labs", "2.5 labs", "tools/run_labs.py --unit E5 --page L04 / L05 / L06", "PASS", S + "out_run_labs.txt: 'run_labs E5: PASS (1/1)' three times."),
 row("E5b-cmd-verify_refs", "2.1 citations", "tools/verify_refs.py --unit E5; tools/verify_refs.py --offline", "PASS", S + "out_verify_refs_live.txt: 'live re-verification of E5: 4 of 560 entries, 0 problems'; " + S + "out_verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems'."),
 row("E5b-lab-twin-isolated", "2.5 labs", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS", S + "out_check_labs_b.txt: 'L04/L05/L06 ... page_code_equals_twin=True expected_equals_output=True', 'ALL_OK', exit 0 (each twin run with python -I -W error from cwd /tmp). Recomputed by ledgers/E5/scripts/E5-b-r4/check_labs_b.py."),
 row("E5b-lab-lint-types", "2.5 labs", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS", S + "out_ruff.txt: 'All checks passed!', '11 files already formatted'; " + S + "out_mypy.txt: 'Success: no issues found in 11 source files' (mypy --no-incremental tests/labs/E5)."),
 row("E5b-lab-pytest", "2.5 labs", "tests/test_labs.py -k E5", "PASS", S + "out_pytest_labs_E5.txt: '11 passed, 192 deselected'."),
 row("E5b-lab-page_smoke", "2.9 page smoke", "tools/page_smoke.py --unit E5 --pages L04 / L05 / L06 (each alone)", "PASS", S + "out_page_smoke.txt: 'page_smoke modules/E/E5/L04.html: PASS', L05 PASS, L06 PASS; each lab 0.0 s; 'page_smoke E5: PASS'."),
 row("E5b-cit-hicks", "2.1 citations / plan §3 L04 and §7.1", "course/modules/E/E5/L04.html:566 (References)", "FAIL",
     "L04.html:566 names the key only as text: `<code>hicks1937mr</code>`, with no data-cite. course/assets/js/refs.js renderCitations() builds ol[data-references] only from elements with [data-cite] (refs.js:72, 'order' list), so the L04 References list renders empty while the paragraph says 'names one source at paper level'. The same subject in L06.html:525 uses `<span data-cite=\"phelps1968money\">` and renders its entry. plans/E5-build-plan.md §3 L04 requires hicks1937mr 'cited at paper level'; §7.1 says 'L04 is-lm-model (paper level)'. The round-3 PASS accepted the <code> form and is not carried.",
     "In course/modules/E/E5/L04.html:566 replace <code>hicks1937mr</code> with <span data-cite=\"hicks1937mr\">hicks1937mr</span>, keeping the sentence unchanged (no locator, no result attributed), so the same paper-level form as L06.html:525 renders the reference entry."),
 row("E5b-cit-L05-L06-none", "2.1 citations", "course/modules/E/E5/L05.html:485; L06.html:525", "PASS",
     "L05.html:485 says 'cites no outside source for its results' and has no data-cite. L06.html:525 has data-cite=\"phelps1968money\" at paper level, no data-locator, and says 'has not read that paper, so it gives no locator and attributes no result to it' (plan §3 L06, §7.1 'L06 phillips-curve and natural rate (paper level)'). grep 'data-cite' in E5 pages: index.html:178-181, project.html:761-764 (other slices), L06.html:525, L04.html:566 (no attribute)."),
 row("E5b-cit-phelps-plan", "2.1 citations / plan §3 L06 and §7.1", "course/modules/E/E5/L06.html:525", "PASS",
     "Round-3 FAIL is fixed: L06.html:525 now `<span data-cite=\"phelps1968money\">phelps1968money</span>` for the expectations-augmented construction, paper level, no locator, no result attributed. Matches plans/E5-build-plan.md §3 L06 and §7.1. check_pages key check passes (" + S + "out_check_pages.txt). Registry: 'verify_refs --unit E5: 4 of 560 entries, 0 problems'."),
 row("E5b-num-L04", "2.2 numbers", "course/modules/E/E5/L04.html why-it-matters, Derivation 2.2, Props 3.2/4.2/4.3, Remarks 4.4/4.5, M1-M3, E1-E3, Lab 1 expected block", "PASS",
     S + "out_rederive_r4.txt (Fraction, independent of the twin): A=3, D=5/4, Y*=28/5, i*=4/5, h/D=4/5, 1/(1-c)=4, b/D=8/5, -(1-c)/D=-1/5, M1 D=3 Y*=14/3 i*=5/6 with IS/LM checks 4 and 3, M2 2/3 and ratio 1/3, M3 2/3 and -1/6, misconception G 1->2: dY=4/5, di=2/5, E1 ratio 1/2, E3 share 1/5, R1 h/D=4 at d=0. All OK. Also " + S + "out_rederive_b.txt ALL_OK."),
 row("E5b-num-L05", "2.2 numbers", "course/modules/E/E5/L05.html why-it-matters, Props 2.1/2.2/3.1, Remarks 2.3/3.2, misconceptions, M1-M3, E1-E3, R2, Lab 1 expected block", "PASS",
     S + "out_rederive_r4.txt: P*=6/5, Y*=1040, dP=1/10, dY=20, demand 1060 at P=1 and 1000 at P=1.6 (misconception: fall 60), LR 8/5 and 19/10, share 1/3 at nu=50 and 8/9 at nu=800, price change 3/50 at nu=400, output increment 8/3, M1 P*=21/20 Y*=995, M2 share 3/4 dY=30 dP=1/5, M3 1 and 7/5, R2 P*=3/2 Y*=1040, stuck-expectation point Y=1060 gap 60, E2 increments 5,5,4,8/3, Remark 2.3 limit 1. All OK."),
 row("E5b-num-L06", "2.2 numbers", "course/modules/E/E5/L06.html Prop 2.1 sentence, Remark 2.2, Part A/B/C, misconceptions, M1-M3, E1-E3, R1-R2, quiz", "PASS",
     S + "out_rederive_r4.txt: beta=5/6 at P=6/5, 1 at P=1; Part A expected price 309/250 (1.236), price 613/500 (1.226), inflation 13/600 both ways; change at gap -0.01 is 1/120; change at 3 percent is 1/60; M1 beta 1/2 pi 0.03; M2 beta 4/5 pi 0.048; M3 change -3/200, pi 1/200; R2 u=31/500 (6.2 percent); R1 ratio 6/5; E3 -29/6000 and 5.5 percent -1/240. Seeded path re-drawn with random.Random(20261028): 12 rows match the printed Part B values, 9 positive gaps all with negative change, 3 negative gaps all with positive change, zero_gap 0, no_change 0. Prop 2.1 'rise of 100 percentage points' is the unit convention of u as a decimal (L06.html:52, Unemployment rates are decimals)."),
 row("E5b-prose-scope", "2.9 prose", "L04-L06 added and changed sentences containing only, all, always, every, any, exactly, same", "PASS",
     "Scope words in added lines (grep of /tmp/e5b_r4_diff.txt '+' lines): 'exactly for its unique equilibrium' (L04 Prop 3.2); 'exactly, because the system is linear' (L04 M3, computed); 'exactly when unemployment differs from the natural rate' (L06 why-it-matters, Cor 3.2 'if and only if'); 'holds vacuously on this path' (L06 quiz q10, with no_change_periods 0); 'every saving rate' is L03 (not this slice). No new unsupported 'only/all/always' claims."),
 row("E5b-math-L04", "2.4 mathematics", "L04.html Derivation 2.2, Prop 3.2, Prop 4.2, Prop 4.3, Remarks 4.4-4.5, P1-P3, R1-R3", "PASS",
     "Determinant of [[1-c, b],[d, -h]] is -D (L04.html:126); Cramer formulas checked by substitution in the page's own proof and by " + S + "out_rederive_r4.txt; Prop 4.2 derivatives match Prop 3.2 (A_G=1, A_Tax=-c); Prop 4.3 'h(1-c) <= D iff 0 <= bd' correct; P2 'strict iff bd > 0' correct; P3 slopes -(1-c)/b and d/h correct; R1 and R3 correct. The added sentence in M3 has no new claim beyond 'exactly'."),
 row("E5b-math-L05", "2.4 mathematics", "L05.html Props 2.1, 2.2, Remarks 1.2, 2.3, 3.2, Prop 3.1, canon-break bullets, P1-P3, R1-R3", "PASS",
     "Prop 2.1 algebra (eta+nu)P = a - Ybar + nu Pe, and Prop 2.2 Delta P = Delta a/(eta+nu), Delta Y = nu Delta a/(eta+nu) re-derived (L05.html:96, :110). Remark 1.2 (IS-LM output affine in 1/P with slope bM/D; zero iff b=0 under M>0, Lesson 4 Remark 4.4) checked against L04.html Prop 3.2 and Definition 2.1. Remark 2.3 limit 1 and the new title are correct. Prop 3.1 fixed point identity correct (L05.html:245). R1 uniqueness proof (intermediate value theorem and strict monotonicity of H) is complete under the stated F."),
 row("E5b-math-L06", "2.4 mathematics", "L06.html Prop 2.1 (proof), Prop 3.1 and proof, Cor 3.2 and proof, Remark 3.3, §4 bullets, P1-P3, R1-R3", "PASS",
     "Prop 2.1 proof re-derived (L06.html:100-104): P_t - P^e_t = (Y_t - Ybar)/nu, substitution, division by P_{t-1}; the first term equals pi^e_t exactly because P^e_t = P_{t-1}(1+pi^e_t). Prop 2.1 now states 'Holding P_{t-1} and pi^e_t fixed' (L06.html:95), which is the derivative in u with the other two arguments fixed. Prop 3.1 'iff' chain correct. Cor 3.2 correct under A3. Remark 3.3 'only unemployment rate' correct by Prop 3.1. §4 supply-shock bullet: u^n + v/beta correct (v=0 gives u^n). Definition 1.2 uniqueness correct."),
 row("E5b-notation", "2.4 / 2.9 notation", "L04-L06 all math; notation/notation.json (symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q; macros)", "PASS",
     "Pages use only standard LaTeX macros (\\nu, \\eta, \\bar, \\pi, \\partial, \\ast, \\beta, \\Delta, \\kappa, \\mathrm, ...; no program macro such as \\E, \\R, \\Var). None of the registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} appears in L04-L06 (grep, empty). The change Y^{\\nu} -> Y^{\\mathrm{s}} (L05.html:65, :75) removes a reuse of the slope letter nu for a supply quantity. Within slice: beta (Phillips slope, L06), nu (AS slope, L05/L06), eta, kappa, b, d, h, c, m-bar used with one meaning each. Plans/E5-build-plan.md §3 L06 says 'Expected inflation is written with the \\E macro'; notation.json defines \\E as 'expectation operator', and L06 writes pi^e_t: plan-conformance note, not a FAIL (see notes)."),
 row("E5b-define-L06-natural-rate", "2.9 define-before-use", "course/modules/E/E5/L06.html:68-70 (A2) vs Definition 1.2 at :83-85", "PASS",
     "Round-3 FAIL fixed: A2 (L06.html:69) now says 'The number u^n is a parameter of the model, and Definition 1.2 below gives its meaning' and no longer uses the term 'natural rate'. The term first appears in why-it-matters (L06.html:52) with the pointer '(Definition 1.2 below)', and in Definition 1.2 (L06.html:84). Phillips curve likewise pointed at Definition 1.1 (L06.html:52)."),
 row("E5b-define-dup-expected-inflation", "2.9 nothing defined twice", "course/modules/E/E5/L04.html:89 (A3) and course/modules/E/E5/L06.html:60 (§1)", "FAIL",
     "The term 'expected inflation' is defined by a dfn in two lessons of E5: L04.html:89 `<dfn>expected inflation</dfn>, the inflation rate expected for the period, is zero` (added in this round; `git diff ccfdf4c b276325` hunk @@ -86,7 +86,7 @@) and L06.html:60 `<dfn>expected inflation</dfn> ... is the inflation rate that is expected for period t`. grep -o '<dfn[^>]*>' over E5 pages lists the term twice. Plan §2.9 requires nothing defined twice; L04 A3 is also the only L04 dfn without id (other L04 dfns share that pattern, so this is the duplicate, not the style).",
     "In course/modules/E/E5/L04.html:89 remove the <dfn> tags so the words read plain ('and expected inflation, the inflation rate expected for the period, is zero' becomes 'and expected inflation is zero'), keeping the single definition in L06.html:60."),
 row("E5b-title-L04", "2.9 hub titles (plan §2.2 'Hub lesson titles match each lesson's <h1>')", "course/modules/E/E5/index.html:149 vs L04.html:36", "PASS",
     "Round-3 FAIL fixed: index.html:149 card-title 'Business cycles and the IS–LM model' equals L04.html:36 h1 'Business cycles and the IS–LM model'. L05 card (index.html:150) 'Aggregate Demand and Aggregate Supply' equals L05 h1; L06 card (index.html:151) 'The Phillips Curve and the Natural Rate' equals L06 h1 (grep of card-title and h1)."),
 row("E5b-nav", "2.9 structure", "L03.html -> L04.html -> L05.html -> L06.html -> L07.html lesson-nav labels", "PASS",
     "L04 nav: Previous 'L03 · The Solow growth model' equals L03 h1; Next 'L05 · Aggregate Demand and Aggregate Supply' equals L05 h1. L05 nav: L04 and L06 labels equal their h1s. L06 nav: Previous 'L05 · Aggregate Demand and Aggregate Supply', Next 'L07 · Central-Bank Policy and the Taylor Rule' equals L07 h1."),
 row("E5b-struct-L04-L06", "2.9 structure", "L04-L06 section order and minimum counts", "PASS",
     "check_pages E5 PASS (" + S + "out_check_pages.txt). Section order read in L04 (why-it-matters, §1 to §9 incl. quiz and references), L05 and L06 (same order, §1 to §9). Problem sets: L04 M1-M3, P1-P3, E1-E3, R1-R3; L05 M1-M3, P1-P3, E1-E3, R1-R3; L06 M1-M3, P1-P3, E1-E3, R1-R3. Each problem has a solution block; key-results table present; quiz present."),
 row("E5b-banned-process", "2.9 banned phrases", "L04-L06 full text", "PASS",
     "check_pages banned-phrase scan over main text PASS. Own grep of L04-L06 for builder, verifier, round N, TODO, FIXME, we, our, I, draft, placeholder, TBD, revised: one hit, 'd Y - h i' inside a Python docstring (L04.html:242), not prose."),
 row("E5b-grades", "2.3 grades", "L04 Prop 3.2, 4.2, 4.3; L05 Props 2.1, 2.2, 3.1; L06 Props 2.1, 3.1, Cor 3.2 and key-results tables", "PASS",
     "Each claim with data-grade T is proved on the page (L04.html:117, :137, :156; L05.html:86, :100, :235; L06.html:90, :268, :278). Key-results rows: L06 Lab Part B row graded C (L06.html:435, 'SIMULATED, one seed') and all others T; a C-graded lab claim names the lab. Grades independent of BLUEPRINT §3 read: T for theorems derived in closed form."),
 row("E5b-labs-simulated", "2.5 labs / 2.8 data", "lab-E5-L06-1 hypothesis (L06.html:114) and docstring (:117); L04 and L05 hypothesis and docstring", "PASS",
     "L06 lab says 'The lab is SIMULATED' and uses random.Random(seed) with seed 20261028 (L06.html:144, lab code). L04 says 'illustrative parameters, not data' and 'no random draws'. L05 says 'illustrative model units, not data' and 'Nothing is random'. No dataset is read by these labs."),
 row("E5b-problems-quiz", "2.6 / 2.9 problems and quiz", "L04-L06 problem sets and retrieval quiz answers and explanations", "PASS",
     "All solution blocks recomputed (" + S + "out_rederive_r4.txt covers every number). Quiz keys: L04 q1-q10 (5.6, 0.8, 4, -0.2, the sign and slope claims) correct; L05 q1-q10 (1.2, 1040, -eta, 20, 0.1, 'strictly between 0 and 1', 0.3, potential output, A3) correct; L06 q1-q10 (1, 0.008333, 0.021667, 0.048, the Phillips slope proportional to 1/P) correct. The L05 q7 explanation has a spacing defect, recorded in its own row."),
 row("E5b-prose-L05-q7-explain", "2.9 prose", "course/modules/E/E5/L05.html:455 (quiz q7 explanation)", "FAIL",
     "Text reads '(Remark 2.3 for the dependence on \\(\\nu \\);Proposition 2.2 gives' with no space after the semicolon (verified by grep ';Proposition' at L05.html:455). The math is right; the typo was introduced in this round (round-3 text had '; Proposition').",
     "In course/modules/E/E5/L05.html:455 change ';Proposition 2.2' to '; Proposition 2.2'."),
 row("E5b-interp-labs", "2.5 labs / 2.9 prose", "L04, L05, L06 'interpretation' paragraphs and lab hypotheses", "PASS",
     "L06 interpretation (L06.html:262) now says 'no period with a nonzero gap has an unchanged inflation rate' and 'holds only vacuously here'. Matches the code (no_change_only_at_zero_gap = AND of (new != old or gap == 0), L06.html:189-202, lab code) and the output (no_change_periods 0). L04 and L05 interpretation paragraphs match their expected blocks (L04.html:331; L05.html:229)."),
 row("E5b-cards-dup-scan", "2.7 retrieval cards", "course/modules/E/E5/cards.json (130 cards, all lessons)", "PASS",
     S + "out_cards_check.txt: 130 cards; lesson counts L01 23, L02 13, L03 16, L04 18, L05 17, L06 17, L07 14, L08 12; duplicate ids []; duplicate fronts []."),
 row("E5b-cards-L04-L06", "2.7 retrieval cards (one row per card group, all 52 read)", "cards.json E5-c053..E5-c070 (L04), E5-c071..E5-c087 (L05), E5-c088..E5-c104 (L06)", "PASS",
     "All 52 cards read against the current lesson text (" + S + "out_cards_check.txt). Changed cards agree: c065 (Prop 4.3, bd >= 0), c071 (Def 1.1), c066/c068 (Remark 4.4, Problem R1). Numbers on cards appear in their lesson: 28/5, 4/5, 1060, 1000, 1040, 0.333333..0.888889, 0.033333, 0.016667, 0.008333, 13/600, 1.236, 1.226 (in the lesson's expected blocks or prose). Cards carrying a grade field: T on c059, c062, c064, c065, c066, c067, c068, c069, c079-c084, c086, c087, c095-c098, c100, c102, c104; C on c103 (SIMULATED); definitional cards (for example c094, c053-c058) carry no grade field and make no empirical claim. Card c060 uses 'only' for the equilibrium sense; L04.html:105 says 'the word has that sense', a paraphrase, not a claim beyond the lesson."),
 row("E5b-card-c095", "2.7 retrieval cards (agree with the CURRENT lesson, carry hypotheses)", "course/modules/E/E5/cards.json id E5-c095 (back field) vs course/modules/E/E5/L06.html:95 (Prop 2.1)", "FAIL",
     "Card back: 'At a fixed P(t-1), inflation falls by beta(t) for each one-unit rise in u(t).' Current Prop 2.1 (L06.html:95): 'Holding P_{t-1} and pi^e_t fixed, the inflation rate falls by beta_t for each rise of one unit in u_t, which is a rise of 100 percentage points.' The card drops the pi^e_t hypothesis, which Prop 2.1 now states explicitly, and the unit convention. Verified in ledgers/E5/scripts/E5-b-r4/out_cards_check.txt.",
     "In course/modules/E/E5/cards.json, E5-c095 back: replace 'At a fixed P(t-1), inflation falls by beta(t) for each one-unit rise in u(t).' with 'Holding P(t-1) and expected inflation pi^e(t) fixed, inflation falls by beta(t) for each one-unit rise in u(t), a rise of 100 percentage points.'"),
]

fragment = {
    "unit": "E5",
    "slice": "E5-b",
    "round": 4,
    "verifier": "Haiku independent verifier, E5 slice b round 4 (did not build E5)",
    "pin": "b276325",
    "base": "ccfdf4c (round-3 pin); round-3 fragment /Users/billyribeiro/.fanout/frags/C-E5-b.round3.json used as context only; rows re-verified from the pin, Carried-from prefixes not used because the cited subjects were re-run",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-E5-b (detached at b276325, .venv symlinked)",
    "scratch": "/tmp (e5b_r4_diff.txt, e5b_cards_r4.txt)",
    "verified_at": "2026-10-28",
    "verdict": "",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "verify_refs: live 4 of 560 entries, 0 problems; offline 560 entries, 0 problems (" + S + "out_verify_refs_*.txt). references/ unchanged in ccfdf4c..b276325 for E5 keys."
    ],
    "freshness_flags": [],
    "notes": [
        "Mutants: none required. E5 is a rubric unit with no autograder (plan §10; VERIFIER_RULES §2.6 applies to projects only). tools/mutate_graders.py was not run for E5.",
        "Non-blocking, for the architect: L05.html:52 (why-it-matters) and L06.html:52 use 'price level' and 'adaptive expectations' before their definitions in §1 and A3 without a pointer. Preview paragraphs; not counted as a row. Round-3 did not flag them either.",
        "Non-blocking, plan conformance: plans/E5-build-plan.md §3 L06 says expected inflation 'is written with the \\E macro', but notation/notation.json defines \\E as the expectation operator and the page writes pi^e_t. The registry meaning governs; the plan wording should be corrected by the architect.",
        "Not checked: the hub (index.html) beyond L04-L06 titles and cards; cards for L01-L03, L07, L08; project.html; the lab twins of other lessons; check_projects; run_graders (rubric unit); lesson hours arithmetic (hub split is another slice's row).",
    ],
    "summary": "",
}
n = len(rows)
fails = [r for r in rows if r["status"] != "PASS"]
fragment["verdict"] = "PASS" if not fails else "FAIL"
fragment["summary"] = f"rows={n} pass={n - len(fails)} fail={len(fails)} unverifiable=0; mutants 0/0 (rubric unit)"
out = root / "ledgers/E5/E5-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(out, fragment["verdict"], fragment["summary"])
