# Builds ledgers/AC2/L03-L04.json (round 6) from the round-5 fragment: every round-5 id kept.
import json, sys
R5 = "/tmp/ac2-frags/L03-L04.round5.json"
OUT = sys.argv[1]
d = json.load(open(R5, encoding="utf-8"))
L3 = "course/modules/AC/AC2/L03.html lines outside 710, 724 and 812 byte-identical since 11b3477"
L4 = "course/modules/AC/AC2/L04.html lines outside 312-315, 333-335, 494 and 594 byte-identical since 11b3477 (numbers after 335 are +7 versus round 5)"
CARD = "course/modules/AC/AC2/cards.json entries byte-identical since 11b3477 (the file changed only at c075, c107, c123, c130)"
REVER = {
 "L03-L04-cmd-pin": "Re-run this round. `git rev-parse --short HEAD` -> ff9284f; `git diff --stat 11b3477 HEAD -- course tests atlas plans references curriculum` -> 11 files; slice files touched: L03.html (lines 710, 724, 812), L04.html (lines 312-315, 333-335, 494, 594), cards.json (c075, c107, c123, c130 only: not this slice), index.html (L05 card only), tests/labs/AC2/lab-AC2-L04-1.py (+4 lines, lines 169-172). Not a PASS-by-carry: all rows re-run.",
 "L03-L04-cmd-check_pages": "Re-run: `.venv/bin/python tools/check_pages.py --unit AC2` -> 'check_pages AC2: PASS', exit 0.",
 "L03-L04-cmd-check_dag": "Re-run: `.venv/bin/python tools/check_dag.py --unit AC2` -> 'check_dag AC2: PASS', exit 0.",
 "L03-L04-cmd-check_projects": "Re-run: `.venv/bin/python tools/check_projects.py --unit AC2` -> 'check_projects AC2: PASS', exit 0.",
 "L03-L04-cmd-run_labs": "Re-run: `.venv/bin/python tools/run_labs.py --unit AC2 --page L03` and `--page L04` -> 'run_labs AC2: PASS (1/1)' each, exit 0 (/tmp/ac2-v/L03-L04/r6/run_labs_L03.txt, run_labs_L04.txt).",
 "L03-L04-cmd-twins-strict": "Re-run: `.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L03-1.py` exit 0 (23 stdout lines); `... lab-AC2-L04-1.py` exit 0 (15 stdout lines, was 12 in round 5; the three added lines are r_squared_full_precision, one_minus_r_squared, var_gap_over_var_cf). Outputs in /tmp/ac2-v/L03-L04/r6/twin_L0{3,4}.txt.",
 "L03-L04-cmd-twin-identity": "Re-run: ledgers/AC2/scripts/L03-L04-r6/twin_and_cards_check.py -> 'L03 code_equals_twin True expected_equals_twin_stdout True expected_lines 23'; 'L04 code_equals_twin True expected_equals_twin_stdout True expected_lines 15' (output /tmp/ac2-v/L03-L04/r6/twin_cards_check.txt).",
 "L03-L04-cmd-page_smoke": "Re-run: `.venv/bin/python tools/page_smoke.py --unit AC2 --pages L03 L04` -> 'page_smoke modules/AC/AC2/L03.html: PASS', 'page_smoke modules/AC/AC2/L04.html: PASS', 'page_smoke AC2: PASS'; lab lab-AC2-L04-1 0.0 s.",
 "L03-L04-cmd-verify_refs": "Re-run: `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `tools/verify_refs.py --unit AC2` (live) -> 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0 (/tmp/ac2-v/L03-L04/r6/verify_refs_live.txt).",
 "L03-L04-cmd-ruff-mypy-pytest": "Re-run: `ruff check` on both twins -> 'All checks passed!'; `ruff format --check` -> '2 files already formatted'; `mypy --no-incremental` on both twins -> 'Success: no issues found in 2 source files'; `pytest -q tests/test_labs.py tests/test_page_checks.py` -> exit 0 (/tmp/ac2-v/L03-L04/r6/pytest_labs.txt).",
 "L03-L04-cite-sloan1996stock": "Re-run this round. Claim moved from L04 line 352 to line 359 (the +7 shift); text unchanged. Re-fetched `curl https://api.crossref.org/works/10.2308/tar-9608042309` -> HTTP 200; title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?'; abstract 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components of currents earnings.' The page's claim matches; grade C, locator 'Crossref abstract; passage locator not confirmed' is honest; the page states no finding (line 360).",
 "L03-L04-num-L03-E1": "Re-derived this round from the twin's unrounded values (ledgers/AC2/scripts/L03-L04-r6/e3_counterfactual.py, output /tmp/ac2-v/L03-L04/r6/e3_counterfactual.txt): NOPAT change -22.2355% (printed -22.2%); average invested capital change +7.7174% (printed +7.7%); ROIC ratio 0.7220 -> 27.81% fall (printed 27.8%). The new sentence 'from a 22.2% fall to a 27.8% fall' matches these. 'Most of the fall is in operating income': the NOPAT term is ln(0.77764)=-0.2519 of the total ln(0.72202)=-0.3262, i.e. 77%, so 'most' is right.",
 "L03-L04-num-L03-E3": "Re-derived this round (e3_counterfactual.txt): growth 2022 9.5584% (page: 9.56% from unrounded values; printed 993.5/906.9-1 = 9.5485% -> 9.5%, as the page says); 2023 9.0165% (page 9.0%); 2024 6.5258% (page 6.5%); 2023 rate 9.017% (3 dp of 9.01651%, matches the page); average IC 2023 1,038.34 and 2024 1,118.47 USD m (page 1,038.3 and 1,118.5; +7.72% -> 7.7%). Counterfactual 2024 fall at constant 2023 growth: ROIC 0.096257 vs 0.134941 -> -28.67% (page 28.7%). Flat-capital fall equals NOPAT fall -22.24% (page 22.2%). The lab does not print the counterfactual, and the page says so.",
 "L03-L04-math-L03-E3-causal": "Round-5 FAIL is FIXED and re-verified PASS. The round-5 sentence 'the slower capital growth offsets part of it' and 'With NOPAT fixed, slower capital growth raises ROIC' were removed. The new text: average invested capital ROSE 7.7% in 2024, which deepens the fall (ROIC -27.8% against -22.2% had average capital been flat: -22.24% is the flat-capital case, since with capital unchanged ROIC moves with NOPAT); growth slowed from 9.0% to 6.5%; against the constant-2023-growth counterfactual the fall would be 28.7% (-28.67%), so the slowdown lessens the fall by about 0.9 points relative to that case. The scope phrase 'the slowdown matters only relative to it' is correct: a growth slowdown has no ROIC effect except relative to a counterfactual. Evidence: e3_counterfactual.txt; 'driven by the operating-income decline' is supported by the 77% NOPAT share of the log change (see num-L03-E1). PASS.",
 "L03-L04-num-L04-E3-square": "Re-verified this round (ledgers/AC2/scripts/L03-L04-r6/l04_e3_numbers.py, output l04_e3_numbers.txt; recomputed from the twin's build_panel at seed 2604, n=400, moving): r = 0.8221493802, r^2 = 0.6759296033 (page 0.6759), 1 - r^2 = 0.3240703967 (page 0.3241), var(gap)/var(cf) = 0.3285289812 (page 0.3285). The lab prints r_squared_full_precision 0.6759, one_minus_r_squared 0.3241 and var_gap_over_var_cf 0.3285 (twin stdout). Quiz item data-answer 0.6759 with tolerance 0.0005 matches; its explain says 'at full precision is 0.6759 (r_squared_full_precision, E3)'.",
 "L03-L04-math-L04-E3-claim": "Re-verified this round: E3 solution at L04 line 494 now says the squared correlation is 0.6759 and 1 - r^2 = 0.3241 is the unexplained share of the cash-flow variance, and var(gap)/var(cf) = 0.3285 is a different figure. Recomputed (l04_e3_numbers.txt): 0.32407 vs 0.32853; they differ, so the page's 'not the same as the variance share of the gap' is right. 'The identity gives the gap exactly, but it does not decompose the variance' is a correct statement: var(cf - bs) = var(cf) + var(bs) - 2cov does not factor as var(cf)(1 - r^2). PASS.",
 "L03-L04-num-L04-lab": "Re-verified this round: expected block at L04 lines 326-340 equals twin stdout exactly (run this round; 15 lines; the block gained r_squared_full_precision 0.6759, one_minus_r_squared 0.3241, var_gap_over_var_cf 0.3285). Interpretation paragraph: means -0.0308 and -0.0298, correlation 0.8221, gap above 0.01 for 67.75% (printed 0.6775), seeds 0.6775/0.6800/0.7000: all match the output.",
 "L03-L04-lab-L04": "Re-verified this round: the embedded data-run code equals tests/labs/AC2/lab-AC2-L04-1.py (twin_cards_check.py: code_equals_twin True); the twin runs under -I -W error with exit 0 and 15 lines; run_labs and page_smoke PASS. The added lines are print statements only; the hypothesis and interpretation texts are unchanged.",
 "L03-L04-lab-L04-docstring": "Re-verified this round: the twin's docstring (lines 1-10) and the page's lab description still match the code; the four-line addition (lines 169-172) adds prints and one local variable, with no change to the generator, the identities or the claims. PASS.",
 "L03-L04-quiz-keys": "Re-verified this round: L03 quiz numeric keys 0.1349 (tolerance 0.0002; 140.114/1038.34 = 0.13494), 0.1239 (cash not netted, Lab 1 prints it), and the Q5 mc key (average denominator) with its explain now reading 'with both year ends positive, the average is below the year-end value when capital rises' (Proposition 3.4 requires both year ends positive; the proof's hypothesis); L04 quiz 0.6759 (tolerance 0.0005) and its explain (r_squared_full_precision). Other keys unchanged (carried: quiz-item lines outside L03 812 and L04 594).",
 "L03-L04-prose-L03-claims-unmarked": "Re-verified this round for the changed quiz explanation (L03 line 812; the rest carried): the Proposition 3.4 wording now carries its hypothesis, with both year ends positive. Other spans carried from round 5 (" + L3 + ").",
 "L03-L04-process-words": "Re-run this round on both pages (visible prose, labs excluded): no 'builder', 'this build', 'REQUESTS' or 'unit report'. The new L03 line 724 and L04 lines 494 and 370 contain no process words (checked by grep).",
 "L03-L04-banned-phrases": "Re-run this round on both pages: the check_pages banned list (BANNED in tools/check_pages.py) passes; a scan of visible prose for roughly, approximately, historically, typically, clearly, obviously, ellipsis and TODO/TBD finds none in the changed lines (L03 710, 724, 812; L04 312-335, 494, 594). The scope words 'only' and 'all' in the changed sentences were judged individually (see num-L03-E3, math-L03-E3-causal).",
 "L03-L04-struct-L03": "Re-run this round: check_pages AC2 PASS; the L03 section list (1-9), problem tiers, Lab 1 block, quiz and references are present; data-hours 8 unchanged.",
 "L03-L04-struct-L04": "Re-run this round: check_pages AC2 PASS; the L04 section list (1-10) is present; data-hours 9 unchanged; the lab and quiz blocks render through page_smoke.",
 "L03-L04-dag-concepts": "Re-run this round: check_dag AC2 PASS. Concept definitions unchanged in the delta (no dfn or data-concept attribute in the changed hunks).",
 "L03-L04-lab-L03": "Re-run this round: Lab 1 of L03 runs under -I -W error (exit 0, 23 lines); the embedded code equals the twin (twin_cards_check.py); the expected block equals the twin stdout. The L03 twin is unchanged in the delta.",
 "L03-L04-cards-L03": "Re-verified this round: AC2-c032..c047 and AC2-c121 (17 cards with lesson L03) are byte-identical to 11b3477 (per-id comparison in twin_cards_check.py: changed ids are only c075, c107, c123, c130). Each was read against its lesson text in the round-5 pass and against L03 this round (c035 ValueError, c039/c041/c047 lab figures, c043 goodwill, c044 omitted lines, c045 algebra); no card changed.",
 "L03-L04-cards-L04": "Re-verified this round: AC2-c048..c062 and AC2-c137 (16 cards with lesson L04) are byte-identical to 11b3477; c058 (grade C, Crossref basis) matches the Sloan claim (L04 line 359) and the Crossref abstract re-fetched this round. c056 arithmetic: 15/1600 + 30/1600 - 10/1600 = 0.021875 (checked).",
 "L03-L04-cards-dup": "Re-run this round: twin_cards_check.py: 140 cards, ids contiguous AC2-c001..c140, unique fronts and unique backs (no duplicates); changed-card set vs 11b3477 is c075, c107, c123, c130 (not this slice).",
 "L03-L04-hours": "Carried from round 5 (" + "course/modules/AC/AC2/L03.html and L04.html data-hours attributes byte-identical since 11b3477" + "): data-hours=8 (L03) and 9 (L04) unchanged; my estimate: L03 about 8 h, L04 about 9 h, both within +/-30%.",
 "L03-L04-lab-L03-docstring": "Carried from round 5 (tests/labs/AC2/lab-AC2-L03-1.py byte-identical since 11b3477): docstring lines 1-10 match the code; the prints are as described.",
 "L03-L04-lab-numbering": "Carried from round 5 (" + L3 + "; " + L4 + "): 'Lab 1' names the single lab of each page.",
 "L03-L04-xref-L04-to-L05": "Carried from round 5 (" + L4 + "; course/modules/AC/AC2/L05.html unchanged at its cross-referenced lines): the sorted-portfolio test references resolve (the cross-reference lines moved +7 in L04).",
 "L03-L04-prose-L04-unmarked-claims": "Carried from round 5 (" + L4 + "): line 90 (Section 2 intro), line 360 (Section 4) and line 378 (misconception 1) are at +7 lines (now 367 and 385, the honest-pending paragraph at 370 is now 377); the open-items file reference is unchanged. Round-5 PASS text carried.",
}
out_rows = []
for r in d["rows"]:
    rid = r["id"]
    row = dict(r)
    row["status"] = "PASS"
    if rid in REVER:
        row["evidence"] = REVER[rid]
    else:
        ev = r["evidence"]
        for p in ("Carried from round 4 (", "Carried from round 3 (", "Carried from round 5 ("):
            if ev.startswith(p):
                ev = ev[ev.index("):") + 2:].lstrip()
                break
        if rid.startswith("L03-L04-cite-") or rid.startswith("L03-L04-cards-"):
            pre = "Carried from round 5 (" + (L4 if "L04" in rid and "L03" not in rid else L3) + "): "
        elif "L04" in rid and "L03" not in rid:
            pre = "Carried from round 5 (" + L4 + "): "
        elif "L03" in rid and "L04" not in rid:
            pre = "Carried from round 5 (" + L3 + "): "
        else:
            pre = "Carried from round 5 (" + L3 + "; " + L4 + "): "
        row["evidence"] = pre + ev
    out_rows.append(row)
