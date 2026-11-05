"""Build ledgers/LX1/LX1-b.json (round 13) and validate it with tools/ledger.py. Every round-12 row id is kept."""
import json
import subprocess
import sys
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE13-LX1-b"
sys.path.insert(0, f"{ROOT}/tools")
import ledger  # noqa: E402

O = "ledgers/LX1/scripts/LX1-b-r13/out"
PASS, FAIL = "PASS", "FAIL"
R12_IDS = json.load(open("/tmp/lx1b-r13-r12ids.json"))

rows = {}


def row(rid, check, location, status, evidence, fix=""):
    rows[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}


G = f"exit 0, output {O}/"
row("lx1b-check-pages", "2.9 structure", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", PASS,
    f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', {G}check_pages.out.")
row("lx1b-check-dag", "2.9 DAG", "course/modules/LX/LX1/L03.html; course/modules/LX/LX1/L04.html", PASS,
    f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', {G}check_dag.out. Own dfn list: scans_r13.py section 3 ({O}/scans_r13.out).")
row("lx1b-check-projects", "2.6 / 2.9 unit tools", "course/modules/LX/LX1/project.html (unit gate)", PASS,
    f"tools/check_projects.py --unit LX1 -> 'check_projects LX1: PASS', {G}check_projects.out. Project content is slice e, not checked here.")
row("lx1b-run-graders", "2.6 autograder", "tools/run_graders.py --unit LX1", PASS,
    f"'run_graders LX1: no autograder (grading: rubric)', {G}run_graders.out. No grader or mutant applies to LX1.")
row("lx1b-dag-links", "2.9 DAG links", "L03.html (L02.html#def-debt-deflation, #def-gold-standard); L04.html (concepts.html#exponential-and-logarithm, L02.html#def-gold-standard, L03.html#def-lender-of-last-resort, #def-bretton-woods-system)", PASS,
    f"scans_r13.py section 3: every concept href resolves to an id in its target file (all 'OK'; {O}/scans_r13.out). concepts.html anchor exponential-and-logarithm (M1, in closure).")
row("lx1b-dag-outside-closure", "2.9 DAG (plan section 4, D1-D15)", "L03.html; L04.html", PASS,
    f"scans_r13.py section 1: outside-closure names (bank run, fire sale, leverage cycle, banking crisis, currency crisis, covered/uncovered interest, efficient market, moral hazard, Fisher, bank reserve, credit default, contagion, term spread, expected inflation, sovereign, deposit insurance) absent from both pages. No outside-closure concept is linked (section 3).")
row("lx1b-run-labs", "2.5 labs", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', {G}run_labs.out.")
row("lx1b-twin-alone-L03", "2.5 labs (twin alone)", "tests/labs/LX1/lab-LX1-L03-1.py", PASS,
    f"Copied alone to /tmp/lx1b-r13/L03, 'python -I -W error lab-LX1-L03-1.py': exit 0, empty stderr ({O}/twin_L03.err, {O}/twin_L03.out).")
row("lx1b-twin-alone-L04", "2.5 labs (twin alone)", "tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"Copied alone with data/fx_monthly.csv to /tmp/lx1b-r13/L04, 'python -I -W error': exit 0, empty stderr ({O}/twin_L04.err, {O}/twin_L04.out).")
row("lx1b-twin-equals-page-code", "2.5 labs (page code = twin; expected = output)", "L03.html data-run lines 150-326, expected 327-382; L04.html data-run 115-304, expected 305-321", PASS,
    f"compare_r13.py ({O}/compare_r13.out): page code equals twin source for L03 and L04; expected blocks equal the twins' stdout line for line (56 and 17 lines); 'ALL EQUAL: True'.")
row("lx1b-page-smoke-L03", "2.9 page_smoke (alone)", "course/modules/LX/LX1/L03.html", PASS,
    f"tools/page_smoke.py --unit LX1 --pages L03 -> 'page_smoke modules/LX/LX1/L03.html: PASS', exit 0 ({O}/page_smoke_L03.out).")
row("lx1b-page-smoke-L04", "2.9 page_smoke (alone)", "course/modules/LX/LX1/L04.html", PASS,
    f"tools/page_smoke.py --unit LX1 --pages L04 -> 'page_smoke modules/LX/LX1/L04.html: PASS', exit 0 ({O}/page_smoke_L04.out).")
row("lx1b-ruff-mypy", "2.5 / conventions", "tests/labs/LX1/lab-LX1-L03-1.py; tests/labs/LX1/lab-LX1-L04-1.py", PASS,
    f"ruff check tests/labs/LX1 'All checks passed!' exit 0; ruff format --check '7 files already formatted' exit 0; mypy --no-incremental on both twins 'Success: no issues found in 2 source files' exit 0 ({O}/ruff_check.out, ruff_format.out, mypy_L03_L04.out).")
row("lx1b-pytest", "2.5 labs (tooling tests)", "tests/test_labs.py; tests/test_page_checks.py (-k LX1)", PASS,
    f"python -m pytest tests/test_labs.py tests/test_page_checks.py -q -k LX1 exit 0 ({O}/pytest_LX1.out); collect-only count in {O}/pytest_collect_LX1.out.")
row("lx1b-verify-refs", "2.1 citations (registry run)", "references/references.json", PASS,
    f"tools/verify_refs.py --offline exit 0 ({O}/verify_refs_offline.out); tools/verify_refs.py --unit LX1 exit 0: 'live re-verification of LX1: 4 of 560 entries, 0 problems' ({O}/verify_refs_unit_LX1.out).")
row("lx1b-citations-L03", "2.1 citations", "L03.html:405 (span data-cite, canon-breaks), L03.html:640 (References)", PASS,
    "Only key friedman1963monetary is cited (L03.html:405, :640). Registry record references/references.json:9400-9412: title 'A monetary history of the United States 1867-1960', author Friedman, year 1963; the page quotes the title and never types the second author (N2). The page attributes no finding to the book ('This lesson attributes no account to it').")
row("lx1b-citations-L04", "2.1 citations", "L04.html section 9 (lines 569-575)", PASS,
    "L04 cites no registry key; it cites the Fed H.10 dataset by its MANIFEST citation and retrieval date (L04.html section 9; course/assets/data/market/MANIFEST.json:36-40). grep for Bernanke, Kindleberger, Garber in L03/L04: no hit.")
row("lx1b-fetch-check", "2.8 data (MANIFEST, offline)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json", PASS,
    f"tools/fetch_data.py --check exit 0: 'fetch_data: 3 datasets, 0 problems' ({O}/fetch_check.out).")
row("lx1b-fx-rebuild", "2.8 data (reproducible sha256)", "course/assets/data/market/fx_monthly.csv; MANIFEST.json fx_monthly (sha256 60572240...)", PASS,
    f"fx_rebuild_and_licence_r13.sh: git archive e919577 into /tmp/lx1b-r13-scratch-fx, tools/fetch_data.py --fetch --only fx_monthly against the live H.10 feed: 'built fx_monthly: 669 rows, 67392 bytes, 1971-01 to 2026-09'. sha256 of the rebuilt file = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256 = checkout file ({O}/fetch_rebuild_fx_monthly_r13.out). retrieved 2026-10-19 not changed.")
row("lx1b-fx-licence", "2.8 licence (quote on issuer page)", "tools/data_sources.yaml fx_monthly (licence, licence_url); MANIFEST fx_monthly.licence", PASS,
    f"curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 ({O}/curl_fed_disclaimer_code.out). The page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information' ({O}/fed_licence_quote.out). Grant matches tools/data_sources.yaml:57-60 and MANIFEST.json:37-38.")
row("lx1b-fx-guard", "2.5 labs (fail loud on bad data)", "tests/labs/LX1/lab-LX1-L04-1.py parse_rate, load_column", PASS,
    "parse_rate raises ValueError on a non-decimal or blank cell and on a non-positive rate; load_column raises on a missing column, a non-YYYY-MM label and a non-consecutive month; no row is skipped (read in full, twin lines 50-90).")
row("lx1b-fx-gbp-clean", "2.8 data (blank cells)", "course/assets/data/market/fx_monthly.csv (GBP column)", PASS,
    f"scans via rederive_r13.py ({O}/rederive_r13.out): 669 data rows, months contiguous, 'blank GBP cells: 0'.")
row("lx1b-honest-data", "2.2 honest data", "L03.html:76, :147-152; L04.html:7, :113-114, :120-122", PASS,
    "L03 is SIMULATED with an honest-pending note (L03.html:76) stating no redistributable historical series is embedded; L04 names its only dataset, licence and retrieval date (L04.html:113-114). No historical number appears in either page without a source.")
row("lx1b-L04-simulated-label", "2.5 labs (SIMULATED labelling)", "L04.html:113-114; twin docstring; expected block line 305", PASS,
    "Part A is labelled SIMULATED in the lab title (L04.html:113), in the hypothesis (:114), in the twin docstring and in the expected block (line 305). Parts B-D are not labelled SIMULATED and read only fx_monthly.csv.")
row("lx1b-L04-manifest-note", "2.8 data (BUILDER_RULES 6.6 dataset in a lab)", "tests/labs/LX1/lab-LX1-L04-1.py docstring lines 1-30; L04.html:113-114, :120-122", PASS,
    "data-files lists fx_monthly.csv (L04.html:112); the hypothesis cites the dataset citation and MANIFEST retrieval date 2026-10-19; the twin docstring states the transform (month-end, last value in the month; CAD, CHF, DKK, JPY, NOK, SEK inverted: MANIFEST.json transform, matches) and the GBP direct quote.")
row("lx1b-open-items-missing", "2.9 open items", "plans/LX1-open-items.md", PASS,
    "plans/LX1-open-items.md present; D-1 (L03 data request) and the Bretton Woods and reference requests are recorded (read in full).")
row("lx1b-num-L03-depth", "2.2 numbers (L03 depths, difference)", "L03.html Part B (expected block lines 327-382), E2 solution, quiz items, key results row 4", PASS,
    f"rederive_r13.py ({O}/rederive_r13.out): depth X = 9.204597 percent -> 9.20; depth Y = 2.686713 -> 2.69; first reached t=12 and t=4; difference 6.517884 -> 6.52 (interpretation, E2); printed 9.20 - 2.69 = 6.51 (E2). E1 exact 2.6867 percent verified.")
row("lx1b-num-L03-path", "2.2 numbers (L03 Part A paths)", "L03.html expected block 327-382; M1 :439-441; M2 :446-448; M3 :452-455; E1-E3", PASS,
    f"rederive_r13.py: every index, real debt (cents), leverage, premium and output-fall value for X and Y in the expected block matches the independent Fraction computation (all 26 rows). M1: P4 = 5764801/6250000 = 0.92236816, V4 = 1084165.7847 -> 1084166. M2: N4 = 3915834.2153 -> 3915834. M3: L4 = 0.2768671 -> 0.2769. Quiz 9: real debt X t=12 = 1274345.2124 -> 1274345 ({O}/rederive_r13.out).")
row("lx1b-num-L04-stats", "2.2 numbers (L04 dispersions, counts)", "L04.html expected block 305-321; interpretation; key results rows 3-4; quiz", PASS,
    f"rederive_r13.py (independent parse of fx_monthly.csv): window one 668 changes, sd 0.027935278 -> 0.027935; window two 321 changes (1999-12 base), sd 0.024699501 -> 0.024700; ratio 0.8841688 -> 0.8842; exact zeros 1976-07, 2012-07, 2019-11 (3), nonzero 665; largest |change| 0.135846 at 1985-03 and 0.096575 at 2008-10 (signed -0.096575) ({O}/rederive_r13.out).")
row("lx1b-num-L04-display-diff", "2.2 numbers (display vs unrounded)", "L04.html interpretation (expected block 305-321 following line); :472; quiz Q7 :528", PASS,
    "Unrounded difference s2 - s1 = -0.0032358 -> -0.003236 (printed). Difference of the two printed figures 0.024700 - 0.027935 = -0.003235, as the interpretation states. Both correct and the page says which is which.")
row("lx1b-num-L04-derived", "2.2 numbers (derived on page)", "L04.html M1, M2, M3 (mech-1..3), P2, R2, E2, misconception 3, quiz ln 1.1 and band bound", PASS,
    f"rederive_r13.py: M1 ln 1.1 = 0.0953101798 -> 0.095310, simple 0.100000, difference 0.004690; M2 mean 1/150, sd sqrt(19/30000) = 0.025166; E2 exp(-0.0965747...) - 1 = -0.092058; R2 h = tanh(z/2) = 0.067819 (z = 0.1358457), rounded 0.0678 gives bound 0.135808 < z; quiz band bound ln(1.0678/0.9322) = 0.135808 -> 0.1358 ({O}/rederive_r13.out).")
row("lx1b-scope-start", "2.9 scope (window two start)", "L04.html:110, :325; card LX1-c063", PASS,
    "Window two = changes dated 2000-01 to 2026-09 (321, first change uses the rate of 1999-12, rederive_r13.out). fx_daily and ust_daily both 'first 2000-01-03' in MANIFEST.json (lines for each id). The lesson calls the start a convention (L04.html:325, c063) and does not claim a cause.")
row("lx1b-math-L03", "2.4 mathematics", "L03.html:94-142 (Lemma 3.1, Prop 3.2, Cor 3.3, Cor 3.4); :67, :121, :145", PASS,
    f"Read each proof. Lemma 3.1 identity: y/(C-y) - x/(C-x) = C(y-x)/((C-x)(C-y)) (checked by hand, P3). Prop 3.2(a) P_t and V_t bounds, (b) closed form (lambda(V_m) - lambda(D) = V_m/(N0+D-V_m) - D/N0 with lambda(D)=D/N0), (c) first maximiser at t=m. Cor 3.3 needs m'<m<=H (given). Numerically: never falls and strict steps for m=0..12 ({O}/rederive_r13.out).")
row("lx1b-math-L04", "2.4 mathematics", "L04.html:58-107 (Def 1.1, Prop 1.2, Remark 1.3, Def 2.1, Prop 2.2, Remark 2.3)", PASS,
    f"Prop 1.2 telescoping proved by cancellation (read); numerically the sum equals ln(x_b/x_a) to 5.6e-16 (window one) and 7.8e-16 (window two) ({O}/rederive_r13.out). Prop 2.2 (a)-(b) follows from A2 (read). Def 1.1 denominator n-1 with n>=2 stated.")
row("lx1b-math-problems", "2.4 mathematics (problems)", "L03.html:431-530 (M1-M3, P1-P3, E1-E3, R1-R3); L04.html:362-460 (M1-M3, P1-P3, E1-E3, R1-R3)", PASS,
    f"Every problem and worked solution read. Numbers re-derived ({O}/rederive_r13.out). P1 and P3 proofs checked; P2 (L04) bound proof checked; R2 (L04) h = tanh(z/2) with d/dh ln((1+h)/(1-h)) = 2/(1-h^2) > 0 checked.")
row("lx1b-grades", "2.3 grades", "L03.html:124, :134, :541-546 (key results); L04.html:468-473 (key results); cards", PASS,
    "Re-graded against BLUEPRINT section 3: derived results T with proof or lab basis; lab-printed values C with the lab named (e.g., L03 key results row 4-5, L04 rows 3-4). No empirical claim is graded above C; none is made.")
row("lx1b-notation", "2.4 notation (plan section 2.3; never redefined)", "L03.html, L04.html, L02.html:57 (kappa), L04.html:85 (Def 2.1), L03.html:96-103 (lambda), L04.html:59 (ell_t)", PASS,
    f"Re-verified on e919577 ({O}/scans_r13.out section 4): L04 no longer uses kappa (it uses x-bar, Def 2.1); L03 uses lambda (28 math hits) and no ell; L04 uses ell_t only (21). The gold parity term is defined once in L02 (L02.html:57) and L04 Def 2.1 states that its fixed exchange rate is a different object. No registered symbol (notation/notation.json: T, Phi, gamma_3, gamma_4, R^*, R^(e*), R_f, Q-blackboard) appears in L03 or L04. The L03 net-worth symbol N is a separate defect: row lx1b-notation-N.")
row("lx1b-notation-registered", "2.4 notation (registered symbols)", "L03.html; L04.html", PASS,
    "scans_r13.py section 4: L03 math letters CDGHLNPVfkmtxy, L04 abefhknstuxz; none of T, R_f, Q, Phi, gamma_3, gamma_4, R^*, R^{e*} occurs. Macros used: \\R, \\ln only. No \\E, \\Prob, \\Var.")
row("lx1b-concepts-defs", "2.9 concept definitions", "L03.html:86 (def-credit-channel-depression), :389 (def-lender-of-last-resort); L04.html:86 (def-bretton-woods-system placeholder)", PASS,
    "scans_r13.py section 3: L03 defines credit-channel-depression and lender-of-last-resort once each with data-concept; L04 defines bretton-woods-system once (placeholder; see lx1b-L04-bretton-definition). Plain dfn terms (leverage, external-finance premium, central bank, monthly log change, dispersion, anchor currency, fixed exchange rate) are not data-concept.")
row("lx1b-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "L03.html; L04.html", PASS,
    f"scans_r13.py section 1 ({O}/scans_r13.out): TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly and ellipsis in prose: none.")
row("lx1b-process-words", "2.9 learner-visible process words", "L03.html; L04.html", PASS,
    "scans_r13.py section 1: build, builder, round, verifier, REQUEST, unit report, fixer, planner, architect, ruling: none in prose (code and expected blocks excluded).")
row("lx1b-scope-words", "2.9 scope words", "L03.html; L04.html", PASS,
    "scans_r13.py section 2 counts (every, all, never, any, only, same, exactly, the first). Each hit read in context: model statements are bounded by 'in the model' or the assumptions; 'every' appears in proofs or lab-printed facts; 'exactly' qualifies the exact-zero count that the lab prints; 'the first' is the first maximising period (proved).")
row("lx1b-structure", "2.9 structure (BUILDER_RULES 4.2)", "L03.html sections 1-10; L04.html sections 1-9", PASS,
    "L03: model, definitions, closed form, lender, canon breaks, misconceptions (4), problem set (3 per tier), key results, quiz (11 items), references. L04: monthly log changes, model, recorded column, canon breaks, misconceptions (4), problem set (3 per tier), key results, quiz (11 items), references. Counts from the pages; check_pages PASS.")
row("lx1b-quiz-explanations", "2.9 quiz explanations vs lesson", "L03.html:553-636; L04.html:483-560", PASS,
    f"Each explanation read against its lesson section: L03 Q1 (Assumption 1.1), Q2 (premium zero at baseline), Q3-Q4 (Lab 1 Part B; Prop 3.2(c)), Q5 (Cor 3.3), Q6 (Part D, Cor 3.4), Q8 (real debt 1274345), Q9 (Y unchanged periods = 8), Q10 (Definition 4.1), Q11 (Section 5). L04 Q1-Q2 (A2; Prop 2.2(b)), Q3-Q4 (Part B, Part C counts), Q5 (Prop 1.2), Q6 (Part C dispersion), Q7 (Problem E3), Q8 (ln 1.1), Q9 (window start), Q10 (Section 4), Q11 (band bound). Numeric answers within tolerance of exact values ({O}/rederive_r13.out).")
row("lx1b-L03-remark42-solvency", "2.4 mathematics (Assumption 1.2, Remark 4.2)", "L03.html:64-67 (Assumption 1.2); :394 (Remark 4.2)", PASS,
    "V_m < N_0 + D (A2) with Prop 3.2(a) V_t <= V_m gives V_t < N_0 + D and N_t > 0 in every period (checked: V_12 = 1274345 < 5000000; V_4 = 1084166 < 5000000, rederive_r13.out). The inequality chain is correct; the symbol N is the subject of row lx1b-notation-N.")
row("lx1b-L03-ratio-claims", "2.4 / 2.2 ratio and functional-form claims", "L03.html:404 (functional-form bullet); :516 (R1); :523 (R2)", PASS,
    "Squared-premium claim: with psi = phi (L - L0)^2 each depth is beta*phi*(bracket)^2, so the ratio is the square of the Cor 3.4 ratio, which differs from it unless the ratio is 1 (the ratio here is 3.426): algebra checked. 'A change of slope cannot change the ratio' follows from the factor cancelling (Cor 3.4).")
row("lx1b-L03-r1-no-result", "2.6 / 2.4 (R1 claims no result)", "L03.html:516 (R1 solution)", PASS,
    "R1 solution describes what an extension would need and states that Prop 3.2 is not carried over without a new proof; it asserts no result about a facility.")
row("lx1b-L04-bretton-definition", "2.9 DAG / concept definition / architect decision", "L04.html:38, :86 (dfn placeholder), :81; plans/LX1-build-plan.md section 0.3 B3 and section 12 item 9, Architect decisions (2026-11-03, binding); plans/LX1-open-items.md; plans/FINAL-ARCHITECT-RULINGS.md", FAIL,
    "Re-verified on e919577: L04.html:86 still places <dfn id=\"def-bretton-woods-system\" data-concept=\"bretton-woods-system\">Bretton Woods system</dfn> followed by 'definition pending.' The binding architect decision (plan line 633) says the definition and end date wait for a request. plans/FINAL-ARCHITECT-RULINGS.md has no Bretton Woods or LX1 ruling (grep: no hit). plans/LX1-open-items.md still asks the architect to confirm the placeholder reading. check_dag passes only because a dfn exists.",
    "Architect ruling required, one of: (a) admit a primary or survey source for the Bretton Woods system through tools/add_reference.py (allow-listed issuer or publisher URL) and define the concept from it with a locator; or (b) record in plans/LX1-build-plan.md or FINAL-ARCHITECT-RULINGS.md that a pending placeholder <dfn> satisfies check_dag. Until one is recorded, the row stays FAIL. No builder edit is requested beyond the ruling.")
row("lx1b-L04-prediction-tested", "2.5 labs (hypothesis vs what is shown)", "L04.html:114 (hypothesis); twin Parts A and C", PASS,
    "The hypothesis predicts the model's zero dispersion (printed 'all exactly zero: True') and says the recorded column's nonzero dispersion is shown by the printed Part C values, not asserted; the printed values (0.027935, 0.024700) show it. No inference is drawn.")
row("lx1b-L03-lab-checks-overreach", "2.5 labs (interpretation scope)", "L03.html:145, :383; twin Parts B-D", PASS,
    "The interpretation (L03.html:383) says the printed depths show what the assumptions imply, not an output fall; the lab prints booleans for ordering and never-falls, which the text describes accurately.")
row("lx1b-L03-misconception-scope", "2.9 misconceptions (claims checked against proofs)", "L03.html:418 (misconception 2); proof L03.html:130 (Cor 3.3)", PASS,
    "Misconception 2 lists the ingredients of the Cor 3.3 proof (durations, V_m closed form, V_m < N0+D, Lemma 3.1, Prop 3.2(b)); compared with the proof at L03.html:124-130, the list is accurate.")
row("lx1b-L04-A2-before-defined", "2.9 definitions before use", "L04.html:84-92 (Def 2.1, Prop 2.2), :400-405 (P2), :450-457 (R2)", PASS,
    "(A2) is stated in Def 2.1 before Prop 2.2; (A3) is stated in P2 before R2 uses it; (A1) is stated in Prop 1.2 before use. No assumption is used before its statement.")
row("lx1b-L04-keyresults-locator", "2.3 key results locator", "L04.html:470-473 (key results rows 3 and 4)", PASS,
    "Row 3 (dispersion values and ratio) cites Lab 1 Parts C and D; row 4 (three zero months) cites Lab 1 Part B; both values are in the printed expected block (lines 305-321).")
row("lx1b-cards-l03-l04", "2.7 retrieval cards (L03, L04)", "course/modules/LX/LX1/cards.json (29 L03 cards, 21 L04 cards)", PASS,
    f"scans_r13.py section 5 ({O}/scans_r13.out): 80 cards in total; 29 L03 and 21 L04 (round 12 counted 20 L04). No duplicate id, front or back; no card cites a key; every number of the form d.dd in an L03/L04 card back occurs in its lesson. Each card read; definitions, derivations, key results and misconceptions each have a card.")
row("lx1b-cards-c052-c053", "2.7 retrieval cards (L04 Prop 2.2, Definition 2.1)", "cards.json LX1-c052, LX1-c053 vs L04.html:84-92", PASS,
    "LX1-c052 states Prop 2.2 with (A2), x-bar > 0 and at least two changes, and conclusion 0 and 0, matching L04.html:90-92. LX1-c053 describes Def 2.1 with x-bar as anchor units per unit of the foreign currency, matching L04.html:84-86. Both use the same symbol as the lesson; the round-12 kappa conflict is gone.")
row("lx1b-L03-partD-label", "2.5 labs (printed labels)", "tests/labs/LX1/lab-LX1-L03-1.py Part D print; L03.html:383 and expected block", PASS,
    "Part D prints the ratio for phi = 1/2, 1, 3 with beta = 1 and the product in its label; the expected block (last three lines) equals the twin output; interpretation says the ratio is the same for all three (matches output).")
row("lx1b-L03-line121-lab-formula", "2.2 / 2.5 (Prop 3.2 interpretation)", "L03.html:120 and :145; twin depth()", PASS,
    "L03.html:120 says the lab does not evaluate part (b); the twin computes the depth as max over the price path (depth() and depth_path()), so the statement is accurate.")
row("lx1b-L03-why-ordering", "2.9 prose (why it matters)", "L03.html:51 (why-it-matters)", PASS,
    "The why-it-matters paragraph says the ordering follows from Assumptions 1.1-1.3 (Cor 3.3) and is not evidence about any economy; consistent with Cor 3.3 and the lab's SIMULATED label.")
row("lx1b-L04-spot-only", "2.8 data (spot-only note)", "L04.html:332 (canon breaks, exchange rates only); tools/data_sources.yaml fx_monthly note (lines 62-70)", PASS,
    "data_sources.yaml fx_monthly note: 'Spot rates only, as for fx_daily'. L04.html:332 quotes that statement and does not claim a forward or interest series.")
row("lx1b-L03-honest-pending-source", "2.8 data (honest-pending note)", "L03.html:76", PASS,
    "The honest-pending note states that no redistributable historical series for gold adherence or output depth is embedded and that the lab is SIMULATED; matches plans/LX1-build-plan.md section 0.3 B1 and open item D-1.")
row("lx1b-L04-twin-docstring-float", "2.5 labs (docstring vs code)", "tests/labs/LX1/lab-LX1-L04-1.py log_changes, show docstrings; L04.html embedded copy", PASS,
    "log_changes: ratio exact Fraction then one float conversion, then math.log, dated by the later month (matches docstring). show(): Decimal(value).quantize with ROUND_HALF_UP on the exact binary value (matches 'rounded half away from zero'). Page code equals twin (compare_r13.py).")
row("lx1b-plan-coverage", "2.9 plan coverage (plan section 3)", "plans/LX1-build-plan.md section 3 (L03 and L04 content)", PASS,
    "L03 covers the model (3 assumptions), leverage and the premium (Def 2.1), the credit-channel chain (Def 2.2), the closed form and orderings (Lemma 3.1 to Cor 3.4), the lender of last resort (Def 4.1, Remark 4.2), canon breaks and the SIMULATED lab. L04 covers the log-change identity, the fixed-exchange-rate model, the GBP two-window lab on fx_monthly, spot-only limits, and no end date for the system (B3).")
row("lx1b-concept-index-title", "2.9 concept index", "course/concepts.html:631-636", PASS,
    "concepts.html:631 (Bretton Woods system, defined here -> L04#def-bretton-woods-system), :635 (Lender of last resort -> L03), :636 ('Nonmonetary (credit) channel of the Great Depression' -> L03#def-credit-channel-depression). The index title is generated from curriculum.json; see notes (architect question on the title's wording).")
row("lx1b-hours", "2.9 hours arithmetic", "L03.html:2, :34; L04.html:2, :34; hub index.html:160-161", PASS,
    "data-hours=10 and 'LX1 · Lesson n of 4 · 10 study hours' on both pages; hub cards 'L03 · 10 h' and 'L04 · 10 h'. Consistent with the plan (4 lessons x 10 h).")
row("lx1b-delta-hunks", "2.9 delta since previous pin (5db69a9..e919577)", "L03.html (26 lines); L04.html (79 lines); cards.json (27 lines); tests/labs/LX1/lab-LX1-L04-1.py (23 lines)", PASS,
    "git diff 5db69a9..e919577 read hunk by hunk for my slice. L03: lambda renames in Lemma 3.1, Prop 3.2, Cor 3.4, Prob P3/R1, key results row 1 (no claim changed; compare_r13 equal). L04: the x-bar rename and parity distinction, the Part A wording, the 'fixed exchange rate' wording (no number changed; expected output equal). cards.json: c030/c032/c036 lambda, c052/c053 x-bar, c083 added. git diff of course/assets, tools, references between the two pins is empty. Every changed hunk was re-verified (rows above).")
row("lx1b-notation-N", "2.4 notation (plan section 2.3: local symbols never redefined across lessons)",
    "L03.html:65-67 (Assumption 1.2, N_t = N_0 - (V_t - V_0)), :96, :103 (Lemma 3.1, C = N_0 + D); cards LX1-c027, LX1-c030, LX1-c031, LX1-c032, LX1-c071, LX1-c082; L01.html:67, :74, :81 (S_N(t) = sum_{k=1}^{N}, every N >= 1)",
    FAIL,
    "The symbol N is defined in L01 as the number of periods in the partial sums S_N(t) = sum_{k=1}^{N} d_{t+k}/(1+r)^k, 'every N >= 1' (L01.html:67, :74, :81). L03 then defines N_t and N_0 as borrower net worth in cents (L03.html:65-67) and uses N_0 + D (C) in Lemma 3.1 and Prop 3.2 (:96, :103, :110). The same letter carries two meanings across lessons, which plan section 2.3 forbids ('defined on the lesson where it first appears and never redefined'). Net worth is also printed in the lab as 'N_0 = 4000000 cents' (expected block line 329).",
    "Rename borrower net worth in L03 to a symbol not used in L01 to L03 (for example A_t and A_0, with C = A_0 + D). Change every occurrence in L03.html (Assumption 1.2, Lemma 3.1, Prop 3.2, Cor 3.3-3.4, Remark 4.2, misconception 2, Problems M2, M3, P2, R1, key results), the lab's printed Part A label (twin line 'N_0 = ...' and NET_WORTH_CENTS docstring/comments), the cards LX1-c027, c030, c031, c032, c071, c082, and then re-embed with tools/embed_labs.py --refresh lab-LX1-L03-1 and rerun compare. Alternatively, the slice a builder may rename L01's count to a letter not used later. Either way the two lessons must use N with one meaning.")

PLAN_NOTES = []
missing = [i for i in R12_IDS if i not in rows]
extra = [i for i in rows if i not in R12_IDS]
print("round-12 ids missing:", missing)
print("new ids:", extra)
assert not missing, missing
ordered = [rows[i] for i in R12_IDS] + [rows[i] for i in extra]

frag = {
    "unit": "LX1",
    "slice": "LX1-b",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b (L03, L04 and lab twins), round 13; did not build LX1 or LX1-b",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin). Nothing carried: every round-12 row id is kept, and each row was re-verified on e919577 (the delta hunks were read in full).",
    "checkout": ROOT,
    "scratch": "/tmp/lx1b-r13 (twin runs), /tmp/lx1b-r13-scratch-fx (fx_monthly rebuild from git archive e919577), /tmp/lx1b-r13-lic (licence page), /tmp/lx1b-r13-gates.log",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": FAIL,
    "rows": ordered,
    "mutants": [],
    "registry_flags": [
        "friedman1963monetary: registry record lists Friedman only (references/references.json:9400-9412, book, 1963); the curriculum string is 'Friedman & Schwartz (1963)' (curriculum/06-profession-capstone.yaml:37). The pages cite the key and the title only. Architect may correct via tools/add_reference.py (plan N2).",
        "Bernanke (1983), AER 73(3) (curriculum/06-profession-capstone.yaml:38): no registry record (plan B2, REFERENCE_REQUEST 2). L03 makes no empirical attribution to it.",
        "Bretton Woods (plan B3, REFERENCE_REQUEST 3): no registry source. L04 defines nothing historical; the pending placeholder is the open row lx1b-L04-bretton-definition.",
    ],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. LX1 is rubric-only; lab twins are demonstrations, so mutation testing does not apply to L03 or L04 (VERIFIER_RULES 2.5 and the rulings). The mutants list is empty by design.",
        "Gates run this round on e919577 (all exit 0): check_pages, check_dag, check_projects, run_labs (7/7), run_graders (rubric), verify_refs --offline and --unit LX1, fetch_data --check, page_smoke for L03 and L04 alone, ruff check and format, mypy --no-incremental on both twins, pytest -k LX1 and its collect-only, build_site.py --check (exit 0, 'site data current: 6 outputs'). Script: ledgers/LX1/scripts/LX1-b-r13/gates_r13.sh; outputs in ledgers/LX1/scripts/LX1-b-r13/out/.",
        "Scripts backing rows (all under ledgers/LX1/scripts/LX1-b-r13/): gates_r13.sh, rederive_r13.py, compare_r13.py, scans_r13.py, fx_rebuild_and_licence_r13.sh, make_fragment_r13.py. Outputs in out/.",
        "Out of slice, for the slice a verifier and the orchestrator: (1) L01.html:105 uses P_t for an asset price (B_t = P_t - F_t), while L02 and L03 use P for the price level (L02 'P price level'); the symbol has two meanings across L01 and L02/L03. (2) L02.html:57 keeps kappa as gold grams per unit (fine within L02); L04 no longer uses it. (3) L01 N (row lx1b-notation-N) is the other side of the N collision.",
        "Not checked: the hub index.html content beyond the two card titles (slice a); the project and its rubric (slice e); the L01 and L02 lessons and their cards (slices a and c); a Pyodide run of the twins outside page_smoke; the full Crossref re-resolution beyond verify_refs --unit LX1; the content of the Friedman book and any historical source (none read, none claimed); the Bernanke AER article (no record admitted, nothing claimed); the live Federal Reserve H.10 page beyond the rebuild of fx_monthly and the licence page.",
        "Architect questions raised: (1) Bretton Woods placeholder (lx1b-L04-bretton-definition, unchanged since round 12); (2) the concept index title 'Nonmonetary (credit) channel of the Great Depression' (concepts.html:636, from curriculum.json) names an episode while L03 states only a model mechanism; (3) the title 'Bretton Woods and Its End' promises an end that L04 does not state (curriculum title; the page's section 4 says why).",
    ],
    "summary": "",
}
n_fail = sum(1 for r in ordered if r["status"] != PASS)
frag["summary"] = (f"LX1-b round 13 on e919577 (base 5db69a9): verdict FAIL. {len(ordered)} rows: pass={len(ordered)-n_fail} fail={n_fail} "
                   f"unverifiable=0. Non-PASS: lx1b-L04-bretton-definition (architect ruling still unrecorded), lx1b-notation-N (net worth N in L03 "
                   f"collides with the count N of L01; cards c027, c030-c032, c071, c082 carry it).")
problems = ledger.validate(frag, "LX1-b")
print("validation problems:", problems)
out = f"{ROOT}/ledgers/LX1/LX1-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(out, "a", encoding="utf-8").write("\n")
print("wrote", out, "rows", len(ordered), "fail", n_fail)
