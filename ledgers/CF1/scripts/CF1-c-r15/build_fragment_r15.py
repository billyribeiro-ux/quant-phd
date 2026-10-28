# Builds ledgers/CF1/CF1-c.json (round 15) from the round-14 fragment (carried rows) and the fresh round-15 rows.
import json, subprocess, datetime, sys
ROOT = "/tmp/verify15-CF1-c"
PREV = json.load(open("/tmp/fanout-frags/CF1-c.round14.json", encoding="utf-8"))
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
OUT = "ledgers/CF1/scripts/CF1-c-r15/out/"
S = "ledgers/CF1/scripts/CF1-c-r15/"
CARRY_FILES = ("course/modules/CF/CF1/L05.html (except line 317), L06.html (except lines 63, 66, 211), tests/labs/CF1/lab-CF1-L05-1.py, "
               "tests/labs/CF1/lab-CF1-L06-1.py, references/references.json, cards.json objects for L05 and L06 (CF1-c062 to c102)")
CARRY = "Carried from round 14 (" + CARRY_FILES + " byte-identical since the previous pin, cef676e..c093bf5; the cited lines are outside every hunk of git diff cef676e c093bf5 for these files): "

FRESH = {
 "CF1-c-cmd-pin": ("2.5-labs", "git rev-parse HEAD in /tmp/verify15-CF1-c", f"git rev-parse HEAD = {PIN} (round-15 pin, c093bf5); .venv symlinked; git status clean except .venv (" + OUT + "pin.out)."),
 "CF1-c-cmd-check_pages": ("2.9-structure", "tools/check_pages.py --all", "Output (" + OUT + "check_pages.out): check_pages CF1: PASS; AC2, AC4, AP1 also PASS; exit 0."),
 "CF1-c-cmd-check_dag": ("dag-concepts", "tools/check_dag.py --all", "Output (" + OUT + "check_dag.out): check_dag CF1: PASS; exit 0. The monte-carlo-npv dfn is at L06.html line 63 and is the only <dfn id=\"def-monte-carlo-npv\"> in course/ (grep)."),
 "CF1-c-cmd-run_labs": ("2.5-labs", "tools/run_labs.py --unit CF1", "Output (" + OUT + "run_labs.out): run_labs CF1: PASS (9/9)."),
 "CF1-c-cmd-page_smoke": ("2.5-labs", "tools/page_smoke.py --unit CF1 --pages L05 L06", "Output (" + OUT + "smoke.out): L05 PASS (lab 0.0 s), L06 PASS (lab 0.3 s); page_smoke CF1: PASS. Runtime boot 1.1 to 1.2 s."),
 "CF1-c-cmd-ruff-mypy-labs": ("2.5-labs", "ruff check and ruff format --check on lab-CF1-L05-1.py and lab-CF1-L06-1.py; mypy --no-incremental on both", "Observed in this round: 'All checks passed!', '2 files already formatted', 'Success: no issues found in 2 source files'."),
 "CF1-c-cmd-pytest-labs": ("2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py", "Re-run this round: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py exits 0 with no F or E (/tmp/cf1-v/c15/pytest_full.out, last line of dots and [100%])."),
 "CF1-c-cmd-verify_refs": ("2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", "Offline: 560 entries, 0 problems (" + OUT + "vr_offline.out). Live CF1: 2 of 560 entries, 0 problems (" + OUT + "vr_live.out)."),
 "CF1-c-cmd-twin-vs-page": ("2.5-labs", "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py /tmp/verify15-CF1-c", "Output (" + OUT + "twin_vs_page.out): L05 and L06 expected output identical to twin output under python -I -W error; code identical to twin ignoring one trailing newline (strict string equality is False in both, as the page wraps the code; the rstrip comparison is True)."),
 "CF1-c-lab-L05-1-run": ("2.5-labs", "tests/labs/CF1/lab-CF1-L05-1.py run under python -I -W error", "Output (" + OUT + "lab_L05.out), exit 0. The page expected block equals the twin output (" + OUT + "twin_vs_page.out: lab-CF1-L05-1 expected identical to twin output: True)."),
 "CF1-c-lab-L06-1-run": ("2.5-labs", "tests/labs/CF1/lab-CF1-L06-1.py run under python -I -W error", "Output (" + OUT + "lab_L06.out) matches L06.html expected block lines 194-205 (twin_vs_page.out); exit 0. Deterministic, seeded (SEED 6, seed 2026 for L05)."),
 "CF1-c-cmd-mutants-na-r13": ("2.5-labs", "ledgers/CF1/mutants/ (project-slice mutants)", "Not applicable to slice c: slice c is the L05 and L06 page and twin slice, not a project slice (brief: project slices only). The ledgers/CF1/mutants folder changed in this delta only through the CF1-d-r15 and CF1-a files; none is cited by a slice c row. PASS (not applicable)."),
 "CF1-c-num-L05-E1-range": ("2.2-numbers", "L05.html E1 solution (line 317, changed since the previous pin)", "Recomputed: 693692.91 - 121251.71 = 572441.20 cents; /100 = 5724.412 -> 5724.41 currency units. Lab output (" + OUT + "lab_L05.out): tail_npv_cents_min 121251.71 tail_npv_cents_max 693692.91; distinct_simple_payback 1 and distinct_discounted_payback 1 (payback 2.750 and 3.469 each take one value). The line-317 claim matches."),
 "CF1-c-num-L06-s3-quantile-unrounded": ("2.2-numbers", "L06.html Section 3 paragraph (line 211, changed) and misconception 2 (line 244, unchanged)", "Recomputed unrounded with the lab's own functions (" + S + "l06_unrounded_r15.py, output " + OUT + "l06_unrounded.out): q10 14896.623057, q90 143406.126569, difference 128509.503511 (4 dp: 128509.5035), which prints as 128509.50. Printed difference 143406.13 - 14896.62 = 128509.51. Gap 0.0065 = printed difference minus unrounded difference (0.0065). Median unrounded 79457.938852. Share SE: sqrt(0.0552*(1-0.0552)/50000) = 0.001021 -> 0.0010. The lab computes quantiles unrounded (quantile() returns sorted floats; printed with .2f). PASS."),
 "CF1-c-struct-L05": ("2.9-structure", "L05.html whole page (470 lines, unchanged count; changed line 317 only)", "wc -l 470; check_pages CF1 PASS; the sections, Propositions 2.1, 2.2, 3.1, Remark 2.3, Lab 1 block, problem tiers M, P, E and quiz present (grep count of h2: 10). The page changed only at line 317 (E1 solution), which re-verifies (num-L05-E1-range, prose-L05-E1-section2-locator)."),
 "CF1-c-struct-L06": ("2.9-structure", "L06.html whole page (465 lines; changed lines 63, 66, 211)", "wc -l 465; check_pages CF1 PASS; h2 sections 1 to 9 present (lines 54, 68, 209, 221, 236, 254, 359, 377, 453); Definition 1.2 at line 63 and the Section 1 paragraph at line 66 are re-verified in their own rows."),
 "CF1-c-banned-scan": ("2.9-structure", "L05.html and L06.html learner text (" + S + "banned_scan_r15.py)", "Output (" + OUT + "banned.out): 0 hits for the BUILDER_RULES 1.2/1.3 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, roughly half, about 6%, historically, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown that, ellipsis) and the process words (builder, build, round, verifier, REQUESTS, agent). Code and expected blocks excluded."),
 "CF1-c-prose-process-path": ("2.9-structure", "L05.html and L06.html learner text (" + S + "banned_scan_r15.py)", "Same scan (" + OUT + "banned.out): 0 process words (builder, build, round, verifier, unit report, agent, REQUESTS) in learner text."),
 "CF1-c-prose-L05-E1-section2-locator": ("2.9-structure", "L05.html E1 solution (line 317, changed)", "New sentence: 'so the simple rule reads years 0 to 3 (Proposition 2.1) and the discounted rule reads years 0 to 4 (its discounted analogue in Section 1)'. Simple payback 2.750 lies in (2,3], so tau_S = 3; discounted 3.469 lies in (3,4], so tau_D = 4 (lab output, lab_L05.out). Proposition 2.1 (line 76) reads years t <= tau_S; Section 1 paragraph (line 70) says both numbers lie within years 0 to tau_D. Correct. 'Years 5 and 6 cannot move either payback value' follows. PASS."),
 "CF1-c-prose-L06-def12-summaries": ("2.9-structure", "L06.html line 63 (Definition 1.2 sentence, changed: adds the sample SD)", "PASS. Line 63 now defines the sample standard deviation as the square root of the sum of squared deviations from the sample mean divided by n-1, as Lab 1 computes it. The lab computes it with statistics.stdev (tests/labs/CF1/lab-CF1-L06-1.py), which divides by n-1. Its standard error is the SD divided by sqrt(n), and the lab prints se_cents = sd_n / sqrt(n) (lab_L06.out lines 4-7). The nearest-rank quantile at ceil(pn) matches the lab quantile() function. The definition sentence is correct; the FAIL is on line 66 (next row)."),
 "CF1-c-prose-L06-section1-def12-summaries": ("2.9-structure", "L06.html line 66 (Section 1 summary sentence, changed)", "FAIL (new witness on the changed sentence). Line 66 says: Definition 1.2 defines the mean, the standard error, the quantiles and the share of draws with a negative NPV that Lab 1 reports. Lab 1 prints two standard errors: the mean se_cents (lab_L06.out lines 4-7) and the share se (share_npv_below_zero 0.0552 se 0.0010, lab_L06.out line 12). Definition 1.2 (line 63) defines only the standard error of the mean. The share SE is introduced only in Section 3 (line 211, binomial formula). The sentence therefore attributes to Definition 1.2 a definition it does not contain. The round-14 point (sample SD) is resolved by line 63."),
 "CF1-c-prose-L06-section1-decision-rule": ("2.9-structure", "L06.html line 66 (second half: 'None of these summaries is a decision rule ... Remark 3.1 shows ...')", "Re-read. 'The decision rule remains the one of L01: accept a project whose NPV at the stated rate is positive' matches L01.html line 64 ('Accept a project whose NPV(r) is positive'). Remark 3.1 is at L06.html line 216 and shows the mean does not fix the share below zero (its own example, X = -1 or +1 vs Y = 0). PASS for this half; the summary sentence is in the FAIL row above."),
 "CF1-c-concepts": ("dag-concepts", "L06.html line 63 dfn monte-carlo-npv (changed line; definition unchanged in place); L05.html dfn payback-period line 58", "check_dag CF1: PASS (" + OUT + "check_dag.out). grep: id=\"def-monte-carlo-npv\" occurs once in course/ (L06.html line 63); L06.html line 39 and project.html line 37 link to it with class concept. L05 dfn payback-period at line 58 unchanged."),
 "CF1-c-cards-duplicates": ("2.7-cards", "course/modules/CF/CF1/cards.json all 103 cards (" + S + "cards_delta_r15.py)", "103 cards, 103 unique ids (" + OUT + "cards_delta.out). Duplicate scan run this round: no duplicate front and no duplicate back among all 103 cards, and none among the 32 L05/L06 cards. Changed cards are CF1-c054, c056, c058, c060, c094 (lesson L04, not in slice c). The 32 L05/L06 cards are byte-identical to cef676e. None of them cites the changed E1 clause or the changed Section 1 and Section 3 sentences (checked against the card text)."),
 "CF1-c-cards-delta-r12": ("2.7-cards", "cards.json cef676e to c093bf5 (" + S + "cards_delta_r15.py)", "Changed ids: CF1-c054, c056, c058, c060, c094 (all lesson L04); changed among L05/L06 cards: none (" + OUT + "cards_delta.out). Replaces the round-12 aebdc15-to-eaf6d87 delta row for this pin."),
 "CF1-c-cards-dupes-r12-cross": ("2.7-cards", "cards.json all cards", "Scan run this round (case-insensitive exact match on fronts and backs over all 103 cards): no duplicates; the 32 slice-c cards have 0 duplicate fronts."),
 "CF1-c-mutants-na-r12": ("2.5-labs", "ledgers/CF1/mutants/", "Not applicable to slice c (project-slice mutants only). PASS (not applicable)."),
 "CF1-c-hub-rungs-r14": ("2.9-structure", "course/modules/CF/CF1/index.html line 151 (changed) and line 152 (unchanged)", "Line 151 now: 'Worked example ... Lab 1 on the project page: a three-year project labelled SIMULATED ... including an NPV of 926.00 dollars at 10 percent (step 7)'. project.html lines 111 and 128 print 'step 7, NPV at 0.10: 926.00 dollars' (project lab output, tests/labs/CF1/lab-CF1-project-1.py; the expected block at project.html line 128). Three-year life (LIFE 3 in the lab). Line 152 unchanged; it names Lab 2 and the autograder, no number. PASS."),
 "CF1-c-hub-L05-card-two-sided": ("2.9-structure", "index.html line 142 (byte-identical, outside the hunk at line 151)", "Line unchanged in git diff cef676e c093bf5 (the index.html hunk is at line 151 only); re-read this round: PASS.", None),
}
rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in FRESH:
        check, loc, ev = FRESH[rid][0], FRESH[rid][1], FRESH[rid][2]
        status = "PASS"
        if rid == "CF1-c-prose-L06-section1-def12-summaries":
            status = "FAIL"
        row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
        if status != "PASS":
            row["fix"] = ("Line 66: change 'Definition 1.2 defines the mean, the standard error, the quantiles and the share of draws with a negative NPV that Lab 1 reports' to name the standard error of the mean, "
                          "and add that the standard error of the share (0.0010) is given in Section 3 (line 211) by the binomial formula; or add the share standard error to Definition 1.2.")
        rows.append(row)
    else:
        row = dict(r)
        row["evidence"] = CARRY + r["evidence"]
        rows.append(row)
