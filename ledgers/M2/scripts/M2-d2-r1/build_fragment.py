"""Build ledgers/M2/M2-d2.json (round 1, closing delta) from the round-10 base fragment.
Fresh rows carry this round's evidence; every other row carries the round-10 evidence under the carry prefix."""
import json, sys

root = sys.argv[1]
base = json.load(open("/Users/billyribeiro/.fanout/frags/D-M2-d2.round10.json", encoding="utf-8"))
S = "ledgers/M2/scripts/M2-d2-r1/out"
PAGES = "course/modules/M/M2/L22.html, L23.html, L24.html and tests/labs/M2/lab-M2-L22-1.py, lab-M2-L23-1.py, lab-M2-L24-1.py"
CARRY = "Carried from round 10 (" + PAGES + " byte-identical since the previous pin 47a36d8c):"

fresh = {
 "G-check-pages": f"Fresh r1: check_pages.py --unit M2 --page L22/L23/L24 printed 'check_pages M2 L22: PASS', 'M2 L23: PASS', 'M2 L24: PASS' (exit 0 each); --unit M2 'check_pages M2: PASS'; --all exit 0 with 'check_pages M2: PASS' ({S}/check_pages_*.txt).",
 "G-check-dag": f"Fresh r1: check_dag.py --unit M2 -> 'check_dag M2: PASS' (exit 0); --all exit 0 with 'check_dag M2: PASS' ({S}/check_dag_M2.txt, check_dag_all.txt).",
 "G-run-labs": f"Fresh r1: run_labs.py --unit M2 --page L22, L23, L24 -> 'run_labs M2: PASS (1/1)' each, exit 0 ({S}/run_labs_L2*.txt).",
 "G-twin-isolated": f"Fresh r1: each twin run alone as 'python -I -W error tests/labs/M2/lab-M2-L2x-1.py' from an empty scratch directory: exit 0, stderr 0 bytes, stdout 9, 11 and 25 lines ({S}/twin_L2x_stdout.txt, twin_L2x_stderr.txt).",
 "G-page-code-equals-twin": f"Fresh r1: run_labs.py --unit M2 --page L22/L23/L24 PASS (its checks include the page lab code equal to the twin, trailing newlines aside; docstring of run_labs.py). Pages and twins byte-identical to 47a36d8c (git rev-parse blob hashes equal, {S}/slice_pages_delta.txt is empty of them).",
 "G-expected-equals-live": f"Fresh r1: run_labs.py --unit M2 --page L22/L23/L24 PASS, which compares each page's expected block with the twin's stdout under the page rule (labs.js); the three runs are in {S}/run_labs_L2*.txt; the twin stdout is in {S}/twin_L2x_stdout.txt.",
 "G-page-smoke-L22": f"Fresh r1: page_smoke.py --unit M2 --pages L22 -> 'page_smoke modules/M/M2/L22.html: PASS', 'page_smoke M2: PASS', exit 0 ({S}/page_smoke_L22.txt).",
 "G-page-smoke-L23": f"Fresh r1: page_smoke.py --unit M2 --pages L23 -> 'page_smoke modules/M/M2/L23.html: PASS', 'page_smoke M2: PASS', exit 0 ({S}/page_smoke_L23.txt).",
 "G-page-smoke-L24": f"Fresh r1: page_smoke.py --unit M2 --pages L24 -> 'page_smoke modules/M/M2/L24.html: PASS', 'page_smoke M2: PASS', exit 0 ({S}/page_smoke_L24.txt).",
 "G-ruff-mypy-twins": f"Fresh r1: ruff check . -> 'All checks passed!'; ruff format --check . -> '555 files already formatted'; mypy --no-incremental -> 'Success: no issues found in 386 source files' (all exit 0; {S}/ruff_check.txt, ruff_format.txt, mypy.txt). The three twins are inside the ruff and mypy scope.",
 "G-pytest-labs-M2": f"Fresh r1: pytest tests/test_labs.py -k M2 -> 27 passed, exit 0 ({S}/pytest_labs_M2.txt).",
 "G-verify-refs-offline": f"Fresh r1: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/verify_refs_offline.txt).",
 "G-verify-refs-live-M2": f"Fresh r1: verify_refs.py --unit M2 (live) -> 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0 ({S}/verify_refs_live_M2.txt). references/references.json changed in the delta only at three entries (bisndbasel, black1973pricing, reinhart2009this; used_by fields); spivak2008calculus and hubbard2015vector records are identical at 47a36d8c and HEAD.",
 "G-cards-dup-scan": f"Fresh r1: card_delta.py over HEAD course/modules/M/M2/cards.json (398 cards): no duplicate ids, duplicate fronts or duplicate backs (case-insensitive) ({S}/card_delta.txt).",
 "G-cards-slice-unchanged": f"Fresh r1: the slice cards that changed between 47a36d8c and HEAD are exactly M2-c330, M2-c334 and M2-c404 (L22, changed), M2-c405 (L24, removed), M2-c420 and M2-c430 (L24, added). L23: 24 of 24 card blocks byte-identical; L22: 12 of 15 byte-identical; L24: 17 of 18 byte-identical (line-based block comparison in card_delta.py, {S}/card_delta.txt). Each changed or added card is re-checked against the current lesson text in CARD-L22 and CARD-L24.",
 "G-delta-hunks": f"Fresh r1: git diff 47a36d8c..HEAD over the slice paths (L22.html, L23.html, L24.html, the three twins): no hunks, blob hashes identical. Over cards.json the only slice hunks are the six cards listed in G-cards-slice-unchanged (cards.json lines 2265 M2-c330, 2286 M2-c334, 2657 M2-c404, 2711 M2-c420, 2775 M2-c430, and the removed M2-c405 block). Each hunk read in full ({S}/card_delta.txt).",
 "CARD-L22": f"Fresh r1: the three changed L22 cards re-checked against L22.html. M2-c330 (cards.json:2265): V(a)=a^2/4, V'(a)=a/2, x_hat=y*=a/2 is L22.html:251 (Example 2.2); 'naive partial ... Misconception 1' is L22.html:270-271. M2-c334 (cards.json:2286): uniqueness not assumed follows from (H2) at L22.html:74 (x_hat(a) in J, a maximizer, no uniqueness hypothesis); J open and the closed-domain Example 2.3 not covered are L22.html:255-256 and :261; (Misconception 2) is L22.html:274-275. M2-c404 (cards.json:2657): 'Assumption 1.1 of Lesson 22' is L22.html:94 (d/da ln a = 1/a for a>0, assumed, not proved); Example 1.5 uses it, L22.html:93 ('Assuming Assumption 1.1 below'). All three are supported by the current text. Note: the closed-domain sentence sits in the takeaway list (L22.html:261), while '(Misconception 2)' points at L22.html:274-275; the claim is supported, only the locator is loose (not a FAIL kind; recorded as an observation).",
 "CARD-L24": f"Fresh r1: M2-c405 (old 'What does Assumption 4.1 state?') is removed and M2-c420 is added with the same Assumption; the remaining single statement is L24.html:132 (Assumption 4.1, d/dx e^x = e^x, assumed and not proved; the predicted derivative e at x0=1 is stated under it, L24.html:136), so the card (cards.json:2711) agrees with the page and no duplicate remains. M2-c430 (cards.json:2775): forward/central quotients and 'the derivative is the limit over both signs of h, when that limit exists' are L24.html:55 (Section 1). 'Section 1' and 'Assumption 4.1' appear in L24. The other 17 L24 cards are byte-identical (card_delta.txt).",
 "CARD-DUP": f"Fresh r1: same scan as G-cards-dup-scan on HEAD cards.json (398 cards): no duplicate ids, fronts or backs ({S}/card_delta.txt).",
 "H-hours": f"Fresh r1: the M2 hub index.html changed in the delta at lines 68-74, 124-138 and 161-167 only (placement quiz, L21-L24 card text); lines 29 and 142 are unchanged. index.html:29 data-hours-lessons=\"240\" data-hours-project=\"60\"; index.html:142 'Twenty-four lessons of ten study hours each, which is 240 hours in total'; L22/L23/L24 line 2 data-hours=\"10\" each; cards at index.html:165-167 show 'L22/L23/L24 · 10 h'. 24 x 10 = 240 and 240 + 60 = 300 match the hub's 300 hours (index.html:31).",
 "DAG-prerequisites": f"Fresh r1: check_dag.py --unit M2 -> 'check_dag M2: PASS' ({S}/check_dag_M2.txt). It recomputes the prerequisite closure from the current curriculum; the L22-L24 pages (L22.html:37, L23.html:37, L24.html:37) are byte-identical to 47a36d8c.",
 "DAG-no-later-definitions": f"Fresh r1: check_dag.py --unit M2 -> 'check_dag M2: PASS' ({S}/check_dag_M2.txt); the slice pages are byte-identical to 47a36d8c.",
 "REG-registry-flags": f"Fresh r1: verify_refs.py --unit M2 -> 'live re-verification of M2: 2 of 560 entries, 0 problems' ({S}/verify_refs_live_M2.txt); the M2 keys cited on L22-L24 (spivak2008calculus, hubbard2015vector) are identical at 47a36d8c and HEAD; registry_flags stays empty.",
 "G-repo-ruff-mypy": f"Fresh r1: ruff check . 'All checks passed!', ruff format --check . '555 files already formatted', mypy --no-incremental 'Success: no issues found in 386 source files' ({S}/ruff_check.txt, ruff_format.txt, mypy.txt). pyproject.toml changed in the delta (extend-exclude gained ledgers/*/lab-mutants); the gates pass with it.",
 "G-render-curriculum-diff": f"Fresh r1: render_curriculum.py -> 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)', then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 with empty output ({S}/render_curriculum.txt, curriculum_diff.txt).",
 "G-build-site-fetch-data": f"Fresh r1: build_site.py --check -> 'site data current: 6 outputs' (exit 0); fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems' (exit 0) ({S}/build_site_check.txt, fetch_data_check.txt). course/assets/data/program.json changed in the delta and is covered by the build_site check.",
 "G-check-projects-all": f"Fresh r1: check_projects.py --all exit 0; 'check_projects M2: PASS' ({S}/check_projects_all.txt). project.html changed in the delta (2 lines, Lab 2 completion text, outside this slice).",
 "LAB-L22-L24-expected": f"Fresh r1: run_labs.py --unit M2 PASS for L22, L23, L24 (expected block equals live output under the page rule, {S}/run_labs_L2*.txt); the twin stdout reproduced under python -I -W error ({S}/twin_L2x_stdout.txt).",
 "G-page-code-equals-twin-dummy": None,
}
fresh.pop("G-page-code-equals-twin-dummy")

