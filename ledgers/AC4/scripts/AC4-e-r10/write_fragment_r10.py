"""Write the round-10 AC4-e fragment: carried rows (cited subject byte-identical), fresh rows, mutants with killed_by."""
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verify10-AC4-e")
R9 = json.loads(Path("/tmp/fanout-frags/AC4-e.round9.json").read_text(encoding="utf-8"))
R9_ROWS = {r["id"]: r for r in R9["rows"]}
R9_MUT = {m["id"]: m for m in R9["mutants"]}
S = "ledgers/AC4/scripts/AC4-e-r10/"
RUN = f"ledgers/AC4/scripts/AC4-e-r10/run_mutants.py on ledgers/AC4/mutants (seeds 0,1,25): {{}}"

# killed_by from the round-10 run (first FAILED test on seed 0)
killed = {}
cur = None
for line in Path("/tmp/ac4-v/e10/mutants_r10_all50.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith("KILLED") or line.startswith("SURVIVED"):
        cur = line.split()[-1]
    elif cur and "seed 0 " in line and "FAILED" in line:
        m = re.search(r"FAILED test_project\.py::(\S+)", line)
        killed[cur] = m.group(1) if m else line.strip()[-80:]
        cur = None
mut_files = sorted(p.name for p in (ROOT / "ledgers/AC4/mutants").glob("m*.py"))
assert len(mut_files) == 50 and all(f in killed for f in mut_files), (len(mut_files), len(killed))

RUN_ALL = "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/run_mutants.py /tmp/verify10-AC4-e /tmp/ac4-v/e10/mut 0,1,25 -> 50 KILLED, 0 SURVIVED (/tmp/ac4-v/e10/mutants_r10_all50.txt)"


def carry(rid, desc):
    r = R9_ROWS[rid]
    return dict(id=rid, check=r["check"], location=r["location"], status="PASS",
                evidence=f"Carried from round 9 ({desc} byte-identical since the previous pin): " + r["evidence"])


def fresh(rid, evidence, status="PASS", fix=None):
    r = R9_ROWS.get(rid, {})
    row = dict(id=rid, check=r.get("check", rid), location=r.get("location", ""), status=status, evidence=evidence)
    if fix:
        row["fix"] = fix
    return row


rows = []
# ---- fresh command and re-derivation rows
rows.append(fresh("proj-autograder-reference",
    "Re-run round 10: tools/run_graders.py --unit AC4 --seeds 0-49 -> 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.2 s)' "
    "(/tmp/ac4-v/e10/grade_ref.txt); pytest on the reference, seeds 0/1/25/1974022705 -> '296 passed'."))
rows.append(fresh("proj-collect-count",
    "Re-run round 10: pytest --collect-only -q on grader/test_project.py with QF_SEED 0, 1, 25, 1974022705 -> '296 tests collected' "
    "each time; page line 265 says 296 checks."))
rows.append(fresh("proj-autograder-alternatives",
    "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/run_alts.py on ledgers/AC4/scripts/AC4-e-r9/alt_a..alt_k.py, alternatives_r4.py's "
    "generated alt_a/alt_b/alt_c (/tmp/ac4-v/e10/alts_r4/) and the new alt_l (ledgers/AC4/scripts/AC4-e-r10/alt_l.py, reference plus "
    "extra informational keys in master_budget and flexible_budget) -> every alternative 'PASS all 296 passed' on seeds 0-9 and 25. "
    "alternatives_r4.py itself is a generator that writes alt_a..c, not a solution: its own run reported '1 error' (not an alternative)."))
rows.append(fresh("proj-alt-l-extra-keys",
    "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/make_alt_r10.py writes alt_l.py; run_alts.py -> 'alt_l.py PASS all 296 passed'. "
    "The specification's 'returns a dictionary with the keys' is not exclusive; the only exact-key assertion found by grep is "
    "variance_decomposition (test_project.py line 120)."))
rows.append(fresh("proj-autograder-alt-decimal",
    "Re-run round 10: run_alts.py on ledgers/AC4/scripts/AC4-e-r9/alt_k.py (Decimal half-up rounding) -> 'PASS all 296 passed'."))
rows.append(fresh("proj-autograder-rerun-mutants-m01-m37",
    RUN_ALL + "; every m01-m37 KILLED with its first failing test in mutants_r10_all50.txt."))
for rid, label in [
    ("proj-mutants-m01-m06", "m01-m06"), ("proj-mutant-m07-empty-name", "m07"), ("proj-mutants-m08-m11", "m08-m11"),
    ("proj-mutant-m12-duplicate-names", "m12"), ("proj-mutants-m13-m20", "m13-m20"), ("proj-mutants-m15-m19", "m15-m19"),
    ("proj-mutants-m21-m24", "m21-m24"), ("proj-mutants-m21-m24-equivalence", "m21-m24 (each KILLED, so none is equivalent)"),
    ("proj-mutants-m25-m29", "m25-m29"), ("proj-mutants-r6-new", "m30-m34"), ("proj-mutants-r7-new", "m35-m37"),
    ("proj-mutants-r8-new", "m38-m40"), ("proj-mutants-r9-new", "m41-m46")]:
    rows.append(fresh(rid, RUN_ALL + "; " + label + " all KILLED (killed_by in this fragment's mutants list)."))
rows.append(fresh("proj-mutants-r10-new",
    "Re-run round 10 (new, my own student-error mutants on the reference): m47_mix_omits_fixed_overhead.py (mix line deducts no "
    "fixed overhead), m48_efficiency_against_budgeted_output.py (efficiency standard on budgeted units), m49_exact_halves_round_down.py "
    "(exact half cent rounds down), m50_flexed_units_is_budget_total.py (flexible_budget units field is the budget total). Each KILLED "
    "on seeds 0, 1, 25 (mutants_r10_all50.txt). Each is a plausible student error that the specification defines against: the mix "
    "variance and reconciliation (project.html Conventions), efficiency standard for the actual output (Conventions), halves up (Conventions), "
    "and units equal to the actual total (grader line 260; the flexed budget 'in total', project.html Required outputs)."))
rows.append(fresh("proj-mutant-descriptions",
    "Re-run round 10: ast.get_docstring over all 50 ledgers/AC4/mutants/m*.py files -> no file without a docstring; each docstring names its error "
    "(m47-m50 written by ledgers/AC4/scripts/AC4-e-r10/make_mutants_r10.py)."))
rows.append(fresh("proj-check-pages",
    "Re-run round 10: .venv/bin/python tools/check_pages.py --all -> 'check_pages AC4: PASS' (exit 0)."))
rows.append(fresh("proj-check-dag",
    "Re-run round 10: .venv/bin/python tools/check_dag.py --all -> 'check_dag AC4: PASS' (exit 0)."))
rows.append(fresh("proj-check-projects",
    "Re-run round 10: .venv/bin/python tools/check_projects.py --all -> 'check_projects AC4: PASS' (exit 0)."))
rows.append(fresh("proj-page-smoke",
    "Re-run round 10: .venv/bin/python tools/page_smoke.py --unit AC4 --pages project -> 'page_smoke AC4: PASS' and "
    "'in-browser grader: All 296 tests pass on seed 1974022705 (0.9 s)' (/tmp/ac4-v/e10/smoke.txt); lab-AC4-project-1 and -2 under 0.1 s."))
rows.append(fresh("proj-ruff-mypy",
    "Re-run round 10: .venv/bin/ruff check course/modules/AC/AC4/grader tests/labs/AC4 -> 'All checks passed!'; ruff format --check -> "
    "'14 files already formatted'; .venv/bin/mypy --no-incremental (repository configuration) -> 'Success: no issues found in 153 source files'. "
    "(An explicit file list run without the repository configuration reports import-not-found for budget_engine and instance; not a finding.)"))
rows.append(fresh("proj-run-labs-ac4",
    "Re-run round 10: .venv/bin/python tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)' (/tmp/ac4-v/e10/labs.txt); "
    ".venv/bin/pytest tests/test_labs.py tests/test_run_labs.py -k AC4 -> 10 passed."))
rows.append(fresh("proj-banned-phrases",
    "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/scan_r10.py (banned regex over project.html text and cards.json front/back) -> 'banned hits: []'; "
    "the memo word counts are in proj-memo-structure-length."))
rows.append(fresh("proj-memo-structure-length",
    "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/scan_r10.py counts the memo-text words of each exemplar: exemplar-a 321 words, "
    "exemplar-b 412 words (body, headings included; both inside 300-600). Headings: A has Result, Causes, Recommendation (no Assumptions); "
    "B has Result, Causes, Assumptions, Recommendation (project.html lines 330-369)."))
rows.append(fresh("proj-hours",
    "Re-run round 10: lesson declared hours data-hours L01..L08 = 6,7,6,6,7,6,6,6 (sum 50; hub index.html data-hours-lessons=\"50\"); "
    "project table lines 277-285 sum 1+2+2+6+4+2+2+1 = 20 (= data-hours-project=\"20\"); 50+20 = 70 (hub eyebrow '70 hours'). "
    "The per-component split is a design target (architect ruling), not checked against pace."))
rows.append(fresh("proj-exemplar-intro-universal-claim",
    "Round 9 FAIL re-verified from scratch against the new line 324: 'Every figure they state is either derived from those figures or "
    "labelled as a what-if, except the sign of Exemplar A's sales mix figure, which its annotation marks as wrong.' Scan of every "
    "number in both memo-text blocks (ledgers/AC4/scripts/AC4-e-r10/memo_numbers.py): Exemplar A states 220,000 (lab step 7), +542,857 "
    "(lab step 4), 1,500 and 1,400 units (case), +180,000 (lab step 3), 5,000 and 9,000 (case budget prices), +462,857 (lab step 6 "
    "magnitude; the lab prints -462,857, so the sign is the exception and annotation C1/C2 says 'mix sign is also wrong'). Exemplar B: "
    "2,820,000 (2,600,000 + 220,000), 3,142,857 (lab step 2), 71.4/80.0/28.6/20.0% and unit counts (case), 4,400 and 8,000 (case "
    "margins), +240,000, -60,000, 40,000, 5,100, 5,300, 5,000,000 (case), 53,000 and 167,000 (labelled 'If the actual input price were "
    "210 cents'), 5,400 (derived threshold, 5,400 - 1,000 = 4,400). Every one is derived or labelled; the exception is exactly the one "
    "the sentence names. Claim now holds."))
rows.append(fresh("proj-exemplar-overall-level",
    "Re-run round 10 on the changed intro (line 324, 'with overall levels 1 and 3'): data-scores A '2,2,2,1,2' -> min 1 (data-level=1); "
    "B '4,4,3,4,4' -> min 3 (data-level=3); both match the intro."))
rows.append(fresh("proj-cards-structure",
    "Re-run round 10: ledgers/AC4/scripts/AC4-e-r10/card_scan.py course/modules/AC/AC4/cards.json -> 128 cards (was 119); ids "
    "AC4-c001..AC4-c128 sequential; no structure problems; lesson counts L01 17, L02 19, L03 18, L04 15, L05 10, L06 16, L07 16, L08 17 "
    "(sum 128); T 47, C 48, ungraded 33; every C card has a basis, no T card has one (python check in this round)."))
rows.append(fresh("proj-cards-duplicates",
    "Re-run round 10: card_scan.py -> 'duplicate fronts: []', 'duplicate backs: []'. Near-duplicate fronts (difflib >= 0.75): "
    "c115/c116 (residual income vs EVA, different measures), c070/c071/c072/c073 (different variances), c079/c112, c059/c060, c073/c074, "
    "c045/c121 ('Define a cost pool' vs 'Define a cost driver'), c003/c111 (different concepts): all distinct questions. Not duplicates."))
rows.append(fresh("proj-cards-sample",
    "Re-run round 10: sampled cards c010, c020, c030, c040, c050, c060, c070, c080 read against their lessons. c040 changed in this round "
    "(In Lab 1, how much cheaper is making than buying, per year?); its back 'Making is cheaper by 25,000.00 CU a year.' matches L03 lab output "
    "line 'relevant difference (make minus buy): -25,000.00'. The others are byte-identical since the previous pin; see the carried rows."))
rows.append(fresh("proj-cards-r10-L01",
    "Changed/added L01 cards read against L01.html: AC4-c003 (Def 2.1, line 88), AC4-c012 (Prop 3.2 'passes through (Q_H,C_H) and (Q_L,C_L)', line 119), "
    "AC4-c014 (lab output 'largest absolute residual_cents 51473' = 514.73 USD; interpretation 'off by up to 514.73 USD'), "
    "AC4-c120 (Def 2.1: 'The contribution margin ratio is m/p, the share of each sales dollar that is left to cover fixed cost'), "
    "AC4-c127 (Prop 3.2: 'v-hat is the only slope that does so', line 119), AC4-c128 ('10 of the 12 months', lab output line 'months with nonzero residual 10 of 12'). "
    "Grades and bases consistent: T cards need no basis; C cards cite 'Lab 1 (SIMULATED)'."))
rows.append(fresh("proj-cards-r10-L02",
    "Changed/added L02 cards read against L02.html: AC4-c029 (lab output 'loss run units 0 to 88' and 'loss run units 2001 to 2088', line 256-257; "
    "interpretation line 264), AC4-c125 ('single_formula_break_even_units 88.89 first_whole_unit 89', line 252; 'The first profitable whole volume is 89 units' in the table row)."))
rows.append(fresh("proj-cards-r10-L03",
    "Changed/added L03 cards read against L03.html and its lab output: AC4-c038 (Prop 2.2, line 95 'Q(m+l+v-p)+F+S'; line 90 'Making is cheaper when Delta<0'), "
    "AC4-c040 (lab output 'relevant difference (make minus buy): -25,000.00'), AC4-c042 (lab 'change in firm profit from dropping: -2,000.00', 'keep-or-drop decision: keep'), "
    "AC4-c043 (lab 'net effect of accepting: 5,000.00', 'decision: accept'), AC4-c122 (line 95: 'book value B ... enters neither expression'), "
    "AC4-c123 (Example 3.1, line 334; line 389 gives -3,000 and -1,000, the change 2,000.00), AC4-c124 (lab 'naive per-hour comparison: order earns 2.50, D earns 5.00 per hour', "
    "'naive decision: reject'; Proposition 4.1 line 348-349)."))
rows.append(fresh("proj-card-c126-basis",
    "AC4-c126 back ('Buy. The full-cost method compares 11.10 per unit with the 10.50 buy price.') matches the lab output (full make cost 11.10, buy price 10.50, "
    "full-cost decision buy). Its basis field, however, is copied from the make-minus-buy row of L03 (line 512), and says 'the identity in Proposition 2.2 gives the same "
    "figure'. Proposition 2.2 (line 90, 95) is the relevant-cost identity Delta = Q(m+l+v-p)+F+S; it does not produce 11.10, 10.50 or the full-cost decision. "
    "The attribution is wrong for this card (cards.json line for AC4-c126, basis).",
    status="FAIL",
    fix="In course/modules/AC/AC4/cards.json, AC4-c126 basis: replace with 'Lab 1 (SIMULATED), make-or-buy lines (full-cost comparison, 11.10 per unit against 10.50)'. "
        "The basis must cite the lab output, not Proposition 2.2. Builder rules: edit the card, do not weaken the attribution check."))
rows.append(fresh("proj-cards-r10-L04",
    "Changed/added L04 cards read against L04.html line 55: AC4-c045 ('A cost pool is a group of overhead costs that share one cause'), "
    "AC4-c121 ('a cost driver is the measured quantity by whose count the pool's cost is assigned, such as the number of setups or the number of inspections')."))
rows.append(fresh("proj-cards-changed-lessons-r10",
    "The round-9 changed-lesson check for L05/L06 cards (AC4-c059..c068, L06 cards) is carried; the round-10 changes are only L01-L04 and "
    "the appended c120-c128, all checked in the proj-cards-r10-* rows."))

# ---- carried rows (cited subject byte-identical)
carry_specs = {
    "proj-instances": "course/modules/AC/AC4/grader/instance.py",
    "proj-alt-instance-coverage": "course/modules/AC/AC4/grader/instance.py and grader/starter.py",
    "proj-spec-empty-name-claim": "course/modules/AC/AC4/project.html line 263 (Constraints) and grader/test_project.py",
    "proj-spec-fresh-objects-claim": "course/modules/AC/AC4/project.html line 263 and grader/test_project.py",
    "proj-spec-clarity-and-errors": "course/modules/AC/AC4/project.html line 263 (Constraints) and grader/test_project.py",
    "proj-messages-no-leak": "course/modules/AC/AC4/grader/test_project.py",
    "proj-rubric-exhaustive": "course/modules/AC/AC4/project.html lines 314-318",
    "proj-rubric-scoring-rule": "course/modules/AC/AC4/project.html line 308",
    "proj-rubric-C4-observation": "course/modules/AC/AC4/project.html lines 306, 316, 373",
    "proj-rubric-C2-terms": "course/modules/AC/AC4/project.html lines 308 and 315",
    "proj-calib-A-scores": "course/modules/AC/AC4/project.html line 326 (exemplar A data-scores) and its memo lines",
    "proj-calib-A-annotation": "course/modules/AC/AC4/project.html lines 343-351",
    "proj-calib-B-scores": "course/modules/AC/AC4/project.html line 357 (exemplar B data-scores)",
    "proj-calib-B-annotation": "course/modules/AC/AC4/project.html lines 377-382",
    "proj-exemplar-B-consequences": "course/modules/AC/AC4/project.html line 370",
    "proj-exemplar-B-threshold": "course/modules/AC/AC4/project.html line 373",
    "proj-exemplar-B-verdict": "course/modules/AC/AC4/project.html line 359",
    "proj-reading-list-sentence": "course/modules/AC/AC4/project.html line 267 (the dt is line 266)",
    "proj-ladder-lede": "course/modules/AC/AC4/project.html line 42",
    "proj-simulated-and-data": "course/modules/AC/AC4/project.html lines 53-56 and 252, and tests/labs/AC4",
    "proj-equal-margin-branch": "course/modules/AC/AC4/grader/test_project.py lines 463-480",
    "proj-grader-equal-margin-comment": "course/modules/AC/AC4/grader/test_project.py lines 472-474",
    "proj-citations-reading": "course/modules/AC/AC4/project.html reading list and references/references.json",
    "proj-spec-coverage-claims": "course/modules/AC/AC4/project.html line 265 and grader/test_project.py",
    "proj-stretch-two-inputs": "course/modules/AC/AC4/project.html line 399",
    "proj-stretch-spending": "course/modules/AC/AC4/project.html line 398",
    "proj-stretch-list-intact": "course/modules/AC/AC4/project.html lines 396-401",
    "proj-lab-1": "course/modules/AC/AC4/project.html lines 53-147 and tests/labs/AC4/lab-AC4-project-1",
    "proj-lab-1-interpretation": "course/modules/AC/AC4/project.html line 146",
    "proj-lab-2": "course/modules/AC/AC4/project.html lines 149-243",
    "proj-purity-order-dependence": "course/modules/AC/AC4/grader/test_project.py",
    "proj-card-c020": "course/modules/AC/AC4/cards.json lines 134-138 (AC4-c020)",
    "proj-card-c078": "course/modules/AC/AC4/cards.json lines 553-557 (AC4-c078)",
    "proj-card-c091": "course/modules/AC/AC4/cards.json line 641 (AC4-c091)",
    "proj-card-c061": "course/modules/AC/AC4/cards.json line 436 (AC4-c061)",
    "proj-cards-targeted": "course/modules/AC/AC4/cards.json cards AC4-c062, c063, c064, c066, c067, c075, c076",
    "proj-cards-number-format": "course/modules/AC/AC4/cards.json cards AC4-c101, c102, c109",
    "proj-cards-changed-lessons": "course/modules/AC/AC4/cards.json cards AC4-c059..c068 and the L06 cards",
    "proj-inputs-every-number-int": "course/modules/AC/AC4/project.html lines 252 and 260",
    "proj-stretch-two-inputs-scope": "course/modules/AC/AC4/project.html line 399",
    "proj-grader-comments": "course/modules/AC/AC4/grader/test_project.py lines 43-44",
    "proj-conventions-no-spending-claim": "course/modules/AC/AC4/project.html line 260 (Conventions, fourth paragraph)",
    "proj-lab-1-interpretation-second-clause": "course/modules/AC/AC4/project.html line 146",
    "proj-lab-1-run-line146-untouched": "course/modules/AC/AC4/project.html lines 53-145",
    "proj-messages-bare-asserts": "course/modules/AC/AC4/grader/test_project.py",
}
for rid, desc in carry_specs.items():
    if rid in R9_ROWS:
        rows.append(carry(rid, desc))
# rows of r9 that are neither carried nor fresh above
done = {r["id"] for r in rows}
missing = [rid for rid in R9_ROWS if rid not in done]
print("r9 rows not yet covered:", missing)

# ---- mutants: every committed project mutant with its first failing test on seed 0
mutants = []
for f in mut_files:
    text = (ROOT / "ledgers/AC4/mutants" / f).read_text(encoding="utf-8")
    doc = re.search(r'"""(.*?)"""', text, re.S).group(1).strip()
    mutants.append(dict(id=f[:-3], file=f"ledgers/AC4/mutants/{f}", description=doc,
                        killed_by=f"{killed[f]} (seed 0; also killed on seeds 1 and 25)"))

rows = [r for r in rows if r["id"] in {x["id"] for x in rows}]
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
missing = [rid for rid in R9_ROWS if rid not in ids]
assert not missing, missing
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) and all(m["killed_by"] for m in mutants) else "FAIL"
non_pass = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 10,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 10, slice AC4-e; did not build AC4)",
    "pin": "af08ad1",
    "base": "96dd532 (round-9 pin; previous fragment /tmp/fanout-frags/AC4-e.round9.json used as context; carried rows cite lines or files byte-identical since 96dd532, the only project.html change is line 324, the only cards.json changes are the ids listed in proj-cards-r10-* rows)",
    "checkout": "/tmp/verify10-AC4-e",
    "scratch": "/tmp/ac4-v/e10",
    "verified_at": "2026-10-28T15:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 96dd532..af08ad1 for this slice (git diff --stat): course/modules/AC/AC4/project.html (one line, 324: exemplars intro); course/modules/AC/AC4/cards.json (AC4-c003, c012, c014, c029, c038, c040, c042, c043, c045 reworded; AC4-c120..c128 appended; 119 -> 128 cards). grader/, tests/labs/AC4/, references/, index.html and L01-L08 are unchanged in the delta (git diff --stat).",
        "The round-9 FAIL proj-exemplar-intro-universal-claim is re-verified from scratch: every number in both memo-text blocks is derived from the case or labelled as a what-if, except Exemplar A's mix sign, which the sentence names and the annotation marks wrong. Now PASS.",
        "New FAIL proj-card-c126-basis: the basis of AC4-c126 copies the Proposition 2.2 attribution from the make-minus-buy row; the buy/full-cost figures are not given by that identity.",
        "Mutants: all 46 committed project mutants re-run on seeds 0, 1, 25 (all KILLED); four new student-error mutants m47-m50 written and all KILLED. Alternatives: alt_a..alt_k, alt_l (new), and the three r4 alternatives all PASS 296/296.",
        "The grader's collected count is 296 on seeds 0, 1, 25 and 1974022705; page smoke in-browser run reports 296 passing.",
        "Hours: lesson data-hours 6,7,6,6,7,6,6,6 = 50, project 20, total 70; consistent with hub. Per-component split not checked against pace (architect ruling).",
        "Not checked: live tools/verify_refs.py (no citation rows changed; references.json byte-identical since 96dd532); the full repository pytest suite (only the AC4 labs, memo-exemplar and page-check tests were run); live web access (none needed for this slice).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "non_pass_ids": non_pass,
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "counts", counts, "mutants", len(mutants), "verdict", verdict)

