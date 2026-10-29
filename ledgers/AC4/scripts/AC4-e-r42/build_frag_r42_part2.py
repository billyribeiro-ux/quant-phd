NOTES = 'Delta b2082cc..e205053 for AC4-e: course/modules/AC/AC4/project.html line 346 (exemplar A level 3 annotation now names the efficiency miss only) and ledger/script files only. Re-verified from scratch this round: the line-346 fix (proj-r40-exemplar-A-C2-level3-annotation and proj-calib-A-annotation now PASS); all rows that cite the exemplar block, the whole page, the mutants or command outputs. Carried from round 41 (148 rows): rows whose cited lines or files are byte-identical since b2082cc (grader/, cards.json, tests/labs/AC4, references, index.html, lesson pages, tools; project.html lines not including 346). Still FAIL: proj-mutant-descriptions and proj-r40-fx23-subdir-mutants (six subdirectory mutants with the reference header as docstring; killed, but the description does not name a student error; files byte-identical to b2082cc). New mutants: r42e_02..r42e_05 (killed on seed 0, all 165 top-level files re-run: 165/165 killed); r42e_01 was equivalent and was removed. Alternatives alt42_a..c pass seeds 0-49. Scope notes: tests/test_memo_exemplars.py is an S7-only test, so the earlier AC4 evidence that cited it as memo coverage is a scope error; the AC4 exemplar annotations are checked by annot_check.py. The bare pytest --collect-only of the grader fails with ModuleNotFoundError budget_engine (as in earlier rounds); the workspace collection gives 563 on seeds 0-49. Not checked: a browser run of the self-assessment form (page_smoke only); the full repository pytest suite; tools/build_site.py was run only for its --check mode; SEC/EDGAR sources (outside this slice). Round labels: the brief says round 42, the previous fragment file is named round41 (its round field reads 40); carry prefix uses round 41.'
import re
exec(open("/tmp/verify42-AC4-e/ledgers/AC4/scripts/AC4-e-r42/build_frag_r42.py").read())

MUT_OUT = O + "mutate_ac4_165.out"
SUB_OUT = O + "subdir_fx23_mutants.out"
FAIL_IDS = {"proj-mutant-descriptions", "proj-r40-fx23-subdir-mutants"}
CARRY_ONLY_MUT = {"proj-r12-mutant-m60-scope", "proj-r30-mutant-equivalent-r30e01", "proj-r38-equivalent-total-sum-of-parts"}
MUT_RERUN_EV = ("Re-run round 42: tools/mutate_graders.py --unit AC4 --seeds 0-49 over all 165 top-level files of ledgers/AC4/mutants/ "
                "(the four new r42e files included): 'mutate_graders AC4: PASS (165/165 killed)', exit 0 (out/mutate_ac4_165.out). "
                "The six AC4-e-r23 subdirectory files were run separately: all KILLED on seed 0 (out/subdir_fx23_mutants.out).")

rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in FAIL_IDS:
        status = "FAIL"
        ev = {
            "proj-mutant-descriptions": "Still defective (ledgers/AC4/mutants/AC4-e-r23/fx23_01..fx23_06, unchanged since b2082cc). Each file's first docstring line is 'Reference solution for the AC4 budget and variance engine (budget_engine.py).' (out/subdir_fx23_mutants.out lists it for each). The file is therefore not a student-error description. All six are KILLED on seed 0 (out/subdir_fx23_mutants.out), so the grader catches them; the defect is only the ledger description.",
            "proj-r40-fx23-subdir-mutants": "Still defective, re-verified: the six AC4-e-r23 subdirectory mutants carry the reference header as their docstring and name no student error; all six KILLED on seed 0 (out/subdir_fx23_mutants.out, run_mutants_files.py).",
        }[i]
        fix = "Rewrite the first docstring line of each of ledgers/AC4/mutants/AC4-e-r23/fx23_01..fx23_06 so that it names the student error the file makes (for example 'Student error: the mix variance uses the exact flexed profit.'), or move the six files out of the mutant ledger; the grader is not changed."
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "FAIL", "evidence": ev, "fix": fix})
        continue
    if i in OV:
        st, ev = OV[i]
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
        continue
    if "mutant" in r["location"].lower() and i not in CARRY_ONLY_MUT:
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": MUT_RERUN_EV})
        continue
    # carry: the cited files are byte-identical to the previous pin (checked with git diff below)
    rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": CARRY + r["evidence"]})

NEW = []
def new(i, check, location, status, evidence):
    NEW.append({"id": i, "check": check, "location": location, "status": status, "evidence": evidence})

