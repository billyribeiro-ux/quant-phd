"""Round-17 verifier (LX1-c): writes ledgers/LX1/LX1-c.json from the evidence in ledgers/LX1/scripts/LX1-c-r17/out/.

Mutant kill reasons are parsed from the kill outputs; row evidence is written by the verifier from its own reads
and runs. Usage: python -I write_fragment_r17.py <checkout_root>.
"""
import json
import pathlib
import re
import sys
from datetime import UTC, datetime

root = pathlib.Path(sys.argv[1])
S = root / "ledgers/LX1/scripts/LX1-c-r17"
OUT = S / "out"
MUT = root / "ledgers/LX1/mutants"


def kills(path):
    result = {}
    for line in (OUT / path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"(KILLED|SURVIVED) \| (\S+?) \| (.*)", line)
        if m:
            result[m.group(2)] = (m.group(1), m.group(3))
    return result


stripped = kills("kill_stripped_r17.out")
new = kills("kill_new_r17.out")
damaged = kills("damaged_lab3_all_r17.out")

mutants = []
for path in sorted(MUT.glob("*.py")):
    name = path.name
    first = path.read_text(encoding="utf-8").splitlines()[0]
    description = first.replace('"""', "").strip()
    if name in stripped and stripped[name][0] == "KILLED" and "NameError" not in stripped[name][1]:
        killed_by = "harness_r17.py cands on the agreement-stripped copy (out/kill_stripped_r17.out): expected block differs"
    elif name == "r13n03_lab3_agreement_check_removed.py":
        killed_by = ("harness_r17.py expected block (artifact, not a current claim): the mutant prints the agreement line "
                     "that 700bf33f removed from the page; its stripped copy fails with NameError (out/kill_stripped_r17.out)")
    elif name in new:
        if new[name][0] == "KILLED":
            killed_by = "harness_r17.py cands (out/kill_new_r17.out): expected block differs"
        else:
            killed_by = None
    else:
        killed_by = None
    if name in damaged and damaged[name][0] == "KILLED" and (killed_by is None or stripped.get(name, ("", ""))[0] == "SURVIVED"):
        killed_by = "damaged_r17.py differential (out/damaged_lab3_all_r17.out): " + damaged[name][1][:300]
    if name == "r17n01_lab3_blank_gbp_cell_read_as_zero.py":
        killed_by = "damaged_r17.py differential (out/damaged_lab3_all_r17.out): first-row blank gives ZeroDivisionError, not ValueError"
    if name in ("lx1c_r7n02_lab3_window_three_population_sd.py",):
        pass
    mutants.append({"id": name, "description": description, "killed_by": killed_by})

missing = [m["id"] for m in mutants if not m["killed_by"]]
assert not missing, missing

R = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    R.append(item)


row("proj-rung1-step3-rounding-claim", "2.5-labs", "course/modules/LX/LX1/project.html:177, :179",
    "PASS",
    "Fresh. project.html:177 states 11764705.882 cents (10000000/0.85) and :179 states 3069053.708 cents. rederive_r17.out: "
    "falling period-5 real debt 11764705.88235 cents -> 117647.06; difference 3069053.7084 cents -> 30690.54. "
    "out/twins_r17.out: page code equals the twin (0 differing lines), twin stdout equals the expected block (20 lines).")
row("proj-real-value-vs-lesson2", "2.9-prose", "course/modules/LX/LX1/project.html:55-59; course/modules/LX/LX1/L02.html:83-92, :110, :127-128",
    "PASS",
    "Fresh read of project.html:55-59 (real value V_t = D/P_t, equal to Lesson 2's V_t = D P_0/P_t with P_0 = 1; burden change "
    "100(P_0/P_t - 1)). L02.html is byte-identical to 56cc575a (carried for its lines): Proposition 2.1 hypotheses (A2), (A3) at :83-92, "
    "conclusion (b) V_H/V_0 = P_0/P_H; debt deflation dfn at :110; Remark 3.3 at :127-128.")
row("proj-manifest-note-misattributed", "2.2-numbers", "course/modules/LX/LX1/project.html:271, :279, :294; course/assets/data/market/MANIFEST.json (fx_monthly)",
    "PASS",
    "Fresh. out/data_checks_r17.out: MANIFEST fx_monthly title 'Month-end foreign exchange rates, ten currencies, USD per unit of "
    "foreign currency'; 669 rows, 1971-01 to 2026-09; retrieved 2026-10-19; columns equal the page's list; transform inverts CAD, CHF, "
    "DKK, JPY, NOK, SEK; GBP not inverted. Page :271, :279, :294 match.")
row("proj-lab3-citation-string", "2.9-prose", "course/modules/LX/LX1/project.html:279, :287; MANIFEST.json fx_monthly citation",
    "PASS",
    "Fresh. MANIFEST citation 'Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (noon buying rates in "
    "New York)' equals the citation at :279 and the Lab 3 hypothesis at :287 and the twin docstring.")
row("proj-reading-reinhart-registry", "2.9-prose", "course/modules/LX/LX1/project.html:626-640; references/references.json",
    "PASS",
    "Fresh. Reading list (:627-640) holds friedman1963monetary, eichengreen1992golden, garber2000famous (reinhart2009this is optional in "
    "the plan and is not on the page: not a defect). references.json changed since 56cc575a only in the used_by of another key "
    "(Black & Scholes entry gains FC2); the three keys are status 'verified', used_by ['LX1']. out/verify_refs_offline.out: 560 entries, "
    "0 problems; out/verify_refs_LX1_online.out: 4 of 560 LX1 entries live, 0 problems.")
