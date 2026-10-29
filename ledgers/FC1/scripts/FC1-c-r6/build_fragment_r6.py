import json, re, pathlib
C = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC6-FC1-c")
S = C / "ledgers/FC1/scripts/FC1-c-r6"
mut_lines = [l for l in (S / "mutate_graders_FC1_r6.out").read_text().splitlines() if re.match(r"^(KILLED|SURVIVED) ", l)]
mutants = []
for l in mut_lines:
    status, rest = l.split(" ", 1)
    name, rest = rest.split(": ", 1)
    desc, killed = rest.rsplit(" -> ", 1)
    mutants.append({"id": name.replace(".py", ""), "description": desc,
                    "killed_by": (killed if status == "KILLED" else "SURVIVED: no test failed on seeds 0-9; re-run on seeds 0-49 also 0 failing (silence_mutants_50seeds.out)")})
rows = json.loads((S / "rows_r6.json").read_text())
FIX = {
 "proj-fixture-claims": "Rewrite project.html line 275 so it names only fixture G's events and the rounding case's events as unchecked lists (B and F are checked at test_project.py lines 173 and 220).",
 "proj-new-mutants-r6": "Fix proj-silence-coverage; then c6n01 and c6n02 must fail the suite on some seed in 0-9.",
 "proj-silence-coverage": "Run the capsys silence check over valid boundary inputs (yield -9999, coupon 0, side -1, periods 12) as well as the INST case in test_project.py.",
 "cards-misconception-refs": "Rewrite cards.json c017 back to match L01 misconception 3: 'No. Equity is the residual, assets minus liabilities (Definition 1.1). Listing it as an asset as well would count it twice (misconception 3).'",
 "cards-notation-Q": "Replace the registered letter Q for customer buy volume in cards c039 and c042 with an unregistered symbol, and make the same change in L03 Remark 2.2 and Corollary 2.4 (lesson slice).",
 "proj-reference-deployment": "Exclude grader/reference.py from the publish step (tools/build_site.py) or move the reference solutions out of course/.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIX[r["id"]]
frag = {
 "unit": "FC1", "slice": "FC1-c", "round": 6,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1 slice c (project.html, grader, project labs, cards.json), round 6; did not build FC1",
 "pin": "9fd6aed",
 "base": "round 5 fragment /Users/billyribeiro/.fanout/frags/C-FC1-c.round5.json (pin 04626e9), context only. Delta 04626e9..9fd6aed in this slice: project.html (lines 54, 176, 184, 275), grader/test_project.py (NotImplementedError wrapper, must_accept re-raise, docstrings at 241 and 305-306, 388-389), cards.json (c030 only). L01-L05.html, index.html and tests/labs/FC1/lab-FC1-L03-1.py changed outside the slice and were read where a card cites them. grader/instance.py, reference.py, starter.py and the project labs are byte-identical to the round-5 pin. Every hunk of the slice delta was read.",
 "checkout": str(C), "scratch": "/tmp/fc1c6",
 "verified_at": "2026-10-29T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Starter run (QF_SEED=0, unmodified starter): 57 failed, 2 passed, 0 Traceback lines. The 2 passing tests (test_non_whole_face_is_refused_or_gives_ints, test_bool_periods_is_not_quietly_accepted_as_a_number) accept any exception by design (page Constraints line 163), so an empty module passes them; not a finding.",
  "Silence rule: test_the_module_prints_nothing runs only on INST (positive yield, coupon 100-900 bps, random side). Valid negative yields (-9999..-1, page line 166 refuses only <= -10000), zero coupon (page line 165 refuses only negative) and the sell side are never run under capsys.",
  "Not a finding: a student who refuses periods above 100 or coupon_bps above 10000 with ValueError survives; the page names no such limit and says other invalid inputs may raise or return, so no page sentence is violated. Recorded only.",
  "Lab twins alone under python -I -W error: exit 0 for project-1, project-2, project-3 and L01-L05 (twins_project.out, twins_lessons.out). run_labs FC1 8/8.",
  "Browser (Pyodide) suite was not driven by hand; page_smoke FC1 (Chromium) PASS covers page load only.",
  "Repo mypy --no-incremental: 229 source files, no issues. ruff check and ruff format --check on tests/labs/FC1 and the grader: pass.",
  "Round 5 non-PASS rows re-verified from scratch: proj-fixture-claims (still FAIL), proj-failure-messages (now PASS), proj-test-docstring (now PASS), cards-notation-Q (still FAIL), proj-reference-deployment (still FAIL).",
  "Cross-slice items seen while reading cards: L03 Remark 2.2 and Corollary 2.4 use Q as the customer volume (plan 9.2 forbids Q on an FC1 page). That is lesson-slice work; the cards row cards-notation-Q covers the cards only."
 ],
 "summary": "FC1-c round 6: verdict FAIL. 40 rows: 34 PASS, 6 non-PASS (proj-fixture-claims, proj-silence-coverage, proj-new-mutants-r6, cards-misconception-refs, cards-notation-Q, proj-reference-deployment). Mutants: 51 (41 from earlier rounds, c5n01-c5n05, c6n01-c6n05); 49 killed, c6n01 and c6n02 survive all 50 seeds. Five alternatives pass seeds 0-49. Reference passes 50/50 seeds and 59 tests. Lint, mypy, check_pages, check_dag, check_projects, page_smoke, run_labs, verify_refs --offline all PASS."
}
(C / "ledgers/FC1/FC1-c.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("wrote", len(rows), "rows", len(mutants), "mutants")
