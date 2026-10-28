"""Build ledgers/CF1/CF1-b.json (round 8) from the round 7 fragment: carry or re-verify each row, add round 8 rows."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

OLD = json.loads(Path("/tmp/fanout-frags/CF1-b.round7.json").read_text(encoding="utf-8"))
PREFIX = ("Carried from round 7 (cited lines byte-identical since the previous pin de53f7e; "
          "the delta to 2c8162b touches only L03 l.51 and l.359, L04 l.7, and cards c033, c034, c088 in this slice): ")

NEW = {
 "CF1-b-cmd-check-pages": "Re-run at 2c8162b: `.venv/bin/python tools/check_pages.py --all` printed 'check_pages CF1: PASS' (all units PASS), exit 0.",
 "CF1-b-cmd-check-dag": "Re-run at 2c8162b: `.venv/bin/python tools/check_dag.py --all` printed 'check_dag CF1: PASS' (all units PASS), exit 0.",
 "CF1-b-cmd-run-labs": "Re-run at 2c8162b: `.venv/bin/python tools/run_labs.py --unit CF1` printed 'run_labs CF1: PASS (9/9)', exit 0.",
 "CF1-b-lab-twin-direct": "Re-run at 2c8162b: each twin under `.venv/bin/python -I -W error` exit 0, stderr 0 bytes (/tmp/cf1-v/CF1-b-r8/lab-CF1-L0{3,4}-1.err). Script ledgers/CF1/scripts/CF1-b-r8/embed_and_cards_check.py (stdlib, `/usr/bin/python3 -I`): embedded code equals the twin (stripped) on L03 and L04; each expected block equals the twin's stdout exactly (24 and 29 lines).",
 "CF1-b-lab-twin-lint": "Re-run at 2c8162b: `.venv/bin/ruff check` on both twins 'All checks passed!'; `ruff format --check` '2 files already formatted'; `.venv/bin/mypy --no-incremental` on both 'Success: no issues found in 2 source files'. Twins unchanged since de53f7e (git diff empty for tests/labs/CF1).",
 "CF1-b-lab-L03-1": "Whole L03.html read this round (l.1-489). Hypothesis l.123 matches the code (outlay 1,000,000 USD, five inflows of 300,000 USD, real rate 0.06, inflation 0.03, 4 x 3 = 12-case grid, no random numbers). Output /tmp/cf1-v/CF1-b-r8/lab-CF1-L03-1.out equals the expected block. Interpretation l.242 matches the printed values: 263,709.14 and 263,709.14; mixed 377,346.63 and 161,465.80; gap 0.00 at inflation 0.00 and 36,913.22, 113,637.49, 194,368.27 at 0.01, 0.03, 0.05. 'The lab does not show ...' is a scope limit the code supports.",
 "CF1-b-lab-L04-1": "Whole L04.html read this round (l.1-555). Embedded code equals the twin; expected block (29 lines) equals the twin stdout. Hypothesis l.145: the grid is -0.5 to 1.0 in steps of 0.0001 (GRID_LOW, GRID_HIGH, GRID_STEP in the twin), matching the page's l.118 'spaced 0.0001 apart'. Interpretation l.300 matches the printed sign column (-, -, 0, +, 0, -, -), roots 0.100000 and 0.200000, gap 0.000000 over six test rates (the gap tuple has six entries), crossover 0.200000 and the ranking table. Independent Fraction recomputation: ledgers/CF1/scripts/CF1-b-r8/recompute_r8.py.",
 "CF1-b-lab-L03-E2-claim": "Re-run this round: ledgers/CF1/scripts/CF1-b-r8/lab_copy_claims.py on a copy with INFLATION = 0.00: 'mixed minus real, cents: 0.00'; 'NPV real flows at nominal rate (mixed): 263709.14 USD' equal to the real NPV; table row 0.00 prints 0.00. The E2 solution's claims hold.",
 "CF1-b-lab-L03-E3-claim": "Re-run this round on a copy with REAL_RATE = 0.10 (same script): 'real rate 0.100000, inflation 0.030000, nominal rate 0.133000' (solution 1.10 x 1.03 - 1 = 0.133); 'largest absolute gap, consistent minus real, cents: 0.000000'. The real NPV changes (solution: the student should check the printed value); the printed real NPV 137,236.03 USD is the value the lab prints on this copy.",
 "CF1-b-numbers-L03": "Re-derived with Fractions this round (ledgers/CF1/scripts/CF1-b-r8/recompute_r8.py): Ex 1.4 n 0.0918, additive gap 0.0018; Ex 2.5 nominal NPV 257.7097 (257.71), real rate 1.08/1.03 - 1 = 0.048544 gives the same NPV; l.248 205 x 1.05 / 200 - 1 = 0.07625, implied inflation 0.025, 200/1.05 = 190.476; l.269 30,000,000 x 1.03^4 = 33,765,264.30 cents; M1 0.066, gap 0.001; M2 1061.208; M3 r = 0.057692, 104/1.10 = 94.545; P3 sqrt(0.005) = 0.070711; E1 shares 0.73706, 0.13998, 0.43092 (73.7, 14.0, 43.1 per cent); E3 1.10 x 1.03 - 1 = 0.133; R2 ratio 2.06; R3 b = 1.06/2.03 = 0.522167 with the error exactly zero. Lab-printed values match the output file.",
 "CF1-b-numbers-L04": "Re-derived with Fractions this round (recompute_r8.py): P NPV at 0, 5, 10, 15, 20, 25, 30 per cent = -2000.00, -680.27, 0.00, 189.04, 0.00, -480.00, -1183.43, equal to -2000(11x-10)(6x-5) at each rate; Ex 4.2 NPVs 18181.82 and 27272.73 at 10 per cent, 8333.33 each at 20 per cent; crossover 0.2; M2 x = 0.884437, r = 0.130662; M3 flows give NPV -(1.5x-1)(x-1); R1 NPV at 10 per cent 0.322314; R2 IRR_A = sqrt(3) - 1 = 0.732051, NPV_A 147.93, NPV_B 81.82; R3 FV 250.00 and -750.00; E2 NPV_A 9090.91 at 10 per cent, -11111.11 and -14814.81 at 35 per cent, crossover 0.30; E3 -680.27; quiz 189.04, 0.21, 13.07, 0.2, 0.",
 "CF1-b-notation-other-symbols": "Whole L03.html and L04.html re-read this round. The delta adds no new symbol: L03 l.51 and l.359 (R1) use only n, r, pi, C^n_t, C^r_t, P_t, prod (defined in Def 1.1 / R1 statement); L04 l.7 uses none. Symbols used in the changed sentences are defined on the page before use (L03 Def 1.1 l.57, Def 1.2 l.62-64).",
 "CF1-b-prose-banned-scan": "Full-file scan this round (python regex, whole word, case-insensitive) of L03.html and L04.html for roughly, historically, half, about, percent, ellipsis, builder, verifier, round, requests, unit report, build, simply, clearly, obviously, typically, generally, usually, most, always, only, every, same, drives, offsets, raises, as much as, single, all. Every hit read: L03 l.320 'half a point' (P3 title, not 'roughly half'); l.421 'about' (prompt); L03 l.138 and L04 l.159-161 'tuple[int, ...]' (code); L04 l.196 'round(' (code, lab); L04 l.121 'at most two' (bound); L04 l.307 'offsets' (Remark 5.1, the identity offsets the outlay, shown by the arithmetic on l.307); L04 l.140 'as much as' (Remark 4.3, B invests twice as much as A, = 200,000 vs 100,000). No banned phrase or ellipsis-as-omission in learner text.",
 "CF1-b-structure-L03": "check_pages CF1 PASS at 2c8162b; whole L03 re-read: eyebrow, h1, lab, section order (s1 to s8), quiz (L03q1 to L03q9 in lesson order), references block and lesson-nav present.",
 "CF1-b-structure-L04": "check_pages CF1 PASS at 2c8162b; whole L04 re-read: sections 1 to 11, lab block, quiz (L04q1 to L04q9 with explanations), references block and lesson-nav present; meta description checked in CF1-b-r5-meta-L04-description.",
 "CF1-b-dag-concepts-L03-L04": "Re-run at 2c8162b: check_dag CF1 PASS. dfn ids unchanged: L03 def-fisher-relation, def-real-vs-nominal-cash-flows; L04 def-internal-rate-of-return, def-multiple-irr-problem; each defined once. The new L03 l.51 and card c088 use 'nominal cash flow' and 'real counterpart' defined in L03 Def 1.1 (l.57).",
 "CF1-b-hours-L03-L04": "Re-run this round: grep data-hours on L01 to L06 = 8 each; index.html l.29 data-hours-lessons=\"48\" data-hours-project=\"12\"; l.31 'Tier U · 60 hours'; index eyebrow '12 h project (20.0% of the 60 module hours)', 12/60 = 20.0%. 6 x 8 = 48, 48 + 12 = 60. Consistent. Pace not failed (architect ruling).",
 "CF1-b-process-words": "Re-scan this round (whole files, case-insensitive) for builder, verifier, round, REQUESTS, unit report, build: no learner-text hits; the only 'round' is the code call round( in the L04 lab (l.196). The new sentences contain none.",
 "CF1-b-grades-L04": "Re-read this round (key results l.450-457; Thm 1.3 l.65-68, Thm 2.1 l.77-79, Cor 2.2 l.85-86, Prop 3.3 l.107-110, Thm 4.1 l.125-127, Remark 5.1 l.305-307). Row l.456 T: Prop 3.3 gives the sign pattern and roots; Thm 4.1 with Example 4.2 gives r* = 120,000/100,000 - 1 = 0.20. Other T rows match their proofs (recomputed in CF1-b-numbers-L04).",
 "CF1-b-r5-recompute-delta": "Superseded and re-checked: `ls ledgers/CF1/scripts` at 2c8162b shows only the round-8 directory CF1-b-r8/, so the round-5 and round-6 scripts are absent and were not re-run. Every value they covered is re-derived by ledgers/CF1/scripts/CF1-b-r8/recompute_r8.py.",
 "CF1-b-r5-meta-L04-description": "Fix applied (L04 l.7 at 2c8162b): the text now reads 'the worked example of a project with two sign changes and two IRRs (Example 3.2)'. 'single' is gone, so the claim no longer conflicts with Problems M3 (l.359-363) and R1 (l.420-424), which are further two-sign-change projects. PASS. Wording note, not a FAIL: the clause 'has exactly one IRR, the worked example of ..., and the mutually exclusive case ...' is a loose list in a meta description; each part is accurate (Theorem 2.1 l.79, Example 3.2 l.100-103, Example 4.2 l.134-135).",
 "CF1-b-cards-L03-L04-other-29": "Cards re-checked this round: scripts/CF1-b-r8/cards_delta.py lists the card changes between de53f7e and 2c8162b; in the L03/L04 range only CF1-c033 (front 'Define the price level.'), CF1-c034 (front and back) and CF1-c088 (front) changed. Each re-checked: c033 back = Definition 1.1 (l.57, P_t = (1+pi)^t, P_0 = 1); c034 back = Definition 1.2 (l.62-64) with the lesson's l.67 'an exact definition ... not an empirical question'; c088 back = Definition 1.1 (l.57). Other L03/L04 cards are byte-identical to de53f7e and carry the round-7 check (basis fields verified there).",
 "CF1-b-cards-duplicate-scan": "Re-run at 2c8162b: ledgers/CF1/scripts/CF1-b-r8/embed_and_cards_check.py: cards 100; duplicate ids 0; duplicate fronts 0; duplicate backs 0. Card delta vs de53f7e: 12 cards changed (c001, c021, c033, c034, c065, c067, c071, c074, c084, c088, c097, c098), all text-only.",
 "CF1-b-r6-mutation-scope": "Lesson slice: no project grader and no mutants required (VERIFIER_RULES; round 5 to 7 notes). Re-checked this round: ledgers/CF1/ contains only scripts/ (no mutants/ directory).",
 "CF1-b-r6-verify-refs": "Re-run at 2c8162b: `.venv/bin/python tools/verify_refs.py --unit CF1` 'live re-verification of CF1: 2 of 560 entries, 0 problems', exit 0; `tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems', exit 0. The two lessons cite no source outside the CF1 entries.",
 "CF1-b-r6-page-smoke": "Re-run at 2c8162b: `tools/page_smoke.py --unit CF1 --pages L03 L04`: 'page_smoke modules/CF/CF1/L03.html: PASS' (lab 0.0 s), 'page_smoke modules/CF/CF1/L04.html: PASS' (lab 0.1 s), 'page_smoke CF1: PASS'.",
 "CF1-b-r6-pytest-labs": "Re-run at 2c8162b: `.venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py`: all dots, 100% (exit 0).",
 "CF1-b-r6-delta-coverage": "Delta de53f7e to 2c8162b, git diff --stat: 27 files; in this slice course/modules/CF/CF1/L03.html (2 lines: l.51, l.359), L04.html (1 line: l.7), cards.json (12 cards, text-only), index.html (eyebrow and paragraphs, hours values unchanged). Every hunk of the slice's files read; tests/labs/CF1 has no diff. The round-6 range (d57df1e to de53f7e) is superseded by this delta.",
 "CF1-b-notation": "Re-read this round: L04 Definition 1.1 (l.57, N the last date, local), Theorem 1.3 (l.67), Remark 5.1 (l.307), R3 (l.436-438), quiz (l.533). No symbol outside notation/notation.json or the page's local definitions.",
 "CF1-b-registry-citations": "Re-run at 2c8162b: verify_refs --unit CF1 (2 of 560, 0 problems) and --offline (560, 0 problems). L03 l.474-478 and L04 l.540-544 cite no registry key ('This lesson cites no registry source'); data-references lists are empty.",
 "CF1-b-r5-cards-scope-c037": "Carried check unchanged; re-read this round: CF1-c037 front, back and basis unchanged between de53f7e and 2c8162b (cards_delta.py lists no change for c037).",
 "CF1-b-prose-L03-l67-each-theorem": "L03 l.67 is byte-identical between de53f7e and 2c8162b (the delta touches only l.51 and l.359). Re-read this round: 'Theorem 1.3 is an algebraic identity between the two rates' with Theorem 2.2 (l.91, constant r and pi), Theorem 2.3 (l.102-103), Remark 2.4 (l.112-113), Theorem 1.3 (l.70-71, proof l.74).",
 "CF1-b-math-L03-theorems-proofs": "Re-checked because R1 solution (l.359) changed: R1 solution now reads 'The result holds for any path of inflation, because the price level cancels exactly. Theorem 2.2 states only the constant case.' Algebra: C^n_t = C^r_t P_t, prod(1+n_s) = prod(1+r_s) P_t, so C^n_t / prod(1+n_s) = C^r_t / prod(1+r_s); holds for any path of pi_s and r_s. Theorem 2.2 (l.91) assumes r and pi constant. Def 1.1-1.2 (l.56-64), Thm 1.3 (l.70-71), Thm 2.2 proof (l.95-98), Thm 2.3 proof (l.107-108), R2 (l.364-366), R3 (l.371-373), P1 (l.307-309) recomputed (see CF1-b-numbers-L03).",
 "CF1-b-grades-L03": "Re-checked because R1 (l.357-359) changed: key-results row l.389 'Consistency holds for an inflation path, with the price level cancelling (R1)', grade T, cites 'Problem R1, solution', which is the algebra above; grade T is correct. Other rows l.385-388 and l.390-391 unchanged and correct (Thm 1.3, Thm 2.2, Thm 2.3, Remark 2.4; C grades read off Lab 1).",
 "CF1-b-prose-L03-why-it-matters-l51": "",
}
NEW.pop("CF1-b-prose-L03-why-it-matters-l51")

NEW_ROWS = [
 {"id": "CF1-b-r8-delta-coverage", "check": "2.9-structure", "location": "git diff --stat de53f7e 2c8162b; course/modules/CF/CF1/L03.html, L04.html, cards.json, index.html; tests/labs/CF1/",
  "status": "PASS", "evidence": "Every hunk in this slice read. L03.html: l.51 (why-it-matters) and l.359 (R1 solution). L04.html: l.7 (meta description). cards.json: c001, c021, c033, c034, c065, c067, c071, c074, c084, c088, c097, c098 (text only; scripts/CF1-b-r8/cards_delta.py). index.html: eyebrow and paragraphs, hours unchanged. tests/labs/CF1: no diff. Lines outside these hunks are byte-identical to de53f7e."},
 {"id": "CF1-b-r8-L03-l51-why-it-matters", "check": "2.9-structure", "location": "course/modules/CF/CF1/L03.html l.51 (why-it-matters)", "status": "PASS",
  "evidence": "New clause 'proves that discounting nominal flows at the nominal rate and real flows at the real rate gives the same NPV' matches Theorem 2.2 (l.90-93). Lab 1 does show both cases (consistent and mixed lines, output file). The sentence omits the constant-rate hypothesis of Theorem 2.2, but it does not claim generality; R1 (l.357-359) separately covers a path of rates. Wording note: 'derives the exact relation' (same sentence, unchanged) names Definition 1.2, which the page states as a definition (l.62-64, l.67), while Theorem 1.3 derives the additive expansion. Not a numerical or claim error."},
 {"id": "CF1-b-r8-L03-R1-solution", "check": "2.4-math", "location": "course/modules/CF/CF1/L03.html l.359 (R1 solution)", "status": "PASS",
  "evidence": "Algebra re-derived (CF1-b-math-L03-theorems-proofs): the price-level cancellation holds for any path of pi_s and r_s, and the sentence 'Theorem 2.2 states only the constant case' matches Theorem 2.2 (l.91, r and pi constant). The removed sentence 'This lesson proves only the constant case' is no longer present; no claim was widened beyond the algebra."},
 {"id": "CF1-b-r8-cards-c033-c034-c088", "check": "2.7-cards", "location": "course/modules/CF/CF1/cards.json CF1-c033, CF1-c034, CF1-c088", "status": "PASS",
  "evidence": "Changed fronts and back checked against the lesson text: c033 'Define the price level.' vs Definition 1.1 (l.57, price level in year t is P_t = (1+pi)^t with P_0 = 1); c034 front 'State the Fisher relation between the nominal rate, the real rate and inflation.' and back 'It is an exact definition of the real rate for a given inflation rate, not an empirical claim (Definition 1.2)' vs l.62-67; c088 'Define a nominal cash flow and its real counterpart.' vs Definition 1.1 (l.57). Each basis (Definition 1.1, Definition 1.2) matches. Grades T match the lesson's Definitions."},
 {"id": "CF1-b-r8-L04-l7-meta-description", "check": "2.9-structure", "location": "course/modules/CF/CF1/L04.html l.7 (meta description)", "status": "PASS",
  "evidence": "The FAIL row CF1-b-r5-meta-L04-description is resolved. Each content clause is accurate: one outlay, non-negative inflows, not all zero, exactly one IRR (Theorem 2.1, l.79); the worked example with two sign changes and two IRRs (Example 3.2, l.100-103); the mutually exclusive case where IRR and NPV rank differently (Example 4.2, l.134-135). Wording note only."},
]

carry_ids = {
 "CF1-b-attribution-fisher", "CF1-b-simulated-label", "CF1-b-prose-L03-l67-each-theorem", "CF1-b-r5-L04-table-thm41-remark51",
 "CF1-b-r5-cards-scope-c037", "CF1-b-cards-L03-finiteness-and-positivity", "CF1-b-cards-L04-one-sign-change", "CF1-b-r6-alt-implementation",
 "CF1-b-r7-L04-l118-grid-step", "CF1-b-r7-L04-l456-crossover-T", "CF1-b-quiz-L03q5", "CF1-b-prose-L03-about43", "CF1-b-prose-L04-superlative",
 "CF1-b-prose-L03-misconception-overstates", "CF1-b-math-L03-thm22-23-convergence", "CF1-b-math-L03-P2", "CF1-b-math-L03-sec3-two-line",
 "CF1-b-math-L04-thms", "CF1-b-math-L04-R2", "CF1-b-math-L04-remark51", "CF1-b-prose-L04-why-one-sign-change", "CF1-b-term-conventional",
 "CF1-b-prose-L04-conventional-def", "CF1-b-heading-L04-s2", "CF1-b-r5-L03-l87-mixed-discounting", "CF1-b-r6-L03-l242-interpretation",
 "CF1-b-r6-L03-l469-quiz-explain", "CF1-b-r6-L04-l312-accept-or-reject",
}
new_ids = set(NEW)
rows = []
for r in OLD["rows"]:
    rid = r["id"]
    if rid in NEW:
        ev = NEW[rid]
        status = "PASS"
    elif rid in carry_ids:
        ev = PREFIX + r["evidence"]
        status = r["status"]
    else:
        raise SystemExit(f"unclassified round 7 row {rid}")
    assert status == "PASS", rid
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
rows += NEW_ROWS
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
missing = [r["id"] for r in OLD["rows"] if r["id"] not in ids]
assert not missing, missing
unused = sorted(k for k in NEW if k not in {r["id"] for r in OLD["rows"]})
assert not unused, unused
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
 "unit": "CF1", "slice": "CF1-b", "round": 8,
 "verifier": "independent Haiku verifier, CF1 slice b (L03, L04 and their lab twins), round 8; did not build CF1 and shares no context with the builders or earlier verifiers",
 "pin": "2c8162b",
 "base": "de53f7e (round 7 pin; round 7 fragment /tmp/fanout-frags/CF1-b.round7.json, context only; its PASS rows carried only where the cited lines are byte-identical)",
 "previous_ledger": "/tmp/fanout-frags/CF1-b.round7.json",
 "checkout": "/tmp/verify8-CF1-b (detached at 2c8162b, .venv symlinked)",
 "scratch": "/tmp/cf1-v/CF1-b-r8",
 "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Lesson slice: no project grader, so no alternative-implementation check and no mutants (round 5 to 7 notes; ledgers/CF1/ has no mutants/ directory). Not applicable, not a skipped check.",
  "Previous FAIL row CF1-b-r5-meta-L04-description is fixed at 2c8162b (L04 l.7 now 'the worked example'); re-verified as PASS.",
  "Changed hunks in this slice: L03 l.51, L03 l.359, L04 l.7, cards c033, c034, c088 (plus card text changes outside the slice). All re-verified; other lines carried with the prefix.",
  "Not re-run: round 5 and 6 scripts (absent). Lab copies E2 and E3 run from ledgers/CF1/scripts/CF1-b-r8/lab_copy_claims.py. Live verify_refs on CF1 checks 2 of 560 entries; no external source is cited by these lessons, so no publisher or SEC site was contacted.",
  "Hours: consistent (6 x 8 = 48; 48 + 12 = 60). Hour pace not judged (architect ruling).",
 ],
 "summary": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "carried": len([r for r in rows if r["evidence"].startswith("Carried")]),
             "re_verified": len([r for r in rows if not r["evidence"].startswith("Carried")]), "non_pass": [r["id"] for r in rows if r["status"] != "PASS"]},
}
out = Path(sys.argv[1])
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", verdict)
