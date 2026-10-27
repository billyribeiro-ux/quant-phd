"""Build the round-5 fragment for slice L05-L06 from the round-4 rows plus this round's re-verification."""
import json
import sys

sys.path.insert(0, "/tmp/verify-ac2r5-l56/tools")
import ledger  # noqa: E402

R4 = "/tmp/ac2-frags/L05-L06.round4.json"
OUT = "/tmp/verify-ac2r5-l56/ledgers/AC2/L05-L06.json"
CARRY = "Carried from round 4 ({loc} byte-identical since 2607c60; no delta hunk touches it): "

# Re-verified this round: id -> (status, evidence, fix)
RERUN = {
    "L05-L06-cmd-pin": ("PASS", "git rev-parse --short HEAD = 11b3477 (round-5 pin); git status: only untracked .venv. Delta 2607c60..HEAD for the slice: L05.html 3 hunks (lines 240, 327, 334), L06.html 5 hunks (lines 345, 350, 359, 457, 465), cards.json 8 records (c058, c064, c103, c107, c119, c123, c130, c134; c058, c103, c107, c119, c130, c134 are outside this slice). Lab twins and references.json and notation.json unchanged (git diff --quiet rc 0).", ""),
    "L05-L06-cmd-check-pages": ("PASS", "tools/check_pages.py --unit AC2 --page L05 -> 'check_pages AC2 L05: PASS' (rc 0); --page L06 -> 'check_pages AC2 L06: PASS' (rc 0). /tmp/ac2-v/L05-L06-r5/check_pages.txt.", ""),
    "L05-L06-cmd-check-dag": ("PASS", "tools/check_dag.py --unit AC2 -> 'check_dag AC2: PASS' (rc 0). /tmp/ac2-v/L05-L06-r5/check_dag.txt.", ""),
    "L05-L06-cmd-run-labs": ("PASS", "tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)' (rc 0). /tmp/ac2-v/L05-L06-r5/run_labs.txt. pytest for the AC2 labs in L05-L06-cmd-lint.", ""),
    "L05-L06-cmd-twins-isolated": ("PASS", "python -I -W error tests/labs/AC2/lab-AC2-L05-1.py rc 0 (16 lines, lab05.out) and lab-AC2-L06-1.py rc 0 (39 lines, lab06.out). scripts/cmp_pre.py (run with -I): each output equals the expected <pre> block of its page line for line: L05 16/16 IDENTICAL, L06 39/39 IDENTICAL.", ""),
    "L05-L06-cmd-page-smoke": ("PASS", "tools/page_smoke.py --unit AC2 --pages L05 L06 -> 'page_smoke modules/AC/AC2/L05.html: PASS', 'page_smoke modules/AC/AC2/L06.html: PASS', 'page_smoke AC2: PASS' (rc 0); lab-AC2-L06-1 0.1 s. /tmp/ac2-v/L05-L06-r5/page_smoke.txt.", ""),
    "L05-L06-cmd-verify-refs-unit": ("PASS", "tools/verify_refs.py --unit AC2 -> 'live re-verification of AC2: 7 of 560 entries, 0 problems' (rc 0). /tmp/ac2-v/L05-L06-r5/verify_refs_live.txt.", ""),
    "L05-L06-cmd-verify-refs-offline": ("PASS", "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (rc 0). /tmp/ac2-v/L05-L06-r5/verify_refs_offline.txt.", ""),
    "L05-L06-cmd-lint": ("PASS", "ruff check on both twins: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'; pytest tests/test_labs.py -k AC2: 11 passed. /tmp/ac2-v/L05-L06-r5/lint_pytest.txt.", ""),
    "L05-L06-cit-sloan-registry": ("PASS", "references/references.json unchanged since 2607c60 (git diff --quiet rc 0); key sloan1996stock, DOI 10.2308/tar-9608042309. Crossref api.crossref.org/works/10.2308/tar-9608042309 re-fetched with plain curl this round: HTTP 200 (cr_sloan.json): title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', Accounting Review 71(3) 289-315, 1996-07. Matches the registry DOI and title.", ""),
    "L05-L06-cit-sloan-claim-s1": ("PASS", "L05.html line 61 claim span (grade C, data-cite sloan1996stock), unchanged this round: 'Sloan (1996) investigates whether stock prices reflect information about future earnings contained in the accrual and cash-flow components of current earnings.' Crossref abstract (HTTP 200 this round): 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components of currents earnings.' The claim restates the question and names no finding.", ""),
    "L05-L06-cit-dechow-registry": ("PASS", "references.json unchanged; dechow1995detecting DOI 10.2308/tar-9505096112. Crossref (HTTP 200, re-fetched this round, cr_dechow.json): title 'Detecting Earnings Management.', The Accounting Review 70(2) 193-225, 1995-04. Page citation 'The Accounting Review 70(2), 1995' matches.", ""),
    "L05-L06-cit-dechow-scope": ("PASS", "L06.html line 61 claim span and §5 bullet 1 and §8 row 6 read this round. Crossref abstract (this round): 'Evaluates alternative accrual-based models for detecting earnings management. Comparison of the specification and power of commonly used test statistics; ...'. Claim matches; no power figure quoted.", ""),
    "L05-L06-cit-dechow-authors": ("PASS", "Ruling (1) applied. grep -c 'Dechow' (case-sensitive) = 0 in L05.html, L06.html and cards.json: authored prose names the key and the title only. Crossref (this round) lists Patricia M. Dechow and Richard G. Sloan; the author question is not resolved here.", ""),
    "L05-L06-num-L05-lab": ("PASS", "Lab 1 of L05 re-run (python -I -W error, rc 0): 16 of 16 lines identical to the page's expected block (scripts/cmp_pre.py). Interpretation figures unchanged this round; the E2 and E3 figures are re-derived under their own rows.", ""),
    "L05-L06-num-L05-derived": ("PASS", "recompute_r5.out: E2 with displayed SD 0.01131 -> 2.1647; with 0.011314 -> 2.1640; with exact SD 0.0113137 -> 2.1640; the lab's 2.164 uses the unrounded simulated gap (lab source: planted_exact = BETA x mean gap). E3 (0.00075 - 0.00223)/0.0010328 = -1.4330 (page: -1.433); with displayed SE 0.00103 -> -1.4369 (page: -1.44). Sweep distances from -2.7996: 0.0559, 0.0268, 0.0084, 0.0005. Figures attributed correctly now; the 'unrounded' label defect is a separate row (L05-L06-r5-unrounded-sd-label).", ""),
    "L05-L06-num-L06-lab": ("PASS", "Lab 1 of L06 re-run (rc 0): 39 of 39 lines identical to the page block. Interpretation figures recomputed: 0.3891 - 0.1806 = 0.2085 printed, 0.2084 unrounded; 0.2084/0.2824 = 0.738; TPR 197/200 = 0.985, FPR 3/1800 = 0.0017; weak TPR 71/200 = 0.355, FPR 129/1800 = 0.0717; flags_only 6/6, differing 12.", ""),
    "L05-L06-num-L06-derived": ("PASS", "recompute_r5.out: 0.2824/0.05 = 5.648 -> 5.6; 0.2781 sqrt(1800/57600) = 0.04916 -> 0.0492; 1800 (0.2781/0.05)^2 = 55,685 (page 55,700) and /0.9 = 61,872 (page 61,900); z = 0.003076/0.001467 = 2.0968 -> 2.097 displayed (page E3 now writes 2.097 and the lab's 2.096 as unrounded). Cause sentence of the E3 tail is a separate row.", ""),
    "L05-L06-num-L06-roughly-4pct": ("PASS", "Tails: 2(1 - Phi(2.096)) = 0.0361 (lab two_sided_tail_a2 0.036) and 2(1 - Phi(2.067)) = 0.0387 (rounded inputs); both 'about 4%' with the calculation shown. The attribution of the 2.067 case is a separate FAIL row (L05-L06-r5-L06-E3-cause).", ""),
    "L05-L06-lab-L05-1-run": ("PASS", "Lab 1 of L05 re-run: expected block identical to the output (16/16, scripts/cmp_pre.py); sweep is 20 seeds per firm count (lab source SWEEP_SEEDS = 20).", ""),
    "L05-L06-lab-L06-1-run": ("PASS", "Lab 1 of L06 re-run (rc 0): identical to the expected block (39/39). Docstring: SIMULATED, one draw at seed 606.", ""),
    "L05-L06-lab-L06-1-overreach-sample": ("PASS", "§4 paragraph (line 350) re-read this round: the sentence 'At that sample size the estimate of a1 is too imprecise to recover the planted value' is removed; the remaining claims (0.2824 at seed 606, 5.6 times the planted 0.05, se_scaling 0.0489 on 57,600 rows) match the lab output. 'The lab says nothing about real firms' unchanged.", ""),
    "L05-L06-lab-L06-1-flag-count": ("PASS", "lab06.out: strong flags_differing 0; weak flags_only_all_firms 6, flags_only_oracle 6, flags_differing 12. Page: '12 of the 200 flags differ' and 'six enter, six leave' match.", ""),
    "L05-L06-card-L05-sloan": ("PASS", "AC2-c064 (grade C, basis 'Crossref abstract; passage locator not confirmed', added this round): front and back match L05.html line 61 claim span and the Crossref abstract; the back quotes no sample period, return level or spread.", ""),
    "L05-L06-card-L06-lab": ("PASS", "AC2-c083 re-verified: 0.2084 = 0.1425 + 0.1965 - 0.1306; 0.2084/0.2824 = 0.738. AC2-c125 re-verified: 0.2781 and 0.0489; 0.2781 sqrt(1800/57600) = 0.0492 vs 0.0489, 'roughly as the square root'. AC2-c082, c085, c086 carried from round 4 (records byte-identical since 2607c60).", ""),
    "L05-L06-card-L06-only-when": ("PASS", "AC2-c084 re-verified: precision 0.355 = 71/200 (flagged count 200, so precision equals TPR); 'most flags are not manipulators' holds (129 of 200).", ""),
    "L05-L06-card-L06-12of200": ("PASS", "AC2-c124 re-verified against lab06.out: flags_only_all_firms 6 (enter under all-firm), flags_only_oracle 6 (leave), rates equal under both (0.355 and 0.0717).", ""),
    "L05-L06-cards-dup-scan": ("PASS", "cards.json (this round): 140 records; ids equal AC2-c001..AC2-c140 in order (python check); no duplicate id. L05 cards c063-c075, c122, c123; L06 cards c076-c088, c124, c125, c128, c138.", ""),
    "L05-L06-struct-banned": ("PASS", "grep -i over L05.html and L06.html visible text for 'roughly half', 'about 6%', 'historically', '...': no hits. 'about' and 'roughly' occur only where a calculation is shown (E3 tails, R1 firm-years).", ""),
    "L05-L06-honest-data": ("PASS", "L05.html 'Honest pending' (line 240) re-read: 'The open items are listed in plans/AC2-open-items.md' (file exists; L05 cites it once, L06 zero times). BLUEPRINT.md §5.3 (line 290) 'Checked and not cleared' lists the Kenneth French Data Library (line 304). SEC company-facts reuse statement 'not yet confirmed' is stated as a limit, not a result.", ""),
    "L05-L06-r2-math-E2-zgap-cause": ("PASS", "L05.html E2 (line 327) re-read: the sweep values -2.7437, -2.7728, -2.7912, -2.7991 are printed by the lab; distances from -2.7996 recomputed 0.0559, 0.0268, 0.0084, 0.0005; 'consistent with' and 'do not establish the rate' are hedged; the 0.0025 gap between 200- and 20-seed means at 500 firms (-2.7937 vs -2.7912) is seed-to-seed (20 seeds are a subset of 200).", ""),
    "L05-L06-r2-num-L06-se-basis": ("PASS", "L06.html §4 (line 350) and R1 (line 465-468) re-read: the 0.2824 basis is the seed-606 non-manipulator SE of a1 (lab output se_non_manipulators 0.2824); 0.2781 is the five-seed mean at 2,000 firm-years; both are labelled as such.", ""),
    "L05-L06-r2-lab-contamination-prop33": ("PASS", "L06.html Lab 1 interpretation (line 345) re-read: decomposition 0.1425 + 0.1965 - 0.1306 = 0.2084 (lab a1_* lines); conditional-mean prediction 0.6223 (lab a1_conditional_mean_prediction); the paragraph says the 0.2084 is not the bias alone, consistent with Proposition 3.3's conditional-mean statement.", ""),
    "L05-L06-r2-prose-s4-lab-bears": ("PASS", "L06.html §4 opening sentence ('The lab bears on the second and third.') unchanged this round. Lab 1 bears on the sample (non-manipulator estimate, lab output) and on the scale (se_scaling output, 2,000 and 64,000 firm-years), as the sentence says.", ""),
    "L05-L06-r2-attribution-sweep": ("PASS", "grep -n Sloan L05.html (this round): line 61 claim span (grade C, sloan1996stock); line 111 lab docstring ('does not reproduce Sloan (1996)'); line 217 interpretation (same); line 222 the question Sloan asks (§3, the question only); line 246 a labelled misconception ('Lab 1 reproduces Sloan's result.', class wrong). Dechow: case-sensitive count 0 in authored prose; L05/L06 cite it only by data-cite key. McLean and Hou appear only as claim-span keys (L05 lines 232-233). No finding is attributed to Sloan or Dechow in learner text.", ""),
    "L05-L06-r3-num-L05-E2-printed": ("PASS", "E2 (line 327) re-derived: 0.0022350 = 0.0008 x 2.7937; 0.08 x sqrt(2/100) = 0.0113137 (page: 0.01131 displayed); lab prints spread_sd_theory 0.01131 and expected_t_at_planted 2.164 (lab source uses unrounded planted and SD). Printed values match; the 'unrounded' label is the separate FAIL row.", ""),
    "L05-L06-r3-num-L05-E3": ("PASS", "E3 (line 334): -1.433 (unrounded inputs, lab seed0_distance_in_se); -1.433 with rounded seed-0 mean and planted spread and SE 0.0010328; -1.4369 with displayed SE 0.00103 (-1.44). Attribution of -1.44 now to the displayed SE is correct. The 'unrounded SD 0.011314' label is the separate FAIL row.", ""),
    "L05-L06-r3-num-L06-decomp": ("PASS", "Lab 1 interpretation (line 345): 0.1425 + 0.1965 - 0.1306 = 0.2084; 0.3891 - 0.1806 = 0.2085 printed; residual 0.000000 (lab a1_decomposition_residual). Recomputed this round.", ""),
    "L05-L06-r3-num-L06-cond-mean": ("PASS", "Lab 1 interpretation: 0.6223 = lab a1_conditional_mean_prediction (strong); E[d|X] = 0.005 = SHIFT x MANIP_SHARE (lab source). Recomputed/printed value matches.", ""),
    "L05-L06-r3-num-L06-se-scaling": ("PASS", "§4 and R1 (lines 350, 465-468): 0.2781 (2,000 firm-years, 1,800 rows) and 0.0489 (64,000 firm-years, 57,600 rows), five seeds 606-610 (lab se_scaling lines). Square-root rule 0.0492 recomputed.", ""),
    "L05-L06-r3-num-L06-a2z": ("PASS", "Interpretation (line 345): z 2.096 from the lab's unrounded inputs (z_a2 2.096), '2.10 standard errors' = 2.096 to two decimals; 2.097 from displayed digits (0.003076/0.001467). Both figures recomputed this round.", ""),
    "L05-L06-r3-prose-L06-imprecise": ("PASS", "The sentence 'At that sample size the estimate of a1 is too imprecise to recover the planted value' is removed from §4 (line 350), so the round-3 concern no longer has a subject; the replacement sentences carry only lab numbers.", ""),
    "L05-L06-r3-cards-c083-c087-c124-c125": ("PASS", "AC2-c083, c087, c124, c125 re-read against lab output and the lesson: c083 (0.738), c087 (rationale 'not sourced in the lesson'; the lesson's §2 has no sourced rationale), c124 (6/6, 12), c125 (0.2781, 0.0489) all consistent.", ""),
    "L05-L06-r3-cit-dechow-crossref-abstract": ("PASS", "Crossref abstract re-fetched this round (cr_dechow.json, HTTP 200): 'Evaluates alternative accrual-based models for detecting earnings management. Comparison of the specification and power of commonly used test statistics; ...'. L06.html §8 row 6 and §5 claim span match and quote no power figure.", ""),
    "L05-L06-r3-cmd-validate": ("PASS", "ledger.validate on this round's fragment ledgers/AC2/L05-L06.json returns an empty list (run in the checkout with .venv/bin/python -I; see notes). The round-3 file ledgers/AC2/L05-L06.json is not present in this checkout, so no earlier file is re-validated.", ""),
    "L05-L06-r3-prose-L06-s5-bullet": ("PASS", "L06.html §5 bullet 2 (line 359) re-read: the 'manipulation through reserves or capitalised costs' sentence is removed; the bullet now states the regressor and that Lab 1 plants no manipulation through revenue (wording problem: separate FAIL row L05-L06-r5-L06-s5-revenue-channel).", ""),
    "L05-L06-r4-arith-L05-E2": ("PASS", "E2 (line 327): 0.0022350/(0.01131/sqrt(120)) = 2.1647 (displayed SD, 2.16474); 0.0022350/(0.011314/sqrt(120)) = 2.1640 (2.16397). Both figures now written correctly.", ""),
    "L05-L06-r4-arith-L06-E3": ("PASS", "E3 (line 457): 0.003076/0.001467 = 2.0968 -> 2.097 displayed; the lab's unrounded 2.096 is labelled as such.", ""),
    "L05-L06-r4-prose-L06-s5-reserves": ("PASS", "The reserves/capitalised-costs sentence is removed from L06.html §5 bullet 2 (line 359); no reserves mechanism remains in §5 (grep 'reserves': only the why-it-matters list at line 52, a general statement).", ""),
    "L05-L06-card-L05-lab": ("FAIL", "AC2-c069..c075 and c122 re-read: unchanged and consistent. AC2-c123 (cards.json line 898) now reads 'using the unrounded SD 0.011314'; 0.011314 is the SD rounded to six decimals (exact sigma sqrt(2/100) = 0.0113137); the value 2.164 is unaffected (exact SD gives 2.1640, 0.011314 gives 2.1640). Mislabelled basis.", "Card AC2-c123: change 'using the unrounded SD 0.011314' to 'using the SD 0.0113137 (sigma sqrt(2/100), unrounded)' or 'using the SD 0.011314 rounded to six decimals'. See L05-L06-r5-unrounded-sd-label."),
}

