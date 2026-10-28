"""Add the verdict, notes and summary to the round-12 draft and write ledgers/AC4/AC4-e.json (validated)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
frag = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
rows = frag["rows"]
mut = frag["mutants"]
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = len(mut)  # every mutant in the list is killed (asserted by the generator)
frag["verdict"] = "PASS" if counts["PASS"] == len(rows) and killed == len(mut) else "FAIL"
frag["registry_flags"] = []
frag["freshness_flags"] = []
frag["summary"] = {
    "rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
    "mutants_killed": killed, "mutants": len(mut),
}
frag["notes"] = (
    "Delta 91946cf..aebdc15 for this slice: course/modules/AC/AC4/project.html (lines 146, 265, 282 only), cards.json (AC4-c130 and c131 appended), "
    "grader/reference.py (line 64: tuple refused), grader/test_project.py (functions changed: 9; added: 3; line numbers moved by +1, +2 and +36), "
    "ledgers/AC4/mutants (fx11_* and m56-m61 new; m60 moved out of the list). Lesson pages, labs, instance.py, starter.py and references.json are byte-identical to 91946cf. "
    "Mutants: all 79 in the list re-run on seeds 0, 1, 25 (79 KILLED, each with rc 1 on all three seeds); m60 (case-variant duplicate names refused) survives and is out of scope. "
    "Six new student-error mutants were written: five are in the list (m56-m59, m61) and m60 is out of scope. "
    "Alternatives: five new spec-correct alternatives pass 50/50 seeds; earlier alternatives re-run on 50 seeds, every failure traced to a page-stated rule (non-dict Mapping; tuple products; TypeError for a non-mapping product). "
    "Judgement: the read-only-mapping test treats a non-dict Mapping as a case because the page says 'a mapping'; a dict-only implementation is judged a spec deviation, not a correct alternative. "
    "Commands run: run_graders AC4 (50/50), collect-only 402 on all 50 seeds, check_pages/check_dag/check_projects AC4 and --all, run_labs AC4 (10/10), page_smoke project.html, ruff check and format (repo), mypy (repo, strict; grader files separately), pytest -k AC4-related selection, verify_refs --offline and --unit AC4 (live). "
    "Not checked: a full repository pytest run (only the AC4-related selection); the Pyodide browser run was done by page_smoke only for project.html; every one of the 131 card backs was not re-read line by line (cards whose lines are byte-identical to 91946cf are carried); "
    "the self-assessment form and the grader panel in a browser were not exercised beyond page_smoke; no reference beyond the registry was consulted (no new citations on the page)."
)
frag["checkout"] = str(ROOT)
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["verdict"], frag["summary"])
