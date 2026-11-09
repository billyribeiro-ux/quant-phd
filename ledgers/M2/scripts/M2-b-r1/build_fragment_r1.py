# Round-1 closing-delta fragment for M2 slice b (pin 95f3f8cb, previous pin e896b7a4). Writes ledgers/M2/M2-b.json.
import json, datetime
PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
BASE = "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a"
S = "ledgers/M2/scripts/M2-b-r1/"
PAGES6 = "course/modules/M/M2/L07.html..L12.html"
def carry(files, text):
    return f"Carried from round 6 ({files} byte-identical since the previous pin {BASE[:8]}): {text}"
ID = "L07.html, L08.html, L09.html, L10.html, L11.html, L12.html and the six twins"
rows = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix:
        r["fix"] = fix
    rows.append(r)

# Gate rows, re-run from scratch at 95f3f8cb (outputs in S).
row("RUN-M2-CHECKS", "2.9 gates: check_pages, check_dag, check_projects, run_labs (unit M2) and the --all static gates",
    "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2",
    "PASS", f"Fresh at {PIN[:8]}: {S}g01_check_pages_M2.out 'check_pages M2: PASS' exit 0; g02 'check_dag M2: PASS' exit 0; "
    f"g03 'check_projects M2: PASS' exit 0; g04 'run_labs M2: PASS (27/27)' exit 0; g04b/c/d (--all) LX1, LX2, PC3 PASS exit 0. "
    f"Command record: {S}run_gates_r1.sh.")
row("LAB-GATES", "2.5 labs: ruff check and format, mypy strict, pytest subset on the slice",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "PASS", f"Fresh: {S}g07 ruff check tests/labs/M2 'All checks passed!' exit 0; g07b ruff format --check '27 files already formatted' exit 0; "
    f"g08 'mypy --no-incremental': 'Success: no issues found in 386 source files' exit 0; g09 pytest (test_labs, test_run_labs, test_page_checks, test_refs, test_page_smoke, -k 'M2 or lab or page or refs') exit 0, 533 collected (g09b_pytest_collect.out).")
row("PAGE-SMOKE-L07-L12", "2.6 page_smoke for the slice pages, alone",
    "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12",
    "PASS", f"Fresh: {S}g06_page_smoke_L07_L12.out 'page_smoke M2: PASS', exit 0.")
