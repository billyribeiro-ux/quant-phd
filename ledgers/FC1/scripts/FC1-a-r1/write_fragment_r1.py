"""Writes ledgers/FC1/FC1-a.json (round 1, closing delta, pin 95f3f8cb) from the round-5 base fragment."""
import json
import sys

ROOT = sys.argv[1]
BASE = "/Users/billyribeiro/.fanout/frags/S-FC1-a.round5.json"
base = json.load(open(BASE, encoding="utf-8"))

LESSONS = ("index.html, L01.html, L02.html, L03.html of course/modules/FC/FC1/ and the twins "
           "tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py")
PREFIX = "Carried from round 5 ({files} byte-identical since the previous pin dde0486b): "

CARD_FILES = {
    "a-r1-l01-cards-lab-T": None,
    "a-r1-l02-cards-lab-T": "cards.json FC1-c029, c030, c033, c034, c095, c096",
    "a-r1-l02-cards-other": "cards.json FC1-c019-c028, c031, c032, c115, c116, c120, c127, c149, c150",
    "a-r1-l03-example-2.5": "cards.json FC1-c043, c139, c140 and L03.html lines 118-121, 351, 477",
}

# Rows re-verified from scratch in this round (subject changed, or a gate re-run).
FRESH = {}

FRESH["a-r1-gate-check-pages"] = ("PASS", "2.9-structure", "course/modules/FC/FC1/ (index.html, L01-L03.html, cards.json)",
    "Re-run at 95f3f8cb (cards.json changed in this delta): tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' "
    "EXIT=0 (ledgers/FC1/scripts/FC1-a-r1/out/check_pages_unit.out); --all EXIT=0 with every unit line PASS (check_pages_all.out).")
FRESH["a-r1-gate-check-dag"] = ("PASS", "2.9-DAG", "course/modules/FC/FC1/",
    "Re-run at 95f3f8cb: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' EXIT=0 (check_dag_unit.out); --all EXIT=0, "
    "every unit line PASS (check_dag_all.out).")
FRESH["a-r1-gate-check-projects"] = ("PASS", "2.6-project-tool", "course/modules/FC/FC1/project.html (tool gate only; project rows belong to other slices)",
    "Re-run at 95f3f8cb: tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' EXIT=0 (check_projects_unit.out); "
    "--all EXIT=0, every unit line PASS (check_projects_all.out). Tool gate only.")
FRESH["a-r1-gate-run-labs"] = ("PASS", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, lab-FC1-L02-1.py, lab-FC1-L03-1.py",
    "Re-run at 95f3f8cb: tools/run_labs.py --unit FC1 -> 'run_labs FC1: PASS (8/8)' EXIT=0 (run_labs_fc1.out).")
FRESH["a-r1-twins-isolated"] = ("PASS", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py",
    "Each twin run alone with python -I -W error: EXIT=0 for L01, L02 and L03 (summary.txt lines twin_L01..twin_L03; out/twin_L0x.out). "
    "L01 Part B prints 'each stage balances: True' and 'cumulative reserves plus cumulative loans equal total deposits: True' (twin_L01.out lines 18-19).")
FRESH["a-r1-page-smoke"] = ("PASS", "2.9-structure", "index.html, L01.html, L02.html, L03.html",
    "Re-run at 95f3f8cb: tools/page_smoke.py --unit FC1 --pages index L01 L02 L03 -> 'page_smoke FC1: PASS' EXIT=0 (page_smoke_fc1.out).")
FRESH["a-r1-ruff-mypy-twins"] = ("PASS", "2.5-labs", "tests/labs/FC1/*.py and the whole repository",
    "Re-run at 95f3f8cb: .venv/bin/ruff check . -> 'All checks passed!'; ruff format --check . -> '555 files already formatted'; "
    "mypy --no-incremental -> 'Success: no issues found in 386 source files' (ruff_check.out, ruff_format.out, mypy_nocache.out).")
FRESH["a-r1-pytest-relevant"] = ("PASS", "2.9-structure", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_page_smoke.py, test_refs.py, test_docs_figures.py",
    "Re-run at 95f3f8cb: .venv/bin/pytest -q on the six files -> EXIT=0, all dots, no failure (pytest_slice.out). test_labs.py is run "
    "without -k FC1 because this delta changed other units' twins; this supersedes the round-5 -k form.")
FRESH["a-r1-verify-refs-offline"] = ("PASS", "2.1-citations", "references/references.json (keys cited by the slice: harris2002trading, mishkin2021economics)",
    "Re-run at 95f3f8cb: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' EXIT=0 (verify_refs_offline.out). "
    "references/ unchanged in this delta.")
