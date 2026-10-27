"""Re-creation and re-observation of the 66 add_reference mutants carried in the S7 data-tooling ledger.

Every mutant is one exact text replacement in a fresh copy of HEAD (``git archive`` into a temp dir, so the
repository itself is never written). The anchor must occur exactly once in the target file. The named killer
tests are run with ``pytest -q -x`` in that copy. A mutant is KILLED when pytest exits 1 (a killer fails),
SURVIVED when every killer passes. The UNMUTATED control runs the union of all killers first and must pass.

Network: the copy's tests may reach urllib (PA1, KD1 do not patch the fetch). Every child process therefore gets
HTTP(S)_PROXY pointing at a closed local port, so no mutant can reach the internet. A kill that comes from that
refused connection is reported as such in ``first_failing`` / ``failure_excerpt``.

Usage (from the repository root, no install needed)::

    .venv/bin/python -I ledgers/S7/mutants/tooling-ar/harness.py            # all 66 mutants + control
    .venv/bin/python -I ledgers/S7/mutants/tooling-ar/harness.py --only R05  # one mutant

Writes ledgers/S7/mutants/tooling-ar/results.json and results.txt next to this file.
"""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PY = REPO / ".venv" / "bin" / "python"
TARGET = "tools/add_reference.py"
DEAD_PROXY = "http://127.0.0.1:9"  # closed port: any network attempt fails fast

T = "tests/test_refs.py::"
DRY = "test_a_dry_run_reports_what_the_run_would_do"
REG = "test_registered_finds_the_entry_that_holds_the_work"
ADMIT_NEW = "test_admit_adds_a_new_work_with_its_unit_source_and_status"
DESCRIBE_ONE = "test_describe_names_the_first_container_title_only"

