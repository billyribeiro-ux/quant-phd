import json, pathlib, sys
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c")
S = "ledgers/LX1/scripts/LX1-c-r4/"
R = "Re-verified round 4 at pin 9a02b1a: "
rows = [
 ("proj-rung1-step3-rounding-claim", "2.6 spec (rung 1 worked steps) / 2.4 arithmetic", "course/modules/LX/LX1/project.html:173, :175", "PASS",
  R + "rederive_r4.out: 10000000/0.85 = 11764705.882 cents -> 117647.06; difference 3069053.708 cents -> 30690.54. Page expected block (lines 146-167) equals twin output (out/lab_check.out, project-1 stdout == expected: True)."),
 ("proj-real-value-vs-lesson2", "2.4 notation and Lesson 2 attribution", "project.html:56, :500; course/modules/LX/LX1/L02.html:84, :89-90 (A2, A3), :97 (D P_0 cancels), :123", "PASS",
  R + "L02.html:84 says Prop 2.1 uses (A2),(A3); :89-90 define them; :97 proves V_t/V_{t-1} = P_{t-1}/P_t with the factor D P_0 cancelling. Page :56 states V_t = D P_0/P_t with P_0 = 1 and names the labs' A1/A2 as their own."),
 ("proj-manifest-note-misattributed", "2.4 data attribution", "project.html:267, :275, :289-292 (lab 3 docstring); course/assets/data/market/MANIFEST.json fx_monthly", "PASS",
  R + "MANIFEST fx_monthly: rows 669, first 1971-01, last 2026-09, retrieved 2026-10-19, transform 'month-end (each column's last value in the month); CAD, CHF, DKK, JPY, NOK, SEK inverted', title 'USD per unit of foreign currency'. Page claims match each field."),
 ("proj-lab3-citation-string", "2.4 citation string", "project.html:277, :285; lab-LX1-project-3 docstring", "PASS",
  R + "Citation string on page equals MANIFEST citation field (checked by program: 'citation on page: True')."),
 ("proj-reading-reinhart-registry", "registry keys on the reading list", "project.html:627-634", "PASS",
  R + "references/references.json holds eichengreen1992golden (line 7946), friedman1963monetary (9399), garber2000famous (9667). grep -c reinhart project.html = 0 (out/final_checks.out)."),
 ("proj-spec-current-undefined", "brief item 1: current condition defined", "project.html:440, :280", "PASS",
  R + "Brief item 1 dates the current condition within the twelve months ending at the last data month, 2025-10 to 2026-09 = window three; Lab 3 expected prints 12 changes (project.html:425-426)."),
 ("proj-exemplar-A-condition", "exemplar A episode and condition dating", "project.html:489-493", "PASS",
  R + "Exemplar A unchanged this round (diff hunks do not touch 485-545). Condition window 2025-10 to 2026-09; MANIFEST last = 2026-09 (field present)."),
 ("proj-gate-commands", "gate commands on pin 9a02b1a", "tools/check_projects.py, check_pages.py, check_dag.py, run_labs.py, fetch_data.py, verify_refs.py, page_smoke.py; ruff; mypy; pytest", "PASS",
  R + "out/gates1.out: check_projects LX1: PASS; check_pages LX1: PASS; check_dag LX1: PASS; run_labs LX1: PASS (7/7); fetch_data: 3 datasets, 0 problems; offline integrity: 560 entries, 0 problems. page_smoke project.html --skip-sweep: PASS (out/page_smoke_project.out). out/lint_pytest.out: ruff check and ruff format --check on tests/labs/LX1 pass; mypy --no-incremental on the three project twins: no issues in 3 source files; pytest test_labs/test_run_labs/test_page_checks: all pass."),
 ("proj-lab1-twin-run", "lab 1 twin run and page code", "tests/labs/LX1/lab-LX1-project-1.py; project.html:76-147", "PASS",
  R + "out/lab_check.out: page code == twin (trailing newline aside): True; python -I -W error rc=0, stderr empty, stdout == expected block: True."),
 ("proj-lab1-numbers", "lab 1 hypothesis, expected block, interpretation", "project.html:75, :148-167, :168", "PASS",
  R + "out/rederive_r4.out: 17.647058... -> 17.65; -13.043478... -> -13.04; 11764705.88 and 8695652.17 cents; difference 3069053.708 cents -> 30690.54. Hypothesis line 75 matches."),
 ("proj-lab2-twin-run", "lab 2 completion twin and page code", "tests/labs/LX1/lab-LX1-project-2.py; project.html:183-255", "PASS",
  R + "Page code differs from twin only at the two blanked returns (lines 212, 217 show ___); all other lines equal. Twin run rc=0, stderr empty, stdout == expected block (lab_check.out)."),
 ("proj-lab2-numbers", "lab 2 hypothesis, expected block", "project.html:182, :245-254", "PASS",
  R + "rederive_r4.out: 40000/0.93 = 4301075.27 cents -> 43010.75; burden 100(1/0.93 - 1) = 7.5269 -> 7.53; 40404.04, 40816.33, 41666.67, 42105.26 match expected lines 247-252."),
 ("proj-lab2-check-claims", "lab 2 interpretation claims about failing mutants", "project.html:255", "PASS",
  R + "Inverted ratio gives -7.00 (rederive_r4.out: 100(0.93-1) = -7.00); out/run_r4.out: lx1c_m02 first diff '  change: -7.00'; no-division mutant m01 prints 40000.00 in every period (out/run_r4.out)."),
 ("proj-lab3-twin-run", "lab 3 twin run, data read and page code", "tests/labs/LX1/lab-LX1-project-3.py; project.html:286-431", "PASS",
  R + "out/lab_check.out: page code == twin: True; rc=0 with data/fx_monthly.csv in scratch; stdout == expected: True. Lab 3 alone reads a file (project.html:282 'only lab on this page that reads a file' holds: labs 1-2 have no data-files)."),
 ("proj-lab3-numbers", "lab 3 hypothesis and expected block", "project.html:285, :411-431", "PASS",
  R + "out/rederive_r4.out (Decimal, 50 digits): window one 668 changes, 3 zeros (1976-07, 2012-07, 2019-11), sd 0.027935 -> 2.79; window two 321 changes, 2 zeros, sd 0.024700 -> 2.47; window three 12 changes, 0 zeros, sd 0.019020 -> 1.90; largest 13.5846 (1985-03), -9.6575 (2008-10), 2.9594 (2026-04); ratio 0.88417 -> 0.88."),
 ("proj-lab3-L04-cross-check", "lab 3 vs Lesson 4 lab output", "project.html:282, :296; course/modules/LX/LX1/L04.html:307-315", "PASS",
  R + "L04 expected prints window one sd 0.027935, window two sd 0.024700, ratio 0.8842; project lab 3 prints 2.79, 2.47 and 0.88 from the same unrounded values (rederive_r4.out)."),
 ("proj-lab3-docstring-claims", "lab 3 docstring and stated ValueError behaviour", "tests/labs/LX1/lab-LX1-project-3.py docstring (project.html:286-312)", "PASS",
  R + "out/raise_checks.out: blank GBP cell -> ValueError; non-decimal '1.5x' -> ValueError; month gap -> ValueError 'month 1996-02 does not follow 1995-12'; forced disagreement (AGREEMENT=-1) -> ValueError; unmodified twin on full file rc=0. Docstring 'No row is skipped or filled' matches load_column."),
 ("proj-lab3-interpretation-claims", "lab 3 interpretation claims", "project.html:432; course/modules/LX/LX1/L04.html:84 (Definition 2.1)", "PASS",
  R + "Difference of unrounded sds 0.3236 -> 0.32 (rederive_r4.out). Window three 12 changes, n-1 = 11. Window two zeros at 2012-07 and 2019-11 (rederive_r4.out). 321 zero changes under parity is arithmetic (321 changes). L04 Definition 2.1 is the fixed-parity model."),
 ("proj-lab-simulated-labels", "SIMULATED labels on labs 1-2 and Lab 3 real-data label", "project.html:42, :44, :71-75, :178-182, :281-285", "PASS",
  R + "Labs 1 and 2 are labelled SIMULATED (project.html:42, :75, :182) and read no file (no data-files attribute); Lab 3 has data-files=\"fx_monthly.csv\" (:283)."),
 ("proj-data-licence-quote", "data licence quote", "project.html:277; course/assets/data/market/MANIFEST.json fx_monthly licence; tools/data_sources.yaml licence", "PASS",
  R + "Programmatic check (out/final_checks.out): the quoted licence sentence occurs verbatim in project.html and equals MANIFEST licence; licence_url federalreserve.gov/disclaimer.htm matches."),
 ("proj-data-snapshot-rebuild", "snapshot matches MANIFEST", "course/assets/data/market/fx_monthly.csv; MANIFEST.json; tools/fetch_data.py --check", "PASS",
  R + "fetch_data --check: 3 datasets, 0 problems (out/gates1.out). Lab 3 reads the snapshot and prints 669 months (out/lab_check.out)."),
 ("proj-data-fields", "data field claims", "project.html:277, :269; MANIFEST fx_monthly columns; fx_monthly.csv header", "PASS",
  R + "CSV header: month, AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK (no interest-rate column); EUR blank count 336, first non-blank 1999-01; GBP blank count 0 (out/rederive_r4.out)."),
 ("proj-data-no-other-series", "no other series embedded; no redistribution grant recorded", "project.html:278; tools/data_sources.yaml (ids)", "PASS",
  R + "data_sources.yaml lists exactly three ids (fx_daily, fx_monthly, ust_daily); no gold, price-level, output, unemployment or bank-failure series is embedded or granted (out/final_checks.out)."),
 ("proj-spec-ladder", "ladder and rung structure", "project.html:40-48, :71-170, :178-255, :257-280, :616", "PASS",
  R + "Ladder rungs and their sections exist; rung 3 spec at :262-271 (edited this round, re-read in full); rung 4 at :619-625."),
 ("proj-spec-curriculum-scope", "brief scope vs curriculum", "curriculum/06-profession-capstone.yaml:19-49; project.html:262-271, :437-447", "PASS",
  R + "Curriculum project brief: pick one episode and one current condition, mechanism-level comparison where analogy holds and breaks, two-page essay, every claim cited, grading rubric. Page brief and spec are consistent with it."),
 ("proj-hours", "time budget arithmetic", "project.html:33, :449-461; course/modules/LX/LX1/index.html:29 (data-hours-lessons=40, data-hours-project=10)", "PASS",
  R + "Table rows 1, 1, 2, 1.5, 2.5, 2 sum to 10; data-hours-project=10; index 40 + 10 = 50 hours."),
 ("proj-rubric-observable", "rubric levels observable", "project.html:469-478", "PASS",
  R + "Rubric table unchanged this round; every level names an element a reader can check (re-read in full)."),
 ("proj-calibration-exemplars", "exemplar scores vs annotations and rubric", "project.html:485, :487, :547, :549, :566-573", "PASS",
  R + "data-scores A 4,4,4,4,3 and B 2,2,1,2,1 match the verdict text (:487, :549). Annotated levels for B: C1 L2 (meets), C2 L2, C3 L1 (meets), C4 L2, C5 L1 each match the descriptor text at :473-477. The C4 L3 miss annotation is handled in proj-exemplar-b-annotations-vs-descriptors."),
 ("proj-exemplar-locators", "exemplar A locators", "project.html:489-493, :500-506, :511-519, :523-528, :535-541", "PASS",
  R + "Episode locator = title field of eichengreen1992golden (title matches registry line 7951); condition locator = MANIFEST last (2026-09); Lesson 2 Prop 2.1(a) and Remark 3.3 (L02.html:127-129) exist and say what A says."),
 ("proj-exemplar-numbers", "exemplar numbers and their citations and rules", "project.html:523-524 (A Numbers), :535 (A Limits), :577-578 (B Numbers)", "FAIL",
  R + "A Numbers (:523-524) states the rule and cites Lab 1 Part B and Lab 3: values 17.65, 2.47, 2.79, 1.90, 0.88 all verified. But A's Limits passage (:535) prints 13.58 percent in 1985-03 and 0.32 percent per month with no lab line and no rounding rule (only 'from unrounded values'). The Meets-C4-level-4 annotation at :528 says each number has its lab line cited and its rule stated, and the rubric C4 level 4 requires both for each computed number. Verified values: 13.5846 (1985-03) and difference 0.3236 (rederive_r4.out). B Numbers (:578): 2.47/2.79 = 0.8853 -> 0.89 and the unrounded ratio 0.8842 -> 0.88 (annotation :582 correct)."),
 ("proj-reading-keys", "reading list keys", "project.html:624-634", "PASS",
  R + "Keys friedman1963monetary, eichengreen1992golden, garber2000famous present in references.json; no other key cited on the page (grep)."),
 ("proj-notation", "notation registry", "project.html math spans; notation/notation.json", "PASS",
  R + "Page symbols D, P_0, P_t, V_t, S_m, m, t, n are not program-wide registered symbols (registry lists T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q); each is defined locally in Conventions (:55-62) or the lab docstrings. No registered symbol reused with a different meaning."),
 ("proj-scope-words", "scope words", "project.html:7, :62, :253, :267, :269, :295, :432, :587", "PASS",
  R + "'only' at :282 ('the only lab on this page that reads a file') is true (labs 1-2 have no data-files). 'all' at :285 and :535 refer to a counted set (all 12 changes; the window). 'every' statements at :269 and :475 are the rubric or spec obligations, not numerical claims."),
 ("proj-process-words", "process words in learner text", "project.html (all prose, labs, comments)", "PASS",
  R + "No builder or review-process wording in learner text; 'Predicted before running' at :75/:285 is the standard lab hypothesis label used on all labs (same label in L04.html:67)."),
 ("proj-links-anchors", "links and anchors", "project.html (all href and id targets); course/modules/LX/LX1/L02.html:110 (def-debt-deflation)", "PASS",
  R + "check_pages LX1: PASS (out/gates1.out); link targets resolve (L02.html def-debt-deflation anchor exists, :110)."),
 ("proj-page-smoke", "page smoke", "course/modules/LX/LX1/project.html", "PASS",
  R + "page_smoke --unit LX1 --pages project.html --skip-sweep: PASS (out/page_smoke_project.out)."),
 ("proj-atlas-autograder-na", "no autograder for the project", "curriculum/06-profession-capstone.yaml:19-49; tools/mutate_graders.py --unit LX1", "PASS",
  R + "Curriculum grading is 'rubric'; tools/mutate_graders.py --unit LX1 exits 0 with no output (no graders for LX1); the project is rubric-only (project.html:271)."),
 ("proj-mutants-student-errors", "student-error mutants", "ledgers/LX1/mutants/*.py (24 files); out/run_r4.out", "PASS",
  R + "All 24 mutants killed: 18 existing (m01-m10, r2n01-04, r3n01-04) and 6 new this round (r4n01-06: burden as share of end price, debt typed in dollars, burden rounded to whole percent, window one drops first change, sd reported per year, window two from 1999-12). Each differs from its target lab expected block (out/run_r4.out)."),
 ("proj-alternatives", "alternative correct implementations", "ledgers/LX1/scripts/LX1-c-r4/gen/alt_lab1_integer_cents.py, alt_lab2_decimal.py, alt_lab3_welford.py", "PASS",
  R + "Three independent correct implementations (integer cents with exact rational rounding; Decimal at 60 digits; Welford standard deviation) each match their lab expected block exactly (out/run_r4.out)."),
 ("proj-exemplar-a-c2-annotation", "exemplar A C2 annotations", "project.html:501-508, :511-519", "PASS",
  R + "Both chains have three steps, the failure at step 2, evidence Remark 3.3 (L02.html:127-129) and Lab 3's zero-change line (project.html:427). Matches C2 L4 descriptor."),
 ("proj-exemplar-b-annotations-vs-descriptors", "exemplar B annotations vs rubric descriptors", "project.html:582 (C4 annotation), :583; descriptor C4 at :476", "FAIL",
  R + "The round-3 defects are fixed: C1 L2 and C3 L1 now match descriptors (:473-475). The C4 L3 'Misses' annotation at :583 says 'the figure is per month and is stated as per year, so its unit is wrong'. C4 descriptors (:476) cover rounding inputs, rounding rules and formula/lab citation only; no level mentions units. The miss at C4 L3 is real (ratio from rounded inputs; no stated rule) but the annotation names a reason outside the descriptor."),
 ("proj-brief-rubric-escape-clauses", "brief item 4 vs C3 level 4 vs spec", "project.html:443 (brief item 4), :475 (C3 L4), :269 (spec constraints), :263 (spec context)", "PASS",
  R + "Round-3 FAIL resolved: brief item 4 (:443), spec constraints (:269) and C3 level 4 (:475) now carry the same counter-evidence clause ('or the essay states that it makes no such claim') and the same inference clause. Exemplar A's C3 annotation (:539) uses the same wording."),
]
ids_r3 = ["proj-rung1-step3-rounding-claim","proj-real-value-vs-lesson2","proj-manifest-note-misattributed","proj-lab3-citation-string","proj-reading-reinhart-registry","proj-spec-current-undefined","proj-exemplar-A-condition","proj-gate-commands","proj-lab1-twin-run","proj-lab1-numbers","proj-lab2-twin-run","proj-lab2-numbers","proj-lab2-check-claims","proj-lab3-twin-run","proj-lab3-numbers","proj-lab3-L04-cross-check","proj-lab3-docstring-claims","proj-lab3-interpretation-claims","proj-lab-simulated-labels","proj-data-licence-quote","proj-data-snapshot-rebuild","proj-data-fields","proj-spec-ladder","proj-spec-curriculum-scope","proj-hours","proj-rubric-observable","proj-calibration-exemplars","proj-exemplar-locators","proj-exemplar-numbers","proj-reading-keys","proj-notation","proj-scope-words","proj-process-words","proj-links-anchors","proj-page-smoke","proj-atlas-autograder-na","proj-mutants-student-errors","proj-alternatives","proj-exemplar-a-c2-annotation","proj-exemplar-b-annotations-vs-descriptors","proj-brief-rubric-escape-clauses"]
got = [r[0] for r in rows]
assert sorted(set(ids_r3) - set(got)) == [], set(ids_r3) - set(got)
assert set(got) - set(ids_r3) == {"proj-data-no-other-series"}, set(got) - set(ids_r3)
print("row ids match round-3 set; count", len(rows), "fails", [r[0] for r in rows if r[3] != "PASS"])
FIX = {
 "proj-exemplar-numbers": "Add to exemplar A's Limits passage (project.html:535) the lab line and rule for 13.58 (Lab 3 window one line) and 0.32 (difference of the two Lab 3 sds): 'rounded half up to two decimals, Lab 3 window one and window two lines'; or lower exemplar A's C4 score to 3 and change its C4 annotation (:528) so it no longer claims every number has its lab line and rule.",
 "proj-exemplar-b-annotations-vs-descriptors": "Rewrite the C4 level-3 annotation at project.html:583 to cite the descriptor: 'Misses C4 level 3: the ratio is computed from rounded inputs, and no number in this passage states its rounding rule or cites its lab line.' Drop the unit remark from the C4 annotation (the unit point stays in the verdict text at :549 only).",
}
out_rows = [{"id": r[0], "check": r[1], "location": r[2], "status": r[3], "evidence": r[4], **({"fix": FIX[r[0]]} if r[3] != "PASS" else {})} for r in rows]
mutants = []
for p in sorted((ROOT / "ledgers/LX1/mutants").glob("*.py")):
    mutants.append({"name": p.name, "file": f"ledgers/LX1/mutants/{p.name}", "description": "student-error mutant of a project lab twin (existing or r4)", "killed_by": "target lab expected block mismatch (see " + S + "out/run_r4.out)"})