new("proj-r42-delta-scope", "The round-42 delta (b2082cc..e205053) touches only project.html line 346 among the slice's pages, plus ledger and script files",
    "git diff --name-status b2082cc e205053; git diff --quiet b2082cc e205053 -- course/modules/AC/AC4/grader course/modules/AC/AC4/cards.json tests/labs/AC4 references course/modules/AC/AC4/index.html course/modules/AC/AC4/L0*.html tools", "PASS",
    "git diff --name-status shows M course/modules/AC/AC4/project.html (one hunk, one line: 346), and A ledgers/AC4/mutants/r40e_01..04 and A ledgers/AC4/scripts/AC4-e-r40/* (the round-40 verifier's own files). The byte-identity command over grader/, cards.json, tests/labs/AC4, references, index.html, L0x.html and tools exits 0, so those rows are carried. The previous fragment is round 41 (file /tmp/fanout-frags/AC4-e.round41.json; its round field reads 40 and its pin b2082cc).")
new("proj-r42-line346-rewrite-hunt", "Hunt for new errors in the rewritten C2 level 3 sentence (project.html line 346)",
    "course/modules/AC/AC4/project.html line 346 against lines 308, 315, 326, 334-336, 345", "PASS",
    "Sentence: 'Misses C2 level 3: the efficiency variance is not tied to a case figure. The volume, price and mix variances are tied, so the memo scores level 2.' Checks: (a) 'tied to a case figure' is the page's defined term (line 308); (b) the efficiency paragraph is absent from exemplar A's Causes (lines 333-337), so 'not tied' is exact; (c) volume (1,500 and 1,400, line 334), price (5,000 and 9,000, line 335) and mix (+462,857, line 336) each meet the definition; (d) 'scores level 2' agrees with data-scores 2 for C2 (line 326) and the C2 level 2 meets (line 345); (e) no banned, scope or process word (scan of line 346); (f) no causal or magnitude claim beyond the case figures; (g) the descriptor it answers (line 315, level 3: each of the four variances tied) is the only condition the sentence names.")
new("proj-r42-exemplar-annotations-vs-scores", "Every exemplar annotation agrees with its per-criterion score (AC4 exemplars A and B)",
    "course/modules/AC/AC4/project.html lines 326-386 (data-scores, data-level, annotation li elements); ledgers/AC4/scripts/AC4-e-r42/annot_check.py", "PASS",
    "annot_check.py (run via the checkout's Python 3.14 with the tools/coursekit loader; out/annot_check.out): exemplar-a data-scores 2,2,2,1,2, data-level 1 (the lowest criterion score, which is the overall-level rule of line 308); exemplar-b 4,4,3,4,4, data-level 3. For each criterion the highest 'meets' level equals the score and no 'misses' level is at or below it: all 10 criterion checks OK.")
new("proj-r42-exemplar-A-arithmetic", "Every figure in exemplar A's memo and annotation recomputes from the case",
    "course/modules/AC/AC4/project.html lines 331-340 and 343-351 (exemplar A)", "PASS",
    "Recomputed in this round: total 220,000 = 2,820,000 - 2,600,000 (actual profit: 1200x5200 + 300x8800 - 5300x200 - 5,000,000 = 2,820,000); volume 542,857 = 3,142,857 - 2,600,000; price 180,000 = 1200x200 - 300x200; efficiency -40,000 = 200x(5,100-5,300); mix shift 462,857 in magnitude; Standard 1000/1400 = 71.4% and 1200/1500 = 80.0%; 1,500 and 1,400 units. Body words: 318 by whitespace count of the memo-text paragraphs (headings removed), inside 300-600. The sign of the mix (+462,857 on the page versus -462,857 in Lab 1) is the excepted, annotated error.")
new("proj-r42-exemplar-B-arithmetic", "Every figure in exemplar B's memo recomputes, and the 5,400 threshold reverses the mix recommendation as stated",
    "course/modules/AC/AC4/project.html lines 362-373 (exemplar B) and 377-382", "PASS",
    "Recomputed: profit 2,820,000 and total +220,000; volume +542,857; 3,142,857 flexed; mix -462,857; Standard margin 5000-3x200 = 4,400 and Deluxe 9000-5x200 = 8,000; shares 71.4%, 80.0%, 28.6%, 20.0%; price +240,000 (1200 x 200) and -60,000 (300 x -200); efficiency 40,000 = 200 x 200 with standard 5,100. Threshold: Deluxe budgeted margin at price p is p - 1,000; equal to Standard's 4,400 at p = 5,400, so the mix variance is zero there and turns favourable below it (Deluxe earns less than Standard). The input-price what-if: 5,300 x 10 = 53,000 and 220,000 - 53,000 = 167,000. Body words 409, inside 300-600.")
