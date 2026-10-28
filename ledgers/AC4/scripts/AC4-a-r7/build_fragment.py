import json, sys
PIN = "de53f7e"
CARRY = "Carried from round 6 ({files} byte-identical since the previous pin d57df1e):"
FRESH = "Re-verified in round 7: "
rows = []
def add(id_, check, loc, status, ev, carry=None):
    text = (CARRY.format(files=carry) + " " + ev) if carry else (FRESH + ev)
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": text})

add("AC4-a-cmd-check-pages", "2.9-structure", "course/modules/AC/AC4/index.html, L01.html, L02.html", "PASS",
    "Re-run at de53f7e: .venv/bin/python tools/check_pages.py --all, exit 0; 'check_pages AC4: PASS' (saved /tmp/AC4-v/a/r7/check_pages.out).")
add("AC4-a-cmd-check-dag", "2.9-dag", "course/modules/AC/AC4/L01.html:59,88; L02.html:57,66; index.html:62-63", "PASS",
    "Re-run: tools/check_dag.py --all, exit 0; 'check_dag AC4: PASS'.")
add("AC4-a-cmd-run-labs", "2.5-labs", "tests/labs/AC4/lab-AC4-L01-1.py, tests/labs/AC4/lab-AC4-L02-1.py", "PASS",
    "Re-run: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)', exit 0; --page L01 PASS (1/1); --page L02 PASS (1/1).")
add("AC4-a-cmd-twins-isolated", "2.5-labs", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py; L01.html:222-241; L02.html:251-263", "PASS",
    "Re-run: python -I -W error on each twin, exit 0 each.")
add("AC4-a-cmd-twin-output-equals-page", "2.5-labs", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py; L01.html:222-241; L02.html:251-263", "PASS",
    "Script ledgers/AC4/scripts/AC4-a-r7/twins.py extracts the pre.expected blocks and compares them with the live stdout: L01 20 lines equal, L02 13 lines equal.")
add("AC4-a-cmd-page-smoke", "2.5-labs", "course/modules/AC/AC4/index.html, L01.html, L02.html", "PASS",
    "Re-run: tools/page_smoke.py --unit AC4 --pages index.html L01.html L02.html -> 'page_smoke AC4: PASS', exit 0.")
add("AC4-a-cmd-pytest-labs-lint", "2.5-labs", "tests/test_labs.py -k AC4; tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py", "PASS",
    "Re-run: .venv/bin/python -m pytest tests/test_labs.py -k AC4 -q -> 10 passed (ten dots, 100%). ruff check: 'All checks passed!'; ruff format --check: '2 files already formatted'.")
add("AC4-a-cmd-verify-refs", "2.1-citations", "references/references.json entries datar2020horngrens, kaplan1998cost", "PASS",
    "Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0; tools/verify_refs.py --unit AC4 (live) -> '2 of 560 entries, 0 problems', exit 0.")
add("AC4-a-cite-none-in-lessons", "2.1-citations", "L01.html:487-491; L02.html:522-525", "PASS",
    "No citation markup in L01 or L02; both pages say no registry source is cited.",
    carry="course/modules/AC/AC4/L01.html and L02.html lines 487-491 and 522-525 (diff hunks for L01 are 119, 261, 263, 387, 473; for L02 81, 98)")
add("AC4-a-cite-hub-reading-list", "2.1-citations", "index.html:172-178", "PASS",
    "index.html is unchanged since d57df1e (absent from git diff --stat d57df1e de53f7e).", carry="index.html")
add("AC4-a-hub-reading-list-claim", "2.1-citations", "index.html:174", "PASS",
    "index.html:174 unchanged; keys datar2020horngrens and kaplan1998cost are present in references/references.json.", carry="index.html")
add("AC4-a-num-hub-placement", "2.2-numbers", "course/modules/AC/AC4/index.html:70,82,84,98,128-135", "PASS",
    "index.html unchanged. Nine items; 8/9 = 88.9% >= 80%, 7/9 = 77.8% < 80%, so eight correct is the bar, as line 70 states.", carry="index.html")
add("AC4-a-num-hub-hours", "2.2-numbers", "index.html:29,40,42,144-151; L01.html:34; L02.html:34; L03-L08 eyebrows", "PASS",
    "Eyebrow hours by grep: L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6; sum 50. L05 and L06 hunks touch no line 35 or 34 (L05 hunks 49-470, L06 hunks 88-490). 50 = data-hours-lessons 50 = 71.4% of 70 h; 20/70 = 28.6%. No arithmetic inconsistency.")
