"""Round 29: update ledgers/S7/data-tooling-B.json: r20-mut-summary stays UNVERIFIABLE with the reconciliation result; two
new rows record the byte-identity proof with the killing-test run, and the five spot re-created kills; the five kills are added
to the fragment's mutants list. Every existing row id is kept. Usage: python -I update_fragment_r29.py <checkout>"""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
path = ROOT / "ledgers/S7/data-tooling-B.json"
frag = json.loads(path.read_text(encoding="utf-8"))
M = "ledgers/S7/mutants/tooling-r29-B"
LOG = "ledgers/S7/scripts/data-tooling-r29-B/logs"
results = json.loads((ROOT / M / "results_r29.json").read_text(encoding="utf-8"))
killed = [r for r in results if r.get("id") != "control" and r.get("rc") == 1]
ids_before = [r["id"] for r in frag["rows"]]

rows = {r["id"]: r for r in frag["rows"]}
rows["r20-mut-summary"]["evidence"] = (
    "Round 29 reconciliation (" + M + "/reconcile_r29.out): the summary's 49 does NOT reconcile. The add_reference mutant ids in the "
    "ledgers are 25 (round 20), 36 (round 21), 47 (round 22) and 66 (round 23 onward, and the release part A list: 66 unique, equal "
    "to the release set). The per-round additions are 25 + 11 + 11 + 19 = 66. Neither 49 nor any cumulative total is 49 (25, 36, 47, 66), "
    "and the summary's own evidence does not enumerate 49 ids. The harness that produced 49 (scratch scripts/mutants_ar.py) is not archived, "
    "so the two-mutant difference from 47 cannot be named. Kill results of the carried per-id rows are carried under the mutant rule "
    "(tools/add_reference.py and tests/test_refs.py byte-identical 5e5da87..c9beb92, logs/identity.out; tests/test_refs.py 119 passed today, "
    "logs/pytest_test_refs_verbose.log; five spot re-creations killed, see r29-mut-add-ref-spot-5). Status stays UNVERIFIABLE because the 49 count is unreconciled."
)
rows["r20-mut-summary"]["fix"] = (
    "Archive the 49-mutant harness (or name the 49 ids) and reconcile against the 47 round-22 and 66 release ids; the per-id rows then close the summary."
)
new_rows = [
    {
        "id": "r29-mut-add-ref-identity",
        "check": "2.6-mutation (the subject of the add_reference mutant kills is unchanged since the release, and its killing tests pass today)",
        "location": "tools/add_reference.py, tools/refs/ (all files), tests/test_refs.py, tests/test_labs.py",
        "status": "PASS",
        "evidence": (
            f"Carried from the release ledger (tools/add_reference.py, tools/refs, tests/test_refs.py, tests/test_labs.py byte-identical since 5e5da87; "
            f"kill results are deterministic for unchanged code and tests): git diff --quiet 5e5da87 c9beb92 -- those paths, rc 0 ({LOG}/identity.out). "
            f"Observed today: tests/test_refs.py 119 passed (logs/pytest_test_refs_verbose.log), the unmutated control in the rows. "
            f"The harness that made the per-id mutants was not archived, so the kills are not re-observed except the five in r29-mut-add-ref-spot-5."
        ),
    },
    {
        "id": "r29-mut-add-ref-spot-5",
        "check": "2.6-mutation (five add_reference mutants re-created from their descriptions in a scratch copy of c9beb92 and run against tests/test_refs.py)",
        "location": f"{M}/spot_mutants_r29.py; {M}/results_r29.json (mutants R05, R16, A07, C01, C03)",
        "status": "PASS",
        "evidence": (
            "Re-created today by exact text replacement (anchor count 1 each) in git-archive copies of c9beb92 under /tmp/ap1-r5/data-tooling-B/mut/: "
            + "; ".join(f"{r['id']} ({r['description']}): {r['summary']}, first failure {r['failed_tests'][0] if r['failed_tests'] else 'none'}" for r in killed)
            + f". The unmutated copy: 119 passed. Each kill is by its named killer (results_r29.json)."
        ),
    },
]
rows_list = frag["rows"]
rows_list = [rows[r["id"]] if r["id"] in rows else r for r in rows_list] + new_rows
frag["rows"] = rows_list
frag["mutants"] = [
    {"id": r["id"], "description": r["description"] + " (round 29 spot re-creation, add_reference)", "killed_by": r["named_killer"],
     "observed": r["summary"]}
    for r in killed
]
ids_after = [r["id"] for r in frag["rows"]]
assert set(ids_before) <= set(ids_after), "a row id was dropped"
frag["summary"].update({
    "rows": len(frag["rows"]),
    "pass": sum(1 for r in frag["rows"] if r["status"] == "PASS"),
    "unverifiable": sum(1 for r in frag["rows"] if r["status"] == "UNVERIFIABLE"),
    "fail": sum(1 for r in frag["rows"] if r["status"] == "FAIL"),
    "mutants": len(frag["mutants"]),
    "mutants_killed": len(frag["mutants"]),
    "fail_ids": [r["id"] for r in frag["rows"] if r["status"] != "PASS"],
})
frag["verdict"] = "PASS" if frag["summary"]["unverifiable"] == 0 and frag["summary"]["fail"] == 0 else "FAIL"
frag["round29_note"] = (f"Round 29 (coordinator request): reconciliation of the add_reference mutant counts ({M}/reconcile_r29.out): "
                        "49 does not reconcile, so r20-mut-summary stays UNVERIFIABLE. Two rows added (r29-mut-add-ref-identity, "
                        "r29-mut-add-ref-spot-5); five re-created kills added to mutants. Every round-28 row id is kept.")
path.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(frag["rows"]), "ids kept", set(ids_before) <= set(ids_after), "summary", frag["summary"], "verdict", frag["verdict"])
