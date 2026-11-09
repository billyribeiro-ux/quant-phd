"""Build ledgers/E3/E3-g.json for round 14 from the round-12 fragment (carry rule) plus round-14 re-verification rows."""
import json
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, "tools")
import ledger  # noqa: E402

R12 = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round12.json", encoding="utf-8"))
old = {r["id"]: r for r in R12["rows"]}

SLICE_HTML = {L: f"course/modules/E/E3/{L}.html" for L in ("L05", "L06", "L07", "L08")}
CARD_LESSON = {}
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
for c in cards:
    CARD_LESSON[c["id"]] = c["lesson"]

REVERIFIED = {
    "E3g12-c125": ("PASS", "Re-verified: card E3-c125 changed in 329c1d7f..1431aa1d. Read against L07.txt lines 56-67 (Proposition 2.2: A1 lotteries A and B of Example 2.1; A2 omega = omega_{1/2} of Example 1.4; A3 v(x) = x^alpha, alpha > 0; statement at line 62; proof at lines 65-67: V(A) = omega(3/10)(50^a + 100^a), V(B) = omega(3/5) 100^a, divide by 100^a and by omega(3/5) > 0). Ratio omega(3/10)/omega(3/5) = 0.7304544982 and thresholds 2/3 and 0.58578644 recomputed at 60 digits (ledgers/E3/scripts/E3-g-r14/recompute_r14.py, output recompute_r14.out). Grade T matches Proposition 2.2 (L07.html). Every hypothesis of the proposition is carried by the card.", None),
    "E3g12-c134": ("PASS", "Re-verified: card E3-c134 changed (wording only). cite kahneman1979prospect, grade C. L07.txt line 34 (grade C: the name appears in the 1979 title; paper not read; no weighting function quoted) and line 292 (basis: registry record, title only) agree with 'used for its title only'. Registry title 'Prospect Theory: An Analysis of Decision under Risk', Econometrica 47(2), 1979 (references/references.json); live Crossref HTTP 200 with the same title, authors, year, container, volume and issue (ledgers/E3/scripts/E3-g-r14/crossref_live_r14.out).", None),
    "E3g12-c142": ("PASS", "Re-verified: card E3-c142 changed (wording). Read against L08.txt lines 43-52: Theorem 2.2 A1 (P finite and nonempty), A2 (u strictly increasing), A3 (f has finitely many outcomes); strict case in the proof (line 50); Remark 2.3 (one-element prior set gives equality by Proposition 1.3). The card states 'never strict for a one-element prior set' and 'strict when the priors give different expected utilities'; both are the lesson's content. Grade T matches line 43. Card's hypotheses are the theorem's.", None),
    "E3g12-c143": ("PASS", "Re-verified: card E3-c143 changed (wording). Read against L08.txt lines 53-60: Proposition 2.4 A1 (prior set {P_k : k = 0..90}, P_k(red) = k/90), A2 (u strictly increasing), A3 (bet on red pays w_red if red, w_no otherwise, w_red > w_no; same for black). Conclusion at line 58 (P_0 worst for red, P_90 for black); proof at line 60. The card carries all three hypotheses. Grade T matches.", None),
    "E3g12-c154": ("FAIL", "Card E3-c154 changed: 'Under A1 to A3 of Proposition 2.4' was replaced by 'With the full prior set of red counts 0 to 90 and a strictly increasing u (Proposition 2.4)'. The new text drops Proposition 2.4's A3 (a bet pays its prize on its own colour with w_red > w_no; L08.txt line 57). The claim 'the worst prior depends on the bet' is what the proof at L08.txt line 60 establishes, and that proof uses u(w_red) - u(w_no) > 0 (A3). Section 6, first misconception (L08.txt line 322) makes the same claim under the full set and the bet. Card rule 10 (cards carry a proposition's hypotheses) is not met. Grade T.", "Restore A3 in E3-c154 back, e.g. 'No. With the full prior set of red counts 0 to 90, a strictly increasing u, and a bet paying its prize on its own colour with w_red > w_no (Proposition 2.4), the worst prior depends on the bet, so one prior is not the worst for both bets (section 6, first misconception).' Then re-run ledgers/E3/scripts/E3-g-r14/cards_r14.py and re-verify the row."),
    "E3g12-c158": ("PASS", "Re-verified: card E3-c158 changed (wording). cite gilboa1989maxmin, grade C. L08.txt line 29 (the name maxmin expected utility is in the 1989 title; no axiom or result stated; Definition 1.2 at line 26) and line 403 (grade C, registry title only) agree. Registry title 'Maxmin expected utility with non-unique prior', Gilboa and Schmeidler, Journal of Mathematical Economics 18(2), 1989; live Crossref HTTP 200 with the same record (crossref_live_r14.out).", None),
    "E3g12-c131": ("PASS", "Card E3-c131 was deleted in 329c1d7f..1431aa1d (cards.json hunk at old lines 859-866; delta_r14.out). Current cards.json has 177 cards and no E3-c131 (cards_r14.out, 'E3-c131 present: False'); a grep of course/, tests/ and tools/ finds no reference to E3-c131. What it covered (Lab 1 part C printed difference 3.7435 versus the unrounded 3.7436) remains on the page as Problem E2 (L07.txt lines 258-262). No slice claim is left without its card.", None),
    "E3g12-c131-basis-note": ("PASS", "The basis note belonged to the deleted card E3-c131. No current card or lesson depends on it: E3-c187 has its own basis 'Lab 1, part C; Problem E2' (cards.json), and L07.txt line 258 holds the Problem E2 solution. PASS on the current state.", None),
    "E3g12-scope-words-cards": ("PASS", "Re-run over all 87 L05-L08 cards (cards_r14.py, cards_r14.out, 'scope words' block). Hits in the six changed cards checked: E3-c125 'only' is 'if and only if' (Proposition 2.2); E3-c134 'only' is 'title only' (L07.txt line 34); E3-c142 'never' is the one-element prior set case (Remark 2.3, Proposition 1.3); E3-c143 none; E3-c154 'every' occurs in the question and is answered by section 6 (L08.txt line 322); E3-c158 'Only the name' (L08.txt line 29). The unchanged cards' hits are the ones round 12 checked against their lessons.", None),
    "E3g12-process-words-cards": ("PASS", "Re-run over the 87 L05-L08 cards (cards_r14.out, 'process words' block): the only hit is 'agent' in E3-c154, in the decision-theory sense. No round, verifier, builder, ledger, fragment, checkout, pin or slice word.", None),
    "E3g12-dup-scan": ("PASS", "Re-run over cards.json (cards_r14.out): 177 unique ids, 177 unique fronts, 177 unique backs. A difflib scan of L05-L08 cards (front or back ratio above 0.6) lists the pairs in cards_r14.out; the pairs involving changed cards are not duplicates (E3-c142, c143, c154, c158 do not appear as the same question twice). E3-c144 and E3-c182 (front ratio 0.96) ask about different urn numbers, as round 12 recorded.", None),
    "E3g12-card-numbers": ("PASS", "Re-run cards_r14.py over the 87 L05-L08 cards (cards_r14.out): every Proposition, Theorem, Corollary, Remark, Definition, Example and section number cited in a card occurs in its lesson text, and 'Lab 1, part X' occurs. One flag, E3-c187 'Problem E2': the literal string is absent, but the L07 problem set titles the problem 'E2 · The gap between printed and unrounded values' (L07.txt line 258; problem-title span in L07.html). The reference resolves. No unresolved reference.", None),
    "E3g12-notation": ("PASS", "notation_r14.py output (notation_r14.out): none of the registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} occurs in L05-L08 cards or lesson text (macro grep empty in L05-L08 text). The changed cards use P_k, P(red), k, w_red, w_no, u, omega, alpha and tau; none is registered. 'P(' in cards is the probability operator that the registered macro \\Prob denotes, or a prior label. No collision.", None),
    "E3g12-verify-refs": ("PASS", "verify_refs.py --offline (ledgers/E3/scripts/E3-g-r14/verify_refs_offline.out): 'offline integrity: 560 entries, 0 problems'. references.json changed only in generated_at and in used_by of one unrelated entry (Black and Scholes 1973, gained FC2); the records of ellsberg1961risk, gilboa1989maxmin and kahneman1979prospect are byte-identical. Live Crossref by plain curl (crossref_r14.sh, crossref_live_r14.out): HTTP 200 for 10.2307/1884324, 10.1016/0304-4068(89)90018-9 and 10.2307/1914185; titles, first authors, years, containers, volumes and issues match. Note: verify_refs --unit requires a live run and was not run with --unit.", None),
    "E3g12-lab-twins-run": ("PASS", "Re-run: python -I -W error tests/labs/E3/lab-E3-L0{5,6,7,8}-1.py, exit 0 and 0 bytes on stderr for each (twin-L0N.out and .err in ledgers/E3/scripts/E3-g-r14/). run_labs.py --unit E3 --page L05..L08, each 'run_labs E3: PASS (1/1)' (run_labs_L0N.out): page code byte-identical to the twin and the expected block equal to the output. Printed values recomputed in lab-printed rows below.", None),
    "E3g12-check-pages-dag-projects": ("PASS", "check_pages.py --unit E3: PASS (check_pages_E3.out); check_dag.py --unit E3: PASS (check_dag_E3.out); check_projects.py --unit E3: PASS (check_projects_E3.out). Project page belongs to another slice; its result is recorded here only as the gate output.", None),
}

