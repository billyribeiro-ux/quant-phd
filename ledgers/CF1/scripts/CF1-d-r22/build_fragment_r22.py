"""Build the round-22 CF1 slice-d fragment from the round-21 fragment: carry, re-verify, and add new rows."""
import json, re, subprocess

CHK = "/tmp/verify22-CF1-d"
OUT = "ledgers/CF1/scripts/CF1-d-r22/out/"
prev = json.load(open("/tmp/fanout-frags/CF1-d.round21.json"))
PREFIX = ("Carried from round 21 (cited files byte-identical since the previous pin f95243f; the only changed CF1 files "
          "in this delta are course/modules/CF/CF1/L06.html line 106 and the cards.json entry CF1-c084):")

FRESH = {
 "lesson-l06-remark-2-4-each-result-conditional": "Round 22 re-verified from scratch. L06.html line 106 now reads 'label the tail probability in E1 and the band in E2 as conditional on that reading; the cents error and the count of standard errors in E1 are not.' E1 solution (line 313): error 84543.40 - 79078.68 = 5464.72 cents (recomputed exact), 5464.72/4400.22 = 1.2419197 (recomputed; prints +1.242 in Lab 1 output, tests/labs/CF1/lab-CF1-L06-1.py run: line 'n 100 mean_npv_cents 84543.40 se_cents 4400.22 error_in_se +1.242'). Tail 2(1-Phi(1.2419)) = 0.214273 (0.2143, recomputed in ledgers/CF1/scripts/CF1-d-r22/out/recompute_e1e2.out) and labelled 'under that reading'. E2 solution (line 320): band 0.0552 +/- 1.96*0.0010 = 0.05324 to 0.05716 (recomputed), labelled 'the 1.96 multiplier is the normal reading of Remark 2.4, which this lesson does not test'. The grep of 'normal' and '1.96' in L06.html finds the normal reading only at lines 105-106, 313, 320: no third exercise applies it. The scope is now exact; FAIL resolved.",
 "cards-changed-c071-c084": "Round 22: cards.json CF1-c084 back text re-read against L06.html line 106 (the same sentence set: 'The tail probability in E1 and the band in E2 are conditional on that reading; the cents error and the count of standard errors in E1 are not.') and E1/E2 solutions (lines 313, 320). Card grade C, basis 'Remark 2.4', cite glasserman2003monte (present in references/references.json, used_by M8 only: flag kept in registry_flags). CF1-c071 unchanged (git diff f95243f d160ac3 touches only CF1-c084 in cards.json).",
 "cards-changed-c071-lesson-agreement": "Round 22: cards.json entries c065, c071, c085 byte-identical to the round-21 pin (git diff shows only the CF1-c084 hunk); CF1-c084 back re-read against L06.html line 106 and E1/E2 solutions (lines 313, 320): agrees (see lesson-l06-remark-2-4-each-result-conditional).",
 "cards-cite-keys-and-locators": "Round 22: every cite key in cards.json is in references/references.json entries (script ledgers/CF1/scripts/CF1-d-r22/out/registry_keys_r22.out: 'cite keys not in registry: []'); CF1-c084 cites glasserman2003monte with grade C and locator 'Registry record title; passage locator not confirmed' (L06.html line 106), consistent.",
 "cards-missing-grade-or-basis": "Round 22 scan (ledgers/CF1/scripts/CF1-d-r22/cards_scan_r22.py, out/cards_scan_r22.out): 109 entries, grades 59 T and 50 C, 'missing grade or basis []', every entry has a cite or a basis ('no cite and no basis: []').",
 "cards-duplicate-scan": "Round 22 scan (out/cards_scan_r22.out): duplicate ids [], duplicate fronts [], duplicate backs [] over all 109 entries, including the rewritten CF1-c084.",
 "cards-numbers-in-lesson": "Round 22: the numbers in the rewritten CF1-c084 back (1, 2, 2003, 2.4) appear in L06.html (scan output 'number ... in L06: True'). The other entries are byte-identical to the round-21 pin.",
 "cards-grade-semantics": "Round 22: 109 entries, 59 T and 50 C (out/cards_scan_r22.out). CF1-c084 is C with basis 'Remark 2.4', a statement that the normal reading is not proved and that no result from the registered text is stated; C is the grade for a reading convention, consistent with the rule in the previous round.",
 "cards-count-vs-plan": "Round 22: 109 entries (out/cards_scan_r22.out). Per lesson: L01 18, L02 18, L03 17, L04 23, L05 18, L06 15; every lesson has at least one card (plans/CF1-build-plan.md section 12 requires at least one per lesson and the rule of BUILDER_RULES section 7, which the count does not contradict).",
 "cards-misconception-locator": "Round 22: whole-file scan of cards.json (out/cards_scan_r22.out) shows no entry without a basis or cite; the only changed entry (CF1-c084) has basis 'Remark 2.4' (L06.html line 103-106 block). The other entries are byte-identical to the round-21 pin.",
 "r15-banned-phrase-scan": "Round 22 scan of cards.json front and back for 'roughly', 'about ', 'historically', 'typically', ellipsis: the three 'about ' hits (CF1-c030 'carries no information about the decision', CF1-c072 'says nothing about what', CF1-c109 'assume about the flows') are ordinary usage, not the banned figure phrase. No hit in CF1-c084.",
 "r16-banned-process-words-scan": "Round 22 scan of cards.json and project.html for 'round', 'verifier', 'builder', 'unit report', 'REQUEST' (scan script ledgers/CF1/scripts/CF1-d-r22/cards_scan_r22.py): no hit in cards.json; project.html unchanged since the round-21 pin.",
 "r15-cards-numbers-and-grades": "Round 22 (current state, supersedes the round-15 count): cards.json has 109 entries, 59 T and 50 C (out/cards_scan_r22.out). The round-15 figure 103 (74 T, 29 C) was the state at that round and is no longer current.",
 "cards-count-r19": "Round 22: cards.json has 109 entries, 59 T and 50 C (out/cards_scan_r22.out); the round-19 figure (77 T, 32 C) is superseded by the round-21 change to 18 definition cards graded C and the round-22 rewrite of CF1-c084 (grade unchanged).",
 "proj-banned-phrases": "Round 22: project.html byte-identical to the round-21 pin (git diff f95243f d160ac3 empty for that file). Its one 'about' is the spec length 'of about 600 to 900 words' (line 188), a range not a figure claim. cards.json scan: no banned phrase (out/cards_scan_r22.out).",
 "proj-structure-and-gates": "Round 22 re-run: tools/check_projects.py --all: 'check_projects CF1: PASS' (out/check_projects.out); tools/check_dag.py --all: 'check_dag CF1: PASS' (out/check_dag.out); tools/check_pages.py --unit CF1: 'check_pages CF1: PASS' (out/check_pages.out). Exit codes 0.",
 "proj-pytest-lab-helper": "Round 22: 'pytest -q tests/test_labs.py -k CF1' gave 9 dots, 100% (out/pytest_labs.out); twins run with python -I -W error exit 0 with empty stderr (out/twins_I_W_error.out).",
 "proj-page-smoke": "Round 22 re-run: tools/page_smoke.py --unit CF1 (out/page_smoke.out): project.html PASS (in-browser grader 'All 157 tests pass on seed 1407000004'), L06.html PASS, index/concepts/review PASS, 'page_smoke CF1: PASS'.",
 "proj-verify-refs": "Round 22: tools/verify_refs.py --unit CF1 (out/verify_refs_live.out): 'live re-verification of CF1: 2 of 560 entries, 0 problems', exit 0; --offline (out/verify_refs_offline.out): 'offline integrity: 560 entries, 0 problems'.",
 "proj-check-dag": "Round 22: tools/check_dag.py --all (out/check_dag.out): all units PASS, CF1 PASS, exit 0.",
 "proj-ruff-format": "Round 22: ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1 (out/ruff.out): 'All checks passed!', '13 files already formatted'; full 'ruff check .' also 'All checks passed!' (out/ruff.out).",
 "proj-mypy-grader-gate": "Round 22: mypy --no-incremental on the CF1 grader (out/mypy.out): 'Success: no issues found in 4 source files'; full repository mypy: 'Success: no issues found in 153 source files' (out/mypy_full.out).",
 "proj-collect-count-50-seeds": "Round 22: collect-only of test_project.py against a copy of reference.py (scripts/CF1-d-r22/collect_seeds.sh, out/collect_r22.out): 157 tests on seeds 0-9 and 1407000004. Seeds 0-49 were not all re-collected this round; the count is seed-independent across the 11 seeds sampled, and project.html line 192 states 157.",
 "proj-mutants-killed": "Round 22 full run: tools/mutate_graders.py --unit CF1 --seeds 0-9 (out/mutate_r22_full.out): 208 of 208 killed (204 previous plus the four new r22d_01..r22d_04), 'mutate_graders CF1: PASS (208/208 killed)'.",
 "proj-alternatives-correct": "Round 22 full run: scripts/CF1-d-r22/run_alts22.py over every alternative file of rounds 7-22 (65 files, 46 unique by content), seeds 0-9 (out/alts_r22.out): all 46 'PASS (10 seeds)', including the reference copy alt ref_reference.py.",
 "proj-alternatives-rerun-all-prior-r18": "Round 22 full run (out/alts_r22.out): all previous alternative engines, rounds 7-21, pass seeds 0-9 with the current suite.",
 "proj-alternatives-rerun-all-r19": "Round 22 full run (out/alts_r22.out): all 46 unique alternatives pass seeds 0-9.",
 "proj-collect-154-r19": "Round 22: the collected count is 157 on seeds 0-9 and 1407000004 (out/collect_r22.out); project.html line 192 states 157, which matches. The round-19 figure 154 is historical and superseded.",
 "proj-page-smoke-r19": "Round 22 re-run: tools/page_smoke.py --unit CF1 PASS for project.html (out/page_smoke.out).",
 "proj-gates-ruff-mypy-r19": "Round 22 re-run: ruff and mypy on the CF1 grader and labs PASS (out/ruff.out, out/mypy.out).",
 "proj-hours-table": "Round 22 re-read project.html lines 216-230: the time-budget cells are 1, 1, 4, 2, 1, 1, 2, summing to 12, equal to data-hours-project=12 (line 33) and the hub split 48+12 (index.html line 29; out in the proj-hours-arithmetic-split row). Hours are design targets (architect ruling), not re-estimated.",
 "proj-hours-arithmetic-split": "Round 22: index.html line 29 data-hours-lessons=48, data-hours-project=12; the six L01-L06 pages carry data-hours=8 (grep: L01, L02, L03, L04, L05, L06 each 8): 6x8=48; 48+12=60; 12/60=20.0%, 48/60=80.0% (index.html line 41 and the hours-split style widths). No arithmetic inconsistency.",
 "r20-hub-hours-arithmetic": "Round 22 re-run of the hub arithmetic: 48 lesson hours (six data-hours=8), 12 project hours (time-budget cells sum to 12), 60 module hours (index.html line 31 header says 60 hours), 20.0%. No inconsistency.",
 "cmd-check-gates-r19": "Round 22 re-run: check_projects, check_dag and check_pages all PASS (out/check_projects.out, out/check_dag.out, out/check_pages.out).",
 "cmd-verify-refs-r19": "Round 22 re-run: verify_refs --unit CF1 live '2 of 560 entries, 0 problems'; --offline '560 entries, 0 problems' (out/verify_refs_live.out, out/verify_refs_offline.out).",
 "cmd-run-labs-r19": "Round 22 re-run: tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)' (out/run_labs.out), exit 0.",
 "cmd-run-graders-r19": "Round 22 re-run: tools/run_graders.py --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (out/run_graders.out), exit 0.",
 "cmd-mutate-graders-r19": "Round 22 re-run (out/mutate_r22_full.out): 208/208 killed.",
 "cmd-mutate-graders-r18": "Round 22 re-run (out/mutate_r22_full.out): 208/208 killed.",
 "cmd-gates-r18": "Round 22 re-run of the checkers and the lab gate (out/check_projects.out, out/check_dag.out, out/check_pages.out, out/run_labs.out, out/run_graders.out): all PASS, exit 0.",
 "cmd-verify-refs-live-r17": "Round 22 re-run: 'live re-verification of CF1: 2 of 560 entries, 0 problems' (out/verify_refs_live.out).",
 "cmd-mutate-graders-r17": "Round 22 re-run (out/mutate_r22_full.out): 208/208 killed.",
 "r20-collect-157-seeds": "Round 22 re-run (out/collect_r22.out): 157 on each of seeds 0-9 and 1407000004.",
 "r20-mutants-full-run": "Round 22 full run (out/mutate_r22_full.out): 208 of 208 killed.",
 "r20-alternatives-all-unique": "Round 22 full run (out/alts_r22.out): 65 files, 46 unique, all PASS on seeds 0-9.",
 "r20-registry-and-verify": "Round 22 re-run: verify_refs live and offline (out/verify_refs_live.out, out/verify_refs_offline.out): 0 problems.",
 "r20-labs-pytest-and-twins": "Round 22 re-run: pytest tests/test_labs.py -k CF1 (out/pytest_labs.out) and twins under python -I -W error (out/twins_I_W_error.out): all pass.",
 "r20-gate-set": "Round 22 re-run of the gate set: check_pages, check_dag, check_projects, run_graders, run_labs, page_smoke, ruff, mypy, verify_refs: all PASS (out directory ledgers/CF1/scripts/CF1-d-r22/out/).",
 "r16-run-gates": "Round 22 re-run of tools/check_projects.py, check_pages.py, check_dag.py, run_labs.py, run_graders.py: PASS (out/).",
 "r13-run-graders-50": "Round 22 re-run: run_graders CF1 50/50 seeds PASS (out/run_graders.out).",
 "r13-twins-under-python-I-W-error": "Round 22 re-run: all nine twins under python -I -W error exit 0 with empty stderr (out/twins_I_W_error.out).",
 "r13-mutants-full-run": "Round 22 full run: 208 of 208 killed (out/mutate_r22_full.out).",
 "r16-mutants-full-run": "Round 22 full run: 208 of 208 killed (out/mutate_r22_full.out).",
 "r13-prior-alternatives-rerun": "Round 22 full run: all prior alternatives (out/alts_r22.out) pass seeds 0-9.",
 "r15-alternatives-rerun-all-prior": "Round 22 full run: all prior alternatives (out/alts_r22.out) pass seeds 0-9.",
 "r16-alternatives-rerun-all-prior": "Round 22 full run: all prior alternatives (out/alts_r22.out) pass seeds 0-9.",
 "r21-delta-coverage": "Round 22 delta: git diff --stat f95243f d160ac3 (160 files). Slice files: course/modules/CF/CF1/project.html, grader/*, tests/labs/CF1/*, cards.json. Changed in slice: cards.json, CF1-c084 only (one line). project.html, grader/*, tests/labs/CF1/* and references/references.json: git diff empty (byte-identical). The L06.html line 106 change is outside this slice but is cited by CF1-c084 and re-verified.",
 "r21-project-meta-line7": "Round 22: project.html byte-identical to the round-21 pin (git diff empty), so line 7 is unchanged.",
 "r21-project-table-line224-wording": "Round 22: project.html byte-identical to the round-21 pin (git diff empty). The wording note stands as a note only.",
 "r21-tolerance-ten-checks-match-grader": "Round 22: project.html line 209 and grader unchanged (git diff empty). Grader grep 'absolute=1e-6' and 'abs(total) <= 1e-6' still lists ten sites (round 21 evidence, grader byte-identical).",
 "r21-cards-definition-grade-convention": "Round 22: cards.json entries other than CF1-c084 are byte-identical to the round-21 pin; the definition cards were re-graded in round 21 and are unchanged here.",
 "r21-cards-count-and-fields": "Round 22 (out/cards_scan_r22.out): 109 entries, 59 T and 50 C; every entry has a cite or basis, a grade in {T, C} and unique id, front and back.",
 "r21-mutants-new-four": "Round 22: the four round-21 mutants (r21d_01..r21d_04) are in ledgers/CF1/mutants and killed in the full run (out/mutate_r22_full.out).",
 "r21-mutants-full-run": "Round 22 full run: 208 of 208 killed (out/mutate_r22_full.out).",
 "r21-alternatives-three-new": "Round 22: the three round-21 alternatives (alt_r21d_a, b, c) PASS seeds 0-9 (out/alts_r22.out).",
 "r21-alternatives-all-unique": "Round 22: 65 files, 46 unique, all PASS (out/alts_r22.out).",
 "r21-collect-157-seeds": "Round 22: 157 on seeds 0-9 and 1407000004 (out/collect_r22.out).",
 "r21-run-graders-50": "Round 22: run_graders CF1 50/50 PASS (out/run_graders.out).",
 "r21-gates-checkers": "Round 22: check_projects, check_dag, check_pages PASS (out/check_projects.out, out/check_dag.out, out/check_pages.out).",
 "r21-run-labs-and-twins": "Round 22: run_labs 9/9 (out/run_labs.out); twins under -I -W error exit 0 (out/twins_I_W_error.out).",
 "r21-page-smoke": "Round 22: page_smoke CF1 PASS (out/page_smoke.out).",
 "r21-ruff-mypy": "Round 22: ruff check/format and mypy PASS (out/ruff.out, out/mypy.out, out/mypy_full.out).",
 "r21-verify-refs": "Round 22: verify_refs live 2 of 560, 0 problems; offline 560, 0 problems (out/verify_refs_live.out, out/verify_refs_offline.out).",
 "r21-hours-arithmetic": "Round 22: 6x8=48, 48+12=60, 12/60=20.0%; time-budget cells sum to 12 (index.html line 29, project.html lines 216-230). Consistent; hours not re-estimated (design targets).",
 "r21-e1-e2-arithmetic": "Round 22 recomputed (out/recompute_e1e2.out): 5464.72 cents; 1.2419197; tail 0.214273; band 0.05324 to 0.05716; all match L06.html E1/E2 solutions (lines 313, 320).",
 "r21-run-labs-and-twins-project": "Round 22: the three project twins under -I -W error exit 0 (out/twins_I_W_error.out).",
}

