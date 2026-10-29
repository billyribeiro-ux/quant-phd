import json, sys
ROOT = sys.argv[1]
prev = json.load(open("/tmp/fanout-frags/AC4-b.round22.json", encoding="utf-8"))
O = "ledgers/AC4/scripts/AC4-b-r23/out/"
RERUN = {
    "AC4b-cmd-check_pages", "AC4b-cmd-check_dag", "AC4b-cmd-run_labs", "AC4b-cmd-twins-isolated",
    "AC4b-cmd-page_smoke", "AC4b-cmd-ruff-mypy", "AC4b-cmd-verify_refs", "AC4b-cmd-pytest", "AC4b-cmd-pin",
    "AC4b-cards-L03-L04", "AC4b-hours-L03-L04",
}
PAGE_PREFIX = ("Carried from round 22 (course/modules/AC/AC4/L03.html, course/modules/AC/AC4/L04.html, "
               "tests/labs/AC4/lab-AC4-L03-1.py, tests/labs/AC4/lab-AC4-L04-1.py byte-identical since the previous pin "
               "fefbf8b; references/references.json and tools/ identical): ")
CARD_IDS = {"AC4-c032", "AC4-c033", "AC4-c038", "AC4-c040", "AC4-c041", "AC4-c042", "AC4-c043", "AC4-c044",
            "AC4-c045", "AC4-c050", "AC4-c053", "AC4-c057", "AC4-c058", "AC4-c121", "AC4-c122", "AC4-c123",
            "AC4-c124", "AC4-c126", "AC4-c131"}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        continue
    r = dict(r)
    if rid.startswith("AC4b17-cards") or rid.startswith("AC4b4-cards") or rid.startswith("AC4b6-cards"):
        r["evidence"] = ("Carried from round 22 (the card objects named in this row are byte-identical to fefbf8b in "
                         "course/modules/AC/AC4/cards.json; checked by object comparison, see "
                         "ledgers/AC4/scripts/AC4-b-r23/out/card_identity.out): " + r["evidence"])
    elif rid == "AC4b-cards-L03-L04" or rid == "AC4b-hours-L03-L04":
        continue
    else:
        r["evidence"] = PAGE_PREFIX + r["evidence"]
    rows.append(r)

def row(rid, check, location, evidence, status="PASS", fix=""):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    rows.append(d)

row("AC4b-cmd-pin", "2.9-structure", "git HEAD of /tmp/verify23-AC4-b",
    "HEAD 503d13980b2ad23201063107a2d6844e00b23d6d (detached). Previous pin fefbf8b. "
    "git diff --stat fefbf8b 503d139 for the slice: L03.html, L04.html, lab-AC4-L03-1.py, lab-AC4-L04-1.py, "
    "references/references.json and tools/run_labs.py, page_smoke.py, check_pages.py, verify_refs.py are byte-identical; "
    "changed: course/modules/AC/AC4/cards.json (cards c037 changed, c136 new), course/assets/data/program.json "
    "(CS2 prerequisite M1, out of slice), course/modules/AC/AC4/index.html (hub lede, out of slice).")
row("AC4b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC4",
    "Run this round: " + O + "check_pages.out 'check_pages AC4: PASS', exit 0.")
row("AC4b-cmd-check_dag", "DAG/concepts", "tools/check_dag.py --unit AC4",
    "Run this round: " + O + "check_dag.out 'check_dag AC4: PASS', exit 0.")
row("AC4b-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4",
    "Run this round: " + O + "run_labs.out 'run_labs AC4: PASS (10/10)', exit 0.")
row("AC4b-cmd-twins-isolated", "2.5-labs",
    "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py under python -I -W error",
    "Run this round: " + O + "twin_L03.out and twin_L04.out, both exit 0, empty stderr (twin_L03.err, twin_L04.err). "
    "Each non-blank printed line of both twins appears verbatim in the page text: " + O + "page_vs_twin.out "
    "(L03 36 lines, L04 38 lines, 0 missing).")
