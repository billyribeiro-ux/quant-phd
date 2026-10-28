import json, pathlib, re
root = pathlib.Path("/tmp/verify22-AC4-d")
prev = json.load(open("/tmp/fanout-frags/AC4-d.round21.json"))
CARRY_PREFIX = ("Carried from round 21 (cited passage byte-identical since the previous pin f95243f; the round-22 "
                "delta touches only L07 lines 56, 100, 122, 333, 374, 378, 387, 422, L08 line 358 and cards c093): ")
def carry_text(ev):
    m = re.match(r"Carried from round \d+ \(.*?\): ", ev)
    rest = ev[m.end():] if m else ev
    return CARRY_PREFIX + rest
RERUN = {
"AC4-d-cmd-pin": "git rev-parse --short HEAD prints d160ac3; git symbolic-ref -q HEAD prints nothing with exit 1 (detached); git status shows only the untracked .venv and this round's ledgers/AC4/scripts/AC4-d-r22/ (scripts/AC4-d-r22/pin.out).",
"AC4-d-r6-delta-coverage": "git diff -U0 f95243f d160ac3 (the round-21 fix commit) for the slice: L07.html new-side lines 56, 100, 122, 333, 374, 378, 387, 422; L08.html line 358; cards.json line 658 (AC4-c093). Every hunk read in full context. L01.html, L02.html, index.html and AC1 files also changed but are outside this slice and were not judged. tests/labs/AC4, project.html and grader/ show no change in this delta (git diff --stat empty).",
"AC4-d-cmd-run_labs": "tools/run_labs.py --unit AC4 (exit 0): 'run_labs AC4: PASS (10/10)' (scripts/AC4-d-r22/run_labs.out).",
"AC4-d-cmd-twin-isolated": "python -I -W error tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py: exit 0, stderr empty (scripts/AC4-d-r22/twin_L07.out, twin_L08.out). The embedded <pre class=expected> block of each page equals the fresh run after html.unescape and strip: L07 True (18 lines), L08 True (19 lines) (scripts/AC4-d-r22/embed_cmp.out).",
"AC4-d-cmd-page_smoke": "tools/page_smoke.py --unit AC4 --pages L07 L08: 'page_smoke modules/AC/AC4/L07.html: PASS', 'page_smoke modules/AC/AC4/L08.html: PASS', 'page_smoke AC4: PASS', exit 0 (scripts/AC4-d-r22/page_smoke.out).",
"AC4-d-cmd-check_pages": "tools/check_pages.py --all (exit 0): 'check_pages AC4: PASS' (scripts/AC4-d-r22/check_pages.out).",
"AC4-d-cmd-check_dag": "tools/check_dag.py --all (exit 0): 'check_dag AC4: PASS' (scripts/AC4-d-r22/check_dag.out).",
"AC4-d-cmd-check_projects": "tools/check_projects.py --all (exit 0): 'check_projects AC4: PASS' (scripts/AC4-d-r22/check_projects.out).",
"AC4-d-cmd-lint-mypy": "ruff check tests/labs/AC4/: 'All checks passed!'; ruff format --check tests/labs/AC4/: '10 files already formatted'; mypy --no-incremental on lab-AC4-L07-1.py and lab-AC4-L08-1.py: 'Success: no issues found in 2 source files' (scripts/AC4-d-r22/ruff_mypy.out).",
"AC4-d-cmd-pytest": "python -m pytest -q -k 'AC4 or ac4' tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py: exit 0, ten dots; collect-only on tests/test_labs.py -k 'AC4 or ac4' gives 10 tests (scripts/AC4-d-r22/pytest_ac4.out, collect.out).",
"AC4-d-cmd-verify_refs": "tools/verify_refs.py --unit AC4: 'live re-verification of AC4: 2 of 560 entries, 0 problems' (exit 0); tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (exit 0) (scripts/AC4-d-r22/vr_live.out, vr_offline.out). The pages cite no registry key.",
"AC4-d-r17-cmd-embed": "Embedded <pre class=expected> of L07.html and L08.html compared with a fresh python -I run of each twin (exact string after html.unescape and strip): both True (scripts/AC4-d-r22/embed_cmp.out, embed_cmp_r22.py).",
"AC4-d-2.2-numbers-L07": "Recomputed this round with exact Fractions (scripts/AC4-d-r22/recompute_r22.out): §4 (lines 128-133) D=3000, t_min=52, Sigma=140000, dS(52)=0, dS(46)=-30000, dB(52)=140000; line 134 K=12000 gives D=1000, t_min=44, Sigma=180000 (M2); M3 r=50 gives t_min 52 > 50 and Sigma=-10000; misconception 1 (line 343) full cost 46: dS=-30000, 46<52; misconception 2 (line 345) D=0, t_min=40, dB(60)=-10000, Sigma=30000. Lab 1 counts 14, 75, 112, 73 and the shares 75/187=0.4011 (line 387) and 73/112=0.6518 (line 327) match the embedded output (twin_L07.out). The changed P2 and P3 statements have their own rows.",
"AC4-d-2.2-numbers-L08": "Recomputed (scripts/AC4-d-r22/recompute_r22.out): §4 RI 30, EVA 6, Lemma 8.2 check -24 = -0.20 x 120, capitalized dRI 72.8 and dEVA 56.8; M3 RI 66.4, EVA 34.4, dRI 36.4, dEVA 28.4; §6 SIM-G 0.20 x 13680 = 2736 and 2250 - 2736 = -486; §6 SIM-A 8000 - 720 = 7280 and 0.8 x 8000 - 720 = 5680; E1 (line 358) 4/28 = 0.1429 (1/7 = 0.1429). Printed 7280.00 and 5680.00 cents equal 72.80 and 56.80 SCU (twin_L08.out).",
"AC4-d-2.2-numbers-L07-E1-seed": "Subject changed: line 387 no longer lists the seeds 1 to 40 sentence. Re-verified: seed scan of the L07 generator over seeds 1 to 40 (scripts/AC4-d-r22/seed_scan_r22.py, seed_scan_r22.out) gives empty-range counts from 59 to 86 against 75 for the shipped seed 20261027, so 'a different seed could give a different share' is supported.",
"AC4-d-L08-E1-seed-claim": "Subject changed: line 358 no longer lists seeds 14, 20, 26 and 28. Re-verified: seed scan of the L08 generator over seeds 1 to 40 (scripts/AC4-d-r22/seed_scan_r22.out) gives discordant counts 0 to 9 against 4 for the shipped seed, so 'a different seed could change it' is supported; the remaining sentence 'the count shows that the two orders can disagree on this input, not how often they disagree' is true of a count of 4 of 28.",
"AC4-d-2.3-grades-L07": "Re-verified after the round-22 edit: §9 key-results table (lines 416-427). Row 4 (line 422) now reads 'when q > 0, q <= K, E <= K and p_m >= v' and is T, citing P2 (line 374) whose statement has the same hypotheses; every C row names Lab 1 and an output line that exists (lines 314, 316, 317, 321; twin_L07.out).",
"AC4-d-2.4-notation": "Re-verified: notation/notation.json, references/ and tools/ unchanged since fd9a9b7 (git diff --stat empty for them). The round-22 text uses only symbols already on the page (q, K, E, p_m, v, r, D, t_min, Sigma); no new symbol.",
"AC4-d-2.8-data": "grep -c data-files on L07.html and L08.html: 0 and 0 (re-run this round).",
"AC4-d-2.9-prose-banned": "Re-run this round on both pages (tags stripped; case-insensitive): roughly, 'about <digit>', historically, typically, usually, generally, ellipsis characters and three dots, builder, verifier, round, build, request, unit report. The only matches are code tokens ROUND_HALF_UP and Decimal rounding in the lab code (L07 lines 157 and 249; L08 lines 154 and 222 of the stripped text). No match in learner prose.",
"AC4-d-r17-process-words": "Same grep re-run this round for build, builder, round, verifier, REQUEST and unit report: zero hits in learner text of L07.html and L08.html; the only 'round' matches are the code token ROUND_HALF_UP.",
"AC4-d-r17-cards-scope": "Re-verified this round: all 35 L07 and L08 cards (scripts/AC4-d-r22/cards_L07_L08.txt) read against the current lesson text. The failing card AC4-c093 now states 'Since q > 0, q <= K, E <= K and p_m >= v, the floor t_min is at most p_m (Problem P2)', which matches P2 at line 374. The other cards cite lines and theorems that are unchanged in this delta.",
"AC4-d-r21-P2-scope-q-le-K": "Re-verified: L07.html line 374 P2 statement is now 'Using q > 0, q <= K, E <= K and p_m >= v, prove that t_min <= p_m'; key-results row 4 (line 422) matches. t_min and D are defined on this page only under q <= K (line 76 'Assume q <= K'; Lemma 7.2 at line 91 'Let q > 0 and q <= K'). The proof (line 376) uses q > 0, E <= K and p_m >= v, so q <= K is a stated, harmless extra hypothesis. PASS.",
"AC4-d-r21-c093-hypothesis": "Re-verified: cards.json line 658 back is 'No. Since q > 0, q <= K, E <= K and p_m >= v, the floor t_min is at most p_m (Problem P2).' It matches the P2 hypotheses (line 374). PASS.",
"AC4-d-L07-opportunity-cost-def": "Subject changed (line 100). The sentence 'Under the hypotheses of Lemma 7.2, E <= K gives D <= q, so with p_m >= v the lowest price never exceeds p_m (P2).' attributes E <= K to the hypotheses of Lemma 7.2. Lemma 7.2 (line 91) states only 'Let q > 0 and q <= K'; E <= K is a §1 input (line 61), not a Lemma 7.2 hypothesis. The arithmetic is right (D <= q for E <= K, q >= 0; checked on a grid of 34944 cases with 0 violations, recompute_r22.out), so only the attribution is wrong. The definition sentence on line 100 (opportunity cost per internal unit, averaged over q; D = 0 gives t_min = v; D = q gives t_min = p_m) is unchanged and correct. Other part of the row: §1 line 72 and §2 line 98 unchanged, carried.",
"AC4-d-r18-L07-midpoint-test-point": "Re-verified: midpoint() (line 82-84) is (t_min + t_max)/2; the sum identity is checked at (t_min, t_max, midpoint) (lines 149-156); the printed line (line 160) matches. One mutant with midpoint() returning t_min (ledgers/AC4/mutants/AC4-d-r20/m20_L07_midpoint_check_uses_lower_end.py) gives identical output, see AC4-d-r22-midpoint-survivor (equivalent on the shipped seed, PASS).",
"AC4-d-2.5-lab-L07": "Lab 1 hypothesis (line 140), §4 lead-in (line 136) and interpretation (line 322) re-read against the twin: the hypothesis (supplier gain zero at t_min; range nonempty exactly when Sigma >= 0; sum identity at both ends and the midpoint; boundary tested at equality) matches what the twin computes (lines 146-160 and the boundary case). Subject lines are unchanged in this delta, so the round-21 result stands. The count-based checks are discussed in AC4-d-r22-check-removal.",
"AC4-d-r3-L07-s1-s5-s6-text": "Re-verified: §1 line 70 and §5 line 327 unchanged; §6 bullet 'The outside sale must be available' (line 333) changed and now reads 'In the model, unavailability is E = 0, which gives D = 0 (since q <= K) and t_min = v.' Checked: E is the units sold outside (line 61), D = max(0, q + E - K) (line 78); with E = 0 and q <= K, D = max(0, q - K) = 0, so t_min = v. Other §6 bullets (332, 334, 335) unchanged. 201 = 200 + 1, 14 with q > K, 187 = 75 + 112, 73/112 = 0.6518 recomputed.",
"AC4-d-r17-mutants-killed": "Re-run this round by transplant of each mutant's changed line onto the current twins (scripts/AC4-d-r22/transplant_lines_r22.py, transplant_lines_r22.out): all 34 round-21 transplant mutants KILLED (output differs or exit 1), including the r17 L07 m02, m05 and the r18 n02 and m19_L07_t_min_divides_by_capacity lines that round 21 did not show. Equivalent on the shipped seed (identical output): r17_L08_m04 and L08_n09 (ledgers/AC4/mutants/AC4-d-r17, AC4-d-r18; see AC4-d-r17-mutant-L08-m04-ties). Superseded full-file copies of an older twin are not counted as kills (see notes).",
"AC4-d-r17-mutant-L08-m04-ties": "Re-run: the one-line transplant of r17_L08_m04 (drops 'and by_ri != 0 and by_ratio != 0' from the discordant test) gives output identical to the shipped twin (exit 0, scripts/AC4-d-r22/transplant_r22.out and the hand-transplant lines). Equivalent on the shipped seed, consistent with the 0 ties among the 28 pairs (the ties check in AC4-d-r19/ties_check.out).",
"AC4-d-r18-equiv-L08-n09": "Re-run: the L08_n09 one-line change (same discordant test without the tie exclusion) gives identical output (scripts/AC4-d-r22/transplant_r22.out); equivalent on the shipped seed.",
"AC4-d-r18-mutants-run": "Re-run this round (scripts/AC4-d-r22/transplant_lines_r22.out): the transplantable round-18 mutants n01, n02, n04, n05, n06, n09 and L08_n01 to n06, n08 are KILLED. L08_n07 was killed by rebasing (round 21). n03, n07, n08, n10, n11, n12, boundary_strict_only and del_* are superseded (their target lines are absent from the current twin) and are not counted.",
"AC4-d-r18-L08-mutants-killed": "Re-run this round: L08_n01 to n06 and n08 KILLED by transplant of the changed line (transplant_lines_r22.out). L08_n07 killed after rebasing its changed line (round 21, AC4-d-r21 transplant) and not re-run this round.",
"AC4-d-r17-prose-scope-words": "Carried from round 21 (lines 322 and 347 byte-identical since the previous pin f95243f; line 322 and line 347 are not in the round-22 delta): line 322 'excluded from every check line' and line 347 'holds for every t, by the computation in §3 and P1 (Theorem 7.3 part 3 states it for t in the range)' unchanged. P1 (line 372) gives the identity for every t, so the sentence is supported.",
"AC4-d-r3-L08-why-and-s3-s5": "Carried from round 21 (cited L08 passages byte-identical since the previous pin f95243f; L08 line 358 is the only changed L08 line and is not cited here): why-it-matters (line 52), §1 (line 78), §3 (lines 98-109), §5 (lines 126-130) unchanged.",
}
PASS_NEW = []
NEW_ROWS = [
 {"id": "AC4-d-r22-delta-hunks", "check": "2.9-structure", "location": "git diff -U0 f95243f d160ac3 for L07.html, L08.html, cards.json (slice lines only)",
  "status": "PASS", "evidence": "Every changed line read in full context: L07 line 56 ('with the following inputs, stated as given': the word 'all' removed; no content change, PASS); line 100 (see AC4-d-L07-opportunity-cost-def, FAIL); line 122 (see AC4-d-r22-L07-l122-theorem-scope, PASS); line 333 (see r3-L07-s1-s5-s6-text, PASS); line 374 (P2, see AC4-d-r22-P2-statement, PASS); line 378 (P3, see AC4-d-r22-P3-statement, PASS); line 387 (E1, see AC4-d-2.2-numbers-L07-E1-seed, PASS); line 422 (key row 4, see AC4-d-2.3-grades-L07, PASS); L08 line 358 (E1, see AC4-d-L08-E1-seed-claim, PASS); cards.json line 658 (c093, see AC4-d-r21-c093-hypothesis, PASS)."},
 {"id": "AC4-d-r22-P2-statement", "check": "2.4-math", "location": "course/modules/AC/AC4/L07.html P2 statement and proof (lines 373-376)",
  "status": "PASS", "evidence": "Proof (line 376): E <= K gives q + E - K <= q, so D = max(0, q + E - K) <= q (q >= 0); with p_m - v >= 0, D(p_m - v) <= q(p_m - v); dividing by q > 0 gives t_min <= p_m. Checked on a grid (q <= K, E <= K, 0 <= v, p_m >= v; 34944 cases) with 0 violations (scripts/AC4-d-r22/recompute_r22.out)."},
 {"id": "AC4-d-r22-P3-statement", "check": "2.4-math", "location": "course/modules/AC/AC4/L07.html P3 (lines 377-380)",
  "status": "PASS", "evidence": "With v = 0 and 0 < q <= K, Lemma 7.2 gives t_min = D p_m / q; the range is nonempty iff t_min <= r iff D p_m <= q r (q > 0), which is Sigma >= 0 with v = 0 (Sigma = q r - D p_m). Grid of 52800 cases (K <= 9, E <= K, p_m < 8, r < 20): 0 violations (recompute_r22.out)."},
 {"id": "AC4-d-r22-L07-l122-theorem-scope", "check": "2.4-math", "location": "course/modules/AC/AC4/L07.html §3 paragraph after Theorem 7.3 (line 122)",
  "status": "PASS", "evidence": "New sentence: 'By Theorem 7.3 part 2, a sale with Sigma >= 0 leaves a nonempty range of prices that both divisions accept.' Theorem 7.3 part 2 (line 115) says the range is nonempty iff Sigma >= 0 under the theorem's hypotheses (q > 0, q <= K, E <= K, p_m >= v, line 112), which are the §1 inputs and the case the page treats as a sale (line 76: if q > K no transfer is possible). The claim is within the theorem's scope."},
 {"id": "AC4-d-r22-L07-l333-unavailability", "check": "2.4-math", "location": "course/modules/AC/AC4/L07.html §6 bullet (line 333)",
  "status": "PASS", "evidence": "'In the model, unavailability is E = 0, which gives D = 0 (since q <= K) and t_min = v.' E is the units S sells outside (line 61); D = E - min(E, K - q) = max(0, q + E - K) (line 78). With E = 0 and q <= K, D = max(0, q - K) = 0 and t_min = v (line 54 of the lab twin and Lemma 7.2). Arithmetic verified in recompute_r22.out."},
 {"id": "AC4-d-r22-cards-c093-text", "check": "2.7-cards", "location": "course/modules/AC/AC4/cards.json AC4-c093 back (line 658)",
  "status": "PASS", "evidence": "Card text matches P2 hypotheses; the question 'Can the lowest transfer price exceed the outside market price?' is answered 'No' under those hypotheses, which the card states. Covered also by AC4-d-r21-c093-hypothesis and AC4-d-r17-cards-scope."},
 {"id": "AC4-d-r22-check-removal", "check": "2.5-labs", "location": "tests/labs/AC4/lab-AC4-L07-1.py lines 146-160; lab-AC4-L08-1.py lines 102-106; scripts/AC4-d-r22/check_removal_r22.out",
  "status": "PASS", "evidence": "Six mutants that replace a counted check by its shipped value (supplier_zero, sign_match, midpoint_inside, sum_identity in L07; gap_ok, sign_ok in L08) exit 0 with identical output. These are equivalent on the shipped seed: each check holds for every case, so a passing check and a removed check print the same count. The architect ruling makes lab survivors out of scope; the lesson's 'checks' wording (L07 line 136, L08 line 134) describes counts the shipped code computes and prints, which the twin does compute (verified by the twin output and the code). Out of scope, recorded for the orchestrator: a printed count cannot detect a removed check on a seed where the check holds."},
 {"id": "AC4-d-r22-midpoint-survivor", "check": "2.5-labs", "location": "ledgers/AC4/mutants/AC4-d-r20/m20_L07_midpoint_check_uses_lower_end.py (midpoint() returns t_min); tests/labs/AC4/lab-AC4-L07-1.py line 82-84, 154",
  "status": "PASS", "evidence": "Mutant exits 0 with output identical to the shipped twin (scripts/AC4-d-r22/mutants_r22.out). The shipped twin computes midpoint as (t_min + t_max)/2 and checks the sum identity there (lines 82-84, 154); the mutant changes the midpoint to t_min, where the identity also holds, so the printed count is unchanged on the shipped seed. Equivalent on the shipped seed; out of scope under the architect ruling (lab twins are not mutation-tested). The lesson's claim that the lab checks the midpoint (L07 line 140) is true of the shipped code."},
]
FIXED_STATUS = {}
rows_out = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
    elif rid in ("AC4-d-L07-opportunity-cost-def",):
        rows_out.append({"id": rid, "check": "2.4-math", "location": r["location"], "status": "FAIL",
                         "evidence": RERUN[rid],
                         "fix": "Replace 'Under the hypotheses of Lemma 7.2, E <= K gives D <= q' with 'With q > 0 and q <= K (Lemma 7.2) and E <= K (§1), D <= q, so with p_m >= v the lowest price never exceeds p_m (P2).'"})
    elif rid == "AC4-d-r17-cards-scope":
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
    elif rid in ("AC4-d-r21-P2-scope-q-le-K", "AC4-d-r21-c093-hypothesis"):
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
    elif rid in RERUN:
        pass
    else:
        if rid in ("AC4-d-r18-L07-midpoint-test-point", "AC4-d-2.5-lab-L07", "AC4-d-r17-prose-scope-words", "AC4-d-r3-L08-why-and-s3-s5"):
            rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
        else:
            rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"], "evidence": carry_text(r["evidence"])})

