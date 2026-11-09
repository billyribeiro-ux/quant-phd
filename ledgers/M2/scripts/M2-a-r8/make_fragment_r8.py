import json

BASE = "/Users/billyribeiro/.fanout/frags/S-M2-a.round7.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyS8-M2-a/ledgers/M2/M2-a.json"
base = json.load(open(BASE, encoding="utf-8"))
PIN = "4540351d"

NEW = {
"M2a-R1-G01": ("PASS", "Re-run at 4540351d (L06.html changed in the delta): ledgers/M2/scripts/M2-a-r8/g01_check_pages.out = 'check_pages M2: PASS', EXIT 0."),
"M2a-R1-G02": ("PASS", "Re-run: g02_check_dag.out = 'check_dag M2: PASS', EXIT 0. check_dag checks concept links only (plans/M2-build-plan.md:331)."),
"M2a-R1-G03": ("PASS", "Re-run: g03_run_labs.out = 'run_labs M2: PASS (27/27)', EXIT 0."),
"M2a-R1-G04": ("PASS", "Re-run under python -I -W error: g04_twin_L01.out .. g04_twin_L06.out, each EXIT 0 with the printed lines. Page code equals twin for all six: twin_and_cards_r8.out prints 'L0n page code == twin: True' after strip() (the one-character difference is the trailing newline). Expected blocks equal output through run_labs (G03)."),
"M2a-R1-G05": ("PASS", "Re-run: g05_pytest_labs.out, tests/test_labs.py -k 'M2 and (L01 or ... or L06)': dots, EXIT 0."),
"M2a-R1-G06": ("PASS", "Re-run: g06_page_smoke.out, 'page_smoke M2: PASS', EXIT 0 (index, L01-L06, --skip-sweep)."),
"M2a-R1-G07": ("PASS", "Re-run: g07_ruff_check.out 'All checks passed!'; g07_ruff_format.out '27 files already formatted'; g07_mypy.out 'Success: no issues found in 6 source files'; all EXIT 0."),
"M2a-R1-G08": ("PASS", "Re-run: g08_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' EXIT 0; g08_verify_refs_unit_M2.out 'live re-verification of M2: 2 of 560 entries, 0 problems' EXIT 0. references/ and tools/ have an empty git diff since aa659725."),
"M2a-R1-G09": ("PASS", "Re-run: g09_check_projects.out 'check_projects M2: PASS', EXIT 0."),
"M2a-R6-G10": ("PASS", "Re-run because cards.json changed in the delta: g10_build_site_check.out 'site data current: 6 outputs' EXIT 0; g10_pytest_build_site.out all dots, EXIT 0."),
"M2a-R1-X01": ("PASS", "Re-verified for the changed prose: L06.html:51 adds '(§2)' after Assumption 2.1; §2 starts at L06.html:69 and Assumption 2.1 is at L06.html:71-73, so the cross-reference is right. L06.html:73 narrows the rule to 'Sections 2 and 3'; the uses in §2-§3 are checked under M2a-R1-X02 and M2a-R1-L06-ASSUME-01. Process-word grep (round, verifier, grader, fixed, pinned, todo, tbd) over L06.html and cards.json finds no process word in the changed text; the hits are unchanged text ('fixed sign', 'rounding'). index.html and L01-L05 prose carried from round 7 (byte-identical since aa659725)."),
"M2a-R1-X02": ("PASS", "Re-verified from scratch at 4540351d. Structure: cards.json has 398 cards, 0 duplicate ids, 0 duplicate fronts (twin_and_cards_r8.out). Slice cards L01-L06: 84 (L01 18, L02 13, L03 14, L04 10, L05 14, L06 15). Cards changed in the delta and checked against the current lesson text: M2-c010 vs L01.html:61 and L01.html:204-206 (Misconception 1, 1/n); M2-c013 vs L01.html:196; M2-c064 vs L06.html:71-73 (no grade; the card's scope sentence is the L06.html:73 rule) and the results of Sections 2 and 3 that use Assumption 2.1, all of which begin 'Assuming Assumption 2.1': Theorem 2.2 (L06.html:77-78), Theorem 2.3 (L06.html:87-88), Corollary 3.1 (L06.html:102-103), remark L06.html:111; M2-c424 and M2-c426 vs L01.html:61 ('A sequence with a limit is convergent', 'A sequence with no limit is divergent'); M2-c427 vs L05.html:92. Cards changed in the delta outside L01-L06 (M2-c087 L07, M2-c417 and M2-c428 L08, M2-c429 L10, M2-c430 L24) are not in this slice and are not verified here."),
"M2a-R1-X-CARD-IDS": ("PASS", "Re-verified: 398 cards (393 at aa659725; c426-c430 added, none removed in this delta), 0 duplicate ids, 0 duplicate fronts (twin_and_cards_r8.out). The id-level delta changes M2-c010, c013, c064, c087, c417, c424, c428, c429, c430 and adds c426, c427 (git diff aa659725..4540351d of cards.json). The new 'convergent' (c424) and 'divergent' (c426) cards have distinct fronts."),
"M2a-R1-X-HRS-01": ("PASS", "Re-verified: data-hours='10' and '10 study hours' in the header of each of L01-L06 (grep); index.html:142 and the card grid (index.html:144-149) show 10 h each. Slice lesson hours 6 x 10 = 60; hub 24 x 10 = 240 (index.html:29 data-hours-lessons=240), project 60, total 300 (index.html:31). The changed why-it-matters paragraph L06.html:51 is supported by L06.html:69-73 (Assumption 2.1 in §2), 77-78 (Rolle) and 87-88 (mean value theorem); its '(§2)' cross-reference is right."),
"M2a-R1-X03": ("PASS", "Re-verified for the changed L06 text: the delta changes prose only (L06.html:51, 73); the math of L06 is re-derived under M2a-R1-L06-MATH-01 and -03. The delta adds no symbol. L05 and L04 math unchanged since aa659725 and carried (see L05 rows)."),
"M2a-R1-L01-CARD-01": ("PASS", "Re-verified for the delta: M2-c010 vs L01.html:61 (for each epsilon the terms are eventually within epsilon) and L01.html:204-206 (Misconception 1: 1/n has limit 0 and no term equals 0); M2-c013 vs L01.html:196 (Section 5: 'Definition 2.1 tests a proposed L. It does not produce L.'; Example 2.3 with candidate 2); M2-c424 and M2-c426 (new) vs L01.html:61 ('A sequence with a limit is convergent. A sequence with no limit is divergent.'). Other L01 cards (c001-c009, c011, c012, c376, c390, c391) are byte-identical since aa659725 and carried, with the same per-id evidence as round 7."),
"M2a-R1-L05-CARD-01": ("PASS", "Re-verified for the delta: new M2-c427 (Section 1 of L05, 'second and third derivatives') vs L05.html:92: f''(x) = (f')'(x) and f'''(x) = (f'')'(x), each when the earlier derivative is differentiable on an open interval containing x. The other 13 L05 cards (c051-c061, c379, c393) are byte-identical since aa659725 and carried: M2-c393 vs L05.html:96 (Assumption 1.4) and M2-c058 (grade C) vs the lab output line 'composite c, 95.062500000, 95.062500855, 8.55e-07' (g04_twin_L05.out)."),
"M2a-R1-L06-MATH-01": ("PASS", "Re-verified from scratch at 4540351d over L06.html:55-109 (changed line 73 is in this range): Proposition 1.1 hypotheses (L06.html:58-59) and proof (L06.html:64, the shrinking-delta step with (c-delta, c+delta) inside I, one-sided quotient inequalities, Q(h) -> f'(c)); Assumption 2.1 (L06.html:71-73); Theorem 2.2 (77-78) and proof (83), with f not constant giving M > m and M or m different from f(a); Theorem 2.3 (87-89) and proof (94), g(x) = f(x) - f(a) - s(x - a) with g(a) = g(b) = 0; Corollary 3.1 (102-103) and proof (108). No gap found in the proofs."),
"M2a-R1-L06-MATH-03": ("PASS", "Re-verified from scratch at 4540351d over the problem set (L06.html:216-312) and key rows (L06.html:321-326): M1 f' = 2x - 4, critical point 2, f(2) = -3 (L06.html:218-220); M2 c = 2/sqrt(3) in (0, 2) (L06.html:227); M3 f' = 3(x-1)(x+1) > 0 on (-2, -1) and f(-2) = -2 < 2 = f(-1) (L06.html:232-234); P1-P3 (L06.html:243-259); E1-E3 (L06.html:267-284, midpoints are odd multiples of 1/8, so none is +-1, which are even multiples); R1 (L06.html:293-295); R2 (L06.html:300-302: chord slope 0, f' = -1 on (0,1), f' = 1 on (1,2)); R3 (L06.html:307-309). Key rows 321-324 are T with the opening 'Assuming Assumption 2.1' where they use it; row 325 is not graded; row 326 is the grade-C lab result (see M2a-R7-L06-KEYROW-326)."),
"M2a-R1-L06-ASSUME-01": ("PASS", "Re-verified from scratch at 4540351d under the narrowed rule at L06.html:73 ('Every result in Sections 2 and 3 that uses it begins its statement with \"Assuming Assumption 2.1\"'), which L06.html:325 repeats. The results of Sections 2 and 3 that use Assumption 2.1 are Theorem 2.2 (L06.html:77-78), Theorem 2.3 (L06.html:87-88), Corollary 3.1 (L06.html:102-103) and the remark at L06.html:111; each statement begins with the opening. Proof sentences (L06.html:83, 94, 108) are not statements. The Lab 1 prediction at L06.html:115 has its Assumption-dependent claim after the opening 'Assuming Assumption 2.1, f is increasing ...'. Uses in §5-§7 are outside the narrowed scope; the problem prompts (L06.html:218, 232) say 'under Assumption 2.1' and are not results (LOW). Assumption 2.1 is not graded (L06.html:73, 325)."),
"M2a-R1-L06-CARD-01": ("PASS", "Re-verified from scratch at 4540351d for all 15 Lesson 6 cards (M2-c062 to c074, c394, c414): c062 vs L06.html:55; c063 vs L06.html:57-59 and 67; c064 (changed) vs L06.html:71-73, and its scope sentence now matches the rule at L06.html:73; c065 vs L06.html:77-78; c066 vs L06.html:87-89 and proof 94; c067 vs L06.html:102-103; c068 vs L06.html:111 and Misconception 2 (L06.html:199-201, direct proof); c069 and c070 vs the lab output (g04_twin_L06.out: 8 of 16; f(-1) = 2, f(1) = -2); c071 vs L06.html:196-197; c072 vs L06.html:204-205; c073 vs L06.html:186; c074 vs L06.html:99; c394 (changed in round 7) vs L06.html:307 (the card's 'for all x and y' is over the domain of f, which is R in R3; LOW wording); c414 (changed) vs L06.html:55. No duplicate fronts in the unit."),
"M2a-R7-L06-KEYROW-326": ("PASS", "Re-verified at 4540351d: key-results row L06.html:326 sits in Section 7 (L06.html:315-330), which the narrowed rule at L06.html:73 and L06.html:325 ('every result in §2 and §3') no longer covers. Its Result is a grade-C Lab 1 fact: 8 of 16 grid intervals increase, f(-1) = 2, f(1) = -2. g04_twin_L06.out prints 'grid intervals on which f increases: 8 of 16' and 'f(-1) = 2; f(1) = -2' (exact Fraction arithmetic, EXIT 0). The Source column gives the derivation with the explicit hypothesis 'assuming Assumption 2.1 (Corollary 3.1)', and the row claims no graded theorem. No missing hypothesis, so PASS."),
}

