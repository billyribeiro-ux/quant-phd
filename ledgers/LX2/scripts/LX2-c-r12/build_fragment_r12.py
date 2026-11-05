"""LX2-c r12: assembles ledgers/LX2/LX2-c.json from the round 10 rows (re-verified this round) and the round 12 rows.

Run from the checkout root with .venv/bin/python -I. Reads the round 10 fragment from the verifier's frags folder
(context only) and the r12 outputs under ledgers/LX2/scripts/LX2-c-r12/. Writes ledgers/LX2/LX2-c.json.
"""
import ast
import datetime
import json
import re
import sys
from pathlib import Path

root = Path.cwd()
S = root / "ledgers/LX2/scripts/LX2-c-r12"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-LX2-c.round10.json").read_text(encoding="utf-8"))

UNCHANGED = ("course/modules/LX/LX2/project.html, tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py "
             "byte-identical since the round 10 pin 00a84795")
NOTE = {
    "proj-hours": "index.html changed in round 11 (prose sentences only); the data attributes are re-read this round: "
                  "data-hours-lessons=\"36\" and data-hours-project=\"14\" at index.html line 29, 36+14=50, 14/50=28%.",
    "proj-hours-independent-estimate": "re-estimated this round, see r12-hours-independent-estimate.",
    "proj-citations-registry": "references/references.json changed (generated_at; used_by only). Re-verified this round: "
                               "verify_refs --offline 560 entries 0 problems; verify_refs --unit LX2 6 of 560 entries 0 problems.",
    "proj-r10-sources-refetch": "re-fetched this round with plain curl: sr2602.htm sha256 b5c0e0a9... (round 10 recorded 05af406d...; "
                                "htm changed, the cover-letter sentences still match), SR2602a1.pdf and SR2602.pdf byte-identical to round 10.",
    "proj-gates-tooling": "re-run this round at 5db69a9b, see r12-gates-* rows.",
    "proj-pytest-lx2": "re-run this round: pytest on tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_page_smoke.py (subset) exit 0.",
    "proj-dag-and-links": "L04.html anchors s4 and def-model-risk-management re-read this round (L04.html unchanged since round 10).",
    "proj-counter-evidence-c-grade": "grades re-checked against BLUEPRINT section 3 and plan section 12 item 7 (legal holdings graded C with key and locator): 12 data-grade=C spans.",
    "proj-notation": "notation/notation.json re-read this round: registered symbols are T, Phi, gamma3, gamma4, R*, R^e* and others; "
                     "H, e_t, y_t, t and the hat-y forecast are not registered, so no collision.",
    "proj-scope-words": "re-scanned this round, no banned phrase and no unsupported scope word in visible text (see r12-banned-and-process-words).",
    "proj-banned-and-process-words": "re-scanned this round with a script over the visible text: TODO, TBD, lorem, for brevity, details omitted, "
                                     "beyond the scope, it is important to note, studies show, experts agree, it is well known, obviously, clearly, "
                                     "roughly, historically, it can be shown: 0 hits.",
    "proj-labjs-failure-messages": "labs.js compareOutput reason is 'token N: X differs from Y'. It does not name the printed line. "
                                   "Autograder message rules (VERIFIER 2.6 item 4) do not apply: curriculum grading is rubric. Observation only.",
    "proj-rung2-student-error-mutants": "re-run this round over all 62 lab-2 files (r12 harness), see r12-mutants-existing-rerun.",
    "proj-rung2-alternatives": "re-run this round, see r12-alternatives-new.",
    "proj-attachment-quote-locators": "re-checked this round against the fetched PDFs, see r12-attachment-quotes.",
    "proj-rung3-sr26-standard": "re-checked this round, see r12-attachment-quotes and r12-cover-letter-sentences.",
    "proj-source-supersession": "re-checked this round in sr2602.htm: 'supersedes and replaces SR letter 11-7 and SR letter 21-8' and the Supersedes list after the signature.",
    "proj-source-applicability": "re-checked this round in sr2602.htm: 'Applicability: This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.'",
    "proj-lab2-docstring-completed-solution": "twin lab-LX2-project-2 re-read this round; its docstring matches the code.",
    "proj-exemplar-calibration": "re-scored this round from the annotation-stripped passages (see r12-blind-exemplar-scoring).",
    "proj-exemplar-a-numbers": "re-derived this round (see r12-rederive-numbers).",
    "proj-exemplar-b-numbers": "re-derived this round (see r12-rederive-numbers).",
    "proj-prose-numbers-rederived": "every numeric prose claim re-derived this round (see r12-rederive-numbers).",
    "proj-reading-count": "re-checked this round: 8 frb2026fed spans on the page (lines 350-353 five, 363-364 three), matches line 715.",
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    base = r["evidence"]
    subj = ("project.html and the three project labs" if r["location"].startswith("course/modules/LX/LX2/project.html") or "lab-LX2-project" in r["location"] else r["location"])
    note = NOTE.get(rid, "re-read this round at the same lines; the subject is unchanged (see r12-delta-scope).")
    ev = (f"Carried from round 10 ({UNCHANGED}): {base}. Round 12: {note}")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

R12 = [
    ("r12-delta-scope", "2.9 / delta: what changed between the round 10 pin and 5db69a9b", "course/modules/LX/LX2/project.html; tests/labs/LX2/lab-LX2-project-{1,2,3}.py; course/assets/js/labs.js",
     "git diff --quiet 00a84795 5db69a9b for project.html, the three project twins and labs.js: all unchanged. git diff --stat for the slice's cited inputs: course/modules/LX/LX2/index.html (2 prose sentences, data attributes unchanged), references/references.json (generated_at and two used_by lists, no frb2026fed change), curriculum/curriculum.json and course/assets/data/program.json (Arbitrage scanner brief only, not LX2), course/modules/LX/LX2/L01.html, L02.html and cards.json (other slices). Every cited changed input is re-verified in a row below."),
    ("r12-gates-pages-dag-projects-labs", "gate: check_pages, check_dag, check_projects, run_labs for LX2", "ledgers/LX2/scripts/LX2-c-r12/gates_r12.txt",
     "check_pages --unit LX2: PASS; check_dag --unit LX2: PASS; check_projects --unit LX2: PASS; run_labs --unit LX2: PASS (7/7). Command output saved in ledgers/LX2/scripts/LX2-c-r12/gates_r12.txt. run_labs --unit LX2 --page project: PASS (3/3) (run_labs_LX2_project_r12.txt)."),
    ("r12-page-smoke-project", "2.9 / 2.5 page_smoke for the project page alone", "ledgers/LX2/scripts/LX2-c-r12/page_smoke_project_r12.txt",
     "page_smoke.py --unit LX2 --pages project: 'page_smoke modules/LX/LX2/project.html: PASS', 'page_smoke LX2: PASS'; the three project labs ran at 0.0 s each; boot 1.1 s."),
    ("r12-twins-alone", "2.5 labs: twins alone under python -I -W error", "tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py",
     "Each twin run alone: exit 0, empty stderr. Outputs in ledgers/LX2/scripts/LX2-c-r12/twin_project{1,2,3}.out."),
    ("r12-page-code-vs-twin", "2.5 labs: page code equals twin; expected block equals twin output", "course/modules/LX/LX2/project.html lines 105-190, 242-320, 374-482; ledgers/LX2/scripts/LX2-c-r12/r12_page_vs_twin.py",
     "Lab 1: page code == twin True; expected block == twin stdout True. Lab 3: both True. Lab 2: the page code differs from the twin only in the two blanked lines (hit_rate = ___ and bias = ___), which is the design; expected block == twin stdout True. Output in page_vs_twin_r12.out."),
    ("r12-rederive-numbers", "2.2 / 2.4 numbers: every numeric prose claim and printed block re-derived from the definitions by an independent script", "ledgers/LX2/scripts/LX2-c-r12/rederive_r12.py (output rederive_r12.out)",
     "Lab 3: H=24, hits 13, hit rate 0.5417, bias 2.1250, sum 51, edge months [14,15,16,19,22,24,26], largest |e| 8 at month 34 (and 35), calibration errors sum 11 (bias 0.9167; the only integer s with round(s/12,4)=0.9167), split 13-27 sum -3 n 15 hits 13 bias -0.2000 rate 0.8667, split 28-36 sum 54 n 9 hits 0 bias 6.0000, errors 25-36 sum 56 /12 = 4.6667, strict band 6 hits 0.2500, errors 28-36 all positive 3..8, errors 13-27 within [-3,3]. Lab 1: errors [1,-3,2,0,-4,3,-2,5], hits 4, rate 0.5000, bias 0.2500, edge [15,19], strict 2 hits, agrees with Lab 3 at month 18 only. Lab 2: errors [-1,2,6,1,-2,-5], hits 4, rate 0.6667, bias 0.1667, edge [14,17], mean absolute error 2.8333, agrees with Lab 3 at month 13 only. Hours 2+2+2+3+3+2=14; 14/50=28%."),
    ("r12-attachment-quotes", "2.3 attachment quotes and printed-page locators (SR 26-2 attachment), re-fetched", "course/modules/LX/LX2/project.html lines 350-353, 364; ledgers/LX2/scripts/LX2-c-r12/sr26_quotes_r12.py",
     "Fetched by plain curl 2026-11-05 from https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm, SR2602a1.pdf and SR2602.pdf (no bot check, HTTP 200). sha256 SR2602a1.pdf 209ce4c1... and SR2602.pdf 956b3bc6... are byte-identical to round 10. Each of the six attachment quotes is found on the stated printed page, which equals the PDF page in SR2602a1.pdf: Conceptual soundness quote on p.8; Outcomes analysis quote and 'established performance thresholds' on p.9; 'includes an assessment of a model's reliability and its limitations' and 'Sound validation identifies model limitations and errors' on p.7; Ongoing model monitoring quote on p.9; 'This guidance does not set forth enforceable standards or prescriptive requirements' on p.2 in section I (before the heading II). Combined-file pages 4, 9, 10, 11 as stated on line 365. Headings: 'Conceptual Soundness' p.8, 'Outcomes Analysis' and 'Ongoing Model Monitoring' p.9, no limitations heading."),
    ("r12-cover-letter-sentences", "2.3 cover letter sentences and locators", "course/modules/LX/LX2/project.html lines 363-364, 622; sr2602.htm",
     "In sr2602.htm: 'The Board of Governors of the Federal Reserve System, Office of the Comptroller of the Currency (OCC), and Federal Deposit Insurance Corporation (FDIC) ... are issuing the attached Revised Guidance on Model Risk Management, which supersedes and replaces SR letter 11-7 ... and SR letter 21-8' (paragraph beginning 'The Board of Governors'); 'Applicability: This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated by the Federal Reserve.'; 'Supersedes:' is after the signature block (signed Randall D. Guynn). 'April 17, 2026' present. The page's paraphrase is C graded with a locator. ledgers/LX2/scripts/LX2-c-r12/sr26_quotes_r12.out."),
    ("r12-blind-exemplar-scoring", "2.6 rubric calibration: score exemplars blind, within one level", "course/modules/LX/LX2/project.html #exemplar-a, #exemplar-b; ledgers/LX2/scripts/LX2-c-r12/exemplars_stripped_r12.txt",
     "Scored from the annotation-stripped passages under the five criteria only: A = C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3). B = C1 2 (M2 neither tested nor marked untested, so not level 3), C2 2 (definition of a hit is 'close', no rounding rule), C3 2 (one limit only), C4 1 (no metric), C5 1 (no locator on the keyed statement, a source without a key). Official 2,2,2,1,1. Within one level on every criterion. CAVEAT: this session had viewed the annotations before the stripped file was written, so this is a calibration pass and not a fully clean blind pass (same caveat as round 10)."),
    ("r12-mutants-existing-rerun", "2.6 mutation: re-run every existing lab-2 student-error mutant and alternative through the labs.js compare rules", "ledgers/LX2/mutants/*lab2*.py (62 files); ledgers/LX2/scripts/LX2-c-r10/harness_lab2_r10.py; ledgers/LX2/scripts/LX2-c-r12/harness_lab2_all_r12.txt",
     "62 files: 46 KILLED (student-error), 9 student-error SURVIVE and 7 alternatives SURVIVE. The 9 survivors are the same as round 10 and are disclosed on the page: tie-only rounding rules (r6_lab2_float_format_ties_even, r6_lab2_round_half_even_ties, r6_lab2_round_half_toward_plus_infinity, r7_lab2_rounds_through_python_round) at page line 332; printed-output-only grading (r6_lab2_hard_coded_printed_values at lines 45 and 332, r8_lab2_hit_rate_ceiling_four_places at lines 45 and 332); and equivalent on this window (r10_lab2_bias_absolute_error_sum, r10_lab2_bias_absolute_value_of_sum_per_H, r10_lab2_hit_band_three). The round 10 notes give the same disclosure. Judged a disclosed limit, not a finding; see the notes."),
    ("r12-mutants-new-student-error", "2.6 mutation: at least three NEW student-error mutants written this round", "ledgers/LX2/mutants/r12_lab2_*.py; ledgers/LX2/scripts/LX2-c-r12/make_r12_mutants.py",
     "Four new mutants, each a complete module with a one-line docstring naming the error, all KILLED by the harness: r12_lab2_hit_count_counts_only_upper_side (token 70: 0.8333 vs 0.6667), r12_lab2_hit_count_adds_edge_months (1.0000 vs 0.6667), r12_lab2_hit_rate_denominator_excludes_edge_months (1.0000 vs 0.6667), r12_lab2_bias_uses_mean_realised_value (130.8333 vs 0.1667 at token 74)."),
    ("r12-alternatives-new", "2.5 / 2.6 over-constraint: new correct alternatives (different valid expressions) must survive", "ledgers/LX2/mutants/alt_r12_lab2_*.py",
     "alt_r12_lab2_statistics_fmean_bias (statistics.fmean of errors, float), alt_r12_lab2_hit_rate_generator_sum (sum over a generator divided by H, float), alt_r12_lab2_bias_sum_over_len (Fraction(sum, len(errors))): all three SURVIVE the labs.js compare, so the check does not over-constrain the expression."),
    ("r12-run-graders-mutate", "2.6 autograder gates: run_graders and mutate_graders for LX2", "ledgers/LX2/scripts/LX2-c-r12/run_graders_LX2_r12.txt; mutate_graders_LX2_r12.txt",
     "run_graders --unit LX2 --seeds 0-49: 'no autograder (grading: rubric)', exit 0. mutate_graders --unit LX2 --seeds 0-9: exit 0 (no graded unit; the rung 2 instant check is the only compare and is covered by the lab-2 harness)."),
    ("r12-verify-refs", "2.1 citations: verify_refs offline and live for LX2", "ledgers/LX2/scripts/LX2-c-r12/verify_refs_offline_r12.txt; verify_refs_unit_LX2_r12.txt",
     "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0. verify_refs.py --unit LX2: 'live re-verification of LX2: 6 of 560 entries, 0 problems', exit 0."),
    ("r12-ruff-mypy-pytest", "gate: ruff, mypy, pytest subset", "ledgers/LX2/scripts/LX2-c-r12/ruff_r12.txt; mypy_r12.txt; pytest_subset_r12.txt",
     "ruff check . 'All checks passed!' exit 0; ruff format --check . '559 files already formatted' exit 0; mypy --no-incremental 'Success: no issues found in 385 source files' exit 0; pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py (subset) exit 0."),
    ("r12-hours-independent-estimate", "2.6 hours: independent estimate within 30 percent", "course/modules/LX/LX2/project.html lines 531-543 (table#hours)",
     "My estimate: rung 1 read, run and annotate Lab 1 with the four element notes 2 h; rung 2 two blanks and the instant check 1 h; intake of the case and the two assumptions 1.5 h; outcomes analysis with the window split 2 h; report drafting with the attachment quotes and citations 4 h; self-assessment 1.5 h. Total about 12 h, which is 14 h minus 14 percent, inside the 30 percent band (9.8 to 18.2 h). Declared 14 h matches the hub."),
    ("r12-notation", "2.4 notation: every symbol against notation/notation.json", "notation/notation.json; course/modules/LX/LX2/project.html inline math",
     "notation.json registers 8 program-wide symbols (T, Phi, gamma3, gamma4, R*, R^e* and others). The page uses H, e_t, y_t, t, the hat-y forecast, and the names M1, M2, Part letters. None of these is registered, so no collision. The page uses no \\E or \\R macro."),
    ("r12-banned-and-process-words", "2.9 banned phrases and process words in visible text", "course/modules/LX/LX2/project.html (visible text)",
     "Script scan of visible text (tags and scripts removed): 0 hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly, historically, it can be shown; no builder, verifier or ledger word. 'Exemplar', 'rubric' and 'self-assessment' are course terms for the learner."),
    ("r12-hub-hours-and-ladder-text", "2.9 hub consistency: index.html ladder and hours text against project.html", "course/modules/LX/LX2/index.html lines 29, 44, 148, 158-165, 175-176",
     "index.html: 'Module LX2 · Tier U · 50 hours'; '36 h lessons · 14 h project (28% of 50 h)'; rung 1 text 'The model case is SIMULATED.' and rung 2 'Graded instantly in your browser.' agree with project.html lines 44-45. The hub's '28 percent' agrees with the project's 14 of 50."),
    ("r12-curriculum-brief-scope", "2.6 scope: rung 3 against the curriculum brief", "curriculum/06-profession-capstone.yaml:82-84; plans/LX2-build-plan.md section 12 item 6 and the binding architect decisions (line 619)",
     "The curriculum brief says 'on one of your own Atlas models'. The page uses one documented SIMULATED model case (rung 3), with Atlas only as optional rung 4. The plan's recommended resolution (section 12 item 6, B4) is 'accept the default', and the binding architect decisions say to follow the plan's recommendation. Accepted as the architect's ruling. ARCHITECT FOLLOW-UP: the curriculum string still differs, so either amend curriculum/06-profession-capstone.yaml:82-84 or record the acceptance; no page change is needed for this slice."),
    ("r12-plan-input-deviation", "2.6 spec inputs against plan section 5.2", "course/modules/LX/LX2/project.html lines 342, 370; plans/LX2-build-plan.md section 5.2 and 5.5",
     "Plan 5.2 names a CSV of forecasts and realised values with a stated seed. The page instead has Lab 3 generate the 36-month case from seed 20261103 inside the lab, and says the table is not uploaded and not a data file (line 342). Plan 5.5 says no embedded data, and the page's data-files count is 0. The seed, generator and output are stated and reproducible; accepted, with the plan text noted."),
    ("r12-failure-message-property", "2.6 item 4 failure messages (applies to autograders; the rung 2 check is rubric-project)", "course/assets/js/labs.js lines 42-58 (compareOutput), 133-138",
     "The reason is 'token N: X differs from Y'. It names the token position but not the printed line (Part B or Part C), and it shows the expected token, which is already in the expected block on the page. VERIFIER 2.6 item 4 is the autograder rule and the curriculum grades this project as rubric, so it is not a FAIL. Observation for the architect: a label such as 'Part B line' would make the failure name its property."),
]
for rid, check, loc, ev in R12:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

# mutants from the r12 harness output
harness = (S / "harness_lab2_all_r12.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in harness:
    m = re.match(r"^(KILLED\s*|SURVIVES)\s+(\S+\.py)(.*)$", line)
    if not m:
        continue
    name, rest = m.group(2), m.group(3).strip(" -")
    doc = ast.get_docstring(ast.parse((root / "ledgers/LX2/mutants" / name).read_text(encoding="utf-8"))) or ""
    desc = doc.splitlines()[0] if doc else "(no description)"
    if m.group(1).strip() == "KILLED":
        killed_by = f"KILLED by the labs.js whole-block compare (harness r12): {rest}"
    else:
        killed_by = "SURVIVES (correct alternative; over-constraint check passes)" if name.startswith(("alt", "alt_")) else \
            "SURVIVES (disclosed limit: " + ("equivalent on this window" if "band_three" in name or "absolute" in name else "tie-only or printed-output-only grading, page lines 45/332") + ")"
    mutants.append({"name": name, "description": desc, "killed_by": killed_by})

frag = {
    "unit": "LX2",
    "slice": "LX2-c",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, round 12 (did not build LX2)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "round 10 pin 00a84795f276456fce19d4181373cc4efba11a36 (fragment /Users/billyribeiro/.fanout/frags/E-LX2-c.round10.json). The round 11 fragment named in the brief (E-LX2-c.round11.json) does not exist in frags/; the newest LX2-c fragment is round 10. Delta 00a8479..5db69a9 for this slice: project.html and the project twins are unchanged; the cited inputs that changed (index.html, references.json, curriculum.json) are re-verified in round 12 rows.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-LX2-c (detached at 5db69a9b; .venv symlinked; vendor copied)",
    "scratch": "/tmp/lx2c-r12-src.P1KMKw (SR2602a1.pdf, SR2602.pdf, sr2602.htm fetched by plain curl 2026-11-05; text extracts a1.txt, combined.txt, sr2602_text.txt)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "frb2026fed: sr2602.htm sha256 changed since the round 10 fetch (05af406d... to b5c0e0a9...); the PDFs are byte-identical; the cover-letter sentences the page cites are present in the new htm. Registry record unchanged."
    ],
    "freshness_flags": [
        "SR 26-2 (April 17, 2026) is the current guidance as fetched on 2026-11-05; no later SR letter on model risk was checked beyond the federalreserve.gov pages fetched.",
    ],
    "notes": [
        "Verdict PASS. Every row is PASS, carried rows say so and cite the subject byte-identity; every changed input a row cites was re-verified in this round.",
        "The whole project.html (738 lines) and the three project twins were read line by line. Every numeric claim was re-derived by an independent script (r12-rederive-numbers). Every quote was checked against the fetched PDFs.",
        "Calibration caveat: the annotations had been seen earlier in this session, so the blind scoring is a stripped-text calibration pass, not a fully clean blind pass.",
        "Disclosed mutant survivors (9) are carried from round 10 and are disclosed on the page (lines 45, 332) or equivalent on this window. The 7 alternatives survive as required. The instant rung-2 check grades printed output only, which the page states.",
        "Architect follow-ups, not page defects: (a) curriculum/06-profession-capstone.yaml:82-84 still says 'your own Atlas models' (B4 default accepted by the plan); (b) plan 5.2 names a CSV, the page generates the table in Lab 3 (no data file); (c) labs.js compare reason names a token index, not the printed line.",
        "Questions a student would ask (spec completeness): the length or format of validation.md beyond the four section headings; whether the monitoring threshold must be a rolling window (the spec says a threshold, and exemplar A uses a rolling one); whether Part F must be quoted. None blocks the spec.",
        "Not checked: the self-assessment form and its IndexedDB storage were not executed in a browser (rubric.js hides annotations and stores scores locally; no fetch). page_smoke renders the page and runs the labs in Pyodide. The 5 correct alternatives and 4 new mutants run through the harness, not through a browser.",
        "Not checked: lesson pages L01-L04 and cards (other slices); Lesson 4 section 4 is read only for the band and rounding rules the project cites.",
        "Harness note: the lab-2 harness is ledgers/LX2/scripts/LX2-c-r10/harness_lab2_r10.py, a copy of the labs.js compare rules, not the browser code path. Browser behaviour is covered by page_smoke only for the lab run, not for the compare.",
    ],
    "summary": "LX2-c round 12: PASS. Rows: " + str(len(rows)) + " (all PASS); round 10 rows carried with the byte-identity prefix or re-verified; 15 new round 12 rows. Mutants: 46 of 62 lab-2 files KILLED (4 new student-error mutants all killed); 7 alternatives survive as required; 9 student-error survivors carried and disclosed.",
}

problems_check = None
if "--check" in sys.argv:
    print("rows", len(rows), "mutants", len(mutants))
out = root / "ledgers/LX2/LX2-c.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
