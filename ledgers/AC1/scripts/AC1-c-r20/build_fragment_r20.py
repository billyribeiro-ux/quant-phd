"""Round 20 (AC1-c): build ledgers/AC1/AC1-c.json from the round-19 fragment and this round's re-runs.

Carry rule: a previous PASS row is carried only when its cited subject is byte-identical since the previous pin
51fa336 (the only changed lines in L07.html and L08.html are :51 and :55). Command rows and rows whose subject
changed (or is a whole page) are re-run or re-verified and carry round-20 evidence.
"""

import json
import re
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
PREV = json.loads(Path("/tmp/fanout-frags/AC1-c.round19.json").read_text(encoding="utf-8"))
CARRY = (
    "Carried from round 19 (course/modules/AC/AC1/L07.html and L08.html: the cited lines are byte-identical since the "
    "previous pin 51fa336, and the only changed lines in those two files are :51 and :55; cards.json, index.html and "
    "tests/labs/AC1/lab-AC1-L07-1.py, lab-AC1-L08-1.py are byte-identical): "
)
RERUN = "Re-run in round 20 (checkout fd9a9b7): "
REVERIFIED = "Re-verified in round 20 against the changed text (fd9a9b7): "

# Rows whose subject changed in fd9a9b7 or that cite whole pages: re-verified with new evidence below.
REVERIFY = {
    "AC1-c-r5-L07-line51-why": "L07.html:51 now reads 'an award the employee loses before the required service is complete' "
    "(gloss of Definition 1.2 (ii) at L07.html:73, 'lost by the employee before it vests'). 'Vests' is defined at "
    "L07.html:55 as the period in which the employee must remain in service; the gloss states the same condition. "
    "'Required service' is ordinary usage, as in 'years of required service' earlier in the same paragraph. No number.",
    "AC1-c-r18-L07-why-it-matters": "L07.html:51 (the forfeiture gloss, changed in fd9a9b7) is re-read above: the gloss "
    "equals Definition 1.2 (ii) and Section 1's vesting definition at L07.html:55. Status PASS.",
    "AC1-c-r5-L08-line51-signed": "L08.html:51 changed in fd9a9b7. The current text attributes the exactness of the "
    "deferred expense and balance to Definition 1.1 (depreciation multiples of 100 cents) and the sum in Definition 1.2 "
    "(L08.html:59, :64). Recomputed: recheck_l08_r20.out, 7,373 cases, 0 violations for DE and DTL integrality; "
    "CT and TE integrality iff r*P_t is a multiple of 100, and P_t a multiple of 100 is sufficient, as L08.html:88 states. "
    "No sign claim remains in L08.html:51.",
    "AC1-c-r18-L08-why-it-matters": "L08.html:51 (changed in fd9a9b7) re-verified: P_t condition only on CT and TE "
    "(L08.html:88, Theorem 2.1 (b) at :92); DE and DTL exact for every P_t (recheck_l08_r20.out). Status PASS.",
    "AC1-c-r19-L08-line51-cumulative-basis": "FAIL in round 19 (Definition 1.1 cited for the cumulative difference). "
    "fd9a9b7 rewrote L08.html:51 to read 'Definition 1.1 makes the depreciation amounts multiples of 100 cents, and the "
    "cumulative difference of Definition 1.2 is a sum of them'. Definition 1.1 (L08.html:59) constrains C, b_t and tau_t, "
    "which are multiples of 100 cents (C a multiple of 10,000; C/L and p_t*C/100 multiples of 100); K_t is the sum of "
    "tau_s - b_s (Definition 1.2, L08.html:64), so it is a sum of multiples of 100. The attribution now matches. "
    "DTL_t = rK_t/100 is an integer for every whole-number rate and every P_t (recheck_l08_r20.out: 0 violations). PASS.",
    "AC1-c-r9-delta-read": "L08.html:51 re-read in round 20 (see AC1-c-r19-L08-line51-cumulative-basis). The "
    "round-9 defect (P_t condition as the basis of the deferred balance) is absent from the current text. PASS.",
    "AC1-c-r5-L08-line55-zero": "L08.html:55 changed in fd9a9b7 (sentence now: 'in this model it is zero at the end of "
    "the asset's life (the proof of Theorem 2.1 (c) gives this)'). Re-verified: Theorem 1.3 gives carrying amount minus "
    "tax base = K_t (L08.html:68-69); K_L = 0 by the proof of Theorem 2.1 (c) (L08.html:95, sum of tau_s = C = L*b). "
    "Units sentence now reads 'integer cents of SCU'; Definition 1.1 (L08.html:59) makes C, b_t, tau_t whole cents. PASS.",
    "AC1-c-banned-phrases": "Whole-page scan of L07.html and L08.html in fd9a9b7 (grep -i for roughly, about N%, "
    "historically, typically, usually, generally, '...', the ellipsis character, builder, build, round, verifier, "
    "REQUEST): no match in either page; the cards are unchanged. PASS.",
    "AC1-c-scope-words": "Scope words in the changed text: L07.html:51 and :55 (no only/all/always); L08.html:51 "
    "('because', 'every P_t', checked above); L08.html:55 ('same', checked above); 'Three terms are used in this section "
    "and the next' (L07.html:55) is a collective claim: 'vesting' used at L07.html:59 and :68 (Section 1), grant-date fair "
    "value at L07.html:59 (Section 1), APIC at L07.html:96 (Section 2). PASS.",
    "AC1-c-notation": "notation/notation.json and notation/ are byte-identical since 51fa336 (git diff --stat). The "
    "changed sentences introduce no new symbol: they use SCU, P_t, K_t, C, b_t, tau_t, r already on the page. PASS.",
    "AC1-c-figures-none": "L07.html and L08.html changed only in two paragraph texts (lines 51 and 55 each); no figure, "
    "canvas or chart element was added (git diff -U0 shows only those hunks). PASS.",
    "AC1-c-lesson-structure": "check_pages AC1 PASS (round 20 re-run); the diff touches only paragraph text at L07.html:51, "
    ":55 and L08.html:51, :55; section order and headings unchanged. PASS.",
}

