import json
C7 = "Carried from round 7 (cited lines byte-identical since the previous pin, verified by sed|md5sum on 0d2d0f3 vs f618cf1):"
rows = []
def R(id, check, location, status, evidence):
    rows.append({"id": id, "check": check, "location": location, "status": status, "evidence": evidence})
def carry(id, check, location, evidence):
    R(id, check, location, "PASS", C7 + " " + evidence)

R("E5b-inventory", "slice inventory", "course/modules/E/E5/L04.html, L05.html, L06.html; tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS",
  "Same three pages and three twins as round 7; git diff 0d2d0f3..f618cf1 --stat shows tests/labs/E5 unchanged; changed in slice: L04.html line 474, L05.html lines 257-258, L06.html (notation and prose hunks, lines 60-436), cards.json (E5-c053..c104 edited, E5-c134..c138 added), index.html line 33 (hub lede).")
R("E5b-cmd-check_pages", "tools/check_pages.py --unit E5", "tools/check_pages.py", "PASS", "output 'check_pages E5: PASS'; rc=0 (ledgers/E5/scripts/E5-b-r8/gates.sh)")
R("E5b-cmd-check_dag", "tools/check_dag.py --unit E5", "tools/check_dag.py", "PASS", "output 'check_dag E5: PASS'")
R("E5b-cmd-run_labs", "tools/run_labs.py --unit E5 (L04-L06)", "tools/run_labs.py", "PASS", "output 'run_labs E5: PASS (11/11)'")
R("E5b-cmd-verify_refs", "tools/verify_refs.py --offline", "tools/verify_refs.py", "PASS", "output 'offline integrity: 560 entries, 0 problems'")
R("E5b-cmd-build_site", "tools/build_site.py --check", "tools/build_site.py", "PASS", "output 'site data current: 6 outputs'")
R("E5b-cmd-check_projects", "tools/check_projects.py --all", "tools/check_projects.py", "PASS", "rc=0; 14 PASS lines, no non-PASS line (/tmp/e5b_r8_scr/projects.txt)")
R("E5b-lab-twin-isolated", "twins run alone under python -I -W error", "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py", "PASS",
  "run from a scratch cwd with -I -W error: L04 rc=0 (26 lines), L05 rc=0 (21 lines), L06 rc=0 (32 lines). Not in slice: lab-E5-project-3.py exits rc=1 when launched from a scratch cwd (relative-path sensitivity, not checked further; project labs are another slice).")
R("E5b-lab-lint-types", "ruff check/format and mypy --no-incremental on the E5 twins", "tests/labs/E5/", "PASS", "ruff: 'All checks passed!', '11 files already formatted'; mypy: 'Success: no issues found in 11 source files'")
R("E5b-lab-pytest", "tests/test_labs.py -k E5", "tests/test_labs.py", "PASS", "11 passed")
R("E5b-lab-page_smoke", "tools/page_smoke.py --unit E5, each page alone", "L04, L05, L06", "PASS", "L04 PASS, L05 PASS, L06 PASS (each run alone)")
R("E5b-lab-code-expected", "page code equals twin; expected block equals twin output", "course/modules/E/E5/L04.html, L05.html, L06.html (code data-run; pre.expected)", "PASS",
  "code element data-run: L04 122 lines == twin, L05 88 == twin, L06 115 == twin; expected block == twin stdout for all three (26, 21, 32 lines)")
carry("E5b-cit-hicks", "Hicks citation absent or correct", "course/modules/E/E5/L04.html:566", "line 566 identical (md5 match)")
carry("E5b-cit-L05-L06-none", "L05/L06 reference sections", "course/modules/E/E5/L05.html:485; L06.html:525", "lines 485 (L05) and 525 (L06) identical (md5 match)")
carry("E5b-cit-phelps-plan", "phelps1968money cited at paper level, no locator", "course/modules/E/E5/L06.html:525", "line 525 identical (md5 match)")
R("E5b-num-L04", "prose numbers vs computed values", "course/modules/E/E5/L04.html why-it-matters (line 20), Derivation 2.2, Props 3.2/4.2/4.3, key-results row line 477", "PASS",
  "changed row line 477 re-verified: Lab 1 Part B prints goods_market_benchmark 4 and multiplier 0.8 (L04 twin output line 9; L04.out); other numbers unchanged (carried).")
