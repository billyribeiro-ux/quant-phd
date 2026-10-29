import json, sys
CAR = "Carried from round 10 (cited subject byte-identical since the round-10 pin e8b10b8; round-11 delta touches only course/modules/M/M2/L13.html, L14.html, L16.html, cards.json, not the cited locators)"
rows = []
def R(id_, check, loc, status, ev):
    rows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})

R("M2c-gate-check-pages", "2.9-structure", "tools/check_pages.py --all", "PASS",
  "Round-11 fresh: scratch/check_pages.out ends 'check_pages AP1: PASS', exit 0 at pin f42f432.")
R("M2c-gate-check-dag", "2.9-dag", "tools/check_dag.py --all", "PASS",
  "Round-11 fresh: scratch/check_dag.out 'check_dag AP1: PASS', exit 0.")
R("M2c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M2", "PASS",
  "Round-11 fresh: scratch/run_labs_M2.out 'run_labs M2: PASS (27/27)', exit 0.")
R("M2c-labs-twin-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py", "PASS",
  "Round-11 fresh: each of the six twins run as python -I -W error exits 0; six twin_*.err files are 0 bytes (scratch/twin_*.out, twin_*.err).")
R("M2c-gate-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2", "PASS",
  "Round-11 fresh: scratch/page_smoke.out 'page_smoke M2: PASS', exit 0.")
R("M2c-gate-ruff-mypy-pytest", "2.5-labs", "ruff check/format tests/labs/M2; mypy --no-incremental on the six L13-L18 twins; pytest tests/test_labs.py -k M2", "PASS",
  "Round-11 fresh: ruff_check.out 'All checks passed!' exit 0; ruff_format.out '27 files already formatted' exit 0; mypy.out 'Success: no issues found in 6 source files' exit 0; pytest_labs_M2.out 27 passed, exit 0.")
R("M2c-verify-refs", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
  "Round-11 fresh: verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit 0. Live run not performed.")
R("M2c-banned-scan", "1.3-1.4-banned", "round-11 changed sentences: L13 l.229, l.301, l.339; L14 l.73, l.78, l.421-422; L16 l.246, l.303; cards M2-c212, M2-c258", "PASS",
  "Round-11 fresh: every added line of git diff e8b10b8..f42f432 read; grep of added lines for round, builder, verifier, revised, fixed, previous returns only 'rounded' (L13 l.229) and 'fixed' in the mathematical sense ('a fixed function', 'holding x fixed', L13 l.107-equivalent and L16 l.246). No process word, no first-person text.")
R("M2c-scope-words", "2.9-scope-words", "round-11 changed sentences: L13 l.98 (list of uses), l.229, l.339; L14 l.73, l.78; L16 l.246, l.303; cards M2-c212, M2-c258", "PASS",
  "Round-11 fresh: L13 l.98 'Each result that uses them says so' lists Example 2.3, Problems M3, E1, E2, E3, R3 and Lab 1; each of these carries an explicit 'Under Assumption 1' (l.102, l.278, l.314, l.321, l.326, l.353, lab l.149 and twin l.165); Section 5 and R1 (l.229, l.339) name the value e and say 'under Assumption 1'. L14 l.78 'each such statement says so': Example 4.1 (l.107, l.109), Lab 1 (l.255), Proposition 3.1 (l.87), Example 5.1 (l.160-162), Proposition 5.2 (l.165, l.273) each carry the phrase. No new universal scope word without a computation.")
R("M2c-notation", "2.4-notation", "notation/notation.json vs round-11 changed symbols (h*, h_0, M, M_3, Assumption 1)", "PASS",
  "Round-11 fresh: notation/ and tools/ not in e8b10b8..f42f432 diff (git diff --name-only). New symbols in L13 l.229/l.301/l.339 are h*, h_0 and M_3, all defined in the same sentence or in Section 4 (l.143 text), and M_3 is the Section 4 meaning. L16 l.246 and L14 l.73 add no symbol.")
R("M2c-structure-order", "2.9-structure", "BUILDER_RULES 4.2 order in L13-L18", "PASS",
  "Round-11 fresh: every hunk of git diff e8b10b8..f42f432 for L13.html, L14.html, L16.html read in full (3+3 hunks in L13, 3 in L14, 2 in L16, no heading, id, or problem added, moved or removed: grep of '+' lines for 'id=' and '<h2' returns none). Section order unchanged.")
