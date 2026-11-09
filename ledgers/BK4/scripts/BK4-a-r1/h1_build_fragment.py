import json
import subprocess
from datetime import UTC, datetime

BASE_PATH = "/Users/billyribeiro/.fanout/frags/G-BK4-a.round1.json"
OUT = "ledgers/BK4/scripts/BK4-a-r1/out/"
base = json.load(open(BASE_PATH, encoding="utf-8"))
CARRY = (
    "Carried from round 1 (the cited files: course/modules/BK/BK4/ index.html, L01-L03.html, cards.json and grader/ "
    "and project.html; tests/labs/BK4/; tools/; notation/; references/; curriculum/ are byte-identical since the previous "
    "pin 2a805c83; git diff --name-only 2a805c83 d9de2fe5 names none of them, see "
    "ledgers/BK4/scripts/BK4-a-r1/out/h1_changed_2a805c83_HEAD.txt and out/h1_cited_paths.txt): "
)

FRESH = {
    "BK4a9-cards-L01-L03": (
        "2.7-cards",
        "course/modules/BK/BK4/cards.json (L01 18, L02 24, L03 25 = 67 cards; L01 ids c001-c015, c091, c101, c106; "
        "L02 ids c016-c035, c092, c095, c099, c102; L03 ids c036-c041, c043, c044, c046-c058, c096, c104, c105, c107)",
        "PASS",
        "Re-verified from scratch this round. cards.json is byte-identical to 2a805c83 (git diff empty). "
        "ledgers/BK4/scripts/BK4-a-r1/h1_cards_recount.py (python -I) over cards.json, output "
        "ledgers/BK4/scripts/BK4-a-r1/h1_cards_recount.out: total 100; no duplicate id, front or back; per lesson "
        "L01 18, L02 24, L03 25, L04 19, L05 14. L01-L03 = 18+24+25 = 67. The defect was this row's own location "
        "string ('17+25+24=56' and 'ids c001..c105'): that sum is 66, not 56, and c106 (L01) and c107 (L03) lie "
        "outside c001..c105. The corrected location lists the true counts and id sets; each id set equals the "
        "recount output line for its lesson. Card contents are not changed by this fix (location text only, ruling 26 "
        "and the closing-delta rule for count text).",
    ),
    "BK4a-hub-concept-anchors": (
        "2.9-structure links",
        "course/modules/BK/BK4/index.html:63-66; L01.html:37; L02.html:37,275; L03.html:37",
        "PASS",
        "Re-verified this round at d9de2fe5. grep -o of course/concepts.html (unchanged since 2a805c83, git diff empty) "
        "finds id=\"clearing-and-settlement\", id=\"trade-lifecycle\" and id=\"bank-money-creation\" once each. "
        "index.html:63 carries data-concept for those three ids (grep -n). Pages checked by out/h1_check_pages_BK4.txt "
        "'check_pages BK4: PASS' and out/h1_check_dag_BK4.txt 'check_dag BK4: PASS' (exit 0 each).",
    ),
    "BK4a-L01-lab-twin": (
        "2.5-labs",
        "course/modules/BK/BK4/L01.html:128-287; tests/labs/BK4/lab-BK4-L01-1.py",
        "PASS",
        "Re-verified this round: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L01-1.py run from /tmp exits 0 "
        "(out/h1_fresh_L01.stdout); page code equals the twin up to the trailing newline (out/h1_twin_compare.txt); "
        "expected block equals the fresh run (out/h1_r9_check_lab_embeds.txt, out/h1_check_lab_embeds.txt); "
        "run_labs BK4 PASS (8/8) (out/h1_run_labs_BK4.txt).",
    ),
    "BK4a-L01-dag-defs": (
        "2.9-structure DAG",
        "course/modules/BK/BK4/L01.html:37,59,64",
        "PASS",
        "Re-verified this round: out/h1_check_dag_BK4.txt 'check_dag BK4: PASS', exit=0, covers the concept links at "
        "L01.html:37,59,64 and the dfn ids; L01.html is unchanged since 2a805c83 (git diff empty).",
    ),
    "BK4a-gate-check-pages": (
        "tools/check_pages.py --unit BK4",
        "tools/check_pages.py --unit BK4",
        "PASS",
        "Re-run this round at d9de2fe5: ledgers/BK4/scripts/BK4-a-r1/out/h1_check_pages_BK4.txt = 'check_pages BK4: PASS', exit=0.",
    ),
    "BK4a-gate-check-dag": (
        "tools/check_dag.py --unit BK4",
        "tools/check_dag.py --unit BK4",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_check_dag_BK4.txt = 'check_dag BK4: PASS', exit=0.",
    ),
    "BK4a7-gate-check-projects": (
        "tools/check_projects.py --unit BK4",
        "tools/check_projects.py --unit BK4",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_check_projects_BK4.txt = 'check_projects BK4: PASS', exit=0.",
    ),
    "BK4a-gate-run-labs": (
        "tools/run_labs.py --unit BK4",
        "tools/run_labs.py --unit BK4",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_run_labs_BK4.txt = 'run_labs BK4: PASS (8/8)', exit=0.",
    ),
    "BK4a-gate-page-smoke": (
        "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03",
        "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_page_smoke_BK4.txt shows PASS for modules/BK/BK4/index.html, L01.html, "
        "L02.html, L03.html and 'page_smoke BK4: PASS', exit=0.",
    ),
    "BK4a-gate-ruff-mypy": (
        "ruff check tests/labs/BK4; ruff format --check tests/labs/BK4; mypy --no-incremental tests/labs/BK4",
        "ruff check tests/labs/BK4; ruff format --check tests/labs/BK4; mypy --no-incremental tests/labs/BK4",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_ruff_mypy_BK4.txt: 'All checks passed!' (exit 0); '8 files already "
        "formatted' (exit 0); 'Success: no issues found in 8 source files' (exit 0).",
    ),
    "BK4a-gate-repo-ruff-mypy-r4": (
        "tests/labs/BK4 (ruff check, ruff format --check, mypy --no-incremental)",
        "tests/labs/BK4 (ruff check, ruff format --check, mypy --no-incremental)",
        "PASS",
        "Same commands as BK4a-gate-ruff-mypy, re-run this round: out/h1_ruff_mypy_BK4.txt, all three exit 0.",
    ),
    "BK4a-gate-pytest-labs": (
        "pytest tests/test_labs.py -k BK4; pytest tests/test_page_checks.py",
        "pytest tests/test_labs.py -k BK4; pytest tests/test_page_checks.py",
        "PASS",
        "Re-run this round at d9de2fe5: out/h1_pytest_BK4.txt: test_labs.py -k BK4 8 dots [100%] exit=0; "
        "test_page_checks.py 41 dots [100%] exit=0.",
    ),
    "BK4a-gate-verify-refs": (
        "tools/verify_refs.py --offline; tools/verify_refs.py --unit BK4 (live part carried)",
        "tools/verify_refs.py --offline; tools/verify_refs.py --unit BK4 (live part carried)",
        "PASS",
        "Offline re-run this round: out/h1_verify_refs_offline.txt 'offline integrity: 560 entries, 0 problems', exit=0. "
        "The live --unit BK4 run is network and was not repeated; its earlier PASS is carried because "
        "references/references.json and the BK4 pages are byte-identical since 2a805c83.",
    ),
    "BK4a10-gates": (
        "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, page_smoke.py, verify_refs.py --offline",
        "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, page_smoke.py, verify_refs.py --offline",
        "PASS",
        "All re-run this round at d9de2fe5 (out/h1_*.txt, each exit 0). run_graders.py not run: slice a has no project "
        "grader, and BK4 grader/ and project.html are absent from git diff 2a805c83..d9de2fe5.",
    ),
    "BK4a-lab-block-equality-r4": (
        "tests/labs/BK4 twins vs course/modules/BK/BK4/L01-L03.html lab blocks",
        "tests/labs/BK4 twins vs course/modules/BK/BK4/L01-L03.html lab blocks",
        "PASS",
        "Re-run this round: ledgers/BK4/scripts/BK4-a-r10/check_lab_embeds.py (unchanged since 2a805c83) over the checkout "
        "root, output out/h1_check_lab_embeds.txt: for L01, L02 and L03 'expected block equals fresh stdout: True' and "
        "'run exit 0'; stdout lines equal expected lines (32, 29, 28). Page code vs twin differs only by the one trailing "
        "newline that tools/embed_labs.py drops (embed_labs.py:97,117); out/h1_twin_compare.txt: equal after trailing-newline "
        "strip: True for all three.",
    ),
    "BK4a9-lab-embed-r9": (
        "ledgers/BK4/scripts/BK4-a-r9/check_lab_embeds.py",
        "ledgers/BK4/scripts/BK4-a-r9/check_lab_embeds.py",
        "PASS",
        "Re-run this round with the r9 script itself (checkout root plus id=path of each fresh twin stdout, "
        "out/h1_fresh_L0n.stdout, from python -I -W error run in /tmp): out/h1_r9_check_lab_embeds.txt shows "
        "'expected block equals a fresh run output: True' for L01, L02 and L03. Its page-code line reads False only "
        "because the twin ends with one newline that tools/embed_labs.py drops (embed_labs.py:117); "
        "out/h1_twin_compare.txt: equal after trailing-newline strip for all three.",
    ),
    "BK4a10-lab-embed": (
        "ledgers/BK4/scripts/BK4-a-r10/check_lab_embeds.py",
        "ledgers/BK4/scripts/BK4-a-r10/check_lab_embeds.py",
        "PASS",
        "Re-run this round (out/h1_check_lab_embeds.txt): 'expected block equals fresh stdout: True' for L01, L02, L03; "
        "page code equals twin up to the trailing newline (out/h1_twin_compare.txt).",
    ),
    "BK4a10-lab-run": (
        "tests/labs/BK4/lab-BK4-L0[123]-1.py",
        "tests/labs/BK4/lab-BK4-L0[123]-1.py",
        "PASS",
        "Re-run this round: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L0n-1.py from the checkout, exit 0 for L01, "
        "L02, L03 (stdout 1618, 1284, 3059 bytes; stderr empty).",
    ),
    "BK4a5-twins-alone": (
        "tests/labs/BK4/lab-BK4-L01-1.py; lab-BK4-L02-1.py; lab-BK4-L03-1.py",
        "tests/labs/BK4/lab-BK4-L01-1.py; lab-BK4-L02-1.py; lab-BK4-L03-1.py",
        "PASS",
        "Re-run this round, each twin alone with python -I -W error: exit 0 for all three (see BK4a10-lab-run).",
    ),
    "BK4a10-recompute": (
        "ledgers/BK4/scripts/BK4-a-r10/recompute_numbers.py",
        "ledgers/BK4/scripts/BK4-a-r10/recompute_numbers.py",
        "PASS",
        "Re-run this round over the checkout root (out/h1_recompute_numbers.txt): 81 lines begin 'PASS', no other line, exit=0.",
    ),
    "BK4a9-recompute-r9": (
        "ledgers/BK4/scripts/BK4-a-r9/recompute_numbers.py",
        "ledgers/BK4/scripts/BK4-a-r9/recompute_numbers.py",
        "PASS",
        "Re-run this round with the r9 script itself over the checkout root: out/h1_r9_recompute_numbers.txt, every line "
        "'OK' (ALL OK), exit=0. The script is unchanged since 2a805c83 (not in the changed-file list).",
    ),
    "BK4a10-delta-hunks": (
        "delta since c93dd52 (re-verified against 95f3f8cb..2a805c83; closing delta 2a805c83..d9de2fe5 re-checked)",
        "course/modules/BK/BK4/L03.html:565; course/modules/BK/BK4/cards.json (hunks @@ -114 and @@ -684 in the "
        "95f3f8cb..HEAD diff; none at 562); L05.html:486 (Example 2.7 line)",
        "PASS",
        "Re-checked this round: git diff --name-only 2a805c83 d9de2fe5 names no file under course/modules/BK/BK4, "
        "tests/labs/BK4, tools, notation, references or curriculum (out/h1_changed_2a805c83_HEAD.txt). The 2a805c83 "
        "hunks in L04.html and L05.html and cards.json (BK4-c014, BK4-c088) are the ones checked in rows BK4a-r1-card-*.",
    ),
}

