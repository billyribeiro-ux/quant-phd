import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/E5/scripts/E5-d-r4"
PIN = "b276325"

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---------- new non-PASS rows (round 4) ----------
row("proj-lab2-gap-survivor", "2.5 labs / 2.6 rubric 3 (student-error survivor)",
    "course/modules/E/E5/project.html Lab 2 (lab-E5-project-2 hypothesis: 'The output-gap line is the log gap of the conventions'; rung 2 ladder: 'It is graded instantly'); tests/labs/E5/lab-E5-project-2.py line 93 (log gap)",
    "FAIL",
    f"Student-error mutant ledgers/E5/mutants/project-2/m02_gap_percent_of_trend.py and new mutant ledgers/E5/mutants/project-2-r4/r4_m05_gap_percent_of_trend.py replace the log gap with the percent-of-trend gap 100(Y-trend)/trend. Both print 'output gap (%): -0.18', identical to the twin output (ledgers/E5/scripts/E5-d-r4/existing_mutants_run.out; diff vs twin run). The page states the output-gap line must be the log gap and says a correct solution prints the expected block, so a wrong gap definition is accepted. The conventions (project.html) say the two gaps differ, and at 2026 Q3 they differ at the fourth decimal (-0.18384 log vs -0.18367 percent; ledgers/E5/scripts/E5-d-r4/recompute.out). Other student errors (spread sign, spread of previous quarter, off-by-one window index, trend at window start) are caught: r4_m01 -0.83, r4_m02 1.01, r4_m03 -0.67, r4_m04 9.10.",
    "Make the printed gap distinguish the two definitions, for example print the gap to four decimals in the completed lab (log -0.1838 vs percent -0.1837) and update the expected block, the hypothesis and the interpretation together; or state on the page that the instant check does not separate the two gap definitions and that the percent-of-trend answer is not accepted by it. Re-run tools/run_labs.py --unit E5.")
row("cards-c050-basis-fact-4-1", "2.7 cards agree with current lesson (rule 10)",
    "course/modules/E/E5/cards.json E5-c050 'basis' field; course/modules/E/E5/L03.html Assumption 4.1 (no 'Fact 4.1' remains)",
    "FAIL",
    "cards.json E5-c050 basis is 'Proposition 4.2 (proof on page, by Fact 4.1)'. The round-4 L03 text renames the implicit-function statement to Assumption 4.1 (L03.html; grep 'Fact 4.1' in L03.html returns 0 matches; 'Assumption 4.1 (implicit-function theorem, used without proof)' present). The card back already says 'Assuming the implicit-function theorem (Assumption 4.1)', so the basis names a result the lesson no longer has. ledgers/E5/scripts/E5-d-r4/card_refs.out lists this as the only cross-reference missing from its own lesson (besides R1, which exists as a problem label).",
    "Change the basis of E5-c050 to 'Proposition 4.2 (proof on page, by Assumption 4.1)'.")
row("cards-c095-holding-condition", "2.7 cards carry a proposition's hypotheses (rule 6/10)",
    "course/modules/E/E5/cards.json E5-c095 back; course/modules/E/E5/L06.html Proposition 2.1 (text: 'Holding P_{t-1} and pi^e_t fixed, the inflation rate falls by beta_t for each rise of one unit in u_t')",
    "FAIL",
    "The card says 'At a fixed P(t-1), inflation falls by beta(t) for each one-unit rise in u(t).' The current L06 Proposition 2.1 states the slope claim under the joint condition 'Holding P_{t-1} and pi^e_t fixed' (checked with snip.py on L06.html, output in ledgers/E5/scripts/E5-d-r4/ card review). The expected-inflation term is omitted from the card, so the slope statement as written is not the lesson's statement. The subject changed in the round-4 L06 edit (the lesson now adds pi^e_t).",
    "Change the back of E5-c095 to: 'Holding P(t-1) and pi^e(t) fixed, inflation falls by beta(t) for each one-unit rise in u(t) (Proposition 2.1).'")