R("E5b-num-L05", "prose numbers vs computed values", "course/modules/E/E5/L05.html lines 52-53, 80, 257-258, 262 (quiz), 164-166", "PASS",
  "L05 twin output: Part B delta_price 0.100000, delta_output 20.000000; Part C 1.6/1.9, long-run output 1000; Part D nu=400 24.000000 and 0.060000, nu=800 26.666667; new Section 4 bullet 3 output 1060 = 1190-200*1.3... (a=1160+30, P^e=1: P=(190+200)/300=1.3, Y=1190-130=1060) and '60 above potential' correct.")
R("E5b-num-L06", "prose numbers vs computed values", "course/modules/E/E5/L06.html lines 95, 109, 181, 200, 202, 241-245, 254, 293-295", "PASS",
  "Lab output: Part A 0.021667 (13/600); Part C 3%: 0.016667 (=1/60), 4%: 0.008333 (=1/120), slope 0.833333; Part B gaps 58bp etc. L06-E2 counts (9 positive, 3 negative) and L06-E3 (-0.0048333) recomputed by hand from the printed draws; R2 0.062 = 0.05+0.01/(5/6); M2 0.048 = 0.04+0.8*0.01; quiz 0.021667 recomputed.")
R("E5b-prose-scope", "scope words (only, all, always, every, any, same, drives, exactly)", "L04 E1 solution and why-it-matters; L05 why-it-matters, Lab 1 interpretation, Section 4 bullets; L06 lines 53, 181, 194-197, 200, 241, 316", "PASS",
  "'every period' (Cor 3.2) proven for all t; 'for every positive shift' (L05 line 164) holds since nu/(eta+nu)>0 under eta>0,nu>0; 'for every value of a' (Prop 3.1) holds; L06 'only' (line 241, L06-E2 counts) recomputed. The new L05 sentences 'this lesson does not compute that case further' make no scope claim.")
R("E5b-math-L04", "mathematics of L04 proofs and derivations", "course/modules/E/E5/L04.html Derivation 2.2, Def 3.1, Prop 3.2, Props 4.2, 4.3, Remarks 4.4, 4.5", "PASS",
  "Recomputed Y*=28/5, i*=4/5 at Lab 1 inputs (D=h(1-c)+bd=5/4; A=3); Prop 4.2 derivatives; Remark 4.5 bd/D recomputed; the only L04 hunk (line 474) is a benchmark-location wording change, re-verified under E5b-num-L04.")
R("E5b-math-L05", "mathematics of L05 propositions, proofs, remarks and the new Section 4 bullet", "course/modules/E/E5/L05.html lines 41-51, 110, 152, 257-258", "PASS",
  "Prop 2.1 solved and recomputed; Prop 2.2 recomputed; new bullet 2 formulas dP=(da+nu dPe)/(eta+nu), dY=nu(da-eta dPe)/(eta+nu) verified by exact-fraction script on 2000 random parameter sets (0 mismatches, scratch in ledgers/E5/scripts/E5-b-r8/); 'differ whenever dPe != 0' holds since nu>0 and eta>0.")
R("E5b-math-L06", "mathematics of L06 Props 2.1, 3.1, Cor 3.2 and proofs", "course/modules/E/E5/L06.html lines 45-49, 186, 190, 228, 254", "PASS",
  "Prop 2.1 proof recomputed: P_t = P^e - (kappa/nu)(u-un); pi = pi^e - beta(u-un) with beta=kappa/(nu P_{t-1}). Prop 3.1 and Cor 3.2 proofs recomputed; all sentences with pi^e_t substitution are consistent with A3 (pi^e_t = pi_{t-1}).")
R("E5b-notation", "every symbol vs notation/notation.json", "L04-L06 all math; notation/notation.json (macros and symbols)", "PASS",
  "L04-L06 contain no \\E or \\Prob macro (grep count 0 for \\E). Page forecast now \\pi^{e}_t (not a registered symbol; registered symbols are T, \\Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}; none occurs in L04-L06 math). Local letters defined in each lesson.")
R("E5b-define-L06-natural-rate", "natural rate defined before use", "course/modules/E/E5/L06.html:68-70 (A2) vs Definition 1.2 at :83-85", "PASS",
  "lines 68-70 and 83-85 identical (md5 match); Definition 1.2 precedes Prop 3.1 and Remark 3.3.")
R("E5b-define-expected-inflation", "expected inflation defined before use; dfn and cards agree", "course/modules/E/E5/L06.html:60 (dfn), :74 (A3); cards E5-c091, E5-c092", "PASS",
  "L06.html:60 defines <dfn>expected inflation</dfn> as pi^e_t and states it is a forecast fixed by a rule; A3 at :74 gives pi^e_t = pi_{t-1}; cards E5-c091 and E5-c092 read pi^e(t) = P(t-1)(1+pi^e(t)) and pi^e(t) = pi(t-1), matching the page.")