row("AC4b-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L03 L04",
    "Run this round: " + O + "page_smoke.out. L03 PASS, L04 PASS, lab 0.0 s each, 'page_smoke AC4: PASS', exit 0.")
row("AC4b-cmd-ruff-mypy", "gates", "ruff check, ruff format --check on tests/labs/AC4; mypy --no-incremental on the two twins",
    "Run this round: " + O + "ruff.out 'All checks passed!' and '10 files already formatted', exit 0; "
    + O + "mypy.out 'Success: no issues found in 2 source files', exit 0.")
row("AC4b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit AC4 (live) and tools/verify_refs.py --offline",
    "Run this round: " + O + "vr_live.out 'live re-verification of AC4: 2 of 560 entries, 0 problems', exit 0; "
    + O + "vr_offline.out 'offline integrity: 560 entries, 0 problems', exit 0. Live run did not reach the registry "
    "for the other 558 entries (the tool checks 2 for AC4).")
row("AC4b-cmd-pytest", "gates", "pytest tests/test_labs.py tests/test_page_checks.py -k AC4 -q",
    "Run this round: " + O + "pytest.out, ten test dots, exit 0.")
row("AC4b-cards-L03-L04", "2.7-cards",
    "course/modules/AC/AC4/cards.json, cards with lesson L03 or L04 (35 cards now)",
    "Re-verified this round. Cards with lesson L03 or L04: 35 (" + O + "card_numbers.out lists them). Changed since "
    "fefbf8b: AC4-c037 (back rewritten, see AC4b23-cards-c037) and new AC4-c136 (see AC4b23-cards-c136). The other 33 "
    "L03/L04 card objects are byte-identical (object comparison, " + O + "card_identity.out). Fronts and ids unique across the "
    "whole file (" + O + "card_identity.out).")
row("AC4b23-cards-c037", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c037; course/modules/AC/AC4/L03.html lines 63-69 (Proposition 1.2)",
    "Back: 'Yes, for every common cost. The two totals differ by the difference of their relevant costs, so the common cost "
    "cancels from the comparison (Proposition 1.2).' Proposition 1.2 (L03 line 65) takes any K, sets T_A - T_B = R_A - R_B, "
    "and its proof (line 66) shows K cancels for any value; so 'every common cost' is the proposition's own scope. "
    "Grade T is correct: proved on the page. The removed sentence about Remark 1.3 now sits in AC4-c136.")
row("AC4b23-cards-c136", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c136; course/modules/AC/AC4/L03.html line 74 (Remark 1.3)",
    "Back: 'No. Proposition 1.2 ranks the alternatives and does not give the profit of either one (Remark 1.3).' L03 "
    "line 74 reads 'Proposition 1.2 ranks the alternatives. It does not give the profit of either one.' Matches. "
    "Grade T, proved on the page. No number and no banned word in the front or back.")
row("AC4b23-card-identity", "2.7-cards", "course/modules/AC/AC4/cards.json (object comparison against fefbf8b)",
    "ledgers/AC4/scripts/AC4-b-r23/card_identity.py run with the checkout's cards.json and "
    "git show fefbf8b:course/modules/AC/AC4/cards.json: " + O + "card_identity.out. Changed ids in the whole file: 15 "
    "(c007, c008, c018, c020, c037, c061, c074, c082, c089, c093, c095, c096, c108, c113, c125; none is an L03/L04 card "
    "except c037); new ids: c135 to c140 (c136 is L03). No id removed.")
row("AC4b23-card-numbers", "2.7-cards", "course/modules/AC/AC4/cards.json L03/L04 cards vs L03.html, L04.html, the twins",
    "ledgers/AC4/scripts/AC4-b-r23/card_numbers.py output " + O + "card_numbers.out: every number in every L03/L04 card "
    "appears as text in its lesson page or in its twin's source. Substring match only (a weak check); the numbers "
    "themselves were re-derived in earlier rows and are unchanged here.")
row("AC4b23-prose-changed-cards", "2.9-structure", "course/modules/AC/AC4/cards.json AC4-c037, AC4-c136",
    "Banned-phrase scan of the two changed or new card texts (roughly, about, historically, typically, usually, generally, "
    "often, half, ellipsis, build, round, verifier, always, only): none present. 'every' in c037 is backed by Proposition 1.2 "
    "(any K).")
