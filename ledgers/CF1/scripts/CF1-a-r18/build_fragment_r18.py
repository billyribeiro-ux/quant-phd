"""Build ledgers/CF1/CF1-a.json for round 18 (slice a). Carried rows keep their round-17 ids and evidence."""
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-a.round17.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in PREV["rows"]}
PIN_PREV = "fefbf8b"

CARRY = {
    "CF1-a-hub-reading-attribution": "course/modules/CF/CF1/index.html lines 164-168",
    "CF1-a-hub-scope-simulated": "course/modules/CF/CF1/index.html line 161; L01.html lines 55, 68, 172, 176-180, 314; L02.html lines 153, 160-164",
    "CF1-a-hub-data-file-claim": "course/modules/CF/CF1/index.html line 161; L01.html line 474; L02.html line 429",
    "CF1-a-hub-numbers-claim": "course/modules/CF/CF1/index.html line 161",
    "CF1-a-L01-corollary42-wording": "course/modules/CF/CF1/L01.html lines 138, 143, 549",
    "CF1-a-L01-grades": "course/modules/CF/CF1/L01.html lines 456-467",
    "CF1-a-L01-misconception-and-quiz": "course/modules/CF/CF1/L01.html lines 331-341, 477-550",
    "CF1-a-L01-dag-concepts": "course/modules/CF/CF1/L01.html lines 37, 59",
    "CF1-a-L01-hours": "course/modules/CF/CF1/L01.html line 34",
    "CF1-a-L01-citations": "course/modules/CF/CF1/L01.html line 557",
    "CF1-a-L01-line55-simulated-label": "course/modules/CF/CF1/L01.html line 55",
    "CF1-a-L01-period-convention": "course/modules/CF/CF1/L01.html lines 55, 206-207, 237",
    "CF1-a-L01-line323-one-rate": "course/modules/CF/CF1/L01.html line 323",
    "CF1-a-L01-line51-why-it-matters": "course/modules/CF/CF1/L01.html line 51",
    "CF1-a-L01-remark32-conventional": "course/modules/CF/CF1/L01.html line 111",
    "CF1-a-L01-meta-and-hub-card-conventional": "course/modules/CF/CF1/L01.html line 7; course/modules/CF/CF1/index.html line 138",
    "CF1-a-L01-misc2-conventional-referent": "course/modules/CF/CF1/L01.html line 338",
    "CF1-a-L01-canon-line322-scope": "course/modules/CF/CF1/L01.html line 322",
    "CF1-a-L01-misc2-positive-needs-C0": "course/modules/CF/CF1/L01.html line 338",
    "CF1-a-r11-date0-term": "course/modules/CF/CF1/L01.html lines 111, 220, 275, 306, 338",
    "CF1-a-r11-changed-numbers": "course/modules/CF/CF1/L01.html lines 111, 322, 338, 438; L02.html lines 280, 300, 508; cards.json CF1-c012",
    "CF1-a-r11-alt-implementations": "tests/labs/CF1/lab-CF1-L01-1.py npv_dollars; tests/labs/CF1/lab-CF1-L02-1.py npv_dollars",
    "CF1-a-r11-check-liveness": "tests/labs/CF1/lab-CF1-L02-1.py lines 220-226; course/modules/CF/CF1/L02.html line 272",
    "CF1-a-L02-lab-docstring": "tests/labs/CF1/lab-CF1-L02-1.py lines 2-8; course/modules/CF/CF1/L02.html lines 165-168",
    "CF1-a-L02-line51-citation": "course/modules/CF/CF1/L02.html line 51",
    "CF1-a-L02-lab-shield-check": "tests/labs/CF1/lab-CF1-L02-1.py lines 223-226",
    "CF1-a-L02-prose-claims": "course/modules/CF/CF1/L02.html line 51; tests/labs/CF1/lab-CF1-L02-1.py lines 220-226, 242",
    "CF1-a-L02-wc-sign": "course/modules/CF/CF1/L02.html lines 51, 128",
    "CF1-a-L02-grades": "course/modules/CF/CF1/L02.html lines 416-423",
    "CF1-a-L02-dag-concepts": "course/modules/CF/CF1/L02.html lines 22-60, 280; check_dag CF1",
    "CF1-a-L02-hours": "course/modules/CF/CF1/L02.html line 34",
    "CF1-a-L02-citations": "course/modules/CF/CF1/L02.html lines 508, 509",
    "CF1-a-L02-references-scope": "course/modules/CF/CF1/L02.html line 508",
    "CF1-a-notation": "notation/notation.json; course/modules/CF/CF1/L01.html lines 111, 337-338; course/modules/CF/CF1/L02.html lines 51, 280, 508",
    "CF1-a-cards-L01-L02": "course/modules/CF/CF1/cards.json cards CF1-c001 to CF1-c032, CF1-c089, CF1-c090 (byte-identical); L01.html line 338",
    "CF1-a-L02-remark34-npv-stream": "course/modules/CF/CF1/L02.html line 148",
    "CF1-a-L02-tax-credit-branch": "tests/labs/CF1/lab-CF1-L02-1.py lines 170-172; course/modules/CF/CF1/L02.html lines 116, 281",
    "CF1-a-L02-line280-accrual": "course/modules/CF/CF1/L02.html line 280",
    "CF1-a-r17-delta": "git diff --stat fefbf8b 7143726 (superseded for this round by CF1-a-r18-delta)",
    "CF1-a-r17-hub-prose-scope": "course/modules/CF/CF1/index.html lines 151-152; course/modules/CF/CF1/project.html lines 44-45, 54, 58, 128, 135-136",
}
FRESH_TEXT = {}  # filled from the verification record below