add("AC4-a-num-L01-examples", "2.2-numbers", "L01.html:81,251,298,305,310-312,348-349", "PASS",
    "Re-derived: Ex 1.4 (6000/500 = 12, 6000/1000 = 6); Ex 4.1 ((30000-18000)/600 = 20, F = 10000, check 18000); M1 (m = 14, 0.35, 21000-7000 = 14000); M2 (v = 35, F = 24000, 62500); M3 (12 and 6). All exact.",
    carry="L01.html lines 81, 251, 298, 305, 310-312, 348-349 (none in the round 7 hunks)")
add("AC4-a-num-L01-lab", "2.2-numbers", "L01.html:134,222-241,242,283,348-362,403-404", "PASS",
    "Twin output equals L01.html:222-241 (20 lines). E1 428 and 1161 hours, 36,435.46 and 67,213.87 USD; E2 51,473 cents = 514.73 USD; E3 10 of 12; key results 18,463.89 USD and 41.99 USD/h match the run.")
add("AC4-a-L01-hypothesis", "2.5-labs", "L01.html:134", "PASS",
    "L01.html:134 unchanged; months 6 and 11 on the line, residuals 0, 10 of 12 nonzero, as printed.", carry="L01.html")
add("AC4-a-L01-proofs", "2.4-mathematics", "L01.html:70-77,91-99,117-125", "PASS",
    "L01:119 changed (residual defined inline as observed cost less fitted cost). Re-read Prop 3.2 and its proof at L01:124: F + vQ_H = C_H and F + vQ_L = C_L, unique slope (C_H - C_L)/(Q_H - Q_L). Prop 1.3 and 2.2 proofs (L01:76, 98) re-checked by cancellation.")
add("AC4-a-L01-canon-and-misconceptions", "2.9-prose", "L01.html:257-283", "PASS",
    "Changed bullets 261 and 263 re-read: 'set the estimate' (Remark 3.3 gives the reason: every number comes from two months) and 'Accounting costs can mix behaviours' match the body. Four bullets at 257-263 match the lead sentence (four conditions). Misconception 4 states 514.73 USD = 51,473 cents, the largest residual.")
add("AC4-a-L01-R1-count", "2.9-prose", "L01.html:373", "PASS",
    "L01.html:373 unchanged; procedure statement contains no figure.", carry="L01.html")
add("AC4-a-L01-R3-unquantified", "2.4-mathematics", "course/modules/AC/AC4/L01.html:387", "PASS",
    "Brute force, ledgers/AC4/scripts/AC4-a-r7/r3_brute.py: v = 10, F = 0; max absolute error over whole hours 0..1200 is 3990 at 1, 401, 801 hours; 3990/4000 = 0.9975 = 99.75%. Line values 10, 4010, 8010 and costs 4000, 8000, 12000 at those hours match the sentence.")
add("AC4-a-L01-P2-circular", "2.9-prose", "L01.html:330", "PASS",
    "L01.html:330 unchanged; epsilon argument re-derived (F/Q < eps for Q > F/eps).", carry="L01.html")
add("AC4-a-L01-misconception-and-keyresults-grades", "2.3-grades", "L01.html:401-404", "PASS",
    "L01.html:401-404 unchanged; T for proved rows, C for SIMULATED rows matching the lab output.", carry="L01.html")
add("AC4-a-L01-lab-interpretation", "2.5-labs", "L01.html:242", "PASS",
    "L01.html:242 unchanged; statements checked against the run (no error bar printed; two loud failures; 400 to 1,200 hour generator range).", carry="L01.html")
add("AC4-a-L01-quiz", "2.9-prose", "L01.html:413-484 (explanation at 473)", "PASS",
    "Numeric answers 10, 1000, 0.75, 20, 10000, 7 re-derived. Changed explanation at 473 re-derived: over 1 to 400 hours the cost is constant at 4000, so a line reproducing it has slope 0 and F = 4000, and then cannot reach 8000 at 401 hours; the sentence is correct. Options and correct flags unchanged.")
add("AC4-a-L01-hours", "2.6-hours", "L01.html:2,34", "PASS",
    "L01.html:2 and 34 unchanged; data-hours 6 and eyebrow 6 match the hub card.", carry="L01.html")
add("AC4-a-L01-lab-intro-units", "2.5-labs", "course/modules/AC/AC4/L01.html:55", "PASS",
    "L01.html:55 unchanged; integer cents and integer hours match the twin's stated conventions.", carry="L01.html")
add("AC4-a-L01-relevant-range-sentence", "2.9-prose", "course/modules/AC/AC4/L01.html:59", "PASS",
    "L01.html:59 unchanged; Definition 1.1 wording re-read.", carry="L01.html")
