"""Build ledgers/LX1/LX1-b.json (round 1, closing delta) from the round-23 base fragment.

Rows re-verified this round carry fresh evidence (gate runs, re-read subjects, plain curl). Every other base row is carried
with the carry prefix: its cited subject files are byte-identical between the base pin dde0486b and the pin 95f3f8cb
(see out/delta_identity_r1.out). Run as: python -I write_fragment_r1.py <checkout_root> <base_fragment_path>.
"""

import datetime
import json
import sys

ROOT, BASE = sys.argv[1], sys.argv[2]
OUT = f"{ROOT}/ledgers/LX1/scripts/LX1-b-r1/out"
SCR = "ledgers/LX1/scripts/LX1-b-r1/out"

base = json.load(open(BASE, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

fresh = {
    "lx1b-check-pages": (
        "2.9-structure",
        "course/modules/LX/LX1/L01.html; L03.html; L04.html",
        f"tools/check_pages.py --unit LX1 -> 'check_pages LX1: PASS', exit 0 ({SCR}/check_pages.out)",
    ),
    "lx1b-check-dag": (
        "2.9-dag",
        "course/modules/LX/LX1/L01.html; L03.html; L04.html",
        f"tools/check_dag.py --unit LX1 -> 'check_dag LX1: PASS', exit 0 ({SCR}/check_dag.out)",
    ),
    "lx1b-check-projects": (
        "2.6-projects",
        "tools/check_projects.py --unit LX1",
        f"tools/check_projects.py --unit LX1 -> 'check_projects LX1: PASS', exit 0, run after the delta that changed "
        f"course/modules/LX/LX1/project.html (slice a C1 row) ({SCR}/check_projects.out)",
    ),
    "lx1b-run-graders": (
        "2.6-autograder",
        "tools/run_graders.py --unit LX1",
        f"tools/run_graders.py --unit LX1 -> 'no autograder (grading: rubric)', exit 0 ({SCR}/run_graders.out)",
    ),
    "lx1b-run-labs": (
        "2.5-labs",
        "tests/labs/LX1/lab-LX1-L01-1.py; lab-LX1-L03-1.py; lab-LX1-L04-1.py",
        f"tools/run_labs.py --unit LX1 -> 'run_labs LX1: PASS (7/7)', exit 0 ({SCR}/run_labs.out)",
    ),
    "lx1b-twin-alone-L01": (
        "2.5-labs",
        "tests/labs/LX1/lab-LX1-L01-1.py",
        f"copied to a fresh scratch dir /tmp/lx1b-r1-L01 with data/fx_monthly.csv; python -I -W error "
        f"tests/labs/LX1/lab-LX1-L01-1.py -> exit 0, stderr 0 bytes ({SCR}/twin_L01.out, twin_L01.err)",
    ),
    "lx1b-twin-alone-L03": (
        "2.5-labs",
        "tests/labs/LX1/lab-LX1-L03-1.py",
        f"fresh scratch dir /tmp/lx1b-r1-L03; python -I -W error tests/labs/LX1/lab-LX1-L03-1.py -> exit 0, "
        f"stderr 0 bytes ({SCR}/twin_L03.out, twin_L03.err)",
    ),
    "lx1b-twin-alone-L04": (
        "2.5-labs",
        "tests/labs/LX1/lab-LX1-L04-1.py",
        f"fresh scratch dir /tmp/lx1b-r1-L04 with data/fx_monthly.csv (byte-identical to the repo file, cmp); python -I "
        f"-W error tests/labs/LX1/lab-LX1-L04-1.py -> exit 0, stderr 0 bytes ({SCR}/twin_L04.out, twin_L04.err)",
    ),
    "lx1b-twin-equals-page-code": (
        "2.5-labs",
        "course/modules/LX/LX1/L01.html, L03.html, L04.html code and expected blocks vs twins",
        f"ledgers/LX1/scripts/LX1-b-r23/twin_page_compare_r23.py run on this checkout with the r1 twin stdout: "
        f"'L01 code==twin True ... expected==stdout True', same for L03 and L04, 'ALL True' ({SCR}/twin_page_compare_r1.out)",
    ),
    "lx1b-page-smoke-L01": (
        "2.9-smoke",
        "course/modules/LX/LX1/L01.html",
        f"tools/page_smoke.py --unit LX1 --pages modules/LX/LX1/L01.html -> 'page_smoke LX1: PASS', exit 0 ({SCR}/page_smoke_L01.out)",
    ),
    "lx1b-page-smoke-L03": (
        "2.9-smoke",
        "course/modules/LX/LX1/L03.html",
        f"tools/page_smoke.py --unit LX1 --pages modules/LX/LX1/L03.html -> 'page_smoke LX1: PASS', exit 0 ({SCR}/page_smoke_L03.out)",
    ),
    "lx1b-page-smoke-L04": (
        "2.9-smoke",
        "course/modules/LX/LX1/L04.html",
        f"tools/page_smoke.py --unit LX1 --pages modules/LX/LX1/L04.html -> 'page_smoke LX1: PASS', exit 0 ({SCR}/page_smoke_L04.out)",
    ),
    "lx1b-ruff-mypy": (
        "2.5-labs",
        "tests/labs/LX1/*.py",
        f"ruff check tests/labs/LX1 -> 'All checks passed!', exit 0; ruff format --check -> '7 files already formatted', exit 0; "
        f"mypy --no-incremental on the three LX1 twins -> 'Success: no issues found in 3 source files', exit 0 "
        f"({SCR}/ruff_check.out, ruff_format.out, mypy.out)",
    ),
    "lx1b-pytest": (
        "2.5-labs",
        "tests/test_labs.py",
        f"python -m pytest tests/test_labs.py -q -k LX1 -> 7 tests passed (seven dots), exit 0 ({SCR}/pytest_labs_LX1.out)",
    ),
    "lx1b-verify-refs": (
        "2.1-citations",
        "references/references.json; tools/verify_refs.py",
        f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({SCR}/verify_refs_offline.out). "
        f"Live run not repeated: references/ and tools/ byte-identical since dde0486b (out/delta_identity_r1.out)",
    ),
    "lx1b-fetch-check": (
        "2.8-data",
        "course/assets/data/market/fx_monthly.csv; MANIFEST.json",
        f"tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems', exit 0 ({SCR}/fetch_check.out)",
    ),
    "lx1b-fx-licence": (
        "2.8-data",
        "tools/data_sources.yaml fx_monthly; MANIFEST licence_url",
        f"plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200 ({SCR}/fed_disclaimer_r1.curl, "
        f"{SCR}/fed_disclaimer_r1.html); the page contains 'Unless otherwise indicated, information on Board's website is in "
        f"the public domain and may be copied and distributed without permission. Please cite to the Board as the source of "
        f"the information.', matching the quoted licence in tools/data_sources.yaml and MANIFEST",
    ),
    "lx1b-r20-licence-page-curl": (
        "2.8-data",
        "https://www.federalreserve.gov/disclaimer.htm (plain curl)",
        f"plain curl -sS -L https://www.federalreserve.gov/disclaimer.htm -> HTTP 200, curl exit 0 ({SCR}/fed_disclaimer_r1.curl); "
        f"licence sentence present in {SCR}/fed_disclaimer_r1.html",
    ),
    "lx1b-num-L01-lab-output": (
        "2.5-labs",
        "course/modules/LX/LX1/L01.html:244-282 (expected block) vs twin stdout",
        f"ledgers/LX1/scripts/LX1-b-r23/twin_page_compare_r23.py on the r1 twin stdout: 'L01 ... expected==stdout True' "
        f"({SCR}/twin_page_compare_r1.out); twin_L01.out exit 0 ({SCR}/twin_L01.out)",
    ),
    "lx1b-plan-coverage": (
        "2.9-structure",
        "plans/LX1-build-plan.md §2.1, §3; plans/FINAL-ARCHITECT-RULINGS.md rulings 14, 16",
        "plans/LX1-build-plan.md byte-identical since dde0486b (out/delta_identity_r1.out). The rulings file changed only by "
        "the hunk @@ -96,0 +97,40 @@ (rulings 30-37 appended); sha1 of lines 32-37 (ruling 14) and 38-41 (ruling 16) equal "
        "at dde0486b and 95f3f8cb. Re-read: ruling 14 'definition pending' dfn for bretton-woods-system; ruling 16 "
        "'P_t is the price level of L02, L03 and the project. L01's observed asset price is A_t'. L04.html:86 carries the "
        "definition-pending dfn; L01.html uses A_t (:105, :144, :145, :451)",
    ),
    "lx1b-delta-hunks": (
        "2.9-structure",
        "git diff dde0486b 95f3f8cb (slice b paths)",
        "git diff --quiet dde0486b HEAD over course/modules/LX/LX1/{L01,L03,L04,cards.json,index.html}, tests/labs/LX1, "
        "plans/LX1-build-plan.md, plans/LX1-open-items.md, references, tools, curriculum, notation, course/assets/data, "
        "course/concepts.html, course/index.html: all IDENTICAL (out/delta_identity_r1.out). Changed in the delta and outside "
        "slice b: course/modules/LX/LX1/project.html (slice a, C1 row), plans/KNOWN-ISSUES.md (appended, other units), "
        "plans/FINAL-ARCHITECT-RULINGS.md (rulings 30-37 appended), tests/test_lx1_project_lab3.py (new, slice a), other units' "
        "files. Slice b has no changed subject, so no row is re-verified for a subject change.",
    ),
    "lx1b-delta-r21": (
        "2.9-structure",
        "git diff dde0486b 95f3f8cb; plans/FINAL-ARCHITECT-RULINGS.md:74-80",
        "Ruling 26 text at lines 74-80 is byte-identical at dde0486b and 95f3f8cb (sha1 e317705197e3 both, out/delta_identity_r1.out); "
        "the rulings-file hunk is at line 97 and later. Ruling 30 (delta verification closes a fixed slice) and ruling 37 (closing "
        "round writes no new mutants) are read in full and applied. The round-21 FAIL rows are carried as PASS in the base "
        "and their subjects are unchanged since dde0486b.",
    ),
    "lx1b-mutants-none": (
        "2.6-mutation",
        "tests/labs/LX1/*; course/modules/LX/LX1/project.html (slice a)",
        "Slice b has no mutants (rubric and lab pages; ruling 23). ledgers/LX1/mutants holds 94 files: 70 lx1c_* (slice c) and "
        "24 r12-r19 project-lab-3 files (slice a/c), none of slice b; they are not run by this slice. Ruling 37: no new "
        "mutants are written in this closing round.",
    ),
}

rows = []
carried_n = 0
for rid, b in base_rows.items():
    if rid in fresh:
        check, loc, ev = fresh[rid]
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    else:
        assert b["status"] == "PASS", rid
        carried_n += 1
        rows.append(
            {
                "id": rid,
                "check": b["check"],
                "location": b["location"],
                "status": "PASS",
                "evidence": (
                    f"Carried from round 23 ({b['location']} byte-identical since the previous pin dde0486b): "
                    + b["evidence"]
                ),
            }
        )

missing = set(fresh) - set(base_rows)
assert not missing, missing

frag = {
    "unit": "LX1",
    "slice": "b",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for LX1-b, round 1 (closing delta, rulings 30 and 37)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "dde0486b (round-23 fragment ~/.fanout/frags/E-LX1-b.round23.json, verdict PASS, 93 rows, 0 non-PASS)",
    "checkout": ROOT,
    "scratch": "/tmp/lx1b-r1-L01, /tmp/lx1b-r1-L03, /tmp/lx1b-r1-L04 (created for the twin runs)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Closing delta (ruling 30) from the round-23 base pin dde0486b to 95f3f8cb. Every slice-b subject (L01, L03, L04, index.html, "
        "cards.json, tests/labs/LX1, plans/LX1-*, references, tools, curriculum, notation, course/assets/data, course/concepts.html, "
        "course/index.html) is byte-identical to the base (out/delta_identity_r1.out). The base had 0 non-PASS rows, so no row was "
        "re-verified for a non-PASS status. Rows re-verified: the gate rows, the rows citing the rulings file or the project page, and "
        "the two plain-curl licence rows. All other rows are carried with the carry prefix.",
        "Ruling 37: no mutants were written in this round. Slice b has no mutants (base mutants: []); the standing set for this slice is empty.",
        "Outside slice b and not verified here: course/modules/LX/LX1/project.html (C1 row, slice a); tests/test_lx1_project_lab3.py "
        "(new, slice a); plans/KNOWN-ISSUES.md appended sections (other units; its LX1 registry lines agree with registry_flags); "
        "ledgers/LX1/mutants/r12-r19 files (project lab 3, slice a/c).",
        "LOW, not a ruling-26 kind, carried from the base as a note (not a FAIL): L04.html:333 uses 'spot rate' for the FX rate of the "
        "data register note; the concept spot-rate (FI1) is a different object. Not recorded in plans/KNOWN-ISSUES.md; the verifier does not edit plans.",
        "LOW, not a ruling-26 kind, carried from the base as a note (not a FAIL): L04.html:59 labels the positivity of Definition 1.1 as "
        "Assumption (A1), a label first stated in Proposition 1.2 (L04.html:85). Forward label only.",
        "Quiz and number re-derivation re-run this round: ledgers/LX1/scripts/LX1-b-r23/quiz_numbers_r23.py with the checkout root, output "
        f"byte-identical to the base output ({SCR}/quiz_numbers_r1.out vs LX1-b-r23/out/quiz_numbers_r23.out). The L01:445 q >= 1 step "
        "(the round-21 fix) reads: q = (1+g)/(1+r) >= 1 when g >= r and r > -1, so the terms are at least d1/(1+r) > 0 and the partial "
        "sums tend to +infinity (Proposition 1.4).",
        "Blind calibration: none in slice b. LX1-b is a lab and page slice with no rubric exemplar; the rubric calibration belongs "
        "to slice c (blind scorer file ~/.fanout/blind/LX1-c.json, not part of this slice).",
        "Not repeated: verify_refs --live (references/ and tools/ byte-identical since dde0486b); render_curriculum (curriculum/ "
        "identical); the full workspace ruff and mypy runs (twins and LX1 files only, as in the base); the r21 and r23 "
        "re-derivation scripts other than quiz_numbers_r23.py (their subjects are carried as byte-identical).",
        "Scripts run this round are in ledgers/LX1/scripts/LX1-b-r1/ (delta_identity_r1.sh, write_fragment_r1.py) with outputs in out/. "
        "The directory ledgers/LX1/scripts/LX1-b-r1/ already held tracked files from an earlier round; they were not modified.",
    ],
    "summary": (
        f"LX1-b round 1 (closing delta, base dde0486b round-23 fragment, pin 95f3f8cb): verdict PASS. Rows: {len(rows)} "
        f"(pass={len(rows)} fail=0 unverifiable=0). Re-verified this round: {len(fresh)} rows (gates, rows citing the rulings file "
        f"and the project page, plain-curl licence rows). Carried with the prefix: {carried_n} rows (subjects byte-identical since "
        f"dde0486b). Slice-b subjects changed since dde0486b: none. Mutants: none (no new mutants per ruling 37)."
    ),
}

json.dump(frag, open(f"{ROOT}/ledgers/LX1/LX1-b.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(f"{ROOT}/ledgers/LX1/LX1-b.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "fresh", len(fresh), "carried", carried_n)