def files_for(rid):
    if ".H0" in rid or "-H0" in rid or "H08b" in rid:
        return "course/modules/M/M2/index.html (and L04.html, L13.html for H07)"
    if rid.startswith("M2a-R1-X") or rid.startswith("M2a-R1-X-"):
        return "course/modules/M/M2/index.html and L01.html-L05.html, with their twins"
    for n in range(1, 6):
        if f"-L0{n}-" in rid:
            return f"course/modules/M/M2/L0{n}.html and tests/labs/M2/lab-M2-L0{n}-1.py"
    if "-L06-" in rid:
        return "course/modules/M/M2/L06.html lines outside the round-8 changes and tests/labs/M2/lab-M2-L06-1.py"
    return "course/modules/M/M2 slice files"

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, ev = NEW[rid]
    else:
        status = r["status"]
        assert status == "PASS", rid
        ev = (f"Carried from round 7 ({files_for(rid)} byte-identical since aa659725; "
              f"git diff aa659725..{PIN} over the slice paths does not touch them): " + r["evidence"])
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})

assert all(r["status"] == "PASS" for r in rows)
assert len(rows) == len(base["rows"]) == 75
assert set(NEW) <= {r["id"] for r in base["rows"]}

frag = {
    "unit": "M2",
    "slice": "a",
    "round": 8,
    "verifier": "independent verifier (Haiku 5.5), unit M2 slice a, round 8 (closing delta verification, rulings 30 and 37)",
    "pin": f"{PIN} (detached checkout HEAD; slice delta aa659725..{PIN}, one commit)",
    "base": "Round-7 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round7.json (verified at pin aa659725; FAIL rows re-verified from scratch).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS8-M2-a",
    "scratch": "ledgers/M2/scripts/M2-a-r8/",
    "verified_at": "2026-11-09",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice diff aa659725..4540351d over course/modules/M/M2, tests/labs/M2, tests/test_labs.py, tools/, references/ and course/assets/data: only course/modules/M/M2/L06.html (lines 51 and 73) and course/modules/M/M2/cards.json changed. index.html, L01-L05, all six twins, tools/, references/ are unchanged.",
        "Round-7 FAIL rows M2a-R1-X02, M2a-R1-L06-CARD-01, M2a-R1-L06-ASSUME-01 and M2a-R7-L06-KEYROW-326 are PASS now: the ruling narrows the rule at L06.html:73 (and L06.html:325) to Sections 2 and 3; M2-c064 states the same narrowed scope; key-results row L06.html:326 is in Section 7 and is a correct grade-C lab fact.",
        "Lesson 6 rule at L06.html:73 now reads 'Every result in Sections 2 and 3 that uses it'. Every §2-§3 result that uses Assumption 2.1 begins with the opening (L06.html:77-78, 87-88, 102-103, 111).",
        "Cards changed in the delta outside L01-L06 (not verified in this slice, owned by the slices of L07, L08, L10, L24): M2-c087 (L07), M2-c417 and M2-c428 (L08), M2-c429 (L10), M2-c430 (L24). The base round also noted removals of M2-c129, c160, c208, c419 at aa659725.",
        "LOW, not ruling-26 kinds: M2-c394 says 'for all x and y' without naming the domain (R3 is on R); L06.html:218 and 232 prompts say 'under Assumption 2.1' rather than 'Assuming' (problems are not results); L06.html:179 interpretation uses 'fixed sign' (unchanged text).",
        "LOW carried from round 7: slice cards without a grade key (c001-c003, c007, c010, c013, c014, c020, c027, c031, c039-c041, c062, c064, c074, c379, c390-c394, c414, c424, c426, c427) are card style, not a result; near-duplicate cards c010/c013 remain distinct.",
        "Mutants: none. The slice has no project grader (ruling 26 mutation applies to project graders only), so mutants is empty by design, as in round 7.",
        "Not checked: lessons L07-L24 and project.html (other slices); no browser screenshot (page_smoke only); cards outside the slice beyond their ids and their delta text; the live verify_refs run was executed (2 of 560 entries) but the other 558 entries were checked offline only.",
    ],
    "summary": ("M2 slice a, round 8 (closing delta verification at 4540351d, rulings 30 and 37). 75 rows: 75 PASS, 0 FAIL, 0 UNVERIFIABLE. "
                "The four round-7 FAIL rows (X02, L06-CARD-01, L06-ASSUME-01, KEYROW-326) are re-verified from scratch under the narrowed Sections 2 and 3 scope and PASS. "
                "Rows whose subject changed were re-verified: X01, X02, X03, X-CARD-IDS, X-HRS-01, L01-CARD-01, L05-CARD-01, L06-MATH-01, L06-MATH-03, L06-CARD-01. "
                "All gates G01-G10 were re-run at 4540351d and pass; the other rows are carried from round 7 with the carry prefix."),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(rows), "rows")