# ---------- rows carried or re-verified from round 3 (re-verified in round 4) ----------
row("proj-exA-c2-annotation", "2.6-rubric-calibration",
    "course/modules/E/E5/project.html #exemplar-a Computation passage and C2 annotation (data-criterion=C2 data-level=4)",
    "PASS",
    "Round-3 FAIL resolved. The Computation passage now names a function or line for every printed number: growth_annualised (0.21), inflation_yoy (1.90), output_gap (-0.18), taylor_value (3.75), the policy-gap line policy[t] - taylor in main (-2.22), read_quarter_spreads (0.96), simulated_path (4.10, 1.53) and states 'Rounding applies only to the printed output'. Blind scoring of exemplar A on C2 gives 4 (ledgers/E5/scripts/E5-d-r4 exemplar review in this fragment's notes).")
row("proj-exA-length", "2.9-structure-prose (brief limits)",
    "course/modules/E/E5/project.html #exemplar-a (Summary and the six passages); Rung 3 Constraints; The brief item 1",
    "PASS",
    "Round-3 FAIL resolved. ledgers/E5/scripts/E5-d-r4/exemplar_words.out: exemplar A Summary = 70 words (limit 80, brief item 1); exemplar A body = 579 words of paragraphs, 586 with headings (limit 600, Constraints). Exemplar B: Summary 16, body 126.")
row("proj-lab2-one-pair", "2.2-lab-prose-vs-code",
    "course/modules/E/E5/project.html Lab 2 hypothesis, twin docstring lines 8-9, Rungs 1-2 paragraph, interpretation",
    "PASS",
    "Round-3 FAIL resolved. The text now says the lab draws 24 quarterly SIMULATED pairs and reads the latest. tests/labs/E5/lab-E5-project-2.py lines 55-56 build tbill and cmt over path['policy'] (24 entries) and the completed line reads yields['cmt_10y'][latest]. Verifier recomputation: 24 pairs, latest spread 0.830281 printed 0.83 (ledgers/E5/scripts/E5-d-r4/recompute.out, 'LAB2 pairs 24').")
row("proj-honest-pending", "2.6-data-honest-pending (plan §6; architect default)",
    "course/modules/E/E5/project.html section#data (p.honest-pending)",
    "PASS",
    "Round-3 FAIL resolved. section#data now carries an honest-pending paragraph with the plan's content: the curriculum names embedded national-accounts data; no redistributable national-accounts source is embedded yet; the lab uses a generated economy labelled SIMULATED; a request is recorded in the DATA_REQUEST entry of plans/E5-open-items.md (the entry exists under '## DATA_REQUESTS', line 6-10). Wording is a close paraphrase of plan §6 (sentence split, '(BUILDER_RULES §1.7)' omitted); substance and pointer match.")
row("cmd-check-projects", "2.6 gate", "tools/check_projects.py --unit E5", "PASS",
    f"Run by verifier on {PIN}: 'check_projects E5: PASS' (ledgers/E5/scripts/E5-d-r4/command_rows.out).")
row("cmd-check-dag", "2.9 gate", "tools/check_dag.py --unit E5", "PASS",
    f"Run by verifier on {PIN}: 'check_dag E5: PASS' (ledgers/E5/scripts/E5-d-r4/command_rows.out).")
row("cmd-check-pages", "2.9 gate", "tools/check_pages.py --unit E5", "PASS",
    f"Run by verifier on {PIN}: 'check_pages E5: PASS' (ledgers/E5/scripts/E5-d-r4/command_rows.out).")
row("cmd-run-labs", "2.5 labs", "tools/run_labs.py --unit E5", "PASS",
    "Run by verifier: 'run_labs E5: PASS (11/11)' (ledgers/E5/scripts/E5-d-r4/run_labs_E5.out). Project twins 1-3: page code equals twin, expected block equals output; twins alone under python -I -W error exit 0 (command_rows.out).")
row("cmd-page-smoke-project", "2.9 gate", "tools/page_smoke.py --unit E5 --pages project", "PASS",
    "Run by verifier: 'page_smoke modules/E/E5/project.html: PASS' with lab-E5-project-1, -2, -3 in Pyodide (ledgers/E5/scripts/E5-d-r4/page_smoke_project.out).")