# id, reading ("exact" | "inferred"), description (from the ledger), anchor, replacement, killer node ids
MUTANTS: list[dict[str, Any]] = [
    # ---- registered(): the entry that already holds the work
    {"id": "R01", "reading": "exact", "description": "registered(): DOI test replaced by 'entry has any DOI'",
     "anchor": 'return bool(e.get("doi") == work.doi)', "replacement": 'return bool(e.get("doi"))',
     "killers": [f"{T}{DRY}[dry-run-new]"]},
    {"id": "R02", "reading": "exact", "description": "registered(): DOI branch skipped (falls through to ISBN and URL)",
     "anchor": '        if work.doi:\n            return bool(e.get("doi") == work.doi)\n', "replacement": "",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "R03", "reading": "exact", "description": "registered(): shared-ISBN branch removed",
     "anchor": "        if work.isbn and set(e.get(\"isbn\") or []) & set(work.isbn):\n            return True\n",
     "replacement": "", "killers": [f"{T}{REG}[shared-isbn]"]},
    {"id": "R04", "reading": "exact", "description": "registered(): shared-ISBN overlap replaced by equality of the ISBN sets",
     "anchor": 'set(e.get("isbn") or []) & set(work.isbn)', "replacement": 'set(e.get("isbn") or []) == set(work.isbn)',
     "killers": [f"{T}{REG}[shared-isbn]"]},
    {"id": "R05", "reading": "exact", "description": "registered(): URL branch removed (always no match)",
     "anchor": 'return bool(work.url and e.get("url") == work.url)', "replacement": "return False",
     "killers": [f"{T}{REG}[url]"]},
    {"id": "R06", "reading": "exact", "description": "registered(): URL branch: any entry matches when the work has a URL",
     "anchor": 'return bool(work.url and e.get("url") == work.url)', "replacement": "return bool(work.url)",
     "killers": [f"{T}{REG}[url]"]},
    {"id": "R07", "reading": "exact", "description": "registered(): URL checked before the DOI",
     "anchor": "    def same(e: dict[str, Any]) -> bool:\n        if work.doi:\n",
     "replacement": '    def same(e: dict[str, Any]) -> bool:\n        if work.url and e.get("url") == work.url:\n            return True\n        if work.doi:\n',
     "killers": [f"{T}{REG}[doi-beats-url]"]},
    {"id": "R10", "reading": "exact", "description": "registered(): DOI test inverted (!=)",
     "anchor": 'e.get("doi") == work.doi', "replacement": 'e.get("doi") != work.doi',
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "R11", "reading": "exact", "description": "registered(): returns a copy of the entry",
     "anchor": "return next((e for e in entries if same(e)), None)",
     "replacement": "return next((dict(e) for e in entries if same(e)), None)",
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "R12", "reading": "exact", "description": "registered(): a work with no identifiers matches the first entry",
     "anchor": 'return bool(work.url and e.get("url") == work.url)',
     "replacement": 'return bool(work.url and e.get("url") == work.url) or not (work.doi or work.isbn or work.url)',
     "killers": [f"{T}{REG}[shared-isbn]"]},
    {"id": "R14", "reading": "exact", "description": "registered(): DOI mismatch falls through to the ISBN and URL branches",
     "anchor": '        if work.doi:\n            return bool(e.get("doi") == work.doi)\n',
     "replacement": '        if work.doi and e.get("doi") == work.doi:\n            return True\n',
     "killers": [f"{T}{REG}[doi-beats-url]"]},
    {"id": "R16", "reading": "exact", "description": "registered(): only the work's first ISBN is compared",
     "anchor": 'set(e.get("isbn") or []) & set(work.isbn)', "replacement": 'set(e.get("isbn") or []) & set(work.isbn[:1])',
     "killers": [f"{T}{REG}[isbn-second]"]},
    {"id": "R17", "reading": "exact", "description": "registered(): only the entry's first ISBN is compared",
     "anchor": 'set(e.get("isbn") or [])', "replacement": 'set((e.get("isbn") or [])[:1])',
     "killers": [f"{T}{REG}[shared-isbn]"]},
    {"id": "R20", "reading": "exact", "description": "registered(): an ISBN that does not match returns no match before the URL",
     "anchor": '        return bool(work.url and e.get("url") == work.url)',
     "replacement": '        if work.isbn:\n            return False\n        return bool(work.url and e.get("url") == work.url)',
     "killers": [f"{T}{REG}[isbn-miss-url]"]},
    {"id": "MU1", "reading": "exact", "description": "registered(): URL test without the work.url guard (None == None matches)",
     "anchor": 'return bool(work.url and e.get("url") == work.url)', "replacement": 'return bool(e.get("url") == work.url)',
     "killers": [f"{T}{REG}[no-identifier]"]},
    # ---- admit(): the run path (entry already held)
    {"id": "A01", "reading": "exact", "description": "admit(): run path looks up an empty registry",
     "anchor": "existing = registered(entries, work)", "replacement": "existing = registered([], work)",
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A02", "reading": "exact", "description": "admit(): run path replaces used_by instead of uniting it",
     "anchor": 'existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))',
     "replacement": 'existing["used_by"] = sorted(set(used_by))',
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A03", "reading": "exact", "description": "admit(): run path does not save the update",
     "anchor": '        registry.save(entries)\n        print(f"UPDATED', "replacement": '        print(f"UPDATED',
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A04", "reading": "exact", "description": "admit(): run path prints the DOI in place of the key",
     "anchor": "UPDATED {existing['key']}", "replacement": "UPDATED {existing['doi']}",
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A05", "reading": "exact", "description": "admit(): run path returns 1 after updating",
     "anchor": "used_by={existing['used_by']}\")\n        return 0", "replacement": "used_by={existing['used_by']}\")\n        return 1",
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A06", "reading": "exact", "description": "admit(): run path drops the source string",
     "anchor": 'existing["source_strings"] = sorted(set(existing["source_strings"]) | {source})',
     "replacement": 'existing["source_strings"] = sorted(set(existing["source_strings"]))',
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    {"id": "A07", "reading": "exact", "description": "admit(): run path keeps the held used_by and drops the units the run names",
     "anchor": 'existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))',
     "replacement": 'existing["used_by"] = sorted(set(existing["used_by"]))',
     "killers": [f"{T}{DRY}[run-unit-added]"]},
    {"id": "MS1", "reading": "exact", "description": "admit(): run path saves before it updates (the saved list is what a save writes)",
     "anchor": ('        existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))\n'
                '        existing["source_strings"] = sorted(set(existing["source_strings"]) | {source})\n'
                "        registry.save(entries)\n"),
     "replacement": ("        registry.save(entries)\n"
                     '        existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))\n'
                     '        existing["source_strings"] = sorted(set(existing["source_strings"]) | {source})\n'),
     "killers": [f"{T}{DRY}[run-unit-held]"]},
    # ---- admit(): the new-entry branch
    {"id": "NA1", "reading": "exact", "description": "admit() new entry: used_by dropped (stored as [])",
     "anchor": "used_by=list(used_by),", "replacement": "used_by=[],", "killers": [f"{T}{ADMIT_NEW}"]},
    {"id": "NA2", "reading": "exact", "description": "admit() new entry: source string dropped",
     "anchor": "source_strings=[source],", "replacement": "source_strings=[],", "killers": [f"{T}{ADMIT_NEW}"]},
    {"id": "NA3", "reading": "exact", "description": "admit() new entry: key taken without checking for collisions",
     "anchor": 'entry.key = next(k for k in (base, *(f"{base}{c}" for c in "bcdefghij")) if k not in taken)',
     "replacement": "entry.key = base",
     "killers": [f"{T}test_admit_does_not_reuse_a_key_the_registry_holds"]},
    {"id": "NA4", "reading": "exact", "description": "admit() new entry: entry not appended to the registry",
     "anchor": "    entries.append(entry.to_json())", "replacement": "    pass", "killers": [f"{T}{ADMIT_NEW}"]},
    {"id": "NA5", "reading": "exact", "description": "admit() new entry: registry not saved",
     "anchor": '    registry.save(entries)\n    print(f"ADDED', "replacement": '    print(f"ADDED',
     "killers": [f"{T}{ADMIT_NEW}"]},
    {"id": "NA6", "reading": "exact", "description": "admit() new entry: status 'pending' instead of 'verified'",
     "anchor": 'status="verified",', "replacement": 'status="pending",', "killers": [f"{T}{ADMIT_NEW}"]},
    {"id": "NA7", "reading": "exact", "description": "admit() new entry: verified_by replaced by 'manual'",
     "anchor": "verified_by=verified_by,\n    )", "replacement": 'verified_by="manual",\n    )',
     "killers": [f"{T}{ADMIT_NEW}"]},
    # ---- main(): argument rules
    {"id": "MS2", "reading": "exact", "description": "main(): --used-by no longer required",
     "anchor": "if not args.used_by:", "replacement": "if False:",
     "killers": [f"{T}test_admitting_a_reference_needs_a_unit"]},
    # ---- main(): dry run
    {"id": "D01", "reading": "exact", "description": "main(): dry run ignores the registry (always WOULD ADD)",
     "anchor": "existing = registered(registry.load(), work)", "replacement": "existing = None",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D02", "reading": "exact", "description": "main(): dry run looks up an empty registry",
     "anchor": "registered(registry.load(), work)", "replacement": "registered([], work)",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D03", "reading": "exact", "description": "main(): dry-run WOULD UPDATE omits the held entry's used_by",
     "anchor": "sorted(set(existing['used_by']) | set(args.used_by))", "replacement": "sorted(set(args.used_by))",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D04", "reading": "exact", "description": "main(): dry-run WOULD UPDATE names the DOI in place of the key",
     "anchor": "WOULD UPDATE {existing['key']}", "replacement": "WOULD UPDATE {existing['doi']}",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D05", "reading": "exact", "description": "main(): --dry-run ignored (the run executes)",
     "anchor": "if args.dry_run:", "replacement": "if False:",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D06", "reading": "exact", "description": "main(): dry run returns 1 after printing",
     "anchor": 'notes={notes}")\n        return 0', "replacement": 'notes={notes}")\n        return 1',
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D07", "reading": "exact", "description": "main(): dry run prints WOULD UPDATE and also WOULD ADD (the else is lost)",
     "anchor": '        else:\n            print(f"WOULD ADD', "replacement": '        if True:\n            print(f"WOULD ADD',
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D08", "reading": "exact", "description": "main(): dry-run branch condition inverted",
     "anchor": '        if existing is not None:\n            print(f"WOULD UPDATE',
     "replacement": '        if existing is None:\n            print(f"WOULD UPDATE',
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D09", "reading": "inferred", "description": "main(): dry-run used_by concatenated instead of united (duplicates shown)",
     "anchor": "sorted(set(existing['used_by']) | set(args.used_by))",
     "replacement": "sorted(existing['used_by'] + args.used_by)",
     "killers": [f"{T}{DRY}[dry-run-unit-held]"]},
    {"id": "D11", "reading": "exact", "description": "main(): dry-run WOULD UPDATE drops the units the new run would add",
     "anchor": "sorted(set(existing['used_by']) | set(args.used_by))", "replacement": "sorted(set(existing['used_by']))",
     "killers": [f"{T}{DRY}[dry-run-unit-added]"]},
    # ---- describe()
    {"id": "C01", "reading": "exact", "description": "describe(): every container title joined, not only the first",
     "anchor": "', '.join(work.container[:1])", "replacement": "', '.join(work.container)",
     "killers": [f"{T}{DESCRIBE_ONE}"]},
    {"id": "C02", "reading": "exact", "description": "describe(): the last container title, not the first",
     "anchor": "', '.join(work.container[:1])", "replacement": "', '.join(work.container[-1:])",
     "killers": [f"{T}{DESCRIBE_ONE}"]},
    {"id": "C03", "reading": "exact", "description": "describe(): container[0] in place of the join (IndexError when there is no container)",
     "anchor": "', '.join(work.container[:1])", "replacement": "work.container[0]",
     "killers": [f"{T}test_describe_handles_a_work_without_a_container"]},
    {"id": "C04", "reading": "exact", "description": "describe(): round-20 defect restored (tuple repr printed)",
     "anchor": "', '.join(work.container[:1])", "replacement": "work.container[:1]",
     "killers": [f"{T}{DRY}[dry-run-new]"]},
    {"id": "C05", "reading": "exact", "description": "describe(): comma after the title dropped",
     "anchor": "'{work.title}', {', '.join(work.container[:1])}", "replacement": "'{work.title}' {', '.join(work.container[:1])}",
     "killers": [f"{T}{DRY}[dry-run-new]"]},
    {"id": "C07", "reading": "exact", "description": "describe(): the last author, not the first",
     "anchor": 'first = work.authors[0].family if work.authors else "?"',
     "replacement": 'first = work.authors[-1].family if work.authors else "?"',
     "killers": [f"{T}test_describe_names_the_first_author"]},
    # ---- admit(): new book / stored fields
    {"id": "NB1", "reading": "exact", "description": "admit() new entry: the work's ISBNs stored empty",
     "anchor": "        work=work,", "replacement": '        work=type(work)(**{**vars(work), "isbn": ()}),',
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NB2", "reading": "exact", "description": "admit() new entry: the work's URL stored as null",
     "anchor": "        work=work,", "replacement": '        work=type(work)(**{**vars(work), "url": None}),',
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NB3", "reading": "exact", "description": "admit() new entry: authors stored empty",
     "anchor": "        work=work,", "replacement": '        work=type(work)(**{**vars(work), "authors": ()}),',
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NB4", "reading": "exact", "description": "admit() new entry: title stored empty",
     "anchor": "        work=work,", "replacement": '        work=type(work)(**{**vars(work), "title": ""}),',
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NB5", "reading": "exact", "description": "admit() new entry: the notes recorded at admission dropped",
     "anchor": "        notes=notes,", "replacement": "        notes={},",
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NB6", "reading": "exact", "description": "admit() new entry: the year stored as 0",
     "anchor": "        work=work,", "replacement": '        work=type(work)(**{**vars(work), "year": 0}),',
     "killers": [f"{T}test_admit_stores_the_identity_and_the_notes_of_a_new_book"]},
    {"id": "NK1", "reading": "exact", "description": "admit() new entry: the issuer short name not used for the key base",
     "anchor": "base = registry.base_key(work, short or None)", "replacement": "base = registry.base_key(work, None)",
     "killers": [f"{T}test_admit_keys_an_issuer_document_from_the_issuer_short_name"]},
    {"id": "TK1", "reading": "exact", "description": "admit() (control): the collision check sees no taken keys",
     "anchor": 'taken = {e["key"] for e in entries}', "replacement": "taken = set()",
     "killers": [f"{T}test_admit_does_not_reuse_a_key_the_registry_holds"]},
    # ---- by_isbn / by_landing / by_doi / main primary branch
    {"id": "IE1", "reading": "exact", "description": "by_isbn(): the edition-mismatch rejection removed",
     "anchor": "if ours is not None and theirs is not None and ours != theirs:", "replacement": "if False:",
     "killers": [f"{T}test_by_isbn_refuses_a_citation_of_another_edition"]},
    {"id": "LD1", "reading": "exact", "description": "by_landing(): a page that declares a DOI is admitted through --url",
     "anchor": '    if doi:\n        return None, {}, f"the page declares DOI', "replacement": '    if False:\n        return None, {}, f"the page declares DOI',
     "killers": [f"{T}test_by_landing_refuses_a_page_that_declares_a_doi"]},
    {"id": "LA1", "reading": "exact", "description": "by_landing(): a non-publisher domain accepted",
     "anchor": 'if authority_for(url, load_authorities("publishers")) is None:', "replacement": "if False:",
     "killers": [f"{T}test_by_landing_refuses_a_site_that_is_not_a_publisher"]},
    {"id": "KD1", "reading": "exact", "description": "by_doi(): a source that parses as neither article nor book is resolved by DOI",
     "anchor": 'if cand.kind not in ("article", "book"):', "replacement": "if False:",
     "killers": [f"{T}test_by_doi_resolves_only_articles_and_books"]},
    {"id": "PA1", "reading": "inferred", "description": "main(): a primary document on a non-issuer domain accepted",
     "anchor": "        if authority is None:", "replacement": "        if False:",
     "killers": [f"{T}test_a_primary_document_is_admitted_only_from_its_issuer"]},
    {"id": "PR1", "reading": "exact", "description": "main(): the primary-document title-recall check removed",
     "anchor": "if recall < PRIMARY_TITLE_RECALL:", "replacement": "if False:",
     "killers": [f"{T}test_a_primary_document_must_carry_its_own_title"]},
    # ---- verifier recorded per mode
    {"id": "VB1", "reading": "exact", "description": "main(): an --isbn admission recorded as verified by crossref",
     "anchor": 'verified_by, short = "openlibrary", ""', "replacement": 'verified_by, short = "crossref", ""',
     "killers": [f"{T}test_an_isbn_admission_is_verified_by_open_library"]},
    {"id": "VB2", "reading": "exact", "description": "main(): an --url article recorded as verified by issuer",
     "anchor": 'verified_by, short = "landing", ""', "replacement": 'verified_by, short = "issuer", ""',
     "killers": [f"{T}test_a_landing_page_admission_is_verified_by_its_landing_page"]},
    {"id": "VB3", "reading": "exact", "description": "main(): an --url primary document recorded as landing",
     "anchor": 'verified_by, short = "issuer", authority.short', "replacement": 'verified_by, short = "landing", authority.short',
     "killers": [f"{T}test_a_primary_document_admission_is_verified_by_its_issuer"]},
    # ---- judged()
    {"id": "JC1", "reading": "exact", "description": "judged(): a citation string that differs from the record is admitted",
     "anchor": "    if res.corrections:", "replacement": "    if False:",
     "killers": [f"{T}test_judged_refuses_a_citation_whose_string_differs_from_the_record"]},
    {"id": "JN1", "reading": "inferred", "description": "judged(): a record that does not match the citation loses its rejection reason",
     "anchor": r'return None, {}, f"record does not match the citation ({notes})\n  record: {describe(work)}"',
     "replacement": 'return None, {}, "record does not match the citation"',
     "killers": [f"{T}test_judged_says_why_a_record_does_not_match"]},
]

CONTROL_ID = "control"


def git_head() -> str:
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def make_copy(commit: str, tag: str) -> Path:
    """A fresh copy of the commit's tree, extracted from git archive; the repository is only read."""
    tree = Path(tempfile.mkdtemp(prefix=f"ar-{tag}-"))
    archive = subprocess.run(["git", "-C", str(REPO), "archive", commit], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(tree, filter="data")
    return tree


def child_env() -> dict[str, str]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "HTTP_PROXY": DEAD_PROXY, "HTTPS_PROXY": DEAD_PROXY,
                "http_proxy": DEAD_PROXY, "https_proxy": DEAD_PROXY, "NO_PROXY": "", "no_proxy": ""})
    return env


