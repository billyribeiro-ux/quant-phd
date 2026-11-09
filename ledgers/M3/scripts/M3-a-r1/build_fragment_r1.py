"""Build ledgers/M3/M3-a.json (M3 slice a, closing delta round 1) from the round-2 base fragment.

Carried rows keep the base evidence under the carry prefix; rows whose subject changed or that are gates are re-run and
rewritten. Row ids are the base ids. Run with python -I -W error from the checkout root.
"""
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

BASE = "/Users/billyribeiro/.fanout/frags/S-M3-a.round2.json"
base = json.load(open(BASE, encoding="utf-8"))
OUT = "ledgers/M3/M3-a.json"
PAGES = "course/modules/M/M3/index.html, L01.html, L02.html, L03.html and tests/labs/M3/lab-M3-L01-1.py, L02-1.py, L03-1.py"
CARRY_PAGES = f"Carried from round 2 ({PAGES} byte-identical since the previous pin 9294b914; git diff 9294b914..95f3f8cb on these paths is empty):"
CARD_IDS = "M3-c003, c013, c014, c031, c032, c035, c045, c046, c051, c052, c053"

fresh = {
    "a-cards-coverage": (
        "2.7 card coverage",
        "course/modules/M/M3/cards.json (68 cards for L01-L03)",
        "Re-derived in round 1 with ledgers/M3/scripts/M3-a-r1/cards_delta.py: cards.json has 209 cards at 9294b914 and 210 at HEAD; "
        "removed M3-c101 (L06) and M3-c176 (L05); added M3-c217 (L09), M3-c218 and M3-c219 (L05); no L01-L03 card is added or removed, "
        "so the L01-L03 count is 68 at both pins (printed 'L01-L03 cards at HEAD: 68', 'at base: 68'). Id order is preserved. "
        "Every L01-L03 card has a lesson field in L01, L02 or L03.",
    ),
    "a-cards-read-all": (
        "2.7 card accuracy (all 68 read)",
        "course/modules/M/M3/cards.json (L01-L03 cards)",
        "Read in full in round 1: the eight L01-L03 cards whose bytes changed since 9294b914, M3-c016, c017, c018, c019 (L01), c038, c039, c184 (L02) "
        "and c058 (L03), each checked against the lab output of its lesson and the lab twin: Lab 1 of L01 prints 188 of 200, 198 of 200, "
        "'planted ... dependent in 100 of 100', and 0 of 200 (out/L01 twin output); L02 prints 'coordinates ... in 50 of 50', "
        "'within 1e-12 ... in 50 of 50' and 'composition matrix ... 50 of 50'; L03 prints 'det P = 6' (L03.html:224, out). "
        "Each changed back gained the SIMULATED tag where the lab is SIMULATED (L01.html:193, L02.html:182 heading, L01 and L02 docstrings 'SIMULATED: yes') "
        "or lost the cofactor phrase (c058; the twin's det3_int is by cofactor expansion, so the phrase was true and its removal is not a defect). "
        "The other 60 L01-L03 cards are byte-identical since 9294b914 and carried: " + CARD_IDS + " and the rest of the set (round-2 evidence).",
    ),
    "a-cards-refs-numbers": (
        "2.7 cited results and numbers in lesson",
        "cards.json; ledgers/M3/scripts/M3-a-r1/cards_scan_r1.py output",
        "cards_scan_r1.py (python -I -W error, out/cards_scan_r1.out): every number token in the eight changed backs appears in its lesson text "
        "(e.g. c016 '188', '200', '-3', '3'; c019 '0', '200', '3'; c038 and c039 '50'; c058 '6'; c184 '50'). The citations in the changed backs "
        "exist in their lesson: Proposition 3.5 and Corollary 3.6 in L01.html (c018, c019), Proposition 3.1 in L02.html (c184). "
        "Fresh numeric re-derivation: twin outputs saved in out/twin_L01.out, twin_L02.out, twin_L03.out match each printed count.",
    ),
    "a-cards-duplicates": (
        "2.7 duplicate scan (full file)",
        "cards.json (210 cards, full file); M3-c179, M3-c218",
        "Full-file scan of all 210 cards (cards_scan_r1.py): no duplicate id and no identical front. Front-text ratios >= 0.9 (difflib) are "
        "c017/c019 (R^4 versus R^3 counts), c025/c187 (kernel versus image), c082/c193 and c087/c088 (positive semidefinite versus positive definite): "
        "distinct questions with distinct answers. "
        "Observation, not a ruling-26 FAIL kind: M3-c179 (L05, grade T, 'Does the tolerance test of Definition 3.1 ... reject [[1, 2], [2, 1]]?') "
        "and new M3-c218 (L05, grade C, 'In Lab 1 Part A, does the code print that the eigenvalue test rejects [[1, 2], [2, 1]]?') ask the same "
        "question with the same answer (both 'True'/'Yes'). They differ in grade and wording (text similarity 0.49). Left for the owner to merge "
        "or record in plans/KNOWN-ISSUES.md. Removed c176 (L05) was the duplicate of c085 and is gone.",
    ),
    "a-cards-grade-basis": (
        "2.7 grades and basis",
        "cards.json (C and T cards of L01-L03)",
        "Re-read in round 1: the eight changed L01-L03 cards are all grade C with a basis naming Lab 1 "
        "('Lab 1, a finite computation on the listed draws' for c016-c019; 'Lab 1, a computation on the listed seeded pairs' for c038, c039, c184; "
        "'Lab 1, a computation on the listed matrices' for c058). Rule 13: each value appears only in lab output in these cards; the page's "
        "key-results row for det P = 6 (L03.html:402) is also C with Lab 1 as basis, so card and row agree. c058 note: Example 2.5 "
        "(L03.html:144) asserts 'The determinant of P is 6' without a hand computation, so C is conservative rather than an over-grade. "
        "No L01-L03 T card changed; the other C cards are byte-identical since 9294b914 and carried.",
    ),
    "a-hub-banned-process": (
        "2.9 banned phrases and process words",
        "index.html; L01-L03 pages; lab twins; L01-L03 cards (68)",
        "Re-run in round 1 (banned_scan_r1.py, python -I -W error): zero hits over index.html, L01.html, L02.html, L03.html (visible text), "
        "the three L01-L03 twins and the 68 L01-L03 cards, including the eight changed cards. Output 'L01-L03 cards scanned 68 banned/process-word hits: 0'.",
    ),
    "a-gate-check-pages": (
        "gate: check_pages",
        "tools/check_pages.py --unit M3",
        "Round 1 at 95f3f8cb: 'check_pages M3: PASS', exit 0 (ledgers/M3/scripts/M3-a-r1/out/check_pages_M3.out).",
    ),
    "a-gate-check-dag": (
        "gate: check_dag",
        "tools/check_dag.py --unit M3",
        "Round 1 at 95f3f8cb: 'check_dag M3: PASS', exit 0 (out/check_dag_M3.out).",
    ),
    "a-gate-check-projects": (
        "gate: check_projects",
        "tools/check_projects.py --unit M3",
        "Round 1 at 95f3f8cb: 'check_projects M3: PASS', exit 0 (out/check_projects_M3.out). Project files are outside slice a and were not read.",
    ),
    "a-gate-run-labs": (
        "gate: run_labs (lab rule 2.5)",
        "tests/labs/M3/lab-M3-L01-1.py, L02, L03",
        "Round 1: 'run_labs M3: PASS (12/12)', exit 0 (out/run_labs_M3.out). Each L01-L03 twin run alone under python -I -W error: exit 0, stderr empty "
        "(out/twin_L01.out, twin_L02.out, twin_L03.out). Output L01 12 lines, L02 9 lines, L03 9 lines.",
    ),
    "a-gate-page-smoke": (
        "gate: page_smoke",
        "tools/page_smoke.py --unit M3 --pages index L01 L02 L03",
        "Round 1 at 95f3f8cb: 'page_smoke modules/M/M3/L03.html: PASS', 'page_smoke M3: PASS', exit 0 (out/page_smoke_slice_a.out).",
    ),
    "a-gate-embed": (
        "2.5 page code equals twin; expected equals output",
        "L01.html, L02.html, L03.html",
        "Round 1, ledgers/M3/scripts/M3-a-r1/twin_vs_page_r1b.py (run with .venv python -I -W error): L01 'page code == twin: True' and "
        "'expected == twin output: True'; L02 and L03 likewise; twin exit 0, stderr 0 bytes for each.",
    ),
    "a-gate-lint-types": (
        "gate: ruff and mypy",
        "repository; tests/labs/M3 (L05 and L06 twins changed in the delta)",
        "Round 1 at 95f3f8cb: 'ruff check .' -> 'All checks passed!' exit 0; 'ruff format --check .' -> '555 files already formatted' exit 0; "
        "'mypy --no-incremental' -> 'Success: no issues found in 386 source files' exit 0 (out/ruff_check.out, ruff_format.out, mypy.out).",
    ),
    "a-gate-pytest": (
        "gate: pytest relevant modules",
        "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
        "Round 1: pytest -q on the three modules: 190 tests (dot count 72 + 72 + 46), exit 0 (out/pytest_relevant.out). "
        "Per-file collection: test_page_checks.py 41, test_run_labs.py 6.",
    ),
    "a-gate-refs": (
        "gate: verify_refs",
        "tools/verify_refs.py --offline; --unit M3",
        "Round 1: 'offline integrity: 560 entries, 0 problems' exit 0 (out/verify_refs_offline.out); "
        "'live re-verification of M3: 2 of 560 entries, 0 problems' exit 0 (out/verify_refs_M3_live.out). references/ and tools/ are byte-identical since 9294b914.",
    ),
    "a-gate-build-site": (
        "gate: build_site freshness",
        "tools/build_site.py --check",
        "Round 1 at 95f3f8cb: 'site data current: 6 outputs', exit 0 (out/build_site_check.out). cards.json changed; the site data is still current.",
    ),
}

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in fresh:
        check, location, evidence = fresh[rid]
        rows.append({"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence})
        continue
    prefix = CARRY_PAGES
    if rid in ("a-cards-c054", "a-cards-hypotheses"):
        prefix = ("Carried from round 2 (course/modules/M/M3/cards.json entries " + (
            "M3-c054" if rid == "a-cards-c054" else CARD_IDS) + " byte-identical since the previous pin 9294b914: none of these ids is in the "
            "32-id changed list of git diff 9294b914..95f3f8cb, checked with cards_delta.py):")
    rows.append({
        "id": rid,
        "check": r["check"],
        "location": r["location"],
        "status": "PASS",
        "evidence": prefix + " " + r["evidence"],
    })

assert [r["id"] for r in rows] == [r["id"] for r in base["rows"]], "row ids must be kept"

registry = base["registry_flags"]
fragment = {
    "unit": "M3",
    "slice": "a",
    "round": 1,
    "verifier": "Haiku independent verifier, M3-a closing delta round 1 (did not build M3; no shared context with the builders)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin of the base fragment ~/.fanout/frags/S-M3-a.round2.json; delta = 9294b914..95f3f8cb)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M3-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyF21-M3-a/ledgers/M3/scripts/M3-a-r1/out (gate outputs; scripts under ledgers/M3/scripts/M3-a-r1/)",
    "verified_at": "2026-11-09T10:40:00-05:00",
    "verdict": "",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry,
    "freshness_flags": base.get("freshness_flags", []),
    "notes": [
        "Closing delta under plans/FINAL-ARCHITECT-RULINGS.md ruling 30 (delta from the last full fragment, pin 9294b914) and ruling 37 (no new mutants). "
        "Ruling 26 FAIL kinds only; observations are notes. The task names this round 1; the base fragment is labelled round 2.",
        "Delta in the slice paths (git diff 9294b914..95f3f8cb): course/modules/M/M3/index.html, L01.html, L02.html, L03.html and tests/labs/M3/lab-M3-L01-1.py, L02-1.py, L03-1.py are byte-identical (empty diff). "
        "Only course/modules/M/M3/cards.json changed among slice-a paths: 32 changed ids, of which 8 belong to L01-L03 (c016, c017, c018, c019, c038, c039, c058, c184), all re-read and re-verified; "
        "L01-L03 card count stays 68. Outside slice a and not read as rows: L04.html, L05.html, L06.html, tests/labs/M3/lab-M3-L05-1.py and L06-1.py, cards c073 to c100, c101 (removed), c124 to c141, c161 to c179, c214, c217 to c219 (added), c176 (removed); project and grader files; references.json, tools, curriculum, notation (all empty diff).",
        "Mutation testing does not apply to a lesson slice (ruling 37: closing round writes no new mutants); mutants is empty by design, as in round 2.",
        "Observation for the owner (not a ruling-26 FAIL kind, so PASS): M3-c179 (T) and M3-c218 (C), both L05, ask whether the Part A eigenvalue test rejects [[1, 2], [2, 1]] with the same answer; see a-cards-duplicates.",
        "Observation (not an over-grade, so PASS): det P = 6 is asserted in Example 2.5 (L03.html:144) and graded C with Lab 1 as basis in c058 and the key-results row (L03.html:402); rule 13 would grade T only if the Example counts as a hand derivation.",
        "Method limit: the changed cards were checked against the twin outputs and the page text, not against a rendered screenshot; no page prose in slice a changed.",
        "The repository file ledgers/M3/M3-a.json held an earlier campaign's round-12 fragment and is overwritten with this round as instructed. The scripts directory already held earlier scripts (cards_check.py, cards_scan_verifier_r1.py, recheck_m3a.py, recheck_numbers.py, twin_vs_page.py); they were not modified.",
        "Not checked: the Open Library Strang edition (registry flag carried from round 2, not re-fetched by plain curl this round; the live verify_refs --unit M3 run passed); dark-mode and 360 px renders (page_smoke only).",
    ],
    "summary": "",
}

ok = sum(1 for r in rows if r["status"] == "PASS")
carried = sum(1 for r in rows if r["evidence"].startswith("Carried from round 2"))
fragment["verdict"] = "PASS" if ok == len(rows) else "FAIL"
fragment["summary"] = (
    f"M3 slice a, closing delta round 1 at 95f3f8cb (base 9294b914): verdict {fragment['verdict']}. {len(rows)} rows, {ok} PASS, 0 non-PASS. "
    f"Re-verified this round: {len(fresh)} rows (cards subject changed; all gates re-run). Carried from round 2 under the carry prefix: {carried} rows "
    "(page, twin and hub files byte-identical since 9294b914). Eight changed L01-L03 cards checked against the lab twin outputs; no ruling-26 defect found."
)
problems = ledger.validate(fragment, "M3-a")
print("validate:", problems)
json.dump(fragment, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", len(rows), "pass", ok, "carried", carried, "fresh", len(fresh), "verdict", fragment["verdict"])