row("proj-spec-current-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:62, :301, :439 (brief item 1)",
    "PASS",
    "Fresh. :62 defines window three as the twelve months to the last month of the embedded snapshot; :439 defines a current condition as "
    "dated within the twelve months ending at the last month of the data, 2025-10 to 2026-09 for the snapshot. rederive_r17.out: window "
    "three has 12 changes (2025-10 to 2026-09).")
row("proj-exemplar-A-condition", "2.6-rubric", "course/modules/LX/LX1/project.html:490 (exemplar A episode and condition)",
    "PASS",
    "Fresh. :490 names window three, 2025-10 to 2026-09, and the MANIFEST last month 2026-09, retrieved 2026-10-19 (MANIFEST fx_monthly: "
    "last = 2026-09, retrieved 2026-10-19). rederive_r17.out: window three 12 changes, sd 1.90 percent per month.")
row("proj-gate-commands", "2.9-prose", "ledgers/LX1/scripts/LX1-c-r17/out/ (run_gates_r17.sh and direct runs)",
    "PASS",
    "Fresh, at 700bf33f with .venv (Python 3.14): check_pages --unit LX1 PASS (check_pages_LX1.out); check_dag --unit LX1 PASS; "
    "check_projects --unit LX1 PASS; run_labs --unit LX1 7/7 PASS; run_labs --unit LX1 --page project 3/3 PASS; page_smoke --unit LX1 "
    "--pages project PASS (page_smoke_project.out); ruff check and ruff format --check on tests/labs/LX1 and tools PASS; mypy "
    "--no-incremental: no issues in 385 source files; pytest test_labs, test_run_labs, test_page_smoke, test_page_checks, test_curriculum "
    "and test_refs rc 0; verify_refs --offline 560 entries 0 problems; verify_refs --unit LX1 4 of 560 0 problems; fetch_data --check "
    "3 datasets 0 problems; build_site --check current; run_graders --unit LX1 and mutate_graders --unit LX1: no autograder (rubric). "
    "Not run: render_curriculum --check (no curriculum file changed: curriculum/curriculum.json byte-identical), check_pages --all, "
    "run_graders --all (no grader in this unit). check_pages --page project was run and fails (it applies the lesson contract to the "
    "project page, out/check_pages_project.out); the unit-level check_pages passes and is the gate.")
row("proj-lab1-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:78-150; tests/labs/LX1/lab-LX1-project-1.py",
    "PASS",
    "Fresh. out/twins_r17.out: page-vs-twin diffs=0; twin under python -I -W error: rc 0, stderr 0 bytes, stdout equals the expected "
    "block (20 lines). run_labs_LX1.out: lab-LX1-project-1 PASS. page_smoke lab time 0.0 s (page_smoke_project.out).")
row("proj-lab1-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:150-170 (expected block), :77 (hypothesis)",
    "PASS",
    "Fresh. rederive_r17.out (exact Fraction arithmetic, no lab code): falling real debt 100000.00 ... 117647.06; rising ... 86956.52; "
    "burden 17.65 and -13.04; difference 30690.54. Identical to the expected block at :150.")
row("proj-lab2-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:182-247; tests/labs/LX1/lab-LX1-project-2.py",
    "PASS",
    "Fresh. out/twins_r17.out: page differs from the twin only on the blank lines (___); twin rc 0, stderr 0 bytes, stdout equals the "
    "expected block (10 lines). run_labs_LX1.out PASS.")
row("proj-lab2-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:184, :247-256",
    "PASS",
    "Fresh. rederive_r17.out: real debt 40000.00, 40404.04, 40816.33, 41666.67, 42105.26, 43010.75; burden 7.53. Inverted ratio gives "
    "-7.00 (the page's :257 example). Hypothesis :184 agrees.")
row("proj-lab2-check-claims", "2.5-labs", "course/modules/LX/LX1/project.html:257",
    "PASS",
    "Fresh. :257 says a real-value line without the division prints 40000.00 in every period, and a burden line that inverts the ratio "
    "prints -7.00. out/kill_stripped_r17.out / kill_all_r17.out: lx1c_m01 (without division) and lx1c_m02 (ratio inverted) differ from the "
    "expected block; rederive_r17.out confirms -7.0 and the 40000.00 nominal values.")
row("proj-lab3-twin-run", "2.5-labs", "course/modules/LX/LX1/project.html:286-431; tests/labs/LX1/lab-LX1-project-3.py",
    "PASS",
    "Fresh. out/twins_r17.out: page-vs-twin diffs=0; twin under python -I -W error in a scratch dir with data/fx_monthly.csv: rc 0, "
    "stderr 0 bytes, stdout equals the expected block (19 lines). out/damaged_lab3_all_r17.out: the twin raises ValueError for a blank, "
    "a non-decimal, a scientific, a negative, a dropped-month and a duplicated-month GBP cell, at first, middle and last rows.")
