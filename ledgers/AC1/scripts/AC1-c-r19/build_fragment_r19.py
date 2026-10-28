"""Round 19 (AC1-c) fragment builder: carries round-18 rows by the carry rule, re-verifies the rows whose
cited subject changed (L08.html lines 51 and 88), reclassifies lab-twin survivors under the architect
ruling, and appends the round-19 rows. Usage: python -I build_fragment_r19.py <checkout>"""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC1-c.round18.json").read_text(encoding="utf-8"))

CARRY_L = (
    "Carried from round 18 (course/modules/AC/AC1/L07.html, tests/labs/AC1/lab-AC1-L07-1.py and "
    "tests/labs/AC1/lab-AC1-L08-1.py byte-identical since the previous pin 7143726; L08.html changed only at "
    "lines 51 and 88, and the cited L08 lines are unchanged; cards.json entries cited are unchanged):"
)
CARRY_CARDS = (
    "Carried from round 18 (cards.json entries c091-c139 byte-identical since the previous pin 7143726; the file "
    "changed only at L04/L05 entries and by appending c140):"
)
CARRY_PLAIN = "Carried from round 18 (files cited byte-identical since the previous pin 7143726):"

REVERIFIED = {
    "AC1-c-r5-L08-line51-signed": (
        "Re-verified in round 19 against the CURRENT L08.html:51 (changed again in 51fa336). The sentence now "
        "makes the current tax and total tax expense exact when P_t is a multiple of 100 cents, and the deferred "
        "expense and deferred balance exact for every P_t. Recomputed with integer arithmetic (ledgers/AC1/scripts/"
        "AC1-c-r19/recheck_l08.py, output recheck_l08_r19.out): 7,373 year cases over 3,000 random Definition 1.1 "
        "assets, DE_t and DTL_t integral in every case; the round-5 defect (the P_t condition as the basis of the "
        "balance) is removed. The one remaining basis word is the subject of AC1-c-r19-L08-line51-cumulative-basis."
    ),
    "AC1-c-r9-delta-read": (
        "Re-read in round 19: L07.html:59, :73, :339, :341 and cards c102, c109 are unchanged since 7143726 "
        "(git diff --stat shows no L07 change; cards entries compared programmatically). L08.html:51 was changed "
        "in 7143726 and again in 51fa336; the round-9 defect (P_t condition as the basis of the deferred balance) "
        "is removed by the current text. Residual attribution: AC1-c-r19-L08-line51-cumulative-basis."
    ),
    "AC1-c-r18-L08-why-it-matters": (
        "Fix applied in 51fa336. L08.html:51 now places the P_t condition only on the current tax and the total tax "
        "expense, and states the deferred expense and balance exact for every P_t (the round-18 defect). Section 2 "
        "(L08.html:88) makes the same split. Re-verified: CT_t = r(P_t - d_t)/100 and TE_t = rP_t/100 "
        "(Theorem 2.1 (b)) give integer cents iff rP_t is a multiple of 100 (d_t is a multiple of 100); DE_t = r d_t/100 "
        "and DTL_t = rK_t/100 are integral for every P_t (recheck_l08_r19.out: 7,373 cases, 0 violations). Residual "
        "attribution of K_t to Definition 1.1: AC1-c-r19-L08-line51-cumulative-basis."
    ),
    "AC1-c-r17-m17a-survivor": (
        "Reclassified in round 19 under the ARCHITECT RULING on lab mutants (lab twins are demonstrations; mutation "
        "testing applies to project graders only). mutants_r19_rerun.out: m17a exits 0 and the twin output is "
        "unchanged in the lab's checks. The lesson claims the lab checks the schedule sums and the Section 2 "
        "identities (course/modules/AC/AC1/L07.html:133); m17a keeps both true (the shifted SBC row still sums each "
        "grant and keeps the identities). The printed-table sentences at L07.html:268 and :358 describe the verbatim "
        "output of the real run, not a property the lab asserts. Out of scope, PASS."
    ),
    "AC1-c-r18-m18c-sbc-omits-last-grant": (
        "Reclassified in round 19 under the ARCHITECT RULING (lab twins are demonstrations; mutation testing applies "
        "to project graders only). mutants_r18.py re-run: m18c exits 0. The lesson claims the lab checks the schedule "
        "sums and the Section 2 identities (L07.html:133); the mutant drops one grant from the statement sum, which "
        "keeps every per-grant schedule sum and every identity true. No lesson sentence claims the lab asserts the "
        "SBC total against an independent schedule. Out of scope, PASS."
    ),
    "AC1-c-r18-m18d-tax-depreciation-shifted": (
        "Reclassified in round 19 under the ARCHITECT RULING (lab twins are demonstrations). m18d exits 0 (re-run). "
        "The lesson states what the lab checks (L08.html:103: Theorem 2.1 (a), (b) every year and the year-5 "
        "balance; not (d)); the mutant keeps those checks true, and no sentence claims the lab asserts the printed "
        "tax-depreciation column. The page's table statements (L08.html:262-265, :300) are about the verbatim real "
        "run output, which is unchanged. Out of scope, PASS."
    ),
    "AC1-c-r18-m18g-base-from-share-count": (
        "Reclassified in round 19 under the ARCHITECT RULING (lab twins are demonstrations). m18g exits 0 (re-run). "
        "The lab's stated checks (L07.html:133, schedule sums and Section 2 identities) still hold for the mutated "
        "base; no lesson sentence claims the lab asserts the base formula of Definition 1.1 (L07.html:63). Out of "
        "scope, PASS."
    ),
    "AC1-c-L08-sec2-integer-cents": (
        "Re-verified in round 19 against the changed L08.html:88 (the P_t condition now applies to CT_t and TE_t only, "
        "L08.html:88): the Definition 1.1 constraints (:58) give integer cents for tau_t, b_t and K_t; the recheck "
        "(recheck_l08_r19.out) confirms the iff and the sufficiency statements. PASS."
    ),
    "AC1-c-r4-L08-cash-convention": (
        "Re-verified in round 19: the cash convention sentence (L08.html:88, 'the cash tax paid in year t is CT_t, so "
        "deferred tax expense moves no cash') is unchanged in substance by 51fa336; :223 and :225 and :330 are "
        "byte-identical. PASS."
    ),
    "AC1-c-r17-card-c111": (
        "Re-verified in round 19: card c111 (cards.json:770-773) states DE_t = DTL_t - DTL_(t-1), with DTL_0 = 0; "
        "L08.html:85 and :88 still define DE_t and DTL_0 = 0 in the current text. PASS."
    ),
    "AC1-c-r17-card-c139": (
        "Re-verified in round 19: card c139 (cards.json:974-977) states TE_t = CT_t + DE_t; L08.html:86 defines it "
        "in the current text (unchanged). PASS."
    ),
}