FRESH = {
    "CF1-a-gate-check-pages": ("tools/check_pages.py --unit CF1", "exit 0, 'check_pages CF1: PASS' (scripts/CF1-a-r18/out/check_pages.out)"),
    "CF1-a-gate-check-dag": ("tools/check_dag.py --all", "exit 0, 'check_dag CF1: PASS' and 'check_dag AP1: PASS' (scripts/CF1-a-r18/out/check_dag.out)"),
    "CF1-a-gate-run-labs": ("tools/run_labs.py --unit CF1", "exit 0, 'run_labs CF1: PASS (9/9)' (scripts/CF1-a-r18/out/run_labs.out)"),
    "CF1-a-gate-page-smoke": ("tools/page_smoke.py --unit CF1 --pages index L01 L02", "exit 0, index, L01, L02 and their labs PASS (scripts/CF1-a-r18/out/page_smoke.out)"),
    "CF1-a-gate-lint-types": ("tests/labs/CF1; mypy --no-incremental tests/labs/CF1", "ruff check . 'All checks passed!'; ruff format --check tests/labs/CF1 '9 files already formatted'; mypy 'Success: no issues found in 9 source files' (scripts/CF1-a-r18/out/ruff_*.out, mypy.out)"),
    "CF1-a-gate-pytest": ("tests/test_labs.py tests/test_page_checks.py tests/test_refs.py", "pytest -q exit 0, all dots (scripts/CF1-a-r18/out/pytest.out)"),
    "CF1-a-cite-verify-refs": ("tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", "offline: '560 entries, 0 problems'; live CF1: '2 of 560 entries, 0 problems', both exit 0 (scripts/CF1-a-r18/out/refs_*.out)"),
    "CF1-a-hub-prereq-placement-math": ("course/modules/CF/CF1/index.html lines 27-66, 68, 90", "line 68 changed and re-derived: 7 of 9 is 77.8 percent (below 80), 8 of 9 is 88.9 percent; items 1-9 recomputed: 110/1.1=100; annuity 2.486852 x 100 = 248.69; 50/0.05=1000; 100/(0.06-0.02)=2500 form; 1000x1.05^2=1102.50; AC1 identities; skill checks 400x0.75+0.25x300=375 and 0.25x300=75"),
    "CF1-a-hub-hours": ("course/modules/CF/CF1/index.html lines 8, 31, 38-41, 136", "48 = 6 x 8 lesson hours; 12 project; 60 total; split 80.0% / 20.0% matches; L01 and L02 are 8 h each (cards line 138-139); no arithmetic inconsistency"),
    "CF1-a-hub-lesson-map": ("course/modules/CF/CF1/index.html lines 136-143", "L05 card line 142 changed; 'what payback ignores after its payback year' checked against L05.html line 70 and Proposition 2.1 (lines 75-76) and the proof (lines 79-80); L01 and L02 cards lines 138-139 match their headings"),
    "CF1-a-hub-ladder-worked-example": ("course/modules/CF/CF1/index.html lines 149, 151; L02.html lines 153-157; lab output lines 257-271", "paragraph line 149 changed: 'You may skip them when you reach the placement bar and answer both skill checks' matches line 68; line 151 Worked example (SIMULATED, 926.00 at step 7) matches project.html line 44 (Lab 1 worked example) and line 128 ('step 7, NPV at 0.10: 926.00 dollars')"),
    "CF1-a-hub-L05-card": ("course/modules/CF/CF1/index.html line 142", "fixed in 7143726: the card now reads 'what payback ignores after its payback year'. L05.html line 70 ('When a payback year exists, neither rule reads a year after it'), line 75-76 (Proposition 2.1, simple payback reads only its payback years) and line 228 ('It ignores flows after its year') agree; the card's 'no finding ... on firm use' matches L05.html lines 234 and 237 and question L05q9 (line 448-451). Round-17 FAIL resolved."),
    "CF1-a-L01-read-full": ("course/modules/CF/CF1/L01.html lines 1-570", "read in full this round, lines 1-570 (page ends at 570 with </html>)"),
    "CF1-a-L01-num-ex12": ("course/modules/CF/CF1/L01.html line 68", "recomputed: 3000/1.08=2777.78, 3200/1.08^2=2743.48, 3400/1.08^3=2699.03, 3600/1.08^4=2646.11, 3800/1.08^5=2586.22; sum 13452.62; unrounded 13452.615; NPV 3452.62 (python -I, this round)"),
    "CF1-a-L01-num-rem13": ("course/modules/CF/CF1/L01.html line 73", "rounded factors 0.9259, 0.8573, 0.7938, 0.7350, 0.6806 give 13452.26 (recomputed, 2777.70+2743.36+2698.92+2646.00+2586.28); 36 cents below 13452.62"),
    "CF1-a-L01-num-M1": ("course/modules/CF/CF1/L01.html line 356", "-100+60/1.1+60/1.21 = 4.1322 -> 4.13; rounded terms 54.55+49.59 = 104.14 -> 4.14 (recomputed)"),
    "CF1-a-L01-num-M2": ("course/modules/CF/CF1/L01.html line 363", "1.06^-4 = 0.79209366; A = 3.46510561; -500+150x3.46510561 = 19.76584 -> 19.77 (recomputed)"),
    "CF1-a-L01-num-rem52-ex53": ("course/modules/CF/CF1/L01.html lines 167, 172", "A(0.10,3)=2.486852; rounded power gives 2.4870 (recomputed); 120x2.486852 = 298.42 (recomputed 298.422)"),
    "CF1-a-L01-num-M3-E": ("course/modules/CF/CF1/L01.html lines 333, 336-337, 370", "-1000+600/1.2+600/1.44 = -83.33; undiscounted 200.00; M3 -200+120/1.2+120/1.44 = -16.67, r=0 gives 40.00 (recomputed); Lab 1 Part A 7,000.00 at 0 and -46.94 at 0.20 match the printed expected block"),
    "CF1-a-L01-num-P3": ("course/modules/CF/CF1/L01.html line 395", "difference (1+r)^-2 (10-120r); r*=1/12=8.33 percent; at 0: 30 and 20; at 0.10: 7.44 and 9.09; at r*: -100+1440/13=10.77 (recomputed)"),
    "CF1-a-L01-num-R1-R3": ("course/modules/CF/CF1/L01.html lines 431, 445-446", "R3 solution line 446 changed and recomputed: 1.05/1.06 gives -0.009434 (shown as -0.0094), 1.05/1.03 gives +0.019417 (shown as +0.0194); borrowing rate rejects, lending rate accepts (NPV sign rule, Section 1); R1 factor (1+r)^(1/2) recomputed by algebra"),
    "CF1-a-L01-num-R2-E1-E3": ("course/modules/CF/CF1/L01.html lines 438, 406, 420", "R2 0.50 vs 0.12 per dollar; E1 sign change between 0.15 and 0.20 with Proposition 3.1 single-crossing; E3 ranges match the twin (outlay randint(50_000, 2_000_000) cents = 500 to 20,000 dollars, level 100 to 4,000, years 1-15, rate 2-15 percent, SEED 20261027)"),
    "CF1-a-L01-math-props": ("course/modules/CF/CF1/L01.html lines 79-106, 124-143, 155-163", "Propositions 2.1, 3.1 (derivative sign and limit), 4.1 (induction for B_t, B_n = 0), Corollary 4.2, 5.1 (geometric sum) re-read and re-derived; no gap found"),
    "CF1-a-L01-lab": ("course/modules/CF/CF1/L01.html line 177 (hypothesis), 178-287 (code), 288-312 (expected), 314 (interpretation); tests/labs/CF1/lab-CF1-L01-1.py", "twin stdout compared with the page expected block by coursekit.compare_output (tolerance 1e-6): equal (scripts/CF1-a-r18/out/L01_twin_stdout.out); run_labs PASS; twin run python -I -W error exit 0"),
    "CF1-a-L01-banned-process": ("course/modules/CF/CF1/L01.html, L02.html, index.html (whole pages)", "grep for roughly, about, historically, typically, usually, generally, builder, verifier, round, REQUEST, unit report, ellipsis: no hit in learner prose (only 'round late', 'round the factor last' as math names, and 'about how to read the number', 'about projects in general' which are not banned phrases)"),
    "CF1-a-L02-read-full": ("course/modules/CF/CF1/L02.html lines 1-522", "read in full this round, lines 1-522"),
    "CF1-a-L02-num-worked": ("course/modules/CF/CF1/L02.html lines 153-157", "6900-2800=4100; 4100-3000=1100; tax 275; OCF 3825 (both routes); NWC 690; year-1 total 3135; year-4 recovery 680 (balance end of year 3 = 680): recomputed"),
    "CF1-a-L02-num-wc-pv": ("course/modules/CF/CF1/L02.html line 300", "-690/1.08+10/1.08^2+680/1.08^4 = -130.4952 (recomputed, python -I) -> -130.50 to the cent; the sum of the four flows is zero"),
    "CF1-a-L02-num-problems": ("course/modules/CF/CF1/L02.html lines 315-397, 442-501", "M1 410.00 (both routes); M2 -160, -40, 0, +200 sum 0; M3 82.64 and -417.36 recomputed; R1 r/(1+r) fraction; R2 -13.21 (recomputed -13.2094) and 13.2 percent; quiz numerics 410, 60, -13.21, 0, 75 recomputed"),
    "CF1-a-L02-math-props": ("course/modules/CF/CF1/L02.html lines 62-106, 109-111, 127-144", "Propositions 1.2, 1.3, 2.2 (algebra), Corollary 2.3, Proposition 3.2 (telescoping), Proposition 3.3 re-derived; no gap"),
    "CF1-a-L02-lab": ("course/modules/CF/CF1/L02.html line 161 (hypothesis), 162-252 (code), 253-271 (expected), 272 (interpretation); tests/labs/CF1/lab-CF1-L02-1.py", "twin stdout equals page expected block under coursekit.compare_output (scripts/CF1-a-r18/out/L02_twin_stdout.out); run_labs PASS; python -I -W error exit 0"),
    "CF1-a-scope-words": ("course/modules/CF/CF1/index.html lines 142, 149, 151; L01.html line 446; L02.html line 508", "scope-word scan over every changed sentence this round (only, all, always, as much as, same, drives, offsets, raises): none in the changed sentences; L02 line 508 universal list unchanged"),
    "CF1-a-mutants": ("tests/labs/CF1/lab-CF1-L01-1.py, lab-CF1-L02-1.py; ledgers/CF1/mutants/CF1-a-r7, -r8, -r9, -r10, -r11, -r17, -r18", "re-run all 70 slice-a mutants with python -I -W error against the twins (scripts/CF1-a-r18/run_mut18.py, out/mutants_r18.txt): 67 killed, 3 survived; the 3 survivors are listed in CF1-a-r18-mutant-survivors (out of scope, with reasons)"),
    "CF1-a-r11-lab-expected-vs-twin": ("course/modules/CF/CF1/L01.html lines 178-313; L02.html lines 162-271; tests/labs/CF1/lab-CF1-L01-1.py, lab-CF1-L02-1.py", "both expected blocks compared with twin stdout this round through coursekit.compare_output: equal under tolerance 1e-6 (True) for L01 and L02"),
    "CF1-a-r11-survivors": ("ledgers/CF1/mutants/CF1-a-r11/n05_l02_identity_check_stubbed_true.py; ledgers/CF1/mutants/CF1-a-r9/r9_m07_no_tax_credit.py; L02.html lines 87, 116, 272", "both still survive this round and remain out of scope: r9_m07 (no tax credit) is not exercised because EBIT is positive in every year of the Lab 2 seed (1100, 1800, 800, 600), and the L02 lab does not claim to test the credit branch (Remark 2.4 says it does not test any firm's tax position); n05 replaces the identity test with a constant True; Proposition 2.2 holds for every flow, so on this seed the printed line is unchanged, and the page (L02.html line 272) says only that the checks confirm the identity numerically"),
    "CF1-a-r17-changed-card-numbers": ("course/modules/CF/CF1/cards.json CF1-c104 (changed this round), CF1-c023, c027, c101 (carried); L02.html lines 106, 153, 269-270, 296", "CF1-c104 re-verified this round: no number in its text; 'Lesson 1' is the rate lesson; 'convention, Section 1 (third rule)' matches L02.html line 83. CF1-c023, c027, c101: byte-identical since fefbf8b, numbers checked in round 17"),
    "CF1-a-r17-new-mutants": ("ledgers/CF1/mutants/CF1-a-r17/r17_m01..r17_m04 (killed), r17_probe (survives, out of scope)", "re-run this round with python -I -W error: r17_m01..m04 KILLED; r17_probe SURVIVED, an exact float equality instead of the 1e-6 tolerance; it still prints True on this seed, and the page (L02.html line 272) describes a numerical confirmation, not an exact-equality test (out of scope)"),
    "CF1-a-r17-alt-implementations": ("ledgers/CF1/scripts/CF1-a-r17/alts/alt_r17_a_tolerance_1e9.py, alt_r17_b_horner_npv.py, alt_r17_c_shield_from_difference_tolerance_1e4.py", "re-run this round: each prints output that passes coursekit.compare_output against the L02 expected block (True, tolerance 1e-6)"),
    "CF1-a-r17-gate-tests-wide": ("ruff check . ; pytest tests/test_labs.py tests/test_page_checks.py tests/test_refs.py", "ruff check . 'All checks passed!'; pytest exit 0 (re-run this round)"),
}
NEW = {
    "CF1-a-r18-delta": ("git diff --stat fefbf8b 7143726 (slice files)", "slice files changed: index.html (lines 68, 142, 149), L01.html (line 446 only), cards.json (c104 in slice; c097 is an L05 card, out of slice). L02.html, both twins, notation/ and tests/labs/CF1/ unchanged. Out-of-slice changes (L05, L06, project.html, grader/test_project.py, AC1 and AC4 labs) not verified here"),
    "CF1-a-r18-L01-R3-rewrite": ("course/modules/CF/CF1/L01.html line 446 (Problem R3 solution)", "new sentences: 'The period-0 value is the period-0 flow plus the period-1 flow discounted at the rate in question.' (formula is C0 + C1/(1+r), correct); 'The problem does not say which of the two rates the owner faces, so each is computed.' (the statement at line 444 says 'lend at 3 percent or borrow at 6 percent'); values -0.0094 and +0.0194 recomputed; 'rejects ... accepts' follows Section 1 rule"),
    "CF1-a-r18-c104-financing-convention": ("course/modules/CF/CF1/cards.json CF1-c104", "back text 'Financing stays out of the flows ... counting interest as a project flow counts the cost of capital twice' matches L02.html line 83 (third rule, labelled a convention); 'the rate of Lesson 1 already charges for that capital' matches L01.html line 55 (the rate is the return on an alternative of the same risk); grade C matches the grade legend (L02.html line 46: C = single study or convention)"),
    "CF1-a-r18-mutant-survivors": ("ledgers/CF1/mutants/CF1-a-r9/r9_m07_no_tax_credit.py; ledgers/CF1/mutants/CF1-a-r11/n05_l02_identity_check_stubbed_true.py; ledgers/CF1/mutants/CF1-a-r17/r17_probe_l02_identity_exact_equality.py", "3 survivors out of 70 (scripts/CF1-a-r18/out/mutants_r18.txt): none violates a sentence in project.html, the grader docstrings, the plan or the contract. project.html line 198 states the negative-tax credit for the ENGINE, which grader/test_project.py line 728 tests; the L02 lab does not implement the engine, its seed has positive EBIT every year, and its docstring states the convention without claiming a test of the branch: out of scope, PASS"),
    "CF1-a-r18-alt-implementations": ("ledgers/CF1/scripts/CF1-a-r18/alts/alt_r18_a_fsum_tol1e9_summed_annuity.py, alt_r18_b_horner_npv_geometric_annuity.py, alt_r18_c_horner_npv_tol1e4.py", "three valid alternatives (math.fsum with tolerance 1e-9 and summed annuity factor; Horner accumulation with geometric annuity; Horner NPV with tolerance 1e-4) pass coursekit.compare_output against the expected blocks (True, tolerance 1e-6); alt_a prints -0.000000 where the twin prints 0.000000, which the numeric comparator accepts"),
    "CF1-a-r18-new-mutants": ("ledgers/CF1/mutants/CF1-a-r18/ (six mutants); ledgers/CF1/scripts/CF1-a-r18/make_new.py", "six new student-error mutants, all KILLED: loan without interest accrual (L01 Part D balance ends nonzero), annuity one year long (Part B gap), additivity subtracting the second stream (Part C), NPV dropping the date-0 outlay (L02), shield check comparing OCF instead of the difference (L02), working capital at 8 percent of revenue (L02)"),
}

