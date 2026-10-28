"""Build ledgers/CF1/CF1-d.json (round 24) from the round-23 fragment, the round-24 command outputs and the mutant run.

Carried rows keep their round-23 id and PASS status only where the cited subject is byte-identical since the pin
503d139 (the delta in CF1 slice-d files is empty; L01.html lines 90 and 466 and index.html lines 122, 125 and 161 changed
and are cited by the rows listed in REVERIFIED).
"""
import json, pathlib, re, sys
ROOT = pathlib.Path("/tmp/verify24-CF1-d")
S = "ledgers/CF1/scripts/CF1-d-r24"
prev = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-d.round23.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

CARRY = ("Carried from round 23 (course/modules/CF/CF1/project.html, grader/, tests/labs/CF1/, references/ and cards.json "
         "byte-identical since the previous pin 503d139; the CF1 lesson and index changes in 503d139..23cbd6a are L01.html lines "
         "90 and 466 and index.html lines 122, 125 and 161, none cited here): ")
LESSON_CARRY = ("Carried from round 23 (cited subject byte-identical since the previous pin 503d139; the 23cbd6a changes "
                "to L01.html lines 90 and 466 and index.html lines 122, 125 and 161 are not cited by this row): ")
CMD_RE = re.compile(r"^(cmd-|proj-structure|proj-pytest|proj-banned|proj-check-dag|proj-ruff|proj-mypy|proj-page-smoke|"
                    r"proj-verify-refs|proj-grader-reference|proj-collect|proj-test-count-72|proj-hours-table|"
                    r"proj-mutants-|proj-alternatives-)")
