# Builds ledgers/CF1/CF1-c.json for round 16 (pin c5daab2) from the round-15 fragment.
# Rows refreshed on this pin carry new evidence; other round-15 PASS rows are carried with their id kept.
import json, re, sys
ROOT = "/tmp/verify16-CF1-c"
prev = json.load(open("/tmp/fanout-frags/CF1-c.round15.json"))
REFRESH = {
 "CF1-c-cmd-pin": ("PASS", "git rev-parse HEAD in /tmp/verify16-CF1-c; git status (detached, .venv untracked symlink only)",
   "git rev-parse HEAD -> c5daab261a60575e3ab884fdded45945b2b84cce (ledgers/CF1/scripts/CF1-c-r16/out/pin.out). Previous pin c093bf5; delta c093bf5..c5daab2 touches course/modules/CF/CF1/L05.html (lines 96, 101), L06.html (line 66), CF1/cards.json (cards CF1-c068, CF1-c099) and AC1 files outside this slice; tests/labs and references are unchanged."),
 "CF1-c-cmd-check_pages": ("PASS", "tools/check_pages.py --all", "ledgers/CF1/scripts/CF1-c-r16/out/check_pages.out: 'check_pages CF1: PASS', exit 0."),
 "CF1-c-cmd-check_dag": ("PASS", "tools/check_dag.py --all", "ledgers/CF1/scripts/CF1-c-r16/out/check_dag.out: 'check_dag CF1: PASS', exit 0."),
 "CF1-c-cmd-run_labs": ("PASS", "tools/run_labs.py --unit CF1", "ledgers/CF1/scripts/CF1-c-r16/out/run_labs.out: 'run_labs CF1: PASS (9/9)', exit 0."),
 "CF1-c-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit CF1 --pages L05 L06", "ledgers/CF1/scripts/CF1-c-r16/out/smoke.out: 'page_smoke modules/CF/CF1/L05.html: PASS', 'page_smoke modules/CF/CF1/L06.html: PASS', 'page_smoke CF1: PASS', exit 0; lab-CF1-L05-1 and lab-CF1-L06 run times in the output are well under 10 s."),
 "CF1-c-cmd-ruff-mypy-labs": ("PASS", "ruff check and ruff format --check on tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py; mypy --no-incremental and ruff check . over the repository",
   "ledgers/CF1/scripts/CF1-c-r16/out/ruff.out: 'All checks passed!', '2 files already formatted', exit 0; ruff_all.out: 'All checks passed!', exit 0; mypy.out: 'Success: no issues found in 153 source files', exit 0."),
 "CF1-c-cmd-pytest-labs": ("PASS", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py", "ledgers/CF1/scripts/CF1-c-r16/out/pytest.out: all dots, exit 0 (the test_docs_figures run covers the docs figure quotes)."),
 "CF1-c-cmd-verify_refs": ("PASS", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", "vr_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0; vr_live.out: 'live re-verification of CF1: 2 of 560 entries, 0 problems', exit 0."),
 "CF1-c-cmd-twin-vs-page": ("PASS", "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py /tmp/verify16-CF1-c (run under python -I)", "out/twin_vs_page.out: both labs 'expected identical to twin output: True'; 'code identical' is True ignoring one trailing newline (strict False is only that newline), as in round 15."),
 "CF1-c-twin-freshness": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py", "git diff --quiet c093bf5 c5daab2 -- tests/labs: unchanged in this delta; twin_vs_page.out confirms the page code equals the twin."),
 "CF1-c-lab-L05-1-run": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py under python -I -W error", "out/lab_L05.out: exit 0; output equals the page expected block (twin_vs_page.out). Project A 2.750 / 3.469, B 2.750 / none, D 2.000 / none; NPV gap 385535.69; tail_draws 1000, distinct_simple_payback 1."),
 "CF1-c-lab-L06-1-run": ("PASS", "tests/labs/CF1/lab-CF1-L06-1.py under python -I -W error", "out/lab_L06.out: exit 0; output equals the page expected block; closed forms 79078.68 and 49379.84; share 0.0552 se 0.0010."),
 "CF1-c-prose-L06-section1-def12-summaries": ("PASS", "course/modules/CF/CF1/L06.html line 66 (Section 1 summary sentence, changed in this round)",
   "Round-15 FAIL resolved. Line 66 now says Definition 1.2 defines the sample mean, the standard error of the mean, the quantiles and the share; that Lab 1 reports each (lab output: mean_npv, se_cents, quantile_10/50/90, share_npv_below_zero); that the share's standard error is not in Definition 1.2 but in Section 3 (line 211: sqrt(p(1-p)/n)); that Lab 1 prints sample SD at 50000 only (lab_L06.py line 71-72 and output line 'n 50000 sd_npv_cents_sample'; the n=100..10000 rows print no SD); and that each se_cents is computed from stdev of the draws at that n (lab_L06.py lines 65-66). Each clause checked against lab_L06.py and the output in out/lab_L06.out. Scope note: Definition 1.2 (line 63) says 'Its standard error is ...' right after the SD sentence; the antecedent is grammatically the SD, but the formula is the mean's (sd/sqrt(n)), and the round-15 verifier accepted it as the mean's SE; recorded in notes as a wording point, not a failure."),
 "CF1-c-prose-L06-section1-decision-rule": ("PASS", "course/modules/CF/CF1/L06.html line 66 (second half: 'The decision rule remains the one of L01 ... Remark 3.1 (Section 3) shows ...')",
   "Second half of line 66 checked: 'the one of L01' matches the L01 decision rule (accept if NPV at the stated rate is positive, cited by the page); 'Remark 3.1 (Section 3)' is at L06.html line 216 under h2 s3 (line 209); its title is 'the mean does not fix the share below zero', matching the clause."),
 "CF1-c-scope-L05-remark23": ("PASS", "course/modules/CF/CF1/L05.html line 96 (Remark 2.3, changed in this round)",
   "'Proposition 3.1 (Section 3)': Proposition 3.1 is at L05.html line 209, inside h2 s3 (line 206, 'Payback and NPV on the same flows'). The sentence 'The defect appears when the decision depends on the later flows as well, which is the case for NPV' is the Proposition 3.1 content (NPV gap = PV of years after tau, line 218); lab output npv_gap_A_minus_B_cents 385535.69 shows the dependence. Scope OK."),
 "CF1-c-lab-L05-hypothesis": ("PASS", "course/modules/CF/CF1/L05.html line 101 (Lab 1 hypothesis, changed in this round)",
   "Each clause checked: A pays back 2.750 simple (lab output line 'project A simple_payback 2.750') and 3.469 discounted (output 'discounted_payback 3.469'; recomputed independently: 3.46933); B has the same flows through year 3 (PROJECT_B indices 0..3 equal PROJECT_A indices 0..3 in lab-CF1-L05-1.py line 25-26) so simple payback equal (output 'simple_payback_equal_A_B True'); B's flows after year 3 are 0 against A's 300000, 200000, 100000 in years 4-6, so 'smaller' holds in every later year and Prop 3.1 gives a lower NPV for B (289367.40 vs -96168.29); D pays back 2.000 with negative NPV (-132231.40); 1000 tails change only years 5 and 6 (lab line 81: PROJECT_A[:5] plus two draws); predicted one value of each payback (distinct_simple_payback 1, distinct_discounted_payback 1)."),
 "CF1-c-scope-L05-lab-B-interpretation": ("PASS", "course/modules/CF/CF1/L05.html line 101 (Lab 1 hypothesis, B clause, changed in this round)",
   "Clause 'Proposition 3.1 (Section 3) gives a lower NPV for B, because B's flows after year 3 are smaller than A's' checked against lab-CF1-L05-1.py lines 25-26 and output npv_cents values; the causal word 'because' is supported: the NPV gap 385535.69 equals the PV of A's years 4-6 (300000/1.1^4 + 200000/1.1^5 + 100000/1.1^6 = 385535.69 recomputed in python -I), which is the Proposition 3.1 identity."),
 "CF1-c-struct-L05": ("PASS", "course/modules/CF/CF1/L05.html whole page (470 lines; changed lines 96 and 101 this round, line 317 unchanged)",
   "wc -l: 470 lines; the delta is 6 changed lines (git diff c093bf5 c5daab2 -- L05.html: 2 hunks, one each at lines 96 and 101). Template sections, page order and data-hours=8 unchanged; check_pages and page_smoke PASS (out/check_pages.out, out/smoke.out); banned_scan_r16 hits 0 (out/banned.out)."),
 "CF1-c-struct-L06": ("PASS", "course/modules/CF/CF1/L06.html whole page (465 lines; changed line 66 this round; lines 63 and 211 unchanged)",
   "wc -l: 465 lines; the delta is 1 changed line (git diff -U0 c093bf5 c5daab2 gives hunk @@ -66 +66 @@ only). Structure, sections, hours (data-hours=8) unchanged; check_pages and page_smoke PASS; banned scan 0 hits."),
 "CF1-c-concepts": ("PASS", "course/modules/CF/CF1/L06.html line 63 dfn monte-carlo-npv (line 63 byte-identical to c093bf5, md5 c2f39e1e) and check_dag", "check_dag CF1: PASS (out/check_dag.out). The round's changed L05/L06 lines (96, 101, 66) add cross-references and a Section 1 summary; none adds a new data-concept, so the concept definitions are unchanged."),
 "CF1-c-cards-delta-r12": ("PASS", "course/modules/CF/CF1/cards.json: git diff c093bf5 c5daab2 (CF1-c068 and CF1-c099 changed; AC1 cards are outside slice c)", "The CF1 diff is exactly two cards: CF1-c068 (L05) front and back, and CF1-c099 (L06) back. Each re-checked below (CF1-c-r16-cards-c068-no-rate, CF1-c-r16-cards-c099-def12)."),
 "CF1-c-cards-duplicates": ("PASS", "course/modules/CF/CF1/cards.json (103 cards)", "python -I scan: 103 cards, duplicate ids 0; duplicate L05/L06 fronts 0; L05 cards 17, L06 cards 15 (out/cards_delta.out)."),
 "CF1-c-cards-dupes-r12-cross": ("PASS", "course/modules/CF/CF1/cards.json all cards", "Same scan as CF1-c-cards-duplicates; the two changed fronts are unique."),
 "CF1-c-cards-L05-other": ("PASS", "cards.json CF1-c068 (changed) and the other L05 cards CF1-c062 to c067, c069 to c074, c096 to c098", "CF1-c068 re-checked below; the other L05 cards are byte-identical since c093bf5 (not in the diff)."),
 "CF1-c-cards-L06-c-other": ("PASS", "cards.json CF1-c099 (changed) and the other L06 cards", "CF1-c099 re-checked below; other L06 cards byte-identical since c093bf5."),
 "CF1-c-cards-L05": ("PASS", "cards.json L05 cards CF1-c062 to c074, c096 to c098, c102", "All 17 L05 cards: the only changed one is CF1-c068 (re-checked). Lesson sources read: L05.html Section 1 line 70 and Lab 1 output."),
 "CF1-c-cards-L06": ("PASS", "cards.json L06 cards CF1-c075 to c087, c099, c100", "All 15 L06 cards: the only changed one is CF1-c099 (re-checked against L06.html line 63 and line 66)."),
 "CF1-c-banned-scan": ("PASS", "course/modules/CF/CF1/L05.html and L06.html learner text (ledgers/CF1/scripts/CF1-c-r16/banned_scan_r16.py)", "out/banned.out: 'L05.html hits 0', 'L06.html hits 0' (banned strings, ellipsis, process words) on the changed sentences too."),
 "CF1-c-prose-process-path": ("PASS", "L05.html and L06.html learner text (banned_scan_r16.py, process-word list: build, round, verifier, REQUESTS, unit report, agent)", "out/banned.out: 0 hits; the changed sentences contain no process words."),
}
NEW = [
 ("CF1-c-r16-L06-line63-sd-n-minus-1", "2.2-numbers", "course/modules/CF/CF1/L06.html line 63 (Definition 1.2 sample SD sentence, unchanged since c093bf5) vs tests/labs/CF1/lab-CF1-L06-1.py line 65 (statistics.stdev)", "PASS", "The page says the sample SD is the square root of the sum of squared deviations divided by n-1, as Lab 1 computes it. Lab line 65 uses statistics.stdev(sample), which is the n-1 sample SD (the Python standard library definition). Output line 'n 50000 sd_npv_cents_sample 49419.62' is produced by statistics.stdev(npvs) (line 71). Consistent."),
 ("CF1-c-r16-L06-line66-share-se-binomial", "2.2-numbers", "L06.html line 66 and Section 3 line 211; lab-CF1-L06-1.py line 78; out/lab_L06.out 'share_npv_below_zero 0.0552 se 0.0010'", "PASS", "Line 211 gives the share's standard error as sqrt(p(1-p)/n) at the estimated p. Recomputed: p = 0.0552, n = 50000: sqrt(0.0552*0.9448/50000) = 0.001021, printed 0.0010 (4 dp). Lab line 78 is the same formula. Line 66 correctly says Def 1.2 does not define it."),
 ("CF1-c-r16-L06-line66-sd-printed-at-50000-only", "2.9-structure", "L06.html line 66 'Lab 1 prints the sample standard deviation at 50000 draws only'; lab-CF1-L06-1.py lines 62-72; out/lab_L06.out", "PASS", "Only one SD line is printed (line 71-72: 'n {N_MAX} sd_npv_cents_sample'); the loop over SAMPLE_SIZES (lines 62-70) prints mean, se and z only. 'only' is supported."),
 ("CF1-c-r16-L06-line66-se-from-size-sd", "2.9-structure", "L06.html line 66 'each standard error of the mean that it reports is computed from the sample standard deviation of the draws at that size'; lab lines 63-66", "PASS", "Lab lines 63-66: sample = npvs[:n]; sd_n = statistics.stdev(sample); se_n = sd_n / math.sqrt(n). Each se_cents row uses the SD of its own sample. Claim matches the code."),
 ("CF1-c-r16-def12-standard-error-antecedent", "2.9-structure", "L06.html line 63: 'Its standard error is the sample standard deviation divided by sqrt(n).'", "PASS", "Wording point, not a failure: 'Its' follows the SD sentence, so the antecedent is grammatically the SD. The formula sd/sqrt(n) is the standard error of the sample mean, and the page's line 66 ('the standard error of the mean') states the referent. Recorded for the builder; the round-15 verifier accepted the mean reading. No row fails on it."),
 ("CF1-c-r16-L05-line96-prop31-section", "2.4-math", "L05.html line 96 'Proposition 3.1 (Section 3)'; Proposition 3.1 at line 209 under h2 s3 (line 206)", "PASS", "Cross-reference correct: Proposition 3.1 is in Section 3. Remark claim (defect appears when the decision depends on later flows, as NPV does) is the content of Proposition 3.1 (line 218: NPV difference = PV of years after tau)."),
 ("CF1-c-r16-L05-line101-discounted-payback-recompute", "2.2-numbers", "L05.html line 101 '3.469 years on the discounted rule'; lab output 'discounted_payback 3.469'", "PASS", "Recomputed in python -I from PROJECT_A at 10%: discounted cumulative -96168.29 at year 3 and 204904.04 in year 4; payback = 3 + 96168.29/204904.04 = 3.46933 -> 3.469. NPV gap 385535.69 recomputed (289367.40 - (-96168.29))."),
 ("CF1-c-r16-cards-c068-no-rate", "2.7-cards", "cards.json CF1-c068 back: '2.750 years, for SIMULATED flows. The simple rule uses no discount rate, so the figure does not depend on the 10 per cent rate (Lab 1; Section 1).' vs L05.html line 70 and lab-CF1-L05-1.py lines 30-46", "PASS", "Lesson line 70 says 'The simple rule uses no discount rate.' Lab payback(flows) takes no rate argument (line 30), and the simple payback is computed from the undiscounted flows (line 166-170: payback(flows)). The 2.750 figure is in the lab output. Card front matches the lab's 'simple payback' field. Grade C basis 'Lab 1 (SIMULATED flows)' is correct for a lab result."),
 ("CF1-c-r16-cards-c099-def12", "2.7-cards", "cards.json CF1-c099 back: 'The sample standard deviation, which divides the sum of squared deviations from the sample mean by n-1, divided by the square root of n (Definition 1.2).' grade T", "PASS", "Matches L06.html line 63 (SD with n-1; SE = SD / sqrt(n)). Grade T on a definition is the proper grade. The card's 'standard error of the sample mean' is the mean's SE, as in line 66."),
 ("CF1-c-r16-twins-and-refs-unchanged", "2.5-labs", "git diff --quiet c093bf5 c5daab2 -- tests/labs ; references/ ; tools/", "PASS", "No change under tests/labs, references/ or tools/ in this delta (git diff --stat restricted paths empty), so the lab results and registry rows carried from round 15 are not invalidated by the twins."),
 ("CF1-c-r16-delta-cross-slice", "2.9-structure", "git diff --stat c093bf5 c5daab2 (111 files): course/modules/AC/AC1/cards.json, grader/test_project.py, project.html; ledgers/CF1/mutants/r15e_01..03 and ledgers/CF1/scripts/CF1-d-r15", "PASS", "All changes outside slice c: AC1 cards, AC1 project and grader (other unit), CF1 project-slice mutants r15e_01..03 (the project slice's grader mutants, not lab slice), CF1-d scripts. Not verified here, by scope."),
 ("CF1-c-r16-mutants-na", "2.5-labs", "ledgers/CF1/mutants/ delta (r15e_01 to r15e_03, project grader mutants)", "PASS", "Slice c is the lab slice (L05, L06 and twins), not a project slice; the project-slice mutant rule (VERIFIER_RULES) does not apply, and no earlier mutant is a lab-twin mutant. The three new r15e mutant files belong to the project slice and are out of this slice."),
 ("CF1-c-r16-coverage-note", "2.5-labs", "scope of this round", "PASS", "What was not re-run on this pin: the full pytest suite (only lab, run-lab and docs-figure tests, per the brief's 'relevant pytest'); live page screenshots (not in the brief for this slice); live web access to any external source (no external source is cited in the delta)."),
]
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in REFRESH:
        st, loc, ev = REFRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
        continue
    if rid == "CF1-c-prose-L06-section1-def12-summaries":
        continue
    ev = re.sub(r"^Carried from round \d+ \([^)]*\):\s*", "", r["evidence"])
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                 "evidence": "Carried from round 15 (cited subject at " + r["location"].split(";")[0] + " byte-identical since the previous pin c093bf5): " + ev,
                 **({"fix": r["fix"]} if "fix" in r else {})})
