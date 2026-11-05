"""Builds ledgers/E4/E4-c.json (round 8) from the round-7 row ids, with round-8 statuses and evidence.

Every row below was re-checked at round 8 on the pin 0dee921a: the pages were read in full, the numbers
were re-derived, the twins were run, and the cards were read. Previous PASS statuses were not carried.
"""
import json
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-E4-c"
PREV = "/Users/billyribeiro/.fanout/frags/E-E4-c.round7.json"
prev = json.load(open(PREV, encoding="utf-8"))
OUT = "/Users/billyribeiro/.fanout/wt/verifyE8-E4-c/ledgers/E4/E4-c.json"
S = "ledgers/E4/scripts/E4-c-r8"

SUFFIX = {
    "2.2-numbers": f"numbers re-derived by {S}/rederive_r8.py (out/rederive_r8.out)",
    "2.2-numbers/prose": f"numbers re-derived by {S}/rederive_r8.py (out/rederive_r8.out)",
    "2.4-math": "every derivation re-derived by hand in this round; numeric checks in " + f"{S}/rederive_r8.py",
    "2.4-mathematics": "every derivation re-derived by hand in this round; numeric checks in " + f"{S}/rederive_r8.py",
    "math": "derivation re-derived by hand in this round",
    "2.5-labs": f"twin run standalone under python -I -W error ({S}/out/twin_*.out); page code and expected block equal to the twin ({S}/twin_vs_page.py, out/twin_vs_page.out)",
    "2.7-cards": f"all 86 L07 to L09 cards read (out/cards_L07_L09.txt); duplicate and basis scan in {S}/slice_checks_r8.py (out/slice_checks_r8.out)",
    "2.9-structure": f"page read in full; banned, process and scope scans in {S}/slice_checks_r8.py (out/slice_checks_r8.out); check_pages, check_dag and page_smoke PASS",
    "2.9-prose": f"prose read in full; banned, process and scope scans in {S}/slice_checks_r8.py (out/slice_checks_r8.out)",
    "2.9-quiz": "quiz item and explanation read against the lesson text",
    "2.9-dag": f"dfn ids unique and definition links resolve ({S}/slice_checks_r8.py, out/slice_checks_r8.out); unlinked closure-outside terms scanned",
    "2.9-hours": "data-hours and hours text read; hub split is slice a",
    "2.9-proof": "proof re-derived by hand in this round",
    "2.9-mechanics": "solution re-derived by hand in this round",
    "2.3-grades": "grades re-graded against BLUEPRINT section 3 by hand",
    "2.1-citations": f"registry record read (references/references.json, milgrom1982information) and verify_refs run ({S}/out/verify_refs_unit_live.out)",
    "2.8-data": "SIMULATED labels read against the code and the hypothesis",
    "2.9-references": "references section read",
    "delta": "delta since round-7 pin 06994db1 read hunk by hunk (git diff)",
    "labels": "assumption and theorem labels read against the text",
    "notation": f"notation scan ({S}/slice_checks_r8.py, out/slice_checks_r8.out)",
    "2.4-mathematics/notation": f"notation scan ({S}/slice_checks_r8.py); derivation re-derived by hand",
    "2.4-math/notation": f"notation scan ({S}/slice_checks_r8.py); derivation re-derived by hand",
    "2.9-structure/cards": "card and page read in full",
}


def suffix_for(check):
    if check in SUFFIX:
        return SUFFIX[check]
    if check.startswith("2.5"):
        return SUFFIX["2.5-labs"]
    if check.startswith("2.7"):
        return SUFFIX["2.7-cards"]
    if check.startswith("2.9"):
        return SUFFIX["2.9-prose"]
    if check.startswith("2.4") or check.startswith("math"):
        return SUFFIX["2.4-math"]
    return "re-read at round 8"


