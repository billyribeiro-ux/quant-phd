import json, sys
C = "Carried from round 4 (course/index.html byte-identical since pin b276325): "
CL = "Carried from round 4 (L01/L02/L03.html hunks since b276325 do not intersect cited lines): "
R = []
def row(id_, check, loc, status, ev): R.append(dict(id=id_, check=check, location=loc, status=status, evidence=ev))
# re-run this round
row("E2a-r4-cmd-check_pages","2.9 structure; tools/check_pages.py","index, L01-L03","PASS","Round 5 re-run at 04626e9: `.venv/bin/python tools/check_pages.py --unit E2` -> 'check_pages E2: PASS' rc 0 (ledgers/E2/scripts/E2-a-r5/cmds.out).")
row("E2a-r4-cmd-check_dag","2.9 DAG; tools/check_dag.py","index, L01-L03","PASS","Round 5 re-run: 'check_dag E2: PASS' rc 0 (cmds.out). Covers the new L02.html:248 bullet and L01 edits.")
row("E2a-r4-cmd-check_projects","2.6 project gate (unit-level)","unit E2","PASS","Round 5 re-run: 'check_projects E2: PASS' rc 0. Project slice not verified here.")
row("E2a-r4-cmd-run_labs","2.5 labs; tools/run_labs.py","lab-E2-L01-1, lab-E2-L02-1, lab-E2-L03-1","PASS","Round 5 re-run per page: 'run_labs E2: PASS (1/1)' x3, rc 0 each (cmds.out).")
row("E2a-r4-lab-isolated","2.5 labs: twin alone under python -I -W error","tests/labs/E2/lab-E2-L01-1.py, lab-E2-L02-1.py, lab-E2-L03-1.py","PASS","Round 5: `.venv/bin/python -I -W error <twin>` rc 0 for all three (cmds.out). Twins unchanged since b276325 (git diff --quiet).")
row("E2a-r4-lab-page-equals-twin-and-expected","2.5 labs: page code equals twin; expected equals stdout","course/modules/E/E2/L01.html:167-279, L02.html:146-240, L03.html:117-200","PASS","Round 5 re-run of ledgers/E2/scripts/E2-a-r5/embed_and_expected_r3.py: 'page code == twin: True', 'expected == stdout: True' for all three, 'ALL OK' (length diff of 1 is the trailing newline only).")
row("E2a-r4-page-smoke","2.9 page_smoke","index, L01, L02, L03","PASS","Round 5: ledgers/E2/scripts/E2-a-r5/smoke_system_chrome.py --unit E2 --pages index L01 L02 L03 -> 'page_smoke E2: PASS' rc 0 (gates.out; installed Chrome channel).")
row("E2a-r4-ruff-mypy","build gate: ruff, mypy strict","repository","PASS","Round 5: `ruff check .` -> 'All checks passed!'; `ruff format --check .` -> '335 files already formatted'; `mypy --no-incremental` -> 'Success: no issues found in 229 source files' (gates.out).")
row("E2a-r4-pytest","tooling tests for labs and page checks","tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py","PASS","Round 5: pytest -q on the three files -> all dots, no failures (gates.out).")
row("E2a-r4-verify_refs","2.1 citations; verify_refs --offline","references/references.json","PASS","Round 5: `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' rc 0 (cmds.out). Live Crossref not run.")
row("E2a-r4-recompute","2.2/2.4 numbers and formulas","index.html; L01.html; L02.html; L03.html","PASS","Round 5 re-run of recompute_e2a_r4.py: 'TOTAL 55 PASS 55 FAIL 0'. Independent of the page text.")
row("E2a-r4-banned-process-words","2.9 BUILDER_RULES 1.3-1.4 banned phrases","index.html, L01-L03","PASS","Round 5 grep -i for TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|obviously|clearly|it can be shown|roughly|historically over the four files: no hits.")
row("E2a-r4-macros-registered","2.9 notation: macros and symbols","index.html, L01-L03","PASS","Round 5 scan: commands used in the four files are \\R and \\E (both in notation.json macros) plus standard KaTeX; no other macro. Bare-letter scan of math: only X (L01.html:322-324, new action label, not a registered symbol) and T (L02.html:60, a prose disclaimer that T never names a type set). notation.json registers T as return observations (module S1).")
row("E2a-r3-notation-T-as-action-label","2.9 notation: T not reused as an action label","course/modules/E/E2/L01.html:322-324","PASS","Re-verified round 5. The action label T was renamed X in the M2 problem and its solution: L01.html:322 'Player 1 chooses S or X ... 3 at (X, L) and 2 at (X, R)'; :324 'Definition 2.1 asks for u_1(S, a_2) > u_1(X, a_2)... X is not strictly dominant'. Payoff and conclusions unchanged: S beats X (4>3, 3>2), X does not dominate S. The registered symbol T (notation.json, S1) no longer appears as an action label on L01-L03.")
row("E2a-r5-L01-M3-solution-paragraph-markup","2.9 structure: well-formed paragraph markup","course/modules/E/E2/L01.html:406","FAIL","Round-5 fix added a sentence outside its paragraph: line 406 reads '...for this game.</p> For large \\(m\\) and \\(n\\) the count is asymptotically ... Proposition 2.2 can avoid the enumeration when its hypotheses hold.</p>'. The '</p>' after 'for this game.' closes nothing, so the 'For large' sentence sits outside any paragraph and the final '</p>' is an unmatched end tag. html.parser (ledgers/E2/scripts/E2-a-r5/p_balance.py) reports 'stray </p>' at line 406; L02, L03 and index are balanced. check_pages does not check nesting, so the gate passes. Fix: delete the '</p> ' after 'for this game.' so the whole solution is one <p> ... </p>, and re-run check_pages and p_balance.py.")
row("E2a-r5-L01-M3-lab-comparison-count","2.4 numbers: lab comparison count claim","course/modules/E/E2/L01.html:406 vs tests/labs/E2/lab-E2-L01-1.py equilibria()","PASS","equilibria() loops row_best over all len(rows)=m actions (self included) and col_best over len(cols)=n, per profile, so the count is mn(m+n); for m=3,n=4: 12 x 7 = 84 and mn(m+n-2)=12 x 5 = 60 (checked by python). The lab does not run a 3x4 game; the sentence describes the code's count for any game, not a printed lab output. L01.html:506 agrees (60, 'as in Problem M3').")
row("E2a-r5-L01-R2-assumption-reference","2.2 cross-reference: Assumption number","course/modules/E/E2/L01.html:399 vs L01.html:94-96","PASS","Line 399 now cites 'Assumption 2 of Proposition 2.2' for the payoffs being the true objectives. L01.html:94 'Assumption 2. Players choose simultaneously ... each player's payoff is its objective.' Matches.")
row("E2a-r5-L01-285-hedge","2.2 prose claim","course/modules/E/E2/L01.html:285","PASS","'can change the set of profiles that are stable' is hedged; no computed claim to check.")
row("E2a-r5-L02-248-symmetric-bullet","2.2 prose vs assumptions","course/modules/E/E2/L02.html:245, 248 vs L02.html:100","PASS","The bullet 'Assumption 3 considers only the profile in which every bidder uses the same bid function' matches L02.html:100 'Every bidder uses the same strategy b(.) ... Only the symmetric profile is considered.' The count 'four assumptions' (L02.html:245) matches L02.html:101 Assumption 4 list. Bullet order follows 245.")
row("E2a-r5-L03-282-price-cases","2.4 mathematics: M2-style price cases at alpha=1","course/modules/E/E2/L03.html:282 vs Def 1.2 (L03.html:~62) and Prop 2.1 (L03.html:~76-84)","PASS","At alpha=1: m_L(6000)=1-alpha=0 so M(6000)=0 and Definition 1.2 (M(p)>0) fails 6000 (c_L=4000<=6000 but weight 0). At p>=10000: M=alpha+(1-alpha)=1 and expected value alpha*12000+(1-alpha)*6000 = 12000 at alpha=1; 6000+6000*1=12000 agrees with Prop 2.1 formula. Reading note: the sentence 'the offered mix is only the high-quality sellers' holds in population weight; low-quality sellers have cost <= p but weight 0. Accepted under the population-share definition.")
row("E2a-r3-L03-misconceptions-problems-quiz","2.2/2.4 L03 problems and quiz incl. L03.html:282","course/modules/E/E2/L03.html:218-230, 237-431","PASS","Re-verified for the changed line 282 (see E2a-r5-L03-282-price-cases). Other lines in range are byte-identical since b276325.")
row("E2a-r3-L02-canon-uniqueness-heading","2.2 L02 assumption bullets","course/modules/E/E2/L02.html:247, 249","PASS","Re-verified after the hunk inserting line 248: line 247 is 'The proof does not establish uniqueness' and its body is accurate (Prop 2.2 claims only an equilibrium). Line 249 'Values are private' matches Assumption 2.")
row("E2a-r3-DAG-forward-mentions","2.9 DAG: forward mentions","L01.html:37, L02.html:37, L02.html:248-249, L03.html:51, index.html:55-56","PASS","Re-verified: 'ledgers' check_dag E2 PASS rc 0 in round 5 (cmds.out). The L02 forward mention of L08 (winner's curse) moved from 248 to 249 and is unchanged text.")
# carried
for id_, chk, loc, ev in [
 ("E2a-r3-hub-meta-M4-title","2.2 hub meta","index.html:35","Index byte-identical since b276325 (git diff --quiet); previous PASS evidence stands."),
 ("E2a-r3-hub-dangling-reference","2.9 hub","index.html:56","as above"),
 ("E2a-r3-hub-placement-item-1-ambiguous-key","2.9 hub placement","index.html:64-70","as above"),
 ("E2a-r3-hub-cards-titles","2.9 hub cards","index.html:110-118 vs L01-L09 h1","as above"),
 ("E2a-r3-hub-L08-simulated-claim","2.5 simulated claim","index.html:117 vs L08.html","as above"),
 ("E2a-r3-hub-prereq-unlocks","2.9 hub","index.html:35-36","as above"),
 ("E2a-r3-hub-objectives","2.9 hub","index.html:44-49","as above"),
 ("E2a-r3-hub-placement-items-2-5","2.9 hub","index.html:72-103","as above"),
 ("E2a-r3-hub-core-reading","2.1 hub reading","index.html:137-144","as above"),
 ("E2a-r3-hours-arithmetic","2.2 hours","index.html:29; L01-L03 data-hours","as above; data-hours attributes not in any hunk"),
 ("E2a-r3-L01-printed-continuous-line","2.5 lab prints","tests/labs/E2/lab-E2-L01-1.py; L01.html:261-279","L01 twin byte-identical; hunks at 285, 322-324, 399-406 do not intersect 261-279."),
 ("E2a-r3-L01-key-result-unique-best-response","2.4 claims","L01.html:422, 392-393","cited lines unchanged in this delta."),
 ("E2a-r3-L01-prop-2.2-3.2-4.2","2.4 statements/proofs","L01.html:91-103, 119-128, 142-155","cited lines unchanged in this delta."),
 ("E2a-r3-L01-examples-remarks-numbers","2.2 numbers","L01.html:76, 81, 107, 132, 139, 159","cited lines unchanged in this delta."),
 ("E2a-r3-L01-misconceptions","2.9 misconceptions","L01.html:293-309","hunk at 285 is outside 293-309."),
 ("E2a-r3-L01-quiz","2.9 quiz","L01.html:434-508","cited range unchanged (line 506 includes the 60 comparison count, re-checked above)."),
 ("E2a-r3-L02-prop-2.5-proof-gap","2.4 proof","L02.html:133","unchanged."),
 ("E2a-r3-L02-R1-solution-gap","2.4 solution","L02.html:357","unchanged."),
 ("E2a-r3-L02-prop-claims-lab-prints","2.5 lab claims","L02.html:145, 231-240","unchanged."),
 ("E2a-r3-L02-misconceptions-quiz-problems","2.9 problems","L02.html:257-270, 278-355, 358-375, 397-466","hunk at 248 is outside all listed ranges."),
 ("E2a-r3-L03-def-prop-2.1","2.4 definitions/proofs","L03.html:55-88","unchanged."),
 ("E2a-r3-L03-prop-2.3-remark-2.4","2.4 statements","L03.html:96-107","unchanged."),
 ("E2a-r3-L03-lab-hypothesis-and-output","2.5 lab","L03.html:116, 184-200","unchanged."),
 ("E2a-r3-L03-akerlof-attribution","3 attribution","L03.html:212, 437","unchanged; registry title read in round 4 (akerlof1970market)."),
]:
    row(id_, chk, loc, "PASS", (CL if "L0" in loc else C) + ev)
