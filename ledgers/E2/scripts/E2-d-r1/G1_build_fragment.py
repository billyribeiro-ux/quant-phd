# Builds ledgers/E2/E2-d.json (round 1, closing delta) from the base fragment F1-E2-d.round1.json.
# Re-verified rows get new evidence; every other PASS row is carried with the carry prefix.
import json, sys
from pathlib import Path
BASE = Path("/Users/billyribeiro/.fanout/frags/F1-E2-d.round1.json")
root = Path(sys.argv[1])
S = "ledgers/E2/scripts/E2-d-r1/"
base = json.loads(BASE.read_text(encoding="utf-8"))
CARRY = ("Carried from round 1 (base fragment F1-E2-d.round1.json, pin 95f3f8cb; course/modules/E/E2/project.html, "
         "grader/, tests/labs/E2/, ledgers/E2/mutants/ and the lesson pages L01-L09 byte-identical since the previous pin "
         "95f3f8cb per git diff --stat 95f3f8cb..HEAD, see " + S + "G1_slice_delta.out): ")
CARD_CARRY = ("Carried from round 1 (base fragment F1-E2-d.round1.json, pin 95f3f8cb; the card entry is byte-identical "
              "since 95f3f8cb, it is not among the 8 ids changed, see " + S + "G1_cards_numbers.out): ")
changed_cards = {"E2-c025", "E2-c037", "E2-c051", "E2-c059", "E2-c060", "E2-c088", "E2-c105", "E2-c130"}
new = {}
def N(id_, status, evidence, fix=None, check=None, location=None):
    new[id_] = (status, evidence, fix, check, location)