ROWS = []
for row in prev["rows"]:
    rid = row["id"]
    if rid in REVERIFIED:
        ROWS.append({"id": rid, "check": row["check"], "location": row["location"], "status": "PASS",
                     "evidence": REVERIFIED[rid]})
        continue
    if row["status"] != "PASS":
        # remaining round-18 FAIL rows: the mutant ones were reclassified above; anything else stays FAIL
        ROWS.append({"id": rid, "check": row["check"], "location": row["location"], "status": "FAIL",
                     "evidence": row["evidence"], "fix": row.get("fix", "")})
        continue
    loc = row["location"]
    if "cards.json" in loc:
        prefix = CARRY_CARDS
    elif "L08.html" in loc:
        prefix = CARRY_L
    else:
        prefix = CARRY_PLAIN
    ROWS.append({"id": rid, "check": row["check"], "location": loc, "status": "PASS",
                 "evidence": prefix + " " + row["evidence"]})

NEW = [
    ("AC1-c-r19-delta-read", "1-delta round-18 pin 7143726 to round-19 pin 51fa336 (slice paths)",
     "git diff --stat 7143726 51fa336 -- course/modules/AC/AC1 tests/labs/AC1",
     "Seven files changed in the unit: L04.html, L05.html, L06.html, L08.html, cards.json, curriculum/01-foundations.yaml and curriculum/curriculum.json. In this slice only L08.html changed, at lines 51 and 88 (two hunks, both rewritten sentences; read in full). L07.html, lab-AC1-L07-1.py and lab-AC1-L08-1.py are byte-identical. cards.json: a programmatic comparison of the 139 round-18 entries shows changed ids c046, c052, c053, c058, c066 and c069 (all L04/L05) and one appended entry c140 (L04); no L07 or L08 card changed. The curriculum change adds M1 to the prerequisites of CS2 (not an AC1 prerequisite); check_dag PASS (below)."),
    ("AC1-c-r19-L08-line51-cumulative-basis", "2.4-math basis: L08 why-it-matters exactness claim (cumulative difference attribution)",
     "course/modules/AC/AC1/L08.html:51",
     "Sentence: 'The deferred expense and the deferred balance are exact for every P_t, because Definition 1.1 makes the depreciation amounts and the cumulative difference multiples of 100 cents.' The P_t-independence and the integer cents are correct (recheck_l08_r19.out: 0 violations in 7,373 cases). But Definition 1.1 (L08.html:58-59) constrains only C, b_t, tau_t and the rate; the cumulative difference K_t is defined in Definition 1.2 (L08.html:64) as a sum of tau_s - b_s. The multiple-of-100 property of K_t follows from Definition 1.1 plus that sum, and Definition 1.1 does not state it. The sentence attributes a property to a definition that does not contain it: a basis stated more exactly than the text supports (recurring defect class).",
     "Change the cause to: 'because Definition 1.1 makes the depreciation amounts multiples of 100 cents, and the cumulative difference of Definition 1.2 is a sum of them.' Make no other change; the claim is otherwise correct."),
    ("AC1-c-r19-L08-line88-condition", "2.4-math: L08 Section 2 integer-cent conditions (changed line 88)",
     "course/modules/AC/AC1/L08.html:88; Theorem 2.1 (b) at :92",
     "Sentence 1: 'For CT_t and TE_t to be integer numbers of cents, r P_t must be a multiple of 100'. TE_t = rP_t/100 (Theorem 2.1 (b)) and CT_t = r(P_t - d_t)/100 with d_t a multiple of 100, so each is integral iff rP_t is a multiple of 100: recomputed in recheck_l08_r19.py (CT integral iff (r*P) % 100 == 0 over the random cases, 0 violations). Sentence 2: 'a P_t that is a multiple of 100 cents is sufficient for every whole-number r' follows since r*P_t is then a multiple of 100. Sentence 3: 'DE_t and DTL_t need no condition on P_t' and the Definition 1.1 divisibility argument hold (DE and DTL integral in all 7,373 cases). Example: P = 50,001 cents with r = 100 gives an integral CT (630,021/100 at r = 21 is not integral, consistent with the condition). PASS."),
    ("AC1-c-r19-cmd-check_pages_dag", "1-structure check_pages and check_dag (round 19 re-run)",
     "tools/check_pages.py --unit AC1; tools/check_dag.py --unit AC1",
     "Re-run on the pin 51fa336: 'check_pages AC1: PASS' (exit 0) and 'check_dag AC1: PASS'. The curriculum prerequisite change (CS2 gains M1) does not touch AC1's prerequisite closure (AC1, S0, S2 and their closure)."),
    ("AC1-c-r19-cmd-run_labs", "2.5-labs run_labs (round 19 re-run)",
     "tools/run_labs.py --unit AC1",
     "'run_labs AC1: PASS (11/11)' on pin 51fa336."),
    ("AC1-c-r19-lab-twins-isolated", "2.5-labs twins alone under python -I -W error",
     "tests/labs/AC1/lab-AC1-L07-1.py; tests/labs/AC1/lab-AC1-L08-1.py",
     ".venv/bin/python -I -W error on each twin: exit 0 for both (outputs in ledgers/AC1/scripts/AC1-c-r19 run; L07 18 lines, L08 13 lines)."),
    ("AC1-c-r19-lab-embed-equals-twin-and-expected", "2.5-labs embedded code and expected block equal the twin and its output (round 19)",
     "course/modules/AC/AC1/L07.html:127-267; course/modules/AC/AC1/L08.html:108-208",
     "Compared programmatically: the embedded code block equals the twin file (both labs: True), and the 'expected' block equals the twin's printed output line for line (L07: True, 18 lines; L08: True, 13 lines)."),
    ("AC1-c-r19-seed-sweep", "2.5-labs 'pass for any seed' claims (L07.html:327; L08.html:273)",
     "ledgers/AC1/scripts/AC1-c-r19/seed_sweep_r19.py; seed_sweep_r19.out",
     "Both twins run under python -I with SEED replaced for seeds 0-40, 999, 123456789, 20260701 and 20260702: 45 seeds each, no failing seed for either lab. Supports the claims that the checks pass for any seed on the shipped generator."),
    ("AC1-c-r19-page_smoke", "2.5-labs and 2.2 browser smoke (round 19)",
     "tools/page_smoke.py --unit AC1 --pages L07 L08",
     "'page_smoke modules/AC/AC1/L07.html: PASS', 'page_smoke modules/AC/AC1/L08.html: PASS', 'page_smoke AC1: PASS' (Chromium, light and dark, 360 px; both labs run in the Pyodide runtime)."),
    ("AC1-c-r19-verify_refs", "1-citations verify_refs (round 19)",
     "tools/verify_refs.py --unit AC1 (live); tools/verify_refs.py --offline",
     "Live: 'live re-verification of AC1: 2 of 560 entries, 0 problems' (exit 0). Offline: 'offline integrity: 560 entries, 0 problems'. The pages cite no new registry keys (L08.html:383 and L07.html:442 state no key)."),
    ("AC1-c-r19-cards-L07-L08", "2.7-cards: L07 and L08 cards identical to the round-18 pin (round 19)",
     "course/modules/AC/AC1/cards.json (40 cards with lesson L07 or L08)",
     "Programmatic comparison of every L07 and L08 card between 7143726 and 51fa336: no change. Card answers were re-read against the lesson texts they cite; c109 and c111 and c139 match L08.html:85-88 in the current text. No duplicate ids (140 entries)."),
    ("AC1-c-r19-mutants-rerun", "2.5-labs archived lab mutants (r7-r17) re-run on the pin",
     "ledgers/AC1/scripts/AC1-c-r19/mutants_r19_rerun.py; mutants_rerun_r19.out",
     "All 41 archived lab-mutant and alternative cases re-run (mutants_r19_rerun.py, a copy of mutants_r18.py). Killed as expected (23 with exit 1): r7 (3), r8 (n2life, n3sign, n4te; n1ceil and n1b are PASS? cases), r9 (7), r10 (m10b, m10d, m10e), r17 (m17b-e), r18 (m18b, m18e, m18f). Exit 0 as recorded: the alternatives alt9a-c, alt10a-b, alt17a, alt18a-c (over-constraint check: a correct alternative must pass; all do), the 'PASS?' cases n1ceil, n1b, m10a, m10c, m18c, and the survivors m17a, m18a, m18d, m18g, which are classified below."),
    ("AC1-c-r19-new-student-mutants", "2.5-labs three new student-error mutants (round 19)",
     "ledgers/AC1/scripts/AC1-c-r19/mutants_r19_new.py; mutants_new_r19.out",
     "m19a (L08 tax depreciation uses the previous year's percent): exit 1, AssertionError. m19b (L08 current tax on pretax income, not taxable income): exit 1, AssertionError. m19c (L07 CFO subtracts the SBC expense): exit 1, AssertionError. All three killed. m19d (L08 rate 20 instead of 21): exit 0; not killed, but no assertion or lesson sentence states the lab checks the value of the rate (L08.html:107 calls the rate a model parameter, not a claim the lab tests it); out of scope, PASS."),
    ("AC1-c-r19-survivor-classification", "2.5-labs survivor classification under the architect ruling on lab mutants",
     "ledgers/AC1/scripts/AC1-c-r19/mutants_rerun_r19.out; course/modules/AC/AC1/L07.html:133; course/modules/AC/AC1/L08.html:103",
     "Lab twins are demonstrations; mutation testing applies to project graders only (ARCHITECT RULING, this round). A surviving lab mutant is a finding only if a lesson sentence claims the lab asserts or checks that property. L07.html:133 claims the lab checks the schedule sums and the Section 2 identities; the survivors m17a, m18c, m18g and the schedule-sum mutant m18a keep both true (m18a is killed by 5 of 45 seeds swept, and the shipped seed keeps the sums). L08.html:103 claims the lab checks Theorem 2.1 (a), (b) and the year-5 balance; m18d keeps those true. The printed-table statements (L07.html:268, :358; L08.html:262-265, :300) describe the verbatim output of the unchanged real runs. All survivors: out of scope, PASS."),
    ("AC1-c-r19-tooling-carried", "tooling gates (pytest, ruff, mypy) carried by unchanged tooling",
     "git diff --stat 7143726 51fa336 -- tools tests references notation",
     "No file under tools/, tests/ (other than tests/labs/AC4), references/ or notation/ changed in this range, so the round-18 tooling rows are carried under the carry rule. The AC4 lab twins that changed are outside this slice."),
]
for item in NEW:
    rid, check, loc, evidence = item[:4]
    if len(item) == 5:
        ROWS.append({"id": rid, "check": check, "location": loc, "status": "FAIL", "evidence": evidence, "fix": item[4]})
        continue
    ROWS.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": evidence})