mut = []
summary = ("E2-a round 5 at 04626e9 (delta since b276325): FAIL on one new row. The round-4 M2 symbol fix (T to X at L01.html:322-324) is verified PASS. "
 "The round-5 edit to the M3 solution (L01.html:406) leaves a stray </p> and an unwrapped sentence (FAIL). Everything else re-run is PASS.")
d = dict(unit="E2", slice="a", round=5, verifier="Haiku independent verifier, E2-a round 5 (did not build E2)",
 pin="04626e9", base="b276325 (round-4 pin; C-E2-a.round4.json used as context only)",
 checkout="/Users/billyribeiro/.fanout/wt/verifyC5-E2-a",
 scratch="ledgers/E2/scripts/E2-a-r5/ (cmds.out, gates.out, p_balance.py, build_fragment_r5.py)",
 verified_at="2026-10-28T00:00:00+00:00", verdict="FAIL", rows=R, mutants=mut,
 registry_flags=[], freshness_flags=[],
 notes=["Delta b276325..04626e9 for slice a: course/modules/E/E2/L01.html (285, 322-324, 399, 404-406), L02.html (248), L03.html (282). index.html, L02/L03 twins, lab-E2-L01-1.py byte-identical (git diff --quiet).",
  "No project graders in slice a; no mutants (VERIFIER_RULES ruling on lab twins).",
  "Not checked: cards.json entries (slice b/c); live Crossref verify_refs; the M3 problem at L01.html:328 read only as a title; run of tools/render_curriculum.py and build_site not in slice a scope."],
 summary=summary)
d["verdict"] = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
json.dump(d, open("ledgers/E2/E2-a.json", "w"), indent=1, ensure_ascii=False)
print(len(R), sum(r["status"]=="PASS" for r in R), sum(r["status"]=="FAIL" for r in R))
