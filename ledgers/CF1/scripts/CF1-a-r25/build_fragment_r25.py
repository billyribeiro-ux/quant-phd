"""Build ledgers/CF1/CF1-a.json for round 25 from the round-24 fragment, carrying byte-identical subjects."""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
prev = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-a.round24.json").read_text())
PREFIX = ("Carried from round 24 (course/modules/CF/CF1/index.html, L01.html, L02.html, both lab twins, notation/, "
          "references/, tools/ byte-identical since the previous pin 23cbd6a; cards.json changed only at entry "
          "CF1-c110, so rows citing other card entries cite unchanged entries): ")
STRIP = re.compile(r"^(Carried from round \d+ \([^)]*\): )+")
NEW = {
    "CF1-a-r23-c110": ("course/modules/CF/CF1/cards.json CF1-c110; course/modules/CF/CF1/L01.html lines 446, 466", "PASS",
        "Re-verified round 25: CF1-c110 now grades T with basis 'Problem R3, values on L01 line 446 (Assumption 4.0 and "
        "Remark 4.3)'. L01.html line 466 grades the same claim T (data-grade=\"T\"). Line 446 is the R3 solution and "
        "carries the values: -1 + 1.05/1.06 = -0.009434 and -1 + 1.05/1.03 = +0.019417, recomputed in Python (out/"
        "card_and_twin_check_r25.out). The card's claims (Assumption 4.0 needs one rate; the decision can change with "
        "the rate; Remark 4.3 and R3 cited) match L01 lines 148 and 442-446. The round-24 FAIL is fixed."),
    "CF1-a-cards-L01-L02": ("course/modules/CF/CF1/cards.json (110 entries, 60 T and 50 C, no duplicate ids)", "PASS",
        "Re-verified round 25: git diff -U0 23cbd6a b49a857 -- cards.json changes exactly two lines, the grade and basis of "
        "CF1-c110 (see CF1-a-r24-delta). Every other entry is byte-identical to 23cbd6a, so the round-24 checks of those entries "
        "stand. CF1-c110 is checked against L01.html lines 147-148 and 442-446 in CF1-a-r23-c110."),
    "CF1-a-r23-cards-changed-subjects": ("course/modules/CF/CF1/cards.json CF1-c001, CF1-c014, CF1-c018, CF1-c021, CF1-c024; L01.html lines 55, 330-341; L02.html lines 56, 90, 122", "PASS",
        "Re-verified round 25: the only card entry changed in this range is CF1-c110 (see CF1-a-r23-c110). The entries cited here "
        "(c001, c014, c018, c021, c024) are byte-identical to 23cbd6a, so their round-24 checks stand: c021 equals L02.html line 90, "
        "c024 equals line 122, c018 equals line 56, c001 equals L01 Definition 1.1 and line 55, c014 refers to L01.html line 341."),
    "CF1-a-r24-delta": ("git diff --stat 23cbd6a b49a857 -- course/modules/CF/CF1 tests/labs/CF1 notation references tools", "PASS",
        "Round-25 delta: 1 file changed, 2 insertions and 2 deletions (course/modules/CF/CF1/cards.json, entry CF1-c110 grade "
        "and basis). index.html, L01.html, L02.html, both twins, notation/, references/ and tools/ are byte-identical to 23cbd6a. "
        "The other changed paths in the commit range (AC4, M1, AC1 ledgers) are outside this slice."),
    "CF1-a-gate-check-pages": ("tools/check_pages.py --unit CF1", "PASS", "check_pages.py --unit CF1 exit 0, 'check_pages CF1: PASS' (scripts/CF1-a-r25/out/check_pages.out), re-run round 25."),
    "CF1-a-gate-check-dag": ("tools/check_dag.py --all", "PASS", "check_dag.py --all exit 0: 'check_dag CF1: PASS', 'check_dag AP1: PASS', 'check_dag AC2: PASS', 'check_dag AC4: PASS' (scripts/CF1-a-r25/out/check_dag.out), re-run round 25."),
    "CF1-a-gate-run-labs": ("tools/run_labs.py --unit CF1", "PASS", "run_labs.py --unit CF1 exit 0, 'run_labs CF1: PASS (9/9)' (scripts/CF1-a-r25/out/run_labs.out), re-run round 25."),
    "CF1-a-gate-page-smoke": ("tools/page_smoke.py --unit CF1 --pages L01 L02 index", "PASS", "page_smoke.py --unit CF1 --pages L01 L02 index exit 0, 'page_smoke modules/CF/CF1/L02.html: PASS', 'page_smoke CF1: PASS' (scripts/CF1-a-r25/out/page_smoke.out), re-run round 25. The shell wrapper 'timeout' is absent on this Mac, so the first attempt exited 127 and was re-run without it."),
    "CF1-a-gate-lint-types": ("ruff check .; ruff format --check .; mypy --no-incremental", "PASS", "ruff check . 'All checks passed!' (out/ruff.out, exit 0); ruff format --check . exit 0; mypy --no-incremental 'Success: no issues found in 153 source files' (out/mypy.out, exit 0), re-run round 25."),
    "CF1-a-gate-pytest": ("pytest -q -k CF1 tests", "PASS", "pytest -q -k CF1 tests: exit 0, nine dots (scripts/CF1-a-r25/out/pytest_CF1.out), re-run round 25."),
    "CF1-a-cite-verify-refs": ("tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", "PASS", "verify_refs.py --offline exit 0: 'offline integrity: 560 entries, 0 problems'; verify_refs.py --unit CF1 exit 0: 'live re-verification of CF1: 2 of 560 entries, 0 problems' (out/refs_off.out, out/refs_live.out), re-run round 25."),
    "CF1-a-r23-lab-twins": ("tests/labs/CF1/lab-CF1-L01-1.py; tests/labs/CF1/lab-CF1-L02-1.py; L01.html line 308 and L02.html embedded blocks", "PASS", "Re-run round 25: python -I -W error exit 0 for both twins; stdout equals the embedded <pre class=\"expected\"> of L01.html and L02.html ('match [True]' for each, scripts/CF1-a-r25/out/card_and_twin_check_r25.out)."),
    "CF1-a-r23-numbers": ("scripts/CF1-a-r25/card_and_twin_check_r25.py (python -I -W error)", "PASS", "Re-run round 25: R3 values -0.009433962 and 0.019417476 (out/card_and_twin_check_r25.out) match the page's -0.009434 (six places) and +0.0194 / +0.019417 (scripts/CF1-a-r25/out/card_and_twin_check_r25.out)."),
    "CF1-a-mutants": ("ledgers/CF1/scripts/CF1-a-r18/run_mut18.py (run against this checkout)", "PASS", "Re-run round 25: python -I -W error run_mut18.py /tmp/verify25-CF1-a gives 'killed 67 survived 3 total 70' (scripts/CF1-a-r25/out/mutants_rerun.out). Survivors: CF1-a-r9/r9_m07_no_tax_credit.py, CF1-a-r11/n05_l02_identity_check_stubbed_true.py, CF1-a-r17/r17_probe_l02_identity_exact_equality.py; all lab mutants, dispositioned in CF1-a-r23-survivors."),
    "CF1-a-r23-survivors": ("ledgers/CF1/mutants/CF1-a-r9/r9_m07_no_tax_credit.py; CF1-a-r11/n05_l02_identity_check_stubbed_true.py; CF1-a-r17/r17_probe_l02_identity_exact_equality.py", "PASS",
        "Re-run round 25: the same three lab-mutant survivors as round 24 (out/mutants_rerun.out). Architect ruling: lab twins are demonstrations, so a surviving lab mutant is not a finding unless a lesson sentence claims the lab checks that property. L02.html line 272 claims 'the two checks confirm Proposition 2.2 and the shield formula numerically'. n05 stubs the identity check to True, which is not a student error; the live check is tested by three new student-error mutants that all print False and exit 0 (CF1-a-r25-new-mutants). r9_m07 (no tax credit) and r17_probe (exact float equality) print identical output for this data and are not claimed by any sentence. Recorded PASS, out of scope."),
    "CF1-a-r24-gate-ruff-mypy-pytest": ("ruff check .; ruff format --check .; mypy --no-incremental; pytest -q -k CF1 tests", "PASS", "Re-run round 25: ruff check 'All checks passed!', ruff format --check exit 0, mypy 'Success: no issues found in 153 source files', pytest CF1 nine dots exit 0 (scripts/CF1-a-r25/out/)."),
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid == "CF1-a-r24-delta":
        pass
    if rid in NEW:
        loc, status, ev = NEW[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev})
        continue
    if rid == "CF1-a-r23-c110":
        pass
    ev = STRIP.sub("", r["evidence"])
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"], "evidence": PREFIX + ev})
rows.append({"id": "CF1-a-r25-new-mutants", "check": "three new student-error mutants of L02 (slice is a lesson slice; written to test the shield and identity checks that L02.html line 272 claims to confirm)",
    "location": "ledgers/CF1/mutants/CF1-a-r25/r25_m01_l02_identity_drops_shield.py; r25_m02_l02_shield_check_uses_full_depreciation.py; r25_m03_l02_identity_uses_ebit_not_ebitda.py; tests/labs/CF1/lab-CF1-L02-1.py lines 61, 65", "status": "PASS",
    "evidence": "Each mutant exits 0 under python -I -W error, but its printed check line flips from True to False: m01 identity line 11 False (shield dropped), m02 shield line 12 False (full depreciation subtracted), m03 identity line 11 False (EBIT instead of EBITDA). Outputs in scripts/CF1-a-r25/out/mut_r25_*.out. The baseline printed True on both lines, so each mutant is killed by output difference (scripts/CF1-a-r25/out/twin_lab-CF1-L02-1.out)."})
