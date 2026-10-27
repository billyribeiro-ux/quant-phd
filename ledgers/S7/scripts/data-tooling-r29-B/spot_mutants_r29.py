"""Round 29 spot re-creation of five add_reference mutants (descriptions from the release ledger, part A mutants list).
Each mutant is one exact text replacement in a scratch copy of the c9beb92 tree (git archive); the unmutated copy is run first.
Usage: python -I spot_mutants_r29.py <checkout> <scratch dir> ; prints a JSON result list (also written to results_r29.json)."""
import json, shutil, subprocess, sys, tarfile, io
from pathlib import Path

checkout, scratch = Path(sys.argv[1]), Path(sys.argv[2])
py = checkout / ".venv/bin/python"
MUTANTS = [
    {"id": "control", "description": "unmutated tree", "file": None, "old": None, "new": None,
     "killer": "tests/test_refs.py (whole file)"},
    {"id": "R05", "description": "registered(): URL branch removed (always no match)",
     "file": "tools/add_reference.py", "old": 'return bool(work.url and e.get("url") == work.url)', "new": "return False",
     "killer": "tests/test_refs.py::test_registered_finds_the_entry_that_holds_the_work[url]"},
    {"id": "R16", "description": "registered(): only the work's first ISBN is compared",
     "file": "tools/add_reference.py", "old": "set(e.get(\"isbn\") or []) & set(work.isbn)", "new": "set(e.get(\"isbn\") or []) & set(work.isbn[:1])",
     "killer": "tests/test_refs.py::test_registered_finds_the_entry_that_holds_the_work[isbn-second]"},
    {"id": "A07", "description": "admit(): run path keeps the held used_by and drops the units the run names",
     "file": "tools/add_reference.py", "old": 'existing["used_by"] = sorted(set(existing["used_by"]) | set(used_by))',
     "new": 'existing["used_by"] = sorted(set(existing["used_by"]))',
     "killer": "tests/test_refs.py::test_a_dry_run_reports_what_the_run_would_do[run-unit-added]"},
    {"id": "C01", "description": "describe(): every container title joined, not only the first",
     "file": "tools/add_reference.py", "old": "', '.join(work.container[:1])", "new": "', '.join(work.container)",
     "killer": "tests/test_refs.py::test_describe_names_the_first_container_title_only"},
    {"id": "C03", "description": "describe(): container[0] in place of the join (IndexError when there is no container)",
     "file": "tools/add_reference.py", "old": "', '.join(work.container[:1])", "new": "work.container[0]",
     "killer": "tests/test_refs.py::test_describe_handles_a_work_without_a_container"},
]
results = []
for m in MUTANTS:
    tree = scratch / m["id"]
    if tree.exists():
        shutil.rmtree(tree)  # scratch copy only
    tree.mkdir(parents=True)
    archive = subprocess.run(["git", "archive", "c9beb92"], cwd=checkout, capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(archive)).extractall(tree)
    if m["file"]:
        p = tree / m["file"]
        text = p.read_text(encoding="utf-8")
        n = text.count(m["old"])
        if n != 1:
            results.append({**m, "error": f"anchor count {n}"}); continue
        p.write_text(text.replace(m["old"], m["new"]), encoding="utf-8")
    run = subprocess.run([str(py), "-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "addopts=", "tests/test_refs.py"],
                         cwd=tree, capture_output=True, text=True)
    tail = run.stdout.strip().splitlines()[-1] if run.stdout.strip() else run.stderr[-300:]
    failed = [l.split("::", 1)[1].split(" ")[0] for l in run.stdout.splitlines() if l.startswith("FAILED")]
    results.append({"id": m["id"], "description": m["description"], "rc": run.returncode, "summary": tail,
                    "failed_tests": failed[:5], "named_killer": m["killer"]})
    print(json.dumps(results[-1], ensure_ascii=False))
Path(checkout / "ledgers/S7/mutants/tooling-r29-B/results_r29.json").write_text(json.dumps(results, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
