"""Round-1 closing delta fragment for CS2 slice b (pin 95f3f8cb, base round-7 fragment at aa659725).

Carries every base row whose cited subject is byte-identical, re-verifies the gate rows and the
card rows whose subject this round touched (cards.json), and adds one scope row for the delta.
Run with: python -I this_file.py <checkout_dir>
"""
import json
import subprocess
import sys
from datetime import UTC, datetime

CHECKOUT = sys.argv[1]
BASE_FRAG = "/Users/billyribeiro/.fanout/frags/S-CS2-b.round7.json"
OUT = f"{CHECKOUT}/ledgers/CS2/CS2-b.json"
BASE_PIN = "aa659725"
PIN = "95f3f8cb"
R = "ledgers/CS2/scripts/CS2-b-r1"

base = json.load(open(BASE_FRAG, encoding="utf-8"))

PAGES = (
    "course/modules/CS/CS2/L05.html, L06.html, L07.html, L08.html, tests/labs/CS2/lab-CS2-L05-1.py .. "
    "lab-CS2-L08-1.py, course/index.html, course/concepts.html, course/modules/CS/CS2/project.html, "
    "notation/notation.json, references/references.json and the tools/ gate scripts"
)
CARRY_FILES = (
    f"course/modules/CS/CS2/L05.html..L08.html, tests/labs/CS2/lab-CS2-L05..L08-1.py, course/index.html, "
    f"course/concepts.html, notation/notation.json, references/references.json: git blob hashes identical "
    f"at {BASE_PIN} and {PIN} (round-1 check)"
)
CARRY_CARDS = (
    f"the 73 L05-L08 card objects of course/modules/CS/CS2/cards.json are canonically identical at {BASE_PIN} and "
    f"{PIN} (the file changed only at HEAD lines 1220, 1332-1333, 1415, 1423, all L09-L11 objects; "
    f"{R}/v1_cards_identity.out)"
)

FRESH = {
    "CS2b-gate-check-pages": (
        f"Re-run this round at {PIN}: check_pages.py --unit CS2 --page L05, L06, L07, L08 each printed "
        "'check_pages CS2 Lnn: PASS' and exit 0; check_pages.py --unit CS2 printed 'check_pages CS2: PASS' exit 0 "
        f"({R}/v1_check_pages_*.out)."
    ),
    "CS2b-gate-check-dag": (
        f"Re-run this round at {PIN}: check_dag.py --unit CS2 printed 'check_dag CS2: PASS', exit 0 "
        f"({R}/v1_check_dag.out)."
    ),
    "CS2b-gate-check-projects": (
        f"Re-run this round at {PIN}: check_projects.py --unit CS2 printed 'check_projects CS2: PASS', exit 0 "
        f"({R}/v1_check_projects.out)."
    ),
    "CS2b-gate-run-labs": (
        f"Re-run this round at {PIN}: run_labs.py --unit CS2 printed 'run_labs CS2: PASS (14/14)', exit 0 "
        f"({R}/v1_run_labs_CS2.out)."
    ),
    "CS2b-gate-lab-exact": (
        f"Re-run this round at {PIN} with {R}/v1_twin_page_eq.py: for L05-L08 the page code block equals the twin "
        "after strip (identical_after_strip=True); each twin run alone with python -I -W error exits 0 with empty "
        "stderr; the expected block equals stdout (equal=True, 31, 17, 10, 15 lines; "
        f"{R}/v1_twin_page_eq.out)."
    ),
    "CS2b-gate-page-smoke": (
        f"Re-run this round at {PIN}: page_smoke.py --unit CS2 --pages L05 L06 L07 L08 printed PASS for each page and "
        f"'page_smoke CS2: PASS', exit 0 ({R}/v1_page_smoke_L05-L08.out)."
    ),
    "CS2b-gate-ruff-mypy": (
        f"Re-run this round at {PIN}: ruff check tests/labs/CS2/ 'All checks passed!'; ruff format --check "
        "tests/labs/CS2/ '14 files already formatted'; mypy --no-incremental on the four L05-L08 twins 'Success: no "
        f"issues found in 4 source files' ({R}/v1_ruff_mypy_twins.out)."
    ),
    "CS2b-gate-pytest": (
        f"Re-run this round at {PIN}: pytest tests/test_labs.py -k CS2 exit 0 with 14 passing tests (progress line of "
        f"14 PASSED lines, 0 FAILED ({R}/v1_pytest_labs_CS2_passed.out); pytest tests/test_page_checks.py exit 0 with "
        f"41 PASSED lines, 0 FAILED ({R}/v1_pytest_page_checks_passed.out)."
    ),
    "CS2b-gate-build-site": (
        f"Re-run this round at {PIN} because cards.json changed (L09-L11 only): build_site.py --check exit 0, "
        f"'site data current: 6 outputs' ({R}/v1_build_site_check.out)."
    ),
    "CS2b-gate-verify-refs": (
        f"Re-run this round at {PIN}: verify_refs.py --offline exit 0, 'offline integrity: 560 entries, 0 problems' "
        f"({R}/v1_verify_refs_offline.out). references/references.json is blob-identical to {BASE_PIN}."
    ),
    "CS2b-cards-duplicates": (
        f"Re-run this round at {PIN} over the whole deck (198 objects, {R}/v1_cards_identity.out): 0 duplicate fronts "
        "(case-folded), 0 duplicate ids; CS2-c077 is absent at HEAD and CS2-c242 and CS2-c243 are present once each "
        "(lesson L06)."
    ),
    "CS2b7-cards-slice-identity": (
        f"Re-run this round at {PIN} ({R}/v1_cards_identity.out): the 73 L05-L08 card objects are canonically identical "
        f"to {BASE_PIN} (slice objects canonical-identical: True; changed slice objects: none). The only changed ids "
        "are CS2-c200 (L11), CS2-c231 (L10), CS2-c244 (L09), CS2-c245 (L11), outside this slice."
    ),
}