# The FAIL row for the residual cumulative-basis attribution (added above as NEW[1]) must be FAIL with a fix.
for r in ROWS:
    if r["id"] == "AC1-c-r19-L08-line51-cumulative-basis":
        r["status"] = "FAIL"
        r["fix"] = ("Change the cause in L08.html:51 to: 'because Definition 1.1 makes the depreciation amounts multiples "
                    "of 100 cents, and the cumulative difference of Definition 1.2 is a sum of them.'")

verdict = "FAIL" if any(r["status"] != "PASS" for r in ROWS) else "PASS"
mutants = [
    {"id": "r7-m8a", "description": "L08 deferred expense from taxable income, not the balance change", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r7-m7a", "description": "L07 last-year branch disabled", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r7-m7b", "description": "L07 base amount plus one cent", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r8-n2life", "description": "L08 book depreciation over LIFE minus one", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r8-n3sign", "description": "L08 deferred expense sign reversed", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r8-n4te", "description": "L08 total tax expense omits the deferred part", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r9-m9a", "description": "L07 last vesting year takes the base, dropping the remainder", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r9-m9b", "description": "L07 vesting window off by one", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r9-m9c", "description": "L07 APIC change sign reversed", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r9-m9d", "description": "L07 cash-flow statement without the SBC add-back", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r9-m9e", "description": "L08 current tax ignores the temporary difference", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r9-m9f", "description": "L08 deferred tax balance sign flipped", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r9-m9g", "description": "L08 deferred tax balance without the tax rate", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r10-m10b", "description": "L07 APIC change one cent short of the SBC expense", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r10-m10d", "description": "L08 deferred expense equals the balance, not its change", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r10-m10e", "description": "L08 current tax computed on pretax plus the difference", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r17-m17b", "description": "L07 vesting window one year long", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r17-m17c", "description": "L07 last vesting year takes the base", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r17-m17d", "description": "L08 tax depreciation uses the first percent every year", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r17-m17e", "description": "L08 cumulative temporary difference not accumulated", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r18-m18b", "description": "L07 cash change equals the APIC change", "killed_by": "AssertionError in lab-AC1-L07-1 (r19 re-run)"},
    {"id": "r18-m18e", "description": "L08 deferred expense uses a stale balance", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r18-m18f", "description": "L08 total tax expense adds the balance instead of the deferred expense", "killed_by": "AssertionError in lab-AC1-L08-1 (r19 re-run)"},
    {"id": "r18-m18a", "description": "L07 schedule check sums years 1 to 5 only (seed-dependent)", "killed_by": "SURVIVES shipped seed; killed by AssertionError under 5 other seeds (r18, r19 sweep); out of scope (lab twin, architect ruling)"},
    {"id": "r19-m19a", "description": "L08 tax depreciation uses the previous year's percent", "killed_by": "AssertionError in lab-AC1-L08-1 (r19, new)"},
    {"id": "r19-m19b", "description": "L08 current tax on pretax income, not taxable income", "killed_by": "AssertionError in lab-AC1-L08-1 (r19, new)"},
    {"id": "r19-m19c", "description": "L07 CFO subtracts the SBC expense", "killed_by": "AssertionError in lab-AC1-L07-1 (r19, new)"},
    {"id": "r19-m19d", "description": "L08 rate 20 instead of 21", "killed_by": "SURVIVES; out of scope (lab twin, architect ruling; no lesson sentence claims the lab checks the rate value)"},
    {"id": "r17-m17a", "description": "L07 SBC row labelled one year early", "killed_by": "SURVIVES; out of scope (lab twin, architect ruling; L07.html:133 claims only the schedule sums and identities, which hold)"},
    {"id": "r18-m18c", "description": "L07 SBC row omits the last grant", "killed_by": "SURVIVES; out of scope (lab twin, architect ruling)"},
    {"id": "r18-m18d", "description": "L08 tax depreciation one year late", "killed_by": "SURVIVES; out of scope (lab twin, architect ruling; L08.html:103 claims only (a), (b) and the year-5 balance)"},
    {"id": "r18-m18g", "description": "L07 base amount floors the share count", "killed_by": "SURVIVES; out of scope (lab twin, architect ruling)"},
]

fragment = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 19,
    "round_note": ("round 19 (independent re-verification of AC1-c after pin 7143726). Delta: L08.html:51 and :88 "
                   "rewritten (51fa336); L04, L05, L06, cards entries c046-c069 and c140, curriculum CS2 prerequisite are "
                   "outside this slice. Architect ruling applied to lab-twin survivors."),
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 19; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "51fa336",
    "base": "7143726 (previous pin, for the delta)",
    "checkout": "/tmp/verify19-AC1-c",
    "scratch": "/tmp/AC1-v/AC1-c-r19",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": verdict,
    "rows": ROWS,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r19/mutants_r19_rerun.py",
        "ledgers/AC1/scripts/AC1-c-r19/mutants_new_r19.out",
        "ledgers/AC1/scripts/AC1-c-r19/mutants_r19_new.py",
        "ledgers/AC1/scripts/AC1-c-r19/mutants_rerun_r19.out",
        "ledgers/AC1/scripts/AC1-c-r19/recheck_l08.py",
        "ledgers/AC1/scripts/AC1-c-r19/recheck_l08_r19.out",
        "ledgers/AC1/scripts/AC1-c-r19/seed_sweep_r19.py",
        "ledgers/AC1/scripts/AC1-c-r19/seed_sweep_r19.out",
        "ledgers/AC1/scripts/AC1-c-r19/build_fragment_r19.py",
    ],
    "notes": (
        "Verdict FAIL on one row: AC1-c-r19-L08-line51-cumulative-basis (L08.html:51 attributes the multiple-of-100 "
        "property of the cumulative difference to Definition 1.1, which does not state it; Definition 1.2 does). "
        "Previous FAIL rows: AC1-c-r5-L08-line51-signed, AC1-c-r9-delta-read, AC1-c-r18-L08-why-it-matters are PASS "
        "(the P_t basis is removed; residual attribution is the new FAIL row). AC1-c-r17-m17a-survivor, AC1-c-r18-m18c, "
        "-m18d and -m18g are PASS under the ARCHITECT RULING on lab mutants (lab twins are demonstrations; no lesson "
        "sentence claims the lab asserts the property those survivors violate). Mutant files are not written under "
        "ledgers/AC1/mutants/ because tools/mutate_graders.py reads that directory. Not checked: project and grader files "
        "(other slices); the hours design targets (architect ruling: arithmetic only); live web sources beyond verify_refs."
    ),
    "summary": (
        f"{verdict}: {sum(r['status'] == 'PASS' for r in ROWS)} PASS, {sum(r['status'] != 'PASS' for r in ROWS)} FAIL "
        f"of {len(ROWS)} rows. FAIL: AC1-c-r19-L08-line51-cumulative-basis. Mutants: 23 killed (archived and new), "
        "4 lab survivors out of scope under the architect ruling, m19d out of scope."
    ),
}
out = root / "ledgers/AC1/AC1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(ROWS), "verdict", verdict, "ids unique", len({r["id"] for r in ROWS}) == len(ROWS))
