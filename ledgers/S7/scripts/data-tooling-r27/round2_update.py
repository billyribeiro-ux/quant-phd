"""Round-27 (round 2 of the data-tooling campaign) updates to the round-26 fragment.

Applies only decisions made and evidenced in round 27 (see the report); every row id is kept.
Run from the checkout: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r27/round2_update.py <page_smoke_all.log> <verify_refs_whole.log>
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

OUT = ROOT / "ledgers/S7/data-tooling.json"
PAGE_SMOKE_LOG, VERIFY_LOG = Path(sys.argv[1]), Path(sys.argv[2])
frag = json.loads(OUT.read_text(encoding="utf-8"))
rows = {r["id"]: r for r in frag["rows"]}


def setrow(rid: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = rows[rid]
    r["status"] = status
    r["evidence"] = evidence
    if status == "PASS":
        r.pop("fix", None)
    else:
        r["fix"] = fix or "Correct or re-derive this row (see evidence) and re-run it."


ps_lines = PAGE_SMOKE_LOG.read_text(encoding="utf-8").splitlines()
ps_final = [line for line in ps_lines if line.startswith("page_smoke ") and (": PASS" in line or ": FAIL" in line)]
ps_pages = [line for line in ps_final if not line.startswith("page_smoke all") and not line.startswith("page_smoke S7")
            and not line.startswith("page_smoke AP1")]
ps_pass = sum(1 for line in ps_pages if line.endswith("PASS"))
ps_fail = [line for line in ps_pages if not line.endswith("PASS")]
ps_scope = [line for line in ps_final if line.startswith(("page_smoke all", "page_smoke AP1", "page_smoke S7"))]
vr_line = [line for line in VERIFY_LOG.read_text(encoding="utf-8").splitlines() if "live re-verification" in line]
pinned = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
print("page_smoke --all pages PASS", ps_pass, "non-PASS", ps_fail, "summary", ps_scope)
print("verify_refs whole:", vr_line)

setrow("R26-ci-not-run-here", "PASS" if ps_pass and not ps_fail else "FAIL",
       f"Run this round at {pinned}. `tools/page_smoke.py --all` (logs27/page_smoke_all.log): {ps_pass} unit pages PASS, "
       f"{len(ps_fail)} not PASS; summary lines: {ps_scope}. `tools/verify_refs.py` with no unit (whole registry, live; "
       f"logs27/verify_refs_whole_live.log): '{vr_line[0] if vr_line else 'NO LINE'}'.")

setrow("r25-cmd-fetch_data-raw-dir", "PASS",
       "Run this round: a scratch --fetch with --keep-raw saved the three zips (raw27/*.raw); `fetch_data.py --fetch --raw-dir` "
       "rebuilt the snapshots from them: 'fetch_data: 3 datasets, 0 problems' (logs27/fetch_raw_dir.log); the CSVs are byte-identical "
       "to the committed files (cmp). MANIFEST differs only in retrieved and raw_sha256, as recorded in R26-data-rebuild-live.")

setrow("r25-cmd-page_smoke-dark-sweep", "PASS",
       "Dark-theme figure controls are swept by the lesson slices' Chromium drives, which covered light and dark at 1280 and 360 px: "
       "L03-L04 rows R25-cmd-chromium-drive (five live figures of L03 and L04 at 360 and 1280 px), R25-fig-L03-bh-geometry and "
       "R25-fig-L03-pvalue-histogram (every control across its range, both themes), and L01-L02 row L01-L02-cmd-fig-drive-a2a631a. "
       "Those rows' subjects (the L01-L04 pages and their figure files) are byte-identical between their pins and df02012 "
       "(git diff --quiet). This does not extend the drives to L05-L08 figures in dark theme; those are not swept dark by this round.")

setrow("r25-diff-scope", "PASS",
       "Re-done for this campaign (git diff --stat 5e5da87 df02012, grouped by top-level directory): 324 files changed, 89586 "
       "insertions and 10221 deletions. ledgers/AP1 and ledgers/S7 (accepted fragments, scripts, history) are the bulk; then tests/labs "
       "(AP1 labs, 22 files), course/modules (AP pages; S7 L01 and project), course/assets (data, js, css, vendor), and the slice's "
       "tools/ (build_site.py, data_sources.yaml, katex_strict.js, page_smoke.py, vendor_spec.yaml), tests/ (page_smoke, run_labs, "
       "koning_spot, fetch_vendor, figure_kernels, memo_exemplars), .github/workflows/ci.yml, pyproject.toml and requirements*.txt. "
       "Each slice file is named in a row (R26-diff-coverage) or here.")

setrow("R26-vendor-two-systems", "PASS",
       "Fixed by ea9d823 and re-judged this round. Diff: tools/vendor.py (242 lines), course/assets/vendor/SPEC.yaml and "
       "tests/test_vendor.py deleted; tests/test_fetch_vendor.py added (11 tests). `tools/fetch_vendor.py --check`: 'vendor: 56 files, "
       "0 problems'. `pytest tests/test_fetch_vendor.py`: 11 passed. Retired-name grep (README, CLAUDE.md, BLUEPRINT, tools, tests, "
       "CI): the only stale hit is course/assets/css/tokens.css:6 ('see assets/vendor/SPEC.yaml'), row R27-stale-spec-pointer. "
       "Mutants of tools/fetch_vendor.py, scratch copy: M1 verify compares size only -> 2 failed; M2 fetch writes a mismatching download "
       "-> 1 failed; M3 --check always exits 0 -> 1 failed; all killed. Retired-test coverage: test_vendor.py had six tests and was added "
       "after 5e5da87, so no release row cited it. sha512 tarball integrity: no equivalent (fetch_vendor verifies per-file sha256 from "
       "LOCK; residual: relock trusts the CDN at lock time, cross-checked only for Pyodide wheels). Extraction mapping and globs: no "
       "equivalent (LOCK lists explicit files). Unsafe-destination refusal: equivalent in test_the_committed_lock_is_well_formed "
       "('..' and absolute paths). Missing member fails closed: equivalent in test_verify_reports_a_missing_file and the fetch tests. "
       "Glob needs a directory and semver ordering: not applicable.")

rows["R27-stale-spec-pointer"] = {
    "id": "R27-stale-spec-pointer",
    "check": "2.9-structure: no document points at a retired file",
    "location": "course/assets/css/tokens.css line 6 ('Fonts (vendored; see assets/vendor/SPEC.yaml)'); course/assets/vendor/SPEC.yaml deleted in ea9d823",
    "status": "FAIL",
    "evidence": "grep -rn 'SPEC.yaml' (excluding ledgers): the comment at tokens.css:6 names course/assets/vendor/SPEC.yaml, which ea9d823 "
                "deleted. The pin file is tools/vendor_spec.yaml.",
    "fix": "Edit the comment in course/assets/css/tokens.css line 6 to name tools/vendor_spec.yaml (comment only; then re-run check_pages and page_smoke S7).",
}
frag["rows"].append(rows["R27-stale-spec-pointer"])

setrow("data-notes", "FAIL",
       "Re-derived this round (ledgers/S7/scripts/data-tooling-r27/data_notes_check.py on the raw H.10 zip saved from the live fetch): the note's "
       "parenthetical 'the release's own monthly series are monthly averages' holds: RXI$US_N.M.EU equals the mean of the daily "
       "RXI$US_N.B.EU values of the month to 4 decimal places in 333 of 333 months from 1999-01 (0 disagreements). fx_daily (6706 rows, 0 "
       "weekend dates, 0 blank cells) and fx_monthly (669 months; EUR blank in 336 months before 1999-01; first EUR 1999-01; the other nine "
       "currencies non-blank in 336 months) also hold. The round-24 evidence says 'the two exact half-way cases, 1999-04 and 2014-11'. "
       "That count is wrong: seven months have an exact half-way mean at the fifth decimal (1999-04, 1999-10, 2002-10, 2006-01, 2012-03, "
       "2014-11, 2024-10). All seven match the published 4-decimal value under half-up rounding; under half-even, 1999-04, 2014-11 and "
       "2024-10 would differ. The data-source note in tools/data_sources.yaml states no count, so the snapshots and the note are not wrong; "
       "the ledger's evidence is.",
    fix="Correct the ledger count to seven exact ties (half-up); no snapshot or note change is needed.")

setrow("r25-cmd-mutant-run", "PASS",
       "Carried under the mutant rule (R26-mutants-152-rerun): the 66 add_reference.py mutants have target tools/add_reference.py and "
       "killer file tests/test_refs.py byte-identical since 5e5da87 (git diff --quiet). Their killing test ids were run at df02012 "
       "(83 distinct killers, '83 passed', logs27/killer_ids_df02012.txt). Carried result: killed. Not re-created this round.")

setrow("mut-plain_title-survivors", "PASS",
       "tools/build_site.py changed (one renamed unused variable, line 382). The plain_title mutants P01-P11 were re-created in a scratch copy "
       "of df02012 (ledgers/S7/scripts/data-tooling-r27/run_build_site_mutants.py; logs27/build_site_mutants.log; bytecode caches cleared "
       "before each run): all ten listed P01, P02, P03, P05, P06, P07, P08, P09, P10, P11 KILLED by their named killers. A first run without "
       "cache clearing showed spurious survivors from stale .pyc files; those were discarded and disclosed.")
setrow("r16-mut-plain-title-killed", "PASS",
       "The same re-creation as mut-plain_title-survivors: P01-P11 all KILLED at df02012 (logs27/build_site_mutants.log).")
setrow("mutant-P-V-family-r18", "PASS",
       "P-family: P01-P11 re-created and killed at df02012 (logs27/build_site_mutants.log). V-family: tools/verify_refs.py and "
       "tests/test_refs.py byte-identical since 5e5da87; their killers passed at df02012 (83 distinct killers), carried under the mutant rule.")

setrow("R26-killer-ids", "PASS",
       "Re-run at df02012: all 83 distinct killing node ids collect and pass ('83 passed in 2.48s', logs27/killer_ids_df02012.txt).")

setrow("R26-mutants-152-rerun", "PASS",
       "Breakdown by target tool (round-27 parse of the 152 mutant entries): 10 build_site.py mutants (P01-P11 family; build_site.py changed "
       "since 5e5da87) re-created in scratch and KILLED at df02012. 142 others carried under the mutant rule: targets tools/add_reference.py (66), "
       "tools/verify_refs.py (10), tools/refs/match.py (1), tools/fetch_data.py via tests/test_fetch_data.py (31), tools/check_pages.py via "
       "tests/test_page_checks.py (13), and tests/labs/S7 twins via tests/test_labs.py (7). Each target and killer file is byte-identical to "
       "5e5da87 (git diff --quiet), and the 83 distinct killers pass at df02012. Survivors among the 10 re-created: none. The 142 carried "
       "results are not re-observed this round.")

frag["notes"] = frag["notes"] + (
    " ROUND 27 (round 2, pin df02012): vendor fixed (ea9d823) and re-judged; whole-registry live verify_refs run; page_smoke --all run; "
    "fetch_data --raw-dir tested; dark-theme figure sweep covered for L01-L04 by the lesson slices' Chromium drives (named rows); ten "
    "build_site mutants re-created and killed; 142 mutants carried under the mutant rule; data-notes corrected to FAIL (seven exact "
    "half-way months, not two). Verbatim reading of evidence strings was done this round for rows 0-159; rows 160-411 were NOT read "
    "verbatim in round 27 and keep their round-26 decisions. Numeric rows with candidate lesson-ledger rows (cands.json, from "
    "ledgers/S7/scripts/data-tooling-r27/cite_match.py) are not cited: claim equivalence was not reviewed row by row.")
frag["verified_at"] = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
frag["pin"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
counts = {s: sum(1 for r in frag["rows"] if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["verdict"] = "PASS" if counts["PASS"] == len(frag["rows"]) else "FAIL"
frag["summary"] = {"rows": len(frag["rows"]), "pass": counts["PASS"], "fail": counts["FAIL"],
                   "unverifiable": counts["UNVERIFIABLE"], "mutants": len(frag["mutants"]),
                   "fail_ids": [r["id"] for r in frag["rows"] if r["status"] != "PASS"]}
OUT.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("validate:", ledger.validate(frag, "S7/data-tooling"))
print("summary:", frag["summary"])