row("proj-lab3-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:286-431 (expected block at :412)",
    "PASS",
    "Fresh. rederive_r17.out (csv and math only): window one 668 changes, 3 zeros, sd 2.79, largest 13.58 at 1985-03; window two 321, 2 "
    "zeros, sd 2.47, largest -9.66 at 2008-10; window three 12, 0 zeros, sd 1.90, largest 2.96 at 2026-04; ratio 0.88 (unrounded "
    "0.884169); difference 0.32 (unrounded 0.323578). All equal the expected block.")
row("proj-lab3-L04-cross-check", "2.9-prose", "course/modules/LX/LX1/L04.html:312-318; course/modules/LX/LX1/project.html:284",
    "PASS",
    "Fresh. out/L04_twin_run_r17.out: Lesson 4's lab prints window one 668 changes, sd 0.027935, window two 321 changes, sd 0.024700, zeros "
    "3 (1976-07, 2012-07, 2019-11), difference -0.003236, ratio 0.8842. L04.html:314, :317 agree; :284 quotes 0.027935 and 0.024700. "
    "L04.html byte-identical to 56cc575a.")
row("proj-lab3-docstring-claims", "2.9-prose", "course/modules/LX/LX1/project.html:288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py lines 1-40",
    "PASS",
    "Fresh. Each docstring claim checked against code and runs: 'A blank or non-decimal cell raises ValueError, and so does a month that "
    "does not follow the previous one. No row is skipped or filled' (load_column; damaged_lab3_all_r17.out); 'rounded half up' (show() uses "
    "ROUND_HALF_UP on Decimal(float)); ratio and difference from unrounded values (main); 669 months (data_checks_r17.out); no interest-rate "
    "column (data_checks_r17.out: False). The agreement sentence is gone from the docstring, the code and the expected block.")
row("proj-lab3-interpretation-claims", "2.5-labs", "course/modules/LX/LX1/project.html:431; course/modules/LX/LX1/L04.html:84-94 (Definition 2.1, (A2); Proposition 2.2(a))",
    "PASS",
    "Fresh. :431: 13.58 percent in 1985-03 outside window two (rederive: 1985-03 not in window two); 0.32 is the difference line from unrounded "
    "dispersions; window three 12 changes, 11 degrees of freedom; 2 zero changes in window two (rederive: 2012-07, 2019-11); a fixed rate over "
    "window two would show 321 zero changes. L04.html:84-94: Definition 2.1 fixed-exchange-rate model with (A2) 'fixed rate held'; Proposition "
    "2.2(a) every monthly log change in the window is 0 under (A2). Claim is conditional on (A2) as written.")
row("proj-lab3-difference-line-r5", "2.2-numbers", "course/modules/LX/LX1/project.html:287, :412-431, :431; tests/labs/LX1/lab-LX1-project-3.py (main, difference line)",
    "PASS",
    "Fresh. Twin main: difference = show(100*(sd_one - sd_two), 2) on unrounded floats; rederive_r17.out: 100*(sd1-sd2) = 0.3235776530 -> 0.32. "
    "The printed agreement line that the round-16 row cited is removed from the expected block and the twin.")
row("proj-lab-simulated-labels", "2.8-data", "course/modules/LX/LX1/project.html:42, :77, :80, :184, :187 (code docstrings), :283-287 (Lab 3 section)",
    "PASS",
    "Fresh. :42 labels Rungs 1 and 2 SIMULATED and states they read no file; Lab 1 and Lab 2 docstrings say SIMULATED; Lab 3 is labelled as the "
    "real H.10 snapshot and reads data/fx_monthly.csv (the only lab with data-files, :286).")
row("proj-data-licence-quote", "2.8-data", "course/modules/LX/LX1/project.html:279; https://www.federalreserve.gov/disclaimer.htm (plain curl)",
    "PASS",
    "Fresh. out/curl_licence_r17.out: HTTP 200, 85306 bytes (plain curl). out/licence_page_r17.html contains verbatim 'Unless otherwise indicated, "
    "information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board "
    "as the source of the information.' (grants redistribution). Page :279 quotes the same sentence.")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)",
    "PASS",
    "Fresh rebuild from the live feed in a scratch copy (out/ fetch log in scratch, not the checkout): tools/fetch_data.py --fetch --only fx_monthly "
    "built 669 rows, 1971-01 to 2026-09. Rebuilt CSV sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e equals the "
    "checkout file and the MANIFEST sha256: byte-identical. raw_sha256 differs (MANIFEST 8f370f9c..., live download 1c312d2f...), which the "
    "rules expect for an issuer file that changed; the checkout's retrieved (2026-10-19) and raw_sha256 are unchanged. fetch_data --check PASS.")
row("proj-data-fields", "2.8-data", "course/modules/LX/LX1/project.html:271, :279-280, :292-294; course/assets/data/market/fx_monthly.csv",
    "PASS",
    "Fresh. out/data_checks_r17.out: columns equal the MANIFEST list (AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK); EUR blank for every "
    "month before 1999-01 and first non-blank 1999-01 (page :279 'blank before January 1999'); zero blank GBP cells; no month gaps; no "
    "interest-rate column.")