RERUN_ROWS = {
    "AC1-c-cmd-run_labs": "tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)'.",
    "AC1-c-r19-cmd-run_labs": "tools/run_labs.py --unit AC1: 'run_labs AC1: PASS (11/11)'.",
    "AC1-c-cmd-check_pages_dag": "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS'; tools/check_dag.py --unit AC1: 'check_dag AC1: PASS'.",
    "AC1-c-r19-cmd-check_pages_dag": "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS'; tools/check_dag.py --unit AC1: 'check_dag AC1: PASS'.",
    "AC1-c-lab-twin-run": "python -I -W error tests/labs/AC1/lab-AC1-L07-1.py exit 0; lab-AC1-L08-1.py exit 0 (outputs in /tmp/AC1-v/AC1-c-r20/).",
    "AC1-c-r19-lab-twins-isolated": "python -I -W error on both twins: exit 0 and 0 (round 20).",
    "AC1-c-lab-embed-equals-twin": "Embedded data-run blocks equal the twin files byte-for-byte after HTML unescape: L07.html:127-249 == lab-AC1-L07-1.py; L08.html:108-195 == lab-AC1-L08-1.py (True, True).",
    "AC1-c-r19-lab-embed-equals-twin-and-expected": "Embedded code equals twins (True, True) and the expected blocks equal the isolated run output (True, True) for L07.html and L08.html.",
    "AC1-c-lab-expected-output": "The data-tolerance expected blocks (L07.html:250-267; L08.html:196-208) equal the isolated run output exactly (True, True).",
    "AC1-c-r9-embed-expected": "Embed and expected checks re-run: both True (see AC1-c-lab-embed-equals-twin).",
    "AC1-c-lab-seed-sweep": "ledgers/AC1/scripts/AC1-c-r20/seed_sweep_r20.py: L07 and L08 each run for 45 seeds (0 to 40, 999, 123456789, 20260702, 20260701): failing seeds [] for both (seed_sweep_r20.out).",
    "AC1-c-r18-seed-sweep": "seed_sweep_r20.py: 45 seeds per lab, failing seeds [] for L07 and L08.",
    "AC1-c-r19-seed-sweep": "seed_sweep_r20.py: 45 seeds per lab, failing seeds [] for L07 and L08.",
    "AC1-c-cmd-page_smoke": "tools/page_smoke.py --unit AC1 --pages L07 L08: 'page_smoke modules/AC/AC1/L07.html: PASS', 'page_smoke modules/AC/AC1/L08.html: PASS', 'page_smoke AC1: PASS'.",
    "AC1-c-r19-page_smoke": "tools/page_smoke.py --unit AC1 --pages L07 L08: 'page_smoke AC1: PASS' (both pages).",
    "AC1-c-cit-verify_refs": "tools/verify_refs.py --unit AC1: 'live re-verification of AC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'.",
    "AC1-c-r19-verify_refs": "tools/verify_refs.py --unit AC1 (live): 2 of 560 entries, 0 problems; --offline: 560 entries, 0 problems.",
    "AC1-c-cmd-pytest_ruff_mypy": "pytest tests/test_labs.py -q: exit 0, 127 passing dots, no failures; mypy (strict, project config): 'Success: no issues found in 153 source files', exit 0; ruff check .: 'All checks passed!', exit 0; ruff format --check tests/labs/AC1: exit 0.",
    "AC1-c-r19-tooling-carried": "git diff --stat 51fa336 fd9a9b7 -- tools tests/test_*.py references notation: no output (no change); the only changed test file in the range is tests/labs/AC1/lab-AC1-L04-1.py, outside this slice, and pytest tests/test_labs.py passes with it.",
    "AC1-c-r18-twins-unchanged": "git diff 51fa336 fd9a9b7 -- tests/labs/AC1/lab-AC1-L07-1.py lab-AC1-L08-1.py: empty (byte-identical).",
    "AC1-c-r7-lab-student-mutants": "ledgers/AC1/scripts/AC1-c-r20/mutants_rerun_r20.out: the archived r7 student-error cases (m7a, m7b, m8a) re-run: FAIL (exit 1) as expected.",
    "AC1-c-r8-lab-student-mutants": "mutants_rerun_r20.out: r8 cases re-run; outcomes identical to round 19 (diff of exit codes empty).",
    "AC1-c-r9-new-mutants": "mutants_rerun_r20.out: m9a-m9g re-run, all FAIL (exit 1), as expected.",
    "AC1-c-r9-alt-implementations-seeds": "mutants_rerun_r20.out: alt9a-alt9c exit 0; seed sweep (seed_sweep_r20.out) no failing seed.",
    "AC1-c-r7-alt-implementations": "mutants_rerun_r20.out: alternatives alt9a-c, alt10a-b, alt17a, alt18a-c all exit 0.",
    "AC1-c-r10-mutants-killed": "mutants_rerun_r20.out: m10b, m10d, m10e exit 1 (FAIL) as expected.",
    "AC1-c-r10-m10a-survivor": "mutants_rerun_r20.out: m10a exit 0 (survives). Lab twin, no lesson sentence claims the lab checks the start year of the expense; out of scope (architect ruling).",
    "AC1-c-r10-m10c-survivor": "mutants_rerun_r20.out: m10c exit 0 (survives). Lab twin; the schedule sums still equal the totals and no lesson sentence claims a check of the divisor; out of scope (architect ruling).",
    "AC1-c-r10-alt-correct-implementations": "mutants_rerun_r20.out: alt9a-c, alt10a-b exit 0 (correct alternatives pass).",
    "AC1-c-r17-mutants-killed": "mutants_rerun_r20.out: m17b-m17e exit 1 (FAIL) as expected; alt17a exit 0.",
    "AC1-c-r17-m17a-survivor": "mutants_rerun_r20.out: m17a exit 0 (survives on the shipped seed); out of scope (architect ruling; L07.html:133 says the lab checks only the schedule sums and identities).",
    "AC1-c-r18-m18a-survivor-check": "mutants_rerun_r20.out: m18a exit 0 on the shipped seed; killed under other seeds (seed-dependent); out of scope under the architect ruling.",
    "AC1-c-r18-m18c-sbc-omits-last-grant": "mutants_rerun_r20.out: m18c exit 0 (survives; the schedule-sum check is unaffected); out of scope under the architect ruling.",
    "AC1-c-r18-m18d-tax-depreciation-shifted": "mutants_rerun_r20.out: m18d exit 0 (survives); L08.html:103 claims only (a), (b) and the year-5 balance; out of scope under the architect ruling.",
    "AC1-c-r18-m18g-base-from-share-count": "mutants_rerun_r20.out: m18g exit 0 (survives); lab checks are the schedule sums and identities; out of scope under the architect ruling.",
    "AC1-c-r18-alt-implementations": "mutants_rerun_r20.out: alt18a, alt18b, alt18c exit 0.",
    "AC1-c-r19-mutants-rerun": "ledgers/AC1/scripts/AC1-c-r20/mutants_r20_rerun.py run on fd9a9b7: 41 cases, outcomes identical to the round-19 output (mutants_rerun_r19.out) in every case.",
    "AC1-c-r19-new-student-mutants": "mutants_r20_new_rerun: ledgers/AC1/scripts/AC1-c-r20/mutants_r19_new_r20.out: m19a, m19b, m19c exit 1 (FAIL) as expected; m19d exit 0 (survives), out of scope under the architect ruling (identical to round 19).",
    "AC1-c-r19-survivor-classification": "mutants_rerun_r20.out and mutants_r19_new_r20.out: survivors are m10a, m10c, m17a, m18a, m18c, m18d, m18g, m19d (all exit 0); classification unchanged.",
}