NEW = [
    ("L05-L06-r5-unrounded-sd-label", "2.2-numbers-basis", "course/modules/AC/AC2/L05.html E2 (line 327, 'with the unrounded SD 0.011314') and E3 (line 334, 'the unrounded theoretical standard deviation' written as 0.011314); course/modules/AC/AC2/cards.json AC2-c123", "FAIL",
     "The value 0.011314 is itself a rounding (to six decimals) of sigma sqrt(2/100) = 0.0113137 (recompute_r5b.out: rounding error 2.9e-7). The page and card c123 call it 'unrounded'. The displayed results are unaffected: 2.1640 with either value, and 0.0010328 with either value; the lab's 2.164 comes from the exact SD and the unrounded simulated gap.",
     "Replace 'unrounded SD 0.011314' (E2, E3, card c123) with 'SD 0.0113137' (the exact value) or with 'the SD 0.011314 rounded to six decimals'.", ""),
    ("L05-L06-r5-L06-E3-cause", "2.2-numbers-cause", "course/modules/AC/AC2/L06.html E3 solution (line 457, sentence 'Using the rounded inputs 0.0031 and 0.0015 gives z = 2.067 and a tail of 0.039, which is an artefact of rounding the standard error.')", "FAIL",
     "The shift from z = 2.096 to 2.067 comes from rounding both inputs, and the two roundings move z in opposite directions (recompute_r5b.out): rounding only the SE gives z = 2.051 (tail 0.040); rounding only the difference gives z = 2.113 (tail 0.035); rounding both gives 2.067 (tail 0.039). Attributing the whole change to the standard error is a cause stated more exactly than the arithmetic supports.",
     "Replace 'which is an artefact of rounding the standard error' with 'which is an artefact of rounding the inputs (rounding the standard error alone gives 2.051, rounding the difference alone gives 2.113)'.", ""),
    ("L05-L06-r5-L06-s5-revenue-channel", "2.5-labs-scope", "course/modules/AC/AC2/L06.html §5 bullet 2 (line 359): 'Lab 1 has no revenue channel, because the planted manipulation enters the discretionary term directly'", "FAIL",
     "Read literally the claim is false: the lab's total-accrual generator (tests/labs/AC2/lab-AC2-L06-1.py, module docstring and make_sample: total = lag x (C1/lag + C2 (drev - drec)/lag + C3 ppe/lag + DA), with C2 = 0.10 from C_TRUE) puts the revenue-less-receivables term in the true accruals. What the lab lacks is a manipulation that runs through revenue, which is the point the bullet means.",
     "Replace 'Lab 1 has no revenue channel' with 'Lab 1 plants no manipulation through revenue (the revenue-less-receivables term does enter the true accruals, with coefficient 0.10)'.", ""),
]