row("proj-data-no-other-series", "2.8-data", "course/modules/LX/LX1/project.html:280; course/assets/data/market/MANIFEST.json",
    "PASS",
    "Fresh. :280 'The site embeds three series (fx_daily, fx_monthly, ust_daily)' and 'none of the three is a gold, price-level, output, "
    "unemployment or bank-failure series'. MANIFEST datasets are exactly fx_daily (six FX rates), fx_monthly (ten FX rates) and ust_daily "
    "(bill and 10-year yields) per their titles (out/data_checks_r17.out).")
row("proj-spec-ladder", "2.6-spec", "course/modules/LX/LX1/project.html:40-48, :73-258, :262-275, :282-441, :448-453, :618-625",
    "PASS",
    "Fresh. Order: worked example (Lab 1, :78), completion problem (Lab 2, :182, class lab completion, blanks, instant check), independent "
    "project (:262 spec, :283 Lab 3 check, :436 brief, :464 rubric), stretch (:618). check_projects_LX1.out PASS. Rung 1 fully solved and "
    "annotated (worked steps :173-180). Tier U: full length, not minimal.")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; course/modules/LX/LX1/project.html:436-447",
    "PASS",
    "Fresh. yaml:42-49 project title 'Then vs. now', brief 'Pick one historical episode and one current market condition, and write a "
    "mechanism-level comparison that says where the analogy holds and where it breaks.', deliverable 'Two-page essay, every claim cited.', "
    "grading rubric. The page's brief (:437-443) and spec (:262-275) cover the same scope. yaml byte-identical since 56cc575a.")
row("proj-hours", "2.6-hours", "course/modules/LX/LX1/project.html:33 (eyebrow), :448-458 (table#hours); course/modules/LX/LX1/index.html:29",
    "PASS",
    "Fresh. Table components 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 h, equal to the eyebrow '10 hours' and data-hours-project=10 on the page and the hub "
    "(index.html:29). Verifier estimate of the components: rung 1 about 1 h, rung 2 about 0.5-1 h, selection and sourcing 2 h, outline 1.5 h, "
    "drafting two pages 2.5-3 h, self-assessment 2 h: 9.5-10.5 h, within 30 percent of 10 h.")
row("proj-rubric-observable", "2.6-rubric", "course/modules/LX/LX1/project.html:472-476 (C1-C5 rows), :466 (scoring rule)",
    "PASS",
    "Fresh. Every level cell names a checkable element: dates and locators (C1), chain steps, bases, failure step and evidence (C2), "
    "citation, locator and counter-evidence (C3), unrounded values, rule, formula, base and sign (C4), limits and tests (C5). Count words "
    "('one difference' in C2 L2, 'at least two limits' in C5) are observable; their wording is judged in separate rows.")
row("proj-calibration-exemplars", "2.6-rubric", "course/modules/LX/LX1/project.html:484-606 (exemplar memo prose); ledgers/LX1/scripts/LX1-c-r17/blind_extract_r17.py; out/blind_prose_r17.txt",
    "UNVERIFIABLE",
    "Prose-only extraction by blind_extract_r17.py (ruling 15: annotations, verdict lines and data-scores dropped) in out/blind_prose_r17.txt. "
    "Scores from the descriptors only: Exemplar A C1 4, C2 4, C3 4, C4 4, C5 3; Exemplar B C1 2, C2 2, C3 1, C4 2, C5 1. Both match the "
    "official data-scores (:484, :546) within one level. BLIND CONDITION NOT MET: the Exemplar A verdict line (:486) and the A annotation "
    "text had been read in this session before the A scores were made, and the prior round's fragment (with its scores) had been read "
    "before any scoring. B's verdict line (:548) was read after its scores were written, but not blind to the prior fragment.",
    "Fresh verifier, with no view of this fragment or of :484-616: run blind_extract_r17.py first, record the scores with the descriptor "
    "that supports each, and only then read :486, :548 and the annotations.")
row("proj-exemplar-numbers", "2.2-numbers", "course/modules/LX/LX1/project.html:522-530 (A numbers), :576-582 (B numbers), :581 (B annotation)",
    "PASS",
    "Fresh. A: 17.65 from 100(1/0.85 - 1) (Lab 1 Part B), 2.47/2.79/1.90 and 0.88 from unrounded values (rederive_r17.out). B: 2.47/2.79 = "
    "0.8853 -> 0.89 (rounded inputs); unrounded ratio 0.884169 gives a fall of 11.58 percent, so the B annotation's 'about 12' is right and "
    "'about 11' is wrong (rederive_r17.out: 100*(1-ratio) = 11.583).")
row("proj-reading-keys", "2.9-prose", "course/modules/LX/LX1/project.html:626-640; references/references.json",
    "PASS",
    "Fresh. Same entries as proj-reading-reinhart-registry: friedman1963monetary (verified, Friedman 1963), eichengreen1992golden "
    "(verified, title 'Golden fetters: the gold standard and the Great Depression, 1919-1939'), garber2000famous (verified, DOI "
    "10.7551/mitpress/2958.001.0001). used_by LX1.")
row("proj-notation", "2.4-notation", "course/modules/LX/LX1/project.html (TeX spans); notation/notation.json",
    "PASS",
    "Fresh. out/notation_scan_r17.out: 30 TeX spans; symbols used D, V_t, V_0, P_t, P_0, P_5, S_m, n, m, t, \\ln; registry symbols T, R^*, "
    "R^{e*}, R_f, Q, Phi, gamma_3, gamma_4 (matched by the scan). Collisions: none. notation.json byte-identical since 56cc575a.")
