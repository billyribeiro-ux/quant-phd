import json, sys
BASE = "/Users/billyribeiro/.fanout/frags/H-M6-b.round1.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyI1-M6-b/ledgers/M6/M6-b.json"
base = json.load(open(BASE, encoding="utf-8"))
PIN_PREV = "d9de2fe5eea982d14cd9f922a61676b847506fbc"
HEAD = "85b109f8ae3045085b52626f323f3c934e7718de"
SCR = "ledgers/M6/scripts/M6-b-r1/"
PFX = "Carried from base round 1 (fragment H-M6-b.round1, pin d9de2fe5; subject byte-identical in d9de2fe5..85b109f8, see " + SCR + "v_cards_cmp.txt and git diff --stat d9de2fe5..HEAD -- course/modules/M/M6 tests/labs/M6): "

# rows re-verified this round (subject changed in d9de2fe5..85b109f8, or non-PASS in base)
new = {
 "M6b-r1-cards-c047": (
  "PASS",
  "Re-verified from scratch at 85b109f8. Changed card (back, cards.json line 290; only hunk in the delta, git diff d9de2fe5..HEAD -- course/modules/M/M6). "
  "New back: 'for each fixed x > 0, y maps to f(x,y) continuously on [0, 1], and for each fixed y > 0, x maps to f(x,y) continuously on [0, 1] (item 2 of Proposition 3.1)'. "
  "This matches L05.html line 118 (Prop 3.1 item 2: 'For each fixed x > 0 ... continuous on [0,1] ... For each fixed y > 0 ... by the same reasoning'). "
  "The restriction to x > 0 and y > 0 is now stated, so the false claim about the x = 0 and y = 0 slices is gone. "
  "Values: 'for x > 0 the integral over y is 1/(1 + x^2); for y > 0 the integral over x is -1/(1 + y^2); y-integral first gives pi/4, x-integral first gives -pi/4' match Statement and Proof (L05.html lines 118-127). "
  "Numeric check with python -I (" + SCR + "v_c047_check.txt, Simpson rule n=20000): int_0^1 f dy at x=0.3, 0.5, 0.9 = 0.917431193, 0.8, 0.552486188 = 1/(1+x^2); int_0^1 f dx at y=0.3, 0.7 = -0.917431193, -0.67114094 = -1/(1+y^2); pi/4 = 0.7853981634. "
  "Grade T matches L05.html line 396 (key-results row, T). The card's assumptions list items 2-4, which are the hypotheses the Statement uses."),
 "M6b-r3-cards-L05-L08": (
  "PASS",
  "Per-id compare d9de2fe5 vs 85b109f8 (" + SCR + "v_cards_cmp.txt): 145 cards at both pins, added [], removed [], changed ['M6-c047'] only; 47 cards with lesson L05-L08 at HEAD. "
  "M6-c047 re-verified from scratch (row M6b-r1-cards-c047, PASS). The other in-slice cards are byte-identical since d9de2fe5 and carry their base evidence: c048, c068, c073, c076, c150, c151 (base PASS rows, cited there), c053, c058, c062, c080, c081, c134, c140 (base PASS rows)."),
 "M6b-r1-cards-duplicates": (
  "PASS",
  "Re-run at 85b109f8: python -I " + SCR + "v_cards_cmp.py output (" + SCR + "v_cards_cmp.txt): no 'DUP ID' line, 'dup fronts 0', counts 145 and 145."),
 "M6b-r3-check-pages": (
  "PASS",
  "Re-run at 85b109f8 because cards.json changed: .venv/bin/python tools/check_pages.py --unit M6 -> 'check_pages M6: PASS', exit 0 (" + SCR + "v_check_pages_M6.txt)."),
 "M6b-r3-check-dag": (
  "PASS",
  "Re-run at 85b109f8: .venv/bin/python tools/check_dag.py --unit M6 -> 'check_dag M6: PASS', exit 0 (" + SCR + "v_check_dag_M6.txt). Gate also run: tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (" + SCR + "v_build_site_check.txt)."),
 "M6b-r3-pytest-lab-suites": (
  "PASS",
  "Re-run at 85b109f8 (cards.json changed): .venv/bin/python -m pytest -o addopts='' -k 'page or lab or card or dag or concept or figure or docs' tests --ignore=tests/test_page_smoke.py -q -> '467 passed, 251 deselected', exit 0 (" + SCR + "v_pytest_subset.txt). tests/test_lx1_project_lab3.py not run (outside slice b)."),
 "M6b-r8-verify-refs-and-pytest": (
  "PASS",
  "Re-run at 85b109f8: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + SCR + "v_verify_refs_offline.txt). pytest subset: row M6b-r3-pytest-lab-suites (467 passed, exit 0)."),
}

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in new:
        status, ev = new[rid]
        nr = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    else:
        nr = {k: v for k, v in r.items() if k != "fix"}
        nr["evidence"] = PFX + r["evidence"]
    rows.append(nr)

