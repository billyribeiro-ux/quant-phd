"""Build ledgers/CF1/CF1-c.json for round 17 from the round-16 fragment (context) plus this round's re-runs."""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
prev = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-c.round16.json").read_text(encoding="utf-8"))
PREFIX = ("Carried from round 16 (course/modules/CF/CF1/L05.html, L06.html, index.html, tests/labs/CF1, references/, tools/ "
          "byte-identical since the previous pin c5daab2; the cited cards.json entries unchanged in the delta): ")
LAB_FILES = "course/modules/CF/CF1/L05.html and L06.html (byte-identical since c5daab2)"
RERUN = {
 "CF1-c-cmd-pin": ("2.5-labs", "git rev-parse HEAD -> fefbf8b67c335e868986ecaed90046e6a3bf5414 (detached); git status: only the untracked .venv symlink. Delta c5daab2..fefbf8b for slice c: course/modules/CF/CF1/cards.json only (cards CF1-c096 changed, CF1-c109 added); L05.html, L06.html, index.html, tests/labs/CF1, tools/, references/, notation/, curriculum/, atlas/ byte-identical (git diff --quiet). Outputs: ledgers/CF1/scripts/CF1-c-r17/out/."),
 "CF1-c-cmd-check_pages": ("2.9-structure", "tools/check_pages.py --all: 'check_pages CF1: PASS', exit 0 (ledgers/CF1/scripts/CF1-c-r17/out/check_pages.out)"),
 "CF1-c-cmd-check_dag": ("dag-concepts", "tools/check_dag.py --all: 'check_dag CF1: PASS', exit 0 (out/check_dag.out)"),
 "CF1-c-cmd-run_labs": ("2.5-labs", "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)', exit 0 (out/run_labs.out)"),
 "CF1-c-cmd-page_smoke": ("2.5-labs", "tools/page_smoke.py --unit CF1 --pages L05 L06: 'page_smoke modules/CF/CF1/L05.html: PASS', 'modules/CF/CF1/L06.html: PASS', lab-CF1-L06-1 0.3 s, 'page_smoke CF1: PASS', exit 0 (out/smoke.out)"),
 "CF1-c-cmd-ruff-mypy-labs": ("2.5-labs", "ruff check . ('All checks passed!'); ruff format --check . ('212 files already formatted'); mypy --no-incremental ('Success: no issues found in 153 source files'). out/ruff.out, out/mypy.out"),
 "CF1-c-cmd-pytest-labs": ("2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: all dots, exit 0 (out/pytest_full.out)"),
 "CF1-c-cmd-verify_refs": ("2.1-citations", "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0; tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems' (out/vr_offline.out, out/vr_live.out)"),
 "CF1-c-cmd-twin-vs-page": ("2.5-labs", "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py run under python -I against this checkout: lab-CF1-L05-1 and lab-CF1-L06-1 'expected identical to twin output: True' (out/twin_vs_page.out). Strict code identity is False for both (the page code block differs from the twin by a trailing newline only: 'ignoring one trailing newline: True'), as in round 16."),
 "CF1-c-twin-freshness": ("2.5-labs", "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py: twin_vs_page.py reports the embedded expected output identical to the twin output (out/twin_vs_page.out); tests/labs byte-identical to c5daab2"),
 "CF1-c-lab-L05-1-run": ("2.5-labs", "python -I -W error tests/labs/CF1/lab-CF1-L05-1.py: exit 0; output out/lab_L05.out ('project A simple_payback 2.750 discounted_payback 3.469 npv_cents 289367.40'; 'tail_npv_cents_min 121251.71 tail_npv_cents_max 693692.91')"),
 "CF1-c-lab-L06-1-run": ("2.5-labs", "python -I -W error tests/labs/CF1/lab-CF1-L06-1.py: exit 0; output out/lab_L06.out ('share_npv_below_zero 0.0552 se 0.0010', 'sd_npv_cents_closed_form 49379.84')"),
 "CF1-c-cards-duplicates": ("2.7-cards", "cards.json: 109 cards, 109 unique ids, 0 duplicate fronts, 0 duplicate backs, all grades valid (ledgers/CF1/scripts/CF1-c-r17/out/cards_r17.out). Previous count 103; +6 added (c104 to c109)."),
 "CF1-c-cards-dupes-r12-cross": ("2.7-cards", "cards.json all cards: 0 duplicate fronts, 0 duplicate backs (out/cards_r17.out)"),
 "CF1-c-mutants-na-r12": ("2.5-labs", "ledgers/CF1/mutants/: this slice (labs) has no project-grader mutants; the 139 mutants there are re-run in CF1-c-cmd-mutants-na-r13 and are not applicable to labs"),
 "CF1-c-cmd-mutants-na-r13": ("2.5-labs", "tools/mutate_graders.py --unit CF1 --seeds 0-9 (re-run this round): 'mutate_graders CF1: PASS (139/139 killed)', exit 0 (out/mutate_graders_CF1.out). These are project-grader mutants, outside slice c; recorded for the re-run requirement."),
 "CF1-c-r16-mutants-na": ("2.5-labs", "Same run as CF1-c-cmd-mutants-na-r13: 139/139 killed, including r15e_01..03 and r16_01..03 (out/mutate_graders_CF1.out)"),
 "CF1-c-r16-coverage-note": ("2.5-labs", "Scope of round 17: slice c delta (cards CF1-c096 changed, CF1-c109 added); every other slice-c row carried from round 16 with its subject byte-identical; all command rows re-run"),
 "CF1-c-registry-r13": ("2.1-citations", "references/references.json unchanged in the delta; tools/verify_refs.py --offline 0 problems; --unit CF1 live 2 of 560 entries 0 problems. graham2001theory (L05.html line 234) and glasserman2003monte (L06.html line 106) entries read again"),
 "CF1-c-registry-r12": ("2.1-citations", "references/references.json entries graham2001theory and glasserman2003monte re-read; unchanged since c5daab2; verify_refs --offline clean (out/vr_offline.out)"),
 "CF1-c-cards-L05": ("2.7-cards", "cards.json L05 cards (CF1-c062 to c074, c096 to c098, c102, c109): c096 changed this delta; the new back is the Definition 1.1 formula (L05.html line 60) but its grade is C with basis 'convention, Section 1 (interpolation)'. See CF1-c-r17-cards-c096-grade. Other L05 cards unchanged and re-checked against L05.html lines 58-62, 70, 75-92, 203, 218 by the carried rows."),
}
NEW = [
 {"id": "CF1-c-r17-cards-c109", "check": "2.7-cards", "location": "cards.json CF1-c109 (lesson L05, grade C, basis 'convention, Section 1 (interpolation)'); L05.html line 62 (Definition 1.1 block, lines 56-63)", "status": "PASS",
  "evidence": "Card back 'That they arrive evenly through the year. This is a convention and not a finding (Definition 1.1).' against L05.html line 62: 'The interpolation assumes that the flows of that year arrive evenly through the year. It is a convention, and it is not a finding.' Same wording, same block. Grade C is consistent with a convention statement. Not a duplicate of CF1-c096 (different question)."},
 {"id": "CF1-c-r17-cards-c096-formula", "check": "2.7-cards", "location": "cards.json CF1-c096 back vs L05.html line 60 (Definition 1.1 display)", "status": "PASS",
  "evidence": "Card back '(tau_S - 1) + (-CUM_(tau_S - 1)) / C_(tau_S)' matches the displayed formula PB = (tau_S - 1) + (-CUM_(tau_S - 1))/C_(tau_S) in Definition 1.1 (L05.html line 60). The formula is correct; only its grade is wrong (next row)."},
 {"id": "CF1-c-r17-cards-c096-grade", "check": "2.3-grades", "location": "cards.json CF1-c096 (grade 'C', basis 'convention, Section 1 (interpolation)'); compare CF1-c062 (grade T, basis 'Definition 1.1') and BLUEPRINT.md section 3 grade table (line 156 onward)", "status": "FAIL",
  "evidence": "The back of CF1-c096 is the definitional formula of the fractional payback (Definition 1.1, L05.html line 60), which the page states as the definition, not as a finding. BLUEPRINT section 3 grade T is 'proved on the page' and C is 'working paper, practitioner research, or single-sample evidence'. Labelling a definition as C with basis 'convention' is a grade mismatch, and the convention it names is the arrival of flows (now card CF1-c109), which the back of c096 no longer states. Same content class as CF1-c062 (grade T, basis Definition 1.1)."},
 {"id": "CF1-c-r17-cards-delta", "check": "2.7-cards", "location": "git diff -U0 c5daab2 fefbf8b -- course/modules/CF/CF1/cards.json; ledgers/CF1/scripts/CF1-c-r17/out/cards_r17.out", "status": "PASS",
  "evidence": "Added CF1-c104 to c109 (L02 to L05 lessons: c109 is slice c, the others are outside it). Changed CF1-c023 (L02), c036 (L03), c051, c053, c056 (L04), c096 (L05). Slice-c changes are c096 (FAIL row above) and the added c109 (PASS row). Full duplicate scan: 0 duplicate fronts, 0 duplicate backs over 109 cards. Card counts in the plan line 240 are outside slice c and were not verified here."},
 {"id": "CF1-c-r17-delta-pages", "check": "2.9-structure", "location": "git diff --quiet c5daab2 fefbf8b -- course/modules/CF/CF1/L05.html L06.html index.html tests/labs/CF1 tools references notation curriculum atlas; md5sum of L05.html 5e8af6466f1aff44a23b91cdd54e36ce and L06.html e7fb0b18f17027e1de6d56e9d452cc10 at both pins", "status": "PASS",
  "evidence": "git diff --quiet returned 0 for all listed paths (byte-identical); md5 matches at c5daab2 and fefbf8b. Therefore every slice-c page row from round 16 is carried, and its cited page text is unchanged."},
 {"id": "CF1-c-r17-mutants-lab-L06", "check": "2.5-labs", "location": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_01 to 05 (mutants of tests/labs/CF1/lab-CF1-L06-1.py); outputs ledgers/CF1/scripts/CF1-c-r17/out/*.out", "status": "PASS",
  "evidence": "Five student-error mutants of the L06 twin (mk_lab_mutants.py). Killed (output differs from out/lab_L06.out at a number the page quotes): 01 population SD for the standard error (se 4400.22 to 4378.16; page quotes 4400.22); 02 quantile rank int(p n)+1 (quantile_10 14896.62 to 14898.90; page quotes 14896.62); 03 discount exponent t instead of t+1 (9 lines change, including the n = 100 mean 84543.40 and the n = 50000 mean 79216.82); 05 standard error divided by sqrt(n-1) (se 4400.22 to 4422.38). Survivor 04 is proved equivalent below."},
 {"id": "CF1-c-r17-mut-L06-04-equivalent", "check": "2.5-labs", "location": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_04_share_counts_zero_npv_as_negative.py; ledgers/CF1/scripts/CF1-c-r17/zero_check.py and out/zero_check.out", "status": "PASS",
  "evidence": "Mutant 04 changes 'x < 0' to 'x <= 0' in the share count. Its output is identical to out/lab_L06.out (0 diffs). Proof on this seed: zero_check.py over the 50000 seeded draws gives exact_zero_draws 0 and min |NPV| 0.148 cents, so no draw equals zero and the mutant is equivalent for seed 6. It is not in the mutants list. The page's sentence 'share of draws with a negative NPV' is not contradicted."},
 {"id": "CF1-c-r17-alt-impl", "check": "2.5-labs", "location": "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py (no assert statements: grep -c assert = 0 each)", "status": "PASS",
  "evidence": "The twins contain no assertions and no grader; their correctness is the printed output versus the page (twin_vs_page.py, page_smoke). Alternative correct implementations are therefore not an over-constraint question for labs; the project grader alternatives are slice d. Recorded as not applicable with the grep result."},
 {"id": "CF1-c-r17-mutants-project-grader", "check": "2.5-labs", "location": "ledgers/CF1/mutants/ (139 project-grader mutants) via tools/mutate_graders.py --unit CF1 --seeds 0-9", "status": "PASS",
  "evidence": "'mutate_graders CF1: PASS (139/139 killed)' (out/mutate_graders_CF1.out). These mutate the project grader, not the labs; they are outside slice c and are recorded only for the re-run requirement."},
 {"id": "CF1-c-r17-mutants-placement", "check": "2.5-labs", "location": "ledgers/CF1/scripts/CF1-c-r17/mutants/ (lab-twin mutants) instead of ledgers/CF1/mutants/", "status": "PASS",
  "evidence": "The brief named ledgers/CF1/mutants/ for new mutants. Lab-twin mutants were kept in the scripts folder because tools/mutate_graders.py globs every file in ledgers/CF1/mutants/ as a grader replacement, so lab mutants there would corrupt the project gate. This is a placement choice; the mutants are cited by path here."},
]

RERUN.update({
 "CF1-c-cards-delta-r12": ("2.7-cards", "Historic round-12 delta (c093bf5..c5daab2) superseded: the current delta is c5daab2..fefbf8b, evidenced by CF1-c-r17-cards-delta (added c104 to c109; changed c023, c036, c051, c053, c056, c096). Round-12 claims about c068 and c099 are unchanged in the current delta (their back text is byte-identical to c5daab2)."),
 "CF1-c-r16-delta-cross-slice": ("2.9-structure", "Historic round-16 delta superseded by CF1-c-r17-delta-pages and CF1-c-r17-cards-delta. git diff --stat c5daab2 fefbf8b: 71 files, none of them L05.html, L06.html, index.html, tests/labs/CF1, tools/ or references/ (git diff --quiet 0); the course changes are AC1 and AC4 cards, AC1 grader and project, and CF1 cards.json."),
 "CF1-c-delta-cross-slice-notes": ("2.9-structure", "cards.json CF1-c054, c056, c058, c060, c094 are all lesson L04 (re-read this round; outside slice c); CF1-c056 changed in this delta but stays an L04 card. project.html of CF1 unchanged (git diff --quiet c5daab2 fefbf8b exit 0)."),
 "CF1-c-cards-L05-other": ("2.7-cards", "cards.json CF1-c062 to c067, c069 to c074 and CF1-c068 (back text byte-identical to c5daab2: 'The simple rule uses no discount rate ...') checked against L05.html line 70; none changed in this delta (CF1-c096 and CF1-c109 are the L05 cards that changed or were added)."),
 "CF1-c-cards-L06-c-other": ("2.7-cards", "cards.json CF1-c099 (back byte-identical to c5daab2) and the other L06 cards CF1-c075 to c087, c100: none changed in this delta (git diff -U0 c5daab2 fefbf8b lists no L06 card)."),
})
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        check, ev = RERUN[rid]
        if rid == "CF1-c-cards-L05":
            rows.append({"id": rid, "check": check, "location": "cards.json L05 cards CF1-c062..c074, c096..c098, c102, c109", "status": "FAIL", "evidence": ev,
                         "fix": "Set cards.json CF1-c096 grade to T with basis 'Definition 1.1' (the back is the definitional formula, consistent with CF1-c062). Keep the convention on CF1-c109 (grade C). Then re-run tests/test_docs_figures.py and the card duplicate scan."})
        else:
            rows.append({"id": rid, "check": check, "location": r["location"], "status": "PASS", "evidence": ev})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": PREFIX + r["evidence"]})
rows += NEW
fail_rows = [x for x in rows if x["status"] != "PASS"]
for x in fail_rows:
    if x["id"] == "CF1-c-r17-cards-c096-grade" and "fix" not in x:
        x["fix"] = "Set cards.json CF1-c096 grade to T with basis 'Definition 1.1' (not 'convention'); the convention stays on CF1-c109 (grade C)."
    if x["id"] == "CF1-c-r17-cards-c096-grade":
        x["verdict"] = "CONFIRMED"
        x["failure_scenario"] = "A learner reads card CF1-c096 as a grade-C finding about the payback convention; the formula is a definition and the grade table gives C only to single-sample or working-paper evidence."
frag = {
 "unit": "CF1", "slice": "CF1-c", "round": 17,
 "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 17; did not build CF1; no shared context with builders or earlier verifiers",
 "pin": "fefbf8b67c335e868986ecaed90046e6a3bf5414",
 "base": "c5daab2 (round 16 pin; the round-16 fragment is context only)",
 "checkout": "/tmp/verify17-CF1-c (detached worktree at fefbf8b; .venv symlinked; vendor copied)",
 "scratch": "/tmp/cf1-v/c17",
 "verified_at": "2026-10-28T10:31:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [
  {"id": "c17_L06_01_population_sd_for_se", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_01_population_sd_for_se.py", "description": "Student uses the population SD (pstdev) for the standard error of the mean instead of the sample SD; the page's Definition 1.2 requires the sample SD.", "killed_by": "lab output: se_cents 4400.22 becomes 4378.16 at n = 100; the page quotes 4400.22 (L06.html line 206)"},
  {"id": "c17_L06_02_quantile_rank_floor_plus_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_02_quantile_rank_floor_plus_one.py", "description": "Student uses rank int(p n) + 1 for the nearest-rank quantile instead of ceil(p n) (off by one on exact integers); the page's quantile definition is nearest-rank.", "killed_by": "lab output: quantile_10_npv_cents 14896.62 becomes 14898.90; the page quotes 14896.62"},
  {"id": "c17_L06_03_discount_exponent_off_by_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_03_discount_exponent_off_by_one.py", "description": "Student discounts year-t receipts by (1+r)^t instead of (1+r)^(t+1), so every receipt is discounted one year too little.", "killed_by": "lab output: 9 lines change (n 100 mean_npv_cents 84543.40 and later rows); the page quotes 84543.40 and 79216.82"},
  {"id": "c17_L06_05_se_divides_by_n_minus_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_05_se_divides_by_n_minus_one.py", "description": "Student divides the sample SD by sqrt(n - 1) instead of sqrt(n) in the standard error.", "killed_by": "lab output: se_cents 4400.22 becomes 4422.38 at n = 100; the page quotes 4400.22"},
 ],
 "registry_flags": ["glasserman2003monte: registry used_by is ['M8'] but CF1 L06 cites this key; the key is no longer in learner text (the span names the title only). Not a row failure. (Carried from round 16.)"],
 "freshness_flags": [
  "Delta c5daab2..fefbf8b for slice c: cards.json only. CF1-c096 changed (grade and basis; FAIL row). CF1-c109 added (PASS row). L05.html, L06.html, index.html, labs, tools, references are byte-identical, so all page rows are carried.",
  "Mutant 04 (x <= 0) is equivalent for seed 6 and is not in the mutants list; its proof row is CF1-c-r17-mut-L06-04-equivalent.",
  "Outside slice c and not verified here: plans/CF1-build-plan.md line 240 (card-count rule now 'BUILDER_RULES section 7'); course/modules/AC/AC1 and AC4 cards and AC1 project files; CF1 L02-L04 card changes."],
 "notes": [
  "Lab-twin mutants were written under ledgers/CF1/scripts/CF1-c-r17/mutants/ and not under ledgers/CF1/mutants/, because tools/mutate_graders.py treats every file in ledgers/CF1/mutants/ as a project grader replacement (deviation from the brief, reason in row CF1-c-r17-mutants-placement).",
  "Lab-twin test: twins run under python -I -W error exit 0. Lab 1 of L06 prints the closed forms and the share of negative NPVs; these are the numbers the page quotes (checked by the carried rows).",
  "Hours not re-estimated (architect ruling); data-hours=8 on L05 and L06 unchanged in this delta."
 ],
 "summary": "CF1-c round 17 (pin fefbf8b): %d rows; FAIL 2 rows for one defect (CF1-c096 grade C with basis 'convention' on a definitional formula; fix: grade T, basis Definition 1.1; rows CF1-c-cards-L05 and CF1-c-r17-cards-c096-grade). Four of five lab mutants killed; mutant 04 equivalent on seed 6 (proof row). New row CF1-c109 PASS. All command rows re-run." % len(rows),
}
out = ROOT / "ledgers/CF1/CF1-c.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", len(fail_rows), "written", out)