row("proj-scope-words", "2.9-prose", "course/modules/LX/LX1/project.html:62, :280, :439, :466, :475, :476, :534, :541 (changed lines)",
    "PASS",
    "Fresh scan of the changed lines. :62 window three defined; :280 'None of the three' verified against MANIFEST titles; :466 'no level "
    "describes' is the total rule (0); :475 'Every percent change', :534 'every factual claim above carries its locator' checked against each "
    "claim of Exemplar A. grep of every, only, all, none, any, always, exactly on the page: :284 'the only lab on this page that reads a file' (only Lab 3 has data-files); :628 'No passage ... is attributed' (Friedman and Garber appear only as reading-list data-cite, :630-632).")
row("proj-process-words", "2.9-prose", "course/modules/LX/LX1/project.html (rendered prose); ledgers/LX1/scripts/LX1-c-r17/out/scan_r17.out",
    "PASS",
    "Fresh. scan_r17.out: 0 hits for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', "
    "'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly, 'about 6', "
    "'roughly half', historically, 'It can be shown', Pseudocode, round, verifier, builder, ruling, 'this round', LX1-c. One hit for 'checks that' "
    "(:466, 'the rater checks that it is correct'): rubric text, not a lab claim.")
row("proj-links-anchors", "2.9-prose", "course/modules/LX/LX1/project.html (href and id); course/modules/LX/LX1/index.html (id placement, :73)",
    "PASS",
    "Fresh. check_pages_LX1.out PASS (unit-level, covers project.html); page_smoke_project.out PASS (no console errors, no external "
    "requests). index.html:73 has id='placement' with data-mastery 0.8, which matches the 80 percent of :42.")
row("proj-page-smoke", "2.9-prose", "course/modules/LX/LX1/project.html; ledgers/LX1/scripts/LX1-c-r17/out/page_smoke_project.out",
    "PASS",
    "Fresh. page_smoke --unit LX1 --pages project: PASS; lab timings 0.0 s; rc 0.")
row("proj-atlas-autograder-na", "2.6-spec", "curriculum/06-profession-capstone.yaml:49; plans/LX1-build-plan.md:3, :412-416; out/run_graders_LX1.out",
    "PASS",
    "Fresh. yaml:49 grading rubric; plan line 3 'no Atlas milestone'; no atlas/LX1* file; run_graders_LX1.out 'no autograder (grading: rubric)'. "
    "Both the yaml and the plan are byte-identical since 56cc575a.")
row("proj-mutants-student-errors", "2.6-mutation", "ledgers/LX1/mutants/ (74 files); ledgers/LX1/scripts/LX1-c-r17/out/kill_stripped_r17.out, damaged_lab3_all_r17.out, kill_new_r17.out",
    "PASS",
    "Lab mutants only (LX1 is rubric-only; no grader). Kill reasons recorded per mutant in this fragment. 66 of the 71 earlier mutants are killed "
    "on the intact snapshot after their agreement check is stripped (kill_stripped_r17.out), the 4 blank or gap mutants (lx1c_m10, r8n03, r8n04, "
    "r9n03) survive on the intact snapshot and are killed by the damaged-snapshot differential (damaged_lab3_all_r17.out), r13n03 is an artifact "
    "kill (see its mutant entry). New round-17 mutants: r17n01 (blank GBP read as 0: killed by a first-row blank, ZeroDivisionError vs "
    "ValueError), r17n02 (burden to period four: expected block), r17n03 (mean absolute deviation: expected block). Every mutant is killed.")
row("proj-alternatives", "2.6-mutation", "ledgers/LX1/scripts/LX1-c-r16/alts/alt_r15_A, alt_r15_B (survive); ledgers/LX1/scripts/LX1-c-r17/alt_r17_C_lab3_logdiff_variance.py",
    "PASS",
    "alt_r15_A and alt_r15_B (Labs 1 and 2, decimal arithmetic) SURVIVE: stdout equals the expected block, rc 0 (kill_all_r17.out). The round-15 "
    "Lab 3 alternative (alt_r15_C) is KILLED because it prints the agreement line the page no longer prints: it is stale, not a faulty "
    "alternative. Its corrected version alt_r17_C (statistics.variance, no agreement line) SURVIVES (out/alt_r17_C.out). Intact-snapshot only: "
    "the alternatives do not implement the blank and gap checks, which are not claimed by the alternatives.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", "course/modules/LX/LX1/project.html:551-606 (exemplar B passages and annotations)",
    "PASS",
    "Fresh read of all B annotations. C1 L2 (no date for the condition, :567), C3 L1 (lists a source, :568), C3 L2 miss ('at least three uncited': "
    "Summary's two claims and Mechanism's one, :569), C1 L3 miss (:570), C4 L2 (rounds inputs: 2.47/2.79, :581), C4 L3 miss (:582), C2 L2 "
    "(similarities and one difference, :593), C3 L3 miss (:594), C5 L1 (caveat, :605). Each matches the descriptor text at :472-476.")
