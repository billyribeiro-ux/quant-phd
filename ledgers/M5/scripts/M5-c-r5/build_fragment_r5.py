"""Build the round-5 fragment for M5 slice c from the round-4 rows (carry rule applied) and the round-5 checks."""
import json
import subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS5-M5-c")
R4 = json.loads(Path("/Users/billyribeiro/.fanout/frags/S-M5-c.round4.json").read_text())
R4_ROWS = {r["id"]: r for r in R4["rows"]}
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
BASE = "edbb7aa8de20e6d2f3035c463a79a318c22623c4"
S = "ledgers/M5/scripts/M5-c-r5/out"

def carry(rid, files):
    r = R4_ROWS[rid]
    return {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
            "evidence": f"Carried from round 4 ({files} byte-identical since the previous pin): " + r["evidence"]}

def row(rid, check, location, evidence, status="PASS", fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    return d

rows = [
 row("M5c-gate-check-pages", "2.9 structure (check_pages)", "course/modules/M/M5 (L08-L10, cards.json)",
     f"{S}/check_pages.out: 'check_pages M5: PASS', exit 0 (gates.sh, run on {PIN[:8]})."),
 row("M5c-gate-check-dag", "2.9 DAG (check_dag)", "course/modules/M/M5 pages",
     f"{S}/check_dag.out: 'check_dag M5: PASS', exit 0."),
 row("M5c-gate-check-projects", "2.6 projects (check_projects, unit-level, recorded for completeness)", "course/modules/M/M5/project.html (outside slice)",
     f"{S}/check_projects.out: 'check_projects M5: PASS', exit 0."),
 row("M5c-gate-run-labs", "2.5 labs (run_labs, unit and per page)", "tests/labs/M5/lab-M5-L08-1.py, L09-1.py, L10-1.py",
     f"{S}/run_labs_L08.out, run_labs_L09.out, run_labs_L10.out: each 'run_labs M5: PASS (1/1)', exit 0."),
 row("M5c-twins-isolated", "2.5 twins alone under python -I -W error", "tests/labs/M5/lab-M5-L08-1.py, lab-M5-L09-1.py, lab-M5-L10-1.py",
     f"{S}/twin_L08.out, twin_L09.out, twin_L10.out: exit 0 each under -I -W error. {S}/page_twin_compare.out (script ledgers/M5/scripts/M5-c-r5/page_twin_compare.py): code_equals_twin=True and expected_equals_stdout=True for L08, L09, L10; stderr 0 bytes; RESULT PASS."),
 row("M5c-gate-page-smoke", "2.9 page_smoke for the slice pages, alone", "course/modules/M/M5/L08.html, L09.html, L10.html",
     f"{S}/page_smoke_L08.out, page_smoke_L09.out, page_smoke_L10.out: 'page_smoke modules/M/M5/Lxx.html: PASS', exit 0."),
 row("M5c-gate-ruff-mypy", "2.5 twins: ruff and mypy", "tests/labs/M5/lab-M5-L08-1.py, L09-1.py, L10-1.py",
     f"{S}/ruff_check_twins.out 'All checks passed!'; {S}/ruff_format_twins.out '3 files already formatted'; {S}/mypy_no_incremental.out 'Success: no issues found in 385 source files'."),
 row("M5c-gate-pytest-labs", "2.5 relevant pytest", "tests/test_labs.py -k M5",
     f"{S}/pytest_labs_M5.out: all tests passed, exit 0."),
 row("M5c-gate-verify-refs-offline", "2.1 citations (verify_refs --offline)", "references/references.json; slice pages",
     f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. No reference or registry file changed in the delta; the live run was not repeated."),
 row("M5c-lab-L08-1", "2.5 lab L08-1 (demonstration; rung not applicable)", "course/modules/M/M5/L08.html:136-271; tests/labs/M5/lab-M5-L08-1.py",
     "Delta: docstring lines 9-10 of the twin (and the embedded copy at L08.html:147-148) now define u = u(1/4) = 1/2 before u/(1-BETA) = 5. Twin output (twin_L08.out): 'V* = 5.000000 after 257 iterations', residual 8.695e-13, largest sampled ratio 0.900000, and 500.000000 at beta = 1. Page code equals twin and expected block equals stdout (page_twin_compare.out)."),
 row("M5c-lab-L09-1", "2.5 lab L09-1 (demonstration; rung not applicable)", "course/modules/M/M5/L09.html:130-274; tests/labs/M5/lab-M5-L09-1.py",
     "Twin unchanged this delta. twin_L09.out reproduces the expected block: certified_stop n 59, 103, 147 with cert = actual error, fixed_count 1.7433922005, naive_step n 126 with actual error 0.0000085808; page_twin_compare.out PASS."),
 row("M5c-lab-L10-1", "2.5 lab L10-1 (demonstration; rung not applicable)", "course/modules/M/M5/L10.html:175-353; tests/labs/M5/lab-M5-L10-1.py",
     "Twin unchanged this delta. twin_L10.out: Part A n=1000 right 0.667166500000, left 0.666166500000; Part B largest_error_over_mesh 0.491631, all_within_2_mesh True; Part C jumps 1 at meshes 0.1 and 0.01; Part D 0.500500000000 and 0.499500000000. page_twin_compare.out PASS."),
 row("M5c-num-L08-worked", "2.2 numbers (worked values, one row per span)", "L08.html:74, :133, :278, :312, :326, :369, :483",
     "Changed lines re-derived (ledgers/M5/scripts/M5-c-r5/numbers_r5.py, out/numbers_r5.out): sqrt(0.75)=0.866025, sqrt(0.5)=0.707107, sqrt(0.5)-0.25=0.457107, sqrt(0.457107)=0.676097, 0.9*5.000000+0.676097=5.176097. Lines :133 and :278 are byte-identical since the previous pin and were verified in round 4."),
 row("M5c-num-L08-counts", "2.2 numbers (iteration counts and a priori counts)", "L08.html:293, :362, :455, :490",
     f"E1 (L08.html:362, changed): lab copies with BETA=0.5 and 0.95 print 40 and 527 iterations ({S}/e1_beta_copies.out); solver count 257 at 0.9 (twin_L08.out). Least n with beta^n*Delta/(1-beta) <= 1e-12, Delta=sqrt(3)/2, is 41, 283, 595 (thresholds 40.66, 282.74, 594.29; numbers_r5.out). The page's 'rises' statement and values match. :293, :455, :490 unchanged and matching."),
 carry("M5c-num-L08-ratio-unrounded", "course/modules/M/M5/L08.html:271"),
 row("M5c-num-L09-apriori-R2", "2.2 numbers (a priori count, Problem R2)", "L09.html:392-399 (R2 statement and solution; changed line 395)",
     f"numbers_r5.out: bound at n=151 is 1.066963e-6 (page 1.067e-6), at n=152 is 9.602671e-7 (page 9.60e-7); threshold 0.9^n <= 1.1547e-7; least n = 152. Certified stop at tol 1e-6 is n=147 (twin_L09.out). Matches."),
 carry("M5c-num-L09-problems-quiz", "course/modules/M/M5/L09.html:311-327, :363, :436-492"),
 carry("M5c-num-L09-E2-ratio", "course/modules/M/M5/L09.html:290, :370"),
 row("M5c-num-L10-example33", "2.2 numbers and 2.4 mathematics (Example 3.3 closed forms)", "L10.html:147 (changed), :471, :485, :580",
     f"numbers_r5.out: exact Fraction sums for n=4, 10, 100, 1000 equal (n+1)(4n-1)/(6n^2) and (4n^2-3n-1)/(6n^2) (direct_sums_match=True). right-2/3 = (3n-1)/(6n^2) <= 1/(2n) and |left-2/3| = (3n+1)/(6n^2) <= 2/(3n) <= 1/n hold for each n. Printed Part A values agree (twin_L10.out)."),
 row("M5c-num-L10-partB-P2", "2.2 numbers (Part B ratio and Problem P2)", "L10.html:352, :451-453, :478 (changed)",
     "L10.html:478 prints largest_error_over_mesh 0.491631, matching twin_L10.out Part B (200 partitions, all_within_2_mesh True). P2 bound |S-2/3| <= m under Assumption 1 is consistent with ratio < 1."),
 row("M5c-num-L10-prop42-R2-R3", "2.2 numbers and 2.4 mathematics (Prop 4.2, Problem R2, Problem R3)", "L10.html:376-381, :502-503, :508-510 (R3 changed)",
     "R3 (:508-510): G(x) = x^2 + 5 has G' = 2x, so Theorem 3.1 gives 2/3, the value of Corollary 3.2. Proposition 4.2 and R2 are unchanged and re-derived. The symbol defect in the R3 solution is logged as M5c5-L10-R3-symbol."),
 row("M5c-math-L08", "2.4 mathematics (Prop 1.3, Remark, Thm 2.2 (a)-(c), Ex 1.2, Ex 2.3, Problems M1-M3, P1-P3, R1-R2)", "L08.html:77-130, 131-134, 317-400 (changed lines 84, 312, 326, 362, 369)",
     "Changed mathematics re-derived: Example 1.2 values; Problem M1 solution; Problem M3 (F(0.75) uses 0.866 >= 0.75, F(0.5) uses 0.707 < 0.75); Problem E1 a priori count; Problem E2 arithmetic. Proposition 1.3 proof (:84) changes only the markup of 'a Cauchy sequence' (concept link). Theorem 2.2 (a)-(c), Example 2.3 and P1-P3 unchanged; no new mathematical claim."),
 carry("M5c-math-L09", "course/modules/M/M5/L09.html:52-130 and :352"),
 row("M5c-math-L10", "2.4 mathematics (Sections 1-4, Lemmas, Theorems, Props, problems)", "L10.html:69-172, 364-381, 418-510 (changed lines 146-147, 167, 389, 478, 496, 508, 510, 528)",
     "Changed items re-derived: Example 3.3 algebra (see M5c-num-L10-example33); Step 3 (:167) argument unchanged, only the concept link; P2 and P3 (:449-462) proofs valid (P3 uses Theorem 3.1 with G' = 1); E2 (:478); R1 solution (:496) names the uses at Lemma 2.1(i), Lemma 2.4(c) and Lemma 2.2, matching the proof at :129-132; R3 (:508-510) math correct; Key results row (:528) T. The hypothesis wording in Section 5 (:389) is logged as M5c5-L10-sec5-hypothesis."),
 row("M5c-math-cross-refs", "2.4 cross-references and 2.1 locators (M2, M5 L01/L02/L06/L07/L08)", "L08: L07 Thm 2.1; L09: L01 Thm 1.2, L02 Thm 2.5, L06 Prop 1.3, L08 Thm 2.2(a); L10: M2 L09 Def 1.3, Lemmas 1.1/1.2, Ex 3.2; L10 :496 (R1)",
     "M2 L09 read: Lemma 1.1 (refinement) at course/modules/M/M2/L09.html:65, Lemma 1.2 (lower below upper) at :75, Definition 1.3 (integrable function and definite integral) at :85. The new R1 solution's citation of Definition 1.3 (boundedness) and Lemma 2.4(c) (integrability on [c,e] and [e,d], L10.html:105-108) match. L08 and L09 citations unchanged."),
 row("M5c-math-grades", "2.3 grades (theorem titles, key-results rows)", "L08.html:413-419; L09.html:414-419; L10.html:522-530 (new row :528)",
     "L10 key-results row at :528 is T with basis 'Example 3.3' and mirrors cards M5-c170, M5-c233, M5-c234 (T, Example 3.3). L08 and L09 tables unchanged; block titles match their table rows. Wording note (not a row): the basis 'Lab 1, Part A checks each row' is accurate for the exact closed forms and error formulas (lab twin lines 83-84), which the page proves; the 1/n inequality is proved on the page, not checked by the lab."),
 row("M5c-struct-L08", "2.9 structure (template sections in order)", "course/modules/M/M5/L08.html", "No heading or section added or removed in the delta (-U0 hunks are in-paragraph or in-block edits); check_pages PASS."),
 row("M5c-struct-L09", "2.9 structure (template sections in order)", "course/modules/M/M5/L09.html", "No heading or section added or removed in the delta; check_pages PASS."),
 row("M5c-struct-L10", "2.9 structure (template sections in order)", "course/modules/M/M5/L10.html", "No heading or section added or removed; the new key-results row (:528) sits inside the existing table; check_pages PASS."),
 row("M5c-prose-banned", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "L08.html, L09.html, L10.html; cards.json (slice cards)",
     "Scan of the 51 added lines (git diff -U0 edbb7aa8 dde0486b, the L08/L09/L10/cards/twin files) for TODO, TBD, lorem, omitted, beyond the scope, for brevity, clearly, obviously, well known, can be shown, roughly, about, it is important: no hit."),
 row("M5c-prose-process-words", "2.9 process words in learner text", "L08.html, L09.html, L10.html; cards.json",
     "Scan of added lines and the three pages for previous, revis, updat, fixed, round, ledger, verif, builder, agent, reviewer, earlier, ruling, audit: no learner-text hit (only 'fixed point', a mathematical term)."),
 row("M5c-prose-html", "2.9 HTML validity (raw < in math)", "L08.html, L09.html, L10.html",
     "html.parser reads L08, L09 and L10 without error. Added lines contain '<' only as a math relation followed by a space (the pattern already used in the round-4 pages), which HTML parses as text."),
 carry("M5c-prose-stock-L09", "course/modules/M/M5/L09.html:272, :485"),
 carry("M5c-prose-L09-nav", "course/modules/M/M5/L09.html:505"),
 carry("M5c-thm-L09-1.3-hypotheses", "course/modules/M/M5/L09.html:86"),
 carry("M5c-quiz-L10-q7", "course/modules/M/M5/L10.html:585"),
 row("M5c-quiz-numeric-answers", "2.2 quiz numeric keys and tolerances", "L08.html:438-483 (changed :441, :483); L09.html:438-489; L10.html:549-603",
     "L08 :441 key 0.866025 with tolerance 1e-6 (exact 0.8660254, difference 4e-7); :483 key 0.676097 with tolerance 1e-6 (exact 0.6760967). L08 key 10 (u=1/2, beta=0.95) and L09, L10 keys unchanged and re-checked."),
 row("M5c-dag", "2.9 DAG and concept links", "L08.html:38-39, :84; L09.html:38-39; L10.html:38-39, :167",
     "check_dag M5 PASS. L08's new link to L02 'cauchy-sequence' (:84) is in its prerequisite closure (L08 Uses L07; L07 Uses L02 cauchy-sequence, L07.html:38). L10 :167 links to the same L02 definition; L10's closure reaches L02 through L06 (L06.html:38 links cauchy-sequence to L02) and L10 uses compactness (L06). The link target matches the convention of L04.html:266."),
 row("M5c-notation", "2.4 notation (notation.json)", "L08.html, L09.html, L10.html math segments",
     "notation/notation.json has 8 registered symbols (T, Phi, gamma_3, ...); none is Delta, kappa or c. The new Delta (L08.html:362, defined in the same sentence) and kappa (L10.html:508) collide with no registered symbol. The unbound 'c' in the R3 solution is logged as M5c5-L10-R3-symbol."),
 carry("M5c-hours", "course/modules/M/M5/L08.html:2, L09.html:2, L10.html:2; course/modules/M/M5/index.html"),
 row("M5c-cards-schema", "2.7 cards schema, ids and grade/basis", "course/modules/M/M5/cards.json (233 cards; 87 in L08-L10)",
     "cards.json parses; 233 cards, no duplicate ids. Delta: removed M5-c067, c175, c222, c229; added M5-c242 (L07), c243 (L08). L08 29, L09 26, L10 32 = 87 in slice (round 4 counted 33 for L10 before c175 was removed). M5-c242 has no grade or basis, as the other definition cards do (e.g., M5-c001)."),
 row("M5c-cards-L08", "2.7 cards L08 (29 cards, each against the lesson text)", "cards.json, lesson L08 cards (c121-c139, c186, c199, c200, c204, c206, c212, c226-c228, c243)",
     "All 29 L08 cards re-read against the lesson this round. Changed: M5-c135 (text; still duplicates a Lesson 9 card, see M5c3-cards-duplicate-fact); M5-c243 new (matches Example 1.2 at L08.html:74 and its T basis); M5-c229 removed. c133/c134/c135 match Misconceptions 1-3 (L08 misconception list); c139, c136-c138, c204, c206, c227, c228 match the twin output."),
 row("M5c-cards-L09", "2.7 cards L09 (26 cards)", "cards.json, lesson L09 cards (c140-c161, c202, c207, c208, c230-c232, c235)",
     "All 26 L09 cards re-read; text unchanged in the delta. c160 remains consistent with the revised Misconception 2 (L09.html:294); c155-c158, c207, c208, c230-c232 match twin_L09.out; c154 matches numbers_r5.out (152, 1.067e-6, 9.60e-7)."),
 row("M5c-cards-L10", "2.7 cards L10 (32 cards)", "cards.json, lesson L10 cards (c162-c189, c209, c233, c234, c236-c239)",
     "All 32 L10 cards re-read this round. Changed: M5-c173 (Prop 4.1; 'even though G is nondecreasing (Remark 4.2)' matches Remark 4.2 at L10.html:371). Removed: M5-c175 (duplicate of c173). c170, c233, c234 match the new Example 3.3 text; c171 and c172 match P2 and Example 3.3; c178 and c181 match P3 and Misconception 3; c182, c183, c185, c209 match twin_L10.out."),
 row("M5c-cards-numbers", "2.7 card numbers appear in their lesson", "cards.json (slice cards) vs L08-L10 and lab outputs",
     "Numbers on the changed or new cards appear in their lesson or lab output: c137 0.900000, c138 5.176097, c139 40/257/527, c154 152, c182 0.667166500000 and 0.000499833333, c209 True, c243 0.866025 (twin outputs and numbers_r5.out)."),
 row("M5c-cards-coverage", "2.7 card coverage (Builder F rule: every named example with a claim has a card)", "L08-L10 blocks; cards.json",
     "Re-checked against the Builder F rule in plans/M5-open-items.md. Every named Definition, Proposition, Lemma, Theorem, Corollary and Example in L08-L10 has a card, including Example 1.2 (now M5-c243). Nine misconceptions are carded (c133-c135, c159-c161, c179-c181). The three <dfn> terms (L08.html:96, L09.html:95, L10.html:65) have cards c124, c140, c164. The round-4 locators (L08.html:56, :63; L09.html; L10.html:120) were not re-read individually this round; the card set covers the blocks and dfn terms listed here."),
 carry("M5c-cards-atomic", "cards.json entries M5-c143, M5-c162, M5-c188, M5-c171 (byte-identical)"),
 row("M5c3-cards-duplicate-fact", "2.7 duplicate cards (full scan)", "cards.json: M5-c135 (L08) and M5-c160 (L09)",
     "Resolved this delta: M5-c175 removed (duplicate of c173); M5-c229 removed (subset of c231); M5-c184 removed. Remaining duplicate: M5-c135 ('Is the fixed point V* of the grid operator the value of the continuous savings problem? No ... A finer or continuous state space has a different operator (Misconception 3)') and M5-c160 ('Does the certificate of Theorem 2.4 bound the error against the continuous savings problem? No ... the discretization error is not covered (Misconception 2)'). Both give the same answer to the same question: the grid result does not give the continuous problem's value. The delta reworded c135 but kept that answer. Severity LOW (card style).",
     status="FAIL",
     fix="Keep one card for the grid-versus-continuous fact (c160) and give c135 a distinct question, for example about the four-state grid's fixed point values, or delete c135 and keep Misconception 3 on the page."),
 row("M5c3-L08-note-docstring", "2.5 lab docstring vs code (L08 twin)", "tests/labs/M5/lab-M5-L08-1.py lines 9-10; course/modules/M/M5/L08.html:147-148",
     "Round-4 defect fixed: the docstring now defines u = u(1/4) = 1/2 (the utility of consumption 1/4) before 'u/(1-BETA) ... which is 5 at BETA = 0.9'. Part C checks V* against 5.0 within 1e-9 and prints 5.000000 (twin_L08.out). Embedded copy equals the twin (page_twin_compare.out)."),
 carry("M5c-prose-footer", "course/modules/M/M5/L08.html:501; L09.html:510; L10.html:620"),
 row("M5c3-L09-misc2-heading", "2.9 misconception heading vs body (L09 Misconception 2)", "course/modules/M/M5/L09.html:293-294",
     "Heading 'The certified bound applies to the continuous savings problem' and body (:294, changed) agree: the body says the lab measures against a reference iterate within 1e-12 of the grid fixed point (Lemma 2.3(c)); the lab's docstring (twin lines 15-18: V_ref is the iterate with cert <= 1e-12) matches, and the body says the discretization error is not measured."),
 carry("M5c3-L09-misc3-fixed-count", "course/modules/M/M5/L09.html:298"),
 row("M5c4-L10-ex33-bound-step", "2.4 mathematics (Example 3.3, the 1/n bound is not shown)", "course/modules/M/M5/L10.html:147",
     "Round-4 LOW row fixed: the page now shows the subtraction. Right-2/3 = (3n-1)/(6n^2) <= 1/(2n); left-2/3 = -(3n+1)/(6n^2), whose absolute value is at most 2/(3n) <= 1/n (numbers_r5.out, True for n = 4, 10, 100, 1000). The page's 'by at most 1/n' is now proved."),
 row("M5c4-L10-R1-weakest-hypothesis", "2.4 mathematics (Problem R1 asks for the weakest hypothesis)", "course/modules/M/M5/L10.html:496",
     "Round-4 LOW row fixed: the solution now states the hypothesis the proof as written needs: G' Riemann-integrable on [a,b] (gives M through 'integrable implies bounded' (M2 L09 Def 1.3) and integrability on each I_i through Lemma 2.4(c)) and fG' Riemann-integrable (needed for I; Lemma 2.2 supplies it only when G' is continuous). It matches the three uses at L10.html:129-132 and does not claim a weaker condition suffices. Accepted."),
 row("M5c4-L10-ex33-grade-display", "2.3 grades (Example 3.3 carded T but not graded on the page)", "course/modules/M/M5/L10.html:146; key-results :528; cards M5-c170, M5-c233, M5-c234, M5-c171",
     "Round-4 LOW row fixed: the Example 3.3 block-title now carries class 'claim' and data-grade 'T' (the pattern of Lemma 1.3 at :69), and the key-results table has a T row for it (:528) whose basis is Example 3.3. The cards grade the same results T with basis Example 3.3."),
 row("M5c5-cards-L08-ex12-grade-display", "2.3 grades (Example 1.2 carded T, page shows no grade)", "course/modules/M/M5/L08.html:72-75 (Example 1.2 block, title at :73); cards.json M5-c243",
     "New in this delta. The block title at L08.html:73 is a plain span with no claim class and no data-grade, and no key-results row (L08.html:413-419) mirrors (BV)(1.0). Card M5-c243 grades the same value T with basis 'Example 1.2 (computed on the page)'. This is the same pattern as the round-4 row M5c4-L10-ex33-grade-display, which was fixed for Example 3.3. Severity LOW (presentation).",
     status="FAIL",
     fix="Add class 'claim' and data-grade=\"T\" to the block-title span at L08.html:73 (as at L10.html:146), or add a key-results row for (BV)(1.0)."),
 row("M5c5-L10-sec5-hypothesis", "2.4 hypotheses (Section 5 bullet states a result that needs Assumption 1 without it)", "course/modules/M/M5/L10.html:389",
     "New in this delta. The bullet 'The integrator is not the variable' says 'For G(x) = x^2 the integral of f(x) = x is 2/3' without Assumption 1. The same bullet attaches '(under Assumption 1)' to the value 1/2 and to the change claim, and Corollary 3.2 (L10.html:136-137) is conditional on Assumption 1. Severity LOW (wording) on this reading; it is a borderline missing hypothesis under ruling 26, and the architect should confirm.",
     status="FAIL",
     fix="Insert '(under Assumption 1)' after 'is 2/3' in the first sentence of the bullet at L10.html:389."),
 row("M5c5-L10-R3-symbol", "2.4 notation (symbol defined in statement, undefined in solution)", "course/modules/M/M5/L10.html:508 (statement, kappa) and :510 (solution, G + c)",
     "New in this delta. The R3 statement now uses kappa for the constant, but the solution's first sentence still reads 'the increments of \\(G + c\\)'. c is not defined in R3 (it is the step point in R2). Severity LOW (notation wording).",
     status="FAIL",
     fix="In the solution at L10.html:510, replace '\\(G + c\\)' with '\\(G + \\kappa\\)'."),
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = set(R4_ROWS) - set(ids)
print("round-4 ids not carried into round 5:", sorted(missing))
assert not missing, missing

counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0}
fragment = {
  "unit": "M5",
  "slice": "c",
  "round": 5,
  "verifier": "Claude Haiku 5.5, independent verifier for M5-c, round 5 (delta verification from round-4 pin edbb7aa8). No build-side context; round-4 rows used only as context and re-verified where the subject changed.",
  "pin": PIN,
  "base": BASE,
  "checkout": str(ROOT),
  "scratch": f"{ROOT}/{S}",
  "verified_at": "2026-11-09T09:55:00Z",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": (
    "Delta from edbb7aa8 to dde0486b for slice c: course/modules/M/M5/L08.html, L09.html, L10.html, cards.json (M5 cards only), tests/labs/M5/lab-M5-L08-1.py. "
    "Other M5 files (L01, L03-L07, project.html, lab-M5-L05-1.py, lab-M5-project-3.py) belong to other slices and were not verified here. "
    "Out-of-slice observations for the owners: cards.json M5-c242 (L07, new) restates M5-c201 (L04 Definition 3.2) and has no grade (definition card, so allowed); M5-c241 (L07) unchanged; M5-c084 (L05) now graded T with basis Example 1.4 (not checked); M5-c055, c064 (L04), c105 (L07), c223 (L06) text changed and c067 (L04), c222 (L05) removed (not checked). "
    "plans/M5-open-items.md:92 still says the Example 3.3 closed forms are graded C; the cards and page now grade them T (stale note outside the slice). "
    "Mutants: none written. Slice c has no project grader (ruling 9 applies to graders); lab twins are demonstrations. "
    "Not checked: rendered screenshots of the pages; run_graders and mutate_graders (no grader in slice c); repository-wide gates outside M5 (check_pages --all, check_dag --all, build_site --check, render_curriculum, fetch_data --check); verify_refs live run (no reference changed). "
    "Severity: the four non-PASS rows are LOW under ruling 26 (card style, notation wording, presentation), except M5c5-L10-sec5-hypothesis which is borderline for 'missing hypothesis' and is for the architect to rule on. Ledger verdict is FAIL because non-PASS rows exist; KNOWN-ISSUES entries are needed for any row deferred under ruling 26."
  ),
  "summary": (
    f"M5-c round 5 (delta from edbb7aa8 to dde0486b) on {PIN[:8]}: verdict FAIL by the ledger rule, no blocking row. "
    "All gates pass (check_pages, check_dag, check_projects, run_labs and isolated twins for L08-L10, page_smoke, ruff, mypy, pytest -k M5, verify_refs offline; page code equals twin and expected equals stdout). "
    "Round-4 rows fixed and re-verified PASS: Example 1.2 is now carded (M5-c243); the L08 docstring defines u; the L09 misconception heading is consistent; the Example 3.3 bound step, the grade display and the R1 weakest-hypothesis answer are fixed. "
    "Four non-PASS rows: M5c3-cards-duplicate-fact (c135 and c160 still give the same answer, LOW), M5c5-cards-L08-ex12-grade-display (Example 1.2 card T with no page grade, LOW), M5c5-L10-sec5-hypothesis (unhedged 2/3 in Section 5, LOW or borderline missing hypothesis), M5c5-L10-R3-symbol (undefined c in the R3 solution, LOW)."
  ),
  "counts": counts,
}
out = ROOT / "ledgers/M5/M5-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts)