def preflight(tree: Path) -> str:
    """Confirms that the copy's tools/ modules are the ones imported (not the repository's)."""
    code = "import sys; sys.path.insert(0, 'tools'); import add_reference; from refs import registry; print(add_reference.__file__); print(registry.ROOT)"
    run = subprocess.run([str(PY), "-c", code], cwd=tree, env=child_env(), capture_output=True, text=True, timeout=120)
    lines = run.stdout.split()
    root = str(tree.resolve())  # /var is a symlink to /private/var on macOS
    if run.returncode != 0 or len(lines) != 2 or not all(str(Path(l).resolve()).startswith(root) for l in lines):
        raise RuntimeError(f"preflight failed: rc={run.returncode} out={run.stdout!r} err={run.stderr[-400:]!r}")
    return lines[0]


def run_killers(tree: Path, killers: list[str]) -> tuple[subprocess.CompletedProcess[str], float]:
    cmd = [str(PY), "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-o", "addopts=", *killers]
    started = time.monotonic()
    run = subprocess.run(cmd, cwd=tree, env=child_env(), capture_output=True, text=True, timeout=900)
    return run, time.monotonic() - started


def summarise(run: subprocess.CompletedProcess[str]) -> tuple[str, str, str]:
    out = run.stdout.splitlines()
    failed = [line.split(" ", 1)[1].split(" - ")[0] for line in out if line.startswith("FAILED ")]
    excerpt = next((line.strip() for line in out if line.startswith("E ")), "")[:300]
    tail = next((line for line in reversed(out) if line.strip()), "")
    return (failed[0] if failed else ""), excerpt, tail