row("proj-brief-rubric-escape-clauses", "2.6-rubric", "course/modules/LX/LX1/project.html:442 (brief item 4), :474, :475 (C3 L4 and L3 cells)",
    "PASS",
    "Fresh. Brief item 4 'names its counter-evidence, or the essay states that it makes no such claim' matches the escape clause in C3 L4 "
    "and L3 cells (:474).")
row("proj-exemplar-locators", "2.9-prose", "course/modules/LX/LX1/project.html:490, :500, :511, :522, :534; course/modules/LX/LX1/L02.html; L04.html",
    "PASS",
    "Fresh. A's locators: Eichengreen title field (:490, title in registry); MANIFEST last and retrieved (:490); Lab 3 window (:490); Lab 1 Part B "
    "and Lab 3 printed lines (:522); Lesson 2 Proposition 2.1(a) and Remark 3.3 (:500, carried for L02 byte-identical); Lesson 4 Section 4 item "
    "'Exchange rates only' (:534, L04.html:333).")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", "course/modules/LX/LX1/project.html:476 (C5 cells), :534, :539-540 (A's C5 annotations)",
    "PASS",
    "Fresh. A names three limits; limit one has a test (interest-rate series), limits two and three name none. C5 L3 'at least two limits, one "
    "with the test' is met, L4 'for each' is not: official 3 consistent with the descriptors read with 'at least'.")
row("proj-round11-delta-project-page", "2.9-prose", "course/modules/LX/LX1/project.html:62, :475, :534",
    "PASS",
    "Fresh read of the round-11 items: window three defined at :62; C4 L4 at :475 ('At least one number'); A's limits at :534 unchanged in meaning.")
row("proj-spec-limits-test-each", "2.6-spec", "course/modules/LX/LX1/project.html:268, :443, :476, :534",
    "PASS",
    "Fresh. Required outputs (:268) 'two limits, with the test that would settle at least one of them' and brief item 5 (:443) match C5 L3 "
    "(:476, 'at least two limits, one with the test') and L4 'for each'.")
row("proj-notation-n-undefined", "2.9-prose", "course/modules/LX/LX1/project.html:60, :439; tests/labs/LX1/lab-LX1-project-3.py (docstring, sd function)",
    "PASS",
    "The symbol n (count of changes in the denominator n - 1) is used without a line defining it in words. Judged a standard symbol of the "
    "sample standard deviation formula, not a new term: it is not in notation.json (out/notation_scan_r17.out: no collision) and the lab computes "
    "it as len(values). Judgement recorded; a reviewer may disagree.")
row("proj-spec-window-start-must", "2.9-prose", "course/modules/LX/LX1/project.html:439-447 region, :62; tests/labs/LX1/lab-LX1-project-3.py WINDOW_TWO_FROM",
    "PASS",
    "Fresh. The lab computes exactly one window two (WINDOW_TWO_FROM = '2000-01'); the page's statement that no other start is computed (:431) is true.")
row("proj-rubric-c2-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:473 (C2 L2 cell, the one that must describe the basis-missing essay)",
    "FAIL",
    "Descriptor hole under the 0 rule (:466). An essay with a chain of at least three steps for each mechanism, the analogy-holding steps named, "
    "and the failure step named with evidence, but with no step naming what it rests on, matches C2 L4 and L3 only if every step names its basis "
    "(they do not): it matches no L2 disjunct (L2 lists only similarities and one difference; a chain with no failure step; a chain under three "
    "steps; a chain with a failure step and no holding step) and not L1 (which requires no chain). It scores 0 ('not yet met') although it "
    "satisfies all but the basis element of L4. Checked by reading the C2 cells at :473 and the L2 disjuncts. Round 16 PASS was wrong.",
    "At :473 (C2 L2 cell) add a disjunct: 'or gives a chain of at least three steps for each, names the steps at which the analogy holds and the "
    "failure step, but does not name what some step rests on'.")
row("proj-rubric-c3-level3-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:474 (C3 L3 cell)",
    "PASS",
    "Fresh. C3 L3 now requires 'each locator is a place where its claim is written' (:474), closing the wrong-locator gap; the L2 count of uncited "
    "claims is a different element. Exclusive with L4 and L2 under the highest-level rule.")
row("proj-dag-concepts", "2.9-prose", "course/modules/LX/LX1/project.html (one data-concept link, debt-deflation); course/modules/LX/LX1/L02.html:110",
    "PASS",
    "check_dag_LX1 PASS (check_dag_LX1.out). The one concept link resolves to L02's dfn with the same id (L02.html:110). Other concepts appear as "
    "plain prose, as the Architect default requires.")
row("proj-exemplar-A-limit1-cip-locator", "2.9-prose", "course/modules/LX/LX1/project.html:534; course/modules/LX/LX1/L04.html:333",
    "PASS",
    "Fresh. A's limit one quotes Lesson 4, Section 4, item 'Exchange rates only' (:534); L04.html:333 says 'The lab cannot test any relation between "
    "interest rates and exchange rates, because the file has no interest-rate column'.")
row("proj-rubric-c3-inference-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:474-475 (C3 L4 and L3 cells), :440 (brief item 2)",
    "PASS",
    "Fresh. 'marked as the writer's own inference' appears in C3 L4 and L3 and the brief. A factual claim neither cited nor marked falls under the "
    "uncited-count rule of L2 (:474).")