RE_VERIFIED = {  # id -> (status, location, evidence) replacing the carried row
    "cards-grade-semantics": ("FAIL", "course/modules/CF/CF1/cards.json entry CF1-c110 (grade and basis); cross-checked against course/modules/CF/CF1/L01.html line 466 and line 446",
        "Round 24 re-read: json load of cards.json gives CF1-c110 grade 'C' with basis 'Assumption 4.0 and Remark 4.3; Problem R3' (cards.json is byte-identical to 503d139, and 23cbd6a changed only L01.html lines 90 and 466 and index.html lines 122, 125 and 161, so the round-23 FAIL is NOT fixed). The card claim, 'the decision can change with the rate that applies (Remark 4.3; Problem R3)', is the claim the lesson grades T at L01.html line 466 (data-grade=\"T\", the row now reads 'the one instance in Problem R3 flips sign between the two rates'). BLUEPRINT section 3: T means proved on the page; L01.html line 446 computes -1 + 1.05/1.06 = -0.009434 and -1 + 1.05/1.03 = +0.019417 (python3 re-computed), a sign flip, so the instance proves the claim. Same claim, two grades: FAIL. Fix (cards.json, owning slice): set CF1-c110 grade to \"T\" and basis to \"Problem R3, values on L01.html line 446\"; or, if the builder prefers, grade the lesson row C and keep the card C, but the two must agree."),
    "index-ladder-rung1-worked-example": ("PASS", "course/modules/CF/CF1/index.html lines 121-126 (rung 1 and rung 2 skill checks, changed in 23cbd6a at lines 122 and 125)",
        "Round 24 recomputed: rung 1 is 400 x 0.75 + 0.25 x 300 = 375 (data-answer 375, tolerance 0.001 on line 121; explain line 123); rung 2 is 0.25 x 300 = 75 (data-answer 75, line 126). The 23cbd6a wording now defines EBITDA as 'revenue less cash operating cost' and the shield as 'the tax saved by the depreciation deduction', matching project.html line 197 (EBITDA = revenue less cash cost) and line 199 (depreciation tax shield). index.html line 151 (ladder rung 1) unchanged in the delta. PASS."),
    "index-ladder-rung1-worked-example-r18": ("PASS", "course/modules/CF/CF1/index.html lines 121-126 and line 151",
        "Round 24: same recomputation as index-ladder-rung1-worked-example (375 and 75); index.html line 151 unchanged since 503d139. PASS."),
    "proj-structure-and-gates": ("PASS", "tools/check_pages.py --unit CF1; tools/check_dag.py --all; tools/check_projects.py --all",
        f"Round 24 re-run on 23cbd6a: {S}/out/check_pages.out 'check_pages CF1: PASS' exit 0; check_dag.out 'check_dag CF1: PASS' exit 0 (check_dag --all also PASS for AC4 and AP1); check_projects.out 'check_projects CF1: PASS' exit 0 (AC4 and AP1 PASS)."),
    "proj-pytest-lab-helper": ("PASS", "tests/labs/CF1/lab-CF1-project-1.py, -2.py, -3.py; tests/test_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_docs_figures.py tests/test_curriculum.py; tools/run_labs.py --unit CF1",
        f"Round 24 re-run: python -I -W error on each project twin exits 0 (project-1 and project-3 print their output; project-2 is the completed twin and exits 0); run_labs.out 'run_labs CF1: PASS (9/9)' exit 0; pytest.out '-q' shows only dots, exit 0 under python -I -W error."),
    "proj-banned-phrases": ("PASS", "course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json",
        f"Round 24: grep -n -i -E 'roughly half|about 6%|historically|\\.\\.\\.|…' over both files: no match. Word-boundary scan (grep -n -w -i -E 'round|builder|verifier|unit report'): only project.html lines 339 and 340, where 'round(r, 6)' is the Python function in Lab 3; no process word in learner text. The substring 'rounded' (project.html line 201) and 'rounding' (line 433) are ordinary words. Output in {S}/out/banned.out."),
    "proj-check-dag": ("PASS", "tools/check_dag.py --all", "Round 24: check_dag CF1 PASS, exit 0 (out/check_dag.out)."),
    "proj-ruff-format": ("PASS", "ruff check . and ruff format --check .", "Round 24: ruff check exit 0; ruff format --check '220 files already formatted' exit 0 (out/ruff.out)."),
    "proj-mypy-grader-gate": ("PASS", "mypy --no-incremental (strict)", "Round 24: 'Success: no issues found in 153 source files' exit 0 (out/mypy.out)."),
    "proj-page-smoke": ("PASS", "tools/page_smoke.py --unit CF1", "Round 24: page_smoke CF1 PASS; modules/CF/CF1/project.html PASS; in-browser grader 'All 157 tests pass' on lab seed run (out/page_smoke.out, exit 0)."),
    "proj-verify-refs": ("PASS", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1 (live)",
        "Round 24: offline integrity '560 entries, 0 problems' exit 0; live re-verification of CF1 '2 of 560 entries, 0 problems' exit 0 (out/verify_refs_offline.out, out/verify_refs_live_unit.out). The registry flags (glasserman2003monte, damodaran2012investment) are carried."),
    "proj-grader-reference-50-seeds": ("PASS", "tools/run_graders.py --all --seeds 0-49", "Round 24: run_graders CF1 PASS (reference 50/50 seeds, slowest 0.3 s) (out/run_graders.out, exit 0)."),
    "proj-collect-count-50-seeds": ("PASS", "pytest --collect-only on the reference copy, QF_SEED 0-10 and 49", "Round 24: 157 tests collected on each of seeds 0-10 and 49 (out/collect_r24.out; script collect_seeds.sh)."),
    "proj-test-count-72": ("PASS", "course/modules/CF/CF1/project.html line 192; grader/test_project.py", "Round 24: project.html line 192 says 'collects 157 checks'; collect-only on 12 seeds gives 157 (out/collect_r24.out). Carried subject byte-identical."),
    "proj-hours-table": ("PASS", "course/modules/CF/CF1/project.html lines 216-230 and data-hours-project (line 33)",
        "Round 24 re-read: the time-budget cells are 1, 1, 4, 2, 1, 1, 2; sum 12 = data-hours-project=12 on line 33. Hours are design targets (architect ruling); the only arithmetic check is against the hub split, see r24-hours-arithmetic."),
    "proj-mutants-r23-new": ("PASS", "ledgers/CF1/mutants/r23d_01..03 (committed in 503d139)", "Carried from round 23: the three round-23 mutants are among the 227 top-level mutants re-run in round 24; each KILLED (see proj-mutants-full-run-r24)."),
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE_VERIFIED:
        st, loc, ev = RE_VERIFIED[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"unexpected non-PASS carried row {rid}")
    pre = LESSON_CARRY if any(k in r["location"] + r["evidence"] for k in ("L01.html", "index.html")) else CARRY
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": pre + r["evidence"]})
new = [
 ("r24-delta-coverage", "2.9 / delta: round-23 pin 503d139 to pin 23cbd6a, CF1 slice d",
  "git diff --stat 503d139 23cbd6a -- course/modules/CF/CF1/project.html cards.json grader tests/labs/CF1 references: empty. CF1 files changed: L01.html (lines 90 and 466) and index.html (lines 122, 125, 161); all re-read in this round. The 11 mutants r24d_01..11 were committed by 23cbd6a and are re-run.",
  "PASS", "git diff --stat 503d139 23cbd6a (CF1 paths); course/modules/CF/CF1/L01.html line 90, 466; index.html 122, 125, 161"),
 ("r24-l01-line-90-remark-2-2", "2.4 / 2.7: Remark 2.2 wording and card CF1-c004",
  "The 23cbd6a sentence says Lab 1, Part C checks 'that the NPV of a bundle of projects that share one rate is the sum of their NPVs'. tests/labs/CF1/lab-CF1-L01-1.py lines 84-95 (Part C) sum two projects' flows and compare npv_dollars(combined, RATE) with the sum of the two NPVs at the same RATE, 50 seeded pairs, and print 'additivity holds to within 1e-6 dollars'. The claim matches. Card CF1-c004 (T) says 'With different rates the sum mixes two prices of time (Remark 2.2)', which matches the remark's first and second sentences.",
  "PASS", "course/modules/CF/CF1/L01.html line 90; tests/labs/CF1/lab-CF1-L01-1.py lines 84-95; cards.json CF1-c004"),
 ("r24-l01-line-466-r3-basis", "2.2 / 2.4: R3 instance behind the T row",
  "L01.html line 446 values -1 + 1.05/1.06 = -0.009434 and -1 + 1.05/1.03 = +0.019417 (python3 re-computed, not copied) flip sign, so 'the one instance in Problem R3 flips sign between the two rates' is proved on the page: T. The card that restates the same claim is CF1-c110 (see cards-grade-semantics, FAIL).",
  "PASS", "course/modules/CF/CF1/L01.html lines 446 and 466"),
 ("r24-index-skill-check-wording", "2.9 / index: rung 1 and rung 2 skill-check definitions",
  "index.html line 122 defines EBITDA as 'revenue less cash operating cost' and line 125 defines the tax shield as 'the tax saved by the depreciation deduction'; project.html line 197 (EBITDA is revenue less cash cost) and line 199 (the depreciation tax shield) agree, and the answers 375 and 75 recompute (400 x 0.75 + 0.25 x 300; 0.25 x 300).",
  "PASS", "course/modules/CF/CF1/index.html lines 122, 125, 121, 126; course/modules/CF/CF1/project.html lines 197, 199"),
 ("r24-mutants-full-run", "2.5 / grader mutation: all top-level mutants re-run on seeds 0-9",
  "227 top-level .py files in ledgers/CF1/mutants/ (the 211 earlier, the 11 r24d committed by 23cbd6a, and the 5 new v24d): 227 KILLED, 0 SURVIVED (out/mutate_r24_all.out, out/mutate_v24d_new.out). Each KILLED line names the first failing test.",
  "PASS", "ledgers/CF1/mutants/*.py; ledgers/CF1/scripts/CF1-d-r24/run_mut_one.sh; out/mutate_r24_all.out"),
 ("r24-mutants-new-five", "2.5 / grader mutation: five new student-error mutants",
  "v24d_01 last-year working capital not recovered: KILLED (test_working_capital_investment_and_recovery_sum_to_zero, seed 0). v24d_02 Monte Carlo fresh generator each draw: KILLED (test_monte_carlo_draws_follow_the_seeded_gauss_stream). v24d_03 normalvariate instead of gauss: KILLED (same test). v24d_04 IRR root at the left grid point with no bisection: KILLED (test_irr_finds_both_roots_of_a_two_sign_change_flow). v24d_05 NPV discounts every flow one period late: KILLED (test_npv_keeps_a_leading_zero_flow_in_its_time_index). A first v24d_04 (reporting lo after bisection) was discarded: bisection stops when hi - lo <= 1e-15 hi, so lo equals the root and that version is equivalent to the reference, not a mutant. Each mutant is a single edit of reference.py asserted to match once (make_mutants24.py).",
  "PASS", "ledgers/CF1/mutants/v24d_01..05; ledgers/CF1/scripts/CF1-d-r24/make_mutants24.py; out/mutate_v24d_new.out"),
 ("r24-alternatives-three-new", "2.5 / over-constraint: three new correct engines pass on seeds 0-9",
  "r24_a finer grid of 8001 points, bisection to 1e-14 (same window, same conventions): PASS 10 seeds. r24_b NPV by Horner's rule on x = 1/(1+r), Fisher by expm1/log1p: PASS 10 seeds. r24_c payback via itertools.accumulate and an IRR grid spaced by 10 ** (-4 + 8k/4000): PASS 10 seeds (out/alts_r24_new.out).",
  "PASS", "ledgers/CF1/scripts/CF1-d-r24/alts/r24_a..c; out/alts_r24_new.out"),
 ("r24-alternatives-all-unique", "2.5 / over-constraint: every unique alternative of all rounds",
  "68 alternative files (CF1-d-r*/alts and r*/e/alts) hold 49 unique contents; all 49 PASS on seeds 0-9 with the suite copied from grader/ (out/alts_r24_all.out, run_alts24.py).",
  "PASS", "ledgers/CF1/scripts/CF1-d-r*/alts/*.py; out/alts_r24_all.out"),
 ("r24-collect-157", "2.9 / test count", "pytest --collect-only: 157 tests on seeds 0-10 and 49 (out/collect_r24.out). Page line 192 says 157.", "PASS", "course/modules/CF/CF1/project.html line 192; grader/test_project.py"),
 ("r24-run-graders-50", "2.5 / grader on seeds 0-49", "run_graders --all --seeds 0-49: CF1 reference 50/50 seeds PASS (out/run_graders.out).", "PASS", "tools/run_graders.py; out/run_graders.out"),
 ("r24-gates", "gates: checkers, labs, twins, ruff, mypy, pytest",
  "check_pages CF1 PASS; check_dag --all PASS (CF1, AC4, AP1); check_projects --all PASS; run_labs CF1 9/9 PASS; page_smoke CF1 PASS; ruff check and format clean; mypy strict 153 files clean; pytest -q of test_labs, test_page_checks, test_refs, test_docs_figures, test_curriculum: exit 0 under python -I -W error. Output files in out/.",
  "PASS", "out/check_pages.out, check_dag.out, check_projects.out, run_labs.out, page_smoke.out, ruff.out, mypy.out, pytest.out"),
 ("r24-twins-isolated", "2.5 / labs: project twins under python -I -W error",
  "lab-CF1-project-1.py, -2.py, -3.py each exit 0 when run alone with python -I -W error. Each lab's printed output matches its embedded expected block (run_labs 9/9).",
  "PASS", "tests/labs/CF1/lab-CF1-project-1..3.py"),
 ("r24-hours-arithmetic", "2.9 / hours: hub split against project budget",
  "index.html lines 29-41 unchanged in the delta; hub split 48 lesson + 12 project = 60 (as the project's line 229 states); project budget 1+1+4+2+1+1+2 = 12. No arithmetic inconsistency. Hours are not re-estimated (architect ruling).",
  "PASS", "course/modules/CF/CF1/project.html lines 216-230, 33, 229; course/modules/CF/CF1/index.html lines 29-41"),
 ("r24-verify-refs", "2.1 citations: registry offline and live for CF1", "verify_refs --offline: 560 entries, 0 problems; verify_refs --unit CF1 (live): 2 of 560 entries re-verified, 0 problems. Registry flags carried (see registry_flags).", "PASS", "tools/verify_refs.py; out/verify_refs_offline.out, out/verify_refs_live_unit.out"),
 ("r24-banned-process-scan", "2.9: banned phrases and process words, round 24", "Banned phrase regex and word-boundary process-word scan on project.html and cards.json: only the Python round() calls on project.html lines 339-340 match the word-boundary scan.", "PASS", "course/modules/CF/CF1/project.html; cards.json; out/banned.out"),
]
rows += [{"id": a, "check": b, "location": d, "status": c, "evidence": e} for a, b, e, c, d in new]
rows.append({"id": "r24-cards-count-and-fields", "check": "2.7 cards: count, fields, grades, uniqueness",
  "location": "course/modules/CF/CF1/cards.json",
  "status": "PASS",
  "evidence": "110 entries; every entry has id, lesson, front, back, grade, basis (cite on the Glasserman/Graham entries); ids unique (110); fronts unique (110); grades 59 T and 51 C (python3 Counter). The only failing card is CF1-c110 (cards-grade-semantics)."})
mutants = []
for line in (ROOT / S / "out/mutate_r24_all.out").read_text().splitlines():
    pass
killed = {}
for path in ["out/mutate_r24_all.out", "out/mutate_v24d_new.out", "out/mutate_v24d_01_03_05.out"]:
    for line in (ROOT / S / path).read_text().splitlines():
        m = re.match(r"KILLED (\S+) seed (\d+): FAILED (\S+)", line)
        if m:
            killed[m.group(1)] = f"{m.group(3)} (seed {m.group(2)})"
        elif line.startswith("SURVIVED"):
            raise SystemExit(line)
for f in sorted((ROOT / "ledgers/CF1/mutants").glob("*.py")):
    text = f.read_text(encoding="utf-8")
    doc = text.split('"""')[1].strip().splitlines()[0]
    mutants.append({"file": f"ledgers/CF1/mutants/{f.name}", "description": doc, "killed_by": killed[f.name]})
rows.append({"id": "r24-mutants-count", "check": "2.5 / grading mutation: count of mutants in the ledger",
  "location": "ledgers/CF1/mutants/*.py", "status": "PASS",
  "evidence": f"{len(mutants)} top-level mutant files, each listed in mutants with its killing test: 227 of 227 KILLED."})
frag = {
 "unit": "CF1", "slice": "CF1-d", "round": 24,
 "verifier": "independent verifier (Haiku), round 24 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
 "pin": "23cbd6a (detached, /tmp/verify24-CF1-d)",
 "base": "503d139 (round-23 pin; delta with git diff --stat 503d139 23cbd6a: no change in the slice files; L01.html and index.html changed)",
 "checkout": "/tmp/verify24-CF1-d",
 "scratch": "/tmp/CF1-v/d24",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": "Round 24 delta for this slice: none in project.html, cards.json, grader/, tests/labs/CF1/, references. The round-23 FAIL (CF1-c110 grade C against lesson grade T) is NOT fixed by 23cbd6a: cards.json is unchanged. 23cbd6a changed L01.html lines 90 and 466 and index.html lines 122, 125, 161. Re-run in this round: check_pages, check_dag, check_projects, run_labs, run_graders 0-49 (CF1 50/50), page_smoke, ruff, mypy, pytest (five files), the three project twins, verify_refs offline and live for CF1, collect-only on 12 seeds, all 227 mutants, all 49 unique alternatives. Five new mutants (v24d_01..05) and three new alternatives (r24_a..c) were written this round. Not re-run: the historical command rows of rounds 13 to 22 (carried by prefix); the live-web reads of external sources (none cited by the changed rows).",
 "summary": f"CF1-d round 24 (pin 23cbd6a): {len(rows)} rows; {sum(1 for r in rows if r['status']=='FAIL')} FAIL: cards-grade-semantics (CF1-c110 graded C while the same claim is graded T at L01.html line 466; fix: set CF1-c110 grade to T with basis 'Problem R3, values on L01.html line 446'). Mutants 227 of 227 killed (5 new). Alternatives 49 of 49 unique pass (3 new). Collect 157. Gates PASS.",
}
out = ROOT / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "verdict", frag["verdict"])
print("validate:", ledger.validate(json.loads(out.read_text(encoding="utf-8")), "CF1-d"))