R("M2c-why-it-matters-length", "2.9-structure", "why-it-matters paragraph of L13-L18", "PASS",
  CAR + ": no round-11 hunk touches a why-it-matters paragraph.")
R("M2c-misconceptions", "2.9-structure", "misconceptions sections of L13-L18", "PASS",
  CAR + ": round-11 hunks are outside the misconceptions sections (L14 Remark l.421-422 is in section 9, not in section 7 Misconceptions; Misconception 2 text re-read and it still marks the reverse-mode cost gap).")
R("M2c-problem-tiers", "2.9-structure", "problem-set tiers of L13-L18", "PASS",
  "Round-11 fresh: no problem added, removed or retiered in the delta; changed problems keep their titles and tiers (L13 P3 l.301, R1 l.339; L16 M2 l.246, E3 l.303).")
R("M2c-quiz", "2.9-structure", "retrieval quizzes of L13-L18", "PASS",
  CAR + ": no round-11 hunk touches a quiz block.")
R("M2c-hours", "2.9-hours", "data-hours on L13-L18; hub index.html", "PASS",
  "Round-11 fresh: git diff e8b10b8..f42f432 -U0 for L13, L14, L16 contains zero data-hours or data-grade lines.")
R("M2c-card-duplicates", "2.7-cards", "course/modules/M/M2/cards.json", "PASS",
  "Round-11 fresh: cards_check.out 'entries 379', 'dup ids []', 'dup fronts []', 'dup backs []' (case-insensitive, stripped).")
R("M2c-cards-L13", "2.7-cards", "cards.json lesson L13 (M2-c181..c201, c380, c381)", "PASS",
  CAR + ": cards byte-identical; M2-c187 (proviso h* <= h0, l.143 wording) still matches L13 l.143 and P3 l.301.")
R("M2c-cards-L14", "2.7-cards", "cards.json lesson L14 (M2-c202..c219; changed M2-c212)", "PASS",
  "Round-11 fresh: M2-c212 back re-derived against L14 R3 l.233-235: 'x if x > 0 else 0' on 0 + 1 eps gives the constant 0 (tangent 0), 'x if x >= 0 else 0' gives x (tangent 1), max(x,0) has no derivative at 0 (one-sided slopes 0 and 1). Card names 'Problem R3', which is L14 l.232. Other L14 cards byte-identical since e8b10b8.")
R("M2c-cards-L15", "2.7-cards", "cards.json M2-c234 (L15, grade T)", "PASS",
  CAR + ": L15.html unchanged; M2-c234 unchanged since e8b10b8.")
R("M2c-cards-L16", "2.7-cards", "cards.json lesson L16 (M2-c239..c249)", "PASS",
  "Round-11 fresh: cards M2-c239..c249 byte-identical since e8b10b8 (no L16 card in cards.json hunk). M2-c241 (F = x^2 y + e^(xy) partials at (1,2)) agrees with the re-derived F_x=2xy+y e^(xy), F_y=x^2+x e^(xy) at (1,2), i.e. 4+2e^2 and 1+e^2 (L16 l.185, l.343 key results).")
R("M2c-cards-L17", "2.7-cards", "cards.json lesson L17 (M2-c251..c264; changed M2-c258)", "PASS",
  "Round-11 fresh: M2-c258 back '(1, 1.8775826) ... |1| + |1.8775826| = 2.8775826 attained at the corner u = (1,1) (Problem R1)' matches L17 l.171-174 (grad f(a) = (1, 1.8775826) from l.28, l.110 lab gradient 1.877583; 1 + cos 0.5 = 1.8775826). L17 unchanged since e8b10b8. Other L17 cards byte-identical.")
R("M2c-cards-L18", "2.7-cards", "cards.json lesson L18 (M2-c265..c279)", "PASS",
  CAR + ": no card of L18 in the delta; L18.html unchanged.")
