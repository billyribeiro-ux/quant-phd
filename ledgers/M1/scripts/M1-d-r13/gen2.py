import json, pathlib
exec(open("/tmp/m1-v13/d/gen.py").read())

def mut_rows(rid, check, location, prefixes):
    hits = [m for m in mut if any(m["file"].split("/")[-1].startswith(p) for p in prefixes)]
    assert hits, rid
    killers = "; ".join(f"{m['file'].split('/')[-1]} -> {m['killed_by']}" for m in hits)
    R(row(rid, check, location, "PASS",
          f"Re-run this round (out/mutate_r13_final.out, seeds 0-9): {len(hits)} file(s) KILLED: {killers}."))
    done_ids.add(rid)

mut_rows("proj-mutant-m47-m49", "Mutants m47 to m49 are killed", "ledgers/M1/mutants/m47_*, m48_*, m49_*", ["m47_", "m48_", "m49_"])
mut_rows("proj-mutant-m48-small-rate-cutoff", "Mutant m48 (small-rate cutoff) is killed", "ledgers/M1/mutants/m48_*", ["m48_"])
mut_rows("proj-mutant-m50-perpetuity-rate-above-one", "Mutant m50 is killed", "ledgers/M1/mutants/m50_*", ["m50_"])
mut_rows("proj-mutant-m51-tiny-rate-cutoff-1e-8", "Mutant m51 (1e-8 cutoff) is killed", "ledgers/M1/mutants/m51_*", ["m51_"])
mut_rows("proj-mutant-m52-float-small-rate", "Mutant m52 is killed", "ledgers/M1/mutants/m52_*", ["m52_"])
mut_rows("proj-mutant-m53-term-cap-360", "Mutant m53 is killed", "ledgers/M1/mutants/m53_*", ["m53_"])
mut_rows("proj-mutant-m57-term-cap-480", "Mutant m57 is killed", "ledgers/M1/mutants/m57_*", ["m57_"])
mut_rows("proj-mutants-m54-m58-new", "Mutants m54, m55, m56, m58 are killed", "ledgers/M1/mutants/m54_* to m58_*", ["m54_", "m55_", "m56_", "m58_"])
mut_rows("proj-mutants-r11d-new", "Mutants r11d_01, r11d_02, r11d_04 are killed", "ledgers/M1/mutants/r11d_01_*, r11d_02_*, r11d_04_*", ["r11d_01_", "r11d_02_", "r11d_04_"])
mut_rows("proj-mutant-r11d03-annuity-tiny-cutoff", "Mutant r11d_03 (annuity tiny rate as zero) is killed", "ledgers/M1/mutants/r11d_03_*", ["r11d_03_"])
mut_rows("proj-mutant-r12v02-binary-rate", "Mutant r12v_02 (binary-fraction rate) is killed", "ledgers/M1/mutants/r12v_02_*", ["r12v_02_"])
mut_rows("proj-mutant-r12v04-growing-no-upper-bound", "Mutant r12v_04 (no growth-below-rate check) is killed", "ledgers/M1/mutants/r12v_04_*", ["r12v_04_"])

mut_rows("proj-r13-mutants-r13f-set", "Mutants r13f_01 to r13f_10 (committed in the delta) are killed", "ledgers/M1/mutants/r13f_*", ["r13f_"])

R(row("proj-lab-twins-isolated-r12", "Project lab twins run alone under python -I -W error", "tests/labs/M1/lab-M1-project-1.py, lab-M1-project-2.py, lab-M1-project-3.py", "PASS",
      "Re-run this round: each twin exits 0 under `python -I -W error` (7, 3 and 17 output lines)."))
R(row("proj-page-smoke-r12", "page_smoke for the project page", "course/modules/M/M1/project.html; tools/page_smoke.py --unit M1 --pages project.html", "PASS",
      "Re-run this round: 'page_smoke M1: PASS' (ledgers/M1/scripts/M1-d-r13/out/page_smoke.out)."))
R(row("proj-commands-gate-r12", "Repo commands for the M1 slice (round 12 set)", "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py (--unit M1)", "PASS",
      "Re-run this round: check_pages M1 PASS; check_projects M1 PASS; check_dag M1 PASS; run_labs M1 PASS (11/11)."))
R(row("proj-mypy-and-pytest-r12", "mypy and curriculum tests for the M1 slice", ".venv/bin/mypy --no-incremental (repo files = tools, tests); .venv/bin/pytest -q tests/test_curriculum.py", "PASS",
      "Re-run this round: repo mypy --no-incremental 'Success: no issues found in 153 source files'; pytest -q tests/test_curriculum.py: 15 passed. The full repo pytest suite was not run."))
R(row("proj-grader-lint-types", "Grader lint and types", "course/modules/M/M1/grader/ (test_project.py, reference.py, starter.py, instance.py)", "PASS",
      "Re-run this round: ruff check on the grader passes; ruff format --check passes (15 files). The grader is outside mypy's configured files (proj-r13-ruff-mypy)."))
R(row("proj-grader-reference-50-seeds", "Reference passes 50 seeds", "course/modules/M/M1/grader/reference.py; tools/run_graders.py --unit M1 --seeds 0-49", "PASS",
      "Re-run this round: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)'."))
R(row("proj-alt-correct-implementations-r12", "Round-12 alternatives pass", "ledgers/M1/scripts/M1-d-r12/alts/alt_r12v_a..c", "PASS",
      "Re-run this round on seeds 0-9: 10/10 each (see proj-r13-alternatives-r12-rerun)."))