CARRY_LOC = {
    # id -> the section and file the carried subject lives in (all byte-identical since 2607c60 per the delta hunks)
}


def main() -> None:
    d = json.load(open(R4, encoding="utf-8"))
    rows = []
    for r in d["rows"]:
        rid = r["id"]
        if rid in RERUN:
            status, ev, fix = RERUN[rid]
            rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev,
                         **({"fix": fix} if status != "PASS" else {})})
        else:
            # carried: subject byte-identical since 2607c60 (no delta hunk touches the section)
            carried_ev = CARRY.format(loc=r["location"].split(";")[0].strip()) + r["evidence"]
            rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                         "evidence": carried_ev, **({"fix": r["fix"]} if r.get("fix") else {})})
    for rid, check, loc, status, ev, fix, _ in NEW:
        rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev,
                     **({"fix": fix} if status != "PASS" else {})})
    # the fix text for card row (L05-L06-card-L05-lab) and the FAIL rows
    for row in rows:
        if row["status"] != "PASS" and not row.get("fix"):
            raise SystemExit("missing fix for " + row["id"])
    counts = {s: sum(1 for x in rows if x["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
    frag = {
        "unit": "AC2",
        "slice": "L05-L06",
        "round": 5,
        "verifier": "AC2 independent verifier, round 5, slice L05-L06 (fresh verifier; did not build AC2; shares no context with the builders or the round 1-4 verifiers)",
        "pin": "11b3477",
        "base": "2607c60",
        "checkout": "/tmp/verify-ac2r5-l56",
        "scratch": "/tmp/ac2-v/L05-L06-r5",
        "verified_at": "2026-10-27T00:00:00+00:00",
        "verdict": "FAIL",
        "mutants": [],
        "registry_flags": d["registry_flags"],
        "freshness_flags": [],
        "notes": [
            "Delta 2607c60..11b3477 read in full (git diff, every hunk): L05.html lines 240 (Honest pending wording), 327 (E2), 334 (E3); L06.html lines 345 (Lab 1 interpretation z sentence), 350 (§4 paragraph; the 'too imprecise' sentence removed), 359 (§5 bullet 2; reserves sentence removed), 457 (E3), 465-468 (R1); cards.json records c064 (grade and basis added), c123 (back text); c058, c103, c107, c119, c130, c134 are outside this slice and were not re-verified here.",
            "Command rows re-run this round (outputs in /tmp/ac2-v/L05-L06-r5/): check_pages, check_dag, run_labs 11/11, twins under python -I -W error (identical to the page blocks, cmp_pre.py), page_smoke, verify_refs --unit AC2 (7 of 560, 0 problems) and --offline (560, 0 problems), ruff, mypy, pytest AC2 labs (11 passed), Crossref HTTP 200 for both DOIs (plain curl).",
            "Every previous non-PASS row was re-verified from scratch: round-4 FAIL rows L05-L06-num-L05-derived, L05-L06-num-L06-derived, L05-L06-r3-num-L05-E3, L05-L06-r3-num-L06-a2z, L05-L06-r3-prose-L06-s5-bullet, L05-L06-r4-arith-L05-E2, L05-L06-r4-arith-L06-E3 and L05-L06-r4-prose-L06-s5-reserves now PASS on the fixed text; each new sentence was recomputed (scripts/recompute_r5.py, recompute_r5b.py).",
            "Carried rows: subject sections byte-identical since 2607c60 (no delta hunk touches them), their round-4 evidence is kept with the carry prefix. Card records not in the cards.json hunks are byte-identical.",
            "Lab 1 of L05 and L06 are SIMULATED; each lab's numbers are labelled as such in the pages and cards. No Beneish or other unconfirmed constant appears in these pages.",
            "Mutation testing: none (lesson slice; project slice only).",
            "Publisher pages (doi.org, AAA, Wiley, OUP, JFE, tandfonline, SSRN) were NOT fetched; only Crossref api.crossref.org records (plain curl, HTTP 200).",
            "Architect questions (not FAILs): the authors of dechow1995detecting remain an open question (ruling 1); learner text names the key and the title only. A15 contract is named in learner text (not on the ruling's word list).",
        ],
        "summary": {
            "rows": len(rows),
            "pass": counts["PASS"],
            "fail": counts["FAIL"],
            "unverifiable": counts["UNVERIFIABLE"],
            "fail_ids": [x["id"] for x in rows if x["status"] != "PASS"],
        },
        "rows": rows,
    }
    json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("rows", len(rows), counts)
    print("validate:", ledger.validate(json.load(open(OUT, encoding="utf-8")), "L05-L06"))


if __name__ == "__main__":
    main()