R("M2c-L13-numbers", "2.2-numbers", "L13 prose numbers: Section 5 l.229, Example 2.3 l.102, E1 l.314, E2 l.321, E3 l.326, R1 l.339, R3 l.353, key results, Misconceptions", "PASS",
  "Round-11 fresh, numcheck_L13 (scratch/nums_L13.out): 2sqrt(M delta) = 4.9136e-8 (prose 4.9e-8); 2delta/h at 1e-8 = 4.4409e-8, at 1e-9 = 4.4409e-7; truncation (h/2)e at 1e-9 = 1.3591e-9, ratio 326.74 (prose 326.7, 327); R3 e*2^-53/1e-8 = 3.018e-8 (prose 3.0e-8); 2^-53/1e-8 = 1.110e-8; R1 h* = 2sqrt(1e-3/e) = 0.0383604 (prose 0.038360); E3 3delta/e = 2.45057e-16, cube root 6.25781e-6 (prose 6.25781e-6); predicted forward step 2sqrt(delta/e) = 1.8076e-8 (prose 1.8e-8); central step 6.2578e-6 (prose 6.3e-6); Example 2.3 forward bounds [0.0135914, 0.0137280], central [4.4854e-5, 4.5760e-5]; ratio bounds (9.990, 10.101) and (98.91, 101.11). Misconception 3 ratio 1.364e-2/4.530e-5 = 301.10 (prose 301.1) and unrounded 301.00 (prose 301.0). Misconception 2 ratio 2.154e-7/6.603e-9 = 32.63 (prose 32.6). Central 1e-5 vs 1e-7 full-precision difference 4.4e-16 (< 1e-15 as stated).")
R("M2c-L13-lab1", "2.5-labs", "L13 Lab 1 hypothesis (l.149), expected block (l.205-219), interpretation (l.~221-230)", "PASS",
  "Round-11 fresh: tests/labs/M2/lab-M2-L13-1.py run as python -I -W error (scratch/L13_full.out) equals the page's expected block line for line (12 table rows, two 'is smallest' lines, two ratio lines). Twin unchanged since e8b10b8.")
R("M2c-L13-theorems", "2.4-mathematics", "course/modules/M/M2/L13.html l.301 (P3 statement, now with f''' continuous on [x-h0, x+h0] so that M_3 is finite); Theorem 2.2, Prop 3.2, Corollary 4.1 statements and proofs", "PASS",
  "Round-11 fresh: round-10 FAIL is fixed. P3 l.301 now reads 'with f''' continuous on [x - h_0, x + h_0], so that M_3 = max|f'''| on [x - h_0, x + h_0] is finite', matching Section 4 l.143 and Corollary 4.1's finiteness hypothesis. B_c'(h) = (M_3/3)h - delta/h^2 and B_c''(h) = M_3/3 + 2delta/h^3 > 0 re-derived; B_c(h*) = 3delta/(2h*) re-derived. Theorem 2.2, Prop 3.2 and Corollary 4.1 re-derived (carried text byte-identical).")
R("M2c-L13-prop32-hypotheses", "2.4-mathematics", "L13.html Prop 3.2 hypotheses, Corollary 4.1 hypotheses, uses in Section 5 l.229", "PASS",
  "Round-11 fresh: Section 5 bullet 1 (l.229) now also says 'under Assumption 1' for M = e and uses Prop 3.2's third hypothesis (exact points x - h, x, x + h) as stated; Prop 3.2 and Corollary 4.1 hypothesis text unchanged since e8b10b8.")
R("M2c-L13-assumption1-list", "2.4-mathematics", "L13.html Assumption 1 list (l.98) vs each use", "PASS",
  "Round-11 fresh: l.98 lists Example 2.3, Problems M3, E1, E2, E3, R3 and Lab 1 as results that use the assumption; each has 'Under Assumption 1' (l.102, l.278, l.314, l.321, l.326, l.353, l.149). Section 5 (l.229), Problem E3 (l.326) and R1 (l.339) use the value e and say so. Assumption 1 is defined in L13 itself (l.98), so no forward reference to L14.")
R("M2c-L13-balanced-proviso", "2.4-mathematics", "course/modules/M/M2/L13.html l.143 and cards.json M2-c187", "PASS",
  "Round-11 fresh: l.143 finiteness sentence and proviso h* <= h0 present; M2-c187 (unchanged) matches. P3 l.301 now states the same finiteness hypothesis.")
R("M2c-L14-numbers", "2.2-numbers", "L14 Example 4.1 (l.107-109), Lab 1, E1, E3, key results (l.431-434)", "PASS",
  "Round-11 fresh: Example 4.1 values re-derived: e^2 = 7.389056099; 2*e^2 = 14.778112198; (x cos x - sin x)/x^2 at 2 = -0.435397775; sum 21.731770522 (prose 21.731770522; key row 21.7317705218 to 10 places rounds to 21.731770522). Lab 1 f2'(1) closed form 2.5067615350 matches twin output (scratch/twin_lab-M2-L14-1.out). Changed text (l.73, l.78, l.421-422) contains no number.")
