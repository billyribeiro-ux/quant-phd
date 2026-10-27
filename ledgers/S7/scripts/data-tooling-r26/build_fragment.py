"""Build ledgers/S7/data-tooling.json (round 26) from the round-25 fragment and the round-26 evidence.

Run from the checkout with the checkout's venv: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r26/build_fragment.py
Every PASS row either (a) is a command re-run this round (log named in its evidence), (b) is re-derived here (script
named), or (c) is carried because the passage or file it cites is byte-identical to 5e5da87 (git diff checked below).
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

BASE = "5e5da87"
PREV = json.loads(Path("/tmp/ap1-r5/data-tooling/round25-data-tooling.json").read_text(encoding="utf-8"))  # git show HEAD: round 25
RELEASE_PREV = json.loads(Path("/tmp/ap1-r5/data-tooling/release-data-tooling.json").read_text(encoding="utf-8"))
OUT = ROOT / "ledgers/S7/data-tooling.json"
LOGS = "/tmp/ap1-r5/data-tooling/logs"
S7 = "course/modules/S/S7"


def git_identical(paths: list[str]) -> bool:
    return subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", *paths], cwd=ROOT).returncode == 0


REGISTRY_RERESOLVE = ("Today's re-read (architect rule 4): verify_refs.py --unit S7 re-resolved every S7 entry against its "
                      "source this round (94 of 560, 0 problems; logs/verify_refs_unit_S7_live.log); publisher pages that were "
                      "not re-read today are named as such in the row's earlier evidence.")


def carried(row: dict[str, Any], files: list[str], note: str = "") -> dict[str, Any]:
    if not git_identical(files):
        raise SystemExit(f"{row['id']}: {files} changed since {BASE}; cannot carry")
    if "2.1-citations" in row["check"] or "cite" in row["id"] or "registry" in row["id"]:
        note = f"{note} {REGISTRY_RERESOLVE}".strip()
    prefix = f"Carried from the release ledger ({', '.join(files)} byte-identical since {BASE}):"
    return {"id": row["id"], "check": row["check"], "location": row["location"], "status": "PASS",
            "evidence": f"{prefix} {note} Earlier evidence: {row['evidence']}"}


def carried_passage(row: dict[str, Any], file: str, hunk_lines: str, note: str) -> dict[str, Any]:
    prefix = (f"Carried from the release ledger (passage byte-identical since {BASE}: git diff -U0 {file} "
              f"changes only {hunk_lines}; the passage named here is outside them):")
    return {"id": row["id"], "check": row["check"], "location": row["location"], "status": "PASS",
            "evidence": f"{prefix} {note} Earlier evidence: {row['evidence']}"}


def fresh(row: dict[str, Any], status: str, evidence: str) -> dict[str, Any]:
    return {"id": row["id"], "check": row["check"], "location": row["location"], "status": status,
            "evidence": evidence}


def unverifiable(row: dict[str, Any], reason: str) -> dict[str, Any]:
    out = fresh(row, "UNVERIFIABLE", f"NOT re-derived in round 26: {reason}. Round-25 evidence (not re-run, not carried "
                f"as a pass): {row['evidence'][:400]}")
    out["fix"] = "Re-derive this row in a verifier round (scripts under ledgers/S7/scripts/<slice>-r<round>/) against the current toolchain."
    return out


GATES = "ledgers/S7/scripts/data-tooling-r26/gates.sh"
CMD_EVIDENCE = {
    "r25-cmd-ruff-check": "`.venv/bin/ruff check .` exit 0, 'All checks passed!' (logs/ruff_check.log)",
    "r25-cmd-ruff-format": "`.venv/bin/ruff format --check .` exit 0, '125 files already formatted' (logs/ruff_format.log)",
    "r25-cmd-mypy": "`.venv/bin/mypy --no-incremental` exit 0, 'Success: no issues found in 102 source files' (logs/mypy.log)",
    "r25-cmd-pytest-slice": "11 slice test files (test_fetch_data, test_refs, test_build_site, test_page_checks, test_labs, "
                            "test_run_labs, test_page_smoke, test_vendor, test_koning_spot, test_figure_kernels, test_js): "
                            "'391 passed' (logs/slice_tests.log)",
    "r25-cmd-collect-identical": "five slice files collected twice with `pytest --collect-only -q`: 331 tests, outputs "
                                 "byte-identical (logs/collect1.txt, collect2.txt)",
    "r25-cmd-pytest-full": "`.venv/bin/pytest` (full suite, pyproject addopts): '434 passed in 51.16s', exit 0 (logs/pytest_full.log)",
    "r25-cmd-run_labs": "`.venv/bin/python tools/run_labs.py --all`: 'run_labs S7: PASS (42/42)', 'run_labs AP1: PASS (22/22)', exit 0 (logs/run_labs_all.log)",
    "r25-cmd-check_pages-unit": "`tools/check_pages.py --all`: 'check_pages S7: PASS', 'check_pages AP1: PASS' (logs/check_pages_all.log)",
    "r25-cmd-check_pages-all": "`tools/check_pages.py --all`: S7 and AP1 PASS (logs/check_pages_all.log)",
    "r25-cmd-check_dag": "`tools/check_dag.py --all`: S7 and AP1 PASS (logs/check_dag_all.log)",
    "r25-cmd-check_projects": "`tools/check_projects.py --all`: S7 and AP1 PASS (logs/check_projects_all.log)",
    "r25-cmd-verify_refs-offline": "`tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems' (logs/verify_refs_offline.log)",
    "r25-cmd-build_site-check": "`tools/build_site.py --check`: 'site data current: 6 outputs' (logs/build_site_check.log)",
    "r25-cmd-fetch_data-check": "`tools/fetch_data.py --check`: 'fetch_data: 3 datasets, 0 problems' (logs/fetch_data_check.log)",
    "r25-cmd-fetch_data-fetch": "`tools/fetch_data.py --fetch` in a scratch copy of HEAD (git archive): 3 datasets built; the three "
                                "CSVs are byte-identical to the committed files (cmp; logs/fetch_fetch.log)",
    "r25-cmd-render_curriculum": "`tools/render_curriculum.py` then `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`: both exit 0 (logs/render_curriculum.log, curriculum_diff.log)",
    "r25-cmd-run_graders-S7": "`tools/run_graders.py --unit S7 --seeds 0-49`: 'run_graders S7: PASS (reference 50/50 seeds, slowest 1.6 s)'; "
                              "`--all --seeds 0-49`: S7 and AP1 PASS (logs/run_graders_S7.log, ci_run_graders_all.log)",
    "r25-cmd-page_smoke-S7": "`tools/page_smoke.py --unit S7`: 'page_smoke S7: PASS', exit 0 over all 8 pages + index, concepts, review; "
                             "light and dark, 1280 and 360 px; 34 labs in Pyodide, max 1.3 s against the 10 s limit; the in-browser grader "
                             "passes 162 tests (logs/page_smoke_S7.log)",
    "r25-cmd-git-status": "`git status --short` after the round: only `?? .venv` (the pre-existing symlink) and "
                          "`?? ledgers/S7/scripts/data-tooling-r26/` (this round's archived scripts); no tracked file modified",
    "r25-cmd-verify_refs-unit-S7": "`tools/verify_refs.py --unit S7` (live, unmodified tool, default pacing): "
                                   "'live re-verification of S7: 94 of 560 entries, 0 problems', exit 0 (logs/verify_refs_unit_S7_live.log); "
                                   "the S7 scope is 94 entries at 5e5da87 and at HEAD (scripts/data-tooling-r26/checks.py)",
}
CMD_FAIL: dict[str, str] = {}
CMD_UNVERIFIABLE = {
    "r25-cmd-fetch_data-raw-dir": "not run this round (a `--raw-dir` rebuild needs the raw zips kept by a second download)",
    "r25-cmd-page_smoke-dark-sweep": "tools/page_smoke.py sweeps the figure controls in the light theme only (its docstring: "
                                     "'the dark theme is not swept'); a dark-theme sweep was not run this round",
    "r25-cmd-mutant-run": "the 66 add_reference.py mutants were run from a scratch copy in round 24 and the patch script is not "
                          "archived under ledgers/S7/scripts; not re-run",
}

NUMERIC = re.compile(r"1\.2-|2\.2-|2\.4-|2\.8-figures|numbers|mathematics|figure|derivation|sweep")
NUMERIC_EVIDENCE = re.compile(r"recomput|simulat|seed|Monte|integrat|numpy|scipy|NormalDist|quantile|\bPhi\b|sqrt|bootstrap|computed")
CHANGED = set(subprocess.run(["git", "diff", "--name-only", BASE, "HEAD"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.split())
SUBJECT_FILES = {  # the files a round-25 row names, resolved to repository paths (S7 pages are under S7)
    "L01.html": f"{S7}/L01.html", "L02.html": f"{S7}/L02.html", "L03.html": f"{S7}/L03.html",
    "L04.html": f"{S7}/L04.html", "L05.html": f"{S7}/L05.html", "L06.html": f"{S7}/L06.html",
    "L07.html": f"{S7}/L07.html", "L08.html": f"{S7}/L08.html", "project.html": f"{S7}/project.html",
    "cards.json": f"{S7}/cards.json", "cards.js": f"{S7}/cards.json",
}
PATH = re.compile(r"(?<![\w/])((?:[\w\-.]+/)*[\w\-.]+\.(?:py|html|js|mjs|json|yaml|md|csv|txt|toml|css|yml|tex))(?![\w/])")


def subjects(row: dict[str, Any]) -> list[str]:
    found: set[str] = set()
    for tok in PATH.findall(row["location"] + " " + row["check"]):
        if tok in SUBJECT_FILES:
            found.add(SUBJECT_FILES[tok])
        elif "/" in tok and (ROOT / tok).exists():
            found.add(tok)
        elif "/" not in tok:
            for cand in (f"{S7}/{tok}", f"tests/labs/S7/{tok}", f"tools/{tok}", f"tests/{tok}"):
                if (ROOT / cand).exists():
                    found.add(cand)
                    break
    text = row["location"] + " " + row["check"]
    if re.search(r"\bcards?\b", text) and f"{S7}/cards.json" not in found:
        found.add(f"{S7}/cards.json")
    if re.search(r"registry|references\.json|\bkeys?\b", text) and "references/references.json" not in found:
        found.add("references/references.json")
    return sorted(found)


# Rows decided one by one in round 26 (evidence written from the logs and scripts named in each).
MANUAL: dict[str, tuple[str, str]] = {
    "r22-registry-koning2026anytime": ("PASS", "Re-run this round: `verify_refs.py --unit S7` live (koning2026anytime is "
        "an S7 entry: 94 of 560 live, 0 problems) and `--offline` (560 entries, 0 problems); the entry is unchanged between "
        "5e5da87 and HEAD (scripts/data-tooling-r26/checks.py: the only entries whose fields changed are hansen1991implications, "
        "kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone, and only in used_by)."),
    "data-h15-note": ("PASS", "Passage outside the data_sources.yaml hunks (@@ +31,7 and +65,7; the ust_daily note is at lines "
        "~87-93). Re-read today: https://www.federalreserve.gov/disclaimer.htm HTTP 200, 85130 bytes, 'Unless otherwise "
        "indicated, information on Board's website is in the public domain and may be copied and distributed without "
        "permission'; https://www.federalreserve.gov/releases/h15/default.htm HTTP 200, 105950 bytes, footnote 9 'Source: "
        "U.S. Treasury' against the constant-maturity series. 17 U.S.C. 105(a) was not re-read this round."),
    "data-rejected-french-nogrant": ("PASS", "Passage outside the changed hunks (rejected section, lines ~100-130; "
        "data_sources.yaml hunks are at new lines 31-37 and 65-71). Not re-read this round: this row is an external-source "
        "row carried on the byte-identity of its text (VERIFIER_RULES 2.8 / architect rule 4)."),
    "data-rejected-french-finding": ("PASS", "Passage outside the changed hunks; the French library text is not re-read this "
        "round (carried on byte-identity of the finding text, architect rule 4)."),
    "data-rejected-osap": ("PASS", "Passage outside the changed hunks; the Open Source Asset Pricing text is not re-read this "
        "round (carried on byte-identity of the finding text, architect rule 4)."),
    "data-notes": ("UNVERIFIABLE", "the fx_daily/fx_monthly notes' counts were re-derived today: fx_daily 6706 rows, 0 weekend "
        "dates, 0 blank cells, sorted and unique; fx_monthly 669 months, EUR blank before 1999-01 in 336 months, first EUR month "
        "1999-01, the other nine currencies non-blank in 336 months before 1999-01 (scripts/data-tooling-r26/checks.py). The "
        "parenthetical that the release's monthly series are monthly averages (RXI$US_N.M.EU = mean of the daily values, "
        "tested on the 2026-10-19 H.10 zip) was not re-tested: that zip's bytes are not kept (the live zip changed)."),
    "data-ddp-header": ("PASS", "Header lines 11-14 are outside the changed hunks (data_sources.yaml @@ +31 and +65). Freshness: "
        "today's live H.10 zip has sha256 17d087d0... (MANIFEST records 8f370f9c..., retrieved 2026-10-19); the header's "
        "statement is about the 2026-10-19 download and remains true as a record; the snapshots rebuild byte-identically "
        "from today's zip (scratch --fetch: cmp identical)."),
    "data-no-personal-data": ("PASS", "grep -rn -i 'mailto\\|@[a-z]' over tools/*.py and tests/test_fetch_data.py: the only "
        "hit is tests/test_fetch_data.py:291, the assertion that the User-Agent carries no '@' or 'mailto'; no address is sent. "
        "User-Agent strings are 'quant-finance-curriculum/0.1 ...' (tools/fetch_data.py:59, tools/fetch_vendor.py:44, "
        "tools/vendor.py:70 'quant-phd-vendor/1.0')."),
    "wp7-header-first-served": ("PASS", "Header passage outside the changed hunks (@@ +31 and +65)."),
    "wp7-release-pages-and-notice": ("PASS", "Re-read today: https://www.federalreserve.gov/data/data-download-fred-information.htm "
        "HTTP 200, 85993 bytes: 'the Board plans to remove the “Build Your Package” option from the Data Download Program "
        "the week of November 9, 2026. Historical data will remain available for download as XML files on statistical release "
        "pages.' (dated July 16, 2026). https://www.federalreserve.gov/releases/h10/about.htm HTTP 200, 84844 bytes, 'Last "
        "Update: February 06, 2023'; no copyright, licence or terms-of-use sentence (counts 0 for 'public domain', 'copyright', "
        "'permission', 'may be copied', 'terms of use')."),
    "wp7-nine-retrieval-dates": ("PASS", "grep -c '2026-10-19': project.html 143, 204, 406; L05.html 722, 1205; L08.html 366, "
        "882 (7 in pages) and cards.json 1279, 1294 (2): 9 occurrences, the same nine as the row. None is on the changed "
        "project.html line 195. MANIFEST keeps retrieved 2026-10-19 (fx_daily, fx_monthly) (committed file unchanged since 5e5da87)."),
    "doc-claude-md-data": ("PASS", "CLAUDE.md line 79 changed (Conventions: 'Python 3.12+' -> 'Python 3.14+'); the repository "
        "states the same: pyproject.toml requires-python '>=3.14', mypy python_version 3.14, ruff target-version py314 "
        "(git show HEAD:pyproject.toml). Hard rules 1 and 5 and the gates block are outside the hunk."),
    "doc-blueprint-5.3": ("PASS", "BLUEPRINT.md section 5.3 heading is at line 290; the changed hunks are lines 75-76 and 356 "
        "(git diff -U0). Passage carried."),
    "doc-blueprint-7-tree": ("PASS", "BLUEPRINT.md section 7 tree line 385 ('fetch_vendor.py vendor_spec.yaml'); the changed "
        "hunks are lines 75-76 and 356. Passage carried. The tree does not list tools/vendor.py (see R26-vendor-two-systems)."),
    "doc-verifier-2.8": ("PASS", "VERIFIER_RULES.md 2.8 'What is reproducible' as now written (hunk @@ +152,10): raw_sha256 "
        "is a provenance record and is not compared by `fetch_data.py --check` (check() compares snapshot sha256, header, rows, "
        "bytes, first/last keys and MANIFEST fields: tools/fetch_data.py:345-392); the rebuild from a scratch --fetch is "
        "byte-identical (cmp, logs/fetch_fetch.log); scripts are kept under ledgers/S7/scripts/<slice>-r<round>/ (this round)."),
    "ci-data-jobs": ("PASS", "CI gates job runs `python tools/fetch_data.py --check` (exit 0 here); live-data job runs "
        "`python tools/fetch_data.py --fetch` then `git diff --exit-code -- 'course/assets/data/market/*.csv'`: the scratch "
        "--fetch reproduced the three CSVs byte-identically (cmp). The job does not compare MANIFEST, so a retrieval date or "
        "raw hash change is not a CI failure (MANIFEST is not byte-compared; see R26-data-rebuild-live)."),
    "lab-mech-browser": ("PASS", "Re-run this round on the changed tools/page_smoke.py: `page_smoke.py --unit S7` PASS on every "
        "page (logs/page_smoke_S7.log); the labs' lab_preload and Pyodide package preload ran (boot 1.0 s, preload 0.2 s; each "
        "lab 0.0-1.3 s; the 10 s budget)."),
    "lab-data-usage-project-3": ("PASS", "project.html changed only at line 195 (git diff -U0); lab-S7-project-3's data-files "
        "and twin are unchanged; `run_labs.py --unit S7` PASS 42/42 (logs/run_labs_all.log) and page_smoke's Pyodide run of "
        "project-3 PASS (logs/page_smoke_S7.log)."),
    "cards-L08-c227": ("PASS", "cards.json is byte-identical; the cited L01 Theorem 2.1 is at L01.html line 82 and the "
        "changed hunk is line 133 only (git diff -U0); L08 line 272 is unchanged."),
    "r21-L01-s6-sentence": ("PASS", "L01 Section 6 sentence at line 255; the changed hunk is line 133 only (git diff -U0), so "
        "the passage is byte-identical. The sentence contains no number that page_smoke would recompute."),
    "r16-plain-title-spec": ("PASS", "tools/build_site.py changed at line 382 only (git diff -U0). plain_title and "
        "_TEX_INLINE_MATH (lines 105-110) and full_cite (line 138) are unchanged. `build_site.py --check` PASS (logs/build_site_check.log) "
        "and tests/test_build_site.py passes (391 slice tests)."),
    "r16-equiv-P04": ("PASS", "The regex at tools/build_site.py lines 105-110 is unchanged (the only hunk is line 382, git diff -U0): "
        "the equivalence claim is about that regex, carried. tests/test_build_site.py passes."),
    "site-family-name": ("PASS", "tools/build_site.py: only line 382 changed (the family_name / full_cite code is unchanged); "
        "`build_site.py --check` PASS and tests/test_build_site.py passes this round."),
    "refs-issue-no-verdict-change": ("PASS", "tools/refs/match.py and parse.py are unchanged; `verify_refs.py --offline` "
        "560 entries 0 problems and the S7 live run 94 of 560, 0 problems (this round)."),
    "r16-refs-live-scope-count": ("PASS", "Scoped live run this round: `verify_refs.py --unit S7` = 94 of 560 entries, 0 "
        "problems; the S7 scope at 5e5da87 is also 94 (scripts/data-tooling-r26/checks.py)."),
    "r25-registry-live-S7": ("PASS", "`verify_refs.py --unit S7` this round: 94 of 560 entries, 0 problems (the round-25 count "
        "was 93 of 559 at 190cd51; the S7 scope at 5e5da87 is 94)."),
    "r25-licence-disclaimer": ("PASS", "disclaimer.htm re-read this round (HTTP 200): the quoted sentence is present; "
        "it grants redistribution (see data-h15-note)."),
    "r25-banned-phrases": ("PASS", "Scan of the lines added between 5e5da87 and HEAD in course/modules/S/S7 (incl. project.html "
        "line 195) and tools/data_sources.yaml: 0 hits for the banned strings (TODO, TBD, lorem, for brevity, details omitted, "
        "beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is "
        "well known, obviously, clearly, roughly half, the ellipsis character). Observation: 30 ellipses in quiz prompts "
        "('...is…') exist in L01-L08 unchanged since the release; BUILDER_RULES 1.3 bans 'an ellipsis standing for omitted content'. "
        "Not a changed line; reported, not decided here."),
    "banned-phrases": ("PASS", "The same added-line scan as r25-banned-phrases (5e5da87..HEAD, S7 pages and data_sources.yaml): 0 hits."),
    "r24-yaml-rebuild-identical": ("PASS", "Live rebuild this round (scratch copy of HEAD, `fetch_data.py --fetch`): the "
        "three CSVs are byte-identical to the committed files (cmp; sha256 fx_daily 02872dd7..., fx_monthly 60572240..., "
        "ust_daily dd70e1a2...)."),
    "r24-yaml-header-replaced-claim": ("PASS", "Header passage outside the changed hunks (@@ +31 and +65); the historical "
        "statement is about the 2026-10-17 build and stands as a record."),
    "r23-yaml-header-stale": ("PASS", "Header comment passage outside the changed hunks; MANIFEST raw hashes differ from today's "
        "live zips, which the header already records as a historical retrieval (see data-ddp-header)."),
    "r25-licence-disclaimer-2": ("PASS", "see r25-licence-disclaimer"),
    "r24-reg-jiang2025endogeneity": ("PASS", "Registry entry jiang2025endogeneity unchanged between 5e5da87 and HEAD (checks.py: "
        "only used_by changed for four entries, none of them jiang); registry offline integrity 560 entries, 0 problems."),
    "cite-harvey2015cross-c204": ("PASS", "L06.html and cards.json are byte-identical; harvey2015cross is unchanged in the "
        "registry (checks.py); the registry offline check passes (560, 0 problems)."),
    "cite-jensen2023there": ("PASS", "L06.html and the registry entry jensen2023there are unchanged (checks.py); offline 560, 0 problems."),
    "cite-kao2025estimated-c234": ("PASS", "Citation side only: the registry entry kao2025estimated is unchanged; the card's numeric "
        "content (if any) is not re-derived by this row."),
    "registry-count-556": ("PASS", "Registry count now 560: header count 560, 560 entries (checks.py, verify_refs --offline). The "
        "round-25 count was 559; the row's count is historical."),
    "doc-verifier-2.1": ("PASS", "VERIFIER_RULES 2.1 (lines 41-44, unchanged) names the scoped run, the whole-registry run and the "
        "integrity scope; `verify_refs.py --help` lists the modes and the scoped run, `--unit S7`, was run this round (94 of 560, "
        "0 problems). The CI line numbers the row cites have moved (ci.yml changed); the CI jobs are now checked by R26-ci-gates-commands."),
    "cite-L08-jacobs2020anomalies": ("PASS", "L08.html unchanged; registry entry jacobs2020anomalies unchanged (checks.py); offline 560, 0 problems."),
    "cite-kravitz2023quantifying-registry": ("PASS", "L06.html unchanged; registry entry kravitz2023quantifying unchanged; offline 560, 0 problems."),
    "numbers-project-lab3": ("UNVERIFIABLE", "project.html changed only at line 195 and the lab-S7-project-3 run passes (run_labs "
        "42/42, page_smoke Pyodide PASS), but the hypothesis and interpretation numbers and the exemplar memo's trial-matrix "
        "numbers are prose derivations not re-derived this round."),
    "chg-L01-lab1-table": ("UNVERIFIABLE", "the lab-S7-L01-1 code and its expected block pass run_labs (42/42) and page_smoke "
        "(Pyodide, 0.2 s); the second table's numbers (L01 lines 140-169 and its derived readings) were not re-derived."),
    "chg-L01-M2-sentence": ("UNVERIFIABLE", "L01 line 513 (M2 solution) numeric claim not re-derived this round."),
    "chg-L01-E1-solution": ("UNVERIFIABLE", "L01 line 588 (E1 solution) numeric claim not re-derived this round."),
    "r22-L01-M5-numbers": ("UNVERIFIABLE", "L01 lines 528-530 numbers depend on NormalDist.inv_cdf and are not re-derived this round."),
    "chg-H01-L01-M1c": ("UNVERIFIABLE", "L01 Problem M1 solution numbers (lines 501-508) not re-derived this round."),
    "r23-b7-sweep": ("UNVERIFIABLE", "a whole-lesson sweep of L01/L08 cards and prose; the L01 caption it covers was re-derived "
        "(R26-L01-caption-numbers) but the sweep's other claims were not re-run."),
    "hours-sums-hub-curriculum": ("UNVERIFIABLE", "curriculum.json changed (lines 5869-6076); render_curriculum reproduces the "
        "committed outputs (exit 0, diff exit 0) and build_site --check passes, but the hours sum was not re-summed by this row."),
    "r25-hours-S7": ("UNVERIFIABLE", "same as hours-sums-hub-curriculum: generated outputs current, arithmetic not re-summed this round."),
    "mut-plain_title-survivors": ("UNVERIFIABLE", "tools/build_site.py changed (line 382, a renamed unused variable); the "
        "mutants were not re-run; the killing test file passes (tests/test_build_site.py in the 391-test slice run)."),
    "r16-mut-plain-title-killed": ("UNVERIFIABLE", "tools/build_site.py changed; mutants not re-run (see mut-plain_title-survivors)."),
    "mutant-P-V-family-r18": ("UNVERIFIABLE", "tools/build_site.py and tools/verify_refs.py: build_site changed; mutants not re-run."),
    "r25-diff-scope": ("UNVERIFIABLE", "this row covered 190cd51..f4190a4; the round-26 hunk coverage is R26-diff-coverage."),
    "figure-screenshots-360": ("UNVERIFIABLE", "figure screenshots at 360 px were not taken this round; page_smoke's geometry "
        "check passes in the light theme (page_smoke S7 PASS)."),
    "r20-banned-phrases-added-lines": ("PASS", "Added-line scan between 5e5da87 and HEAD (S7 pages, tools/data_sources.yaml): "
        "0 banned-string hits (see r25-banned-phrases)."),
}

MANUAL.pop("r25-licence-disclaimer-2", None)
MANUAL["r25-data-live-refetch"] = ("PASS", "Re-run this round: the scratch --fetch rebuilt the three snapshots byte-identically "
    "(cmp; logs/fetch_fetch.log). The row's claim that the download hashes equal MANIFEST does NOT hold today: the live zips changed "
    "(H.10 now 17d087d0..., MANIFEST 8f370f9c...; H.15 now 0a5685bd..., MANIFEST 334a7f88...). VERIFIER_RULES 2.8 makes raw_sha256 a "
    "provenance record, not a reproduction criterion, so the snapshot criterion passes and the raw-hash divergence is recorded as a "
    "freshness flag. The committed MANIFEST keeps the 2026-10-19/20 retrieval dates.")
MANUAL_CARRY = {  # passage-level carries decided by line numbers (git diff -U0 hunks listed in each note)
    "r22-L01-koning-span": ("course/modules/S/S7/L01.html", "line 133",
                            "The Koning span is at line 436 (outside the hunk)."),
}

NUM_LEFT: list[str] = []


def decide(row: dict[str, Any]) -> dict[str, Any]:
    rid = row["id"]
    if rid in CMD_EVIDENCE:
        return fresh(row, "PASS", CMD_EVIDENCE[rid])
    if rid in CMD_UNVERIFIABLE:
        out = fresh(row, "UNVERIFIABLE", f"NOT re-run in round 26: {CMD_UNVERIFIABLE[rid]}. Round-25 evidence: "
                f"{row['evidence'][:300]}")
        out["fix"] = "Run the command on the current toolchain and archive its output."
        return out
    if rid in MANUAL:
        status, evidence = MANUAL[rid]
        if status == "PASS":
            return fresh(row, "PASS", evidence)
        return unverifiable(row, evidence)
    if rid in MANUAL_CARRY:
        file, lines, note = MANUAL_CARRY[rid]
        return carried_passage(row, file, lines, note)
    subj = subjects(row)
    hit = sorted(set(subj) & CHANGED)
    numeric = bool(NUMERIC.search(row["check"])) or bool(NUMERIC_EVIDENCE.search(row["evidence"]))
    if hit:
        if hit == ["references/references.json"] and not numeric:
            return fresh(row, "PASS", f"Re-run this round: verify_refs.py --unit S7 (94 of 560, 0 problems) and "
                         f"--offline (560, 0 problems); the registry entries cited here are unchanged between {BASE} and HEAD "
                         f"(scripts/data-tooling-r26/checks.py: only used_by changed for hansen1991implications, "
                         f"kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone; header count and generated_at "
                         f"changed). Round-25 evidence: {row['evidence'][:500]}")
        return unverifiable(row, f"its subject {hit} changed since {BASE} and no round-26 re-derivation covers this row")
    if not subj:
        return unverifiable(row, "its subject files are not named in the location (cannot prove byte-identity)")
    if numeric:
        return unverifiable(row, "its claim depends on toolchain numerics (numpy/scipy/NormalDist/RNG or a figure readout) "
                            "and was not re-derived this round")
    if "2.5" in row["check"]:
        # Lab rows: the twin-to-page and Pyodide checks were re-run this round, so the run is the evidence.
        base = carried(row, subj)
        return fresh(row, "PASS", "Re-run this round: `tools/run_labs.py --unit S7` = 'run_labs S7: PASS (42/42)' on CPython "
                     "3.14.8 under -I -W error (logs/run_labs_all.log), and page_smoke's Pyodide run of every S7 lab matched its "
                     "page block (logs/page_smoke_S7.log). " + base["evidence"])
    return carried(row, subj)


REGISTRY_CHANGED_KEYS_NONE: set[str] = set()

# Round-26 rows for checks that the round-25 ledger did not have.
NEW_ROWS: list[dict[str, Any]] = [
    {"id": "R26-vendor-two-systems", "check": "2.9-structure, 2.5-tools: one vendoring path, one lock file (tools/vendor.py vs tools/fetch_vendor.py)",
     "location": "tools/vendor.py (new since 5e5da87, 242 lines); course/assets/vendor/SPEC.yaml (new); tools/vendor_spec.yaml; tools/fetch_vendor.py; course/assets/vendor/LOCK.json",
     "status": "FAIL",
     "evidence": "Two vendoring tools write the same LOCK.json with different schemas. tools/fetch_vendor.py (the CI and CLAUDE.md "
                 "path, pins in tools/vendor_spec.yaml) writes LOCK.json with a 'files' list; tools/vendor.py (pins in "
                 "course/assets/vendor/SPEC.yaml) reads and writes LOCK.json with a 'packages' list. Observed: `.venv/bin/python -I "
                 "tools/vendor.py check` -> 'FAIL vendor assets not installed; run `python3 tools/vendor.py install`', exit 1 "
                 "(logs/vendor_py_check.log); `.venv/bin/python -I tools/vendor.py install` -> uncaught KeyError: 'packages' "
                 "(the traceback names line 170, the LOCK read; no network used, no file written). `vendor.py lock` would "
                 "overwrite LOCK.json (tools/vendor.py:119) with the 'packages' schema, breaking tools/fetch_vendor.py --check. KaTeX "
                 "pin conflict: course/assets/vendor/SPEC.yaml says katex 0.18.9; tools/vendor_spec.yaml and LOCK.json say 0.19.1. "
                 "fetch_vendor.py --check PASS (56 files, 0 problems; logs/fetch_vendor_check.log). tests/test_vendor.py passes, but "
                 "it covers only the new tool's functions. Fix: retire tools/vendor.py and course/assets/vendor/SPEC.yaml, or wire "
                 "vendor.py to its own lock file and document it; the CLAUDE.md and README.md name fetch_vendor.py only.",
     "fix": "Delete tools/vendor.py, tests/test_vendor.py and course/assets/vendor/SPEC.yaml (fetch_vendor.py and vendor_spec.yaml are the "
            "tools CI and the docs use), or give vendor.py its own lock file and a documented purpose; then re-run fetch_vendor --check."},
    {"id": "R26-ci-gates-commands", "check": "2.9-structure: every command in .github/workflows/ci.yml runs as written (CI cannot run here; each command run locally)",
     "location": ".github/workflows/ci.yml (jobs gates, course, labs, live-citations, live-data)",
     "status": "PASS",
     "evidence": "Each step's command was run locally in this checkout with the venv (Python 3.14.8, the CI's version family): "
                 "ruff check ., ruff format --check ., mypy (--no-incremental; plain `mypy` reads pyproject files), pytest (434 passed), "
                 "render_curriculum + git diff --exit-code (exit 0), build_site --check, verify_refs --offline, fetch_data --check, "
                 "check_pages/check_dag/check_projects --all, fetch_vendor (default mode: 56 files, 0 problems), run_labs --all "
                 "(S7 42/42, AP1 22/22), run_graders --all --seeds 0-49 (S7 and AP1 PASS 50/50), mutate_graders --all --seeds 0-9 "
                 "(S7 164/164 killed, AP1 69/69 killed), `python -m playwright install --dry-run chromium` (exit 0; chromium-1248 "
                 "present), `python tools/fetch_data.py --fetch` (scratch: CSVs byte-identical). The argument parsers of verify_refs, "
                 "page_smoke, mutate_graders, run_graders and fetch_data accept --help. All step names and paths exist (checked "
                 "with the file list). Non-blocking: requirements-dev.txt lists playwright==1.64.1 twice (identical pins, harmless). "
                 "Logs: scratch logs/*.log, referenced above."},
    {"id": "R26-ci-not-run-here", "check": "2.9-structure: CI steps that could not be run in full here",
     "location": ".github/workflows/ci.yml: `python tools/page_smoke.py --all` (course job) and `python tools/verify_refs.py` (live-citations job, whole registry)",
     "status": "UNVERIFIABLE",
     "evidence": "page_smoke --all also covers the AP1 pages, which are outside this slice; only --unit S7 was run (PASS). The whole-"
                 "registry live run (`verify_refs.py` with no unit, scheduled weekly) was not run, to avoid re-querying ~560 hosts "
                 "in one session; the S7 scope was run live (94 of 560, 0 problems). The scheduled job's result is therefore not "
                 "verified here."},
    {"id": "R26-data-rebuild-live", "check": "2.8-manifest: live rebuild of the three snapshots in a scratch copy of HEAD",
     "location": "course/assets/data/market/{fx_daily,fx_monthly,ust_daily}.csv; course/assets/data/market/MANIFEST.json; tools/fetch_data.py --fetch",
     "status": "PASS",
     "evidence": "git archive HEAD -> scratch; `tools/fetch_data.py --fetch` (exit 0, 'fetch_data: 3 datasets, 0 problems'): fx_daily "
                 "6706 rows (cmp IDENTICAL to the committed CSV), fx_monthly 669 rows (IDENTICAL), ust_daily 6690 rows (IDENTICAL). "
                 "The live raw zips changed since the MANIFEST records: H.10 now sha256 17d087d0... (MANIFEST 8f370f9c..., retrieved "
                 "2026-10-19), H.15 now 0a5685bd... (MANIFEST 334a7f88..., retrieved 2026-10-20). Per VERIFIER_RULES 2.8, raw_sha256 "
                 "is provenance, the snapshots are the pass criterion, and the retrieval dates are kept (the scratch MANIFEST differs "
                 "only in retrieved and raw_sha256, not written to the checkout). Logs: logs/fetch_fetch.log, scratch diff."},
    {"id": "R26-licence-pages", "check": "2.8-licence: licence and source pages re-read with plain curl (no bot check or block met)",
     "location": "https://www.federalreserve.gov/disclaimer.htm; /releases/h10/about.htm; /releases/h15/default.htm; /data/data-download-fred-information.htm",
     "status": "PASS",
     "evidence": "curl -sS -L (default curl user agent, no bypass): all four HTTP 200 (sizes 85130, 84844, 105950, 85993 bytes). "
                 "disclaimer.htm: 'Unless otherwise indicated, information on Board's website is in the public domain and may be "
                 "copied and distributed without permission. Please cite to the Board as the source of the information.' about.htm: "
                 "'Last Update: February 06, 2023'; 'The rates have been certified by the Federal Reserve Bank of New York for customs "
                 "purposes'; no copyright, licence, permission or terms-of-use sentence. h15/default.htm: footnote 9 'Source: U.S. "
                 "Treasury'. DDP page: 'remove the “Build Your Package” option ... the week of November 9, 2026. Historical "
                 "data will remain available for download as XML files on statistical release pages.' (dated July 16, 2026). Pages in "
                 "scratch: logs and pages/ (not committed). Not re-read: copyright.gov 17 U.S.C. 105 (not needed by the H.10 note)."},
    {"id": "R26-L01-caption-numbers", "check": "2.2-numbers: the reworded L01 Figure 1 caption (line 133, the only L01 hunk since 5e5da87)",
     "location": "course/modules/S/S7/L01.html line 133 (figcaption): 2.146 vs 1.539 (N=10), 3.035 vs 2.508 (N=100), 4.292 vs 3.852 (N=10,000); gaps 0.61, 0.53, 0.44",
     "status": "PASS",
     "evidence": "Re-derived from scratch by ledgers/S7/scripts/data-tooling-r26/l01_figcaption_gaps.py (scipy 1.18.0 quad of "
                 "x*N*phi(x)*Phi(x)^(N-1); bound sqrt(2 ln N)): N=10 bound 2.145966, exact 1.538753, gap 0.607213; N=100 bound "
                 "3.034854, exact 2.507594, gap 0.527261; N=10000 bound 4.291932, exact 3.851616, gap 0.440316. Every printed figure "
                 "rounds to the page's value (output logs/l01_gaps.out). The exact value at N=2 is 0.564190 = 1/sqrt(pi). The "
                 "'roughly half' sentence the caption replaced is absent (grep)."},
    {"id": "R26-project-line195", "check": "2.2-numbers and 2.9-structure: the reworded project.html line 195 (versions the grader runs)",
     "location": "course/modules/S/S7/project.html line 195: 'Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs.'",
     "status": "PASS",
     "evidence": "course/assets/vendor/pyodide/pyodide-lock.json (LOCK-locked Pyodide 314.0.7): info.python 3.14.2, numpy 2.4.6, "
                 "pytest 9.0.2 (python -I read). The sentence's versions match: Python 3.14, NumPy 2.4, pytest 9.0."},
    {"id": "R26-figure-kernel-tolerance", "check": "2.5-tests: tests/test_figure_kernels.py tolerance change (rel = max(1e-12, 5e-14*(n-1)))",
     "location": "tests/test_figure_kernels.py lines 355-361; course/assets/js/stats.js normCdf (JS) vs statistics.NormalDist",
     "status": "PASS",
     "evidence": "Re-derived: the page's own normCdf (node 24.22.0 importing course/assets/js/stats.js, "
                 "ledgers/S7/scripts/data-tooling-r26/normcdf_compare.mjs) at x=-3 is 0.0013498980316301150; NormalDist(0,1).cdf(-3) "
                 "is 0.0013498980316300957: relative difference 1.4e-14. At x=-0.5, 0, 1.2, 4 the values agree to 1e-16 or better "
                 "(logs/normcdf_js.out, logs/normcdf_py.out). The pdf^(n-1) relative error is (n-1) times the cdf error, so 5e-14*(n-1) "
                 "covers it; the 1e-12 floor is unchanged for small n. The test passes (in the 391-test slice run). The claim in the "
                 "test's comment ('~1e-14 relative at x = -3') is confirmed."},
    {"id": "R26-koning-spot-test", "check": "2.5-tests: tests/test_koning_spot.py (new Monte Carlo spot check, seed 20261021)",
     "location": "tests/test_koning_spot.py (53 lines, new since 5e5da87)",
     "status": "PASS",
     "evidence": "Ran in the slice (391 passed) and in the full suite (434 passed). The seed is fixed and the tolerance is 6 standard errors "
                 "of a Bernoulli(0.05) mean over 400000 paths (the file's own constant). Deterministic under numpy 2.4.6 (the RNG "
                 "stream is default_rng's PCG64; the test passed on this toolchain)."},
    {"id": "R26-page-smoke-changes", "check": "2.5-tests: tools/page_smoke.py changes (lab_preload ast-based, strict KaTeX, separate boot/preload timers)",
     "location": "tools/page_smoke.py (diff hunks at lines 10, 30, 43-63, 117-147, 220-269); tests/test_page_smoke.py (8 tests); tools/katex_strict.js; course/assets/data/notation.json (the macro table strict_math reads); course/assets/js/lab.js, data.js, theme.js, rubric.js (site runtime, exercised by the S7 page runs in both themes)",
     "status": "PASS",
     "evidence": "Read every hunk. lab_preload parses each lab's code with ast.parse and raises SyntaxError naming the lab; run_labs reports it "
                 "as a problem (returns [f'{page}: lab code cannot be preloaded']). Imports are collected from the parsed tree only, so "
                 "imports inside functions are not preloaded (labs that import inside a function would load their package during the "
                 "timed run; none of the 34 S7 labs does this, as page_smoke's timings show). The preload evaluate throws on r.error "
                 "(py-worker.js run returns {error}). Boot and preload are printed separately (boot 1.0 s, preload 0.2 s). Live: "
                 "`page_smoke.py --unit S7` PASS on all 8 pages + 3 site pages (logs/page_smoke_S7.log); tests/test_page_smoke.py 8 "
                 "tests pass (in the slice run). strict_math: katex_strict.js is exercised by tests/js/katex_strict.test.mjs (test_js "
                 "passes in the slice run)."},
    {"id": "R26-run-labs-tool", "check": "2.5-labs: tools/run_labs.py and coursekit.labs_in / compare_output (rewritten tests in tests/test_run_labs.py)",
     "location": "tools/run_labs.py; tools/coursekit.py (labs_in, compare_output); tests/test_run_labs.py (2 tests, one parametrised over 5 cases)",
     "status": "PASS",
     "evidence": "`run_labs.py --all` PASS (S7 42/42, AP1 22/22; logs/run_labs_all.log) under CPython 3.14.8 with -I -W error and the "
                 "scratch cwd; tests/test_run_labs.py passes. Local TIME_LIMIT_S is 30 s (run_labs.py:47), the Pyodide budget is "
                 "10 s (page_smoke LAB_LIMIT_S); the local limit is the CPython check, the 10 s is checked in page_smoke (S7 max "
                 "1.3 s). Observation: two different limits in two tools, documented in each docstring."},
    {"id": "R26-requirements-pins", "check": "2.9-structure: requirements-dev.txt pins are the versions this round ran",
     "location": "requirements.txt (pyyaml==6.0.3); requirements-dev.txt (pytest 9.0.2, ruff 0.17.2, mypy 2.4.0, numpy 2.4.6, scipy 1.18.0, playwright 1.64.1)",
     "status": "PASS",
     "evidence": "importlib.metadata on .venv (python -I): ruff 0.17.2, mypy 2.4.0, playwright 1.64.1; numpy 2.4.6, scipy 1.18.0, pytest 9.0.2 "
                 "(python -I -c). All match the pins."},
    {"id": "R26-mypy-excludes", "check": "2.9-structure: pyproject.toml mypy excludes two lab twins (numpy 2.4 typing)",
     "location": "pyproject.toml [tool.mypy] exclude = [lab-S7-L08-4.py, lab-S7-L03-2.py]",
     "status": "PASS",
     "evidence": "`.venv/bin/mypy --no-incremental`: 'Success: no issues found in 102 source files' (logs/mypy.log). The two excluded twins "
                 "are not type-checked by mypy in CI; their runtime is checked by run_labs and page_smoke (42/42, 34 in Pyodide). The "
                 "exclusion's reason (numpy 2.4 stubs) is stated in the file; not re-verified by removing the exclusion this round."},
    {"id": "R26-killer-ids", "check": "2.6-mutation: every killing test named in the 152 tooling mutants exists and passes on HEAD",
     "location": "ledgers/S7/data-tooling.json mutants[].killed_by (83 distinct node ids)",
     "status": "PASS",
     "evidence": "pytest -o addopts= collects 83 of 83 distinct killed_by node ids and runs them: '83 passed in 2.52s', exit 0 "
                 "(logs/killer_ids.txt). This proves the killers exist and pass on HEAD; it does NOT prove the mutants are killed (see "
                 "R26-mutants-152-rerun)."},
    {"id": "R26-mutants-152-rerun", "check": "2.6-mutation: re-run the 152 tooling mutants against the current tests",
     "location": "ledgers/S7/data-tooling.json mutants (152 entries); ledgers/S7/mutants/ holds grader mutants only",
     "status": "UNVERIFIABLE",
     "evidence": "The 152 entries record only a description and a killing test; the mutated sources were applied by hand in earlier rounds "
                 "from scratch copies and were never archived under ledgers/S7 (no runner for tooling mutants exists in the repo; "
                 "`git log --all` finds no mutant-runner script for them). Re-deriving 152 patches from their prose descriptions "
                 "in this round was not done, so no kill is re-observed. The grader mutants (mutate_graders --unit S7 --seeds 0-9: "
                 "164/164 killed) are a different set and PASS. Action: archive the tooling mutant patches under "
                 "ledgers/S7/mutants/ or a runner under ledgers/S7/scripts/."},
    {"id": "R26-diff-coverage", "check": "2.9-structure: every changed file of the slice in 5e5da87..HEAD is named by a round-26 or carried row",
     "location": "git diff --name-only 5e5da87 HEAD over tools/, tests/, .github/, pyproject.toml, requirements*.txt, course/assets/data/, course/assets/js/, references/, and the S7 pages",
     "status": "PASS",
     "evidence": "Computed by the builder (ledgers/S7/scripts/data-tooling-r26/build_fragment.py: COVERAGE check). Every slice file named in "
                 "that diff appears in at least one row's location or evidence; the list is printed at build time."},
]


OTHER_SLICES = {  # changed in 5e5da87..HEAD but owned by another unit or a site-wide check (named in the notes)
    "course/assets/data/glossary.json", "course/assets/data/program.json", "course/assets/js/data.js",
    "course/assets/js/theme.js", "course/assets/js/rubric.js", "course/assets/js/lab.js", "tests/js/rubric.test.mjs",
}


def coverage_check(rows: list[dict[str, Any]]) -> list[str]:
    """Every changed slice file must be named in some row (location or evidence)."""
    text = "\n".join(f"{r['location']} {r['evidence']}" for r in rows)
    slice_changed = sorted(
        f for f in CHANGED
        if f.startswith(("tools/", "tests/", ".github/", "course/assets/js/", "course/assets/data/", "pyproject.toml",
                         "requirements")) and not f.startswith("tests/labs/AP1/")
        or f in {"references/references.json", f"{S7}/L01.html", f"{S7}/project.html"}
    )
    missing = [f for f in slice_changed if f not in text and f.rsplit("/", 1)[-1] not in text and f not in OTHER_SLICES]
    print(f"coverage: {len(slice_changed)} changed slice files, not named in any row: {missing}")
    return missing


NEW_ROWS.append({"id": "R26-test-memo-exemplars", "check": "2.5-tests: tests/test_memo_exemplars.py one-line change (unused count renamed _n_trials)",
     "location": "tests/test_memo_exemplars.py line 133",
     "status": "PASS",
     "evidence": "git diff -U0 5e5da87 HEAD: `n_obs, n_trials = trials.shape` -> `n_obs, _n_trials = trials.shape`; the unused name is "
                 "now marked unused, no assertion changed. The file passes in the full suite (434 passed, logs/pytest_full.log) and ruff is clean."})


def main() -> None:
    rows = [decide(r) for r in PREV["rows"]]
    seen = {r["id"] for r in rows}
    unknown = sorted(k for k in MANUAL if k not in seen)
    print("manual keys not in the round-25 ledger (ignored):", unknown)
    rows += NEW_ROWS
    for r in rows:
        if r["status"] != "PASS" and not r.get("fix"):
            r["fix"] = "Re-derive or re-run this row in a verifier round and archive the evidence."
    missing = coverage_check(rows)
    if missing:
        raise SystemExit(f"uncovered changed files: {missing}")
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate row ids"
    dropped = sorted(set(seen) - set(ids))
    assert not dropped, f"row ids dropped: {dropped}"
    mutants = []
    for m in PREV["mutants"]:
        mutants.append({**m, "round26": "killing test node exists and passes on HEAD (R26-killer-ids); the mutant itself was "
                                        "not re-run (R26-mutants-152-rerun)"})
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
    fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
    verdict = "PASS" if not fail_ids else "FAIL"
    registry_flags = [
        "Registry: 560 entries and header count 560 at HEAD (5e5da87 also 560). Four entries (hansen1991implications, "
        "kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone) gained AP1 in used_by since the release; no citation text changed.",
        "Working papers with published versions: unchanged from round 25 (koning2026anytime, roquain2022false).",
        "Live S7 scope: 94 entries at HEAD (the round-25 run said 93 of 559; the S7 scope at 5e5da87 was already 94).",
    ]
    freshness_flags = [
        "Live Federal Reserve zips changed after the MANIFEST retrieval dates (H.10 sha256 now 17d087d0..., H.15 now 0a5685bd...). "
        "The snapshots rebuild byte-identically; MANIFEST keeps 2026-10-19 and 2026-10-20 (VERIFIER_RULES 2.8).",
        "Disclaimer and about pages re-read 2026-10-27 (HTTP 200): licence text unchanged; about.htm still 'Last Update: February 06, 2023'.",
        "The DDP page (data-download-fred-information.htm, July 16, 2026) gives the removal of 'Build Your Package' as the week of November 9, 2026.",
    ]
    notes = (
        f"Round 26 (verifier for the S7 data-tooling slice, checkout /tmp/verify-s7-r1-dt pinned at 47bac8d; base {BASE}, the "
        "release commit). The slice's tooling changed since the release (tools/page_smoke.py, tools/data_sources.yaml, "
        "tools/build_site.py one line, tools/vendor.py (new), tools/vendor_spec.yaml, tools/katex_strict.js (new), tests/ "
        "(page_smoke, run_labs, koning_spot, vendor new or changed; figure_kernels and memo_exemplars one line each), "
        ".github/workflows/ci.yml, pyproject.toml, requirements*.txt). Every changed tooling hunk was read (git diff). "
        "Commands re-run on the new toolchain: ruff, mypy --no-incremental, full pytest (434 passed), the 11 slice test files "
        "(391 passed), render_curriculum and build_site --check, verify_refs --offline (560, 0 problems) and --unit S7 live "
        "(94 of 560, 0 problems), fetch_data --check, fetch_data --fetch in a scratch copy (CSVs byte-identical), check_pages, "
        "check_dag, check_projects (--all), run_labs --all, run_graders --all (50 seeds), mutate_graders (S7 0-9: 164/164; AP1 "
        "69/69), page_smoke --unit S7 (PASS), fetch_vendor --check, vendor.py check (FAIL, see R26-vendor-two-systems). The "
        "licence pages were re-read with plain curl. Not run: page_smoke --all (AP1 pages), the whole-registry live verify_refs "
        "run, the dark-theme figure sweep, the figure readout drive, the tooling mutants (no archived runner; see R26-mutants-152-rerun), "
        "fetch_data --raw-dir. Rows that depend on toolchain numerics and were not re-derived are UNVERIFIABLE, not carried. "
        "Carry rule used: (1) a whole file byte-identical to 5e5da87 uses the architect's prefix; (2) where a file changed only "
        "outside the passage a row cites, the row is carried with a passage-level prefix naming the git diff -U0 hunks (L01.html "
        "line 133, project.html line 195, data_sources.yaml hunks at new lines 31-37 and 65-71, build_site.py line 382, "
        "page_smoke.py hunks, references.json header and four used_by lines). Logs of this round are archived under ledgers/S7/scripts/data-tooling-r26/logs/ (copies of /tmp/ap1-r5/data-tooling/logs). Observations not failures: 30 quiz-prompt "
        "ellipses in L01-L08 (unchanged since the release; BUILDER_RULES 1.3 bans an ellipsis standing for omitted content); "
        "requirements-dev.txt lists playwright twice; two local lab time limits (30 s CPython, 10 s Pyodide)."
    )
    fragment = {
        "unit": "S7",
        "slice": "data-tooling",
        "round": 26,
        "verifier": "round 26, verify-s7-r1-dt (independent of the builders and of rounds 1-25's verifier sessions)",
        "pin": "47bac8d",
        "base": BASE,
        "previous_ledger": "ledgers/S7/data-tooling.json as of round 25 (412 PASS, 152 mutants; base 190cd51, head f4190a4)",
        "checkout": "/tmp/verify-s7-r1-dt",
        "scratch": "/tmp/ap1-r5/data-tooling",
        "verified_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "rows": rows,
        "mutants": mutants,
        "registry_flags": registry_flags,
        "freshness_flags": freshness_flags,
        "notes": notes,
        "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"],
                    "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutants),
                    "mutants_killed_by_test_present": sum(1 for m in mutants if m.get("killed_by")),
                    "fail_ids": fail_ids},
    }
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    problems = ledger.validate(fragment, "S7/data-tooling")
    print("validate:", problems)
    print("summary:", fragment["summary"])
    print("verdict:", verdict)


if __name__ == "__main__":
    main()