def control(commit: str) -> dict[str, Any]:
    killers = list(dict.fromkeys(k for m in MUTANTS for k in m["killers"]))
    tree = make_copy(commit, "control")
    try:
        module = preflight(tree)
        run, secs = run_killers(tree, killers)
        first, excerpt, tail = summarise(run)
        return {"id": CONTROL_ID, "killers": killers, "rc": run.returncode, "seconds": round(secs, 2),
                "module": module, "status": "pass" if run.returncode == 0 else "FAIL", "summary": tail,
                "first_failing": first, "failure_excerpt": excerpt}
    finally:
        shutil.rmtree(tree, ignore_errors=True)


def mutant(commit: str, m: dict[str, Any]) -> dict[str, Any]:
    tree = make_copy(commit, m["id"])
    try:
        path = tree / TARGET
        text = path.read_text(encoding="utf-8")
        count = text.count(m["anchor"])
        base = {k: m[k] for k in ("id", "reading", "description", "anchor", "replacement", "killers")}
        base.update({"file": TARGET, "anchor_count": count})
        if count != 1:
            return {**base, "status": "error", "summary": f"anchor occurs {count} times, expected 1"}
        path.write_text(text.replace(m["anchor"], m["replacement"], 1), encoding="utf-8")
        module = preflight(tree)
        run, secs = run_killers(tree, m["killers"])
        first, excerpt, tail = summarise(run)
        if run.returncode == 0:
            status = "survived"
        elif run.returncode == 1:
            status = "killed"
        else:
            status = "killed-by-error"  # pytest internal/collection error: the mutant broke the test run
        return {**base, "status": status, "rc": run.returncode, "seconds": round(secs, 2), "module": module,
                "first_failing": first, "failure_excerpt": excerpt, "summary": tail}
    finally:
        shutil.rmtree(tree, ignore_errors=True)