CMD = {
    "E4c-cmd-check-pages": (f"{S}/out/check_pages_E4.out", "check_pages.py --unit E4: PASS"),
    "E4c-cmd-check-dag": (f"{S}/out/check_dag_E4.out", "check_dag.py --unit E4: PASS"),
    "E4c-cmd-check-projects": (f"{S}/out/check_projects_E4.out", "check_projects.py --unit E4: PASS"),
    "E4c-cmd-run-labs": (f"{S}/out/run_labs_L07.out, run_labs_L08.out, run_labs_L09.out", "run_labs.py --unit E4 --page L07/L08/L09: PASS (1/1 each)"),
    "E4c-cmd-twins-standalone": (f"{S}/out/twin_L07-1.out, twin_L08-1.out, twin_L09-1.out", "each twin run alone under .venv python -I -W error from an empty directory: exit 0"),
    "E4c-expected-equals-output": (f"{S}/out/twin_vs_page.out", "expected blocks equal the live twin output (28, 20, 18 lines); page code equals twin apart from the final newline"),
    "E4c-cmd-page-smoke": (f"{S}/out/page_smoke_L07-9.out", "page_smoke.py --unit E4 --pages L07 L08 L09: PASS (L09 lab 5.0 s, L07 0.0 s, L08 0.1 s)"),
    "E4c-cmd-ruff-mypy-twins": (f"{S}/out/ruff_check.out, mypy_twins.out", "ruff check and format --check: pass; mypy --no-incremental on the three twins: no issues"),
    "E4c-cmd-pytest-labs": (f"{S}/out/pytest_labs_E4.out", "pytest tests/test_labs.py -k E4: 13 passed"),
    "E4c-cmd-verify-refs": (f"{S}/out/verify_refs_offline.out, verify_refs_unit_live.out", "verify_refs --offline: 560 entries 0 problems; verify_refs --unit E4 live: 3 of 560 re-verified, 0 problems"),
    "E4c-cmd-run-graders": (f"{S}/out/run_graders_E4.out", "run_graders.py --unit E4: PASS (grader panel, not this slice)"),
}

CHANGED_FAIL_OVERRIDES = {
    "E4c-L07-problems-E1": {
        "status": "FAIL",
        "check": "2.2-numbers",
        "location": "course/modules/E/E4/L07.html:459 (Problem E1 solution)",
        "evidence": "Re-read at 0dee921a. The solution writes '1/3 - 0.330625 = 0.002708' and '0.002708/0.02 = 0.135' with '=', but 1/3 - 0.330625 = 0.0027083... and the ratio is 0.13541..., so both are rounded values with no rounding rule stated. Recomputed in " + f"{S}/rederive_r8.py" + " (out/rederive_r8.out: 0.0027083333, 0.13541666). The printed lab value 0.330625 is exact, so no printed digit is misquoted.",
        "fix": "In L07.html:459 replace the two '=' with approximation signs and state the rounding: '1/3 - 0.330625 = 0.0027083... (about 0.002708, six decimals)' and 'In units of the tolerance it is 0.0027083.../0.02 = 0.13541... (about 0.135, three decimals)'. No other change.",
    },
    "E4c8-L08-misc3-printed-range": None,
}

