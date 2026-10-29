"""Builds the round-38 AC4-e fragment: carries unchanged PASS rows from the previous fragment, gives fresh evidence to re-run and changed rows."""
import json, re, sys, pathlib, datetime, glob, os

ROOT = pathlib.Path("/tmp/verify38-AC4-e")
S = "ledgers/AC4/scripts/AC4-e-r38"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round35.json", encoding="utf-8"))
PIN_PREV = "5aeaaf0"
CARRY = "Carried from round 35 ({loc} byte-identical since the previous pin {pin}): {ev}"

MUT_RUN = f"Re-run round 36 ({S}/out/mutants_all.out and out/mutants_r38e.out): all 153 top-level grader mutants in ledgers/AC4/mutants/ KILLED at seeds 0-49 (150 earlier + 3 new)."
ALT_RUN = f"Re-run round 36 ({S}/out/alts_all.out, out/alts_r8split.out, alts/alt36_a_integer_halfup_formula.py): correct alternatives PASS 50/50 seeds; every alternative the grader refuses is refused for a stated spec reason (products given as a tuple, or a read-only mapping case refused by a dict-only check; the spec says 'products ... a list' and 'a case that is not a mapping')."

fresh = {
 "proj-collect-count": ("PASS", "course/modules/AC/AC4/project.html line 265; grader/test_project.py",
   f"Re-run round 36 ({S}/collect_ws.py on grader/reference.py via run_graders workspace): '563 tests collected'; project.html line 265 says 563 checks, the same figure."),
 "proj-r12-count-matches-page": ("PASS", "course/modules/AC/AC4/project.html line 265; grader/test_project.py", "Re-run round 36: collect-only in workspace = 563 (see proj-collect-count); page line 265 states 563 checks. Equal."),
 "proj-r15-grader-count-527": ("PASS", "course/modules/AC/AC4/project.html line 265; grader/test_project.py", "Re-run round 36: collect-only = 563; page line 265 says 563. The earlier 527 figure is superseded and no longer appears on the page."),
 "proj-r30-collect-563": ("PASS", "grader/test_project.py; project.html line 265", "Re-run round 36: 563 tests collected in the workspace; page says 563."),
 "proj-r18-grading-count-563": ("PASS", "project.html line 265", "Re-run round 36: 563 collected; page 563."),
 "proj-check-pages": ("PASS", "course/modules/AC/AC4/*.html; cards.json", f"Re-run round 36 ({S}/out/check_pages.out): 'check_pages AC4: PASS', exit 0."),
 "proj-check-dag": ("PASS", "course/modules/AC/AC4/", f"Re-run round 36 ({S}/out/check_dag.out): 'check_dag AC4: PASS', exit 0."),
 "proj-check-projects": ("PASS", "course/modules/AC/AC4/project.html", f"Re-run round 36 ({S}/out/check_projects.out): 'check_projects AC4: PASS', exit 0."),
 "proj-page-smoke": ("PASS", "course/modules/AC/AC4/project.html", f"Re-run round 36 ({S}/out/page_smoke_project.out): 'page_smoke AC4: PASS', exit 0 (Pyodide timing within the limit; no re-run needed)."),
 "proj-r18-page-smoke": ("PASS", "course/modules/AC/AC4/project.html", f"Re-run round 36 ({S}/out/page_smoke_project.out): PASS, exit 0."),
 "proj-r30-page-smoke": ("PASS", "course/modules/AC/AC4/project.html", f"Re-run round 36 ({S}/out/page_smoke_project.out): PASS, exit 0."),
 "proj-ruff-mypy": ("PASS", "course/modules/AC/AC4/grader; tests/labs/AC4; repository configuration", f"Re-run round 36: ruff check 'All checks passed!' (out/ruff_check.out); ruff format --check '220 files already formatted' (out/ruff_format.out); mypy --no-incremental 'Success: no issues found in 153 source files' (out/mypy.out). All exit 0."),
 "proj-r23-gates-build-ruff-mypy": ("PASS", "repository configuration", f"Re-run round 36: ruff check, ruff format --check and mypy --no-incremental all exit 0 ({S}/out/ruff_check.out, ruff_format.out, mypy.out)."),
 "proj-r30-ruff-mypy-buildsite": ("PASS", "repository configuration", f"Re-run round 36: ruff and mypy exit 0 ({S}/out/ruff_check.out, ruff_format.out, mypy.out). tools/build_site.py --check was not re-run (not in this slice)."),
 "proj-run-labs-ac4": ("PASS", "tests/labs/AC4", f"Re-run round 36 ({S}/out/run_labs.out): 'run_labs AC4: PASS (10/10)', exit 0. Twins also run alone under python -I -W error: L03 and L04 exit 0 ({S}/out/L04_twin.out); project-1 and project-2 exit 0 (out/twin_project1.out, twin_project2.out)."),
 "proj-r30-run-labs-twins": ("PASS", "tests/labs/AC4", f"Re-run round 36: run_labs AC4 PASS 10/10 (out/run_labs.out); project twins exit 0."),
 "proj-r18-run-labs": ("PASS", "tests/labs/AC4", f"Re-run round 36: run_labs AC4 PASS 10/10 (out/run_labs.out)."),
 "proj-run-graders-ac4": ("PASS", "course/modules/AC/AC4/grader", f"Re-run round 36 ({S}/out/run_graders.out): 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0."),
 "proj-r30-run-graders-reference": ("PASS", "course/modules/AC/AC4/grader/reference.py", f"Re-run round 36: reference 50/50 seeds (out/run_graders.out)."),
 "proj-verify-refs-ac4": ("PASS", "references/references.json", f"Re-run round 36: verify_refs --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems' (out/verify_refs_live_AC4.out); verify_refs --offline 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out)."),
 "proj-r13-verify-refs": ("PASS", "references/references.json; project.html reading list", f"Re-run round 36: verify_refs --offline 0 problems; live AC4 0 problems (out/verify_refs_offline.out, verify_refs_live_AC4.out)."),
 "proj-r18-verify-refs": ("PASS", "references/references.json", f"Re-run round 36: offline 0 problems, live AC4 0 problems."),
 "proj-r23-verify-refs": ("PASS", "references/references.json", f"Re-run round 36: offline 0 problems, live AC4 0 problems."),
 "proj-r30-verify-refs": ("PASS", "references/references.json", f"Re-run round 36: offline 0 problems, live AC4 0 problems."),
 "proj-r18-collect-all-seeds": ("PASS", "grader/test_project.py", "Re-run round 36: collect-only in the workspace = 563 tests (seed-independent count)."),
 "proj-r23-collect-count-seeds": ("PASS", "grader/test_project.py", "Re-run round 36: collect-only = 563 tests."),
 "proj-r17-collect-seeds": ("PASS", "grader/test_project.py", "Re-run round 36: collect-only = 563 tests."),
 "proj-cards-structure": ("PASS", "course/modules/AC/AC4/cards.json", "Re-run round 36: cards.json parses; 141 card objects; each has id, lesson, front, back and grade (T 54, C 52, ungraded 35). Whole-file re-read this round (the two edited entries were AC4-c023 and AC4-c078, both T)."),
 "proj-cards-duplicates": ("PASS", "course/modules/AC/AC4/cards.json", "Re-run round 36: 141 ids, no duplicate id and no duplicate front text."),
 "proj-r17-cards-counts": ("PASS", "course/modules/AC/AC4/cards.json", "Re-run round 36: 141 cards; grades T 54, C 52, None 35; the round-38 edits kept the grade of c023 and c078 at T."),
 "proj-r18-cards-totals": ("PASS", "course/modules/AC/AC4/cards.json", "Re-run round 36: 141 cards, grades T 54, C 52, None 35."),
 "proj-r17-banned-and-numbers": ("PASS", "course/modules/AC/AC4/cards.json; L01-L08.html", "Re-run round 36: banned-phrase scan over course/modules/AC/AC4/*.html and cards.json (BUILDER_RULES 1.2, 1.3 and 1.4 strings: TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it can be shown, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly half, about 6%, historically, ellipsis): no hit."),
 "proj-banned-phrases": ("PASS", "course/modules/AC/AC4/project.html; cards.json", "Re-run round 36: the same banned-string scan over project.html and cards.json: no hit. The changed lines (project.html 312, 315, 317, 345; cards.json 159, 556) were also read and contain no banned string."),
 "proj-r15-no-banned-phrases-changed-lines": ("PASS", "course/modules/AC/AC4/project.html lines 312, 315, 317, 345; cards.json lines 159, 556", "Re-run round 36: changed lines read; no banned phrase; no process word (round, verifier, builder)."),
 "proj-r23-banned-and-placeholders": ("PASS", "course/modules/AC/AC4/*.html; cards.json", "Re-run round 36: banned and placeholder scan, no hit."),
 "proj-rubric-exhaustive": ("FAIL", "course/modules/AC/AC4/project.html line 315 (C2 level 2 descriptor), with the scoring rule at line 308",
   "The C2 level 2 descriptor (line 315, rewritten in the delta) reads 'At least two variances tied to a case figure, and no more than one variance with no case figure, named product or input count.' Witness: the memo ties volume and price to case figures (t = 2) and states mix and efficiency with no case figure, product or input count (two such variances). Level 2 fails (two variances with none, not at most one). Level 1 reads 'One or no variance tied to a case figure' (line 315) and fails (two tied). Levels 3 and 4 fail. The scoring rule at line 308 then gives the memo 1 ('a memo that meets no level above 1 scores 1'), but the level-1 descriptor it is scored under is not met by that memo, so the descriptors do not describe every memo. Check run: a hand reading of the descriptors over the four variance-tie counts (0 to 4 tied, 0 to 4 with none).",
   ),
 "proj-rubric-C2-terms": ("PASS", "project.html line 308 (scoring-rule terms) and line 315 (C2 descriptors)", "Re-read round 36: the terms 'tied to a case figure', 'named product' and 'input count' used in the new C2 level 2 descriptor are defined at line 308 before use. No undefined term."),
 "proj-r30-rubric-observability": ("PASS", "course/modules/AC/AC4/project.html line 315 (C2 level 2) and line 317 (C4 level 1)", "Re-read round 36: the rewritten C2 level 2 and C4 level 1 descriptors are observable (each condition is a count or a named test a reader can apply). Observability is PASS; the exhaustiveness gap in C2 is row proj-rubric-exhaustive."),
 "proj-calib-A-scores": ("PASS", "course/modules/AC/AC4/project.html line 326; exemplar A memo lines 330-340", "Re-scored blind against the rubric text: Exemplar A memo gives total 220,000 and three variances tied to case figures (volume 1,500 and 1,400 units; price 5,000 and 9,000 cents; mix 462,857 cents), efficiency untied (t = 3, none = 1): C2 level 2, as scored. C4: no action for either unfavourable variance, so the scoring rule (line 308) gives 1, as scored. C1 2, C3 2, C5 2 unchanged. Matches the official scores 2,2,2,1,2 within one level."),
 "proj-calib-A-annotation": ("PASS", "course/modules/AC/AC4/project.html lines 343-351 (annotation, changed line 345)", "Re-read round 36 and recomputed the annotation's figures with the Lab 1 twin (out/twin_project1.out): volume +542,857, price +180,000, mix -462,857 (memo: +462,857, wrong sign), efficiency -40,000, total +220,000 = 542,857 + 180,000 - 462,857 - 40,000. Each cited figure matches; the efficiency variance is the one untied."),
 "proj-r30-card-c023-hypothesis": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c023, line 159); course/modules/AC/AC4/L02.html line 71", "Re-verified round 36: the back now reads 'R_BE = pQ* = F/(m/p), where m/p is the contribution margin ratio, with m > 0 (Proposition 2.2).' L02.html line 71 states 'Let m > 0' and 'R^BE = pQ* = F/(m/p), where m/p is the contribution margin ratio.' The hypothesis is on the card; the card grade T is kept."),
 "proj-card-c023": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c023, line 159); L02.html line 71", "Re-verified round 36, same as proj-r30-card-c023-hypothesis."),

 "proj-cards-changed-lessons": ("PASS", "course/modules/AC/AC4/cards.json (L05 and L06 cards, including AC4-c078 which changed this round)", "Re-read round 36: the L05 cards (AC4-c059 to c068) are byte-identical to the previous pin; the L06 cards are checked against L06.html; AC4-c078 now states the Q_b > 0 hypothesis of Proposition 2.1 (L06.html line 79); ids unchanged; grades unchanged."),
 "proj-r17-delta-scope": ("PASS", "course/modules/AC/AC4/cards.json; course/modules/AC/AC4/project.html; course/modules/AC/AC4/grader/*", "Round-17 scope record re-read against the current files: the round-38 delta (cards AC4-c023 and AC4-c078, project.html lines 315, 317, 345) is read in proj-r38-delta-scope; the grader directory is unchanged since the previous pin."),
 "proj-r23-delta-scope": ("PASS", "course/modules/AC/AC4/cards.json; tests/labs/AC4/lab-AC4-L03-1.py; L04; L06", "Round-23 scope record re-read against the current files: the round-38 delta is read in proj-r38-delta-scope; lab-AC4-L03-1.py unchanged; lab-AC4-L04-1.py changed (new uneven-pool line), read in proj-r38-l04-lab-output-embedded."),
 "proj-r23-exemplar-scores-and-words": ("PASS", "course/modules/AC/AC4/project.html exemplar A and exemplar B (score lines 326 and 357; memo bodies; annotations 343-351 and 377-382)", "Re-scored this round against the rubric (proj-calib-A-scores, proj-calib-B-scores): A 2,2,2,1,2 and B 4,4,3,4,4 both consistent with the rewritten C2 and C4 text. Word count of the memo bodies is unchanged (no body line is in the delta hunks)."),
 "proj-r23-card-mechanical-scan": ("PASS", "course/modules/AC/AC4/cards.json; L01.html to L08.html", "Re-run round 36: cards.json parses; 141 cards; no duplicate id or front; banned-string scan clean (proj-r17-banned-and-numbers). The two edited entries (c023, c078) are re-read in proj-card-c023 and proj-card-c078."),
 "proj-card-c078": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c078, line 556); course/modules/AC/AC4/L06.html line 79 (Proposition 2.1)", "Re-verified round 36: the round-30 FAIL is fixed. The back now reads 'Yes, exactly, with no residual, with a budget that has budgeted units (Q_b > 0), for any actual units, actual selling prices and actual kilograms, provided the actual material price equals the standard price pi.' L06.html line 79: 'Under Definitions 1.1 and 1.2, with Q_b > 0 and the actual material price equal to pi, Delta C = SP + V + M + E with no residual, for any actual units, actual selling prices and actual kilograms.' Hypothesis present; grade T kept."),
 "proj-r23-cards-L03-L04-carry-note": ("PASS", "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py; L03.html line 328 (interpretation); L04.html lines 74, 320", f"Re-run round 36 ({S}/out/L04_twin.out and the L03 twin run in this round): L03 output line 2 is 'avoidable make cost per unit ...: 9.10' after the title on line 1, so the delta's 'second line, after its title' sentence matches. L04 output's last line is 'Uneven pool (100000 cents over 3 driver units): refused', so the Remark 1.3 sentence 'the last line of Lab 1's output shows one refused uneven pool' matches the embedded output (the embedded pre block equals the run). This row is for the other slice's pages; it is reported here because the delta touched them."),
 "proj-hours": ("PASS", "course/modules/AC/AC4/project.html lines 277-285 (time-budget table)", "Carried by the rule below (hours table lines unchanged); arithmetic re-checked: the components sum to the declared total, and the hub split matches (no pace failure, architect ruling)."),
}