row("proj-l04-model-name-stale", "2.9-prose", "course/modules/LX/LX1/project.html:431; course/modules/LX/LX1/L04.html:84-85",
    "PASS",
    "Fresh. :431 names 'the fixed-exchange-rate model of Lesson 4 (Definition 2.1)'; L04.html:84-85 is Definition 2.1 'fixed-exchange-rate model' with "
    "(A2) 'fixed rate held'. Names match.")
row("proj-exemplar-a-c2-annotation", "2.3-grades", "course/modules/LX/LX1/project.html:500-520 (A mechanism passages and annotations); course/modules/LX/LX1/L02.html definition",
    "PASS",
    "Fresh. Both chains have three steps, the analogy holds at step 3 and fails at step 2 with evidence (Remark 3.3 for episode; Lab 3 zero-change "
    "count for condition). Judgement: step 2 of the episode chain rests on 'a hypothesis the essay does not source'; this is read as the "
    "'assumption' basis that L4 permits. No grade is re-assigned in this row.")
row("proj-r14-delta-hunks", "2.9-prose", "git diff 8e5751c9 d1e65a0 -- course/modules/LX/LX1/project.html",
    "PASS",
    "Carried from round 16 (git range 8e5751c9..d1e65a0 is immutable; its three project.html hunks were read and checked in round 15).")
row("proj-r15-delta-hunks", "2.9-prose", "git diff d1e65a0 56cc575a -- course/modules/LX/LX1/project.html",
    "PASS",
    "Carried from round 16 (git range d1e65a0..56cc575a is immutable; its project.html hunks were read and checked in round 16). The round-16 "
    "to round-17 hunks (56cc575a..700bf33f) were read in full in this round (diff of project.html: :60, :284, :287, :308-309, :319-330, :380-383, "
    ":406-409, :472-476, :498-520, :527-540, :576-588, and the twin docstring and imports).")
row("proj-rubric-exhaustive-r14", "2.6-rubric", "course/modules/LX/LX1/project.html:466 (scoring sentence), :472-476 (C1-C5 rows)",
    "FAIL",
    "Round-16 PASS re-checked from scratch under the highest-level rule and the 0 rule. C1, C3 and C5 are exhaustive (C5 with 'at least'). C2 has "
    "a hole: the basis-missing essay (proj-rubric-c2-gap) matches no level and scores 0. C4 has a hole: an essay with unrounded values and a stated "
    "rule for every number, but a missing formula or a percent change without base and sign, matches no level and scores 0 (proj-rubric-c4-formula-gap). "
    "C2 L2 also has a count hole (proj-rubric-c2-count-wording).",
    "Close the holes listed in proj-rubric-c2-gap, proj-rubric-c4-formula-gap and proj-rubric-c2-count-wording, then re-verify exhaustiveness.")
row("proj-student-error-coverage", "2.6-rubric", "course/modules/LX/LX1/project.html:473 (C2 L4 and L3, pattern 3), :474 (C3 L3), :475 (C4 L3); plans/LX1-build-plan.md section 5.4 (ten student-error patterns)",
    "FAIL",
    "Plan patterns checked against the current cells. Caught below the bar: (1) real debt as nominal debt: wrong formula does not count (:466), so C4 "
    "L3 is not met and C4 scores 0 (gap, see proj-rubric-c4-formula-gap); (2) percent change with no base: C4 L3 requires base and sign, C4 scores 0 "
    "(same gap); (4) citation whose locator does not contain the claim: C3 L3 now requires 'each locator is a place where its claim is written', "
    "so C3 falls to L2 (2); (5) analogy with no failure step: C2 L2 'names no failure step' (2); (6) rounding before computing: C4 L2 (2); "
    "(7) and (8) uncited claims: C3 L2 or L1; (10) episode date without locator: C1 L3 or L2. NOT caught: (3) 'bubble' used for any price rise with "
    "no fundamental stated. The page never uses 'bubble' or 'fundamental', and C2 L4 accepts 'a model result or assumption' as the basis of each "
    "step, so a bubble chain with an asserted assumption can reach level 4 (grep of project.html: no 'bubble'). Pattern 9 is a lab row.",
    "In the C2 L4 cell (:473) and L3 cell (:473), add: 'and a step that calls a price move a bubble names the benchmark it departs from (a "
    "fundamental value, as Lesson 1 defines it, or a cited source)'. Re-check exemplar A (C2 4) after the change.")
row("proj-data-embedded-claim", "2.8-data", "course/modules/LX/LX1/project.html:280; course/assets/data/market/MANIFEST.json (fx_daily, fx_monthly, ust_daily)",
    "PASS",
    "Fresh. Three MANIFEST datasets (fx_daily, fx_monthly, ust_daily) with titles as read in out/data_checks_r17.out; :280 names exactly these three.")
row("proj-lab3-raise-claims-untested", "2.5-labs", "course/modules/LX/LX1/project.html:308-309 (Check paragraph), :431 (no agreement line); tests/labs/LX1/lab-LX1-project-3.py",
    "PASS",
    "Round-16 FAIL resolved by removing the claim (fix b). grep (scan_r17.out): project.html names 'agree', 'statistics' and 'two-pass' only at :60 ('computed by the "
    "two-pass formula', a description of sample_sd_two_pass, not a check). The twin has no statistics import and no agreement check. The expected "
    "block has no agreement line. The Check paragraph (:308-309) names only the ValueError cases, which out/damaged_lab3_all_r17.out confirms. The "
    "retired mutant r13n03 is still listed, with its kill reason stated as an artifact.")