R("M2c-L14-lab1", "2.5-labs", "L14 Lab 1 hypothesis, expected block, interpretation", "PASS",
  CAR + ": L14 Lab 1 text and twin unchanged; twin output 2.5067615350 both lines.")
R("M2c-L14-theorems", "2.4-mathematics", "course/modules/M/M2/L14.html l.73 (new sentence in Definition 2.1), l.78 (Assumption 1 paragraph), l.421-422 (Remark 9)", "PASS",
  "Round-11 fresh: round-10 FAIL is fixed. Definition 2.1 now says at l.73 'The exponential and sine rules hold under Assumption 1'. l.78 now reads 'The exponential and sine rules of Definition 2.1 and the statement of Proposition 3.1 assume them' (singular/plural agreement fixed). The four named statements carry the phrase (Example 4.1 l.107, Prop 3.1 l.87, Lab 1 l.255, Prop 5.2 l.273). Remark l.422: Misconception 2 marks the reverse-mode cost gap and Problem R2 treats only storage (both re-read, true).")
R("M2c-L15-numbers", "2.2-numbers", "L15 Prop 3.5, Lab 1, E1, E2, E3", "PASS",
  CAR + ": L15.html unchanged.")
R("M2c-L15-theorems", "2.4-mathematics", "L15 Prop 2.1, 2.2, Example 2.4, 3.3, 3.4, Prop 3.1, Cor 3.2, Problems", "PASS",
  CAR + ": L15.html unchanged; M2-c234 unchanged.")
R("M2c-L15-lab1", "2.5-labs", "L15 Lab 1", "PASS",
  CAR + ": L15.html and tests/labs/M2/lab-M2-L15-1.py unchanged; twin output 'n = 10000: 0.500000 0.000050000' reproduced (scratch/twin_lab-M2-L15-1.out).")
R("M2c-L16-numbers", "2.2-numbers", "L16.html Example 1.3, Lab 1 hypothesis/interpretation, M2 (l.246), E1, E3 (l.303)", "PASS",
  "Round-11 fresh: M2 at (0,1): 2e^0 * 1 = 2 (l.246). E3 at (1,2): F_xy = F_yx = 2x + e^(xy) + xy e^(xy) = 2 + 3e^2 = 24.167168 (l.303; 2 + 3*7.389056099 = 24.167168). Example 1.3 and Lab 1 text unchanged.")
R("M2c-L16-prop21-31", "2.4-mathematics", "L16.html Remark 1.2, Proposition 2.1, Proposition 3.1", "PASS",
  CAR + ": the round-11 hunks are at l.246 and l.303 only.")
R("M2c-L16-R3-dependence", "2.4-mathematics", "L16.html R3 statement and solution", "PASS",
  CAR + ": R3 unchanged.")
R("M2c-L16-R3-xref", "2.9-structure", "L16.html R3 cross-reference to Proposition 2.1 of this lesson", "PASS",
  CAR + ": R3 unchanged.")
R("M2c-L16-assumption1", "2.4-mathematics", "L16.html l.68 Assumption 1 list 'Example 1.3, Lab 1, Problems M2, E1 and E3' and key-results row", "PASS",
  "Round-11 fresh: grep of 'Assumption 1' in L16 plain text: uses at Example 1.3 (l.31), Lab 1 (l.49), E1 (l.158), M2 (l.136, now with the parenthetical), E3 (l.166), key-results row (l.185). Problem M2 and E3 both say 'under Assumption 1'. List complete and each use says so.")
R("M2c-L17-numbers", "2.2-numbers", "L17.html E3, R1, E2, Lab 1 numbers", "PASS",
  CAR + ": L17.html unchanged since e8b10b8.")
R("M2c-L17-theorems", "2.4-mathematics", "L17.html Theorem 3.1, proof, P2, Section 4", "PASS",
  CAR + ": L17.html unchanged.")
R("M2c-L17-g-w-rename", "2.4-notation", "L17.html uses of g and w", "PASS",
  CAR + ": L17.html unchanged.")
R("M2c-L17-lab1", "2.5-labs", "L17 Lab 1 hypothesis, expected block, interpretation", "PASS",
  CAR + ": L17.html and lab-M2-L17-1 unchanged; twin output 'sampled direction ... 62 degrees' reproduced.")