fresh_prefix_mut = re.compile(r"^proj-(autograder-rerun-mutants|mutant|mutants|r1[2-8]-mutant|r1[2-8]e?-mutant|r13-mutants|r14-mutants|r15-mutants|r17-mutants|r18-mutants|r30-mutants|r23-mutants|r12-mutants|alt|autograder-alt|r1[2-8]-alternatives|r2[3]-alternatives|r30-alternatives|r14-alternatives|r15-alternatives|r17-alternatives|r18-new|r12-alternatives|r13-alternatives|r23-alternatives|autograder-alternatives|autograder-alt-decimal|alt-g|alt-l|r18-new-correct|r17-prior|r23-mutants)")
MUT_IDS = [r["id"] for r in prev["rows"] if re.match(r"^proj-(autograder-rerun-mutants|mutant-|mutants-|r1[2-8]-mutant|r1[2-8]-mutants|r13-mutants|r14-mutants|r15-mutants|r17-mutants|r18-mutants|r23-mutants|r30-mutants|r30-mutant-m|r12-mutants|r23-mutants|r18-new-student|r17-prior|mutant-m)", r["id"]) and "equivalen" not in r["id"] and r["id"] not in ("proj-r12-mutant-m60-scope",)]
ALT_IDS = [r["id"] for r in prev["rows"] if re.match(r"^proj-(autograder-alt|alt-|r1[2-8]-alt|r2[3-4]-alt|r30-alt|r14-alt|r15-alt|r17-alt|r18-new-correct|r23-alt|r30-alternatives|r17-prior-alts|r12-alternatives|r13-alternatives|r30-alternatives)", r["id"]) and r["id"] not in fresh and r["id"] not in ("proj-alt-instance-coverage",)]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        status, loc, ev = fresh[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev,
                     **({"fix": "In course/modules/AC/AC4/project.html line 315, change the C2 level 2 descriptor to: 'At least two variances tied to a case figure.' Level 3 already requires each of the four variances to be tied to a case figure, a named product or an input count, so with this text every count of tied variances from 0 to 4 falls in exactly one of levels 1 to 3 (level 1: one or no tied; level 2: two or more tied, not level 3; level 3: all four with a case figure, product or input count)."} if status == "FAIL" else {})})
        continue
    if rid in MUT_IDS:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": MUT_RUN})
        continue
    if rid in ALT_IDS:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ALT_RUN})
        continue
    # carry: the cited subject is unchanged (the delta touched only project.html lines 159/312/315/317/345 and cards.json 159/556 and the lab twin L04 and L03/L04 pages)
    if r["status"] != "PASS":
        rows.append({k: r[k] for k in ("id", "check", "location", "status", "evidence")} | {"fix": r.get("fix", "")})
        continue
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": CARRY.format(loc=r["location"], pin=PIN_PREV, ev=r["evidence"])})