prev_summary = prev["summary"]
frag = {
    "unit": "CF1", "slice": "CF1-a", "round": 25,
    "verifier": "independent Haiku verifier, round 25, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1",
    "pin": "b49a857", "base": "23cbd6a",
    "previous_fragment": "/tmp/fanout-frags/CF1-a.round24.json (pin 23cbd6a)",
    "checkout": str(root), "scratch": "/tmp/cf1-v/a25",
    "verified_at": "2026-10-28T12:00:00+00:00", "verdict": "PASS",
    "rows": rows,
    "mutants": [
        {"name": m, "description": d, "result": "KILLED"} for m, d in [
            ("r25_m01_l02_identity_drops_shield.py", "L02 identity check drops the depreciation shield term; prints False"),
            ("r25_m02_l02_shield_check_uses_full_depreciation.py", "L02 shield check subtracts full depreciation instead of depreciation times tax rate; prints False"),
            ("r25_m03_l02_identity_uses_ebit_not_ebitda.py", "L02 identity check applies tax to EBIT instead of EBITDA; prints False")]],
    "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta 23cbd6a..b49a857 for this slice: only course/modules/CF/CF1/cards.json, CF1-c110 grade C to T and basis rewritten. index.html, L01.html, L02.html, both twins, notation/, references/, tools/ byte-identical.",
        "Carried rows state the files byte-identical since 23cbd6a; cards-citing rows cite entries that the diff does not touch.",
        "Re-run this round: check_pages, check_dag, run_labs 9/9, page_smoke (L01, L02, index), verify_refs offline and live (CF1), ruff check, ruff format, mypy, pytest -k CF1, check_projects --all, both twins under -I -W error against embedded output, 70 lab mutants (67 killed, 3 dispositioned).",
        "Not run: alternative correct implementations and a new full alt-implementation pass; the lab twins are byte-identical to 23cbd6a, so CF1-a-r17/r18 alternatives are carried. This slice has no project grader, so the three new mutants are L02 twin mutants, not a project-slice requirement.",
        "Not checked: external sources (no citation changed; live verify_refs covered the 2 CF1 entries). No browser screenshot; page_smoke is the Pyodide check run here."],
    "summary": ("Slice CF1-a round 25 (pin b49a857, delta from 23cbd6a): PASS. The round-24 FAIL on CF1-c110 is fixed: the card now grades T with basis 'Problem R3, values on L01 line 446', matching L01.html line 466 (T). R3 values recomputed (-0.009434, +0.019417). All gates re-run and green; both twins match embedded output; 70 lab mutants re-run (67 killed, 3 dispositioned as out of scope); 3 new L02 student-error mutants killed. Carried rows cite unchanged subjects."),
}
out = root / "ledgers/CF1/CF1-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print("rows", len(rows), "ids unique", len({r["id"] for r in rows}) == len(rows), "prev ids kept", {r["id"] for r in prev["rows"]} <= {r["id"] for r in rows})