NEW_ROWS = [
    {
        "id": "E4c8-L08-misc3-printed-range",
        "check": "2.2-numbers / 2.5-labs (rounding rule; what the lab prints)",
        "location": "course/modules/E/E4/L08.html:595-596 (misconception 3, 'Lab 1 prints values from 0.013 to 0.167')",
        "status": "FAIL",
        "evidence": f"Lab 1 Part C prints Corr(v,p*)^2 = 0.013061 (cost 0.17) and 0.166667 (cost 0.12) (out/twin_L08-1.out lines 'part C: ... Corr(v,p)^2 = ...'; expected block L08.html:557-562). The sentence says the lab prints values 0.013 and 0.167, which are rounded to three decimals, and the page states no rounding rule (plan 2.1 item 1 requires one for a rounded figure). The range is correct; the printed digits are not.",
        "fix": "In L08.html:596 replace '\\(0.013\\)' and '\\(0.167\\)' with the printed values '\\(0.013061\\)' and '\\(0.166667\\)' (cost 0.17 and cost 0.12).",
    },
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in CHANGED_FAIL_OVERRIDES and CHANGED_FAIL_OVERRIDES[rid]:
        o = CHANGED_FAIL_OVERRIDES[rid]
        rows.append({"id": rid, "check": o["check"], "location": o["location"], "status": o["status"], "evidence": o["evidence"], "fix": o["fix"]})
        continue
    if rid in CMD:
        loc, ev = CMD[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": f"Re-run at round 8 on pin 0dee921a: {ev}. Output: {loc}."})
        continue
    status, evidence = "PASS", None
    if rid == "E4c-L08-prop-5.2":
        evidence = ("Round-7 FAIL fixed and re-checked. Assumption A4 now states (i) N continuous on [0,1] and (ii) the sign-change bracket "
                    "condition (L08.html:313-321), both assumed. Proposition 5.2(c) (L08.html:308-309) says 'Assuming A4'; its proof (L08.html:330) "
                    "cites A4(i) and A4(ii) by number. Limit in 5.2(a) re-derived by hand (L08.html:325-328): kappa*beta -> a sigma_v^2, Var(D_I) and "
                    "Var(D_U)/V_U limits as stated. Numerically G(1e-6)-G(0) = -6.25e-14 (out/rederive_r8.out). Key-results row (L08.html:723), "
                    "Section 6 (578) and References (800) all say A4 is assumed.")
    elif rid == "E4c-L09-res-1":
        evidence = ("Round-7 FAIL fixed. Problem Res 1 solution (L09.html:405) now says Proof 1 applies to P_2 and the bet -x-k, because M is a union of "
                    "P_2 cells (Definition 1.2); the sum then gives E[-x-k | D] >= 0 per P_2 cell and -S_1 - k*pi(M) >= 0. Re-derived: adding S_1 >= 0 gives "
                    "-k*pi(M) >= 0, contradicting k>0 and pi(M)>0.")
    elif rid == "E4c-L08-misc-claims":
        evidence = ("Misconceptions at L08.html:583, 587, 591 read and checked (Proposition 5.1(a), Definition 4.6(i), the cost statement). "
                    "The sentence at L08.html:595-596 is judged separately in row E4c8-L08-misc3-printed-range (FAIL), so this row covers only 583, 587, 591 and 599-600.")
    elif rid == "E4c-L07-prop-7.6":
        evidence = ("Subject changed in the round-8 delta (L07.html:102, 107 now define tau_eta and tau_bar as in L06 Proposition 6.7). Re-derived: "
                    "kappa = a sigma_e^2/lambda; sigma_eta^2 = sigma_e^2 + kappa^2 sigma_u^2; Y = p/theta_s = v + eta; Corr(v,Y)^2 = sigma_v^2/(sigma_v^2+sigma_eta^2) = tau_eta/(tau_v+tau_eta). "
                    "Assumption A1 of L06 (L06.html:61-64) requires sigma_u^2 > 0, so the remark at L07.html:122 about Proposition 6.7 is correct. Numbers: rederive_r8.out L07 block.")
    if evidence is None:
        evidence = f"Round 8 fresh re-check at 0dee921a of {r['location']}: " + suffix_for(r["check"]) + "."
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})

rows += NEW_ROWS
rows.append({
    "id": "E4c8-delta-read",
    "check": "delta",
    "location": "course/modules/E/E4/L07.html:99-107, 132; L08.html:51, 66-79, 311-336, 569-579; L09.html:124, 402-405; index.html:33, 167; cards.json (46 changed lines)",
    "status": "PASS",
    "evidence": "git diff 06994db1..0dee921a read hunk by hunk for the slice (the twins lab-E4-L07-1, L08-1, L09-1 are byte-identical to the round-7 pin). Every changed sentence was re-checked: L07 Prop 7.6 notation, L08 A3 wording, A4 split, Prop 5.2 and its proof, Section 5.1 wording, Section 6 bullets, quiz explanation (rounding rule stated), L09 Lab 1 paragraph and Res 1 solution, hub text.",
})
rows.append({
    "id": "E4c8-twin-page-equal",
    "check": "2.5-labs",
    "location": "tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py; course/modules/E/E4/L07.html, L08.html, L09.html",
    "status": "PASS",
    "evidence": f"Embedded data-run code equals the twin apart from the final newline (rstrip equal for all three); run by {S}/twin_vs_page.py (out/twin_vs_page.out).",
})
rows.append({
    "id": "E4c8-rederive-numbers",
    "check": "2.2-numbers",
    "location": "course/modules/E/E4/L07.html, L08.html, L09.html (every printed and quoted number)",
    "status": "PASS",
    "evidence": f"Independent re-derivation from the lesson formulas, not from the twins: {S}/rederive_r8.py (out/rederive_r8.out): L07 Parts A to E exact (1/3, 4/9, 1/6, 1/18, 1/66, 9/22, 1/2, 2500/5001, Var(p) list), Prop 7.7 signs on an exact grid; L08 G(0)=ln2/4, G(1)=ln(5/3)/4, G(0.5)=0.158997, root values and gaps at costs 0.12 to 0.18, monotone G and Corr on the 999-point grid, noiseless Part D; L09 exhaustive enumeration of 5^6 bets: 500 strict, 0 strict-and-nonneg, 625 nonneg, 0 nonzero, first witnesses.",
})
rows.append({
    "id": "E4c8-scope-banned-dfn-notation",
    "check": "2.9-structure",
    "location": "course/modules/E/E4/L07.html, L08.html, L09.html (prose, scope words, dfn ids, notation)",
    "status": "PASS",
    "evidence": f"{S}/slice_checks_r8.py (out/slice_checks_r8.out): 0 banned phrases, 0 process words; scope-word sentences read one by one (out/scope_hits.txt); dfn ids unique and every definition link resolves; no forbidden raw macro (mathbb, Phi, gamma, R-ast, mathbb-Q); out-of-closure names (Bayes, martingale, fixed point, state price) absent from the three pages.",
})
rows.append({
    "id": "E4c8-cards-L07-L09",
    "check": "2.7-cards",
    "location": "course/modules/E/E4/cards.json (E4-c130 to E4-c211, E4-c222 to E4-c224, E4-c232, E4-c233: 86 cards)",
    "status": "PASS",
    "evidence": f"All 86 cards read against the current lesson text (out/cards_L07_L09.txt). Full-file duplicate scan over 232 cards: no duplicate ids, fronts or backs ({S}/slice_checks_r8.py). Every T card has a basis. Numbers on cards appear in their lesson text or lab output.",
})
rows.append({
    "id": "E4c8-registry-milgrom",
    "check": "2.1-citations",
    "location": "course/modules/E/E4/L09.html:512; references/references.json (key milgrom1982information)",
    "status": "PASS",
    "evidence": f"Registry record (verified_by crossref): title 'Information, trade and common knowledge', Journal of Economic Theory, volume 26, issue 1, pages 17-27, year 1982. L09.html:512 quotes these fields exactly and states no result of the paper ({S}/out/slice_checks_r8.out).",
})