row("cmd-pytest", "2.5 labs / 2.9 gate", "pytest tests/test_labs.py -k E5; pytest tests/test_page_checks.py", "PASS",
    "Run by verifier: 11 passed (-k E5), all of test_page_checks.py passed; collect-only count 11 (ledgers/E5/scripts/E5-d-r4/tests_ruff_mypy.out).")
row("cmd-verify-refs", "2.1 citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit E5", "PASS",
    "Run by verifier: 'offline integrity: 560 entries, 0 problems'; 'live re-verification of E5: 4 of 560 entries, 0 problems' (command_rows.out).")
row("proj-spec-ladder", "2.6 spec and ladder",
    "course/modules/E/E5/project.html #ladder, #spec, #data, #lab-3-section, #brief, #stretch", "PASS",
    "Ladder order matches check_projects (rung 1 worked example, rung 2 completion with class 'lab completion', rung 3 spec and check, rung 4 stretch). Spec names terms, inputs (five series, term spread from data/ust_daily.csv), required outputs (diagnosis.md, dashboard, self_assessment.md), constraints and grading mode (rubric only). Round-4 text edits (Inputs: 'The project uses no series beyond the five listed in the data section'; Data 'Honest-pending note') read in full and are consistent with the rest of the page.")
row("proj-hours", "2.6 hours", "course/modules/E/E5/project.html #hours-table; data-hours-project=30 (project.html line 33; index.html line 29); curriculum/02-economics-finance-core.yaml line 158", "PASS",
    "Table rows 2+3+6+8+7+4 = 30 h = data-hours-project. index.html data-hours-lessons=80, data-hours-project=30, hub split 72.7%/27.3% = 80/110 (index.html lines 29, 37). Curriculum E5 hours 110 (yaml line 158). Verifier's own estimate ~25 h, within the 30% tolerance (carried reasoning from round 3; the table itself is byte-identical this round).")
row("proj-rubric-observable", "2.6 rubric 1", "course/modules/E/E5/project.html table#rubric (C1-C5, levels 1-4)", "PASS",
    "All 20 level descriptors read in this round. Each names a checkable element (for example 'states the rounding rule', 'names one signal that disagrees with the flag', 'compares the policy rate with the Taylor value at the stated coefficients', 'states that caveats exist with no specific limit named'). Each level contains the one below it per the rubric text.")
row("proj-calib-exB", "2.6 rubric 2", "course/modules/E/E5/project.html #exemplar-b (data-scores 2,2,2,2,1)", "PASS",
    "Blind scoring from the rubric alone: C1 2 (four sources, no date ranges), C2 2 (growth on a non-stated convention 'the change from the previous quarter', rounding unstated), C3 2 (gap rule applied to 2026 Q2 value 0.24, not 2026 Q3), C4 2 (rule 2 + 0.5 gap omits inflation terms), C5 1 (caveats with no specific limit). Official 2,2,2,2,1; annotations agree. Exemplar B numbers re-derived: 2 + 0.5 x (-0.1838) = 1.908, printed 1.91 (recompute.out 'EXEMPLAR B').")
row("proj-calib-exA-blind", "2.6 rubric 2", "course/modules/E/E5/project.html #exemplar-a (data-scores 4,4,4,4,3)", "PASS",
    "Blind scoring of exemplar A from the rubric alone: C1 4, C2 4 (every printed number names its function; rounding stated), C3 4 (growth named as the disagreeing signal), C4 4 (coefficient change with sign, size, basis), C5 3 (the trend end-point is named with no direction; direction given for target and basis). Official 4,4,4,4,3; the blind scores are within one level, and each annotation's claim is now true.")
row("proj-adversarial-and-mutants", "2.6 rubric 3 / grader rules", "course/modules/E/E5/project.html #spec Grading mode; no grader in course/ or tests/", "PASS",
    "Rubric-only project (no autograder). tools/mutate_graders.py --unit E5 ran with no graders and no output (ledgers/E5/scripts/E5-d-r4/mutate_graders_E5.out, rc 0). Mutation testing for the completion lab is reported in proj-lab2-gap-survivor.")