# post-loop overrides
RERUN["AC4-d-r18-L07-E1-wording"] = ("Subject changed (line 387: the sentence about seeds 1 to 40 and 186 pairs was removed). Re-verified this round: "
    "'The output gives 75 empty ranges among 187 pairs with q <= K' (twin_L07.out: 'cases with q <= K and an empty range: 75', feasible 112, 187 total); "
    "75/187 = 0.4011 (recompute_r22.out); 'the boundary pair is not empty, since its lowest and highest prices are equal' (boundary: t_min = t_max = 5200.00, nonempty True); "
    "'describes the generator's settings ... a different seed could give a different share' (seed_scan_r22.out).")
for i, r in enumerate(rows_out):
    if r["id"] == "AC4-d-r18-L07-E1-wording":
        rows_out[i] = {"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN["AC4-d-r18-L07-E1-wording"]}
    if r["id"] == "AC4-d-L07-opportunity-cost-def":
        rows_out[i]["status"] = "FAIL"
        rows_out[i]["fix"] = ("Replace 'Under the hypotheses of Lemma 7.2, E <= K gives D <= q, so with p_m >= v the lowest price never exceeds p_m (P2).' "
                              "with 'With q > 0 and q <= K (Lemma 7.2) and E <= K (§1), D <= q, so with p_m >= v the lowest price never exceeds p_m (P2).'")
        rows_out[i]["evidence"] = RERUN["AC4-d-L07-opportunity-cost-def"]
        rows_out[i]["location"] = "course/modules/AC/AC4/L07.html §2 paragraph after the Lemma 7.2 proof (line 100)"
rows_out.extend(NEW_ROWS)

mutants = []
ids_killed = [m["id"] for m in prev["mutants"]]
for m in prev["mutants"]:
    mutants.append({"id": m["id"], "description": m["description"], "file": m.get("file", ""),
                    "killed_by": "round 22 transplant of the mutant's changed line onto the current twin (scripts/AC4-d-r22/transplant_lines_r22.out): KILLED"})
for name, src in [("AC4-d-r20/m20_L07_displaced_forgets_internal_order.py", "r20"), ("AC4-d-r20/m20_L07_sign_check_strict_at_zero.py", "r20"),
                  ("AC4-d-r20/m20_L08_eva_taxes_residual_income.py", "r20")]:
    mutants.append({"id": "r20:" + name.split("/")[1], "description": "round-20 lab-twin mutant " + name.split("/")[1] + " (2-3 changed lines against the current twin)",
                    "file": "ledgers/AC4/mutants/" + name, "killed_by": "full-file run against the current twin (scripts/AC4-d-r22/mutants_r22.out): exit 0 and output differs: KILLED"})

counts = {}
for r in rows_out:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment = {
 "unit": "AC4", "slice": "AC4-d", "round": 22,
 "verifier": "round-22 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
 "pin": "d160ac3",
 "base": "f95243f (round-21 pin; /tmp/fanout-frags/AC4-d.round21.json used as context; its PASS rows re-verified or carried only where the cited passage is byte-identical to f95243f)",
 "checkout": "/tmp/verify22-AC4-d (detached worktree at d160ac3, .venv symlink)",
 "scratch": "/tmp/AC4-d-v22 (scratch); command outputs and scripts in ledgers/AC4/scripts/AC4-d-r22/",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows_out,
 "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta f95243f..d160ac3 for the slice: L07.html lines 56, 100, 122, 333, 374, 378, 387, 422; L08.html line 358; cards.json line 658 (AC4-c093). L01/L02/index.html and AC1 files changed too and are outside this slice (not judged).",
  "FAIL row: AC4-d-L07-opportunity-cost-def (line 100 attributes E <= K to the hypotheses of Lemma 7.2). Every other previous FAIL row (AC4-d-r21-P2-scope-q-le-K, AC4-d-r21-c093-hypothesis, AC4-d-r17-cards-scope) is fixed and re-verified PASS.",
  "Lesson slice, not a project slice: the at-least-3 new student-error mutant rule does not apply; no new mutants were written. All earlier lab-twin mutants were re-run: 34 round-21 transplants (all KILLED), 3 round-20 full files (KILLED), and the round-20 survivor m20_L07_midpoint_check_uses_lower_end (equivalent on the shipped seed, PASS row AC4-d-r22-midpoint-survivor). Superseded full-file copies of an older twin (r17 L07 m03, L08 m02, r18 n03, n07, n08, n10-n12, boundary_strict_only, del_*) differ from the current twin in many lines; their full-file outputs are not counted as kills. r17 L07 m03 and L08 m02 are the same mutations as r18_carry_L07_nonempty_strict and r17_carry_L08_ratio_ge_strict (killed).",
  "Equivalent on the shipped seed (identical output, PASS, not in the mutants list): r17_L08_m04_discord_ignores_ties and L08_n09_discord_pairs_same_name_order.",
  "Check-removal survivors (six; AC4-d-r22-check-removal): replacing a printed count's check by its shipped value leaves the output identical. Recorded as out of scope; flagged to the orchestrator as a limit of count-based lab checks (a removed passing check cannot change a printed count).",
  "Alternative correct implementations: not rerun this round (the twins are unchanged since fd9a9b7, git diff --stat fd9a9b7 d160ac3 for tests/labs/AC4 is empty); the round-19 and round-20 alternatives are carried.",
  "Hours: L07 6 and L08 6 (data-hours line 2); hub 50 + 20 unchanged in this delta; hours not judged on pace (architect ruling).",
  "Project grader and project.html: unchanged since fd9a9b7 (no AC4 grader file in the delta), so the round-20 mutate_graders run is carried.",
  "Not checked: live verify_refs beyond the unit run (no network use beyond the tool's own run); Pyodide timing beyond page_smoke; the round-20 seed scans were re-run this round for L07 and L08 (seed_scan_r22.out)."
 ],
 "summary": {"rows": len(rows_out), **{k.lower(): v for k, v in counts.items()}, "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m.get("killed_by") and "KILLED" in m["killed_by"])},
}
out = root / "ledgers/AC4/AC4-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows_out), counts, "mutants", len(mutants))
