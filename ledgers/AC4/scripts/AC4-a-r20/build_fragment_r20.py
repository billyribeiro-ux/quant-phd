"""Builds ledgers/AC4/AC4-a.json (round 20) from the round-19 fragment: fresh rows where a cited line is in a
changed hunk or a command row was re-run; every other PASS row carried with the round-19 prefix."""
import json, sys
from pathlib import Path

ROOT = Path("/tmp/verify20-AC4-a")
prev = json.load(open("/tmp/fanout-frags/AC4-a.round19.json"))
S = "ledgers/AC4/scripts/AC4-a-r20/"
PIN_PREV = "51fa336"

FRESH = {
 "AC4-a-cmd-check-pages": ("PASS", "re-run r20: 'check_pages AC4: PASS' (ledgers/AC4/scripts/AC4-a-r20/check_pages.out, rc=0)"),
 "AC4-a-cmd-check-dag": ("PASS", "re-run r20: 'check_dag AC4: PASS' (check_dag.out, rc=0)"),
 "AC4-a-r19-cmd-check-projects": ("PASS", "re-run r20: 'check_projects AC4: PASS' (check_projects.out); project.html itself is another slice and was not read"),
 "AC4-a-cmd-run-labs": ("PASS", "re-run r20: 'run_labs AC4: PASS (10/10)' (run_labs.out, rc=0)"),
 "AC4-a-cmd-twins-isolated": ("PASS", "re-run r20 under python -I -W error: L01 rc=0, 21 lines (twin_L01.out, incl. rc line); L02 rc=0, 13 output lines (twin_L02.out)"),
 "AC4-a-cmd-twin-output-equals-page": ("PASS", "expected_vs_twin.py (r20): 'L01 page line 222 expected 20 lines stdout 20 IDENTICAL'; 'L02 page line 251 expected 13 stdout 13 IDENTICAL' (expected_vs_twin.out)"),
 "AC4-a-cmd-page-smoke": ("PASS", "re-run r20: 'page_smoke AC4: PASS' (page_smoke.out, rc=0): index, L01, L02, project, concepts, review all PASS"),
 "AC4-a-cmd-pytest-labs-lint": ("PASS", "re-run r20: pytest -k AC4 'rc=0 ..........' (10 passed); ruff check 'All checks passed!'; ruff format --check '2 files already formatted'; mypy --no-incremental on both twins 'Success: no issues found in 2 source files' (pytest_labs.out, ruff.out, mypy.out)"),
 "AC4-a-cmd-verify-refs": ("PASS", "re-run r20: offline '560 entries, 0 problems' rc=0; live AC4 '2 of 560 entries, 0 problems' rc=0 (verify_refs_offline.out, verify_refs_live_AC4.out)"),
 "AC4-a-r18-cmd-build-site-check": ("PASS", "re-run r20: build_site.py --check 'site data current: 6 outputs' rc=0 (build_site_check.out)"),
 "AC4-a-num-L01-lab": ("PASS", "re-verified r20: L01.html:242 changed (ValueError sentence). Twin output (twin_L01.out lines 16-20) prints 'months on the fitted line exactly [6, 11]' (months 6 and 11 have the lowest 428 h and highest 1161 h, twin output lines 9 and 14), 'largest absolute residual_cents 51473' = 514.73 USD, 'months with nonzero residual 10 of 12'; the two ValueError lines are printed by the try/except at twin file lines 79-82. Other locators (134, 222-241, 283, 348-362, 403-404) unchanged and carried from round 19 checks."),
 "AC4-a-L01-lab-interpretation": ("PASS", "re-verified r20: L01.html:242 now reads 'two invalid-input cases, each of which raises ValueError and is caught and printed'. Twin file lines 79-82 are 'try: ... except ValueError as exc: print(f\"ValueError for {label}: {exc}\")' and twin output lines 19-20 print the two ValueError messages; the claim is true. 'off by up to 514.73 USD at the others': largest abs residual 51473 at month 1 (not an extreme month). 'simulated range of 400 to 1,200 hours' unchanged. PASS."),
 "AC4-a-r18-L01-why-it-matters": ("PASS", "re-verified r20: L01.html:51 now reads 'a number from the split inherits the limits of the method that produced it'. The limits are stated in Section 5 (L01.html:260 'The split is a convention of the method'; L01.html:261 'Extreme months carry the estimate'); the wording claims no more than Section 5 shows. Cards AC4-c008 agree. PASS."),
 "AC4-a-L02-remark-2-3-whole-units": ("PASS", "re-verified r20: L02.html:81 Remark 2.3 'Lab 1 prints both values'. Twin L02 prints 'single_formula_break_even_units 88.89 first_whole_unit 89' and 'check operating_income(88) -12.00 operating_income(89) 1.50' (twin_L02.out). 88.89 = 120000/1350 (F=1200.00 USD, m=13.50 USD; recompute_r19.py output); ceil = 89; OI(88) < 0 <= OI(89). Remark's general claim (m | F gives whole Q*) is an arithmetic fact of Remark 2.3 text. PASS."),
 "AC4-a-L02-sensitivity-proofs": ("PASS", "re-verified r20: L02.html:108 Proposition 3.3 now begins 'In the single-segment model of Proposition 2.2'. Proposition 2.2 is stated at L02.html:71 for constant F, Proposition 3.3 at L02.html:107-108, and its proof at L02.html:113 cites Proposition 2.2. Proof '(F + dF)/m - F/m = dF/m' is algebra. Other lines 91-114 unchanged and carried. PASS."),
 "AC4-a-L02-remark-5-2-and-prop-5-1": ("PASS", "re-verified r20: L02.html:283 Remark 5.2 now says Proposition 5.1 'does not apply across such a change'. Proposition 5.1 (L02.html:272-278) assumes constant shares w_k, so when shares change its hypothesis fails. Also 'each segment needs its own weighted margin, as Research problem R3 shows' refers to R3 at L02.html:416-420 (unchanged). PASS."),
 "AC4-a-L02-misconceptions": ("FAIL", "re-verified r20: L02.html:311 misconception 'A plan above break-even is safe' now says 'A plan's operating income is non-negative exactly when its volume is at or above the zero of the segment it lies in (Proposition 4.1).' Proposition 4.1 (L02.html:121-127; statement 122, proof 127) gives a zero of a segment only conditionally: the zero on [0,T] is F/m 'if F/m <= T', the zero above T is (F+S)/m 'if that value exceeds T', and the proposition says 'at most one zero in each segment'. Witness: F=30000 USD, m=10 USD, T=2000 units, S=0: on [0,2000] OI=10Q-30000 <= -10000 < 0 (computed: OI(2000)=-10000, OI(1500)=-15000), so segment 1 has no zero and 'the zero of the segment it lies in' has no referent for a plan at 1,500 units. The 'exactly when' biconditional is therefore stated more exactly than Proposition 4.1 supports. Other three items at 300-317 are unchanged and were re-read (item 2 uses 88.89 and 2,088.89; item 3 OI(2001)=-1186.50 USD; item 4 numbers 4 and 25 units, carried)."),
 "AC4-a-L02-problems": ("PASS", "re-verified r20: L02.html:405 (R1 solution) now reads 'A step is the right treatment if the cost changes when volume crosses the threshold and stays fixed on each side of it, and a fixed cost is right if the cost is incurred at every volume in the relevant range.' The statement is consistent with Proposition 4.1 (step = jump at T, constant each side) and with R1 'Specify the test' stem; no number is changed. R3 (416-420) and M3 (341-344), E2 (384-394), R2 unchanged and carried from round 19. PASS."),
 "AC4-a-cards-L01-L02": ("FAIL", "re-verified r20: cards.json unchanged since 51fa336. AC4-c007 back still says 'and the method does not minimize the error across the history'. The delta does not restore that clause: L01.html:279 reads 'the method states no error measure', and grep -i 'minimi|least.squares|error measure' over L01/L02/index finds no lesson sentence stating that the high-low line does not minimize error (only the distractor at L01.html:457); Remark 3.3 (L01.html:128-130) says the method 'carries no measure of its own error' and does not say it fails to minimize. The card asserts a claim with no locator in the lesson or lab. Other 37 L01/L02 cards agree with the current lesson text (numbers re-checked against twin output, see carried rows). FIX: in course/modules/AC/AC4/cards.json, AC4-c007 back, replace 'and the method does not minimize the error across the history' with 'and the method states no error measure (Remark 3.3)'; then run tools/build_site.py --check. Remark 3.3 (L01.html:128-130) supports the replacement wording."),
 "AC4-a-banned-phrases": ("PASS", "re-run r20: grep -n -o -i for roughly, about [0-9%], historically, typically, usually, generally, round, builder, verifier, request, unit report, ..., ellipsis across index.html, L01.html, L02.html: no hits (rc=1; banned_grep.out). PASS."),
 "AC4-a-cite-none-in-lessons": ("PASS", "re-run r20: grep -i horngren|kaplan|datar|data-ref in L01.html and L02.html: only the empty <ol data-references></ol> at L01.html:490 and L02.html:525 (cite_grep.out). PASS."),
 "AC4-a-hub-data-status": ("PASS", "re-run r20: grep random/seed in tests/labs/AC4/lab-AC4-L0[12]-1.py: L01 twin uses 'import random' and a seeded generator (seed_grep.out lines 3-22); index.html unchanged since 51fa336, data-status line carried."),
 "AC4-a-L02-key-results-profitable": ("PASS", "re-run r20: L02.html:433 unchanged; it cites Remark 2.3 at L02.html:81, whose changed sentence ('Lab 1 prints both values') is re-verified above; card AC4-c125 unchanged and consistent. PASS."),
}
for rid in ("AC4-a-cmd-check-pages",):
    pass

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in FRESH:
        st, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev,
                     **({"fix": r["fix"]} if st == "FAIL" and "fix" in r else {})})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"unexpected non-PASS carry {rid}")
    ev = r["evidence"]
    loc = r["location"]
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": f"Carried from round 19 ({loc} byte-identical since the previous pin {PIN_PREV}): " + ev})
missing = set(FRESH) - seen
print("FRESH rows not in round 19 (new):", missing)
json.dump(rows, open("/tmp/AC4-a-r20-rows.json", "w"), ensure_ascii=False, indent=1)
print(len(rows), sum(1 for r in rows if r["status"] == "FAIL"))