rows = []
for row in base["rows"]:
    rid = row["id"]
    if rid in FRESH:
        rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": "PASS",
                     "evidence": FRESH[rid]})
        continue
    if rid.startswith("CS2b-cards") or rid.startswith("CS2b4-cards"):
        prefix = f"Carried from round 7 ({CARRY_CARDS}):"
    else:
        prefix = f"Carried from round 7 ({CARRY_FILES}):"
    rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": "PASS",
                 "evidence": f"{prefix} {row['evidence']}"})

rows.append({
    "id": "CS2b1-delta-scope",
    "check": "Closing delta scope (ruling 30): git diff aa659725..95f3f8cb over the slice paths",
    "location": "course/modules/CS/CS2/ and tests/labs/CS2/ and tools/ notation/ references/ curriculum/ course/index.html",
    "status": "PASS",
    "evidence": (
        f"Re-run this round: git diff --name-status {BASE_PIN} {PIN} -- course/modules/CS/CS2 tests/labs/CS2 lists "
        "only 'M course/modules/CS/CS2/cards.json'. git diff --name-only over tools, notation, references, curriculum, "
        "course/index.html, course/concepts.html and course/assets/data lists no file. Blob hashes of the slice pages, "
        "twins, project.html, index, concepts, notation and references are identical at both pins (round-1 script "
        f"output in {R}/v1_blob_identity.out and {R}/v1_scope_diff.out). Slice content changed: none."
    ),
})

fragment = {
    "unit": "CS2",
    "slice": "b",
    "round": 1,
    "round_note": (
        f"Closing delta verification (rulings 30 and 37) of CS2 slice b at pin {PIN}. Base: the round-7 fragment "
        f"S-CS2-b.round7.json at pin {BASE_PIN}. Delta scope: git diff {BASE_PIN}..{PIN} over the slice paths changed "
        "only course/modules/CS/CS2/cards.json, at HEAD lines 1220, 1332-1333, 1415, 1423 (CS2-c200, c231, c244, c245; "
        "lessons L09, L11, L10, L11). No L05-L08 page, twin, or card object changed. All base rows were PASS. Gate rows "
        "and card rows whose subject touched cards.json were re-run; every other row is carried with its base evidence "
        "and the byte-identity statement."
    ),
    "verifier": "Haiku 5.5 independent verifier, CS2 slice b, closing delta (did not build CS2)",
    "pin": PIN,
    "base": f"{BASE_PIN} (round-7 pin; base fragment ~/.fanout/frags/S-CS2-b.round7.json)",
    "checkout": CHECKOUT,
    "scratch": f"{R}/ (v1_* files)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Ruling 37: a closing round writes no new mutants. The standing mutant set for this slice is empty: it is a "
        "lesson and card slice (no project grader; lab twins are demonstrations, ruling 9), so no mutants are listed.",
        "Not run: run_graders and mutate_graders (no grader in this slice); verify_refs live (references/ unchanged); "
        "check_pages --all and check_dag --all (unit-level runs used; other units are outside this slice).",
        "Outside this slice and not verified here (ruling 30 forbids new-defect hunting): the changed card texts "
        "CS2-c200 (L11), CS2-c231 (L10), CS2-c244 (L09), CS2-c245 (L11) in cards.json; the L04 and other unit changes "
        "in the same range.",
        "The tracked ledgers/CS2/CS2-b.json in this worktree was a round-8 fragment at pin ce7b382; it is replaced by "
        "this closing fragment in this worktree only.",
    ],
    "summary": (
        f"Slice b (L05-L08, twins, slice cards), closing delta at pin {PIN} against round-7 base {BASE_PIN}. "
        f"Rows: {len(rows)}, all PASS: {len(FRESH)} re-run this round (10 gates and the cards duplicate/identity checks), "
        f"{len(base['rows']) - len(FRESH)} carried from round 7 with byte-identity statements, 1 scope row. No slice subject changed; "
        "the only delta is cards.json outside L05-L08."
    ),
}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "verdict", fragment["verdict"])