row("proj-conventions-gaps", "2.2 numbers / 2.4 notation", "course/modules/E/E5/project.html #conventions (Output gap; Rounding)", "PASS",
    "recompute.out: log gap 2026 Q3 = -0.183842 (page -0.18384), percent-of-trend gap -0.183673 (page -0.18367). Both print -0.18. Same sign at all 20 window dates (recompute.out 'SIGN MISMATCH dates []'), as ln x and x-1 share a sign for x>0. L07 Section 1 writes the percent-of-trend gap as y(t) (L07.html 'percent of trend output: y_t = 100(Y_t - Y^trend_t)/Y^trend_t'), and L07 Definition 1.4 uses y_t.")
row("proj-lab1-numbers", "2.2 / 2.5", "course/modules/E/E5/project.html Lab 1 hypothesis and interpretation; tests/labs/E5/lab-E5-project-1.py", "PASS",
    "recompute.out 'LAB1': growth 0.209242358, inflation 1.896019507, gap -0.183841618; printed 0.21, 1.90, -0.18; flag mixed (growth > 0, gap < 0). Window 2021 Q4 to 2026 Q3 (label(4), label(23)). run_labs matches the expected block; the interpretation (growth annualised from one quarter, inflation needs four lags) agrees with the code.")
row("proj-lab3-table", "2.2 / 2.5 labs", "course/modules/E/E5/project.html Lab 3 expected block; tests/labs/E5/lab-E5-project-3.py", "PASS",
    "Every row of the expected block re-derived independently (ledgers/E5/scripts/E5-d-r4/recompute.out, printed lines): 2025 Q4 3.15 1.92 0.11 3.91 1.44 3.94 -2.49 0.37; 2026 Q1 2.51 1.98 0.19 4.07 1.65 4.06 -2.40 0.60; 2026 Q2 2.48 1.85 0.24 4.12 1.53 3.90 -2.36 0.80; 2026 Q3 0.21 1.90 -0.18 4.10 1.53 3.75 -2.22 0.96. Matches the page and run_labs output.")
row("proj-lab3-expected-prose", "2.2 prose vs code", "course/modules/E/E5/project.html Lab 3 hypothesis paragraph and interpretation", "PASS",
    "Hypothesis figures (growth 0.21, inflation 1.90, gap -0.18, unemployment 4.10, policy 1.53, Taylor 3.75, policy gap -2.22, spread 0.96), the seven signs and flag 'mixed' match recompute.out and the twin output. Interpretation: day counts 62, 61, 63, 64 match recompute.out 'days=' fields.")
row("proj-lab3-days-and-spread", "2.2 / 2.8 data", "course/modules/E/E5/project.html Lab 3 interpretation and #data-spread; course/assets/data/market/ust_daily.csv", "PASS",
    "recompute.out: 6690 snapshot rows, blank 0, first 2000-01-03, last 2026-09-30. sha256 of ust_daily.csv = dd70e1a21c56e6a32ed056aa8cb99060a6cda516be05a3f4afdee9c1178d50a0, equal to course/assets/data/market/MANIFEST.json sha256 (id ust_daily, rows 6690).")
row("proj-data-licence", "2.8 licence quote", "course/modules/E/E5/project.html #data-spread (licence sentence); https://www.federalreserve.gov/disclaimer.htm", "PASS",
    "Plain curl (this round): 'HTTP 200' for https://www.federalreserve.gov/disclaimer.htm; the page contains verbatim 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' The quoted sentence on project.html matches; tools/data_sources.yaml ust_daily.licence matches.")
row("proj-basis-claims", "2.8 / 2.1 attribution", "course/modules/E/E5/project.html #data-spread (basis paragraph); Exemplar A Limits", "PASS",
    "'tbill_3m is ... on a discount basis' and 'the constant-maturity series names the U.S. Treasury as its source' match tools/data_sources.yaml ust_daily.note. Exemplar A's claim that a yield-based spread would be smaller: with discount d and t days, the investment yield y = d/(1 - dt/360) > d, so cmt - y < cmt - d (algebra, not recall).")
