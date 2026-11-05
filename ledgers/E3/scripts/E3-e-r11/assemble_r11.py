"""Assembles the round-11 E3-e fragment from rows_r11.py output and the kill logs."""
import json, re, sys, subprocess
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD11-E3-e"
S = ROOT + "/ledgers/E3/scripts/E3-e-r11/out/"
rows = json.load(open("/tmp/e3e_r11/rows.json"))
prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-e.round10.json"))
prev_ids = [r["id"] for r in prev["rows"]]
missing = [i for i in prev_ids if i not in {r["id"] for r in rows}]
print("round-10 ids missing:", missing)
mutants = []
for line in open(S + "mutate_E3_seeds0-9.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+)\.py: (.*?) -> (.*)$", line.strip())
    if not m:
        continue
    name, desc, killed = m.group(1), m.group(2), m.group(3)
    if name.startswith("r11_"):
        continue
    mutants.append({"id": name, "description": desc, "file": f"ledgers/E3/mutants/{name}.py", "killed_by": killed + " (seeds 0-9, mutate_graders)"})
kill = dict(l.split(": ", 1) for l in open(S + "kill_r11.txt", encoding="utf-8").read().splitlines() if ": " in l and not l.startswith("DONE"))
for name in ["r11_01_prospect_root_of_a_negative_value_raises_value_error", "r11_02_crra_certainty_equivalent_reported_as_final_wealth", "r11_03_gamma_hat_clamped_below_one_minus_1e3"]:
    doc = open(f"{ROOT}/ledgers/E3/mutants/{name}.py", encoding="utf-8").readline().strip().strip('"')
    res = kill.get(name, "")
    killed_by = res.split("FAILED ", 1)[1].strip() + " (seed 0)" if res.startswith("KILLED") else ""
    mutants.append({"id": name, "description": doc, "file": f"ledgers/E3/mutants/{name}.py", "killed_by": killed_by})
print("mutants:", len(mutants), "killed:", sum(1 for m in mutants if m["killed_by"]))
notes = [
 "Pin ccaeeaf (round-11 checkout detached, .venv symlinked). Delta from round-10 pin 47a36d8c inside slice e: course/modules/E/E3/project.html (107 changed lines; read in full), course/modules/E/E3/grader/test_project.py (two hunks: docstring at :665-668, new test at :870-900; both read), tests/labs/E3/lab-E3-project-3.py (101 changed lines; page code equals the twin), L01-L08 and the E3 hub are NOT slice-e subjects except for prose, notation, attribution and links: their 70 changed lines were read (git diff -U0), and their cited passages were not all re-read (rows E3e-r8-05, -06, E3e-55..60 are UNVERIFIABLE for that reason).",
 "Carried rows: only where the cited file is byte-identical (instance.py, reference.py, notation.json, plans/E3-*, FINAL-ARCHITECT-RULINGS.md, lab-E3-project-1/2 twins, L06.html, index.html, mutants r7_*). Rows citing test_project.py passages carry because the passage content is unchanged (the round-11 hunks are at :665-668 and :870-900).",
 "Blind scoring of the exemplars was NOT achieved: the official scoring sat in the same file read as the memo text. The re-score from the descriptors is recorded in E3e-12 and agrees with the page.",
 "Alternatives: full-suite runs (QF_SEED=0) of the five plan-6.4 fixtures from ledgers/E3/scripts/E3-d-r10/alts/: alt5 48 passed; alt1 (grid, zoom, Newton polish) fails the recovery loop and the seed-49 check (alt diagnosis in ledgers/E3/scripts/E3-e-r11/alt1_diag_r11.py: loglik -126.038268 vs reference -126.031539); alt2 (pure Newton) fails three tests; alt3 (Nelder-Mead) fails the two mixed-lottery fixture tests; alt4 (bisection) fails the exact-half test (prospect gamma 0 returns 2 for CE 2.5). Only seed 0 was run for the full suite, and seed-specific tests for seeds 1-9 were not run for the alternatives (run time). Alt1 seeds 1-2 partial output files were killed mid-run and are not evidence.",
 "Mutants: mutate_graders --unit E3 --seeds 0-9 on the 150 pre-existing mutants: 150 of 150 KILLED. Three new round-11 mutants (r11_01..03) were written; two were killed on seed 0 by real tests; r11_03 (gamma_hat clamped at 0.999) survives seeds 0-9 and is a FAIL. The mutate log also contains entries for r11_* from the first, invalid versions (SyntaxError at collection); those are disregarded and replaced by the kill_r11 results.",
 "Gates run this round: check_pages E3 PASS; check_dag E3 PASS; check_projects E3 PASS; run_labs E3 PASS (3/3); page_smoke project PASS (in-browser 48 pass); run_graders E3 0-49 PASS (reference 50/50); verify_refs --offline 560 entries 0 problems; ruff check and format on tests/labs/E3 and grader PASS; mypy --no-incremental (repo) PASS 385 files; collect-only 48 tests; twins under python -I -W error exit 0.",
 "Lab 3 (rung 3) estimate-keys defect: main() reads result['largest_score']; the spec and the new suite test require exactly seven keys. The round-10 record of this row (E3e5-03) was re-verified: the twin does not call an engine.",
 "Plan-6.6 deviation found in this round: C1 level-4 descriptor on the page differs from the binding plan wording (E3e-r11-rubric-C1-level4).",
 "Round-10 FAIL rows status: E3e4-exemplar-B-level still FAIL (re-verified, data-level 3 vs plan 4). E3e5-03 still FAIL (re-verified). E3e-13 now PASS (word counts 117 and 450 re-derived; the page no longer says 603).",
 "Not checked: lesson prose and lesson numbers in L01-L08 hunks (lesson slices own them); cards (no cards in slice e); lab-E3-L0x twins; the full text of L02-L08 page_smoke (not re-run); the 5-alternative seed window 0-9 for the seed-specific tests; blind exemplar scoring; the grader's numeric docstrings at :1064-1073 (carried, not re-derived); the reference's whole-suite runtime under contention (a 50-seed run took about 24 minutes under load).",
]
freshness = ["plans/FINAL-ARCHITECT-RULINGS.md item 7 quotes exemplar word counts 103 and 375; the page now has 117 and 450 (verified by exemplar_words_r11.py). The ruling text is stale; the page is correct."]
fails = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m["killed_by"] for m in mutants) else "FAIL"
frag = {
 "unit": "E3", "slice": "e", "round": 11,
 "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 11 (did not build E3; read verifier-rules.md, the round-10 fragment as context, and the project page, grader, labs, plans and registry records)",
 "pin": "ccaeeaf4", "base": "47a36d8c (round-10 pin; round-10 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round10.json)",
 "checkout": ROOT, "scratch": "/tmp/e3e_r11/",
 "verified_at": "2026-11-05T09:30:00+00:00",
 "verdict": verdict,
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": freshness,
 "notes": notes,
 "summary": f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']=='FAIL')} FAIL, {sum(1 for r in rows if r['status']=='UNVERIFIABLE')} UNVERIFIABLE. Non-PASS: {', '.join(fails)}. Mutants: {len(mutants)} listed, {sum(1 for m in mutants if m['killed_by'])} killed (r11_03 survives). Alternatives: alt5 PASS on seed 0 full suite; alt1, alt2, alt3, alt4 FAIL (see E3e-32).",
}
json.dump(frag, open(ROOT + "/ledgers/E3/E3-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written; verdict", verdict, "rows", len(rows), "non-pass", fails)