FRESH["a-r3-gates-full"] = ("PASS", "2.9-gates", "ledgers/FC1/scripts/FC1-a-r1/gates_r1.sh (out/summary.txt)",
    "Round-1 gate run at 95f3f8cb: check_pages, check_dag, check_projects (unit and all), run_labs FC1, ruff check, ruff format --check, "
    "mypy --no-incremental, pytest (slice files), verify_refs --offline, build_site --check ('site data current: 6 outputs'), "
    "fetch_data --check ('3 datasets, 0 problems'), page_smoke FC1, and the three twins under python -I -W error: every command EXIT=0 (summary.txt).")

FRESH["a-r1-l01-cards-lab-T"] = ("PASS", "2.7-cards", "cards.json FC1-c014, FC1-c092, FC1-c093, FC1-c125",
    "Re-verified at 95f3f8cb. FC1-c125 is removed in this delta (ledgers/FC1/scripts/FC1-a-r1/out/cards_delta_r1.out: 'removed: FC1-c125'); "
    "no reference to FC1-c125 remains outside ledgers/ (grep over the checkout, excluding .git, .venv and ledgers, returns nothing). "
    "FC1-c014, c092, c093 are byte-identical (cards_delta_r1.out lists them as unchanged). Each is grade C with a basis naming Lab 1 "
    "Parts A, C and D; their statements match twin_L01.out: Part A exact comparison True (line 13), Part C 181790 and 686189 cents "
    "(lines 22-23 region of the Part C block), Part D sign test True, True, False. The Part B claim formerly on c125 is now a clause of "
    "FC1-c103 and is checked in a-r1-l01-cards-other.")
FRESH["a-r1-l01-card-c153-locator"] = ("PASS", "2.7-cards", "cards.json FC1-c153 (back, changed in this delta)",
    "Re-verified at 95f3f8cb. FC1-c153 back: 'Under A2′ with d > 0, A1 with 0 < ρ ≤ 1, and the no-withdrawal and no-repayment parts of A3, "
    "exactly when φ = 1 or ρ = 1 (Proposition 3.5).' L01.html line 132 states Proposition 3.5 under Assumption 2.0 with d > 0, A2′, A1 with "
    "0 < ρ ≤ 1, and the no-withdrawal and no-repayment parts of A3 (A3 at L01.html line 76), with limit d/(1 − φ(1 − ρ)) and equality with d/ρ "
    "iff φ = 1 or ρ = 1. Check: equality means 1 − φ(1 − ρ) = ρ, i.e. (1 − ρ)(1 − φ) = 0, for d > 0. The card's hypotheses and answer match.")
FRESH["a-r1-l01-cards-other"] = ("FAIL", "2.7-cards", "cards.json FC1-c016 (back); L01.html lines 103-113 (Proposition 3.1 and proof), line 334 (misconception 2)",
    "Re-verified at 95f3f8cb. FAIL on FC1-c016 (grade T). Front: 'Is the deposit multiplier 1/ρ at every stage?' Back begins 'No.' and states the "
    "hypothesis 'Under Assumption 2.0 with d > 0 and 0 < ρ ≤ 1'. At ρ = 1 the multiplier is (1 − (1 − ρ)^(n+1))/ρ = 1 = 1/ρ at every stage, so the "
    "answer 'No' is false under the card's own hypothesis. L01.html line 113 (proof) states that when ρ = 1 'the formula gives S_n = d for every n'; "
    "only the 'smaller than 1/ρ' clause is qualified by ρ < 1 (line 334). Rest of the row, verified: FC1-c103 back ('Yes. ... (Proposition 2.2; Lab 1, "
    "Part B prints True).') is correct: Proposition 2.2 (L01.html lines 89-90) proves it, and twin_L01.out lines 18-19 print True. Its lab clause "
    "is a corroboration on a T card, the same pattern as FC1-c015 accepted in round 5, so it is not a row defect. Other L01 cards in this row are "
    "byte-identical since dde0486b (cards_delta_r1.out).",
    "Change the answer in FC1-c016 back from 'No.' to 'No, when ρ < 1.' (or restrict its hypothesis to 0 < ρ < 1 and keep 'No.'), keeping the "
    "rest of the back, so the answer holds on every case the back states. Then re-run tools/check_pages.py --unit FC1 and this delta's card scan.")