row("AC4b-hours-L03-L04", "hours", "course/modules/AC/AC4/L03.html and L04.html data-hours and eyebrow; course/modules/AC/AC4/index.html line 29", "Re-verified this round: L03 and L04 declare data-hours=\"6\" (lines 2) and eyebrow '6 study hours' (L04 line 34). Sum of the eight lesson declarations is 50, equal to index.html data-hours-lessons=\"50\". Arithmetic consistent; no pace estimate failed (architect ruling).")
row("AC4b23-hub-hours", "hours", "course/modules/AC/AC4/L01..L08.html data-hours; course/modules/AC/AC4/index.html line 29",
    "Re-run this round: data-hours 6,7,6,6,7,6,6,6 for L01..L08 sum to 50, equal to index.html data-hours-lessons=\"50\", "
    "plus data-hours-project=\"20\" gives 70, equal to 'Module AC4 · Tier U · 70 hours' (index.html line 31). The hub "
    "lede changed (line 33) and the hub is outside this slice (no L03/L04 claim changed). Hours are design targets "
    "(architect ruling): no pace estimate failed.")
row("AC4b23-slice-delta", "2.9-structure", "git diff fefbf8b 503d139 -- course/modules/AC/AC4 tests/labs/AC4 references tools",
    "Slice-relevant changes: cards.json only (and the hub, out of slice). L03.html, L04.html, the twins, references.json and "
    "the four tool scripts used here are byte-identical. Changed outside the slice: project.html, grader/test_project.py, "
    "L01/L02/L05..L08 pages, AC4 labs L05..L08, AC1 files, course/assets/data/program.json (CS2 prerequisite M1). "
    "Those are not verified in this slice.")

prev_ids = [r["id"] for r in prev["rows"]]
new_ids = [r["id"] for r in rows]
missing_ids = [i for i in prev_ids if i not in new_ids]
assert not missing_ids, missing_ids
fragment = {
    "unit": "AC4",
    "slice": "AC4-b",
    "round": 23,
    "verifier": "round-23 independent verifier (Haiku) for slice AC4-b: L03, L04 and their lab twins; did not build AC4 "
                "and shares no context with the builders or earlier verifiers",
    "pin": "503d13980b2ad23201063107a2d6844e00b23d6d",
    "base": "fefbf8b (previous pin; L03, L04 and the twins byte-identical since)",
    "checkout": "/tmp/verify23-AC4-b (detached worktree at 503d139; .venv symlink; vendor copied)",
    "scratch": "/tmp/AC4-v/AC4-b/ (round-17 scratch files reused for carried number rows; round-23 outputs under ledgers/AC4/scripts/AC4-b-r23/out/)",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "rows": rows,
    "mutants": [],
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Lesson-and-twin slice: no grader or project file in scope, so no student-error mutants and no alternative implementations were written (the brief reserves both for project slices).",
        "Twins are demonstrations: a mutated twin that still exits 0 is out of scope (architect ruling); none was written.",
        "Carried rows cite L03.html, L04.html, the twins, references.json and tools that are byte-identical to fefbf8b (git diff verified). Their subjects were not re-read this round, but their evidence is carried with the prefix required by the brief.",
        "Registry flags carried unchanged: datar2020horngrens (year 2020 record vs 17th ed. 2021 source string) and kaplan1998cost (author list). Both are open issues in references/references.json, not failures of the slice.",
        "Card AC4-c037 changed back text but kept grade T; the Remark 1.3 sentence moved to AC4-c136.",
    ],
}
fails = [r["id"] for r in rows if r["status"] != "PASS"]
fragment["summary"] = {"rows": len(rows), "pass": len(rows) - len(fails), "fail": len(fails),
                       "unverifiable": 0, "fail_ids": fails}
fragment["verdict"] = "PASS" if not fails else "FAIL"
json.dump(fragment, open("ledgers/AC4/AC4-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(fragment["summary"], fragment["verdict"])
