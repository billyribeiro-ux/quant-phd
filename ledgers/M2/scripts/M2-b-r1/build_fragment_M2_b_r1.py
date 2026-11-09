import json, datetime
PIN = "2a805c831410ab77c38c227f7e121e8537193ce9"
BASE_PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
CK = "/Users/billyribeiro/.fanout/wt/verifyG1-M2-b"
S = "ledgers/M2/scripts/M2-b-r1"
base_ids = [r["id"] for r in json.load(open("/Users/billyribeiro/.fanout/frags/F2-M2-b.round1.json"))["rows"]]
CARRY = ("Carried from round 1 (base fragment ~/.fanout/frags/F2-M2-b.round1.json, pin 95f3f8cb; "
         "course/modules/M/M2/L07.html..L12.html, course/modules/M/M2/index.html, tests/labs/M2 twins, "
         "notation/notation.json, references/ and ledgers/M2/mutants/ byte-identical since that pin, "
         "per git diff --name-only 95f3f8cb..2a805c83): ")
fresh = {}
fresh["RUN-M2-CHECKS"] = ("PASS", "tools/check_pages.py --unit M2; tools/check_dag.py --unit M2; tools/check_projects.py --unit M2; tools/run_labs.py --unit M2; tools/build_site.py --check",
    "Fresh at 2a805c83: r1_check_pages.out 'check_pages M2: PASS' exit 0; r1_check_dag.out 'check_dag M2: PASS' exit 0; r1_check_projects.out 'check_projects M2: PASS' exit 0; r1_run_labs_M2.out 'run_labs M2: PASS (27/27)' exit 0; r1_build_site_check.out 'site data current: 6 outputs' exit 0; --all variants r1_check_pages_all.out and r1_check_dag_all.out PASS for LX1, LX2, PC3, exit 0. Command record: " + S + "/run_gates_r1.sh.")
