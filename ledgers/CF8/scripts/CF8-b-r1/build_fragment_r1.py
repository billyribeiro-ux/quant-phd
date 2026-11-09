"""Build the CF8-b round-1 delta fragment from the round-6 base fragment.

Carries a base PASS row only after git proves its cited files are byte-identical
between the base pin and HEAD; command rows and rows whose subject changed are re-verified.
"""
import datetime
import json
import subprocess
import sys

ROOT = sys.argv[1]
BASE_PATH = sys.argv[2]
BASE_PIN = "9fd6aed"
HEAD = "95f3f8cb"
S = "ledgers/CF8/scripts/CF8-b-r1"

base = json.load(open(BASE_PATH, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

L03 = ["course/modules/CF/CF8/L03.html", "tests/labs/CF8/lab-CF8-L03-1.py"]
L04 = ["course/modules/CF/CF8/L04.html", "tests/labs/CF8/lab-CF8-L04-1.py"]
L05 = ["course/modules/CF/CF8/L05.html", "tests/labs/CF8/lab-CF8-L05-1.py"]
PAGES = ["course/modules/CF/CF8/L03.html", "course/modules/CF/CF8/L04.html", "course/modules/CF/CF8/L05.html"]
TWINS = ["tests/labs/CF8/lab-CF8-L03-1.py", "tests/labs/CF8/lab-CF8-L04-1.py", "tests/labs/CF8/lab-CF8-L05-1.py"]
NOTATION = ["notation/notation.json"]

CARRY = {
    "CF8b-r3-L03-thm1.3": L03,
    "CF8b-r3-L03-thm2.2": L03,
    "CF8b-r3-L03-example-2.3-remark-2.4": L03,
    "CF8b-r3-L03-lab-prose": L03,
    "CF8b-r3-L03-problems-M-P-E-R": L03,
    "CF8b-r3-L03-quiz": L03,
    "CF8b-r3-L03-grades-and-canon": L03,
    "CF8b-r3-L04-thm2.1-cor2.2": L04,
    "CF8b-r3-L04-thm2.3-example-2.4": L04,
    "CF8b-r3-L04-thm2.4-hypothesis": L04,
    "CF8b-r3-L04-key-result-2.4-grade": L04,
    "CF8b-r3-L04-example-2.5-slip": L04,
    "CF8b-r3-L04-lab-prose": L04,
    "CF8b-r3-L04-definitions-and-canon": L04,
    "CF8b-r3-L04-DSO-L01-consistency": L04,
    "CF8b-r3-L04-problems-quiz-misconceptions": L04,
    "CF8b-r3-L05-prop2.1": L05,
    "CF8b-r3-L05-prop2.2": L05,
    "CF8b-r3-L05-remark2.4-95pct": L05,
    "CF8b-r5-L05-lab-prose": L05,
    "CF8b-r3-L05-stderror-M2": L05,
    "CF8b-r3-L05-problems-M-P-E-R": L05,
    "CF8b-r3-L05-canon-seed-spread": L05,
    "CF8b-r3-L05-commercial-paper-definition": L05,
    "CF8b-r3-L05-quiz-key-results": L05,
    "CF8b-r3-notation": L05 + NOTATION,
    "CF8b-r5-notation-q-level-vs-value": L05 + NOTATION,
    "CF8b-r5-notation-L03-L04": L03 + L04 + NOTATION,
    "CF8b-r3-banned-and-process-words": PAGES + TWINS,
}
# Rows re-run at HEAD in this round (command rows, or rows whose evidence the delta gates re-produce).
REVERIFIED = {
    "CF8b-r3-cmd-check-pages", "CF8b-r3-cmd-check-dag", "CF8b-r3-cmd-run-labs", "CF8b-r3-cmd-twins-isolated",
    "CF8b-r3-twin-page-equality", "CF8b-r4-cmd-page-smoke", "CF8b-r3-cmd-ruff", "CF8b-r3-cmd-mypy",
    "CF8b-r3-cmd-pytest", "CF8b-r3-cmd-verify-refs", "CF8b-r3-structure-counts", "CF8b-r3-dag-concepts",
    "CF8b-r6-seed-claim",
}

# Byte-identity of every carried subject, proven by git (exit 0 = no change in the range).
for rid, files in CARRY.items():
    rc = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", BASE_PIN, HEAD, "--", *files]).returncode
    if rc != 0:
        raise SystemExit(f"subject changed, cannot carry {rid}: {files}")

def carry(rid):
    files = CARRY[rid]
    row = dict(base_rows[rid])
    row["evidence"] = (
        f"Carried from round 6 ({', '.join(files)} byte-identical since the previous pin {BASE_PIN}; "
        f"verified by git diff --quiet {BASE_PIN} {HEAD} -- those paths, exit 0): "
        f"basis (round 6): {base_rows[rid]['evidence']}"
    )
    return row

REV = {
    "CF8b-r3-cmd-check-pages": (
        "Re-run at 95f3f8cb: 'check_pages CF8: PASS', exit 0 (ledgers/CF8/scripts/CF8-b-r1/check_pages_CF8.out); "
        "per-page runs --page L03, L04, L05 each exit 0 (check_pages_L03/L04/L05.out)."
    ),
    "CF8b-r3-cmd-check-dag": (
        "Re-run at 95f3f8cb: 27 'check_dag <UNIT>: PASS' lines including 'check_dag CF8: PASS', exit 0 "
        "(ledgers/CF8/scripts/CF8-b-r1/check_dag_all.out). program.json and glossary.json changed at HEAD; the DAG still passes."
    ),
    "CF8b-r3-cmd-run-labs": (
        "Re-run at 95f3f8cb: 'run_labs CF8: PASS (8/8)', exit 0 (ledgers/CF8/scripts/CF8-b-r1/run_labs_CF8.out)."
    ),
    "CF8b-r3-cmd-twins-isolated": (
        "Run as python -I -W error with env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0 in /tmp/cf8b-r1-twins: exit 0 each, "
        "stderr 0 bytes; stdout md5 L03 b434a24db289d8da5f02c1bb3b9589e7, L04 de995caa489fb3d5094989e1749f908f, "
        "L05 b6270131b58581ca974aade0aae644d5, identical to round 6 (twin-L0{3,4,5}.out/.err in /tmp/cf8b-r1-twins)."
    ),
    "CF8b-r3-twin-page-equality": (
        "ledgers/CF8/scripts/CF8-b-r1/twin_vs_page_r1.out: for L03, L04, L05 the single data-run block equals the twin "
        "after HTML unescape (True x3) and the single expected block equals the fresh -I -W error stdout (True x3)."
    ),
    "CF8b-r4-cmd-page-smoke": (
        "Re-run alone at 95f3f8cb: 'page_smoke CF8: PASS', exit 0 (ledgers/CF8/scripts/CF8-b-r1/page_smoke_CF8_b.out)."
    ),
    "CF8b-r3-cmd-ruff": (
        "Re-run at 95f3f8cb: 'All checks passed!' (ruff_check.out) and '555 files already formatted' (ruff_format.out), "
        "both exit 0; the three twins pass ruff check and ruff format --check, '3 files already formatted' (ruff_twins.out). "
        "pyproject.toml changed at HEAD (extend-exclude only); the gate still passes."
    ),
    "CF8b-r3-cmd-mypy": (
        "Re-run at 95f3f8cb: 'Success: no issues found in 386 source files', exit 0 (ledgers/CF8/scripts/CF8-b-r1/mypy.out). "
        "The file count is 386 (round 6 counted 229) because the tree grew; no issue."
    ),
    "CF8b-r3-cmd-pytest": (
        "Re-run at 95f3f8cb: tests/test_labs.py -k CF8 gives 8 passed, exit 0 (pytest_labs_CF8.out); "
        "tests/test_docs_figures.py gives 14 passed, exit 0 (pytest_docs.out)."
    ),
    "CF8b-r3-cmd-verify-refs": (
        "Re-run at 95f3f8cb: 'offline integrity: 560 entries, 0 problems', exit 0 (ledgers/CF8/scripts/CF8-b-r1/verify_refs_offline.out). "
        "references.json changed at HEAD (generated_at, used_by for BK4, FC2, LX1); the slice pages cite no key: "
        "L03 line 506-507, L04 571-572, L05 426-427 (empty data-references lists). Live run not run."
    ),
    "CF8b-r3-structure-counts": (
        "check_pages CF8: PASS at 95f3f8cb (check_pages_CF8.out). git diff --quiet 9fd6aed 95f3f8cb over L03/L04/L05 pages "
        "and twins is empty (exit 0), so there are no changed hunks in the slice this round."
    ),
    "CF8b-r3-dag-concepts": (
        "check_dag CF8: PASS at 95f3f8cb (check_dag_all.out). The slice pages are byte-identical to 9fd6aed, so no "
        "data-concept or link was added or removed."
    ),
    "CF8b-r6-seed-claim": (
        "Re-run this round: the L05 twin with SEED 2026 replaced by 0..9 (run as -I -W error, ledgers/CF8/scripts/CF8-b-r1/seed_sensitivity_r1.out). "
        "Min quantile (-364132, -373438, -374237, -352204, -373040, -362324, -356845, -359919, -361556, -371994) and "
        "shortfall_years at buffer 0 (1703, 1673, 1686, 1674, 1686, 1683, 1646, 1695, 1664, 1695) differ from seed 2026 "
        "(quantile -365525, shortfall_years 1676) in all ten seeds; the sentence at L05 line 218 holds."
    ),
}

rows = []
for rid in base_rows:
    if rid in REVERIFIED:
        rows.append({"id": rid, "check": base_rows[rid]["check"], "location": base_rows[rid]["location"],
                     "status": "PASS", "evidence": REV[rid]})
    elif rid in CARRY:
        rows.append(carry(rid))
    else:
        raise SystemExit(f"row {rid} has no decision")

# Re-derived arithmetic (script arith_r1.py) is cited as added support on carried math rows.
ARITH = f"{S}/arith_r1.out"
for r in rows:
    if r["id"] in {"CF8b-r3-L03-example-2.3-remark-2.4", "CF8b-r3-L04-thm2.1-cor2.2", "CF8b-r3-L04-example-2.5-slip",
                   "CF8b-r3-L04-thm2.3-example-2.4", "CF8b-r3-L05-remark2.4-95pct", "CF8b-r3-L05-stderror-M2",
                   "CF8b-r3-L05-problems-M-P-E-R", "CF8b-r3-L05-quiz-key-results"}:
        r["evidence"] += f" Re-derived this round by script ({ARITH}): P6 460095, U_11 -888640, half_up 881834, k=100, 99/2000 = 0.0495, p(1-p)=0.146316, SE 0.0085532, E1 1320, E2 3655.25, R3 N 36579."

assert len(rows) == len(base_rows) == 42, len(rows)
assert all(r["status"] == "PASS" for r in rows)

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
fragment = {
    "unit": "CF8",
    "slice": "CF8-b",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for CF8-b, round 1 (delta verification of ruling 30; did not build CF8)",
    "pin": HEAD,
    "base": f"{BASE_PIN} (round-6 pin; base fragment ~/.fanout/frags/C-CF8-b.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-CF8-b",
    "scratch": "/tmp/cf8b-r1-twins",
    "verified_at": now,
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        f"Slice delta {BASE_PIN}..{HEAD} over the slice paths is empty: course/modules/CF/CF8/L03.html, L04.html, L05.html, "
        "tests/labs/CF8/lab-CF8-L03-1.py, lab-CF8-L04-1.py, lab-CF8-L05-1.py and notation/notation.json are byte-identical (git diff --quiet exit 0). "
        "The round-6 hunks (L04 lines 48-52 and 458-464; L05 hunks) are already in the base pin, so no subject of this slice changed this round.",
        "Slice scope per plans/FINAL-ARCHITECT-RULINGS and slices.json (CF8 b = L03-L05 and their lab twins). cards.json (CF8 slice c) "
        "changed in the delta and touches the L04 and L05 cards; cards are not judged here and belong to CF8-c. index.html and L01/L02 changed and are not in slice b.",
        "references.json changed (generated_at, used_by for BK4, FC2, LX1); no slice-b page cites a registry key, so verify_refs is a registry integrity check only for this slice.",
        "program.json and glossary.json changed (build_site output). build_site --check: 'site data current: 6 outputs' (ledgers/CF8/scripts/CF8-b-r1/build_site_check.out); check_dag PASS.",
        "Standing mutant set for this slice: none (lessons only; no project grader in CF8-b). No new mutants authored (ruling 37).",
        "Not checked: the Pyodide runtime (run_labs and page_smoke use local CPython 3.14); live verify_refs (no key cited); L03 body lines 260-519 "
        "were not re-read this round (carried by byte identity, read in rounds 4 and 5); run_graders and mutate_graders (project only, out of slice).",
    ],
    "summary": {"rows": len(rows), "pass": len(rows), "fail": 0, "unverifiable": 0, "fail_ids": []},
}
out = f"{ROOT}/ledgers/CF8/CF8-b.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, "rows", len(rows))