row("proj-taylor-exA", "2.2 numbers (exemplar A)", "course/modules/E/E5/project.html #exemplar-a Policy reading and Limits", "PASS",
    "recompute.out: Taylor 3.752108 unrounded; the rule 1 + 1.5 pi + 0.5 gap on the printed-rounding box gives 3.750000 to 3.770000 (the page's range). Phi_y 0.5 -> 1.0 changes the Taylor value by 0.5 x (-0.183842) = -0.091921, policy gap -2.224971 -> -2.133050 (page -2.13); half-gap -0.091921 lies in [-0.0925, -0.0875]. Higher target lowers the value (sign of -PHI_PI).")
row("proj-exB-numbers", "2.2 numbers (exemplar B)", "course/modules/E/E5/project.html #exemplar-b", "PASS",
    "2026 Q2 gap 0.238060 (table 0.24) correct as the Q2 value; 2 + 0.5 x gap(2026 Q3) = 1.908 printed 1.91 (recompute.out). The exemplar's errors are the ones its annotations name.")
row("proj-notation", "2.9 notation", "notation/notation.json (8 registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q); course/modules/E/E5/project.html", "PASS",
    "No registered symbol is used on the project page (grep for T, Phi, gamma, R^*, R_f, Q in project.html: no notation hits; the page uses g_t, pi^yoy, y^log, Ytilde, i_t, i^*_t, r^n, u^n, phi_pi, phi_y, pi-bar, defined in Conventions). Within-unit note (not a registry violation): i^*_t is the Taylor value here, while L04 uses (Y^*, i^*) for the IS-LM equilibrium; the page defines its use locally. Registry check and BUILDER_RULES 'never give a registered symbol a different meaning' are satisfied.")
row("proj-dag", "2.9 DAG", "course/modules/E/E5/project.html (no data-concept link); tools/check_dag.py --unit E5", "PASS",
    "check_dag E5: PASS (command_rows.out). The project uses only in-unit terms (Taylor rule, output gap, natural rate of unemployment, policy rate, term spread) defined in L04, L06, L07 or its own Conventions; no concept link is made.")
row("proj-reading-list", "2.1 citations", "course/modules/E/E5/project.html #reading (data-cite solow1956contribution, hicks1937mr, phelps1968money, blanchard2020macroeconomics); references/references.json", "PASS",
    "All four keys exist with status verified (references.json records read this round: solow1956contribution DOI 10.2307/1884513, hicks1937mr DOI 10.2307/1907242, phelps1968money DOI 10.1086/259438, blanchard2020macroeconomics OpenLibrary, year 2020; registry flag below). The page attributes no passage to any reading (page text, #reading paragraph). Friedman (1968) not cited.")
row("proj-atlas-disclosure", "2.6 spec", "course/modules/E/E5/project.html #spec Inputs ('The project uses no series beyond the five listed in the data section'); curriculum/02-economics-finance-core.yaml lines 184-190", "PASS",
    "The page no longer names Atlas (round-4 wording). The curriculum brief still says 'from Atlas' (yaml 186-188); this is architect decision B2 and is recorded in registry_flags, not as a page defect.")
row("proj-process-words", "2.9 prose (no process words in learner text)", "course/modules/E/E5/project.html (whole page)", "PASS",
    "Scan for builder, verifier, planner, architect, round, draft, TODO, placeholder, B1, B2: 0 matches. The page now contains the plan-mandated honest-pending note, which names 'DATA_REQUEST' and 'plans/E5-open-items.md' (project.html line 343). The same pattern appears on other units' pages (AC2 L04, L05, project pages), so it is recorded in registry_flags, not failed.")
row("proj-page-length-and-voice", "2.9 structure", "course/modules/E/E5/project.html section ids; six brief headings in exemplars", "PASS",
    "Required sections present in order: ladder, conventions, rungs, lab-3-section, spec, data, brief, hours, rubric (with exemplars and self-assessment form), stretch, reading, references. Exemplars use the six brief headings in order (Summary, Data, Computation, Diagnosis, Policy reading, Limits). page_smoke renders the self-assessment form.")
