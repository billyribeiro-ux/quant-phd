import json, sys
src = json.load(open("/tmp/fanout-frags/CF1-c.round13.json"))
PREFIX = "Carried from round 13 (cited subject byte-identical since eaf6d87): "
fresh = {
 "CF1-c-lab-L05-docstring-checks": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py line 1 (module docstring) now reads 'It shows what payback uses.' and the page code block (L05.html line 102) matches it (twin_vs_page.out). The lab has no assert and prints only (grep -n assert: none; print lines 65-88), so 'shows' is the right verb; the round-13 word 'checks' is gone from both places."),
 "CF1-c-cmd-pin": ("PASS", "git rev-parse HEAD in /tmp/verify14-CF1-c = cef676e5 (round-14 pin, see git log -1); .venv symlinked."),
 "CF1-c-cmd-check_pages": ("PASS", "tools/check_pages.py --all: check_pages AC4: PASS; check_pages CF1: PASS; check_pages AP1: PASS (ledgers/CF1/scripts/CF1-c-r14/gates.out)."),
 "CF1-c-cmd-check_dag": ("PASS", "tools/check_dag.py --all: check_dag AC2, AC4, CF1, AP1: PASS (gates.out)."),
 "CF1-c-cmd-run_labs": ("PASS", "tools/run_labs.py --unit CF1: run_labs CF1: PASS (9/9) (gates.out)."),
 "CF1-c-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit CF1 --pages L05 L06: page_smoke modules/CF/CF1/L05.html PASS, L06.html PASS, page_smoke CF1: PASS; rc 0 (ledgers/CF1/scripts/CF1-c-r14/smoke.out). zsh has no timeout command; the run was a plain invocation."),
 "CF1-c-cmd-ruff-mypy-labs": ("PASS", "ruff check and ruff format --check on lab-CF1-L05-1.py and lab-CF1-L06-1.py: All checks passed!, 2 files already formatted; mypy --no-incremental on the two twins: Success: no issues found in 2 source files (gates.out)."),
 "CF1-c-cmd-pytest-labs": ("PASS", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: 100% dots, rc 0 (pytest.out)."),
 "CF1-c-cmd-verify_refs": ("PASS", "tools/verify_refs.py --offline: 560 entries, 0 problems (vr_off.out); tools/verify_refs.py --unit CF1 (live): 2 of 560 entries, 0 problems (vr_live.out)."),
 "CF1-c-cmd-twin-vs-page": ("PASS", "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py: for both L05 and L06 the page pre.expected equals the twin's output (True); page code equals the twin when one trailing newline is ignored (True); the strict comparison is False only for that trailing newline (twin_vs_page.out)."),
 "CF1-c-twin-freshness": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py: the page code block for L05 (line 102) equals the twin line 1 (changed docstring, 'It shows what payback uses.'); L06 page code equals its twin (twin_vs_page.out)."),
 "CF1-c-lab-L05-1-run": ("PASS", "python -I -W error tests/labs/CF1/lab-CF1-L05-1.py: rc 0, 11 output lines (ledgers/CF1/scripts/CF1-c-r14/l05.out); the output matches the page expected block (twin_vs_page.out)."),
 "CF1-c-lab-L06-1-run": ("PASS", "python -I -W error tests/labs/CF1/lab-CF1-L06-1.py: rc 0 (l06.out); output matches the L06 page expected block."),
 "CF1-c-lab-L05-payback-raise": ("PASS", "tests/labs/CF1/lab-CF1-L05-1.py line 38 raises ValueError for flows[0] not negative (unchanged); the changed line 1 docstring says 'It shows what payback uses.' (no claim of checks); the page docstring at L05.html line 102 and the payback() docstring at L05.html line 135 agree with the twin."),
 "CF1-c-cmd-mutants-na-r13": ("PASS", "ledgers/CF1/mutants/ holds the project-slice mutants of other slices; slice c is lessons L05 and L06 and their labs, so no mutant backs a slice-c row (not applicable)."),
 "CF1-c-num-L06-s3-quantile-unrounded": ("PASS", "L06.html Section 3 paragraph (line 211) and misconception 2 (line 244). Re-derived: the unrounded quantiles from the lab (l06_unrounded.py, .6f output) are 14896.623057 and 143406.126569 cents; their difference is 128509.5035 cents (arith_r14.out), which prints as 128509.50; the printed difference 128509.51 minus it is 0.006488, shown as 0.0065 and attributed to rounding of the two printed quantiles (rounding errors 0.003057 and 0.003431). Both sentences now state these values correctly. The lab does not print the unrounded difference (the code prints :.2f); the 6-dp output comes from a local copy, not from the lab."),
 "CF1-c-hub-L05-card-two-sided": ("PASS", "course/modules/CF/CF1/index.html line 142 now reads 'Payback and Its Discounted Form', equal to L05.html title (line 6) and h1 (line 36). Grep for 'What Firms Actually Use' across the checkout finds no learner-facing hit (only ledgers/ scratch scripts)."),
 "CF1-c-title-L04-next-link": ("PASS", "course/modules/CF/CF1/L04.html line 549 Next link reads 'L05 · Payback and Its Discounted Form', matching L05.html h1 (line 36)."),
 "CF1-c-num-L06-E3-width": ("PASS", "L06.html E3 solution (line 327): 143406.13 - 14896.62 = 128509.51 cents, 1285.10 currency units (printed; 128509.51/100 = 1285.0951 rounds to 1285.10). Unrounded width 128509.5035 cents -> 1285.095035 units -> 1285.10 to two decimals (arith_r14.out). The 'not a confidence interval' sentence is unchanged in meaning."),
 "CF1-c-prose-L06-misconception-count": ("PASS", "L06.html section 5, misconceptions 1 to 3 (lines 239-248): three li.misconception items, count 3; misconception 2 (line 244) band sentence checked against the unrounded figures above."),
 "CF1-c-struct-L05": ("PASS", "L05.html: check_pages PASS; the only change in this round is line 102 (code docstring), checked against the twin; the rest of the page is byte-identical to eaf6d87 (git diff -U0)."),
 "CF1-c-struct-L06": ("PASS", "L06.html: check_pages PASS; changed lines 66, 211, 244 and 327 read in full (sections 1, 3 and 5 and the E3 solution); section order and blocks unchanged."),
 "CF1-c-banned-scan": ("PASS", "grep -E for roughly, about N, historically, typically, ellipsis, builder, verifier, round, build, unit report, usually, often, always, only, drives, offsets, raises, never over both pages (sed-stripped tags; output reviewed). Hits are in shown calculations or quiz distractors (e.g. 'About 0.1' at L06 line 411 is a quiz option; 'About 0.0532 to 0.0572' at line 320 follows the shown band 0.0552 +/- 1.96 x 0.0010). No banned phrase in the changed sentences."),
 "CF1-c-prose-process-path": ("PASS", "No process word (build, builder, round, verifier, REQUESTS, unit report) in learner text of L05.html or L06.html (grep, output reviewed)."),
 "CF1-c-cards-delta-r12": ("PASS", "course/modules/CF/CF1/cards.json is byte-identical between eaf6d87 and cef676e (git diff --quiet exit 0); no card changed."),
 "CF1-c-hours": ("PASS", "L05.html and L06.html data-hours=8 (line 2) unchanged; index.html line 29 unchanged; hub card hours 8 h (line 142) unchanged."),
}
new = {
 "CF1-c-prose-L06-section1-decision-rule": ("PASS", "L06.html line 66 (rewritten): 'accept a project whose NPV at the stated rate is positive. This lesson applies that rule to the expected NPV.' L01.html line 64 states the same rule ('Accept a project whose NPV(r) is positive'). 'Remark 3.1 shows that the expected NPV does not fix the share of draws that lose money' matches Remark 3.1 (line 216) and its example X = +/-1, Y = 0 (both mean 0; Pr(X<0)=1/2, Pr(Y<0)=0)."),
 "CF1-c-prose-L06-section1-def12-summaries": ("FAIL", "L06.html line 66 (sentence 'Definition 1.2 defines the summaries that Lab 1 reports, in plain words.'): Definition 1.2 (line 63) defines the sample mean, the standard error, the nearest-rank quantile and the share below zero. Lab 1 also prints the sample standard deviation (lab output line 'n 50000 sd_npv_cents_sample 49419.62', reported at L06.html line 206) and the closed-form standard deviation. The sample standard deviation appears in Definition 1.2 only inside the standard-error definition and is not defined as a summary, so the sentence claims more than Definition 1.2 defines."),
 "CF1-c-hub-rungs-r14": ("PASS", "index.html lines 151-152 (cross-slice hub, changed this round): 'Lab 1 on the project page: a three-year project ... ending in an NPV of 926.00 dollars at 10 percent' matches the project-1 twin output 'step 7, NPV at 0.10: 926.00 dollars' (run in this round, 13 lines, rc 0); 'Lab 2 ... with its three blanks' matches three '___' in project.html Lab 2 code (count 3). The claim that Lab 2 output matches the expected output when the blanks are right is project-slice and was not re-run here."),
}
rows = []
seen = set()
for r in src["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in fresh:
        st, ev = fresh[rid]
        rows.append({**r, "status": st, "evidence": ev})
    elif r["status"] == "PASS":
        rows.append({**r, "evidence": PREFIX + r["evidence"]})
    else:
        raise SystemExit("unhandled non-PASS row " + rid)
for rid in fresh:
    if rid not in seen:
        raise SystemExit("fresh id not in r13 " + rid)
for rid, (st, ev) in new.items():
    rows.append({"id": rid, "check": "2.2-numbers" if "quantile" in rid else "2.9-structure", "location": ev.split(" ")[0] if False else "L06.html line 66" if "line66" in rid or "section1" in rid else "index.html lines 151-152", "status": st, "evidence": ev})
out = {k: v for k, v in src.items() if k not in ("rows",)}
out.update({
 "round": 14,
 "pin": "cef676e",
 "base": "eaf6d87ce236a6945ba2a58b05f45ef8f2d186cd (round 13 pin; the round-13 fragment is context only)",
 "checkout": "/tmp/verify14-CF1-c (detached worktree at cef676e; .venv symlinked; vendor copied)",
 "scratch": "/tmp/cf1-v/c14",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "rows": rows,
 "mutants": [],
})
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(len(rows), sum(1 for r in rows if r["status"] == "FAIL"))