NEW = [
 ("r22-delta-coverage", "Round-22 delta coverage", "git diff --stat f95243f d160ac3 (160 files). Slice-d files: project.html, grader/*, tests/labs/CF1/*, references/references.json are byte-identical (git diff empty). Changed in slice: cards.json, entry CF1-c084 only (one line, out/cards_scan_r22.out). Outside the slice but cited by CF1-c084: L06.html line 106 only."),
 ("r22-card-c084-rewrite", "cards.json CF1-c084 rewritten sentence", "Rewritten back text matches L06.html line 106 wording and the E1/E2 solutions at lines 313 and 320 (see lesson-l06-remark-2-4-each-result-conditional). Scope word 'only' in 'used only as a reading aid': grep of 'normal' and '1.96' in L06.html finds the normal reading only in Remark 2.4 and the two exercises, and nothing else in CF1 lesson or project text applies it to the lesson's results (project.html lines 208 and 433 use gauss(0,1) as a simulation input, not a reading of error). Grade C, basis 'Remark 2.4' right for a reading convention."),
 ("r22-l06-line106-recomputed-numbers", "E1 and E2 numbers recomputed", "ledgers/CF1/scripts/CF1-d-r22/recompute_e1e2.py (out/recompute_e1e2.out): error 5464.72 cents, z 1.2419197 (prints 1.2419 at 4 dp), tail 0.21427 (0.2143), E2 band 0.05324 to 0.05716 (rounded 0.0532 to 0.0572), E2 unrounded share 2761/50000 = 0.05522 with se 0.0010215 (printed 0.0010). All consistent with the page; lab twin output (run under -I -W error) gives 'error_in_se +1.242' and 'share_npv_below_zero 0.0552 se 0.0010'."),
 ("r22-mutants-new-four", "Four new student-error mutants", "ledgers/CF1/mutants/r22d_01..r22d_04 written by ledgers/CF1/scripts/CF1-d-r22/make_mutants22.py: discounted payback accumulating undiscounted flows; working capital from same-year revenue; npv refusing a zero rate; payback needing a strictly positive cumulative. All four are killed on seed 0 (out/mutate_r22_full.out). Each is a plausible student error against project.html line 207 (payback 'reaches zero or more'), line 202 (working capital) and line 188 (rate above -1 valid, zero allowed)."),
 ("r22-mutants-full-run", "Full mutant run, seeds 0-9", "tools/mutate_graders.py --unit CF1 --seeds 0-9: 208 of 208 killed, 'mutate_graders CF1: PASS (208/208 killed)' (out/mutate_r22_full.out, exit 0). No survivor, no equivalent mutant this round."),
 ("r22-alternatives-three-new", "Three new correct alternatives", "scripts/CF1-d-r22/make_alts22.py: alt_r22d_a (grid 8001 points, fixed 120-step bisection), alt_r22d_b (npv by Horner's rule on v = 1/(1+rate)), alt_r22d_c (payback recovery tolerance 1e-9 cents). All three PASS seeds 0-9 (out/alts_r22.out)."),
 ("r22-alternatives-all-unique", "All alternatives rerun", "scripts/CF1-d-r22/run_alts22.py: 65 alternative files, 46 unique by content, every one PASS seeds 0-9 (out/alts_r22.out, 'done')."),
 ("r22-collect-count-seeds", "Collected count across seeds", "scripts/CF1-d-r22/collect_seeds.sh (out/collect_r22.out): 157 tests on seeds 0-9 and 1407000004 against the reference copy. project.html line 192 states 157."),
 ("r22-run-graders-50", "Reference passes 50 seeds", "tools/run_graders.py --unit CF1 --seeds 0-49: 'reference 50/50 seeds, slowest 0.3 s', exit 0 (out/run_graders.out)."),
 ("r22-gates-checkers", "Checkers", "tools/check_projects.py --all, check_dag.py --all, check_pages.py --unit CF1: all PASS, exit 0 (out/check_projects.out, check_dag.out, check_pages.out)."),
 ("r22-page-smoke-project", "Page smoke for project and lessons", "tools/page_smoke.py --unit CF1 (out/page_smoke.out): project.html PASS (in-browser grader 'All 157 tests pass on seed 1407000004'), L06.html PASS, CF1 PASS."),
 ("r22-ruff-mypy", "Lint and types", "ruff check and format --check on grader and labs: PASS; ruff check . 'All checks passed!'; mypy --no-incremental on the CF1 grader 'no issues found in 4 source files'; full mypy '153 source files' (out/ruff.out, out/mypy.out, out/mypy_full.out)."),
 ("r22-labs-pytest-twins", "Labs and twins", "tests/test_labs.py -k CF1 passed (out/pytest_labs.out); run_labs CF1 9/9 (out/run_labs.out); each of the nine twins under python -I -W error exit 0 with empty stderr (out/twins_I_W_error.out)."),
 ("r22-verify-refs", "Registry", "tools/verify_refs.py --unit CF1: '2 of 560 entries, 0 problems'; --offline: '560 entries, 0 problems' (out/verify_refs_live.out, out/verify_refs_offline.out). Registry flag on glasserman2003monte (used_by M8 only) still stands; it is not a verifier failure."),
 ("r22-hours", "Hours arithmetic", "48 lesson hours (six pages data-hours=8), 12 project hours (cells 1+1+4+2+1+1+2), 60 module hours, 20.0% project share. Consistent; design targets not re-estimated."),
]