row("cards-scope-and-duplicates", "2.7 full scan", "course/modules/E/E5/cards.json (130 cards)", "PASS",
    "All 130 cards read this round. ids E5-c001..E5-c130 contiguous (checked), no duplicate normalised fronts or backs (checked), grades T 69 / C 8 / no grade 53 (cards without a grade carry no basis; graded cards all have a basis). Lesson counts L01 23, L02 13, L03 16, L04 18, L05 17, L06 17, L07 14, L08 12 = 130. The 7 cards changed since the previous pin (c043, c046, c049, c050, c065, c071, c128) were re-read against the current lesson text: c043, c046, c049, c065, c071 and c128 agree; c050 has the stale basis row above.")
row("cards-numbers-in-lesson", "2.7 numbers (rule 10)", "course/modules/E/E5/cards.json; L01-L08.html", "PASS",
    "ledgers/E5/scripts/E5-d-r4/card_numbers.out: every number on every card appears as a standalone token in its lesson page except E5-c102 (1.236, 1.226). Those appear as 1.236000 and 1.226000 in the Lab 1 Part A expected block of L06.html line 231 (same numbers, printed to six places; c102 cites Lab 1, Part A).")
samples = [
 ("cards-sample-1", "E5-c010 (Laspeyres, L01)", "L01.html Definition 2.1: P^L = sum p1 q0 / sum p0 q0. Card matches."),
 ("cards-sample-2", "E5-c020 (nominal vs real growth, L01)", "Arithmetic: 105/995 = 0.105528, 4/23 = 0.173913, real = 1.105528/1.173913 - 1 = -0.058254 (python check). Card matches lab output in L01 page."),
 ("cards-sample-3", "E5-c030 (TFP, L02)", "L02.html Definition 2.2: TFP is the level A of Definition 1.1; its log growth is what the residual is meant to measure. Card matches."),
 ("cards-sample-4", "E5-c040 (zero is a fixed point, L03)", "L03.html Remark 2.3: g(0)=0, zero is a fixed point; Proposition 2.2 concerns positive fixed points; A4 excludes zero. Card matches."),
 ("cards-sample-5", "E5-c050 (derivatives of k*, L03)", "Re-derived from k* = (s/(n+delta))^(1/(1-alpha)): dk*/ds = k*/((1-alpha)s), dk*/ddelta = dk*/dn = -k*/((1-alpha)(n+delta)). Card back matches L03 Proposition 4.2; basis row stale (see cards-c050-basis-fact-4-1)."),
 ("cards-sample-6", "E5-c060 (equilibrium definition, L04)", "L04.html Definition 3.1: an equilibrium is a pair (Y*, i*) satisfying both relations. Card matches."),
 ("cards-sample-7", "E5-c070 (no dynamics, L04)", "L04.html section 5: 'dynamics (§5). A single equilibrium does not recur, and a static model cannot generate a path.' Card matches."),
 ("cards-sample-8", "E5-c080 (demand shock, L05)", "dP = da/(eta+nu), dY = nu da/(eta+nu) re-derived; L05 Lab output delta_price 0.1, delta_output 20 for da=30, nu=200, eta=100 (cards c083, c086 agree). Card matches."),
 ("cards-sample-9", "E5-c090 (inflation definition, L06)", "L06.html section 1: pi(t) = (P(t) - P(t-1))/P(t-1); annual periods give an annual rate. Card matches the lesson's section-1 definition."),
 ("cards-sample-10", "E5-c100 (natural rate and inflation, L06)", "Lab 1 Part C 0.016667 at 3 percent with natural rate 5 percent and slope 5/6 (0.02 x 0.833333). Definition 1.2 (L06) defines u^n as the rate at which output is potential. Card matches."),
 ("cards-sample-11", "E5-c110 (Taylor rule, L07)", "L07.html Definition 1.4: i_t = r^n + pi_t + phi_pi(pi_t - pibar) + phi_y y_t. Card matches."),
 ("cards-sample-12", "E5-c120 (multiplier units, L08)", "L08.html Definition 1.2: 'in cents per cent, so it is a number with no unit'. Card matches."),
 ("cards-sample-13", "E5-c130 (no estimate, L08)", "L08.html: 'This page gives no estimate of any multiplier in any economy ... cites no source on it and states no empirical claim about it.' Card matches."),
]
for rid, what, ev in samples:
    row(rid, "2.7 sample", f"course/modules/E/E5/cards.json {what}", "PASS", ev)