CARRIED_FILES = {
    "L05": "course/modules/E/E3/L05.html and tests/labs/E3/lab-E3-L05-1.py",
    "L06": "course/modules/E/E3/L06.html and tests/labs/E3/lab-E3-L06-1.py",
    "L07": "course/modules/E/E3/L07.html and tests/labs/E3/lab-E3-L07-1.py",
    "L08": "course/modules/E/E3/L08.html and tests/labs/E3/lab-E3-L08-1.py",
}

rows = []
carry_prefix_base = "Carried from round 12 ({files} byte-identical since the previous pin 329c1d7f):"
for rid, r in old.items():
    if rid in REVERIFIED:
        status, ev, fix = REVERIFIED[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
        if status != "PASS":
            row["fix"] = fix
        rows.append(row)
        continue
    if rid.startswith("E3g12-c"):
        cid = "E3-c" + rid.split("-c")[1]
        lesson = CARD_LESSON.get(cid)
        if lesson not in CARRIED_FILES:
            raise SystemExit(f"card {cid} lesson {lesson} outside slice")
        files = f"{CARRIED_FILES[lesson]}, and card {cid} unchanged in course/modules/E/E3/cards.json"
    elif rid in ("E3g12-L05-prose-numbers", "E3g12-L06-prose-numbers", "E3g12-L07-prose-numbers", "E3g12-L08-prose-numbers", "E3g12-L05-L08-key-results", "E3g12-L05-L08-problem-solutions", "E3g12-L05-L08-quiz-keys", "E3g12-lab-twins-run-unused"):
        files = "course/modules/E/E3/L05.html to L08.html and tests/labs/E3/lab-E3-L05-1.py to L08-1.py"
    elif rid == "E3g12-L04-theorem-cross-lesson":
        files = "course/modules/E/E3/L04.html"
    elif rid == "E3g12-r11-c130-grade-resolved":
        files = "course/modules/E/E3/L07.html and card E3-c130 in course/modules/E/E3/cards.json"
    elif rid == "E3g12-delta-round12":
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": "Carried from round 12 (history: the commit range ccaeeaf4..329c1d7f, whose hunks are unchanged): " + r["evidence"]})
        continue
    else:
        raise SystemExit(f"unclassified round-12 row {rid}")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": carry_prefix_base.format(files=files) + " " + r["evidence"]})

NEW = [
    ("E3g14-delta-round14", "2.9 delta 329c1d7f..1431aa1d within the slice", "course/modules/E/E3/L05.html to L08.html; tests/labs/E3/lab-E3-L05-1.py to L08-1.py; course/modules/E/E3/cards.json; references/references.json",
     "PASS", "delta_r14.out: no diff in the four slice pages or the four slice twins. The slice's cards.json hunks are c125, c131 (deleted), c134, c142, c143, c154, c158; each read in full (rows above). Outside the slice and not verified here: cards.json c183 (L04, grade T added), L01 and L02 lessons, the L01 twin, project and grader, references.json (generated_at; used_by of one unrelated entry), curriculum.json (another unit's project brief). None of them is a claim of L05-L08; the registry records of the three keys the slice cites are byte-identical."),
    ("E3g14-lab-L05-printed", "2.5 lab printed values recomputed", "tests/labs/E3/lab-E3-L05-1.py; course/modules/E/E3/L05.html Lab 1 expected block",
     "PASS", "run_labs L05 PASS (run_labs_L05.out). recompute_r14.py with Fractions (recompute_r14.out, L05 lines) reproduces: V0 = 80/49; U = -49/80; (1-gamma)U = V0^(1-gamma) True; theta = 1; mean 5/2; CE1 = 8/5; CE1 at gamma 0.5, 2, 3 = 2.2500, 1.6000, 1.3720 (falls); V0(4,4) = 4.0000, V0(1,10) = 4.3311; U(4,4) = -0.2500, U(1,10) = -0.5500; EIS = psi = 0.5, 2, 0.25. The four plans' V0 and U orders agree; two plans tie exactly in both (values 2 and -1/2), as Corollary 3.3 requires at psi = 1/gamma. All printed values match."),
    ("E3g14-lab-L06-printed", "2.5 lab printed values recomputed", "tests/labs/E3/lab-E3-L06-1.py; course/modules/E/E3/L06.html Lab 1 expected block",
     "PASS", "run_labs L06 PASS (run_labs_L06.out). recompute_r14.out (L06 lines): W = 200, 50, -100 at lambda = 1, 3/2, 2; lambda* = 5/3 = 1.6667; combined lottery 100 versus separate -200; alpha = delta = 0.5: lambda* = 1.2910 and W(2) = -8.6835. The remaining L06 lines (concavity of the gain part, convexity of the loss part, monotonicity, equal-magnitude ratio 2) are analytic facts for alpha = delta = 1/2: x^(1/2) is concave and -(-x)^(1/2) has second derivative 0.25(-x)^(-3/2) > 0 on x < 0. All printed values match."),
    ("E3g14-lab-L07-printed", "2.5 lab printed values recomputed", "tests/labs/E3/lab-E3-L07-1.py; course/modules/E/E3/L07.html Lab 1 expected block",
     "PASS", "run_labs L07 PASS (run_labs_L07.out). recompute_r14.out (L07 lines), 60-digit decimal: omega_{1/2} at 0.01, 0.05, 0.3, 0.5, 0.6, 0.95, 0.99 = 0.0834, 0.1557, 0.2858, 0.3536, 0.3913, 0.6788, 0.8298 (printed part A); closed form equals the general formula (gap 2e-60); on the 1001-point grid one sign change and last omega(p) > p at 0.278 (printed); Gamma(A) = 42.8686327357, Gamma(B) = 39.1250770027 at alpha = 1 and 4.8787555762, 3.9125077003 at alpha = 0.5 (printed 42.8686, 39.1251, 4.8788, 3.9125); weighted value of L 49.8328 (prose). Printed difference 42.8686 - 39.1251 = 3.7435 and unrounded difference 3.743555733 -> 3.7436 (Problem E2, prose)."),
    ("E3g14-lab-L08-printed", "2.5 lab printed values recomputed", "tests/labs/E3/lab-E3-L08-1.py; course/modules/E/E3/L08.html Lab 1 expected block",
     "PASS", "run_labs L08 PASS (run_labs_L08.out). recompute_r14.out (L08 lines): EU CE at P(red) = 1/2 = 101951.2195 (= 4180000/41; expected wealth 102500); maxmin at P(red) = 1/3 = 99523.8095; known urn CEs 103125.0000 (red) and 106451.6129 (black); Part B Epstein-Zin CE = 101951.219512 for psi in {0.5, 1.5, 3} and beta in {0.9, 0.95} by closed form, gaps 1e-11 (twin printed largest gap 2.91e-11, all below 1e-6); Part C maxmin urn CE 100000 (worst prior has no red or no black). Prospect value V_p = 5 - sqrt(50) = -2.071068 CU and CE = 99892.7670 cents: checked by hand (x = -1.072330 CU). All printed values match."),
    ("E3g14-page-smoke", "2.5 lab timing and 2.9 render checks", "course/modules/E/E3/L05.html to L08.html",
     "PASS", "page_smoke.py --unit E3 --pages L05 L06 L07 L08: 'page_smoke E3: PASS', exit 0 (page_smoke_L05-L08.out). Zero console errors, math rendered and re-parsed, no external requests, no horizontal scroll at 360 px, every lab under the time limit."),
    ("E3g14-ruff-mypy", "gates: ruff, mypy", "repository (ruff check ., ruff format --check ., mypy --no-incremental)",
     "PASS", "ruff check . -> 'All checks passed!' (ruff_check.out); ruff format --check . -> '553 files already formatted' (ruff_format.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' (mypy.out)."),
    ("E3g14-pytest-relevant", "gates: relevant pytest", "tests/test_run_labs.py, test_labs.py, test_page_checks.py, test_refs.py, test_page_smoke.py",
     "PASS", "pytest -q on those five files: exit 0, all dots (pytest_relevant.out). Tooling tests only; no tool or test changed in the delta."),
    ("E3g14-hours-arithmetic", "2.9 hours arithmetic", "course/modules/E/E3/index.html data-hours-lessons, data-hours-project; L01-L08 data-hours; project.html data-hours-project; curriculum.json E3 hours",
     "PASS", "data-hours = 7 on each of L01 to L08 (grep output in this round): 8 x 7 = 56 = index.html data-hours-lessons 56. index.html data-hours-project 14 = project.html data-hours-project 14. 56 + 14 = 70 = curriculum.json E3 'hours' 70. Project share 14/70 = 20%, inside 10 to 40%."),
]
for rid, check, loc, status, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
notes = [
    "Slice: E3 L05-L08 lessons, the 87 retrieval cards of L05 (22), L06 (19), L07 (18), L08 (28), and the four curriculum lab twins. Mutants: none; the slice is lessons and cards, and lab twins are demonstrations (VERIFIER rulings), so no grader mutation applies.",
    "Previous fragment: /Users/billyribeiro/.fanout/frags/D-E3-g.round13.json does not exist. The latest is round 12 (pin 329c1d7f, 107 rows, all PASS), used as the previous fragment. Round-12 rows are carried or re-verified per the verifier rules; row ids are kept.",
    "Delta 329c1d7f..1431aa1d inside the slice: cards.json c125, c131 (deleted), c134, c142, c143, c154, c158. L05-L08 HTML and the four slice twins are unchanged. Carried rows (81 cards and 9 lesson-level rows plus the history row) cite byte-identical subjects.",
    "Defect found this round: E3-c154 lost Proposition 2.4's hypothesis A3 (w_red > w_no, bet on own colour) in the 329c1d7f..1431aa1d edit. Fix in the row. Verdict is FAIL until the card is corrected and re-verified.",
    "Out of slice, observed only: cards.json E3-c183 (L04) gained grade T; L01 cards renamed the mixture weight alpha to tau; the L04 verifier should read those.",
    "Not checked: check_projects and page_smoke for the project page (other slice); the Epstein-Zin Proposition 3.2 proof was carried from round 12 (lesson text unchanged), not re-derived line by line this round beyond the printed values; a live verify_refs --unit E3 run (the offline gate and direct Crossref checks of the three keys were run); the L05-L08 prose outside the cards was carried, not re-read this round.",
]
registry_flags = []
freshness_flags = []
summary = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows),
"card_rows": sum(1 for r in rows if re.fullmatch(r"E3g1[24]-c\d{3}", r["id"])),
           "mutants": 0, "mutants_killed": 0}
fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 14,
    "verifier": "Haiku 5.5 independent verifier, slice g, round 14",
    "pin": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "base": "329c1d7feac5479403c351e64587c867278452cc (round-12 pin; the round-13 fragment is absent)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD14-E3-g",
    "scratch": "/Users/billyribeiro/.fanout/scratch/E3-g-r14",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary,
}
problems = ledger.validate(fragment, "E3-g")
print("validate:", problems)
json.dump(fragment, open("ledgers/E3/E3-g.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), summary)