row("TWIN-ISOLATED", "twins run alone under python -I -W error, exit 0, empty stderr",
    "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "PASS", f"Fresh, from the checkout: {S}twin_L07..L12 .stdout/.stderr; exit 0 for all six, stderr 0 bytes for all six (command: cd tests/labs/M2 && .venv/bin/python -I -W error lab-M2-LNN-1.py).")
row("REFS-OFFLINE", "reference registry integrity for the slice pages",
    "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2; tools/build_site.py --check; course/modules/M/M2/L07.html..L12.html",
    "PASS", f"Fresh: {S}g10 'offline integrity: 560 entries, 0 problems' exit 0; g12 'live re-verification of M2: 2 of 560 entries, 0 problems' exit 0; g11 'site data current: 6 outputs' exit 0. references/references.json byte-identical to e896b7a4 (carry_identity_r1.out).")

row("DELTA-HUNKS", "closing delta e896b7a4..95f3f8cb over the slice paths (ruling 30): every changed subject re-verified",
    "course/modules/M/M2/cards.json (slice cards); course/modules/M/M2/L07-L12.html and six twins (unchanged)",
    "PASS", f"git diff --name-only e896b7a4..HEAD -- course/modules/M/M2 lists L04.html, L05.html, L06.html (M2-a slice, not graded here) and cards.json. "
    f"Slice pages L07-L12 and the six twins are byte-identical (carry_identity_r1.out). Slice card delta (card_delta_r1.out): changed M2-c087, c161 (L11), c169, c176 (L12), c417, c421, c422, c423, c425; added M2-c428 (L08), M2-c429 (L10); removed M2-c129 (L09), M2-c160 (L11). Each changed or added card is verified in its CARD row. "
    f"ledgers/M2/mutants, tools/, notation/, references/ and tests/labs/M2 unchanged (diff 0). Out-of-slice card changes not graded (ruling 30): see notes.")

card_l07 = ("Re-verified from scratch. M2-c087 (Lemma 3.1): hypothesis '0 <= t < 1' matches L07.html:318-319 (grade T, Lemma 3.1); proof at L07.html:324 covers t = 0 and 0 < t < 1 (the t = 1/(1+h) step is for 0 < t < 1). "
    "M2-c422: back 'checks the identity exactly at each degree n from 0 to 10 for x = 3/10, each error 3/10 times the error one degree lower' matches tests/labs/M2/lab-M2-L07-1.py part_b (Fraction arithmetic; error != X_B**(n+1)/(1-X_B) raises; ratio check for n >= 1) and the hypothesis sentence at L07.html:135. "
    "Observation (not a ruling-26 kind): c422 carries basis 'Lab 1, part B (printed decimals)' and grade C, but the identity is Proposition 2.3 (L07.html:118, grade T) and the check is exact; the basis text is stale from the earlier printed-decimal version. Recommend grade T citing Proposition 2.3.")
row("CARD-L07", "cards for lesson L07 agree with L07.html; hypotheses carried; numbers appear in the lesson",
    "course/modules/M/M2/cards.json: M2-c087, M2-c422 (changed); other 22 L07 cards identical", "PASS", card_l07)

row("CARD-L08", "cards for lesson L08 agree with L08.html; hypotheses carried; no duplicate",
    "course/modules/M/M2/cards.json: M2-c417 (changed), M2-c428 (added); M2-c113 identical",
    "PASS", "Re-verified from scratch. M2-c417 (grade T) states Theorem 1.2 with 'Assuming Assumption 1.1, let p < q ... phi(p) = phi(q) ... phi'(c) = 0 for some c with p < c < q' = L08.html:76-77; "
    "'special case of the mean value theorem (Theorem 2.3 of Lesson 6) ... Lesson 8 uses it in no other form (Remark 1.3)' = L08.html:81-82 (Remark 1.3 text: 'This lesson uses it in no other form'). "
    "M2-c428 (no grade): 'Assumption 1.1 ... continuous on a closed interval [p, q] with p < q attains a maximum and a minimum ... Assumption 2.1 of Lesson 6, no grade given' = L08.html:61-62 ('No grade is given to it here'). "
    "Lesson 6 is in L08 'Uses' (L08.html:38), so the cross-lesson cites are prerequisites. M2-c113 byte-identical to e896b7a4 (carry). Observation: c417 restates Rolle's theorem that also appears as M2-c065 (L06); same theorem, lesson-specific framing; not a ruling-26 kind.")

row("CARD-L09", "cards for lesson L09 agree with L09.html; hypotheses carried; duplicates removed",
    "course/modules/M/M2/cards.json: M2-c423, M2-c425 (changed); M2-c129 (removed); 17 other L09 cards identical",
    "PASS", "Re-verified from scratch. M2-c423 (no grade): sums 1/8 and 1/8 for x(1-x), n = 2 (L09.html:280); integral 1/6 'a forward reference to Lesson 10, Theorem 2.1 (under Assumption 2.1 of Lesson 6) that Lesson 9 does not derive' = L09.html:280 (hypothesis carried); bracket by suprema and infima = Definition 1.3 (L09.html:85-86) and Misconception 2 (L09.html:280). "
    "M2-c425 (grade T): 'Theorem 2.2 and Corollary 2.3 are for monotone f only' = L09.html:91 (Remark 1.4), L09.html:99-100 (Theorem 2.2 monotone), L09.html:114-115 (Corollary 2.3 monotone); 'x(1 - x) ... not monotone on [0, 1]' true (rises to 1/4 at 1/2); integrability of x(1-x) 'cited from later lessons' = L09.html:91 and L09.html:280 (Lesson 11, Lemma 1.1). "
    "Removed M2-c129 (grade T) asked the same endpoint-sum question for the same integrand as M2-c423 (duplicate removed). Carried: M2-c423 vs M2-c425 not duplicates.")

row("CARD-L10", "cards for lesson L10 agree with L10.html; hypotheses carried; no duplicate",
    "course/modules/M/M2/cards.json: M2-c421 (changed), M2-c429 (added); M2-c135 identical",
    "PASS", "Re-verified from scratch. M2-c421 (no grade): 'F(b) - F(a): the value of F at b minus its value at a' with Theorem 2.1 (L10.html:76-77) in Section 2; the removed sentence is not needed. "
    "M2-c429 (grade T): 'Assuming Assumption 2.1 of Lesson 6, let p < q. If phi is continuous on [p, q] and differentiable on (p, q), then there is c with p < c < q and phi(q) - phi(p) = phi'(c)(q - p)' = L10.html:62-63 (grade T, 'Theorem 1.2 (mean value theorem, Theorem 2.3 of Lesson 6)'); 'used here without reproof (Remark 1.3)' = L10.html:67-68. "
    "Observation (not a ruling-26 kind): M2-c429 and M2-c066 (L06, 'Theorem 2.3 (mean value theorem)') ask the same question about the same theorem in two lessons (difflib ratio 0.86); not a false, unproved, or mis-hypothesised statement.")

row("CARD-L11", "cards for lesson L11 agree with L11.html; hypotheses carried; grade and content consistent",
    "course/modules/M/M2/cards.json: M2-c161 (changed), M2-c160 (removed); other L11 cards identical",
    "FAIL", "Re-verified from scratch. M2-c161 (grade T): 'It gives the integral of x from 0 to 1 equal to minus itself, which forces that integral to be 0. It is 1/2, so the boundary term 1 is needed. The boundary term is not always zero: it vanishes in Example 2.2 only because v(1) = 0 and u(0) = 0 (Misconception 1)'. "
    "The content matches L11.html:103-104 (Example 2.3: boundary term 1; integral 1/2), L11.html:236-237 (Misconception 1: dropping it gives the integral = minus itself) and L11.html:97 (Example 2.2: v(1) = 0, u(0) = 0). "
    "But Example 2.3 proves the integral 1/2 and the identity 'Under Assumption 2.1 of Lesson 6, Theorem 2.1 applies' (L11.html:104) and Theorem 2.1 is stated under Assumption 2.1 (L11.html:84-86). The card states '1/2' and the identity as T results with no Assumption 2.1 qualifier (missing hypothesis, ruling 26). "
    "Removed M2-c160 is a limits question, fine. Same omission exists in unchanged M2-c152 (grade T, '1/2 (Example 2.3)') and M2-c150/153 carry the assumption.",
    fix="In M2-c161 back, qualify the T claim: append 'under Assumption 2.1 of Lesson 6' after 'It is 1/2' (or after 'Example 2.3'), as M2-c150 and M2-c168 do. Apply the same convention to unchanged M2-c152 in the same pass, or the architect rules that answer cards cite results without restating assumptions.")

row("CARD-L12", "cards for lesson L12 agree with L12.html; hypotheses carried; no duplicate",
    "course/modules/M/M2/cards.json: M2-c169, M2-c176 (changed); other 15 L12 cards identical",
    "FAIL", "Re-verified from scratch. M2-c176 (grade T): 'The integrand tends to 0, yet the integral from 1 to infinity of dx/x diverges (Theorem 3.3, Remark 3.4). (Misconception 2)' matches L12.html:223-224 (Theorem 3.3), L12.html:233-234 (Remark 3.4), and the second misconception item L12.html:253-255. PASS. "
    "M2-c169 (grade T): values 1 (p = 2) and 1/2 (p = 3) match L12.html:96 (Example 2.3). But the card cites 'Theorem 2.2' with no hypothesis. Theorem 2.2 is stated 'Assuming Assumption 2.1 of Lesson 6' (L12.html:81-82) and Example 2.3 says 'By Theorem 2.2 (under Assumption 2.1)' (L12.html:96). The card carries no Assumption 2.1 and grades T (missing hypothesis, ruling 26). "
    "Sibling M2-c168 (L12) carries 'Assuming Assumption 2.1'. Same omission in unchanged M2-c178 ('for every integer p >= 2 it converges (Theorem 2.2)').",
    fix="In M2-c169 back, change to '(Example 2.3, from Theorem 2.2 under Assumption 2.1 of Lesson 6)'. Apply the same qualifier to unchanged M2-c178 in the same pass.")

row("CARD-DUP", "no duplicate ids, no duplicate fronts across all cards.json; near-duplicates reviewed",
    "course/modules/M/M2/cards.json (all 398 cards)", "PASS",
    f"card_delta_r1.py / card_delta_r1.out: 398 cards, 0 duplicate ids, 0 duplicate normalized fronts. Near-duplicate fronts (ratio >= 0.8) reviewed: M2-c429 vs M2-c066 (0.86, same MVT question in two lessons; observation, not a ruling-26 kind); M2-c423 vs removed M2-c129 duplicate resolved by the removal; all other pairs ask different items (different lab parts, propositions, or integrands). Near-duplicate backs: M2-c346/c385 (0.93), M2-c188/c189 (0.83), outside the slice.")

row("XREF-L07-L12", "cross-references between pages and cards resolve",
    "course/modules/M/M2/L07.html..L12.html; cards M2-c113, M2-c135, M2-c425; L10 key-results row 5",
    "PASS", "M2-c425 cites Remark 1.4 (L09.html:90-91, present). M2-c422 cites Lab 1 part B (present, L07.html:135). M2-c417 cites Remark 1.3 (L08.html:81, present). M2-c429 cites Remark 1.3 (L10.html:67, present). M2-c113 and M2-c135 byte-identical (carry). L10 key-results row 5 (L10.html:390): L10 identical (carry).")

row("DAG-L07-L12", "concepts used outside the prerequisite closure, by name or link (cards included)",
    "course/modules/M/M2/L07.html..L12.html; changed cards", "PASS",
    "Pages carried (byte-identical). Changed and added cards contain no dfn or concept link. Cross-lesson card cites: M2-c417, M2-c428 cite Lesson 6 (L08 'Uses' L08.html:38 names Lesson 6 Rolle); M2-c429 cites Lesson 6 (L10 'Uses' L10.html:38 names the mean value theorem of Lesson 6); M2-c423 cites Lesson 10 Theorem 2.1 as a forward reference named as such in L09.html:280 (prose-only, no concept, no link; M2-build-plan.md section 2 lists no L09 concept at stake).")

row("PROSE-PROCESS", "no process words in learner text (verifier rules item 12)",
    "course/modules/M/M2/L07.html..L12.html; changed and added cards", "PASS",
    f"Pages carried (byte-identical). Changed and added cards scanned by {S}prose_cards_r1.py: 11 cards, 0 hits (round, verifier, ledger, fix, delta, changed, now, earlier, version, ruling).")
row("PROSE-BANNED", "banned strings (BUILDER_RULES 1.3-1.4) absent from learner text",
    "course/modules/M/M2/L07.html..L12.html; changed and added cards", "PASS",
    f"Pages carried. Changed and added cards: {S}prose_cards_r1.py, 0 hits (TODO, TBD, lorem, obviously, clearly, it can be shown, ..., studies show, and others).")

row("NOT-L09-R", "L09 Section 1 notation (carry)", "course/modules/M/M2/L09.html Section 1", "PASS",
    carry("course/modules/M/M2/L09.html", "L09 Section 1 notation re-read in round 6; L09 unchanged."))
row("NOT-GLOBAL", "every symbol on the slice pages matches notation/notation.json (carry)",
    "course/modules/M/M2/L07.html..L12.html; notation/notation.json", "PASS",
    carry("course/modules/M/M2/L07.html..L12.html and notation/notation.json", "notation registry (8 symbols) identical; the changed cards use only local letters (phi, c, p, q, F, G) that notation.json does not register."))
row("HOURS-L07-L12", "hours arithmetic: lesson data-hours and hub split (carry)",
    "course/modules/M/M2/L07.html..L12.html eyebrow and data-hours; course/modules/M/M2/index.html", "PASS",
    carry("the six slice pages and index.html", "data-hours=\"10\" on each of L07.html..L12.html and data-hours-lessons=\"240\" on index.html (grep re-run at 95f3f8cb: six lessons of 10 h; the lesson total 240 is the hub value; 240/24 = 10 per lesson for L01-L24)."))
row("GRADE-L07-L12", "data-grade spans on the slice pages match the claims (carry)",
    "course/modules/M/M2/L07.html..L12.html data-grade spans; L10 key-results table", "PASS",
    carry("the six slice pages", "grade spans read in round 6; pages unchanged."))

for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    row(f"STRUCT-{L}", f"structure of {L}: sections, blocks, interpretations, quiz (carry)", f"course/modules/M/M2/{L}.html", "PASS",
        carry(f"course/modules/M/M2/{L}.html", "page read in full in round 6; unchanged."))
    row(f"NUM-{L}", f"numbers in prose match unrounded values (carry)", f"course/modules/M/M2/{L}.html", "PASS",
        carry(f"course/modules/M/M2/{L}.html", "numbers re-derived in round 6 (numbers_L10_r6.py for L10); page unchanged."))
    row(f"MATH-{L}", f"proofs and statements graded T are proved with their hypotheses (carry)", f"course/modules/M/M2/{L}.html", "PASS",
        carry(f"course/modules/M/M2/{L}.html", "proofs read in round 6; page unchanged."))
    row(f"LAB-{L}", f"lab {L} twin: page code equals twin, expected block equals output, twin isolated (carry; run_labs fresh in RUN-M2-CHECKS)",
        f"course/modules/M/M2/{L}.html lab section; tests/labs/M2/lab-M2-{L}-1.py", "PASS",
        carry(f"course/modules/M/M2/{L}.html and tests/labs/M2/lab-M2-{L}-1.py", "run_labs 27/27 and isolated run fresh at 95f3f8cb (RUN-M2-CHECKS, TWIN-ISOLATED)."))

row("LAB-L07-DOC", "L07 lab docstring and interpretation match the code (carry)",
    "tests/labs/M2/lab-M2-L07-1.py (g_prime_formula, part D); course/modules/M/M2/L07.html:309", "PASS",
    carry("tests/labs/M2/lab-M2-L07-1.py and L07.html", "docstring and interpretation re-read in round 6; both identical."))
row("LINK-L11-chain", "L11 Lemma and Theorem links resolve to the lessons they cite (carry)",
    "course/modules/M/M2/L11.html:38 and Sections 2-3", "PASS", carry("L11.html", "re-read in round 6."))
row("PROOF-L11-hyp", "L11 integration-by-parts hypotheses checked in the proof (carry)",
    "course/modules/M/M2/L11.html:83-124", "PASS", carry("L11.html", "re-read in round 6."))
row("PROOF-L12-integrability", "L12 integrability hypotheses checked in the proof (carry)",
    "course/modules/M/M2/L12.html:81-92 and 217-220", "PASS", carry("L12.html", "re-read in round 6."))
row("QUIZ-L07-L12", "quiz answers match the lesson text (carry)",
    "course/modules/M/M2/L07.html..L12.html quiz sections", "PASS", carry("the six slice pages", "quiz read in round 6; pages unchanged."))
row("MUTANTS-NA", "mutant set (project graders only; M2 has none in this slice; ruling 37: no new mutants)",
    "ledgers/M2/mutants/", "PASS", carry("ledgers/M2/mutants/", "git diff e896b7a4..HEAD -- ledgers/M2/mutants is empty (0 files); no new mutants authored in this closing round (ruling 37)."))
row("KR-L10", "L10 key-results row 5 cites the right source (carry)",
    "course/modules/M/M2/L10.html:390", "PASS", carry("course/modules/M/M2/L10.html", "source cell unchanged; re-read in round 6."))

frag = {
    "unit": "M2",
    "slice": "b",
    "round": 1,
    "verifier": "independent Haiku verifier, M2 slice b, closing delta (rulings 30, 37); fresh context, no builder context",
    "pin": PIN,
    "base": f"{BASE} (round-6 fragment ~/.fanout/frags/S-M2-b.round6.json, verdict PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M2-b (detached at 95f3f8cb, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyF21-M2-b/ledgers/M2/scripts/M2-b-r1",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round label: the task fixes round=1 for this closing delta; the base fragment is round 6 (pin e896b7a4). Carry prefixes cite round 6 as the previous round.",
        "Delta scope (ruling 30): git diff e896b7a4..95f3f8cb over the slice paths. Pages L07-L12, the six twins, index.html, notation, references, tools, tests/labs/M2 and ledgers/M2/mutants are byte-identical; the only slice subject that changed is course/modules/M/M2/cards.json.",
        "Out of slice, not graded (ruling 30; belongs to M2-a or another owner): L04.html, L05.html, L06.html hunks (M2-a); cards M2-c010, c013 (grade T removed), c044, c064, c187 (L13), c263 (L17), c334 (L22), c394, c414, c424 (L01, L04, L06, L01); added M2-c426 (L01), M2-c427 (L05), M2-c430 (L24); removed M2-c048 (L04), c208 (L14), c419 (L15). Observation for the M2-a owner: L05.html:92 now defines f'' and f''' in prose, while L07.html:59 (Definition 1.1, higher derivative) defines them again; M2-c427 (L05) asks the same question.",
        "Observation (not a ruling-26 kind): M2-c422 basis 'printed decimals' is stale and grade C understates a Proposition 2.3 (T) result; the check is exact (lab-M2-L07-1.py part B).",
        "Observation (not a ruling-26 kind): M2-c429 and M2-c066 ask the same MVT question in L10 and L06; M2-c417 and M2-c065 restate Rolle in L08 and L06.",
        "Missing-hypothesis convention: M2-c150, c153, c168, c137, c142, c149, c159 carry 'Assuming Assumption 2.1 of Lesson 6'; answer cards M2-c161 (changed), M2-c169 (changed), and unchanged M2-c152, c178, c147, c134 do not. The two changed cards are FAIL; the unchanged ones are listed for the same pass or an architect ruling on answer cards.",
        "Mutants: none authored (ruling 37). M2 slice b has no project grader; the standing mutant set for M2 is empty in this slice (MUTANTS-NA).",
        "Exemplar calibration: not applicable (lesson slice, not a rubric slice).",
        "Not checked in this round: full line-by-line re-read of the carried pages (carried by byte identity per ruling 30); the 533 pytest collected tests were run only as the subset selected by -k, not as the full suite.",
    ],
    "summary": "M2-b closing delta (round 1, pin 95f3f8cb, previous e896b7a4): 52 rows; FAIL 2 (CARD-L11 M2-c161, CARD-L12 M2-c169: missing Assumption 2.1 qualifier on T-graded answer cards); the gate rows, the other card rows, and all carried rows PASS.",
}
json.dump(frag, open("ledgers/M2/M2-b.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open("ledgers/M2/M2-b.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "fails", [r["id"] for r in rows if r["status"] != "PASS"])