frag = {
 "unit": "LX1", "slice": "LX1-c", "round": 4,
 "verifier": "Claude Haiku 5.5, independent verifier for LX1-c, round 4 (did not build LX1)",
 "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
 "base": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b (round-3 pin). Delta read for project.html (lede, Conventions, Constraints, brief item 4, exemplar B), tests/labs/LX1/lab-LX1-L03-1.py and L03/L04 hunks as context. Every row re-verified from the current pin; no PASS carried.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c (detached at 9a02b1a, .venv symlinked)",
 "scratch": "/tmp/lx1c-r4-* (disposable; removed by harness)",
 "verified_at": "2026-11-04T09:00:00+00:00",
 "verdict": "FAIL",
 "rows": out_rows,
 "mutants": mutants,
 "registry_flags": ["eichengreen1992golden, friedman1963monetary, garber2000famous present in references/references.json (lines 7946, 9399, 9667). reinhart2009this not cited anywhere on the page."],
 "freshness_flags": ["fx_monthly MANIFEST retrieved 2026-10-19; unchanged in this pin."],
 "notes": [
  "Two FAIL rows: proj-exemplar-numbers (exemplar A Limits passage numbers 13.58 and 0.32 carry no lab line and no stated rounding rule while the C4 level-4 annotation says they do) and proj-exemplar-b-annotations-vs-descriptors (exemplar B C4 level-3 miss annotated with a unit error that no C4 descriptor covers).",
  "Round-3 FAIL rows: proj-brief-rubric-escape-clauses now PASS (wording matches across brief, spec and C3 level 4); exemplar B C1 and C3 annotations now match descriptors.",
  "Labs: 3/3 project twins run under python -I -W error with rc 0, empty stderr, stdout equal to expected block; page code equals twin for labs 1 and 3 and differs from twin for lab 2 only at the two blanks.",
  "Mutants: 24 of 24 killed (18 existing, 6 new). Alternatives: 3 of 3 independent implementations pass. Lab 3 stated ValueError behaviours verified on altered data.",
  "Not checked: full workspace gate (full pytest, mypy over the whole workspace, build_site --check, render_curriculum, the other LX1 slices); L03/L04 lesson content beyond the cross-checked lines (other slices); browser rubric form interaction beyond page_smoke; the reinhart/other reading entries' book-level content (no passage cited, so no attribution to check). Exemplar scoring was read against descriptors after reading annotations, not blind."
 ],
 "summary": "LX1-c round 4: verdict FAIL. 42 rows: 40 PASS, 2 FAIL (proj-exemplar-numbers, proj-exemplar-b-annotations-vs-descriptors). All gate commands, labs, mutants and alternatives pass on 9a02b1a. Both FAIL rows are rubric-annotation defects, not arithmetic defects; every Lab 3 figure re-derives exactly."
}
fp = ROOT / "ledgers/LX1/LX1-c.json"
fp.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", fp)