ALL_ROW_IDS_RERUN_OR_REVERIFY = set(REVERIFY) | set(RERUN_ROWS)

NEW_ROWS = [
    {
        "id": "AC1-c-r20-delta-read",
        "check": "1-delta round-19 pin 51fa336 to round-20 pin fd9a9b7 (slice paths)",
        "location": "git diff -U0 51fa336 fd9a9b7 -- course/modules/AC/AC1/L07.html course/modules/AC/AC1/L08.html",
        "status": "PASS",
        "evidence": "git diff --stat 51fa336 fd9a9b7 -- course/modules/AC/AC1 tests/labs/AC1: L04.html, L05.html, L06.html, project.html, grader/test_project.py and tests/labs/AC1/lab-AC1-L04-1.py changed (outside this slice); L07.html and L08.html changed in two hunks each (@@ -51 +51 @@ and @@ -55 +55 @@); lab twins L07 and L08, cards.json, index.html, references/, notation/, tools/ unchanged.",
    },
    {
        "id": "AC1-c-r20-L07-line51-gloss",
        "check": "2.2-why-it-matters gloss L07 (forfeiture) changed in fd9a9b7",
        "location": "course/modules/AC/AC1/L07.html:51; :55 (vesting); :73 (Definition 1.2 (ii))",
        "status": "PASS",
        "evidence": "New gloss 'no forfeitures (an award the employee loses before the required service is complete)' versus Definition 1.2 (ii) 'lost by the employee before it vests' (L07.html:73) and the vesting sentence at L07.html:55 ('the period in which the employee must remain in service before the award is theirs'): the same condition. The gloss uses no number and no causal claim.",
    },
    {
        "id": "AC1-c-r20-L07-line55-terms",
        "check": "2.9-scope words: 'Three terms are used in this section and the next' (L07 Section 1 intro)",
        "location": "course/modules/AC/AC1/L07.html:55; :59, :68 (vesting, grant-date fair value); :96 (APIC in Section 2)",
        "status": "PASS",
        "evidence": "grep: 'vest' appears at L07.html:59 and :68 (Section 1), 'grant-date fair value' at :59 (Section 1), 'APIC' at :96 (Section 2 display). Each of the three terms appears in Section 1 or Section 2, so the collective sentence is true. The sentence does not say each term appears in both sections, and none of the three is used as a claim beyond its definition at :55.",
    },
    {
        "id": "AC1-c-r20-L07-line55-units",
        "check": "2.4-units: 'integer cents of SCU ... worked examples write them with a dollar sign' (L07 Section 1)",
        "location": "course/modules/AC/AC1/L07.html:55; :59 (f_g in integer cents); :86, :119 (Example 1.4, 2.3 dollar amounts); :293, :303 (M1, M3)",
        "status": "PASS",
        "evidence": "Definition 1.1 (L07.html:59) states f_g in integer cents; Example 1.4 (:86) writes '$12.00 ... that is 1,200 cents', '$12,000', '$3,000'; Example 2.3 (:119) and M1, M3 (:295, :303) use dollar signs, all read as SCU per the sentence at :55 and the lab's SCU printing (tests/labs/AC1/lab-AC1-L07-1.py cents_text).",
    },
    {
        "id": "AC1-c-r20-L08-line51-multiples",
        "check": "2.4-math basis: L08 why-it-matters 'exact for every P_t, because Definition 1.1 makes the depreciation amounts multiples of 100 cents, and the cumulative difference of Definition 1.2 is a sum of them'",
        "location": "course/modules/AC/AC1/L08.html:51; :59 (Definition 1.1); :64 (Definition 1.2); :85 (DE_t, DTL_t); :88 (Section 2 exactness sentence)",
        "status": "PASS",
        "evidence": "Definition 1.1: C a multiple of 10,000 cents, C/L a multiple of 100 cents, tau_t = C p_t/100 with integer p_t summing to 100, so tau_t is a multiple of 100 (C multiple of 10,000). Definition 1.2: K_t = sum of (tau_s - b_s), a sum of multiples of 100. DTL_t = r K_t/100 and DE_t = r(tau_t - b_t)/100 are whole cents for every whole-number r and every P_t, since neither involves P_t. recheck_l08_r20.out (fresh script, 7,373 cases): 0 violations for DE and DTL integrality. The basis sentence is correct as written.",
    },
    {
        "id": "AC1-c-r20-L08-line51-current-tax",
        "check": "2.4-math: 'current tax and total tax expense are exact in integer cents when P_t is a multiple of 100 cents' (L08 why-it-matters)",
        "location": "course/modules/AC/AC1/L08.html:51; :88 (CT_t, TE_t integer condition, sufficiency for whole-number r); :92 (Theorem 2.1 (b))",
        "status": "PASS",
        "evidence": "L08.html:88 says CT and TE are integer cents iff r P_t is a multiple of 100 and that a P_t multiple of 100 is sufficient for every whole-number r. recheck_l08_r20.out: CT integral iff (r*P) % 100 == 0 (0 violations in 3,000 random cases); P=50,001, r=21 gives CT = 630,021/100 (not integer), and P a multiple of 100 gives integer CT for r=100. The why-it-matters sentence states the sufficient condition, which is what :88 states; it does not claim necessity.",
    },
    {
        "id": "AC1-c-r20-L08-line55-units-and-zero",
        "check": "2.2-section 1 L08 (changed units sentence and zero temporary difference at end of life)",
        "location": "course/modules/AC/AC1/L08.html:55; :59 (Definition 1.1); :68-69 (Theorem 1.3); :92, :95 (Theorem 2.1 (c) proof)",
        "status": "PASS",
        "evidence": "'Amounts are in integer cents of SCU ... The worked examples write the same amounts with a dollar sign, which here means SCU': Example 1.4 (L08.html:77, '$100,000') and Example 2.2 (:100, '$50,000') use dollar signs. 'Definition 1.1 makes C, b_t and tau_t whole numbers of cents' is supported by :59 (C multiple of 10,000; C/L and p_t C/100 multiples of 100). 'Zero at the end of the asset's life' follows from Theorem 1.3 (carrying minus tax base = K_t) and K_L = 0 (Theorem 2.1 (c), proof at :95).",
    },
    {
        "id": "AC1-c-r20-new-mutant-m20a",
        "check": "2.5-labs student-error mutant m20a: L08 tax percentage index wraps (rotated tax schedule)",
        "location": "tests/labs/AC1/lab-AC1-L08-1.py (tax_dep line); course/modules/AC/AC1/L08.html:103, :209",
        "status": "PASS",
        "evidence": "mutants_new_r20.out: m20a exit 0 (survives on the shipped seed); mutant_seed_sweep_r20.out: 0 failing seeds of 45. The rotated percentages still sum to 100 and the totals and identities still hold, so the lab's checks (book and tax totals, Theorem 2.1 (a), (b), the year-5 balance) cannot see the timing. L08.html:103 claims only (a), (b) and the year-5 balance. Out of scope under the architect ruling on lab twins.",
    },
    {
        "id": "AC1-c-r20-new-mutant-m20b",
        "check": "2.5-labs equivalent mutant m20b: balance floored at zero (max(cumulative, 0))",
        "location": "tests/labs/AC1/lab-AC1-L08-1.py (dtl line); course/modules/AC/AC1/L08.html:64 (negative balance remark)",
        "status": "PASS",
        "evidence": "mutants_new_r20.out: m20b exit 0. Equivalent for every seed: with TAX_PERCENT (40, 30, 20, 10, 0) and cost a multiple of 10,000 cents, the cumulative tax shares 40, 70, 90, 100, 100 are at least the book shares 20, 40, 60, 80, 100, so K_t = cost*(cumulative tax share - cumulative book share)/100 >= 0 in every year and the floor never changes a value. The lesson's negative-balance remark (L08.html:64) is about the definition, not a lab check.",
    },
    {
        "id": "AC1-c-r20-new-mutant-m20c",
        "check": "2.5-labs student-error mutant m20c: expense index shifted one year (L07 schedule)",
        "location": "tests/labs/AC1/lab-AC1-L07-1.py (index line); course/modules/AC/AC1/L07.html:133 (lab checks), :327 (E2 'pass for any seed'), :331 (E3)",
        "status": "PASS",
        "evidence": "mutants_new_r20.out: m20c exit 0 on the shipped seed; mutant_seed_sweep_r20.out: 21 of 45 seeds fail (seeds 2, 3, 5, 6, 10, ...), so the check has teeth on other seeds. The shipped-seed survivor is a timing error the lab's stated checks do not test (L07 lab docstring lines 131-133: checks are schedule sums and Section 2 identities). Out of scope under the architect ruling; the correct code passes all 45 seeds, consistent with E2.",
    },
    {
        "id": "AC1-c-r20-alt-implementations",
        "check": "2.5-labs over-constraint: correct alternative implementations (round 20)",
        "location": "tests/labs/AC1/lab-AC1-L08-1.py (current line); tests/labs/AC1/lab-AC1-L07-1.py (yearly_expense)",
        "status": "PASS",
        "evidence": "mutants_new_r20.out: alt20a (current tax from P_t minus the difference, algebraically identical) exit 0; alt20b (expense by cumulative rounding of cost shares, no remainder branch) exit 0; mutants_rerun_r20.out: alt18a-c, alt17a, alt9a-c, alt10a-b exit 0.",
    },
    {
        "id": "AC1-c-r20-mutants-rerun",
        "check": "2.5-labs all archived lab mutants re-run on fd9a9b7",
        "location": "ledgers/AC1/scripts/AC1-c-r20/mutants_r20_rerun.py; mutants_rerun_r20.out",
        "status": "PASS",
        "evidence": "41 cases re-run with python -I -W error. Every case's exit status equals the round-19 output (diff of the outcome column empty). Survivors remain m10a, m10c, m17a, m18a, m18c, m18d, m18g, m19d, each out of scope under the architect ruling on lab twins.",
    },
]