row("cards-derivations", "2.7 math", "cards.json E5-c014, c022, c035, c052, c051, c062, c064, c065, c079, c080, c099, c102, c122-c125, c128, c129",
    "PASS",
    "Re-derived this round by python: 5/4 - 27/23 = 7/92; basket B 11/10 and 19/10 (L01 Proposition 2.4 text); ln 1.25 = 0.223144 and 0.25 - that = 0.026856; 1.1^0.3 = 1.029006 and 0.3 ln 1.1 = 0.028593; k* = 5.5843115042, (k*)^0.3 = 1.6752934513; 10/7 = 1.4285714286; shares 0.333333..0.888889 and changes 0.2..0.033333 for nu 50..800; 13/600 = 0.021667; 5/6 x 0.01 = 0.008333; S(N) with c = 0.6, dG = 10000 gives 10000, 16000, 19600; Bernoulli bound c^N <= 1/(1+N(1/c-1)) holds for N = 1..30; tax multiplier -c/(1-c) x 10000 = -15000. Closed forms from L04 Propositions 3.2, 4.2, 4.3 agree with the card text.")
row("cards-lab-numbers", "2.7 numbers vs lab", "cards.json c019-c021, c033-c034, c036, c048, c051-c052, c067-c069, c082-c087, c100-c104, c113-c117, c127-c129",
    "PASS",
    "Each card number that is a lab output appears in its lesson's expected block (card_numbers.out shows presence of every number token except c102, handled above). c048 period 692 and the 1e-12 tolerance match L03 twin lines (round-3 record, L03 not changed in those lines). c127 162500/187500/25000 and c128 10000/16000/25000 match L08 expected block (L08.html lines 191-207).")
row("cmd-ruff-mypy", "gate (labs)", "tests/labs/E5/*.py (ruff); tests/labs/E5/lab-E5-project-1..3.py (mypy)", "PASS",
    "ruff check tests/labs/E5: 'All checks passed!'; ruff format --check: '11 files already formatted'; mypy --no-incremental on the three project twins: 'Success: no issues found in 3 source files' (tests_ruff_mypy.out). Whole-repo ruff and mypy not run: no .py outside tests/labs/E5 changed in slice d.")