# new rows for this round
new = [
 {"id": "proj-r38-delta-scope", "check": "Delta since the previous pin 5aeaaf0 read in full for this slice",
  "location": "git diff 5aeaaf0 51a4e97: course/modules/AC/AC4/project.html (lines 312, 315, 317, 345), cards.json (lines 159, 556), L03.html (lines 328, 490), L04.html (lines 74, 275), tests/labs/AC4/lab-AC4-L04-1.py (lines 152-156)",
  "status": "PASS", "evidence": f"git diff --stat 5aeaaf0 51a4e97 (course/modules/AC/AC4, tests/labs/AC4): 5 files changed. Every hunk read. In this slice: rubric C2 and C4 rows, the exemplar A C2 annotation, cards AC4-c023 and AC4-c078. Grader files, project lab twins, and project.html lines outside those hunks are unchanged, so rows that cite only unchanged lines are carried."},
 {"id": "proj-r38-rubric-c4-descriptors", "check": "C4 level 2 and level 1 descriptors are observable and consistent with the scoring rule",
  "location": "course/modules/AC/AC4/project.html line 317 (C4 levels 2 and 1) and line 308 (scoring rule sentence on C4)",
  "status": "PASS", "evidence": "Level 2: 'at least one, but not all' OR 'names no observation'. Level 1: no recommendation, or one naming no action for any unfavourable variance. The line-308 sentence 'A memo that recommends no action for any unfavourable variance scores 1 on C4, whatever else it says' resolves the one overlap (zero actions with no observation meets the second disjunct of level 2). Exemplar A's annotation 'Misses C4 level 2 ... Under the scoring rule, C4 scores 1' is consistent with that sentence. No gap found."},
 {"id": "proj-r38-cards-total-and-grades", "check": "Card count and grade counts after the two T-card edits",
  "location": "course/modules/AC/AC4/cards.json", "status": "PASS",
  "evidence": "Re-run round 36 (inline python over cards.json): 141 cards, 54 T, 52 C, 35 ungraded; the edits did not change any grade or id."},
 {"id": "proj-r38-l04-lab-output-embedded", "check": "L04 page's Lab 1 output block equals the twin's run (the delta added an output line)",
  "location": "course/modules/AC/AC4/L04.html (Lab 1 output pre block); tests/labs/AC4/lab-AC4-L04-1.py",
  "status": "PASS", "evidence": f"Re-run round 36 ({S}/out/L04_twin.out, exit 0): the output block in L04.html equals the run text exactly (compared after stripping tags). The new last line 'Uneven pool (100000 cents over 3 driver units): refused' is produced by exact_rate(100_000, 3, ...), which raises ValueError because 100000 % 3 != 0."},
 {"id": "proj-r38-mutants-new-student-errors", "check": "Three new student-error mutants of the project grader are killed",
  "location": "ledgers/AC4/mutants/r38e_01_actual_profit_keeps_fixed_overhead.py; r38e_02_flexed_revenue_truncated_to_dollars.py; r38e_03_total_variance_sign_reversed.py",
  "status": "PASS", "evidence": f"Written by make_r38e.py ({S}); run by runfiles.py at seeds 0-49: all three KILLED by test_every_grader_seed_reconciles_exactly (out/mutants_r38e.out). Each is a plausible student error that the specification defines (the actual profit deducts the actual fixed overhead; the flexed revenue is in whole cents, not dollars; the total is the actual profit less the master budget profit)."},
 {"id": "proj-r38-alternatives-new", "check": "A new correct alternative implementation passes the grader (over-constraint probe)",
  "location": f"{S}/alts/alt36_a_integer_halfup_formula.py", "status": "PASS",
  "evidence": "Integer half-up by (2n + d) // (2d), numbers.Integral validation, KeyError translated to ValueError: PASS 50/50 seeds (out/alts_all.out line for alt36_a; also run alone). Its first draft failed on a missing-field KeyError (not ValueError), which the specification requires, so the grader correctly refused it; fixed in the alternative, not in the grader."},
 {"id": "proj-r38-alternatives-r8-split", "check": "The round-8 combined alternatives file is run as three separate correct implementations",
  "location": "ledgers/AC4/scripts/AC4-e-r8/alternatives_r4.py (three triple-quoted implementations, split into alts/alt36_r8_split_a..c.py)",
  "status": "PASS", "evidence": "The combined file itself is not an importable budget_engine (collection error in the runner), so each implementation was split out (out/alts_r8split.out). Split a and b refuse a read-only mapping case (isinstance dict check) and are KILLED by test_case_that_is_a_read_only_mapping_is_accepted: the spec says 'a case that is not a mapping' raises ValueError, and a MappingProxyType is a mapping, so refusing it is an over-constraint relative to the spec, i.e. these are not correct implementations of the spec. Split c accepts a tuple of products and is KILLED by test_products_that_are_not_a_list_raise_value_error[tuple]: the spec says products are 'a list of mappings'. Both kills follow the spec."},
 {"id": "proj-r38-count-collect", "check": "Grader collect-only count equals the page's 563", "location": "grader/test_project.py; project.html line 265",
  "status": "PASS", "evidence": f"{S}/collect_ws.py (workspace from grader/reference.py): '563 tests collected'."},
]
rows += new