# every row id from the base is kept
assert [r["id"] for r in rows] == [r["id"] for r in base["rows"]]
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
n_pass = sum(r["status"] == "PASS" for r in rows)

frag = {
 "unit": "M6",
 "slice": "b",
 "round": 1,
 "verifier": "Haiku independent verifier (closing delta, rulings 30/37; did not build M6)",
 "pin": HEAD,
 "base": "H-M6-b.round1 (~/.fanout/frags/H-M6-b.round1.json, verdict FAIL, pin d9de2fe5eea982d14cd9f922a61676b847506fbc). Closing delta d9de2fe5..85b109f8 over the slice paths: course/modules/M/M6/cards.json only (M6-c047 back). No M6 HTML, twin, notation, curriculum, references or tools hunk in the delta.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyI1-M6-b (detached at 85b109f8, .venv symlinked)",
 "scratch": SCR + " (v_* files; base close_* files unchanged)",
 "verified_at": "2026-11-09",
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Lesson slice, no grader in slice b: mutants [] is intentional (ruling 37: closing round writes no new mutants; the M6 lesson slice has no standing mutant set; tools/mutate_graders.py is for project graders, which are outside slice b).",
  "Ruling 30 delta: the only in-slice hunk between d9de2fe5 and 85b109f8 is cards.json M6-c047 (per-id compare, " + SCR + "v_cards_cmp.txt). Base rows whose subject did not change are carried with the carry prefix; keys kept.",
  "Ruling 26 kinds: the one base FAIL (M6b-r1-cards-c047, missing hypothesis: 'each one-variable slice is continuous on [0, 1]') is fixed at 85b109f8 and re-verified PASS; the aggregate row M6b-r3-cards-L05-L08 that failed on it is PASS.",
  "Base evidence in carried rows still names the base round G-M6-b.round1 (pin 2a805c83) where it cites an earlier carry; those chains are unchanged, since no M6 HTML, twin or notation file changed in d9de2fe5..85b109f8.",
  "Out of slice (not verified here; owners): cards.json M6-c005, c032, c098, c120 and added c152, c153, c154 were in the 2a805c83..d9de2fe5 delta and are not in this delta.",
  "Overwrite notice: ledgers/M6/M6-b.json at the checkout's pin is replaced by this round-1 closing fragment as the task instructs; the prior file is recoverable from git.",
  "Not run: mypy --no-incremental on the twins (carried; tests/labs/M6 has no hunk); run_labs, page_smoke, ruff and the twin isolated runs (carried; no M6 HTML, twin or ruff-relevant file changed in the delta); mutate_graders, run_graders, check_projects, render_curriculum (no grader, project or curriculum hunk in slice b)."
 ],
 "summary": "M6 slice b closing delta d9de2fe5..85b109f8: verdict " + verdict + ". " + str(n_pass) + " of " + str(len(rows)) + " rows PASS. The base FAIL rows M6b-r1-cards-c047 and M6b-r3-cards-L05-L08 are PASS after the card fix (cards.json M6-c047 back now states the x>0 and y>0 continuity restriction of Prop 3.1 item 2). Re-run gates: check_pages M6, check_dag M6, build_site --check, verify_refs --offline (560 entries, 0 problems), pytest subset (467 passed), cards per-id compare (145 cards, no duplicates). Carried rows are the base PASS rows whose subject is unchanged."
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", len(rows), "pass", n_pass, "verdict", verdict)