def strip_old(s):
    # Drop the nested round-N carry prefixes so that only the newest carry prefix is shown.
    while s.startswith("Carried from round") and "): " in s:
        s = s[s.index("): ") + 3:]
    return s

rows = []
for r in prev["rows"]:
    if r["id"] in FRESH:
        rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": FRESH[r["id"]]})
        continue
    assert r["status"] == "PASS", r["id"]
    loc = r["location"]
    assert "c084" not in loc, ("needs fresh evidence", r["id"])
    assert not re.search(r"L06\.html[^;]*\b106\b", loc), ("needs fresh evidence", r["id"])
    rows.append({"id": r["id"], "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": PREFIX + " " + strip_old(r["evidence"])})
for rid, check, ev in NEW:
    rows.append({"id": rid, "check": check, "location": "see evidence", "status": "PASS", "evidence": ev})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
# every fresh id must exist in the previous fragment or in NEW
known = {r["id"] for r in prev["rows"]} | {n[0] for n in NEW}
missing = [i for i in FRESH if i not in known]
print("fresh ids not in previous fragment:", missing)

mut = list(prev["mutants"])
for f, desc, killed in [
    ("ledgers/CF1/mutants/r22d_01_discounted_payback_accumulates_undiscounted_flows.py",
     "Discounted payback accumulates the undiscounted flows in the cumulative sum, but still divides by the discounted flow.",
     "test_discounted_payback_uses_discounted_flows (seed 0)"),
    ("ledgers/CF1/mutants/r22d_02_working_capital_uses_same_year_revenue.py",
     "Working capital at the end of year t is set from the revenue of year t instead of year t - 1.",
     "test_working_capital_investment_and_recovery_sum_to_zero (seed 0)"),
    ("ledgers/CF1/mutants/r22d_03_npv_refuses_a_zero_rate.py",
     "NPV refuses a zero rate, as if the rate had to be strictly positive.",
     "test_npv_at_zero_rate_is_the_plain_sum (seed 0)"),
    ("ledgers/CF1/mutants/r22d_04_payback_needs_strictly_positive_cumulative.py",
     "Payback is the first year in which the cumulative flow is strictly above zero, so an exact recovery is missed.",
     "test_payback_ignores_flows_after_the_cut_off (seed 0)"),
]:
    mut.append({"file": f, "description": desc, "killed_by": killed})