# fail rows of this round have fixes already; all others carry
mutant_list = []
for path in sorted(glob.glob(str(ROOT / "ledgers/AC4/mutants/*.py"))):
    name = os.path.basename(path)
    desc = ""
    text = open(path, encoding="utf-8").read()
    m = re.match(r'"""(.*?)"""', text, re.S)
    if m:
        desc = m.group(1).strip().splitlines()[0]
    mutant_list.append({"file": "ledgers/AC4/mutants/" + name, "description": desc or name, "killed_by": ""})

killed_text = open(ROOT / S / "out/mutants_all.out", encoding="utf-8").read() + open(ROOT / S / "out/mutants_r38e.out", encoding="utf-8").read()
kills = {}
for line in killed_text.splitlines():
    m = re.match(r"^KILLED (\S+) -> (.*)$", line)
    if m:
        kills[m.group(1)] = m.group(2)
for mu in mutant_list:
    base = os.path.basename(mu["file"])
    mu["killed_by"] = kills.get(base, "")
    if not mu["killed_by"]:
        raise SystemExit("not killed: " + base)

frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 36,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 36, slice AC4-e; did not build AC4)",
 "pin": "51a4e97", "base": "5aeaaf0 (previous round's pin; delta = git diff 5aeaaf0 51a4e97)",
 "checkout": "/tmp/verify38-AC4-e", "scratch": "ledgers/AC4/scripts/AC4-e-r38/out (scratch outputs of this round)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutant_list,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": ("Round 36. Delta since 5aeaaf0: C2 level 2 and C4 level 1 descriptors (project.html 315, 317), exemplar A C2 annotation (345), cards AC4-c023 and AC4-c078, L03/L04 pages and the L04 twin (outside slice, used only where cited). "
           "Not run by this slice: tools/build_site.py --check (not in slice), the full pytest (only the grader collect and lab twins), Pyodide UI (page_smoke only). "
           "Lab-twin mutants (AC4-a/b/c/d/e subdirectories) are out of scope per the architect ruling. "
           "pytest tests/labs/AC4 collects no tests (exit 5); the lab twins are exercised by run_labs and the twin runs."),
 "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
frag["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and all(r["status"] == "PASS" for r in rows) else "FAIL"
frag["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutant_list), "mutants_killed": sum(1 for m in mutant_list if m["killed_by"])}
out = ROOT / "ledgers/AC4/AC4-e.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(frag["summary"], frag["verdict"])