ids17 = [r["id"] for r in PREV["rows"]]
rows = []
for rid in ids17:
    old = prev_rows[rid]
    if rid in FRESH:
        loc, ev = FRESH[rid]
        rows.append({"id": rid, "check": old["check"], "location": loc, "status": "PASS", "evidence": ev})
    elif rid in CARRY:
        files = CARRY[rid]
        rows.append({
            "id": rid,
            "check": old["check"],
            "location": files,
            "status": "PASS",
            "evidence": f"Carried from round 17 ({files} byte-identical since the previous pin {PIN_PREV}): {old['evidence']}",
        })
    elif rid == "CF1-a-hub-L05-card":
        loc, ev = FRESH_HUB = ("course/modules/CF/CF1/index.html line 142", FRESH["CF1-a-hub-L05-card"][1])
        rows.append({"id": rid, "check": old["check"], "location": loc, "status": "PASS", "evidence": ev})
    else:
        raise SystemExit(f"row {rid} not covered")
for rid, (loc, ev) in NEW.items():
    rows.append({"id": rid, "check": rid.replace("CF1-a-", "").replace("-", " "), "location": loc, "status": "PASS", "evidence": ev})

# every round-17 row id is kept; the L05 card is the one FAIL that is now re-verified and PASS
assert {r["id"] for r in rows} >= set(ids17)
for r in rows:
    if r["status"] != "PASS":
        raise SystemExit("non-PASS row " + r["id"])

