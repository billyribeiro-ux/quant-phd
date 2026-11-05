"""Write the round-10 SC1-e fragment from the rows above (values only; no computed claims)."""
import json
import sys

out_path = sys.argv[1]
rows = [
    ("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json", "PASS",
     "scan_r10.py -> out/scan_r10.out: 206 cards, 206 distinct ids, all match SC1-cNNN; keys are back, basis, cite, front, grade, id, lesson (or without basis/grade for definitional cards); per lesson L01 24, L02 28, L03 20, L04 25, L05 33, L06 28, L07 25, L08 23; check_pages SC1 PASS (out/check_pages.txt). Ids are not in file order (c186 and c206 to c219 appended), which no rule requires."),
    ("SC1e-full-read-cards", "2.7-cards", "course/modules/SC/SC1/cards.json (all 206 cards)", "PASS",
     "All 206 fronts and backs read in out/cards_L01.txt to out/cards_L08.txt (dump_cards.py). Each card checked against current lesson text in the rows SC1e-L01-statements to SC1e-L08-statements, with the changed cards of the round-9 to pin delta (out/delta_r9_to_pin.diff) re-checked against lesson text."),
    ("SC1e-full-read-lessons", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html", "UNVERIFIABLE",
     "Rendered L01 to L08 with html_to_text.py (out/L01.txt to out/L08.txt, 344,057 bytes). This round read in full every lesson hunk of the round-9 to pin delta (out/delta_r9_to_pin.diff: L02 to L08, L01 unchanged) and every lesson section cited by a card that changed or whose cited lesson text changed. The unchanged remainder of L02 to L08 was NOT re-read line by line in this round (context budget), so it is not claimed as read now. Round-9 reading of that remainder is not carried because the lesson files changed."),
    ("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all pairs)", "PASS",
     "scan_r10.py -> out/scan_r10.out: no identical front, no identical back. SequenceMatcher ratio >= 0.6 on front+back: c064/c202 0.792 (Assumptions 4.2(a) and 4.2(b)), c170/c218 0.718 (90114 pairs versus 78 pairs), c116/c117 0.703 (Lemma 2.1(i) versus (ii)), c161/c167 0.672, c137/c139 0.655 (Theorem 1.3 versus Corollary 1.5(a)), c206/c211 0.628, c196/c198 0.626, c067/c068 0.601, c081/c082 0.600. Each pair asks a different fact."),
    ("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text", "PASS",
     "scan_r10.py: no process word (builder, verifier, round, fixer, ledger, reviewer, sub-agent) in any card. grep -i population over cards.json and out/L01 to L08: no hits (out/grep_population_r10.out, empty)."),
    ("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a numeric token", "PASS",
     "scan_r10.py: 307 numeric tokens (decimals and 2+ digit numbers) in the cards, 0 absent from the card's own lesson text. Substring test, therefore weak; values recomputed in SC1e-numbers-recomputed."),
    ("SC1e-numbers-recomputed", "2.2-numbers", "cards c010, c051, c053, c111 to c114, c115, c124, c148 to c150, c159, c170 to c174, c183, c187, c201, c205", "PASS",
     "recompute_r10.py -> out/recompute_r10.out (no lab code imported): c111 1014 triples, c112 78 pairs, c170 sum n*2^n (n=1..12) = 90114 over 8190 sequences, c113 P(M10>=2)=281/512, 2P(S10>2)=11/32, P(S10=2)=105/512, c114 495 and 495 of 4096 walks, c129 5 of 8, c148 14893+6885=21778 (0.332306), c171 counts 512,0,384,0,288,0,224,0,180,0 sum 1588 and 794/4096, c172 exact truncated means 5.480560, 11.815731, 24.557203. numbers_inline_r10.py -> out/numbers_inline_r10.out: c115 erfc(1/sqrt2)=0.3173105079, c174 densities 0.241971 and 0.109848, P(tau_1<=2)=0.4795, c053 2*sqrt2/20=0.14142 and 0.0125, c149 SE 0.0210 and 0.0230, c150 gap 1.239 SE, c159 SE 0.0230, c187 gap +13.21% at H=2,N=1 and -6.6% at H=2,N=2, c183 log-derivative zero at H=a^2/3, c201 1-Phi(1)=0.1586552539. All agree with the card numbers."),
    ("SC1e-L03-gap", "2.5-labs", "course/modules/SC/SC1/L03.html Lab 1 expected block; cards c051, c052, c187", "PASS",
     "out/lab_L03.stdout (twin run python -I -W error, exit 0): H=2,N=1 se 0.1601 against 2*sqrt2/20=0.141421, relative +13.2%; H=2,N=2 se 0.0934 against 0.1, -6.6%; largest |z| other than H=1,N=2 is 1.84 (H=1,N=128). Card c187 says within 14 percent and largest +13.2 percent at H=2,N=1: agrees. Card c051 says largest |z|=2.39 at H=1,N=2 and no other above 1.84: agrees."),
    ("SC1e-labs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py", "PASS",
     "tools/run_labs.py --unit SC1 -> out/run_labs.txt: 'run_labs SC1: PASS (11/11)', exit 0. Each of the eight lesson twins run alone with python -I -W error: exit 0 (out/lab_L01.stdout to out/lab_L08.stdout)."),
    ("SC1e-labs-page-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html (data-run and expected blocks)", "PASS",
     "embed_check_r10.py <repo> -> out/embed_check_r10.out: for L01 to L08 the page code equals the twin and the expected block equals the twin stdout (exit 0, one run each)."),
    ("SC1e-page-smoke", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html", "PASS",
     "tools/page_smoke.py --unit SC1 --pages L01 ... L08 -> out/page_smoke.txt: 'page_smoke SC1: PASS', exit 0."),
    ("SC1e-check-pages-dag", "2.9-prose", "course/modules/SC/SC1/", "PASS",
     "tools/check_pages.py --unit SC1 -> out/check_pages.txt 'check_pages SC1: PASS' exit 0; tools/check_dag.py --unit SC1 -> out/check_dag.txt 'check_dag SC1: PASS' exit 0."),
    ("SC1e-delta-read", "2.7-cards", "cards.json and L01 to L08 html since c93dd526", "PASS",
     "git merge-base --is-ancestor c93dd526 HEAD: ancestor. out/delta_r9_to_pin.diff: every hunk of cards.json (c008, c035, c052, c053, c084, c086, c087, c102, c117, c118, c139, c140, c145, c150, c164, c165, c170, c193 changed; c219 added) and of L02 to L08 html (L01 html unchanged; tests/labs/SC1 and notation unchanged) was read in full. Hunks in L07 and L08 longer than the display width were read to their tails."),
    ("SC1e-c048-round7", "2.9-prose", "course/modules/SC/SC1/cards.json card SC1-c048; L03.html Theorem 2.3", "PASS",
     "c048 front and back read this round: Assumption 3.2 and 3.1, Q(P_n) to t in mean square, error at most 2t|P_n|. L03.txt Theorem 2.3 section is not in the delta (out/delta_r9_to_pin.diff hunks are at L03 html lines 51 and 382), so the statement is unchanged; it matches."),
    ("SC1e-L01-statements", "2.9-prose", "course/modules/SC/SC1/L01.html; cards SC1-c001 to c017, c186, c206 to c210, c219", "PASS",
     "Carried from round 9 (L01.html byte-identical since c93dd526; delta out/delta_r9_to_pin.diff has no L01 hunk) for cards c001 to c007, c009 to c017, c186, c206 to c210. Re-checked this round: c008 against L01.txt lines 88 to 100 (Remark 1.3 hypotheses and conclusion, mean 0, covariance min(t_i,t_j)); c219 (new) against L01.txt line 100 (Gaussian process, mean 0, covariance min(s,t) for s,t>0): PASS."),
    ("SC1e-L02-statements", "2.9-prose", "course/modules/SC/SC1/L02.html; cards SC1-c018 to c041, c184, c185, c211 to c213", "PASS",
     "Re-checked this round against L02.txt lines 147 to 152 (Proposition 2.4(b) step 1 and step 2: M_m = sqrt(2 log 2) sqrt(m) 2^(-m/2), sum m r^m = r/(1-r)^2): c030, c031, c032. Remark 2.6 (L02.txt 289 to 295): c035 (changed card) PASS. Misconceptions (L02.txt 323 to 329): c039, c040 PASS; sum 1/m partial sum at least 1+k/2 and variance bookkeeping 2^(-(m+1)/2) verified. Carried from round 9 for the other L02 cards (their cited L02 html is outside the delta)."),
    ("SC1e-L03-statements", "2.9-prose", "course/modules/SC/SC1/L03.html; cards SC1-c042 to c060, c187, c188", "PASS",
     "Re-checked this round against L03.txt lines 84 to 94, 114, 231, 237 to 257, 335: c052 (now 'theoretical standard error', matches lines 114, 231, 335), c053 (changed; wording equals line 237 'The constant changes from 2 to c'), c054 (matches the H1 and H2 sentence at line 239 and the delta hunk at html line 382), c056 to c058 (lines 249 to 257), c187 (line 231). Carried from round 9 for the other L03 cards (no delta hunk in their sections)."),
    ("SC1e-L04-statements", "2.9-prose", "course/modules/SC/SC1/L04.html; cards SC1-c061 to c082, c202 to c204", "PASS",
     "Delta hunks at L04 html lines 321 (E[Z_t^2] under Assumptions 4.1 and 4.2) and 432 (martingale question) re-checked: c071 E[Z_t^2]=e^(theta^2 t) (Lemma 2.1 with 2 theta: e^(-theta^2 t) e^(2 theta^2 t)=e^(theta^2 t), checked by hand) and c073 (X_t=B_t+t not a martingale) match. Hunk 468 (sources sentence) has no card. Carried from round 9 for the other L04 cards."),
    ("SC1e-L05-statements", "2.9-prose", "course/modules/SC/SC1/L05.html; cards SC1-c083 to c105, c189, c193 to c200, c214, c216", "PASS",
     "Re-checked this round: c084 (Definition 1.2, L05.txt 68 to 72), c086 and c087 (Lemma 1.3 and Theorem 1.4, L05.txt 78 to 102 and 124, 'transition density'), c193 (A4(a) pi-system, L05.txt 44), c102 (misconception, L05.txt 300: 225 points, largest gap 5.55e-16), c103 and c104 (L05.txt 346 to 350, 444 to 499 hunks: A4(a), A4(f), A4(i) named). c216 (5.55e-16 about 2.5 times 2.2e-16, L05.txt 256). Carried from round 9 for the other L05 cards."),
    ("SC1e-L06-statements", "2.9-prose", "course/modules/SC/SC1/L06.html; cards SC1-c106 to c133, c217", "PASS",
     "Re-checked this round: c108 (Lemma 1.2 with the kappa' sentence added, L06.txt 50), c116 to c118 (Lemma 2.1 hypotheses B continuous, B_0=0, a>0, t>0; L06.txt 88 to 98), c119 (Definition 2.2, L06.txt 102), c120 and c121 (Proposition 2.3, L06.txt 108 to 112), c122 (L06.txt 136), c123 and c124 (Theorem 2.5, L06.txt 142 to 146). Lab counts c111 to c114, c127, c129 recomputed (out/recompute_r10.out, out/lab_L06.stdout). Carried from round 9 for the other L06 cards."),
    ("SC1e-L07-statements", "2.9-prose", "course/modules/SC/SC1/L07.html; cards SC1-c134 to c159, c191, c215", "FAIL",
     "All L07 cards re-checked this round except as stated: c137, c138, c143, c145, c146, c148, c149, c150, c153, c154, c155 to c159, c191 and c215 PASS against L07.txt 50 to 78, 84 to 92, 100 to 122, 380 to 386 and lab output out/lab_L07.stdout. c139 PASS (hypotheses now carried). c140 FAILS: see row SC1e-c140-hypotheses."),
    ("SC1e-L08-statements", "2.9-prose", "course/modules/SC/SC1/L08.html; cards SC1-c161 to c183, c201, c205, c218", "PASS",
     "Re-checked this round against L08.txt 42 to 64 (Definition 1.1, Proposition 1.2 H1 and H2, Corollary 1.3), 66 to 80 (Corollaries 1.4 and 1.5), 330 to 336 (canon break: c175 example), 344 to 352 (misconceptions c176, c178), 368 and 462 to 468 (c174, c183 formulas), and lab output out/lab_L08.stdout (c170 90114, c171 counts, c172 means, c173 z values -1.05, -0.69, -0.77, c174 densities). Changed cards c164 and c165 match Corollary 1.4 and 1.5 (H1, H2 of Proposition 1.2). c180 parity sentence (L08 html hunk 364) matches. Carried from round 9 for the other L08 cards."),
    ("SC1e-assumption-labels", "2.4-math", "cards naming A1 to A5, Assumptions 2.1, 3.1, 3.2, 4.1, 4.2", "PASS",
     "Every assumption label used by a card is defined in the lesson named: A1(a) to (e) in L01, Assumption 2.1 in L02, A2 in L02, A3 and A4(a) to (i) in L05 (A4(a) at L05.txt 44, A4(i) at 60), A5 in L07 (L07.txt 76 to 78), Assumptions 3.1, 3.2 in L03, 4.1 and 4.2 in L04. The changed labels in c103, c104, c193 match L05.txt 100 to 102 and 444 to 499."),
    ("SC1e-cross-references", "2.9-prose", "cards naming Problems, Sections, Lab parts and numbered results", "PASS",
     "scan_r10.py: 249 cross-reference tokens (Lemma, Proposition, Theorem, Corollary, Remark, Example, Definition, Problem, Assumption, Lab) checked against the card's own lesson text: 0 absent. 37 'of Lesson K' references, checked against the lesson in which the named result appears (c140 and c139 use Lesson 5 and Theorem 1.3 of Lesson 7 correctly)."),
    ("SC1e-hypotheses-carried", "2.4-math", "cards for Lemma, Proposition, Theorem, Corollary, Remark statements", "FAIL",
     "Card SC1-c140 (Corollary 1.5(b)) carries A5, A3 and A4 but not H1 (standard Brownian motion with continuous paths and B_0=0) and H3 (H>0), which the lesson's statement names at L07.txt line 74. All other statement cards re-checked this round carry their hypotheses. See SC1e-c140-hypotheses for the fix."),
    ("SC1e-grades-audit", "2.3-grades", "cards with grade C and grade T", "PASS",
     "Counts: grade T 120, grade C 23 (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c148 to c150, c170 to c174, c187, c216, c218). Every C card names a Lab in basis; every T or C card has a basis (scan_r10.py). Cards whose result depends on A3 or A4 are graded T with the assumption named (c115, c137, c139, c164, c165, c174)."),
    ("SC1e-cites-and-registry", "2.1-citations", "cards.json cite fields", "PASS",
     "scan_r10.py: cite is [] on all 206 cards. No card cites a registry key, so verify_refs was not needed for this slice."),
    ("SC1e-notation", "2.4-math", "cards and L01 to L08 text; notation/notation.json", "PASS",
     "git diff c93dd526 HEAD -- notation is empty, so the registry is unchanged. Cards and lessons use H as horizon, Phi only as the standard normal CDF, Q(P) for quadratic variation, nu_a and tau_a for first passage. No T, gamma, R^*, R^(e*) or R_f symbol in the cards."),
    ("SC1e-dag", "2.9-prose", "cards; L01 to L08 text", "PASS",
     "check_dag.py --unit SC1 -> out/check_dag.txt PASS. scan_r10.py: no data-concept markup and no concept link in any card."),
    ("SC1e-scope-words", "2.3-grades", "cards using every, all, any, always, only, for every, holds for all", "PASS",
     "Scope claims checked: c111 (1014 of 1014, lab output), c112 (78 of 78), c170 (all 90114 pairs, lab output), c218 (all 78 pairs), c051 (no other |z| above 1.84), c102 (Theorem 2.1 holds for all u,v>0, L05.txt 300), c153 (Proposition 2.2(a) on every continuous path), c157 (P(M_H=a)=0 for fixed H>0, a>0), c058 (no pathwise claim, L03.txt 257)."),
    ("SC1e-r8-twin-docstring-only", "2.5-labs", "tests/labs/SC1/ twins", "PASS",
     "git diff c93dd526 HEAD -- tests/labs/SC1 is empty: the twins are the same bytes as at the round-9 pin. run_labs PASS 11/11 and each twin exit 0 under python -I -W error (out/lab_L0x.stdout) re-run this round."),
    ("SC1e-c052-term", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c052 front", "PASS",
     "Round-9 FAIL cleared. Front now reads 'what is the theoretical standard error of the mean of Q'. L03.txt lines 114, 231 and 335 use 'theoretical standard error'. grep -i population over cards.json and out/L01 to out/L08: 0 hits (out/grep_population_r10.out). Value H*sqrt(2/N)/20 with Var(Q)=2H^2/N and 400 paths: matches R1 and recompute_r10.py (c053 and c052 values)."),
    ("SC1e-c150-assumption-reference", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c150 back", "PASS",
     "Card back says 'assuming A3 and A4 of Lesson 5 and Assumption A5 of Lesson 7', and the gap is 1.24 standard errors. L07.txt line 380 and lab output out/lab_L07.stdout (0.7586, se 0.0317, sqrt(2/pi)=0.797885, gap 0.0393 = 1.24 se) match. A5 is stated at L07.txt 76 to 78."),
    ("SC1e-c140-hypotheses", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c140 front", "FAIL",
     "New in round 10. The lesson statement of Corollary 1.5(b) (L07.txt line 74) reads 'Assuming A5 and H2 of Theorem 1.3 (...), and under H1 and H3 of Theorem 1.3, E[M_H]=sqrt(2H/pi)'. The card front names only A5, A3 and A4. H1 (B a standard Brownian motion with continuous paths and B_0=0) and H3 (H>0) are missing, although the sibling card SC1-c139 carries them. Fix: rewrite the front of SC1-c140 as 'Corollary 1.5(b). Hypotheses: B is a standard Brownian motion with continuous paths and B_0=0; H>0 is fixed; Assumptions A3 and A4 of Lesson 5 hold; Assumption A5 (the tail formula for a nonnegative variable) holds. What is E[M_H]?' Leave the back unchanged (its arithmetic is verified in numbers_inline_r10.out)."),
    ("SC1e-c219-new", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c219", "PASS",
     "New card (round-10 delta). Its statement and answer match L01.txt line 100 (Remark 1.3 consequence: Gaussian process with mean 0 and covariance min(s,t) for s,t>0). Distinct from SC1-c008 (law of the vector) and from SC1-c006 (definition of a Gaussian process); near-duplicate scan shows no pair at ratio 0.6 or above with it."),
]
data = {
    "unit": "SC1",
    "slice": "e",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all cards of course/modules/SC/SC1/cards.json (206) against lessons L01 to L08; round 10",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-SC1-e",
    "scratch": "ledgers/SC1/scripts/SC1-e-r10/out",
    "verified_at": "2026-11-05T08:52:00Z",
    "verdict": None,
    "rows": [],
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 10 at pin 00a84795 (HEAD). Delta since round-9 pin c93dd526 read in full (out/delta_r9_to_pin.diff). "
        "Cards: 206 (round 9 had 205; c219 added, no card removed). Lesson html hunks in L02 to L08; L01 and tests/labs/SC1 and notation unchanged. "
        "Round-9 FAIL SC1e-c052-term is cleared. New FAIL SC1e-c140-hypotheses (Corollary 1.5(b) card omits H1 and H3). "
        "Gates run this round: check_pages, check_dag, run_labs (11/11), page_smoke (SC1), embed_check (8 of 8), lab twins alone under python -I -W error, scan_r10, recompute_r10, numbers_inline_r10. "
        "Not run: ruff, mypy, pytest, verify_refs: no Python module outside the twins changed in this slice and the slice cites no registry key. "
        "Not checked: a full line-by-line re-read of the unchanged lesson text (see SC1e-full-read-lessons, UNVERIFIABLE); no subagents were available to split the reading. "
        "Mutants: none, since this slice has no grader (as in rounds 4 to 9)."
    ),
    "summary": "",
}
for rid, check, loc, status, ev in rows:
    data["rows"].append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
statuses = [r["status"] for r in data["rows"]]
data["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
fails = [r["id"] for r in data["rows"] if r["status"] != "PASS"]
data["summary"] = (
    f"SC1 slice e round 10 at 00a84795: {len(data['rows'])} rows; PASS {statuses.count('PASS')}, FAIL {statuses.count('FAIL')}, "
    f"UNVERIFIABLE {statuses.count('UNVERIFIABLE')}. Non-PASS: {', '.join(fails)}. Verdict FAIL."
)
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(data["verdict"], data["summary"])