fragment = {
    "unit": "E5",
    "slice": "E5-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E5-d, round 4 (did not build E5; no shared context with the builders)",
    "pin": PIN,
    "base": "ccfdf4c (round-3 pin); delta slice d: course/modules/E/E5/project.html, course/modules/E/E5/cards.json, tests/labs/E5/lab-E5-project-2.py (plus lesson edits L03-L08 read for card agreement)",
    "checkout": str(ROOT),
    "scratch": "/tmp/e5d-r4-run (lab-E5-project-3 twin run dir with data/ust_daily.csv)",
    "verified_at": "2026-10-29T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "m01_gap_intercept_only", "description": "project-2 existing: output gap uses the intercept only (no slope term)", "killed_by": "run output differs from twin (ledgers/E5/scripts/E5-d-r4/existing_mutants_run.out)"},
        {"id": "m02_gap_percent_of_trend", "description": "project-2 existing: output gap is the percent-of-trend gap, which prints -0.18 like the log gap at 2026 Q3", "killed_by": ""},
        {"id": "m03_gap_lagged_output", "description": "project-2 existing: gap uses lagged output", "killed_by": "run output differs from twin"},
        {"id": "m04_gap_window_24", "description": "project-2 existing: trend window of 24 quarters", "killed_by": "run output differs from twin"},
        {"id": "m05_spread_reversed", "description": "project-2 existing: spread is bill minus 10-year", "killed_by": "run output differs from twin"},
        {"id": "m06_spread_fixed_offset", "description": "project-2 existing: spread is a fixed offset", "killed_by": "run output differs from twin"},
        {"id": "m07_gap_sign_flipped", "description": "project-2 existing: gap sign flipped", "killed_by": "run output differs from twin"},
        {"id": "m08_gap_log10", "description": "project-2 existing: gap uses log10 instead of ln", "killed_by": "run output differs from twin"},
        {"id": "r4_m01_spread_sign_reversed", "description": "student error: spread = tbill - cmt for the latest quarter", "killed_by": "printed term spread -0.83 vs 0.83"},
        {"id": "r4_m02_spread_previous_quarter", "description": "student error: spread taken from the previous quarter's pair", "killed_by": "printed term spread 1.01 vs 0.83"},
        {"id": "r4_m03_gap_time_index_off_by_one", "description": "student error: trend evaluated at index WINDOW instead of WINDOW-1", "killed_by": "printed output gap -0.67 vs -0.18"},
        {"id": "r4_m04_gap_trend_at_window_start", "description": "student error: trend read at the window's first quarter (intercept only)", "killed_by": "printed output gap 9.10 vs -0.18"},
        {"id": "r4_m05_gap_percent_of_trend", "description": "student error: percent-of-trend gap 100(Y-trend)/trend, which the page's conventions say is not the output-gap line", "killed_by": ""},
    ],
    "registry_flags": [
        "references/references.json blanchard2020macroeconomics: record year 2020 while curriculum yaml says '8th ed. (2021)' (notes.year). The page prints no year in prose. Architect to decide.",
        "curriculum/02-economics-finance-core.yaml lines 184-190 still say the brief uses series 'from Atlas'; the page uses no Atlas series (architect decision B2). Edit the yaml or accept the discrepancy.",
        "plans/E5-open-items.md NOTATION_REQUESTS names u^{\\ast} for the natural rate of unemployment; the page uses u^n. Stale planning note.",
        "project.html honest-pending note cites plans/E5-open-items.md and the DATA_REQUEST entry (learner-visible planning path). Same pattern on other units' pages; architect to decide whether learner text should cite it.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 4, slice d (project.html rubric, rung labs, cards.json), pin b276325. Previous fragment /Users/billyribeiro/.fanout/frags/C-E5-d.round3.json (pin ccfdf4c) had 4 FAIL rows; all 4 are resolved in this pin and re-verified from scratch (proj-exA-c2-annotation, proj-exA-length, proj-lab2-one-pair, proj-honest-pending). "
        "Every row was re-verified from scratch on b276325 because the subjects (project.html, cards.json, lab-E5-project-2.py) changed; no PASS row is carried by byte identity. "
        "Read in full: project.html (780 lines); all 130 cards in cards.json; the delta in L03-L08 used to check card agreement; the three project twins and run_labs output. "
        "Exemplar calibration: blind scoring of exemplar A gives 4,4,4,4,3 and exemplar B 2,2,2,2,1, equal to the official scores. "
        "Lab 2 survivor: the percent-of-trend gap passes the instant check (m02 and r4_m05), which the page's 'graded instantly' and 'the output-gap line is the log gap' sentences do not allow. "
        "Scripts: ledgers/E5/scripts/E5-d-r4/ (recompute.py, card_numbers.py, card_refs.py, exemplar_words.py, snip.py, build_fragment.py and outputs). New mutants: ledgers/E5/mutants/project-2-r4/ (r4_m01..r4_m05 wrong solutions; alt01 and alt02 correct alternatives, both identical to the twin output). "
        "Not run: render_curriculum.py, build_site.py --check, fetch_data.py --check, check of full repo pytest/ruff/mypy (no curriculum, site data, market input or repo .py outside tests/labs/E5 changed in slice d); page_smoke run for the project page only, as the rules require."
    ),
    "summary": (
        "E5-d round 4: verdict FAIL. 3 non-PASS rows: proj-lab2-gap-survivor (the percent-of-trend output gap passes the completion check, FAIL), cards-c050-basis-fact-4-1 (basis cites a removed 'Fact 4.1', FAIL), cards-c095-holding-condition (slope card omits the pi^e-fixed condition of current Proposition 2.1, FAIL). "
        "All round-3 FAIL rows are resolved and re-verified PASS. Gates PASS: check_pages, check_dag, check_projects, run_labs (11/11), page_smoke (project), pytest (11 E5 labs, page checks), ruff, mypy, verify_refs."
    ),
}

out = ROOT / "ledgers/E5/E5-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", sum(1 for r in rows if r["status"] != "PASS"))