# ---- locations for the rows added in round 10
LOC = {
    "proj-alt-l-extra-keys": "ledgers/AC4/scripts/AC4-e-r10/alt_l.py; course/modules/AC/AC4/grader/test_project.py line 120",
    "proj-mutants-r10-new": "ledgers/AC4/mutants/m47_mix_omits_fixed_overhead.py; m48_efficiency_against_budgeted_output.py; m49_exact_halves_round_down.py; m50_flexed_units_is_budget_total.py",
    "proj-cards-r10-L01": "course/modules/AC/AC4/cards.json AC4-c003, c012, c014, c120, c127, c128; course/modules/AC/AC4/L01.html lines 88, 119",
    "proj-cards-r10-L02": "course/modules/AC/AC4/cards.json AC4-c029, c125; course/modules/AC/AC4/L02.html lines 252-257, 264",
    "proj-cards-r10-L03": "course/modules/AC/AC4/cards.json AC4-c038, c040, c042, c043, c122, c123, c124; course/modules/AC/AC4/L03.html lines 90, 95, 334, 348-349, 389",
    "proj-card-c126-basis": "course/modules/AC/AC4/cards.json line 891 (AC4-c126), basis field; course/modules/AC/AC4/L03.html line 512",
    "proj-cards-r10-L04": "course/modules/AC/AC4/cards.json AC4-c045, c121; course/modules/AC/AC4/L04.html line 55",
    "proj-cards-changed-lessons-r10": "course/modules/AC/AC4/cards.json AC4-c059..c068 and L05/L06 ids (unchanged)",
}
for r in rows:
    if not str(r.get("location", "")).strip():
        r["location"] = LOC[r["id"]]
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("relocated")