add("AC4-a-L01-section5-heading", "2.9-prose", "course/modules/AC/AC4/L01.html:255", "PASS",
    "Heading 'Where the canon breaks' matches the template name at BLUEPRINT.md:430. Four bullets at 257-263 (changed at 261 and 263, re-read above) match the lead sentence.")
add("AC4-a-L01-R3-range-sentence", "2.9-prose", "course/modules/AC/AC4/L01.html:387 (last sentence of R3 solution)", "PASS",
    "Now reads 'if the range is restricted to 1 to 400 hours, the cost is a fixed 4,000 USD'. Brute force shows cost 4000 at every hour 1..400 (values {4000}), so the sentence is correct. The round-6 witness (0 to 400 hours gives {0, 4000}) is resolved by the restriction to 1 to 400.")
add("AC4-a-L02-sensitivity-proofs", "2.4-mathematics", "course/modules/AC/AC4/L02.html:91-114 (line 98)", "PASS",
    "L02:98 changed: 'no step, meaning no jump in fixed cost at a threshold volume'. Matches the Section 4 step definition (L02:118). Proof at L02:103: OI(Q+h) - OI(Q) = mh; DOL identity re-derived.")
add("AC4-a-L02-step-proposition", "2.4-mathematics", "course/modules/AC/AC4/L02.html:120-128", "PASS",
    "L02.html:120-128 unchanged; piecewise-linear zero argument re-derived.", carry="L02.html")
add("AC4-a-L02-cvp-definitions", "2.4-mathematics", "course/modules/AC/AC4/L02.html:57,66,70-76,86", "PASS",
    "Lines unchanged; Def 1.1 assumptions and Prop 2.2 proof re-derived.", carry="L02.html")
add("AC4-a-L02-lab-numbers", "2.2-numbers", "course/modules/AC/AC4/L02.html:134,251-263,264,267", "PASS",
    "Twin output equals L02.html:251-263 (13 lines). Recomputed: margin 1350 cents; F/m = 88.89; OI(88) = -12.00; OI(89) = 1.50; upper zero 2088.89; OI(2000) = 25,800.00 and OI(2001) = -1,186.50; OI(2500) = 5550.00; DOL = 3,375,000/555,000 = 6.08; 1% volume rise (25 units) gives 6.08%; 411.11 units = 16.44% of 2500; 100/13.50 = 7.41.")
add("AC4-a-L02-lab-hypothesis", "2.5-labs", "course/modules/AC/AC4/L02.html:134", "PASS",
    "L02.html:134 unchanged; each predicted value matches the run.", carry="L02.html")
add("AC4-a-L02-canon-practice-claim", "2.3-grades", "course/modules/AC/AC4/L02.html:292", "PASS",
    "L02.html:292 unchanged; refers to Lesson 1 Remark 3.3, which exists.", carry="L02.html")
add("AC4-a-L02-costing-convention-claim", "2.1-citations", "course/modules/AC/AC4/L02.html:293", "PASS",
    "L02.html:293 unchanged; no citation attached.", carry="L02.html")
add("AC4-a-L02-canon-bullets-mix-units", "2.9-prose", "course/modules/AC/AC4/L02.html:287,291,293,294", "PASS",
    "Unchanged lines; Lab 1, Definition 1.1, Proposition 5.1 and Propositions 2.2, 3.2 referenced exist.", carry="L02.html")
add("AC4-a-L02-misconceptions", "2.9-prose", "course/modules/AC/AC4/L02.html:300-317", "PASS",
    "L02.html:300-317 unchanged. Re-derived: 88.89 and 2,088.89; 2,001 units loses 1,186.50 USD. The 'only if' wording at 311 matches card AC4-c020 (see AC4-a-cards-L01-L02). 'Safe' is read as a positive margin of safety, which Definition 3.1 requires (Q_plan > Q*); the page does not define 'safe' separately, which is accepted as lay usage.", carry="L02.html")
add("AC4-a-L02-problems", "2.4-mathematics", "course/modules/AC/AC4/L02.html:326-420", "PASS",
    "L02.html:326-420 unchanged; M1 (1500, 120000), M2 (1429, 3 and -4 USD), M3 (200, 20%, 100, 10%), P1-P3, E1 (89 and 88 whole volumes), E2 (411.11; 2411.11), E3, R1, R2 (-6.58/USD; 82.76 - 88.89 = -6.13), R3 (10 USD below 1,000; 3,000 above) re-derived.", carry="L02.html")