N("gate-check-pages", "PASS", "tools/check_pages.py --unit E2 re-run at 2a805c83: 'check_pages E2: PASS' exit 0 (" + S + "G1_check_pages.out)")
N("gate-check-dag", "PASS", "tools/check_dag.py --unit E2 re-run: 'check_dag E2: PASS' exit 0 (" + S + "G1_check_dag.out)")
N("gate-check-projects", "PASS", "tools/check_projects.py --unit E2 re-run: 'check_projects E2: PASS' exit 0 (" + S + "G1_check_projects.out)")
N("gate-run-graders", "PASS", "tools/run_graders.py --unit E2 --seeds 0-49 re-run: 'run_graders E2: PASS (reference 50/50 seeds, slowest 0.2 s)' exit 0 (" + S + "G1_run_graders_E2.out)")
N("gate-mutate-graders", "PASS", "tools/mutate_graders.py --unit E2 re-run (standing set, ruling 37): 'mutate_graders E2: PASS (64/64 killed)' exit 0 (" + S + "G1_mutate_graders_E2.out)")
N("gate-run-alternatives", "PASS", "ledgers/E2/scripts/run_alternatives.py re-run: alt01-alt05 each 'PASS suite 50/50 seeds; symmetric-bid mismatches vs reference 0' exit 0 (" + S + "G1_run_alternatives.out)")
N("gate-run-labs-unit", "PASS", "tools/run_labs.py --unit E2 re-run: 'run_labs E2: PASS (12/12)' exit 0 (" + S + "G1_run_labs_unit.out)")
N("gate-ruff", "PASS", "ruff check . re-run: 'All checks passed!' exit 0; ruff format --check . re-run: '555 files already formatted' exit 0 (" + S + "G1_ruff_check.out, " + S + "G1_ruff_format.out)")
N("gate-mypy", "PASS", "mypy --no-incremental re-run (strict per pyproject): 'Success: no issues found in 386 source files' exit 0 (" + S + "G1_mypy.out)")
N("gate-pytest-labs-E2", "PASS", "pytest -k E2 re-run: '16 passed, 710 deselected in 7.91s' (" + S + "G1_pytest_k_E2.out; tests/test_labs.py contributes 15 per --collect-only, " + S + "G1_collect_k_E2.out)")
N("gate-verify-refs-offline", "PASS", "tools/verify_refs.py --offline re-run: 'offline integrity: 560 entries, 0 problems' exit 0 (" + S + "G1_verify_refs_offline.out); references/references.json unchanged since 95f3f8cb")
N("gate-build-site-check", "PASS", "tools/build_site.py --check re-run (cards.json changed): 'site data current: 6 outputs' exit 0 (" + S + "G1_build_site_check.out)")
N("proj-process-words", "PASS", "Re-verified over the cards.json subject: ledgers/E2/scripts/E2-d-r1/G1_process_words.py scans the 8 changed cards for process words (round, ruling, verifier, fixer, draft, TODO, verify*, fixed, audit*, reviewer, closing): no hits (" + S + "G1_process_words.out). project.html, tests/labs/E2 and grader/ byte-identical since 95f3f8cb (carried for those files).")
N("cards-structure", "PASS", "tools/check_pages.py --unit E2 re-run PASS (cards.json: unique ids, lesson exists, valid grade, cite keys; " + S + "G1_check_pages.out); " + S + "G1_cards_numbers.py: 135 cards, duplicate fronts {}")
N("cards-structure-r9", "PASS", "re-run of cards-structure on the 135-card cards.json at 2a805c83 (" + S + "G1_cards_numbers.out: 135 cards, 0 duplicate fronts; " + S + "G1_check_pages.out PASS)")
N("cards-numbers-in-lesson", "PASS", "ledgers/E2/scripts/E2-d-r1/G1_cards_numbers.py re-run over all 135 cards: every number in front/back appears in the card's lesson text, 0 problems (" + S + "G1_cards_numbers.out)")
N("cards-changed-c025", "PASS", "E2-c025 (L02) re-verified: front 'n at least 2 bidders, all following the equilibrium of Proposition 2.2'; back '(n - 1)/(n + 1), under Assumptions 1 to 4 of Proposition 2.2 ... (Proposition 2.5)'. L02.html line 128 Proposition 2.5 'Let n >= 2, and let the bidders follow the equilibrium of Proposition 2.2. Under Assumptions 1 to 4 ... is (n - 1)/(n + 1)'. Proof lines 130-134: integral beta n int x^n = (n-1)/(n+1), correct. Hypotheses carried; grade T matches proposition T.")
N("cards-changed-c035-c037-c124", "PASS", "E2-c035 (L03): 'Under Assumptions 1 to 3 (the setting of Proposition 2.1), the share 1 - alpha trades (Proposition 2.3)'; L03.html lines 72-75 hold Assumptions 1-3 inside Proposition 2.1, line 97 Proposition 2.3 'Assume the setting of Proposition 2.1 ... share 1 - alpha'. E2-c037 (L03, changed): 'No. In this model the main loss is withheld trade: at the price 6000 the high-quality sellers do not trade (Proposition 2.3)'; L03.html line 97-102 and misconception line 220 ('the loss is withheld trade', c_H = 10000 > 6000); PASS. E2-c124 (L03): '2000 alpha cents per seller ... (Proposition 2.3)'; L03.html line 97 and proof line 102 'Each of them has a gain of 2000 cents, so the gains lost per seller are 2000 alpha'. All three PASS.")
N("cards-changed-c051", "PASS", "E2-c051 (L04, changed): 'No. The high type pays the education cost t c_H to reach the higher wage y_H instead of y_L (Remark 2.1).' L04.html line 219 (Remark 2.1): 'the high type's cost t c_H', wage y_H vs y_L at e = 0; line 237 misconception says the same. PASS.")
N("cards-changed-c060-c072", "PASS", "E2-c060 (L05, grade C, changed): full title 'Equilibrium in Competitive Insurance Markets: An Essay on the Economics of Imperfect Information', QJE 90(4). references/references.json entry rothschild1976equilibrium: title identical, container 'The Quarterly Journal of Economics', volume 90, issue 4, 1976; L05.html line 254 uses the same title and says 'cited by its title, year and venue only ... this lesson derives no result'. E2-c072 (L06, grade C): Holmstrom (1979), 'Moral Hazard and Observability', Bell Journal of Economics 10(1); registry holmstrom1979moral title, container 'The Bell Journal of Economics', volume 10, issue 1, 1979 match; L06.html line 248 cites the same. PASS.")
N("cards-changed-c088", "PASS", "E2-c088 (L07, T, changed; base FAIL cleared): back now 'With v_H > 0, Delta = v_H - v_L > 0 and c = p_L v_L - p_H Delta < 0, the optimum excludes type L (Proposition 3.2). In any feasible menu, q_L > 0 gives type H a rent of at least Delta q_L ... (Lemma 3.1).' L07.html lines 139-140 Proposition 3.2 'with v_H > 0 and Delta = v_H - v_L > 0, let c = p_L v_L - p_H Delta; ... q_L = 0 when c < 0'; proof (lines 147-153) gives q_L = 0 optimal when c < 0. Lemma 3.1 (line 129) gives U_H >= U_L + Delta q_L >= Delta q_L with U_L >= 0. Claim true. JUDGEMENT: the card does not name Assumptions 1, 2 and 4 of L07 (designer's problem); the proposition's explicit 'with' clause is now carried, the front fixes the seller's revenue problem, and the claim is not false without the naming, so no FAIL (see notes).")
N("cards-changed-discrete-EM", "FAIL", "E2-c098 PASS: n=5, a=2000 discrete E[M] = 85418692002000/64048012001 = 1333.66656252604 (recomputed with fractions; matches 1333.66656253 in L08.html line 135 and 1333.67 on the card). E2-c099 PASS: L08.html Proposition 3.1 line 125 (Assumptions 1 and 2, whole c). E2-c100 PASS: L08.html line 135 Remark 3.2 '1333 - 1333.66656253 = -0.66656253 ... rounds to -0.67'. E2-c105 (L08, T, changed) FAILS: its back 'Not every positive shading' is a universal claim with no parameter restriction. It is false for n = 2, a = 1: L08.html Example 2.4 gives E[M] = 4/9 cents and the M3 solution (line 322) says a 1-cent shading is large enough; every positive whole-cent shading c >= 1 > 4/9 gives expected profit c - E[M] >= 5/9 > 0, so no positive shading fails there. It holds only when E[M] > 1 cent (e.g. n = 5, a = 2000, shading 1333, L08.html line 293 and line 135). The back also answers 'not every' to a question that asks 'any'.", "Scope the E2-c105 back to the lesson's base case, e.g. 'Not in general. For n = 5 and a = 2000 cents, a shading of 1333 cents leaves -0.67 cents (Remark 3.2); whether a positive whole-cent shading suffices depends on E[M] (Proposition 3.1), and for n = 2, a = 1 the 1-cent shading already suffices (Example 2.4, Problem M3).' and make the front ask about a positive shading (not 'any'). Then re-verify E2-c105 with tools/check_pages.py --unit E2 and tools/build_site.py --check.")
N("cards-lesson-linked-unchanged", "PASS", "Re-verified the changed members of this row. E2-c051 (L04, changed): 'No. The high type pays the education cost t c_H to reach the higher wage y_H instead of y_L (Remark 2.1).' L04.html lines 218-219 (Remark 2.1: cost t c_H, wage y_H vs y_L at e = 0) and line 237 (misconception) agree. PASS. E2-c059 (L05, changed): 'First best 7,875,000 cents ... shortfall of 1,875,000 cents. Only the low type's quantity is distorted ... (Remark 2.1, Proposition 1.4).' Recomputed by fractions: first best 0.75*4.5e6+0.25*18e6 = 7,875,000; menu 6,000,000; gap 1,875,000. L05.html lines 239-241 (run output) and Remark 2.1 line 249 agree. PASS. The other members (c044, c045, c055-c058, c063, c067-c071, c073, c075) carried: their card entries are byte-identical since 95f3f8cb (" + S + "G1_slice_delta.out shows only 8 cards changed) and their lessons are unchanged.")
N("cards-new-c130", "PASS", "E2-c130 (L02, T; base FAIL cleared): front now 'What is the mean of the second-highest of n independent uniform values on [0, 1], for n at least 2?'; back '(n - 1)/(n + 1), the same number as the expected winning bid. Proposition 2.5 does not claim that this mean is a second-price revenue.' L02.html line 128 Proposition 2.5 'Let n >= 2' and its second statement 'the mean of the second-highest of n independent uniform values on [0, 1] is also (n - 1)/(n + 1)'; the lesson's closing paragraph (after the proof) says it does not claim the second-price revenue identity. Recomputed: density n(n-1)x^(n-2)(1-x) integrates to 1, mean (n-1)/(n+1). PASS. No duplicate front (" + S + "G1_cards_numbers.out).")

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in new:
        status, evidence, fix, check, location = new[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix
        rows.append(row)
        continue
    # carry
    if r["status"] != "PASS":
        raise SystemExit(f"base non-PASS row not re-verified: {rid}")
    ev = r["evidence"]
    prefix = CARD_CARRY if (rid.startswith("cards-") or rid.startswith("proj-")) and "cards.json" in r["location"] else CARRY
    if rid.startswith("cards-changed-") and any(c in rid for c in ["c025", "c037", "c051", "c059", "c060", "c088", "c105", "c130"]):
        raise SystemExit(f"row whose subject changed was not re-verified: {rid}")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": prefix + ev})
# rows whose cited subject changed must have been re-verified
for rid in ["cards-changed-c035-c037-c124", "cards-changed-c060-c072", "cards-changed-discrete-EM", "cards-lesson-linked-unchanged"]:
    assert rid in new, rid

fragment = {
    "unit": "E2",
    "slice": "d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-d, closing delta round 1 (did not build E2; checkout verifyG1-E2-d)",
    "pin": "2a805c83",
    "base": "F1-E2-d.round1.json (pin 95f3f8cb; itself the closing delta from 33744e5, round-9 fragment PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-E2-d",
    "scratch": "none outside the checkout; all runs in ledgers/E2/scripts/E2-d-r1/ (files prefixed G1_)",
    "verified_at": "2026-11-09T17:07:40+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": base["mutants"],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Closing delta (ruling 30) from 95f3f8cb to 2a805c83. The slice's content delta is course/modules/E/E2/cards.json only "
        "(8 cards changed: E2-c025, c037, c051, c059, c060, c088, c105, c130; 9 insertions, 9 deletions). project.html, grader/, "
        "tests/labs/E2/, ledgers/E2/mutants/, L01-L09 pages, notation/ and references/ are byte-identical to 95f3f8cb "
        "(git diff --stat). The other delta hunks (plans/FINAL-ARCHITECT-RULINGS.md rulings 38-39, tests/labs/E4, tests/labs/M3, "
        "tests/test_lx1_project_lab3.py) are outside the slice and were covered only by the repo-wide ruff and mypy re-runs. "
        "Rows re-verified from scratch: the base FAIL rows (cards-changed-c088, cards-new-c130) and every row whose cited subject "
        "changed (cards-changed-c025, -c035-c037-c124, -c051, -c059 via cards-lesson-linked-unchanged, -c060-c072, -discrete-EM "
        "for c105, cards-structure, cards-numbers-in-lesson). New outcome: E2-c088 and E2-c130 PASS; E2-c105 FAILS (a "
        "ruling-26 defect in the changed card's back, a T claim that needs a parameter restriction). "
        "No new mutants were written (ruling 37). The standing set (64 grader mutants) was re-run and all 64 are killed. "
        "Judgement calls: (1) E2-c088 PASS although the card does not name Assumptions 1, 2 and 4 of L07, because the explicit "
        "'with' clause of Proposition 3.2 is carried, the designer's problem is fixed by the front, and the claim is true without "
        "the naming; the same convention holds in the unchanged cards c105-style T claims. (2) E2-c105 FAIL (see its fix). "
        "Carry prefix uses round 1, the base fragment's round; the base's own carried rows keep their round-9 origin in their "
        "evidence text. "
        "Not run this round: full pytest suite (only -k E2, per the targeted rule); verify_refs live (offline only); "
        "page_smoke and run_labs twins under python -I -W error (carried: pages and tests/labs/E2 byte-identical); "
        "blind exemplar scorers (no rubric or exemplar text changed in E2, so no new calibration is needed; project rubric rows carried). "
        "Observation (not a row): the base's note that E2-c025 was judged on the auction model's standing assumption is consistent "
        "with the L02 text."
    ),
    "summary": "",
}
n_fail = sum(1 for r in rows if r["status"] != "PASS")
fragment["summary"] = (f"E2-d closing delta round 1 on pin 2a805c83 (base 95f3f8cb): {len(rows)} rows, "
                       f"{len(rows) - n_fail} PASS, {n_fail} FAIL. FAIL: cards-changed-discrete-EM (E2-c105 'Not every positive shading' "
                       f"is false for n = 2, a = 1, where any positive whole-cent shading exceeds E[M] = 4/9). Cleared: cards-new-c130, "
                       f"cards-changed-c088. Gates re-run PASS: check_pages, check_dag, check_projects, run_labs 12/12, run_graders 50/50, "
                       f"mutate_graders 64/64, run_alternatives 5/5, ruff, mypy (386 files), pytest -k E2 (16 passed), verify_refs offline 560/0, "
                       f"build_site --check.")
out = root / "ledgers/E2/E2-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", n_fail)