rows = []
seen = set()
for row in PREV["rows"]:
    rid = row["id"]
    seen.add(rid)
    if rid == "AC1-c-r19-L08-line51-cumulative-basis" or rid in REVERIFY:
        new = dict(row)
        new["status"] = "PASS"
        new["evidence"] = REVERIFIED + REVERIFY[rid]
        rows.append(new)
    elif rid in RERUN_ROWS:
        new = dict(row)
        new["status"] = "PASS"
        new["evidence"] = RERUN + RERUN_ROWS[rid]
        rows.append(new)
    elif row["status"] == "PASS":
        new = dict(row)
        new["evidence"] = CARRY + row["evidence"]
        rows.append(new)
    else:
        raise SystemExit(f"unexpected non-PASS previous row {rid}")

rows.extend(NEW_ROWS)
# Every previous PASS/FAIL id is kept; the round-19 FAIL row is re-verified and now PASS.
assert {r["id"] for r in PREV["rows"]} <= {r["id"] for r in rows}

mutants = []
for m in PREV["mutants"]:
    mutants.append({"id": m["id"], "description": m["description"],
                    "killed_by": m["killed_by"] + " (round 20 re-run: identical outcome)"})
mutants += [
    {"id": "r20-m20a", "description": "L08 tax percentage index wraps, rotating the tax schedule",
     "killed_by": "SURVIVES on all 45 seeds; out of scope (lab twin, architect ruling; no lesson sentence claims a check of tax timing)"},
    {"id": "r20-m20b", "description": "L08 deferred balance floored at zero (max(cumulative, 0))",
     "killed_by": "SURVIVES; EQUIVALENT for every seed (cumulative tax shares >= book shares, so K_t >= 0; proof in AC1-c-r20-new-mutant-m20b)"},
    {"id": "r20-m20c", "description": "L07 expense index shifted one year (year - grant_year - 1)",
     "killed_by": "AssertionError on 21 of 45 seeds (mutant_seed_sweep_r20.out); SURVIVES on the shipped seed; out of scope (lab twin, architect ruling)"},
]