add("AC4-a-L02-remark-5-2-and-prop-5-1", "2.9-prose", "course/modules/AC/AC4/L02.html:283 (with 419)", "PASS",
    "L02.html:283 and 419 unchanged; Remark 5.2 'cannot give a single break-even' is consistent with R3 (3,000 inside the upper range, none below 1,000).", carry="L02.html")
add("AC4-a-L02-key-results-grades", "2.3-grades", "course/modules/AC/AC4/L02.html:431-439", "PASS",
    "L02.html:431-439 unchanged; T rows are proved on the page; C rows match the lab output.", carry="L02.html")
add("AC4-a-L02-quiz", "2.9-prose", "course/modules/AC/AC4/L02.html:448-519 (line 490 re-checked)", "PASS",
    "L02.html:448-519 unchanged; numeric answers 3000, 150000, 89, 500, 2 and the 740.7 and 7.41 explanation at 490 re-derived.", carry="L02.html")
add("AC4-a-L02-hours", "2.6-hours", "course/modules/AC/AC4/L02.html:2,34", "PASS",
    "L02.html:2 and 34 unchanged; data-hours 7 and eyebrow 7 match the hub card.", carry="L02.html")
add("AC4-a-cards-L02-changed", "2.7-cards", "cards.json AC4-c030, AC4-c118, AC4-c119", "PASS",
    "Re-read against L02 text: c030 5,550.00 USD (L02:258); c118 411.11 units, 16.44%, upper break-even 2,088.89 (L02:259, 267); c119 6.08 and 1% gives 6.08% (L02:260, 267). Card lines 376-379 and 416-420 unchanged; the d57df1e to de53f7e hunks in cards.json are at lines 137 and 556 only.")
add("AC4-a-banned-phrases", "2.9-prose", "course/modules/AC/AC4/index.html, L01.html, L02.html", "PASS",
    "Full scan of the three pages for roughly, historically, typically, generally, usually, ellipses and process words (round, builder, verifier, unit report): none in learner prose; 'about' occurs only in the project page, not this slice. The math \\ldots in L02 M2 is a non-terminating decimal, not an omission.")
add("AC4-a-hub-workspace-seed", "2.9-prose", "index.html:161; project.html:299; course/assets/js/grader.js:50-53", "PASS",
    "Hub line 161 says 'for the seed shown in the autograder panel of the project page'. project.html:299 says 'with the seed shown in the autograder panel', and grader.js:50-53 renders 'Your instance seed is ${seed}' in the grader panel. project.html:299 is not in the round 7 hunks (those are 260, 265, 398).")
add("AC4-a-hub-prereq-unlocks", "2.9-prose", "index.html:35-36,60-65", "PASS",
    "index.html unchanged; curriculum prereqs unchanged in this diff (AC4 prereqs [AC1]).", carry="index.html")
add("AC4-a-hub-objectives-placement", "2.9-prose", "course/modules/AC/AC4/index.html:45-56,68-137", "PASS",
    "index.html unchanged.", carry="index.html")
add("AC4-a-hub-skill-check-rung1", "2.4-mathematics", "course/modules/AC/AC4/index.html:128-130", "PASS",
    "index.html unchanged; 2,000 + 4 x 1,200 = 6,800 USD.", carry="index.html")
add("AC4-a-hub-data-status", "2.9-structure", "course/modules/AC/AC4/index.html:169; tests/labs/AC4/*.py", "PASS",
    "index.html unchanged; tests/labs/AC4 twins unchanged in the round 7 diff.", carry="index.html and tests/labs/AC4")
add("AC4-a-footer-L01-L02", "2.9-structure", "L01.html:500; L02.html:535", "PASS",
    "Footer lines unchanged.", carry="L01.html and L02.html")
add("AC4-a-L02-loss-volumes-printed", "2.5-labs", "course/modules/AC/AC4/L02.html:130", "PASS",
    "L02.html:130 unchanged; the lab prints the loss runs and the single and step formula values as stated.", carry="L02.html")
add("AC4-a-L02-steps-bullet", "2.9-prose", "course/modules/AC/AC4/L02.html:291", "PASS",
    "L02.html:291 unchanged; matches the lab's second formula and loss run.", carry="L02.html")
add("AC4-a-L02-key-results-profitable", "2.9-prose", "course/modules/AC/AC4/L02.html:433 (with Remark 2.3 at L02.html:81 and card AC4-c024)", "PASS",
    "L02:433 unchanged ('non-negative'). L02:81 changed (now qualified by whole cents) and still says ceil(Q*); 'profitable' at L02:438 is used for OI(89) = 1.50 > 0. Consistent.")