carry("E5b-title-L04", "index title and lesson titles agree", "course/modules/E/E5/index.html:149-151 vs L04.html:36, L05.html:36, L06.html:36", "index lines 149-151 and lesson lines 36 identical (md5 match); index hunk is line 33 only.")
carry("E5b-nav", "previous/next navigation", "L04.html:572-573, L05.html:492-493, L06.html:531-532", "lines identical (md5 match).")
carry("E5b-struct-L04-L06", "section order and minimum counts", "L04-L06 h2/h3 headings", "no heading line in any changed hunk (hunks touch lines 474, 254-261 and L06 lines 57-436 that contain no h2 changes); section counts unchanged; L06 has sections 1-9 in order (L06 text lines 21, 37, 182, 193, 205, 317).")
R("E5b-banned-process", "no process words in learner text", "L04-L06 full text", "PASS",
  "grep -i for round|builder|verifier|revis|fixed|corrected|bug|audit|earlier version over the three pages: the only matches are math ('round(x*10**6)' in lab code, 'held fixed', 'fixed point', 'Expected prices fixed') and no learner-facing process wording.")
carry("E5b-hours", "hours arithmetic and meta-rows", "L04.html:2,35; L05.html:2,35; L06.html:2,35; index meta-row", "lines 2 and 35 of each page and the index meta-row identical (md5 match on the cited lines).")
R("E5b-grades", "grades of Props, Derivations and Remarks", "L04 Props 3.2, 4.2, 4.3; L05 Props 2.1, 2.2, 3.1; L06 Props 2.1, 3.1, Cor 3.2", "PASS",
  "L06 Props 2.1, 3.1 and Cor 3.2 graded T and proved on page (lines 90-104, 183-190, 281); L05 Props graded T (lines 34-47, 150); L04 Props 3.2/4.2/4.3 graded T and proved on page; lab-result rows graded T (exact) or C (SIMULATED, L06 row line 436).")
carry("E5b-labs-simulated", "labs disclose SIMULATED data and say nothing about any economy", "L06.html:114 and docstring (lab twin lines 53-56); L04 and L05 hypothesis", "line 114 identical (md5 match); twin unchanged.")
R("E5b-problems-quiz", "problem sets, retrieval quiz answers and explanations", "L04-L06 problem sets and quizzes (L06 lines 207-316 text numbering)", "PASS",
  "L06 M1 0.5, M2 0.048, M3 0.005 and 0.015, P1/P2 proofs, R2 0.062 and quiz answers 0.021667, 0.048, 0.008333 recomputed; quiz explanations at L06 line 316 match the lab output. L04 and L05 problem sets unchanged in the delta.")
carry("E5b-prose-L05-q7-explain", "L05 quiz q7 explanation and data-correct", "course/modules/E/E5/L05.html:455", "line 455 identical (md5 match).")
R("E5b-interp-labs", "interpretation paragraphs after expected blocks", "L04, L05, L06 'interpretation' paragraphs", "PASS",
  "L06 interpretation (text line 181): 'Part B prints 12 periods' ok; 'check holds only vacuously here' matches output (zero_gap_periods 0, no_change_periods 0). L04 and L05 paragraphs match their outputs (L04 lines 215-226; L05 lines 164-166).")
R("E5b-cards-dup-scan", "duplicate card ids and text", "course/modules/E/E5/cards.json (138 cards)", "PASS",
  "138 cards, ids unique (script), schema per tools/check_pages.py passes; no card id repeated; L04-L06 cards by lesson: L04 19, L05 18, L06 20 plus E5-c134 (L04), E5-c137 (L05), E5-c135, E5-c136, E5-c138 (L06). Cards E5-c131, E5-c132 (L08) and E5-c133 (L03) are outside this slice.")
R("E5b-cards-L04-L06", "cards agree with the current lesson text and carry hypotheses; every card number appears in its lesson", "cards.json E5-c053..c104 and E5-c134..c138", "PASS",
  "every changed or new card re-checked against its lesson: c091-c104 use pi^e and match L06 Props/Remarks/Cor; c102 1.236/1.226/0.021667 printed by lab; c103 grade C with SIMULATED basis matches L06 row line 436; c134 matches Remark 4.5 (bd/D, zero iff bd=0); c137 matches Remark 1.2; c138 matches Remark 3.3; c135/c136 match A1/A2. Cards without a grade field are accepted by the schema.")