out = {
    "unit": "E4",
    "slice": "c",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 8 (did not build E4)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "checkout": ROOT,
    "scratch": "/tmp/e4c8_* (labs run from empty directories with the venv python -I -W error)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "grossman1980 (Grossman and Stiglitz, AER 1980) still has no registry record (B1, REFERENCE_REQUEST R-E4-1); L08 cites no key, which is correct.",
        "mascolell1995microeconomic author conflict (B3) is outside this slice (L09 and L08 do not cite it).",
    ],
    "freshness_flags": [],
    "notes": (
        "Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py; the L07 to L09 cards of cards.json. "
        "Pin 0dee921a (round-7 pin 06994db1). Delta read hunk by hunk. Round-7 FAIL rows E4c-L08-prop-5.2 and E4c-L09-res-1 are re-checked and PASS. "
        "No round-7 PASS row was carried: each row was re-checked this round. Lab twins are demonstrations: mutation testing does not apply to this slice (ruling), so mutants is empty. "
        "Two new non-PASS rows are rounding defects (class 1): L07.html:459 and L08.html:596. Observations that are not FAIL rows: (1) Proposition 5.2(c) and the bisection use A4; A4(i) continuity is assumed, not derived, and is stated as such. "
        "(2) Lemma 7.4, Proposition 7.6 and Proposition 7.7 state their hypotheses in the statement; Proposition 7.6 cites A1 to A4 and G of L06, and L06 Assumption A1 includes sigma_u^2 > 0. "
        "(3) L09 why-it-matters uses 'common knowledge' and 'prior' with pointers to later definitions (accepted as forward pointers, as in round 7). "
        "(4) The L08 Emp 3 and Mech 3 approximations use the approximation sign and the lab's printed six decimals; not flagged."
    ),
    "could_not_check": (
        "The Grossman and Stiglitz (1980) paper (no registry record, B1; the lessons cite no key, so there is nothing to check against it). "
        "The abstract of Milgrom and Stokey (1982) was not read: L09 states no result of that paper, so no claim is attributed. "
        "The L06 statements used by L07 and L08 (Definition 6.1, Definition 6.2, Assumptions A1 to A4 and G, Proposition 6.7, Corollary 6.8 where cited) were read only at the cited locations, not as a full slice (slice a/b). "
        "Browser rendering beyond page_smoke (no figure on these pages). The lab timing under Pyodide was measured by page_smoke only."
    ),
    "summary": (
        "Slice E4-c round 8 (L07, L08, L09, their lab twins and their cards). Rows: see counts below. Non-PASS: E4c-L07-problems-E1 (L07.html:459, rounded "
        "values written with '=') and E4c8-L08-misc3-printed-range (L08.html:596, lab 'prints 0.013 to 0.167' with no rounding rule). All other rows PASS, including the round-7 FAILs E4c-L08-prop-5.2 and E4c-L09-res-1, now fixed."
    ),
}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print("rows", len(rows), Counter(r["status"] for r in rows))