add("AC4-a-cards-L01-L02", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c001 to AC4-c030, AC4-c118, AC4-c119", "PASS",
    "Every card re-read against its lesson. c020 now reads 'only if', matching L02.html:311 (the round-6 FAIL is resolved). c017, c024, c025 (no-step wording matches L02:98), c013, c014, c029, c030, c118, c119 re-derived from the lab output. 119 cards; no duplicate ids; no duplicate fronts; the 32 ids in the slice are present. The c020 'safe' wording is read as in AC4-a-L02-misconceptions.")
add("AC4-a-L02-remark-2-3-whole-units", "2.9-prose", "course/modules/AC/AC4/L02.html:81 (Remark 2.3)", "PASS",
    "Now reads 'When F and m are whole numbers of cents, Q* is a whole number exactly when m divides F'. Integer divisibility: F/m is an integer iff m | F for integers m != 0. The round-6 witness (12.50 USD margin) is outside the stated premise, since 12.50 USD is 1250 cents, an integer.")
add("AC4-a-L01-R3-range-sentence-dup", "2.9-prose", "course/modules/AC/AC4/L01.html:387", "PASS",
    "Duplicate-check row: no other sentence in R3 or in the lab text asserts a fixed cost over 0 to 400 hours.")
frag = {
 "unit": "AC4", "slice": "AC4-a", "round": 7,
 "verifier": "round-7 independent verifier (Haiku) for slice AC4-a: hub index.html, L01, L02 and lab twins lab-AC4-L01-1, lab-AC4-L02-1 (did not build AC4; shares no context with builders or rounds 1-6)",
 "pin": PIN, "base": "d57df1e",
 "checkout": "/tmp/verify7-AC4-a (detached worktree at de53f7e, .venv symlinked)",
 "scratch": "/tmp/AC4-v/a/r7",
 "verified_at": "2026-10-27T16:00:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta d57df1e..de53f7e for this slice: L01.html lines 119, 261, 263, 387, 473; L02.html lines 81, 98; cards.json lines 137 (AC4-c020 back) and 556 (AC4-c079, not in this slice). index.html unchanged. Lab twins unchanged. L05, L06, project.html, grader/test_project.py and cards outside c001-c030/c118/c119 are other slices and were not judged here, except that their eyebrow lines (L05:35, L06:35) and project.html:299 were checked for the hub rows.",
  "Every changed hunk in L01.html and L02.html and the c020 card was read and re-derived; L01.html (1-502) and L02.html (1-537) and index.html (1-184) were read in full this round.",
  "Previous non-PASS rows re-verified from scratch: AC4-a-cards-L01-L02 (now PASS), AC4-a-L02-remark-2-3-whole-units (now PASS), AC4-a-L01-R3-range-sentence (now PASS). Rows whose cited subject changed this round were re-verified: L01-proofs, L01-canon-and-misconceptions, L01-R3-unquantified, L01-quiz, L02-sensitivity-proofs, L02-remark-2-3. Rows whose subject is byte-identical carry the round-6 PASS with the prefix.",
  "Mutants: not required, since AC4-a is a lesson and hub slice, not a project slice. None written, none claimed.",
  "Alternative correct implementations: not applicable to the lesson slice. The lab twins were run unchanged and their output compared to the page expected blocks.",
  "Judgement call (not a FAIL): card AC4-c020 and L02:311 use 'safe' without a formal definition; it is read as a positive margin of safety (Definition 3.1 requires Q_plan > Q*). A plan exactly at a zero (OI = 0) is therefore not 'above', consistent with the page's usage.",
  "Not checked: the full repository gate (out of scope for a slice verifier); project.html, grader and the L03-L08 page content (other slices); the reading-list books were not fetched from publisher pages (their identity rests on the registry Open Library entries, as in round 6); no live Crossref or publisher page was fetched; no access block was encountered or bypassed."
 ],
 "summary": ""
}
frag["summary"] = (f"Slice AC4-a round 7 (pin {PIN}, base d57df1e): {len(rows)} rows; {sum(r['status']=='PASS' for r in rows)} PASS, "
    f"{sum(r['status']!='PASS' for r in rows)} non-PASS. The three round-6 FAILs are resolved (c020 now 'only if'; Remark 2.3 now has the whole-cents premise; R3 now says 1 to 400 hours). "
    "Commands re-run: check_pages, check_dag, run_labs (10/10, L01 1/1, L02 1/1), twins under -I -W error with output equal to the page blocks, page_smoke, pytest test_labs -k AC4 (10 passed), ruff on twins, verify_refs offline (560, 0 problems) and live for AC4 (2, 0 problems).")
out = "/tmp/verify7-AC4-a/ledgers/AC4/AC4-a.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, len(rows))