rows = []
carried = 0
for r in base["rows"]:
    if r["id"] in FRESH:
        check, location, status, evidence = FRESH[r["id"]]
        rows.append({"id": r["id"], "check": check, "location": location, "status": status, "evidence": evidence})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS base row not re-verified: {r['id']}")
    carried += 1
    rows.append({
        "id": r["id"],
        "check": r["check"],
        "location": r["location"],
        "status": "PASS",
        "evidence": CARRY + r["evidence"],
    })

rows.append({
    "id": "BK4a-delta-2a805c83-d9de2fe5-scope",
    "check": "2.9-structure delta scope",
    "location": "git diff 2a805c83..d9de2fe5 over course/modules/BK/BK4, tests/labs/BK4, tools, notation, references, curriculum",
    "status": "PASS",
    "evidence": "git diff --stat 2a805c83 d9de2fe5 over those paths prints nothing (exit 0). The full 2a805c83..HEAD list "
                "(out/h1_changed_2a805c83_HEAD.txt, 676 files) touches only other units (CS2, E2, E3, E5, M2, M4, M6 course "
                "pages and cards; CS2 project and grader), ledger artifacts, plans/E3-open-items.md, "
                "plans/FINAL-ARCHITECT-RULINGS.md and the tests/labs CS2, E3 and E5 twins. No course/modules/BK or tests/labs/BK4 file is in the list. "
                "No BK4 slice-a row cites a ruling or an E3/CS2/E5 file (grep of the base rows), so rulings 38a, 39 and 40 "
                "do not reach this slice.",
})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)) == len(base["rows"]) + 1, "row ids must be kept and unique"

counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows)}
fragment = {
    "unit": "BK4",
    "slice": "a",
    "round": 1,
    "round_note": "Closing delta verification (ruling 30) of slice a from base fragment "
                  "~/.fanout/frags/G-BK4-a.round1.json (pin 2a805c83). Ruling 37: no new mutants. Ruling 26: FAIL kinds only. "
                  "Verifier H1 (independent, Haiku 5.5).",
    "verifier": "independent verifier H1 (Haiku 5.5), BK4 slice a closing delta round 1",
    "pin": "d9de2fe5eea982d14cd9f922a61676b847506fbc",
    "base": "2a805c831410ab77c38c227f7e121e8537193ce9 (base fragment ~/.fanout/frags/G-BK4-a.round1.json, verdict FAIL, "
            "146 rows, one FAIL row BK4a9-cards-L01-L03 whose defect is its own location text)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyH1-BK4-a",
    "scratch": "ledgers/BK4/scripts/BK4-a-r1/ (h1_* scripts; out/h1_* outputs)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts["FAIL"] == 0 and counts["PASS"] == len(rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Delta 2a805c83..d9de2fe5 (git diff --name-only): no file under course/modules/BK/BK4, tests/labs/BK4, tools, "
        "notation, references, curriculum, or the BK4 grader and project.html changed. Every slice-a row subject is "
        "byte-identical to the base pin, so the only re-verified row is the base's non-PASS row BK4a9-cards-L01-L03, and "
        "the slice gates were re-run.",
        "The base's FAIL row BK4a9-cards-L01-L03 was a location-text defect (ruling 30 and the count-text rule): its "
        "location said 17+25+24=56 and ids c001..c105; the file holds 18+24+25=67 with c106 and c107 outside that range. "
        "Recounted and corrected; no card content changed.",
        "Observation (not a ruling-26 kind, carried): BK4-c106 (L01, 'gross value of a day's payments') has no grade and "
        "no basis. BUILDER_RULES section 7 requires a grade only for a graded result, so a definitional card without a grade "
        "is accepted by check_pages; not a finding.",
        "Observation (carried): BK4-c032 paraphrases the Crossref title with the defined abbreviation CCP; L02.html:277 uses "
        "the same wording.",
        "Lab twin convention: the page code block drops the twin's single trailing newline by design (embed_labs.py:97,117); "
        "not a finding.",
        "Not checked: verify_refs --unit BK4 live run (network; not repeated; carried); run_graders and mutate_graders (no "
        "project grader in slice a; ruling 37 writes no mutants); full pytest suite (targeted gates only, per the "
        "test-what-changed rule); line-by-line re-read of index.html, L01-L03.html (not required: no byte changed since "
        "2a805c83, and only FAIL and changed-subject rows are re-verified under ruling 30); the L04/L05 slice-b/c content "
        "(not slice a).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "carried": carried,
        "fresh_or_new": len(rows) - carried,
        "mutants": 0,
    },
}
json.dump(fragment, open("ledgers/BK4/BK4-a.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open("ledgers/BK4/BK4-a.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "carried", carried, "verdict", fragment["verdict"])