R("E5b-card-c095", "card E5-c095 vs L06 Prop 2.1", "cards.json E5-c095 vs course/modules/E/E5/L06.html:95 and :90-96", "PASS", "card text 'pi(t) = pi^e(t) - beta(t)(u(t) - u^n) ... falls by beta(t) for each rise of one unit in u(t)' matches Prop 2.1 at L06.html:90-96; grade T matches the claim tag.")
carry("E5b-hub-data-labs-scope", "hub Data meta-row scope", "course/modules/E/E5/index.html:37", "index line 37 identical (md5 match).")
carry("E5b-wim-cross-refs", "'below' cross-references", "course/modules/E/E5/L04.html:52 ('Definition 3.1 below', 'Definition 4.1 below', 'Remark 4.4 below')", "line 52 identical (md5 match); Definitions 3.1, 4.1 and Remark 4.4 remain below it.")
carry("E5b-plan-hub-L05-card", "hub card for L05 matches L05 text", "course/modules/E/E5/index.html:150 vs L05.html:80", "index line 150 and L05 line 80 identical (md5 match).")
R("E5b-plan-L05-ad-from-is-lm", "plan conformance: AD curve from IS-LM (architect decision)", "course/modules/E/E5/L05.html:80, :257 vs plans/E5-build-plan.md:259", "FAIL",
  "plans/E5-build-plan.md line 259 (unchanged since 0d2d0f3) says 'the aggregate-demand curve from IS-LM'; L05.html:80 still says 'This lesson does not derive its demand curve from the IS-LM specification of Lesson 4. It takes the linear form A1 as the model'. Still unresolved; the page and the plan conflict.")
R("E5b-plan-notation-E", "plan conformance: expected inflation written with the \\E macro", "course/modules/E/E5/L06.html:60, :74, :79, :93-104 vs plans/E5-build-plan.md:232 and :263", "FAIL",
  "Plan line 263 (binding, unchanged) says 'Expected inflation is written with the `\\E` macro'; plan line 232 says NOTATION_REQUESTS: none and the plan uses the registered \\E macro. The round-8 page uses \\pi^{e}_t instead (no \\E in L04-L06). The deviation is not recorded: plans/E5-open-items.md NOTATION_REQUESTS says 'None', and no architect ruling exists. Fix: architect either amends plan line 263 and records \\pi^{e}_t via NOTATION_REQUESTS (or in the NOTATION section), or the builder restores \\E with a non-stochastic meaning request.")
R("E5b7-notation-E", "registry meaning of the symbol used for expected inflation (round-7 FAIL re-verified)", "course/modules/E/E5/L06.html:60, :74, :79, :93, :101-104, :315; notation/notation.json macro '\\E'", "PASS",
  "The round-7 conflict (registered \\E = expectation operator used for a non-stochastic forecast) is gone: grep finds no \\E in L04-L06; the page now writes \\pi^{e}_t, which is not a registered symbol and conflicts with no registered meaning (notation.json symbols listed). The plan-level conflict is carried as E5b-plan-notation-E.")
R("E5b7-xref-A3-section4", "prose cross-reference 'Section 4 states what the rule ...' (round-7 FAIL re-verified)", "course/modules/E/E5/L06.html:74", "PASS",
  "L06.html:74 now reads 'Section 4 states what the rule leaves out.' Section 4 (text lines 194-197) states the rule is a specification, that no other dynamics are given, that the supply-shock term is absent, that beta is not constant, and that the natural rate is not estimated; these are what the rule leaves out.")
R("E5b8-cards-new", "new cards E5-c134..c138 (grade and cite consistency)", "cards.json E5-c134..c138", "PASS",
  "c134 -> Remark 4.5 (T); c135 -> Assumption A1; c136 -> Assumption A2; c137 -> Remark 1.2 and Lesson 4 Remark 4.4; c138 -> Remark 3.3; each card's numbers appear in its lesson.")
R("E5b8-L05-section4-bullet", "new L05 Section 4 bullet 2 (expectations move with the shock)", "course/modules/E/E5/L05.html:258", "PASS",
  "Derivation: Y^d = a - eta P, Y^s = Ybar + nu(P - Pe); eta+nu times P gives P = (a - Ybar + nu Pe)/(eta+nu); changes give dP=(da+nu dPe)/(eta+nu), dY=nu(da-eta dPe)/(eta+nu); verified numerically (0 mismatches of 2000). 'differ whenever dPe != 0' holds since nu > 0 (dP differs by nu dPe/(eta+nu)).")