frag = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 20,
    "round_note": "round 20 (independent re-verification of AC1-c after pin 51fa336). Delta: L07.html:51 and :55 and L08.html:51 and :55 rewritten (fd9a9b7). L04, L05, L06, project and grader files are outside this slice. Previous FAIL AC1-c-r19-L08-line51-cumulative-basis is re-verified and now PASS.",
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 20; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "fd9a9b7",
    "base": "51fa336 (previous pin, for the delta); round-19 fragment /tmp/fanout-frags/AC1-c.round19.json",
    "checkout": "/tmp/verify20-AC1-c",
    "scratch": "/tmp/AC1-v/AC1-c-r20",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r20/mutants_r20_rerun.py",
        "ledgers/AC1/scripts/AC1-c-r20/mutants_rerun_r20.out",
        "ledgers/AC1/scripts/AC1-c-r20/mutants_r20_new.py",
        "ledgers/AC1/scripts/AC1-c-r20/mutants_new_r20.out",
        "ledgers/AC1/scripts/AC1-c-r20/mutant_seed_sweep_r20.py",
        "ledgers/AC1/scripts/AC1-c-r20/mutant_seed_sweep_r20.out",
        "ledgers/AC1/scripts/AC1-c-r20/seed_sweep_r20.py",
        "ledgers/AC1/scripts/AC1-c-r20/seed_sweep_r20.out",
        "ledgers/AC1/scripts/AC1-c-r20/recheck_l08_r20.py",
        "ledgers/AC1/scripts/AC1-c-r20/recheck_l08_r20.out",
        "ledgers/AC1/scripts/AC1-c-r20/build_fragment_r20.py",
    ],
    "notes": "Not checked: project and grader files (other slices); the hours design targets (architect ruling: arithmetic only; index.html unchanged since 51fa336 (carried hub rows)); live web sources beyond verify_refs (no network fetch of the references beyond the tool).",
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = f"PASS: {n_pass} of {len(rows)} rows. Mutants: {len(mutants)} listed (archived and new); lab survivors out of scope under the architect ruling; m20b equivalent."
out = CHECKOUT / "ledgers/AC1/AC1-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "mutants", len(mutants))