FRESH["a-r1-l02-forward-pointers"] = ("PASS", "2.9-DAG", "L02.html line 270; L04.html lines 57 and 84; L05.html lines 58 and 63",
    "Re-verified at 95f3f8cb. L04/L05 changed lines in this delta are 51, 99, 503, 551, 590 (L04) and 52, 79, 90, 100, 540, 541 (L05); none of the "
    "cited lines is among them (cited_lines_r1.out). L02.html line 270 unchanged ('Lesson 4 defines the order types and the limit order book, and "
    "Lesson 5 defines clearing and settlement'). L04.html line 57 (<dfn id=\"def-order-types\">) and 84 (<dfn id=\"def-limit-order-book\">) and "
    "L05.html line 58 (<dfn id=\"def-clearing-and-settlement\">) and 63 (<dfn id=\"def-trade-lifecycle\">) are byte-identical to dde0486b.")
FRESH["a-r1-dag-definitions"] = ("PASS", "2.9-DAG", "L01 dfn lines 59, 81; L02 lines 58, 92; L03 lines 57, 61; L04 lines 57, 84; L05 lines 58, 63",
    "Re-verified at 95f3f8cb (cited_lines_r1.out: all cited lines identical to dde0486b). id uniqueness grep (out/ and this round): each of "
    "def-bank-money-creation, def-financial-intermediary (L01), def-asset-class-taxonomy, def-exchange-vs-otc (L02), def-bid-ask-spread, "
    "def-market-maker (L03), def-limit-order-book, def-order-types (L04), def-clearing-and-settlement, def-trade-lifecycle (L05) appears once as an id.")
FRESH["a-r1-cards-grade-convention"] = ("PASS", "2.7-cards", "cards.json, 104 L01-L03 cards (L01 34, L02 29, L03 41)",
    "Re-verified at 95f3f8cb (ledgers/FC1/scripts/FC1-a-r1/out/cards_r1.out): grade/basis mismatches over all 169 cards in cards.json: none. "
    "T cards that mention a lab: FC1-c015 (accepted in round 5) and FC1-c103 (see a-r1-l01-cards-other).")
FRESH["a-r1-cards-dup-gaps"] = ("PASS", "2.7-cards", "cards.json FC1-c025, FC1-c033 and full scan",
    "Re-verified at 95f3f8cb (cards_r1.out): 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs over 169 cards. Id gaps in 001-172: "
    "FC1-c125 (removed in this delta; not referenced), FC1-c134 (pre-existing gap), FC1-c163 (gap noted in round 5); none is referenced.")
FRESH["a-r1-l03-cards"] = ("PASS", "2.7-cards", "cards.json, all 41 L03 cards; changed FC1-c050 and FC1-c105",
    "Re-verified at 95f3f8cb. FC1-c050 (changed): front 'Under B1 to B4, why does the symmetric profile (c+k, c+k) with k ≥ 3 fail to be an "
    "equilibrium?'; back: undercut to c+k−1 wins all N and earns (k−1)N, the tie earns kN/2, and (k−1)N > kN/2 exactly when k > 2. This matches "
    "L03.html lines 156-158 (the derivation, 'exactly when 2(k − 1) > k, that is k > 2') and the k ≥ 3 of Proposition 3.2 (line 150). "
    "FC1-c105 (changed): back matches Assumption A2 at L03.html line 81 word for word in substance (no fees, no interest on cash, no inventory cost, "
    "no information; cash and shares the only two quantities). The other 39 L03 cards are byte-identical (cards_delta_r1.out). Lesson lines unchanged.")
FRESH["a-r2-cards-near-dup-scan"] = ("PASS", "2.7-cards", "cards.json, 104 L01-L03 cards",
    "Re-run at 95f3f8cb (neardup_r1.out): Jaccard over front+back: top pairs FC1-c036/c137 (0.722, quoted spread vs mid: distinct facts), "
    "FC1-c152/c153 (0.71, 'is the limit at most d/ρ' vs 'when does it equal d/ρ' of Proposition 3.5: distinct answers), FC1-c013/c122 (0.70, "
    "distinct facts per round-4 calibration). Front-only top pairs are the templated 'What does Assumption X fix?' questions. FC1-c050 vs "
    "FC1-c170 fronts now have Jaccard 0.185 (was 0.88 in round 5), so they are no longer a near duplicate. 0 duplicate ids.")

# Carried rows: prefix + base evidence. Files per row.
def carry_files(rid):
    if rid in CARD_FILES and CARD_FILES[rid]:
        return CARD_FILES[rid]
    return LESSONS

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH:
        f = FRESH[rid]
        status, check, location, evidence = f[0], f[1], f[2], f[3]
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = f[4]
    else:
        files = carry_files(rid)
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
               "evidence": PREFIX.format(files=files) + r["evidence"]}
        if r["status"] != "PASS":
            raise SystemExit(f"base non-PASS row {rid} must be re-verified, not carried")
    rows.append(row)