new("proj-r42-memo-test-coverage", "No repository test checks the AC4 exemplar annotations or scores (scope of the memo evidence)",
    "tests/test_memo_exemplars.py (module docstring lines 1-3 and PROJECT = S7/project.html); tests/test_page_checks.py; tools/check_projects.py lines 59-71", "PASS",
    "tests/test_memo_exemplars.py is written for the S7 integrity project (its docstring: 'The integrity memo (course/modules/S/S7/project.html, rung 3)'); its exemplar assertions read S7's page. The 55 passing tests of that file and tests/test_page_checks.py (out/pytest_memo_page_checks.out) therefore do not exercise the AC4 memo. The AC4 page makes no claim that a test checks its annotations, so this is a scope note on earlier round evidence, not a page defect. The structural check tools/check_projects.py (levels 1-4, data-level present, exemplars at two or more levels) passes for AC4 (out/check_projects.out). The annotation/score agreement for AC4 is checked by ledgers/AC4/scripts/AC4-e-r42/annot_check.py (proj-r42-exemplar-annotations-vs-scores).")
new("proj-r42-mutants-new-student-errors", "Four new student-error grader mutants (r42e_02..r42e_05) are killed, and each names a student error",
    "ledgers/AC4/mutants/r42e_02_master_budget_key_named_without_cents.py; r42e_03_flexed_variable_cost_is_actual_input_cost.py; r42e_04_standard_inputs_summed_over_products_times_total.py; r42e_05_favourable_efficiency_refused.py; generator ledgers/AC4/scripts/AC4-e-r42/make_r42e.py", "PASS",
    "Each file is the reference solution with one student error applied (single replacement asserted in make_r42e.py) and a docstring that begins 'Student error:'. Killed on seed 0 (out/mutate_ac4_165.out): r42e_02 (key total_revenue instead of total_revenue_cents) by test_master_totals_and_profit; r42e_03 (flexed variable cost = input price x actual inputs) and r42e_04 (standard inputs summed over products times total units) by test_every_grader_seed_reconciles_exactly[30]; r42e_05 (favourable efficiency refused) by test_every_grader_seed_reconciles_exactly[15]. The page requires the efficiency variance in both directions (line 265). Four of four killed; r42e_01 was rejected as equivalent (next row).")
new("proj-r42-mutant-equivalent-total-r42e01", "The mutant that sets the total variance to the sum of the four variances is equivalent, so it is excluded from the mutant list",
    "ledgers/AC4/scripts/AC4-e-r42/make_r42e.py (MUTANTS entry r42e_01, first run, file since removed); compare ledgers/AC4/scripts/AC4-e-r30/equivalent/r30e_01_total_is_sum_of_the_four_variances.py and AC4-e-r38/equivalent/r38e_02", "PASS",
    "The mutant survived the first run (out/new_r42e_mutants.out, SURVIVED r42e_01). It is equivalent, by the identity the page states (line 257-259: the four variances sum to the total exactly). Proof: with price = sum AU(ap-bp), volume = flexed - master, mix = sum AU(bp - q s) - F - flexed, eff = s(sum q AU - AQ): price + volume + mix + eff = sum AU ap - s AQ - F - master = total, identically in the case values, because the flexed term cancels. So on every case where the four variances are right, the mutant returns the same total, and where a variance is wrong the variance test kills the mutant. The file was removed from ledgers/AC4/mutants/ and is not counted. Same mutant as the earlier equivalents r30e_01 and r38e_02.")
new("proj-r42-alternatives-correct", "Three new correct alternative implementations (written from the page specification, not from the reference) pass the whole suite on seeds 0-49",
    "ledgers/AC4/scripts/AC4-e-r42/alts/alt42_a_floor_half_and_operator_index.py; alt42_b_numbers_integral_and_pipeline.py; alt42_c_strict_type_decimal.py; run by ledgers/AC4/scripts/AC4-e-r42/run_alts.py", "PASS",
    "alt42_a rounds by math.floor(q + 1/2) and validates with operator.index plus a bool refusal; alt42_b validates with numbers.Integral and uses a single named pipeline; alt42_c uses strict type(x) is int checks and Decimal ROUND_HALF_UP quantize, and refuses a tuple of products. Each passes the suite on seeds 0-49 (out/alts42.out: 'PASSES ... on seeds 0-49' for all three). The runner uses the same run_suite as the grader and reports a FAILS line for any failure, as the mutant runs show.")
new("proj-r42-lab-expected-match", "The two Lab twins' output equals the embedded expected output on the page",
    "course/modules/AC/AC4/project.html lines 137-145 and 233-241 (pre class=expected); tests/labs/AC4/lab-AC4-project-1.py and lab-AC4-project-2.py via python -I -W error", "PASS",
    "Run in this round: both twins exit 0 with the 9 output lines (out/twin_project1.out, out/twin_project2.out). diff of the page's expected block against the twin output (sed line ranges): the 9 lines are identical in content for both labs; the only difference is the <pre> wrapper on the first and last lines of the page block.")