carry_extra = {
 "CARD-L23": "course/modules/M/M2/cards.json lesson L23 blocks, 24 of 24 byte-identical since 47a36d8c (card_delta.txt)",
 "N-L24-remark44-numbers": "cards.json block M2-c365 (cards.json:2526) byte-identical",
 "M-L24-remark44-assumption": "cards.json block M2-c365 (cards.json:2526) byte-identical",
 "N-L24-minimizers": "cards.json block M2-c370 (cards.json:2548) byte-identical",
 "N-L22-partA-ln": "cards.json block M2-c328 (cards.json:2249) byte-identical",
 "N-L22-partB-5.4e-12": "cards.json block M2-c329 (cards.json:2257) byte-identical",
 "N-L23-cents-minus15-plus16": "cards.json block M2-c352 (cards.json:2407) byte-identical",
 "N-L23-price-cents": "cards.json blocks M2-c341..c343, c382 byte-identical",
 "N-L23-ratios-and-shifts": "cards.json blocks M2-c345, c346, c384, c385 byte-identical",
 "G-notation": "notation/notation.json is not in the 47a36d8c..HEAD delta",
}
carry_fresh_done = set(fresh)

rows = []
carried = []
for r in base["rows"]:
    rid = r["id"]
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS"}
    if rid in fresh:
        row["evidence"] = fresh[rid]
    else:
        extra = carry_extra.get(rid)
        pref = CARRY if rid != "CARD-L23" else "Carried from round 10 (" + extra + "):"
        if rid in carry_extra and rid != "CARD-L23":
            pref = CARRY[:-1] + "; " + extra + ":"
        row["evidence"] = pref + " " + r["evidence"]
        carried.append(rid)
    rows.append(row)