R("M2c-L18-numbers", "2.2-numbers", "L18 Example 4.2, P3, E1, E2, E3, R3, Lab 1 hypothesis", "PASS",
  CAR + ": L18.html and its twin unchanged.")
R("M2c-L18-theorems", "2.4-mathematics", "L18 Definition 3.1, Propositions 3.2/3.3, Theorem 4.1, R1, R2, P2", "PASS",
  CAR + ": L18.html unchanged.")
R("M2c-L18-assumption1", "2.4-mathematics", "L18.html l.250, l.265, l.333; card M2-c277", "PASS",
  CAR + ": L18.html and M2-c277 unchanged.")
R("M2c-L18-lab1", "2.5-labs", "L18 Lab 1 hypothesis, expected block, interpretation", "PASS",
  CAR + ": L18 twin output 'remainder over step length, k = 1e-03: 1.0000e-03' reproduced (scratch/twin_lab-M2-L18-1.out).")
R("M2c-grades", "2.3-grades", "grade tags in L13-L18", "PASS",
  "Round-11 fresh: no data-grade or grade change in the round-11 hunks (grep of -U0 diff for the L13, L14, L16 pages and cards for M2-c212 and M2-c258 shows only text changes); grades T on the changed cards are unchanged.")
R("M2c-attribution", "2.1-citations", "references sections of L13-L18 and attributed claims", "PASS",
  CAR + ": no bibliographic data or theorem locator added. L16 E3 now cites 'Lesson L19 (Theorem 2.1 there, on the symmetry of mixed partials)': L19.html l.72 'Theorem 2.1 (symmetry of the mixed partials)' confirmed.")
R("M2c-labs-data", "2.5-labs", "L13-L18 lab blocks and data-files", "PASS",
  CAR + ": no data-files change; tests/labs/M2 changed only in lab-M2-L23-1.py (outside slice c).")
R("M2c-L14-assumption1-claim", "2.4-mathematics", "course/modules/M/M2/L14.html l.73 vs Definition 2.1 and l.79 (Assumption 1 paragraph)", "PASS",
  "Round-11 fresh: round-10 FAIL is fixed. Definition 2.1 (l.73) now states the Assumption 1 dependence it had lacked, so 'each such statement says so' holds for the exponential and sine rules of Definition 2.1.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
 "unit": "M2", "slice": "c", "round": 11,
 "verifier": "Haiku 5.5 independent verifier (B11)",
 "pin": "f42f4329dcb0b5c2257e40cd6c27e734fa700d46",
 "base": "e8b10b8110923bd88c3b4bd0e36e1571be3e6725 (round-10 pin; round-10 fragment /Users/billyribeiro/.fanout/frags/B-M2-c.round10.json used as context and for carried rows)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB11-M2-c",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB11-M2-c/ledgers/M2/scripts/M2-c-r11",
 "verified_at": "2026-10-29",
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Slice c (L13-L18 and six lab twins). Delta e8b10b8..f42f432 touches slice paths only in L13.html (l.229 'under Assumption 1' in Section 5, l.301 P3 finiteness, l.339 R1), L14.html (l.73 new sentence in Definition 2.1, l.78 agreement, l.421-422 Remark), L16.html (l.246 M2, l.303 E3), cards.json (M2-c212 in L14, M2-c258 in L17; other changed cards are outside the slice). No tools, notation, references, or other slice twins changed. No project grader in the slice, so no mutation test (ruling); check_projects --all run and PASS. Lesson-page round: no student-error mutants; the labs were checked by re-running each twin under python -I -W error and comparing the expected block of L13 Lab 1 line for line.",
 "summary": "Slice c, round 11: %d rows. Both round-10 FAILs are fixed: M2c-L13-theorems (P3 l.301 now states the finiteness of M_3) and M2c-L14-theorems / M2c-L14-assumption1-claim (Definition 2.1 l.73 now states its Assumption 1 dependence; l.78 agreement fixed). No new defect found in the round-11 delta. Re-derived every new number in L13 l.229, l.301, l.339 and L14 l.73/l.78/l.421, L16 l.246/l.303, and cards M2-c212, M2-c258. Carried rows cite only byte-identical subjects or sentences outside every round-11 hunk." % len(rows),
}
out = sys.argv[1]
json.dump(frag, open(out, "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), "verdict", verdict)