new("proj-r42-gates-rerun", "Every command gate for this slice re-run at e205053",
    "ledgers/AC4/scripts/AC4-e-r42/run_cmds.sh and the separate commands listed in the evidence", "PASS",
    "check_pages --all, check_dag --all, check_projects --all: exit 0. run_labs --unit AC4: 10/10, exit 0. page_smoke --unit AC4 --pages project.html: PASS, exit 0. ruff check: passed; ruff format --check: 220 files formatted; mypy --no-incremental: 153 files, no issues; both twins exit 0; run_graders --unit AC4 --seeds 0-49: reference 50/50, exit 0; mutate_graders --unit AC4 --seeds 0-49: 165/165 killed, exit 0 (the bare run in run_cmds.sh was 161/161 before the four r42 files were added; the 165 run is the full re-run); tools/build_site.py --check: 6 outputs current, exit 0; tools/verify_refs.py --offline: 560 entries 0 problems; --unit AC4 live: 2 of 560 entries 0 problems; pytest tests/test_memo_exemplars.py tests/test_page_checks.py: 55 passed (scope note in proj-r42-memo-test-coverage). Not run: the full repository pytest suite (outside the slice).")
new("proj-r42-hours-split", "The hours of the time-budget table and the hub split agree",
    "course/modules/AC/AC4/project.html lines 277-285; course/modules/AC/AC4/index.html lines 29, 31, 39", "PASS",
    "The table sums to 20 (1, 2, 2, 6, 4, 2, 2, 1) and its Total row reads 20; the page header data-hours-project is 20; index.html declares data-hours-lessons=50 and data-hours-project=20, 50 + 20 = 70, which matches the module's 70 hours in the description and eyebrow. No arithmetic inconsistency. Design-target pace not judged (architect ruling).")
new("proj-r42-banned-process-whole-file", "Whole-file scan of the page and cards for banned phrases, placeholders and process words",
    "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json", "PASS",
    "grep counts zero for: roughly half, About 6%, historically, TODO, TBD, lorem, left as an exercise, It can be shown that, ellipsis character, three dots, builder, verifier, 'round N', REQUESTS, unit report, statistically significant (both files). The changed line 346 contains no scope word from the list in the brief (only, all, always, same, drives, offsets, raises, as much as).")
new("proj-r42-subdir-fx23-killed", "The six AC4-e-r23 subdirectory mutants are KILLED by the grader (the defect is the description only)",
    "ledgers/AC4/mutants/AC4-e-r23/fx23_01..fx23_06", "PASS",
    "run_mutants_files.py on the six files: KILLED on seed 0 each (out/subdir_fx23_mutants.out). The FAIL row proj-mutant-descriptions covers their docstrings.")

all_rows = rows + NEW
ids = [r["id"] for r in all_rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert all(r["id"] in ids for r in prev["rows"]), "a previous id dropped"

import sys
sys.path.insert(0, "/tmp/verify42-AC4-e/tools")
import importlib
mut = []
for line in open(MUT_OUT, encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line.rstrip("\n"))
    if m:
        name, desc, killed = m.group(2), m.group(3), m.group(4)
        mut.append({"file": "ledgers/AC4/mutants/" + name, "description": desc,
                    "killed_by": (killed + " [KILLED]") if m.group(1) == "KILLED" else "SURVIVED"})
for line in open(SUB_OUT, encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line.rstrip("\n"))
    if m:
        name, desc, killed = m.group(2), m.group(3), m.group(4)
        mut.append({"file": "ledgers/AC4/mutants/AC4-e-r23/" + name, "description": desc,
                    "killed_by": (killed + " [KILLED]") if m.group(1) == "KILLED" else "SURVIVED"})
surv = [m for m in mut if m["killed_by"] == "SURVIVED"]
print("mutants", len(mut), "survived", len(surv))

from collections import Counter
counts = Counter(r["status"] for r in all_rows)
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 42,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 42, slice AC4-e; did not build AC4)",
    "pin": "e205053",
    "base": "b2082cc (the previous fragment is /tmp/fanout-frags/AC4-e.round41.json, pinned at b2082cc; its own round field reads 40, but the file is the round-41 fragment named in the brief, so 'Carried from round 41' is used)",
    "checkout": "/tmp/verify42-AC4-e",
    "scratch": "/tmp/ac4-v/AC4-e",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": all_rows,
    "mutants": mut,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": {"rows": len(all_rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
                "mutants": len(mut), "mutants_killed": sum(1 for m in mut if m["killed_by"] != "SURVIVED"), "mutants_survived": len(surv)},
}
frag["notes"] = NOTES
json.dump(frag, open("/tmp/verify42-AC4-e/ledgers/AC4/AC4-e.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("summary", frag["summary"])