out = {
 "unit": "M2",
 "slice": "d2",
 "round": 1,
 "verifier": "Claude Haiku 5.5, independent closing-delta verifier for M2-d2, round 1 (did not build M2; no context shared with the builders).",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "47a36d8c78633793ccc762ae19dcd5e19b780d19 (round-10 base fragment ~/.fanout/frags/D-M2-d2.round10.json, verdict PASS). Delta 47a36d8c..95f3f8cb over the slice paths.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M2-d2",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyF21-M2-d2/ledgers/M2/scripts/M2-d2-r1",
 "verified_at": "2026-11-09T15:30:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": (
  "Closing delta (rulings 30 and 37): no new mutants; ruling 26 FAIL kinds only. Scope = the slice as the round-10 base notes define it: L22.html, L23.html, L24.html, their twins tests/labs/M2/lab-M2-L22-1.py, L23-1.py, L24-1.py, and the M2 cards of those lessons (lab-only slice; no grader, no mutants). "
  "Delta 47a36d8c..95f3f8cb over the slice paths: the three pages and three twins are blob-identical; cards.json changed for M2-c330, M2-c334, M2-c404 (L22), M2-c405 removed and M2-c420, M2-c430 added (L24); L23 cards are byte-identical. "
  "Rows whose subject changed (the changed cards, index.html hours, project.html via check_projects, references.json, CURRICULUM.md and curriculum.json, program.json, pyproject.toml) were re-verified from scratch this round. Every other row is carried from round 10 with the carry prefix. "
  "Observations (notes, not rows): (1) card M2-c334 gives '(Misconception 2)' as the locator for the closed-domain sentence, which is in the takeaway list at L22.html:261; the claim is supported and the locator is loose (LOW, not a FAIL kind). "
  "(2) Remark 4.4 and L24.html:243 state the signed computed error -6.603e-9, which Lab 1 does not print (it prints the magnitude); the page says so, and the base round re-derived the signed value. "
  "Not run: the full pytest suite (only -k M2 is relevant); run_graders and mutate_graders (no grader in this slice, and ruling 37 leaves the standing mutant set empty for a lab-only slice); verify_refs live over the whole registry (only the M2 keys matter here); Pyodide for other units. "
  "Card line numbers are cards.json line numbers at HEAD. card_delta.py uses the file's own layout (' {' opens a card), so cards whose text contains braces are compared."
 ),
 "summary": "",
}
n = len(rows)
out["summary"] = (f"slice d2 round 1 (closing delta): rows={n}, pass={n}, fail=0, unverifiable=0. Mutants 0 (lab-only slice, ruling 37). "
                  f"Fresh this round: {len(fresh)} rows (gates re-run, cards changed in the delta re-derived from the lesson text, index.html hours, project check, references, curriculum render, site data). "
                  f"Carried from round 10: {len(carried)} rows (their subjects are byte-identical since 47a36d8c). Verdict PASS.")
json.dump(out, open(root + "/ledgers/M2/M2-d2.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", n, "fresh", len(fresh), "carried", len(carried))