R("E5b8-L05-remark12-removes", "'§4 states what that choice removes' (Remark 1.2, L05.html:80)", "course/modules/E/E5/L05.html:80, :257", "PASS",
  "Section 4 first bullet states the consequence of the non-linear demand curve (closed forms of Prop 2.1 do not apply), which is what the linear choice removes. Accepted, not a FAIL; the 'removes' wording is the same as the L06 wording that was fixed, so the architect may prefer 'leaves out'.")
R("E5b8-L04-key-row", "L04 key-results row 477 benchmark location", "course/modules/E/E5/L04.html:477", "PASS",
  "row now reads 'Lab 1 Part B gives 0.8 against the benchmark 4 that Part B prints'; Lab 1 Part B output line 'goods_market_benchmark 4' and 'multiplier 0.8'; matches.")

mutants = []
registry_flags = [
  "E5b-plan-notation-E: plan lines 232 and 263 prescribe the \\E macro for expected inflation; the page now uses \\pi^{e}_t and no NOTATION_REQUESTS or open-items entry records the change.",
  "E5b-plan-L05-ad-from-is-lm: plan line 259 requires the AD curve from IS-LM; L05 takes the linear form (unchanged since round 7).",
]
freshness_flags = []
notes = [
  "Delta 0d2d0f3..f618cf1 touched L04.html (1 line), L05.html (2 lines of Section 4), L06.html (notation rewrite and prose), cards.json (edits and 5 new cards), index.html (1 lede line). tests/labs/E5, notation.json, plans/E5-build-plan.md and tools are unchanged.",
  "Carried rows cite lines verified byte-identical by md5 of sed -n on 0d2d0f3 vs f618cf1 (see scripts).",
  "Mutants: none. E5 is a rubric unit with no grader; the L04-L06 twins are demonstrations, so no mutation set applies to this slice. No alternative implementations were run because no grader is in scope.",
  "Not checked by me: lessons L01-L03, L07, L08 and project.html (other slices); cards E5-c131..c133 (L08, L03); lab-E5-project-3 run from a scratch cwd exits 1 (out of slice); run_graders (no E5 grader); render_curriculum; live verify_refs; the L05 'Lab 1' R1 proof (a sketch in the page) was read but not re-derived line by line.",
  "The L05 'removes' wording (Remark 1.2) is accepted as stating a consequence (see E5b8-L05-remark12-removes).",
  "The hub lede (index.html:33) changed to 'most of them static'; I checked it against the module statement 'static except for the Solow recursion and the adaptive-expectations path'; consistent.",
]
frag = {
 "unit": "E5", "slice": "b", "round": 8,
 "verifier": "Haiku independent verifier, E5 slice b round 8 (did not build E5)",
 "pin": "f618cf1",
 "base": "0d2d0f3 (round-7 pin); round-7 fragment /Users/billyribeiro/.fanout/frags/C-E5-b.round7.json used as context. Rows whose cited lines are unchanged are carried with the 'Carried from round 7' prefix; every row whose subject changed was re-verified.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC8-E5-b (detached at f618cf1, .venv symlinked)",
 "scratch": "/tmp/e5b_r8_scr (lab outputs, text extracts, projects.txt)",
 "verified_at": "2026-10-29",
 "verdict": "FAIL",
 "rows": rows, "mutants": mutants, "registry_flags": registry_flags, "freshness_flags": freshness_flags, "notes": notes,
}
n_fail = sum(r["status"] == "FAIL" for r in rows); n_pass = sum(r["status"] == "PASS" for r in rows)
frag["summary"] = (f"E5 slice b (L04-L06 and twins), round 8 at f618cf1: {len(rows)} rows, {n_pass} PASS, {n_fail} FAIL. "
  "Resolved from round 7: E5b7-notation-E (page no longer uses \\E) and E5b7-xref-A3-section4 (L06.html:74 now 'leaves out'). "
  "New FAIL: E5b-plan-notation-E (plan lines 232/263 still prescribe \\E; the page's \\pi^{e}_t deviation is not recorded). "
  "Still FAIL: E5b-plan-L05-ad-from-is-lm (architect decision). All commands PASS: check_pages, check_dag, check_projects, run_labs, verify_refs, build_site --check, the three twins under -I -W error, page_smoke, ruff, mypy, pytest -k E5; page code and expected blocks equal the twins.")
json.dump(frag, open("/Users/billyribeiro/.fanout/wt/verifyC8-E5-b/ledgers/E5/E5-b.json", "w"), indent=1, ensure_ascii=False)
print(len(rows), n_pass, n_fail)