for rid, chk, loc, st, ev in NEW:
    rows.append({"id": rid, "check": chk, "location": loc, "status": st, "evidence": ev})
# keep original FAIL id present (resolved row)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for old in prev["rows"]:
    assert old["id"] in ids, old["id"]
notes = [
 "Round 16 (pin c5daab2; previous pin c093bf5, round-15 fragment is context only). The round-15 FAIL (L06 line 66, 'the standard error' that Lab 1 reports) is resolved: line 66 now names the mean's standard error, states that the share's standard error is in Section 3 (binomial formula, line 211), and that the SD is printed at 50000 only. All four clauses checked against lab_L06 lines 62-79 and out/lab_L06.out.",
 "Changed lines in slice c (git diff -U0 c093bf5 c5daab2): L05.html 96 (Remark 2.3, 'Section 3' cross-reference), 101 (Lab 1 hypothesis, 'Section 3' cross-reference); L06.html 66 (Section 1 summary); cards CF1-c068 and CF1-c099. L06 line 63 is unchanged. Every other slice-c row is carried with its round-15 id and the cited subject marked byte-identical.",
 "Wording point (not a failure): L06.html line 63 'Its standard error is ...' has an ambiguous antecedent (the SD sentence precedes it). Suggested builder fix if the page is reworked: 'The standard error of the sample mean is ...'. Not a failing row because the formula and line 66 name the mean's SE.",
 "Hours not re-estimated (architect ruling); data-hours=8 on L05 and L06 unchanged in this delta; no hub-split arithmetic changed.",
 "No project-slice mutants: slice c is the lab slice. Three new project-slice mutant files (r15e_01..03) entered ledgers/CF1/mutants in this delta and are out of scope.",
]
summary_txt = f"CF1-c round 16 (pin c5daab2): rows {len(rows)} (pass {sum(1 for r in rows if r['status']=='PASS')}, fail {sum(1 for r in rows if r['status']!='PASS')}). Round-15 FAIL row CF1-c-prose-L06-section1-def12-summaries re-verified and PASS. Carried rows keep round-15 ids and are marked 'Carried from round 15'."
frag = {
 "unit": "CF1", "slice": "CF1-c", "round": 16,
 "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 16; did not build CF1; no shared context with builders or earlier verifiers",
 "pin": "c5daab261a60575e3ab884fdded45945b2b84cce",
 "base": "c093bf5 (round 15 pin; the round-15 fragment is context only)",
 "checkout": "/tmp/verify16-CF1-c (detached worktree at c5daab2; .venv symlinked; vendor copied)",
 "scratch": "/tmp/cf1-v/c16",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
 "mutants": [], "registry_flags": prev["registry_flags"], "freshness_flags": prev["freshness_flags"],
 "notes": notes, "summary": summary_txt, "rows": rows,
}
json.dump(frag, open(f"{ROOT}/ledgers/CF1/CF1-c.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(rows), frag["verdict"])
