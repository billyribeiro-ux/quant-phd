import json, sys, datetime, pathlib
root = pathlib.Path("/tmp/verify23-AC4-d")
prev = json.load(open("/tmp/fanout-frags/AC4-d.round22.json"))
CARRY = "Carried from round 22 (cited passage byte-identical since the previous pin d160ac3; the only changed lines in this delta are L07.html line 100, L08.html line 102 and cards AC4-c095, c108, c113, c137-c140): "
NEW = {
 "AC4-d-cmd-pin": "git -C /tmp/verify23-AC4-d rev-parse --short HEAD prints 503d139; git symbolic-ref -q HEAD exits 1 (detached). Checkout is the round-23 pin.",
 "AC4-d-r6-delta-coverage": "git diff --stat d160ac3 503d139 -- course tests atlas plans references curriculum tools: slice files changed are course/modules/AC/AC4/L07.html (line 100), course/modules/AC/AC4/L08.html (line 102) and course/modules/AC/AC4/cards.json (AC4-c020, c037, c095, c108, c113, c135-c140); tests/labs/AC4/* unchanged (empty diff). Non-slice files (AC1, M1, CF1 cards) not judged.",
 "AC4-d-cmd-run_labs": "python tools/run_labs.py --unit AC4 printed 'run_labs AC4: PASS (10/10)' and exit 0 (scripts/AC4-d-r23/run_labs.out).",
 "AC4-d-cmd-twin-isolated": "python -I -W error on tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py: both exit 0 (scripts/AC4-d-r23/twin_L07.out, twin_L08.out).",
 "AC4-d-cmd-page_smoke": "tools/page_smoke.py --unit AC4 --pages L07 L08: both pages PASS, 'page_smoke AC4: PASS', exit 0 (scripts/AC4-d-r23/page_smoke.out).",
 "AC4-d-cmd-check_pages": "tools/check_pages.py --all: 'check_pages AC4: PASS', exit 0 (scripts/AC4-d-r23/check_pages.out).",
 "AC4-d-cmd-check_dag": "tools/check_dag.py --all: 'check_dag AC4: PASS', exit 0 (scripts/AC4-d-r23/check_dag.out).",
 "AC4-d-cmd-check_projects": "tools/check_projects.py --all: 'check_projects AC4: PASS', exit 0 (scripts/AC4-d-r23/check_projects.out).",
 "AC4-d-cmd-lint-mypy": "ruff check tests/labs/AC4 and ruff format --check: 'All checks passed!', '10 files already formatted'; mypy --no-incremental on lab-AC4-L07-1.py and lab-AC4-L08-1.py: 'Success: no issues found in 2 source files' (scripts/AC4-d-r23/ruff_r23.out, mypy_r23.out).",
 "AC4-d-cmd-pytest": "pytest -q -k AC4 on tests/test_labs.py, tests/test_page_smoke.py, tests/test_page_checks.py: exit 0, all dots (scripts/AC4-d-r23/pytest_ac4_r23.out).",
 "AC4-d-cmd-verify_refs": "tools/verify_refs.py --unit AC4 (live): 'live re-verification of AC4: 2 of 560 entries, 0 problems', rc 0 (scripts/AC4-d-r23/vr_live_AC4_r23.out). tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc 0 (scripts/AC4-d-r23/vr_offline_r23.out).",
 "AC4-d-r17-cmd-embed": "scripts/AC4-d-r23/embed_cmp_r23.py: the expected blocks of L07.html (18 lines) and L08.html (19 lines) equal the stdout of the twins run under python -I -W error (scripts/AC4-d-r23/embed_cmp_r23.out).",
 "AC4-d-2.2-numbers-L08": "Re-read this round: L08.html §4 (lines 115-122): RI 30 -> 102.8 (200 - 0.09 x 1,080 = 102.8), EVA 6 -> 62.8 (0.8 x 200 - 0.09 x 1,080 = 62.8), changes 72.8 and 56.8 recomputed; §5 (line 128) RI 15/20, ratio 0.12/0.10 recomputed; §6 lines 296-298 SIM-G 2250 - 2736 = -486 recomputed; §7 line 303 (C 1,000 -> RI 30, C 1,400 -> RI -6) recomputed; Lab 1 expected block (lines 272-290) equal the twin output (embed_cmp_r23.out). §3 has no numbers in the changed line 102.",
 "AC4-d-2.4-math-L08": "L08.html Definition 8.1 (lines 65-76), Lemma 8.2 (86), Lemma 8.3 (92), Proposition 8.4 statement (line 102 now 'with r and tau unchanged', lines 101-107) and proof (line 107): Subtracting the before/after definitions gives dRI = dOI - r dC and dEVA = (1-tau) dOI - r dC, which needs r and tau unchanged, so the new hypothesis is exactly what the proof uses. §3 line 109: dRI - dEVA = tau dOI (equal to Lemma 8.2 applied to the change) and the sign statement with r > 0, tau <= 1, dC > 0 re-derived. PASS.",
 "AC4-d-L07-opportunity-cost-def": "Re-verified against the new line 100 of L07.html: 'With q > 0 and q <= K (Lemma 7.2) and E <= K (section 1), D <= q, so with p_m >= v the lowest price never exceeds p_m (P2).' Lemma 7.2 (line 89-96) hypotheses are 'q > 0 and q <= K' (confirmed); section 1 bullets state 'E <= K' (confirmed); D = max(0, q+E-K) (line 76-78) gives D <= q when E <= K and q >= 0; P2 (lines 373-376, solution in the same block) proves t_min <= p_m by the same chain. The previous FAIL (E <= K attributed to Lemma 7.2) is fixed. Re-derived: t_min = v + D(p_m-v)/q <= v + (p_m - v) = p_m. PASS.",
 "AC4-d-r3-L08-why-and-s3-s5-text": "Re-verified: L08.html §3 (lines 98-109) including the changed Proposition 8.4 statement at line 102: 'with r and tau unchanged' is consistent with the sentence before it at line 98 ('with the rate and the tax rate unchanged') and with the proof. why-it-matters (line 52) and §5 (lines 126-130) unchanged.",
 "AC4-d-L08-tau-zero-scope": "Re-verified on L08.html §3 line 109 (paragraph after Proposition 8.4, unchanged): dRI - dEVA = tau dOI, so the two changes are equal only when tau = 0 or dOI = 0 (both stated); the 'with r > 0, tau <= 1, dC > 0' sign claim re-derived. PASS.",
 "AC4-d-2.9-prose-banned": "Re-scan of all added lines (scripts/AC4-d-r23/added_lines_slice_r23.txt: 2 page lines; cards.json added/changed texts) for roughly/about/historically/typically/usually/half/ellipsis: no match (command output in scripts/AC4-d-r23/). Other learner prose carried.",
 "AC4-d-r17-process-words": "Re-scan of the added slice lines and the new/changed card texts for build/builder/round/verifier/REQUEST/unit report: no match.",
 "AC4-d-r17-mutants-killed": "Re-run this round: 37 transplanted mutants (scripts/AC4-d-r23/transplant_lines_r23.out) all KILLED; full-file copies in ledgers/AC4/mutants/AC4-d-r17, r19 and r20 re-run (scripts/AC4-d-r23/full_mutants_r23.out): 32 differ from the current twin (KILLED), 1 survivor (r20 m20 midpoint, see AC4-d-r22-midpoint-survivor), 17 superseded untagged r18 copies (scripts/AC4-d-r23/r18_untagged_r23.out) not counted as kills per round 20.",
 "AC4-d-r18-mutants-run": "Re-run this round: scripts/AC4-d-r23/full_mutants_r23.out and r18_untagged_r23.out cover all 26 AC4-d-r18 files (9 L08_n tagged, 17 untagged).",
 "AC4-d-r19-mutants-rerun": "Re-run this round: scripts/AC4-d-r23/transplant_lines_r23.out covers the r19 transplants (m19_L07_firm_surplus..., m19_L07_t_min_divides_by_capacity, m19_L08_first_year_charge..., m19_L08_residual_income_after_tax, r17_carry_L08_ratio_ge_strict, r18_carry_L07_*, r18_carry_L08_ri_side_strict): all KILLED; the eleven r19 full files are in full_mutants_r23.out.",
 "AC4-d-r17-cards-scope": "cards.json now has 140 cards; L07 cards are c082-c096, c117, c137, c138 and L08 cards c097-c109, c113-c116, c129, c134, c139, c140 (scripts/AC4-d-r23/card_coverage_r23.out). Scope re-verified for the changed and new entries.",
 "AC4-d-r17-cards-cover": "scripts/AC4-d-r23/card_coverage_r23.out: L07 18 cards, L08 21 cards, every L07/L08 card is in the scope listed above; c110-c112 are L06 cards.",
 "AC4-d-r6-cards-dup-scan": "scripts/AC4-d-r23/cards_r23.py on course/modules/AC/AC4/cards.json: total cards 140, duplicate ids [], duplicate fronts [].",
 "AC4-d-r17-cards-scope-ok": "AC4-c082 carried; AC4-c095, c108 re-verified this round (new text below); AC4-c082 unchanged.",
 "AC4-d-r19-cards-c095-basis": "cards.json AC4-c095 basis is 'Lab 1 (SIMULATED), output lines for the counts and the four check lines' (the four check lines are the supplier-gain, sign, midpoint and sum lines of the expected block); grade C. The new front and back: 75 empty, 112 feasible, consistent with 'cases with q <= K and an empty range: 75' and 'cases with a feasible range: 112' (201 cases = 14 with q > K + 75 + 112; 187 = 201 - 14). PASS.",
 "AC4-d-2.7-cards-L07-L08": "Re-verified cards of the slice after the delta: changed AC4-c095, AC4-c108, AC4-c113 and new AC4-c137, c138 (L07), AC4-c139, c140 (L08). Each back agrees with the expected block of its lesson (checks in the table below). Each back number appears in the lesson html (scripts/AC4-d-r23/cards_r23.out; the two false hits AC4-c087/c088 '30,000' are TeX '30{,}000' in L07, not a missing number).",
 "AC4-d-r3-L08-cards-c113-c116": "AC4-c113 re-verified: 'SIM-D has the larger base, 124,000 cents against 59,000 for SIM-A, and the smaller residual income, -4130.00 against -2440.00 cents' matches the SIM-A and SIM-D rows of the expected block (lines 272-290). c114-c116 unchanged.",
 "AC4-d-r22-delta-hunks": "Delta d160ac3..503d139 read hunk by hunk for the slice (scripts/AC4-d-r23/added_lines_slice_r23.txt: 2 page lines): L07.html line 100 and L08.html line 102 re-verified (rows AC4-d-L07-opportunity-cost-def, AC4-d-r3-L08-why-and-s3-s5-text). cards.json hunks: AC4-c095, c108, c113 changed; AC4-c137, c138, c139, c140 added; AC4-c020, c037, c135, c136 are L02/L03 cards outside this slice (not judged here).",
 "AC4-d-r20-superseded-mutants": "Superseded full-file copies re-run (scripts/AC4-d-r23/r18_untagged_r23.out, full_mutants_r23.out). Their intended mutations are covered by transplants (r18 n01, n02, n04, n05, n06, n09 and r17 L07 m03, r17 L08 m02) and by the r23 check that the L08 tie-guard and same-name-order mutations are equivalent (scripts/AC4-d-r23/tie_guard_transplant_r23.out, n09_transplant_r23.out).",
 "AC4-d-r17-mutant-L08-m04-ties": "The full file r17_L08_m04_discord_ignores_ties.py differs from the current twin in older boundary and wording lines (lines 71-111 of the copy), so its full-file run is not counted as a kill. Its intended mutation (drop 'and by_ri != 0 and by_ratio != 0' at twin line 119) transplanted onto the current twin gives identical output (scripts/AC4-d-r23/tie_guard_transplant_r23.out, 'exit 0 output_differs False'): equivalent on the shipped seed.",
 "AC4-d-r18-equiv-L08-n09": "The full file L08_n09_discord_pairs_same_name_order.py differs from the current twin in older boundary lines; its intended mutation (twin line 116 'if a.name < b.name' -> '<=') transplanted onto the current twin gives identical output (scripts/AC4-d-r23/n09_transplant_r23.out, 'output_differs False'): equivalent on the shipped seed. Self-pairs have by_ri = 0 and are removed by the guard at line 119.",
 "AC4-d-r20-equivalent-survivors": "Re-verified by the two transplants above (scripts/AC4-d-r23/tie_guard_transplant_r23.out, n09_transplant_r23.out).",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW:
        ev = NEW[rid]
        status = "PASS"
        check = r["check"]
        loc = r["location"]
    elif rid == "AC4-d-L07-opportunity-cost-def":
        ev = NEW[rid]; status = "PASS"; check = r["check"]; loc = r["location"]
    else:
        ev = CARRY + r["evidence"]; status = r["status"]; check = r["check"]; loc = r["location"]
        if status != "PASS":
            raise SystemExit("unexpected non-PASS carry " + rid)
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
ids = {r["id"] for r in rows}
assert set(NEW) <= ids, set(NEW) - ids
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
EXTRA = [
 ("AC4-d-r23-delta-slice-hunks", "2.9-structure", "course/modules/AC/AC4/L07.html line 100; L08.html line 102; cards.json", "PASS",
  "git diff d160ac3 503d139 -- course/modules/AC/AC4/L07.html course/modules/AC/AC4/L08.html course/modules/AC/AC4/cards.json: L07 1 line changed (100), L08 1 line changed (102), cards: 3 changed (c095, c108, c113), 4 added (c137-c140) in the slice, plus c020, c037, c135, c136 (L02/L03, outside this slice). No tests/labs/AC4 or project/grader change in the delta."),
 ("AC4-d-r23-L08-prop84-hypothesis", "2.4-math", "course/modules/AC/AC4/L08.html Proposition 8.4 (line 102) and proof (line 107)", "PASS",
  "Re-derived: dRI = (OI+dOI) - r(C+dC) - (OI - rC) = dOI - r dC; dEVA = (1-tau)(OI+dOI) - r(C+dC) - ((1-tau)OI - rC) = (1-tau) dOI - r dC. Both use the same r and tau before and after, so 'with r and tau unchanged' is the exact hypothesis of the proof. The lesson's own §3 sentence (line 98) already states it. Numerical check on §4: 80 - 0.09 x 80 = 72.8 and 0.8 x 80 - 0.09 x 80 = 56.8 (scripts/AC4-d-r23/)."),
 ("AC4-d-r23-cards-c095-c108-c113-edits", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c095, AC4-c108, AC4-c113", "PASS",
  "Each edited back re-checked against the expected block of L07.html (lines 304-321) and L08.html (lines 272-290): c095 '75 have an empty range' (line 'cases with q <= K and an empty range: 75') and 'The other 112 have a feasible range' (201 - 14 = 187; 187 - 75 = 112); c108 '8 of 8 divisions' (identity line 'holds for 8/8 divisions'), 'Lemma 8.2' is the EVA - RI identity (line 86); c113 base 124,000 vs 59,000, RI -4130.00 vs -2440.00 cents (rows of the table). Grades C with lab basis, as rule (e) requires."),
 ("AC4-d-r23-cards-c137-c140", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c137, c138 (L07), AC4-c139, c140 (L08)", "PASS",
  "c137: supplier-gain zero at t_min and nonempty iff surplus >= 0, '187 of 187' = checks 'supplier gain is zero at t_min: 187/187' and 'range is nonempty exactly when the firm-wide surplus is >= 0: 187/187'. c138: 'for all 112 feasible pairs' = 'gains sum to the surplus at both ends and the midpoint: 112/112'. c139: '9 of 9' = 'RI >= 0 exactly when OI/C >= r holds for 9/9 divisions, boundary included'; boundary RI 0.00. c140: SIM-D 5.67% vs SIM-A 4.86% (table rows) and both returns below 9%. All grade C with basis naming Lab 1 (SIMULATED). Source: scripts/AC4-d-r23/cards_r23.out."),
 ("AC4-d-r23-embed-and-twin-stdout", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py; lab-AC4-L08-1.py; the expected blocks in L07.html and L08.html", "PASS",
  "scripts/AC4-d-r23/embed_cmp_r23.py: 'L07 expected block equals twin stdout: True' (18 lines); 'L08 ... True' (19 lines). Twins unchanged since fd9a9b7 (git diff empty for tests/labs/AC4)."),
 ("AC4-d-r23-transplant-mutants", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r23/transplant_lines_r23.py on tests/labs/AC4 twins", "PASS",
  "37 of 37 previous line-level mutants (r17, r18, r19 lists in the round-22 fragment) KILLED on the current twin (scripts/AC4-d-r23/transplant_lines_r23.out)."),
 ("AC4-d-r23-full-mutants", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17, AC4-d-r18 (untagged), AC4-d-r19, AC4-d-r20", "PASS",
  "Full-file copies re-run under python -I -W error (scripts/AC4-d-r23/full_mutants_r23.out, r18_untagged_r23.out): 32 KILLED (exit or output differs), 1 survivor m20_L07_midpoint_check_uses_lower_end (identical output, equivalent on the shipped seed, AC4-d-r22-midpoint-survivor), 17 untagged r18 copies differ from the current twin and are superseded (not counted, see AC4-d-r20-superseded-mutants)."),
 ("AC4-d-r23-verify-refs", "2.1-citations", "tools/verify_refs.py --unit AC4; tools/verify_refs.py --offline", "PASS",
  "Live: 2 of 560 entries, 0 problems. Offline: 560 entries, 0 problems. L07/L08 references lists unchanged in the delta."),
]
for rid, check, loc, status, ev in EXTRA:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
mutants = []
for m in prev["mutants"]:
    m2 = dict(m)
    m2["killed_by"] = "round 23 transplant of the mutant's changed line onto the current twin (ledgers/AC4/scripts/AC4-d-r23/transplant_lines_r23.out): KILLED"
    mutants.append(m2)
notes = prev["notes"] if isinstance(prev["notes"], list) else [prev["notes"]]
notes = [
 "Delta d160ac3..503d139 read hunk by hunk for the slice: L07.html line 100 (opportunity-cost paragraph after Lemma 7.2) and L08.html line 102 (Proposition 8.4 hypothesis); cards.json AC4-c095, c108, c113 edits and new AC4-c137 to c140. L02, L03 cards (AC4-c020, c037, c135, c136), AC1 and CF1 changes are outside this slice and not judged.",
 "The one previous FAIL row (AC4-d-L07-opportunity-cost-def) is fixed: E <= K is now attributed to section 1 and q <= K to Lemma 7.2, and the chain D <= q is re-derived. Every previous PASS row is re-verified (command rows, affected numbers, changed cards) or carried with the prefix. No new FAIL rows.",
 "Lesson-only slice: the project-slice rule of at least 3 new student-error mutants does not apply; no new mutants were written this round. Lab twins are unchanged since fd9a9b7, so the alternative-implementation rows of rounds 19 and 20 are carried (the twin is the object they test).",
 "Equivalence of the r17 L08 m04 and r18 L08 n09 full-file copies was re-derived this round by transplanting only each intended mutation onto the current twin (tie-guard removal; '<' to '<=' in the pair loop): identical output on the shipped seed. The full copies differ from the current twin in older boundary lines, so they are not counted as kills.",
 "Not checked this round: the r17 alternative-implementation scripts (carried), the full-file r18 superseded copies beyond their exit code and output comparison, Pyodide timing beyond page_smoke, mutate_graders (project grader unchanged in the delta, carried), and the independent integer recompute (lab twins unchanged; carried from round 20 and round 22).",
]
summary = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows), "mutants": len(mutants), "mutants_killed": len(mutants)}
frag = {
 "unit": "AC4",
 "slice": "AC4-d",
 "round": 23,
 "verifier": "round-23 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
 "pin": "503d139",
 "base": "d160ac3 (round-22 pin; /tmp/fanout-frags/AC4-d.round22.json used as context; previous PASS rows re-verified or carried only where the cited passage is byte-identical)",
 "checkout": "/tmp/verify23-AC4-d (detached worktree at 503d139, .venv symlink)",
 "scratch": "/tmp/AC4-d-v23 (scratch); command outputs and scripts in ledgers/AC4/scripts/AC4-d-r23/",
 "verified_at": NOW,
 "verdict": "PASS" if summary["fail"] == 0 and summary["pass"] == summary["rows"] else "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": summary,
}
out = root / "ledgers/AC4/AC4-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), summary)