def write_text_report(results: list[dict[str, Any]], path: Path) -> None:
    lines = [f"{'id':<5} {'status':<16} {'reading':<9} {'first failing killer / failure excerpt':<}", "-" * 110]
    for r in results:
        if r["id"] == CONTROL_ID:
            lines.append(f"{'CTRL':<5} {r['status']:<16} {'-':<9} {len(r['killers'])} killers, rc={r['rc']}, {r['seconds']}s")
            continue
        detail = r.get("first_failing", "") or r.get("summary", "")
        lines.append(f"{r['id']:<5} {r['status']:<16} {r.get('reading', ''):<9} {detail}")
        if r.get("failure_excerpt"):
            lines.append(f"{'':<32}E: {r['failure_excerpt']}")
        lines.append(f"{'':<32}{r['description']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    commit = git_head()
    started = time.monotonic()
    ctrl = control(commit)
    print(json.dumps({k: ctrl[k] for k in ("id", "status", "rc", "seconds", "summary")}), flush=True)
    if ctrl["status"] != "pass":
        (HERE / "results.json").write_text(json.dumps({"commit": commit, "control": ctrl}, indent=1) + "\n", encoding="utf-8")
        print("CONTROL FAILED: mutant results would not be trustworthy; stopping", file=sys.stderr)
        return 2
    results: list[dict[str, Any]] = [ctrl]
    for m in MUTANTS:
        if only and m["id"] != only:
            continue
        r = mutant(commit, m)
        results.append(r)
        print(json.dumps({k: r.get(k) for k in ("id", "status", "first_failing", "seconds")}), flush=True)
    counts: dict[str, int] = {}
    for r in results[1:]:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    payload = {"commit": commit, "python": str(PY), "total_seconds": round(time.monotonic() - started, 1),
               "counts": counts, "mutant_count": len(results) - 1, "control": ctrl, "mutants": results[1:]}
    (HERE / "results.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    write_text_report(results, HERE / "results.txt")
    print(json.dumps({"counts": counts, "total_seconds": payload["total_seconds"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
