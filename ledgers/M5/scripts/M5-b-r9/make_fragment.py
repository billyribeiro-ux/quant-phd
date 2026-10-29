import json, datetime
S = "ledgers/M5/scripts/M5-b-r9/"
P = "course/modules/M/M5/"
def row(i, check, loc, ev):
    return {"id": i, "check": check, "location": loc, "status": "PASS", "evidence": ev}
gates = S + "check_pages.txt"
rows = [
 row("B-01", "check_pages M5 (page contract, banned strings, claims, locators)", P+"L05.html, L06.html, L07.html", "ledgers/M5/scripts/M5-b-r9/check_pages.txt: 'check_pages M5: PASS', EXIT 0 (run at b6865c7)"),
 row("B-02", "check_dag M5 (concept defined once, no use before definition)", P+"L05.html, L06.html, L07.html", "ledgers/M5/scripts/M5-b-r9/check_dag.txt: 'check_dag M5: PASS', EXIT 0"),
 row("B-03", "check_projects M5 (project ladder, hours sum, grading mode)", P+"project.html", "ledgers/M5/scripts/M5-b-r9/check_projects.txt: 'check_projects M5: PASS', EXIT 0"),
 row("B-04", "run_labs M5 (page code byte-identical to twin; twin runs; expected block equals output)", "tests/labs/M5/, L05.html:84-175, L06.html:99-222, L07.html:192-305", "ledgers/M5/scripts/M5-b-r9/run_labs.txt: 'run_labs M5: PASS (13/13)', EXIT 0"),
 row("B-05", "Lab twins re-run alone under python -I -W error, expected blocks compared to output", "tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py", "ledgers/M5/scripts/M5-b-r9/twin-L05.txt, twin-L06.txt, twin-L07.txt: exit 0, no stderr; L07 part A/B/C lines equal L07.html:290-303 (checked by run_labs)"),
 row("B-06", "Every paragraph, definition, proposition, proof, misconception and problem of L05-L07 read line by line", P+"L05.html:1-403, L06.html:1-435, L07.html:1-535", "Full read in round 9 (Read tool, whole file); delta hunks read in ledgers/M5/scripts/M5-b-r9/delta.diff (249 lines, all hunks L05-L07 and project.html)"),
 row("B-07", "Lab code: no network, stdlib only, deterministic; docstrings match code", "tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py", "Read in full. Imports: fractions, itertools, math only. L06 docstring Part A (prefix 4096, 8 steps, keep half with more pool indices) matches bisect_prefix(); L07 docstring TOL=1e-12 for A and B, none for C matches code lines 214, 252, 277. Twins unchanged since ce7b382 (git diff --stat empty)"),
 row("B-08", "Lab twins are not changed by this round; re-run confirms expected output", "tests/labs/M5/", "git diff ce7b382..b6865c7 -- tests/labs/M5 is empty; run_labs PASS 13/13"),
 row("B-09", "Interpretation paragraphs after each lab match printed output", P+"L05.html:174; L06.html:221; L07.html:304", "L05:174 sup=1 for each order, 1/2^n on [0,1/2] (output lines 156-167); L06:221 widths 1/2..1/256, indices increase (output 205-214), 12/49 < 1/4 (output 217), 45 pairs at distance 1 (output 219); L07:304 0.840117 < sin 1 = 0.841471 (output 299), 0.980390 and 0.999798 (output 301-302)"),
 row("B-10", "Targeted pytest: test_labs -k M5, test_run_labs, test_page_checks, test_docs_figures", "tests/", ".venv/bin/pytest -q tests/test_page_checks.py tests/test_run_labs.py tests/test_docs_figures.py -k 'M5 or page or lab or docs' -> 61 passed; tests/test_labs.py -k M5 -> passed (no failures printed)"),
 row("B-11", "References: no citation keys in L05-L07; verify_refs offline integrity", "references/references.json", "ledgers/M5/scripts/M5-b-r9/verify_refs.txt: 'offline integrity: 560 entries, 0 problems', EXIT 0; live run not performed (no network use in this verifier)"),
 row("B-12", "Arithmetic: all numbers recomputed (bound ratio 48.92, 0.99^100, 1/196, 12/49, 6.2723e-7, 91 iterations, 0.8401167, sin1-q 0.0013542591, 5/sqrt26, 50/sqrt2501)", P+"L05.html:293; L06.html:323; L07.html:294,309-318,351,389-408,426", "Python re-derivation (round 9): cos bound/error at n=5 = 48.9244; ln-based R2 threshold = 90.7126 so n=91; E3 quotient 0.840116725732564, sin1-q = 0.0013542590753; grid argmax over k/200 pairs = (0.995,1.0); 3/7^14 etc. consistent; 5/sqrt(26)=0.980581, 50/sqrt(2501)=0.999800 bound the printed maxima 0.980390 and 0.999798"),
 row("B-13", "Forward and backward cross-references point to existing labelled results", P+"L05.html:52,174,181,200,227; L06.html:56,69,181,272,277; L07.html:52,67,102,124,189,528-529", "grep: L04 Def 1.1, Def 3.2, Def 4.1, Prop 1.7, Prop 3.3, Prop 4.2 exist (L04.html); L02 def-cauchy-sequence and Theorem 2.5 exist; L01 Def 1.1 completeness axiom; L08 Prop 1.3 'grid space is complete'; L08 cites L07 Theorem 2.1 (L08.html line with 'Theorem 2.1 of Lesson 7 applies with X = R^G', which resolves the round-8 unchecked item on L07.html:52)"),
 row("B-14", "Proof validity (Prop 1.3, 2.1, 2.4, 2.5, 3.1, 3.2 of L05; Lemma 1.2, Prop 1.3, 1.4, 2.1, 3.1 and Cor 2.2, 3.2 of L06; Lemma 2.2, Thm 2.1, Prop 1.4, 2.4, 3.1, Cor 3.2 of L07)", P+"L05.html:73-77,208-221,230-234,242-245; L06.html:69-82,89-92,231-236,243-245,255-267; L07.html:112-127,139-146,169-185", "Each step re-read; Cor 3.2 proof (L07.html:179-185) is new and gives the three steps needed (Prop 3.1 gives the contraction inequality with beta = L; f(I) in I is hypothesis (4); I complete by Def 1.2 via L02 Thm 2.5). No gap found"),
 row("B-15", "Proofs of problems and solutions (mechanics, proof, empirical, research tiers)", P+"L05.html:272-302; L06.html:272-333; L07.html:342-433", "Each solution re-derived: L05 emp-3 0.99^100 = 0.366032; L06 mech-2 max 2 at -1 and 2, min -2 at -2 and 1; L06 res-3 case analysis complete; L07 M2 n=14; M3 f(x)=x^2/4 fixed point 0; P1-P3; R1; R2 n=91; R3"),
 row("B-16", "Definitions and the scope of the defined term match their use (L05 uniform, L06 compact, L07 contraction and complete)", P+"L05.html:58-66; L06.html:58-61,94-97; L07.html:58-68", "Def 1.2 of L05 places N before x; L06 Def 1.1 sequential compactness states the definition used everywhere; L07 Def 1.1 states 'same beta for every pair' and matches misconception 1 at L07.html:320-321"),
 row("B-17", "Claims about the lab's exactness and what it does not show", P+"L05.html:86,174; L06.html:101,221; L07.html:194,304", "L05 line 174: printed sup on [0,1] is the distance to 0, not to f, and Prop 2.4 proves the non-uniform case; L06: prefix-only claim, grid max lower bound 'always' true since grid subset [0,1]; L07: grid check does not prove no fixed point, Section 4 does (matches code docstring L07.html:201-202)"),
 row("B-18", "Canon-breaks items and misconceptions (no unstated hypothesis used)", P+"L05.html:255-257,263-265; L06.html:288-297; L07.html:310-312,320-329", "L05 unbounded example: f_N(2N)=2 > 1 for any N, correct; L06 (0,1) no maximum; L07 item 2: |phi x - phi y|/|x-y| -> 1 with x=y+h, y->inf, and sqrt(x^2+1) > |x|, correct; item 1: only candidate fixed point 0 not in (0,1]"),
 row("B-19", "Retrieval quiz items: answers and explanations", P+"L05.html:322-387; L06.html:354-419; L07.html:457-518", "Each correct option and explain text re-checked: L05 q7 (sup of x/n on R infinite), q5, q8; L06 q1-q8 (45 pairs, -1 odd limit, 2 max); L07 q1, q4, q6, q8 and numeric answers 3, 6.2723e-7, 0.8415, 0.5403"),
 row("B-20", "Key-results tables match the propositions they cite", P+"L05.html:305-320; L06.html:337-352; L07.html:439-455", "Each row's source label exists (e.g. L07 'Problem R3 (Assumption 2(c))', 'Canon-breaks, items 1 and 2'); grades T, all results proved on the page"),
 row("B-21", "Hub hours agree with lesson hours (index.html)", "course/modules/M/M5/index.html:137-139; L05/L06/L07 data-hours", "index.html shows L05 10 h, L06 10 h, L07 11 h; lessons data-hours 10, 10, 11 and eyebrows 10, 10, 11 study hours (grep at round 9); index.html unchanged since ce7b382 (git diff empty)"),
 row("B-22", "Section structure, lesson navigation and page contract", P+"L05.html, L06.html, L07.html", "check_pages PASS; nav previous/next links: L05->L04/L06, L06->L05/L07, L07->L06/L08 exist"),
 row("B-23", "Lab twin files (L05-L07) byte-identical to page code blocks", "tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py", "md5 d5f446ce..., 5cb06c78..., a3755974...; run_labs compares page code (unescaped) to twin: PASS"),
 row("B-24", "Notation: every symbol and macro against notation/notation.json", P+"L05.html, L06.html, L07.html, cards.json", "Registered macros \\R and \\N used (no \\mathbb left in L05-L07 or cards.json: grep empty, R8-02 fixed); registered symbols T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q not used in slice; local letters (beta, S, N, c, L, B(S), C_b, f_n) defined where used; ell^infinity(S) defined as L04 Example 1.6"),
 row("F-01", "Proofs and statements of L07 Corollary 3.2 and Lemma 2.2 agree with the page's remarks", P+"L07.html:175-185", "Corollary statement, proof and key results row (L07.html:449) agree; no contradictory sentence found"),
 row("F-02", "Expected lab output matches interpretive text at L07 (grids, windows)", P+"L07.html:56,98-101,123-126,181,296,336", "Re-read; the references to 'Lab 1 part C' in E2 and card c120 match printed values 0.999798 and window [-50,50] on 201 points"),
 row("F-03", "Problem solutions cite the right results (Example 2.3, Problem R1, Problem R3, Assumption 2(c))", P+"L07.html:344,351,419,433", "Each cross-reference resolves to the stated item"),
 row("F-04", "L05 Prop 2.4 and Prop 2.5 cited consistently in text and cards", P+"L05.html:52", "Proposition 2.4 (non-uniform on [0,1]) and 2.5 (uniform on [0,a]) cited at L05.html:81,174,256,264 and cards c075, c076, c080 agree"),
 row("F-05", "Card M5-c115 and L07 misconception 1 agree", "cards.json M5-c115 vs L07.html:320-321", "Card text matches the misconception; the card's 'Misconception 1' label matches the page"),
 row("F-06", "Changed cards (c102, c104, c106) agree with current lesson text", "cards.json M5-c102, M5-c104, M5-c106 vs L07.html:67, 88-103, 106-109", "c102 matches Def 1.2 closed-interval sentence; c104 matches Theorem 2.1(a); c106 matches Lemma 2.2 first claim; each card number appears in its lesson"),
 row("R8-01", "Round-8 fix: B(S)/B(N) citation of L04 Example 1.6 now matches L04 naming", P+"L05.html:227; L06.html:272,277,288,296; cards.json M5-c077, c094", "L04.html:213-214 defines ell^infinity(S) = bounded real functions on S; L05.html:227 and L06.html:272 state the mapping explicitly ('written l^infinity(S) in L04, Example 1.6'; 'where that example writes this space as l^infinity(S)'). No stale citation remains. FIXED"),
 row("R8-02", "Round-8 fix: \\mathbb{R}/\\mathbb{N} replaced by registered \\R/\\N", P+"L05.html, L06.html, L07.html, cards.json", "grep -n mathbb over L05-L07 and cards.json returns no lines (round 9). Replacements read in delta.diff hunks. FIXED"),
 row("R8-03", "Round-8 fix: Corollary 3.2 has a proof block", P+"L07.html:175-185", "Proof block present at L07.html:179-185 with three steps; L07.html:514 claim ('every theorem ... is proved on the page') now holds for Cor 3.2. FIXED"),
]
frag = {
 "unit": "M5", "slice": "b", "round": 9, "verifier": "independent verifier (Haiku 5.5), round 9",
 "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
 "base": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB9-M5-b",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB9-M5-b/ledgers/M5/scripts/M5-b-r9",
 "verified_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": ["verify_refs ran with --offline only; no live Crossref/landing re-verification in this round (no network use)"],
 "notes": [
  "Slice: course/modules/M/M5/L05.html, L06.html, L07.html and their lab twins tests/labs/M5/lab-M5-L05-1.py, lab-M5-L06-1.py, lab-M5-L07-1.py; the cards for these lessons in cards.json; project.html changes and L02-L04 changes are outside this slice (read only where cross-referenced).",
  "Round-9 delta (ce7b382..b6865c7) hunks in slice were all read: L05 Prop 3.1 and Prop 3.4-era text, L06 Example 3.3 / Prop 3.4 / misconceptions / quiz, L07 \\R macro swaps, new Corollary 3.2 proof, and the lab docstring (no code change); the L07 interpretation text is unchanged except macros.",
  "Previous round PASS rows were not carried; every row was re-checked this round because L05-L07 and cards changed.",
  "No grader in this slice; mutation testing does not apply (VERIFIER_RULES rulings). mutants list is empty by design.",
  "page_smoke M5 returned PASS with a one-line output; the --pages filter did not change its scope in the output, so it was treated as a unit-level run.",
  "Full repository gate was not run (targeted set per verifier rules): ruff check ., mypy --no-incremental (255 files, no issues), build_site --check (site data current), targeted pytest all passed.",
  "Not checked: live verify_refs (network); the L08-L10 content beyond the cross-references quoted above; whether the \\R macro renders identically in every browser (page_smoke reports no katex errors); .venv symlink shows as modified in git status (environment only)."
 ],
 "summary": "M5-b round 9: 33 rows, 33 PASS. Round-8 R8-01, R8-02, R8-03 fixed and verified; no new defect found in L05-L07 or their twins after a full read of the three pages, cards for these lessons, and every delta hunk."
}
out = "ledgers/M5/M5-b.json"
import os
os.makedirs("ledgers/M5", exist_ok=True)
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", out, len(rows))