mutants = []
mdir = ROOT / "ledgers/CF1/mutants/CF1-a-r18"
for f in sorted(mdir.glob("*.py")):
    name = f.stem
    mutants.append({
        "id": "r18-" + name.split("_")[1],
        "file": f"ledgers/CF1/mutants/CF1-a-r18/{f.name}",
        "description": "student-error mutant of the lab twin (new, round 18): " + name,
        "killed_by": "round 18 run_mut18.py: stdout differs from twin, or run fails (killed)",
    })

fragment = {
    "unit": "CF1",
    "slice": "CF1-a",
    "round": 18,
    "verifier": "independent Haiku verifier, round 18, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1 and shares no context with the builders",
    "pin": "7143726",
    "base": PIN_PREV,
    "previous_fragment": "/tmp/fanout-frags/CF1-a.round17.json",
    "checkout": str(ROOT),
    "scratch": "/tmp/CF1-v/a-r18",
    "verified_at": sys.argv[2],
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 18 delta from fefbf8b: index.html lines 68, 142, 149; L01.html line 446 (Problem R3 solution); cards.json CF1-c104 (in slice) and CF1-c097 (an L05 card, out of slice). L02.html, both lab twins and notation/ are byte-identical to the previous pin.",
        "The round-17 FAIL (CF1-a-hub-L05-card) is re-verified as PASS: the card now reads 'after its payback year', which agrees with L05.html line 70 and Proposition 2.1.",
        "Six new student-error mutants (m04-r18_m01..m06) were killed; all 70 slice-a mutants were re-run; 67 killed, 3 out-of-scope survivors (r9_m07, n05, r17_probe).",
        "Three new alternative implementations (ledgers/CF1/scripts/CF1-a-r18/alts) and three round-17 alternatives pass the repository comparator. alt_r18_a prints -0.000000 where the twin prints 0.000000; the comparator accepts it.",
        "Not checked: the out-of-slice pages (L03 to L06, project.html, the project grader) and the live reference fetch beyond the two CF1 entries that verify_refs re-verifies live; no bot-protected source was read.",
        "Hours: declared hours (48 lesson, 12 project, 60 total, 80/20 split) are arithmetically consistent with the lesson cards; per the architect ruling, no pace-based hour estimate fails a row.",
    ],
    "summary": f"Slice CF1-a round 18 (pin 7143726, delta from fefbf8b): PASS, {len(rows)} rows, all PASS. The round-17 FAIL on the hub L05 card is resolved. Changed subjects re-verified: hub placement sentence (line 68), hub L05 card (line 142), hub ladder paragraph (line 149), L01 Problem R3 solution (line 446), card CF1-c104. Gates re-run: check_pages, check_dag, run_labs (9/9), page_smoke, ruff, mypy, pytest (three files), verify_refs offline and live (CF1). Mutants: 70 run, 67 killed, 3 out-of-scope survivors. Alternatives: 6 run, all match.",
}
out = ROOT / "ledgers/CF1/CF1-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants))