extra = [
 {"id": "CF1-c-delta-L06-line211-given-model", "check": "2.2-numbers", "location": "L06.html line 211 (changed: 'given the model' removed)",
  "status": "PASS", "evidence": "Only the clause 'given the model' was removed; the sentence now says the middle 80% 'spans 128509.51 cents by the printed quantiles, which is the difference of the two printed figures'. 143406.13 - 14896.62 = 128509.51 (l06_unrounded.out). The removed clause did not carry a number. PASS."},
 {"id": "CF1-c-delta-L05-E1-scope-words", "check": "2.4-math", "location": "L05.html line 317 (E1 solution, changed)",
  "status": "PASS", "evidence": "Scope words checked: 'reads years 0 to 3' (simple) and 'years 0 to 4' (discounted) follow from tau_S = 3 and tau_D = 4 (lab_L05.out values 2.750 and 3.469) and Proposition 2.1 (line 76) and Section 1 (line 70). 'Cannot move either payback value' is backed by Proposition 2.1 and its discounted analogue; the lab's 1000 tails confirm one value each (distinct_simple_payback 1, distinct_discounted_payback 1). PASS."},
 {"id": "CF1-c-delta-cross-slice-notes", "check": "2.9-structure", "location": "cards.json CF1-c054, c056, c058, c060, c094 (L04); project.html lines 189 and 192 (test count 132 to 138), line 402 wording",
  "status": "PASS", "evidence": "These changes are outside slice c (L04 cards and the project slice). They were not verified here. The slice-c cards and pages do not cite them. Recorded for the cross-slice verifier: project.html line 192 now says 138 checks. The project grader is not in slice c. PASS (out of slice; recorded only)."},
]
frag = {
 "unit": "CF1", "slice": "CF1-c", "round": 15,
 "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 15; did not build CF1; no shared context with builders or earlier verifiers",
 "pin": PIN, "base": "cef676e (round 14 pin; the round-14 fragment is context only)",
 "checkout": "/tmp/verify15-CF1-c (detached worktree at c093bf5; .venv symlinked; vendor copied)",
 "scratch": "/tmp/cf1-v/c15",
 "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "mutants": [],
 "registry_flags": PREV["registry_flags"],
 "freshness_flags": [
   "Delta cef676e..c093bf5 for slice c: L05.html line 317 (E1 solution); L06.html lines 63 (Definition 1.2 dfn sentence), 66 (summary sentence), 211 (Section 3 quantile sentence); index.html line 151 (rung 1 text). cards.json changed only for L04 cards CF1-c054, c056, c058, c060, c094 (all outside slice c). Lab twins, references and tools are byte-identical. The rows citing those lines were re-verified; every other slice-c row is carried.",
   "project.html and grader/test_project.py changed in this delta (test count 132 to 138; a C1 annotation wording) and are outside slice c; not verified here."],
 "notes": "Round 15 (pin c093bf5). Round-14 FAIL on the sample standard deviation is resolved: Definition 1.2 (L06.html line 63) now defines the sample SD with n-1, which Lab 1 computes with statistics.stdev. A NEW FAIL on the same sentence (line 66): it says Definition 1.2 defines 'the standard error' that Lab 1 reports, but Lab 1 prints two standard errors (mean and share) and Definition 1.2 defines only the mean's. Fix as in the row. The line 211 quantile sentence and the E1 solution are correct on recomputation. The rung-1 text on the hub is correct against project lab step 7. Hours were not re-estimated (architect ruling). No project-slice mutants: slice c is not a project slice.",
 "summary": "",
 "rows": rows + extra,
}
n = len(frag["rows"])
fails = [r["id"] for r in frag["rows"] if r["status"] != "PASS"]
frag["summary"] = f"CF1-c round 15 (pin c093bf5): rows {n} (pass {n - len(fails)}, fail {len(fails)}). FAIL: {', '.join(fails)}. Fresh rows re-run on this pin; carried rows keep round-14 ids and are marked 'Carried from round 14'."
json.dump(frag, open(ROOT + "/ledgers/CF1/CF1-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(n, fails)