fresh["LAB-GATES"] = ("PASS", "tests/labs/M2 lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "Fresh: r1_ruff_labs.out 'All checks passed!' exit 0; r1_ruff_format.out '27 files already formatted' exit 0; r1_mypy_labs.out 'mypy --no-incremental tests/labs/M2: Success: no issues found in 27 source files' exit 0; r1_pytest_labs_smoke.out pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py -k 'M2 or lab or page or refs' exit 0 (all dots, no failures).")
fresh["PAGE-SMOKE-L07-L12"] = ("PASS", "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12",
    "Fresh: r1_page_smoke_L07_L12.out 'page_smoke modules/M/M2/L07..L12.html: PASS', 'page_smoke M2: PASS', exit 0 (run alone for the slice pages).")
fresh["TWIN-ISOLATED"] = ("PASS", "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py",
    "Fresh: r1_twins_isolated.out: each twin run as python -I -W error exit 0, stderr 0 bytes for L07, L08, L09, L10, L11, L12.")
fresh["REFS-OFFLINE"] = ("PASS", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2; tools/build_site.py --check; course/modules/M/M2/L07.html..L12.html",
    "Fresh: r1_verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' exit 0; r1_verify_refs_unit.out 'live re-verification of M2: 2 of 560 entries, 0 problems' exit 0; r1_build_site_check.out 'site data current: 6 outputs' exit 0. Slice pages carry no new reference (references/ unchanged in the delta).")
fresh["DELTA-HUNKS"] = ("PASS", "course/modules/M/M2/cards.json (only slice subject changed); " + "course/modules/M/M2/L07-L12.html and six twins unchanged",
    "git diff --name-only 95f3f8cb..2a805c83 over course/modules/M/M2, tests/labs/M2, notation, references, tools, tests, ledgers/M2/mutants lists only course/modules/M/M2/cards.json for the slice (r1_delta.out; out-of-slice tests/labs/E4, tests/labs/M3, tests/test_lx1_project_lab3.py are not M2). cards.json: 398 -> 395 cards; 0 added; removed M2-c417 (L08), M2-c428 (L08), M2-c429 (L10); 28 changed ids, of which L07-L12 are c096, c099, c102, c104, c107, c111, c112, c113, c114, c134, c143, c145, c146, c147, c152, c161, c162, c163, c169, c177, c178, c180, c422, c423, c425 (all re-verified below); out-of-slice changed ids c064 (L06), c265 (L18), c430 (L24) not graded here (ruling 30). Every changed slice card is listed in r1_delta.out and cards_base_95f3f8cb.json / cards_head_2a805c83.json.")
fresh["CARD-L07"] = ("PASS", "course/modules/M/M2/cards.json: M2-c096, M2-c422 (changed); other 22 L07 cards byte-identical",
    "Re-verified against L07.html text: c422 (grade C->T, basis removed) is answered by Proposition 2.3 (every n, x != 1) and Lab 1 part B prints exact checks for n=0..10 at x=3/10 (lab uses fractions.Fraction; r1 lab run output 'part B: error equals x^(n+1)/(1-x) exactly'). c096 (T) rests on Proposition 2.3: at x=3/10 the error shrinks, at x=2 the error is -2^(n+1), so -2048 at n=10 (Lab 1 part C output 'error = -2048'); Misconception 3 of L07 states the same. No new numbers outside the lesson or lab output (cards_checks: none missing).")
fresh["CARD-L08"] = ("PASS", "course/modules/M/M2/cards.json: changed M2-c099, c102, c104, c107, c111, c112, c113, c114; removed M2-c417, M2-c428; other L08 cards byte-identical",
    "Re-verified against L08.html: c099 and c102, c104, c111, c112, c113, c114 carry 'Under Assumption 1.1' (Theorem 1.2, Theorem 2.1, Example 2.3, Example 2.4 are stated under Assumption 1.1 in L08.html); c102 xi and Lagrange-form identity = Example 2.3 text; c104 ratio 2^(n+2)(1-x) in [2^(n+1),2^(n+2)) = Example 2.4 text; c111 = Problem L08-R3 and (1/2)^n; c112 = Misconception 1; c113 = Remark 3.2, Misconception 2; c114 bound 5.625, 8.4375 vs remainder 0.9, 0.54 = Remark 3.3 and Misconception 3 values (recomputed: 0.36/0.064, 0.216/0.0256, 0.36/0.4, 0.216/0.4). c107 (grade C, Lab 1 part C): printed R_1(0.9)=8.10000000 and Lagrange form 8.10000000 at printed xi 0.535841; exact xi=1-0.1^(1/3) gives 8.1 exactly. Removed c417/c428/c429 are referenced nowhere (grep). Assumption 1.1 is defined in L08.html.")
fresh["CARD-L09"] = ("PASS", "course/modules/M/M2/cards.json: changed M2-c423, M2-c425; other 17 L09 cards byte-identical",
    "Re-verified against L09.html: c423 = Misconception 2 (endpoint sums 1/8 and 1/8, integral 1/6 from Lesson 10 Theorem 2.1 under Assumption 2.1 of Lesson 6, forward reference not derived); c425 = Remark 1.4 (integrability results are for monotone f) and Misconception 2 (x(1-x) integrability cited from Lesson 11 Lemma 1.1 with Theorem 2.2 for x and x^2). Both page-level statements match. Base row's 'c129 removed' is not a delta fact: M2-c129 is absent at both 95f3f8cb and 2a805c83.")
fresh["CARD-L10"] = ("PASS", "course/modules/M/M2/cards.json: changed M2-c134, c143, c145, c146, c147; removed M2-c429; other L10 cards byte-identical",
    "Re-verified against L10.html: c134 (MVT on each subinterval, Theorem 1.2 under Assumption 2.1, Remark 1.3, proof of Theorem 2.1) matches; c143 matches 'Where the canon breaks' (continuity on the closed interval; open-interval continuity leaves a and b uncovered); c145 = Misconception 1 (integrability of f=F' is a hypothesis); c146 = Misconception 2, G(x)=x/(1+x)+5 gives G(1)-G(0)=1/2 and G(1)=11/2 (recomputed); c147 = Misconception 3 (Example 2.2, F not polynomial). c429 removed (duplicate MVT card; referenced nowhere).")
fresh["CARD-L11"] = ("FAIL", "course/modules/M/M2/cards.json: M2-c161 (changed); M2-c152, c162, c163 (changed, PASS); other L11 cards byte-identical",
    "L11.html Example 2.3 (line 'Under Assumption 2.1 of Lesson 6, Theorem 2.1 applies to them. Then int x = [x^2] - int x'): the identity that results from dropping the boundary term is Theorem 2.1 applied under Assumption 2.1. Card M2-c161 back, first sentence 'It gives the integral of x from 0 to 1 equal to minus itself, which forces that integral to be 0.' carries no Assumption 2.1 qualifier; the qualifier appears only later, before 'the integral is 1/2'. The base FAIL (no qualifier) is therefore only partly fixed. c152 (qualifier at the start of its answer), c162 and c163 PASS. Base row claim 'M2-c160 removed' is not a delta fact: M2-c160 is absent at both pins.", "Edit M2-c161 back so the first clause carries the qualifier, e.g. 'Under Assumption 2.1 of Lesson 6, it gives the integral of x from 0 to 1 equal to minus itself, which forces that integral to be 0. The integral is 1/2, so the boundary term 1 is needed. The boundary term is not always zero: it vanishes in Example 2.2 because v(1) = 0 and u(0) = 0 (Misconception 1).' Then rerun tools/check_pages.py --unit M2.")
fresh["CARD-L12"] = ("PASS", "course/modules/M/M2/cards.json: changed M2-c169, c177, c178, c180; M2-c176 byte-identical at both pins; other 13 L12 cards byte-identical",
    "Re-verified against L12.html: c169 now reads 'from Theorem 2.2 under Assumption 2.1 of Lesson 6' (Example 2.3 text: By Theorem 2.2 (under Assumption 2.1), p=2 gives 1, p=3 gives 1/2; recomputed 1/(p-1)); c177 qualifier + Misconception 1 (error exactly 1/b, recomputed b^(1-p)/(p-1) at p=2); c178 = Misconception 3 and Remark 3.4 (p=1 diverges, p>=2 converges under Assumption 2.1, nothing for 0<p<1); c180 = Section 4 text (exponents p<=0 not treated; non-integer powers not established). c176 is identical at 95f3f8cb and 2a805c83 (base row listed it as changed; corrected here).")
fresh["CARD-DUP"] = ("PASS", "course/modules/M/M2/cards.json (all 395 cards at 2a805c83)",
    "cards_checks_r1.py: 0 duplicate ids; normalized duplicate fronts across all cards: only the pair M2-c342/M2-c343 (L23, P'(y0) vs P''(y0) collapsed by normalization; not a duplicate, out of slice). Card count 398 -> 395 (r1_delta.out).")
fresh["XREF-L07-L12"] = ("PASS", "course/modules/M/M2/L07.html..L12.html; cards M2-c096, c102, c107, c111, c113, c114, c134, c143, c145-c147, c161-c163, c169, c177, c178, c180, c422, c423, c425",
    "Every card cross-reference resolves in its lesson: Misconception 1/2/3, Remark 1.3/1.4, Remark 3.2/3.3, Example 2.3/2.4, Problem L08-R3, Section 4, Lab 1 part B/C, Theorem 2.2 and Lesson 11 Lemma 1.1 (exists in L11.html Section 1). Removed ids referenced nowhere (grep over course, tools, tests, notation, references).")
fresh["DAG-L07-L12"] = ("PASS", "course/modules/M/M2/L07.html..L12.html; changed cards M2-c423 and M2-c425",
    "check_dag.py --unit M2 PASS (r1_check_dag.out). c423 names Lesson 10 Theorem 2.1 and c425 names Lesson 11 Lemma 1.1 as forward references for the non-monotone integrand; both are the same prose-only forward references already on L09.html (Misconception 2 and Remark 1.4). No new registered concept is introduced by a card.")
fresh["PROSE-PROCESS"] = ("PASS", "course/modules/M/M2/L07.html..L12.html; changed and added cards (28 changed ids)",
    "Regex scan of the front and back of every changed card (script cards_checks/scan in " + S + ") for process words (now, previous, earlier, changed, revised, corrected, verifier, builder, round, draft, we, I, my, our, fixed, stale): hits only 'changed' in the English front of M2-c162 ('leave the limits of integration unchanged') and index letters i / I of math. No process words in learner text.")
fresh["PROSE-BANNED"] = ("PASS", "course/modules/M/M2/L07.html..L12.html; changed and added cards",
    "Same scan for BUILDER_RULES 1.3-1.4 strings (TODO, TBD, lorem, ellipsis, for brevity, omitted, beyond the scope, left as an exercise, you can add, important to note, studies show, experts agree, well known, obviously, clearly, historically, roughly, about N): no hits.")
carry_rows = {
 "NOT-L09-R": "L09 Section 1 notation (carry)",
 "NOT-GLOBAL": "every symbol on the slice pages matches notation/notation.json (carry); the changed card text uses no notation.json symbol (T, Phi, gamma, R*, R_f, Q) with a new meaning (scan in r1_cards_checks.out)",
 "HOURS-L07-L12": "hours arithmetic: lesson data-hours and hub split (carry; index.html and pages byte-identical)",
 "GRADE-L07-L12": "data-grade spans on the slice pages match the claims (carry)",
 "STRUCT-L07": "structure of L07 (carry)", "NUM-L07": "numbers in prose match unrounded values (carry)", "MATH-L07": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L07": "L07 lab twin: page code equals twin, expected block equals output, twin isolated (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "STRUCT-L08": "structure of L08 (carry)", "NUM-L08": "numbers in prose match unrounded values (carry)", "MATH-L08": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L08": "L08 lab twin (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "STRUCT-L09": "structure of L09 (carry)", "NUM-L09": "numbers in prose match unrounded values (carry)", "MATH-L09": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L09": "L09 lab twin (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "STRUCT-L10": "structure of L10 (carry)", "NUM-L10": "numbers in prose match unrounded values (carry)", "MATH-L10": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L10": "L10 lab twin (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "STRUCT-L11": "structure of L11 (carry)", "NUM-L11": "numbers in prose match unrounded values (carry)", "MATH-L11": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L11": "L11 lab twin (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "STRUCT-L12": "structure of L12 (carry)", "NUM-L12": "numbers in prose match unrounded values (carry)", "MATH-L12": "proofs and statements graded T are proved with their hypotheses (carry)",
 "LAB-L12": "L12 lab twin (carry; run fresh in RUN-M2-CHECKS and TWIN-ISOLATED)",
 "LAB-L07-DOC": "L07 lab docstring and interpretation match the code (carry)",
 "LINK-L11-chain": "L11 Lemma and Theorem links resolve to the lessons they cite (carry)",
 "PROOF-L11-hyp": "L11 integration-by-parts hypotheses checked in the proof (carry)",
 "PROOF-L12-integrability": "L12 integrability hypotheses checked in the proof (carry)",
 "QUIZ-L07-L12": "quiz answers match the lesson text (carry)",
 "MUTANTS-NA": "mutant set: ledgers/M2/mutants/ byte-identical; ruling 37 no new mutants; lesson slice (carry)",
 "KR-L10": "L10 key-results row 5 cites the right source (carry)",
}

base = json.load(open("/Users/billyribeiro/.fanout/frags/F2-M2-b.round1.json"))
base_rows = {r["id"]: r for r in base["rows"]}
rows = []
for rid in base_ids:
    check = base_rows[rid]["check"]
    if rid in fresh:
        st, loc, ev = fresh[rid][0], fresh[rid][1], fresh[rid][2]
        row = {"id": rid, "check": check, "location": loc, "status": st, "evidence": ev}
        if st != "PASS":
            row["fix"] = fresh[rid][3]
    else:
        row = {"id": rid, "check": check, "location": base_rows[rid]["location"], "status": "PASS",
               "evidence": CARRY + carry_rows[rid]}
    rows.append(row)
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
frag = {
  "unit": "M2", "slice": "b", "round": 1,
  "verifier": "independent Haiku verifier, M2 slice b, closing delta (rulings 30, 37); fresh context, no builder context",
  "pin": PIN,
  "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (base fragment ~/.fanout/frags/F2-M2-b.round1.json, verdict FAIL, 52 rows); delta 95f3f8cb..2a805c83",
  "checkout": CK + " (detached at 2a805c83, .venv symlinked, vendor copied)",
  "scratch": CK + "/" + S,
  "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
  "verdict": verdict,
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Delta (ruling 30): git diff 95f3f8cb..2a805c83 over the slice paths changes only course/modules/M/M2/cards.json for M2. Pages L07-L12, index.html, the six twins, notation/, references/, tools/, tests/labs/M2/ and ledgers/M2/mutants/ are byte-identical. Out-of-slice changes (not graded): tests/labs/E4/lab-E4-L04-1.py, tests/labs/M3/lab-M3-L09-1.py, tests/test_lx1_project_lab3.py.",
    "Re-verified from scratch: every base non-PASS row (CARD-L11, CARD-L12) and every row whose subject changed (CARD-L07..L10, CARD-DUP, XREF, DAG, PROSE, DELTA-HUNKS, gates). Carried rows cite only byte-identical subjects.",
    "Corrections to the base fragment's delta notes (not findings): M2-c160 does not exist at either pin (no removal in this delta); M2-c176 is byte-identical at both pins (not changed); M2-c421 is byte-identical (not changed); M2-c129 is absent at both pins; M2-c417, c428, c429 are removed at 2a805c83 (base said c417 changed, c428 added, c429 added).",
    "Observation (ruling-26 non-FAIL kind): M2-c161 first clause is the only remaining unqualified T-graded claim; c152 keeps the qualifier at the start of its answer. M2-c169 qualifies its source ('from Theorem 2.2 under Assumption 2.1') in the answer; accepted.",
    "Observation: at 2a805c83 the cards grade M2-c422 as T on the strength of Proposition 2.3 with Lab 1 part B as a check; the lab is exact-fraction, so the lab citation is a check and not the source of the result.",
    "Out-of-slice changed ids (M2-a or other owners, not graded here): c064 (L06), c265 (L18), c430 (L24), plus the L01/L04/L06/L13-L24 changes listed in r1_delta.out.",
  ],
  "summary": None,
}
frag["summary"] = (f"M2-b closing delta round 1 (pin 2a805c83, previous 95f3f8cb): {len(rows)} rows; PASS {counts['PASS']}, FAIL {counts['FAIL']}. "
  "FAIL: CARD-L11 (M2-c161 first clause lacks the Assumption 2.1 qualifier). The gate rows, the other card rows (including CARD-L12, now PASS) and all carried rows PASS.")
json.dump(frag, open(CK + "/ledgers/M2/M2-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(CK + "/" + S + "/fragment_written.txt", "w").write(str(counts) + " " + verdict + "\n")
print(counts, verdict)