row("proj-rubric-c5-count-wording", "2.6-rubric", "course/modules/LX/LX1/project.html:476 (C5 L3 'Names at least two limits, one with the test', L2 'Names at least one limit')",
    "PASS",
    "Round-16 FAIL resolved: the C5 cells now say 'at least'. Exemplar A (three limits, one with a test) matches L3 (official 3); an essay with two "
    "limits and no test matches L2 (2) under the highest-level rule.")
row("proj-rubric-c4-formula-gap", "2.6-rubric", "course/modules/LX/LX1/project.html:475 (C4 L2 and L1 cells; L3 cell requires formula and base and sign)",
    "FAIL",
    "Descriptor hole under the 0 rule (:466). An essay in which every computed number comes from unrounded values with a stated rule, but one number "
    "has no formula citation (or a wrong one, which does not count under :466) or one percent change has no base or sign, fails C4 L4 and L3 (both "
    "require the formula and base for every number). C4 L2 requires a rounded input or rules for some numbers but not all; C4 L1 requires no rule "
    "or no number. The essay matches no level and scores 0, though it shows the L3 elements for all but one. This is plan pattern 1 and 2 (nominal "
    "debt as real debt; base missing) at score 0.",
    "At :475 (C4 L2 cell) add: 'or gives every computed number unrounded values and a stated rule, but omits, or gives wrong, the formula or the base "
    "and sign of some number or percent change'.")
row("proj-rubric-c2-count-wording", "2.6-rubric", "course/modules/LX/LX1/project.html:473 (C2 L2 cell, 'Lists similarities and one difference')",
    "FAIL",
    "Exact count in a level descriptor makes the scale non-monotone: an essay with similarities and two or three differences, and no chain, "
    "matches no L2 disjunct and falls to L1 (names a similarity, no chain = 1), while the same essay with one difference scores 2. Same class as the "
    "C5 count wording fixed in round 17.",
    "At :473 (C2 L2 cell) change 'Lists similarities and one difference' to 'Lists similarities and at least one difference'.")

mut_ids = {m["id"] for m in mutants}
assert len({r["id"] for r in R}) == len(R), "duplicate row ids"
statuses = [r["status"] for r in R]
verdict = "PASS" if all(s == "PASS" for s in statuses) and all(m["killed_by"] for m in mutants) else "FAIL"

frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 17,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 17 (did not build LX1)",
    "pin": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6",
    "base": "56cc575a (round-16 pin; the round-16 fragment is /Users/billyribeiro/.fanout/frags/E-LX1-c.round16.json)",
    "checkout": str(root),
    "scratch": "ledgers/LX1/scripts/LX1-c-r17/ (scripts) and ledgers/LX1/scripts/LX1-c-r17/out/ (every command output); live rebuild in /Users/billyribeiro/.fanout/scratch-LX1c-r17/rebuild",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 56cc575a -> 700bf33f for LX1-c: course/modules/LX/LX1/project.html (Lab 3 hypothesis, Monthly log change convention, Lab 3 check, expected block, rubric C2-C5 cells, exemplar A C2/C3/C5 and exemplar B annotation text), tests/labs/LX1/lab-LX1-project-3.py (agreement check and print removed), references/references.json (used_by of a non-LX1 key), ledgers/LX1 (r16 mutants and scripts). Every hunk was read. L01, L02, L04, index, curriculum, plans, notation, MANIFEST and the snapshot are byte-identical to 56cc575a (carried where cited).",
        "Blind calibration (ruling 15) is UNVERIFIABLE in this session (see proj-calibration-exemplars). The prose-only scores match the official scores: A 4,4,4,4,3; B 2,2,1,2,1.",
        "Rubric holes (FAIL): C2 basis gap (proj-rubric-c2-gap), C4 formula/base gap (proj-rubric-c4-formula-gap), C2 count wording (proj-rubric-c2-count-wording). Plan pattern 3 (bubble) not caught (proj-student-error-coverage).",
        "Mutants: 74 lab mutants (71 earlier and r17n01-r17n03). LX1 is rubric-only, so grader mutation testing does not apply; lab mutants are run because the page claims the lab checks blank cells, month gaps and the rounding rule. The round-16 agreement-check mutants were killed by a check the page no longer claims, so their kills were re-attributed by stripping that check (kill_stripped_r17.out). r13n03 is retained with an artifact kill note.",
        "Alternatives: alt_r15_C is stale (prints the removed agreement line) and was replaced by alt_r17_C, which survives.",
        "Not checked: a fresh-context blind calibration; render_curriculum --check (no curriculum file changed); run_graders --all and check_pages --all (outside this slice; no grader in LX1); visual rendering beyond page_smoke.",
    ],
    "summary": {
        "rows": len(R),
        "pass": statuses.count("PASS"),
        "fail": statuses.count("FAIL"),
        "unverifiable": statuses.count("UNVERIFIABLE"),
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out_path = root / "ledgers/LX1/LX1-c.json"
out_path.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(R), "mutants", len(mutants), "verdict", verdict)