missing_fresh = [k for k in FRESH if k not in {r['id'] for r in base["rows"]}]
assert not missing_fresh, missing_fresh

mutants = []
for m in base["mutants"]:
    mutants.append({"id": m["id"], "description": m["description"],
                    "killed_by": "KILLED in the round-1 standing set run (out/mutants_r1.out): " + m["killed_by"]})

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
verdict = "PASS" if counts["FAIL"] == 0 and all(r["status"] == "PASS" for r in rows) else "FAIL"

frag = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 1,
    "verifier": "Claude Haiku 5.5 independent verifier, FC1-a closing delta (ruling 30), round 1 of this verification; did not build FC1; read verifier-rules.md; base = round-5 fragment at dde0486b; re-verified every row whose subject changed and re-ran the gates and the standing lab-claim mutants at 95f3f8cb",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; round-5 fragment /Users/billyribeiro/.fanout/frags/S-FC1-a.round5.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF11-FC1-a",
    "scratch": "/tmp is unused; all scratch output is under ledgers/FC1/scripts/FC1-a-r1/out/",
    "verified_at": sys.argv[2],
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": base["registry_flags"],
    "freshness_flags": base["freshness_flags"],
    "notes": [
        "Scope (ruling 30): slice a = index.html, L01-L03.html, twins tests/labs/FC1/lab-FC1-L01/L02/L03-1.py, and the L01-L03 cards of cards.json. Delta dde0486b..95f3f8cb: the twins, index.html, L01-L03.html and the curriculum, references and tools inputs are byte-identical. cards.json changed for FC1-c016, c050, c103, c105, c153 (L01-L03), removed FC1-c125 (L01), and changed L04/L05 cards (c061, c067, c075, c082, c089, c090, c100) and added c171 (L04), c172 (L05) that belong to other slices and were not verified here. L04.html and L05.html changed only at lines 51, 99, 503, 551, 590 and 52, 79, 90, 100, 540, 541; the slice cites L04/L05 lines 57, 84, 58, 63 only, which are unchanged (cited_lines_r1.out). project.html changed at lines 38, 54, 101, 171, 188, 323; the hub cites its lines 42-47, unchanged.",
        "Ruling 37: no new mutants written. The standing lab-claim set (5 mutants, the base's list) was re-run against the three twins under python -I -W error: all 5 KILLED (out/mutants_r1.out). Lab-claim mutants are not grader mutants (ruling 9); no FC1-a grader exists.",
        "Round-5 PASS rows not touched by this delta are carried with the round-5 prefix; their cited files are byte-identical since dde0486b (cited_lines_r1.out, git diff --stat).",
        "The one FAIL is FC1-c016: its 'No.' answer is false at rho = 1, which its own hypothesis 0 < rho <= 1 admits (L01.html lines 103-113 show S_n = d there). This is a ruling-26 kind (false statement); a fixer should change the back and this closing delta should be re-verified once more (ruling 30).",
        "Advisory (no row): FC1-c103 is graded T and ends with 'Lab 1, Part B prints True'. The same pattern is on FC1-c015, accepted in round 5, so the row passes. A stricter reading would grade the lab clause C, as FC1-c125 was.",
        "Advisory (no row): FC1-c050 now asks why (c+k, c+k) with k >= 3 fails, and FC1-c170 asks which profiles are equilibria. They have different answers and a front Jaccard of 0.185, so they are not duplicates. The round-5 advisory on c050/c170 is closed.",
        "Repo state: ledgers/FC1/FC1-a.json already existed in the checkout at round 6, pin 9fd6aed (an ancestor of dde0486b), not the round-5 pin named as base. This fragment overwrites it, as the task directs. The base used here is the round-5 fragment named in the task.",
        "Not run: run_graders.py and mutate_graders.py (no FC1-a grader); render_curriculum.py (curriculum unchanged in this delta); Chromium screenshots (no figures in the slice). Bibliographic years were not re-read beyond verify_refs --offline (references unchanged); registry_flags carry round 5.",
    ],
    "summary": ("FC1-a closing delta (round 1 of this verification) at 95f3f8cb: %d rows (the 80 round-5 ids kept): %d PASS, %d FAIL, 0 UNVERIFIABLE. "
                "The one FAIL is FC1-c016 (a false 'No' answer at rho = 1). All gates re-run EXIT=0. Standing mutants: 5 of 5 KILLED. "
                "Verdict %s.") % (len(rows), counts["PASS"], counts["FAIL"], verdict),
}
out = f"{ROOT}/ledgers/FC1/FC1-a.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("wrote", out, "rows", len(rows), counts, verdict)