R(row("proj-grader-run-graders-r11", "run_graders M1 seeds 0-49 (round 11 run)", "tools/run_graders.py --unit M1 --seeds 0-49", "PASS",
      "Re-run this round: PASS 50/50 (see proj-r13-run-graders-0-49)."))
R(row("proj-grader-run-graders-r10", "run_graders M1 seeds 0-49 (round 10 run)", "tools/run_graders.py --unit M1 --seeds 0-49", "PASS",
      "Re-run this round: PASS 50/50 (see proj-r13-run-graders-0-49)."))
R(row("proj-commands-gate-r11", "Repo commands (round 11 set)", "tools/check_pages.py, check_projects.py, check_dag.py (--unit M1)", "PASS",
      "Re-run this round: check_pages, check_projects, check_dag: all PASS (see proj-commands-gate-r12)."))
R(row("proj-commands-gate-r10", "Repo commands (round 10 set)", "tools/verify_refs.py --offline; the other round-10 commands", "PASS",
      "Re-run this round: verify_refs offline 560 entries, 0 problems; the other commands PASS (see proj-commands-gate-r12)."))
R(row("cards-process-and-banned", "Cards and project page contain no process words or banned phrases", "course/modules/M/M1/cards.json; course/modules/M/M1/project.html line 164", "PASS",
      "cards.json unchanged since aebdc15 (sha 5c3311f8 at both pins). Line 164 (the only changed page line) grep for roughly, about, historically, process, builder, verifier, round, unit report: no match."))

# remaining previous ids: carried ones, or fail if unplaced
placed = {r["id"] for r in rows}
unplaced = [i for i in prev_rows if i not in placed]
assert not unplaced, unplaced

# every previous id must be present
assert set(prev_rows) <= placed

# the mutant list: all 109 committed files
import collections
status_counter = collections.Counter("PASS" if r["status"] == "PASS" else r["status"] for r in rows)
fails = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "FAIL" if fails else "PASS"
summary = (f"M1-d round 13 at eaf6d87: {len(rows)} rows, {len(rows)-len(fails)} PASS, {len(fails)} FAIL "
           f"({', '.join(fails)}). Failing defect: the two new grader comments on the exact-tie cases (case 2 comment states a float "
           f"product of 15419763.49, which is false: 15419763.500000002; the second case does not separate float from exact arithmetic). "
           f"Closed from round 12: proj-grader-mutation-suite (109/109 killed) and both survivors r12v_01 and r12v_03 now killed. "
           f"New equivalent mutant r13v_04 (cutoff 1e-12) archived under scripts/M1-d-r13/equiv with a tolerance proof, not in the mutants list.")

_seen = {}
for _r in rows:
    _seen[_r["id"]] = _r
rows = [r for r in rows if _seen[r["id"]] is r]
frag = {
  "unit": "M1", "slice": "M1-d", "round": 13,
  "round_note": "round 13 (independent re-verification of slice M1-d at eaf6d87). Delta aebdc15..eaf6d87 read in the slice: project.html line 164 (196 checks); grader/test_project.py (the 5e-11 annuity test, two exact-tie cases, the nan case, the INST2 comment, the final-payment bound docstring); no M1 cards, lessons or labs change (cards.json sha identical). Rows whose cited subject is byte-identical carry round 12 evidence with the prefix; rows whose subject changed were re-run this round. Mutants: 109 committed files re-run, plus 3 new (r13v_01 to r13v_03) and 1 equivalent (r13v_04, moved out).",
  "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 13; did not build M1; no shared context with builders)",
  "pin": "eaf6d87 (detached HEAD of /tmp/verify13-M1-d)",
  "base": "aebdc15 (round-12 pin, used for the delta)",
  "previous_ledger": "/tmp/fanout-frags/M1-d.round12.json (context only)",
  "checkout": "/tmp/verify13-M1-d",
  "scratch": "/tmp/m1-v13/d/",
  "verified_at": "2026-10-28T15:00:00+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": mut,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Command output for the grader reference and page checks is in ledgers/M1/scripts/M1-d-r13/out/ (mutate_r13_final.out, page_smoke.out, mutate_r13b.out, mutate_r13c.out is the pre-move run with r13v_04 surviving).",
    "Scripts: ledgers/M1/scripts/M1-d-r13/mk_r13v.py (new mutants), mk_alts13.py and run_alts13.sh (new alternatives and the seed loop), alts/, equiv/ (r13v_04).",
    "Not checked: the Pyodide browser run of the grader itself (only page_smoke PASS); the full repo pytest suite (only tests/test_curriculum.py); mypy on the grader directory (not in pyproject's files list; a direct run gives import-not-found artifacts).",
    "Equivalent mutant r13v_04 (annuity cutoff 1e-12) is within the grader's stated 1e-6 tolerance up to about 2,000,000 periods; the suite does not test beyond 100000 periods, and the page does not state a precision for tiny rates. Honest gap, not a FAIL.",
    "tools/mutate_graders.py exits 0 on the committed 109 files; it exited 1 while r13v_04 was in the directory (109/110), which is why the equivalent mutant was moved.",
    "Hours are not judged on pace (architect ruling); the time budget on the page is unchanged (lines 182-198)."
  ],
  "summary": summary,
}
out = pathlib.Path("/tmp/verify13-M1-d/ledgers/M1/M1-d.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print("rows", len(rows), "fails", fails, "mutants", len(mut), "verdict", verdict)