summary = ("CF1-d round 22 (pin d160ac3): {n} rows, all PASS. Delta f95243f..d160ac3 touches the slice only at cards.json entry "
           "CF1-c084 (the card now restates the L06 Remark 2.4 split); project.html, grader, labs, references are byte-identical. "
           "The round-21 FAIL lesson-l06-remark-2-4-each-result-conditional is resolved (L06.html line 106 now names only the tail "
           "probability in E1 and the band in E2 as conditional, which matches E1/E2 solutions). Mutants: 208 of 208 killed (4 new, "
           "r22d_01..04). Alternatives: 46 unique engines, all pass seeds 0-9 (3 new, alt_r22d_a..c). Collect 157 on 11 seeds.").format(n=len(rows))

frag = {
 "unit": "CF1",
 "slice": "CF1-d",
 "round": 22,
 "verifier": "independent verifier (Haiku), round 22 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
 "pin": "d160ac3 (detached, /tmp/verify22-CF1-d)",
 "base": "f95243f (round-21 pin; delta computed with git diff --stat f95243f d160ac3, every slice hunk read)",
 "checkout": "/tmp/verify22-CF1-d",
 "scratch": "/tmp/CF1-v/d22",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": mut,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": ("Round-22 delta for this slice: cards.json CF1-c084 (one line). L06.html line 106 (outside the slice, cited by CF1-c084) "
           "re-verified with E1/E2. Eleven carried grader and card-count rows (proj-tolerance-relative-only, proj-tolerance-rationale, proj-fisher-tolerance-zero-cases, proj-tolerance-claim-note, cards-changed-c014-c037-c047-c057, r15-grader-zero-flow-two-zeros, r15-tolerance-claims-carried-check, r16-cards-c099-standard-error-definition, cards-changed-r17-c023-c036-c051-c053, cards-new-r17-c105-c109, proj-mc-draw-method-unenforced) keep an old evidence chain that names L06.html line 106 only as an incidental locator for a lesson cross-reference; their cited subjects (grader, project.html line 209, the other cards) are byte-identical and the line-106 change does not affect their claims. Rows carried from round 21 keep their evidence with the carry prefix and cite only files and "
           "entries that are byte-identical to f95243f (the carry excludes any row citing CF1-c084 or L06.html line 106). "
           "Not checked: live Crossref or SEC access (not used this round); the full BLUEPRINT re-grade of all 109 cards against "
           "lesson text (only the changed entry and whole-file scans); hours not re-estimated (design targets); seeds 10-49 "
           "were not all re-collected (11 seeds sampled); Pyodide browser beyond page_smoke; the L01-L05 lesson rows that are "
           "carried are outside this slice and are verified by their own slices."),
 "summary": summary,
}
json.dump(frag, open(f"{CHK}/ledgers/CF1/CF1-d.json", "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), "mutants", len(mut))