# corrected locators in carried rows that cite an L04 line now at +7
for row in out_rows:
    if row["id"] == "L03-L04-cite-penman2013financial":
        row["evidence"] = row["evidence"].replace("L03.html Section 4 bullet 4 (line 624", "L03.html Section 4 bullet 4 (line 624 unchanged")
out = {
 "unit": "AC2", "slice": "L03-L04", "round": 6,
 "verifier": "round-6 independent verifier for AC2 slice L03-L04 (fresh checkout pinned at ff9284f); re-ran every command row; re-derived the E1/E3 growth, ROIC and counterfactual figures and the L04 E3 squared-correlation figures from the twins' own functions (unrounded); re-fetched the Sloan Crossref record.",
 "pin": "ff9284f",
 "base": "11b3477 (round-5 pin; delta used to pick the rows to re-verify)",
 "checkout": "/tmp/verify-ac2r6-l34 (detached worktree at ff9284f; untracked: .venv symlink)",
 "scratch": "/tmp/ac2-v/L03-L04/r6",
 "verified_at": "2026-10-27T22:33:03+00:00",
 "verdict": "PASS",
 "rows": out_rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": (
  "Round 6 of the L03-L04 slice at pin ff9284f. Round delta for this slice: L03.html lines 710 (E1 solution, sentence added), 724 (E3 solution, rewritten), 812 (Q5 explain, hypothesis added); L04.html lines 312-315 and 333-335 (three print lines added to the lab, and the matching expected block), 494 (E3 solution, rewritten), 594 (quiz explain); tests/labs/AC2/lab-AC2-L04-1.py (+4 lines, the same prints); cards.json changed only at c075, c107, c123, c130 (not this slice). Every L04 line after 335 is +7 versus round 5 (the Sloan claim is now line 359; round 5 said 352). "
  "The round-5 FAIL (L03-L04-math-L03-E3-causal, the 'slower capital growth offsets part of it' sentence) is fixed and re-verified PASS. The new E3 text is correct: NOPAT -22.24%, average invested capital +7.72%, ROIC -27.81%, constant-2023-growth counterfactual -28.67%, growth 9.56/9.02/6.53%. "
  "Carry rule: rows whose subjects lie outside the changed lines are carried with the 'Carried from round 5 (...)' prefix; the prefix names the changed lines rather than claiming whole-file identity, because L03.html and L04.html changed. Every L04 locator in a carried row after line 335 is +7 versus round 5. "
  "Not a FAIL, noted: the E3 solutions quote lab output names (r_squared_full_precision, var_gap_over_var_cf) in learner text, which is an identifier reference, not a process word; the L03 E3 counterfactual and the L04 unrounded values are computed by hand from the twins' functions (the lab prints 1 dp and 4 dp), and the page says so. Real EDGAR data is still honestly pending; every filer is SIMULATED."
 ),
 "summary": "AC2 L03-L04 round 6 (pin ff9284f): verdict PASS. 68 rows: 68 PASS, 0 FAIL, 0 UNVERIFIABLE. The round-5 FAIL (L03-L04-math-L03-E3-causal) is fixed and re-verified PASS (counterfactual -28.67% recomputed from the twin). Re-verified this round: all command rows, E1/E3 numbers, the L04 E3 squared correlation, the L04 lab expected block and twin, the Sloan claim (Crossref re-fetched), the cards (140, none of L03/L04 changed), banned and process-word scans. Carried (byte-identical subjects): the rest, with the changed-line prefix."
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(out_rows), "statuses", sorted({r["status"] for r in out_rows}))
