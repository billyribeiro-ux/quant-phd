"""Build the round-8 AC4-c fragment from the round-7 fragment: carry unchanged-subject rows, replace re-verified rows.

Run with -I: python -I build_fragment.py <checkout> <round7.json>
"""

import json
import sys
from pathlib import Path

co = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
CARRY_PREFIX = (
    "Carried from round 7 (cited subject byte-identical since the previous pin; the page-level diff, "
    "L05.html line 246 and L06.html lines 7, 52, 259, 345, lies outside it):"
)
CARRY = {
    "AC4-c-grades", "AC4-c-math-L05", "AC4-c-math-L06", "AC4-c-cards-L05", "AC4-c-cards-L06",
    "AC4-c-L05-cards-verbatim-check", "AC4-c-cards-c076", "AC4-c-quiz-keys", "AC4-c-L05-hypothesis-causal",
    "AC4-c-L05-P2-scope", "AC4-c-open-items-path", "AC4-c-L06-R1-unanswered", "AC4-c-L06-M2-misconception-kg",
    "AC4-c-L06-sign-convention", "AC4-c-L05-s4-fixed-error-scale", "AC4-c-L05-s5-volume-term",
    "AC4-c-L05-lab-stale-identity-label", "AC4-c-L05-lab-identity-line", "AC4-c-L06-P1-step-reason",
    "AC4-c-L05-remark23-L06-defs", "AC4-c-L05-definition-1-3-L06", "AC4-c-L05-misc3-split",
    "AC4-c-L06-misc1-mix", "AC4-c-L06-R3-standard", "AC4-c-L06-q4-sufficient", "AC4-c-L06-E1-static-variance",
    "AC4-c-L06-operating-variance-term", "AC4-c-L05-q8-explain", "AC4-c-L06-necessity-unproved",
    "AC4-c-L05-def11-operating-income", "AC4-c-L05-s3-exactness", "AC4-c-L06-prop21-proof-scope-r7",
    "AC4-c-L06-prop22-r7", "AC4-c-L05-definition-1-3-L06", "AC4-c-L06-honest-pending-r7", "AC4-c-L05-round7-edits",
}
FRESH = {
    "AC4-c-cmd-check-pages": "Re-run r8 on pin 2c8162b: 'check_pages AC4: PASS'.",
    "AC4-c-cmd-check-dag": "Re-run r8: 'check_dag AC2: PASS', 'check_dag AC4: PASS', 'check_dag CF1: PASS', 'check_dag AP1: PASS'.",
    "AC4-c-cmd-check-projects": "Re-run r8: 'check_projects AC2/AC4/CF1/AP1: PASS'.",
    "AC4-c-cmd-run-labs": "Re-run r8: 'run_labs AC4: PASS (10/10)'.",
    "AC4-c-twins-run": "Re-run r8: python -I -W error on both twins exit 0; printed output equals the embedded expected blocks (cmp_embedded.py: L05 17 lines, L06 14 lines, equal).",
    "AC4-c-page-smoke": "Re-run r8: 'page_smoke modules/AC/AC4/L06.html: PASS', 'page_smoke AC4: PASS'.",
    "AC4-c-lint-types-pytest": "Re-run r8: ruff check 'All checks passed!' and ruff format --check '10 files already formatted' on tests/labs/AC4; mypy --no-incremental on the two twins 'Success: no issues found in 2 source files'; pytest -k AC4 10 passed. Full-repo mypy and pytest not run.",
    "AC4-c-citations": "Re-run r8: verify_refs --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems'; --offline '560 entries, 0 problems'. L05.html:467 and L06.html:487 are '<ol data-references></ol>' (empty).",
    "AC4-c-numbers": "Recomputed r8 from unrounded values: 650/1150 = 56.5217% (displayed 56.5); 60 - 56.5217 = 3.4783 (displayed 3.48, then 3.5 pp); 1,500x(-40)+1,900x40 = 16,000; 150x1,660 = 249,000; 1,160,000 master OP; 1,425,000 flexed OP; 265/140 = 1.893; 2,800 standard kg = 2x650+3x500; 2,950 actual kg = 1,350+1,600. Budget 600 of 1,000 = 60% exact.",
    "AC4-c-dag-concepts": "Re-verified r8: L05 Def 1.1 (line 49) 'revenue less total cost (operating income of Lesson L01)' with AC4 L01 line 98; L06 line 52 'contribution is revenue less the cost of the material used' matches L06 Definition 1.2 line 65; dfn ids def-master-budget (L05:49), def-flexible-budget (L05:54), def-budget-variance-analysis (L06:65), each defined once.",
    "AC4-c-structure": "Re-verified r8 headings: L05 sections 1-10 (Two budgets..., ..., Where the canon breaks, Misconceptions, Problem set, Key results, Retrieval quiz, References); L06 sections 1-9 (Definitions and notation ... References). Problem tiers and honest-pending paragraphs present.",
    "AC4-c-banned-phrases": "Re-run r8: grep -i for roughly/historically/typically/generally/usually/half/ellipsis/build/builder/verifier/round on L05.html, L06.html and both twins: no learner-text hits; 'about' hits are not figures.",
    "AC4-c-cards-dup-scan": "Re-run r8 (cards.json, 119 cards): 0 duplicate ids, 0 duplicate normalised fronts; L05/L06 cards AC4-c059..068, c069..081, c110..112 identical to the previous pin (identity check).",
    "AC4-c-lab-L05-output": "Re-run r8: twin output (17 lines) equals the embedded pre.expected block (cmp_embedded.py); embedded code block equals the twin after tag stripping (only final newline differs). L05.html lines 93-241 unchanged in this delta.",
    "AC4-c-lab-L06-output": "Re-run r8: twin output (14 lines) equals the embedded expected block; embedded code equals the twin. Hypothesis values -40,000 / +249,000 / +16,000 / -75,000 / +150,000 / +140,000 reproduced.",
    "AC4-c-L06-lab-docstring-residual": "Re-run r8: mutant m01 raises 'ValueError: the four variances leave a residual of -150000 cents'. The docstring claim 'raises ValueError if the residual is not zero' holds; the page claims only that.",
    "AC4-c-L06-meta-desc": "Round-7 FAIL cleared. L06.html line 7 now reads '... gives the operating-profit variance of this lesson, which Lesson L05 calls the static variance.' L05.html line 78 defines static variance as Pi_a - Pi_m, and L06 operating-profit variance = contribution variance + fixed-cost variance = Pi_a - Pi_m (algebra on both sides), so the attribution is correct. L05 uses 'static variance' (not 'operating-profit variance').",
    "AC4-c-L06-interp-sentences": "Re-verified r8 (line 259 changed): 650/1,150 = 56.52% -> 56.5%; budget 600/1,000 = 60%; gap 60 - 56.52 = 3.48, shown as 3.5 pp; 150x1,660 = 249,000; 2,950 kg vs 2,800 standard kg (2x650+3x500); 140,000 after -10,000; check units 690 = 0.6x1,150 and 460 = 0.4x1,150. Lab output: check_on_mix_sales_mix_variance 0, check_on_mix_efficiency_variance 0, check_on_mix_sales_volume_variance 249000.",
    "AC4-c-L06-scope-when-zero": "Re-verified r8 (line 52 changed): 'when zero' and 'sufficient condition' match Prop 2.2(a),(b) and 'No converse is claimed'; line 52 now defines the contribution variance as the change in contribution (revenue less material cost, Definition 1.2 line 65), matching Prop 2.1.",
    "AC4-c-L06-why-def12": "Re-verified r8 (line 52 changed): '(the change in contribution, which is revenue less the cost of the material used, Definition 1.2)' matches L06 Definition 1.2 line 65 ('The contribution is revenue less the cost of the material used'); the contribution variance T = C_a - C_b (line 72) is the change in that quantity.",
    "AC4-c-L06-section1-ref": "Re-verified r8: line 52 reference to Section 1 / Definition 1.2 holds (as above); Section 1 at line 56 cites L05 Definition 1.3 (L05.html:58, verified); Section 4 heading 'Where the canon breaks' at L06.html:265.",
    "AC4-c-lab-L06-mutants": "Re-run r8 on 13 L06 mutants (previous round m01-m04, n01-n03 and new s01-s04 and s03 duplicate of n02): killed by ValueError residual or non-whole cents: m01, m02, m03, n01, n02, n03, s01, s02, s03, s04. Survivor m04 (sales price variance on budget units) prints the same -40,000 on this case, so the identity check cannot detect it; the page does not claim the lab detects a sales-price error (limitation, no FAIL row: the page claims only that a nonzero residual raises ValueError, which holds).",
    "AC4-c-lab-alt-impl": "Re-run r8: alternative correct implementations alt01 (mix as sum minus total), alt02 (mix as sum CM q_a - Q_a CMbar), alt03 (mix in float then round), alt04 (CMbar with per-product weights), alt05 (efficiency per-product loop) all exit 0 with output identical to the twin (no over-constraint).",
    "AC4-c-L05-lab-mutants": "Re-run r8: n04 (fixed overhead flexes with units) and n05 (flexed material from actual kg) and new s05 (flexed budget at budget units) print output differing from the embedded block (flexible_variance -50,000 / +140,000); the L05 identity assert holds by construction and does not catch them, so the printed-output comparison does.",
    "AC4-c-hours": "Re-run r8: data-hours L01..L08 = 6,7,6,6,7,6,6,6 (sum 50) equals index.html data-hours-lessons=\"50\"; L05 data-hours 7 and L06 data-hours 6 (L05.html:2, L06.html:2). No pace estimate used (architect ruling).",
}
NEW = [
    {
        "id": "AC4-c-L05-s4-relevant-range-r8",
        "check": "2.9 L05 section 4 bullet 1 (relevant range), rewritten in round 8",
        "location": "course/modules/AC/AC4/L05.html line 246",
        "status": "PASS",
        "evidence": "New text: 'If capacity must be added above some volume, fixed overhead may rise there, and a flexed budget that keeps it at 500,000 cents then understates the cost at that volume.' Conditional, no number; consistent with Q8 explanation (L05.html:454: outside the relevant range the linear cost function no longer holds, so a flexed budget can misstate cost) and with C(Q)=F+vQ. The lab evaluates only 1,000 budgeted and 1,150 actual units (twin master_units 1000, actual_units 1150; no other volume in the twin).",
    },
    {
        "id": "AC4-c-L06-P3-r8",
        "check": "2.4 L06 P3 solution (one product), rewritten in round 8",
        "location": "course/modules/AC/AC4/L06.html line 345",
        "status": "PASS",
        "evidence": "'M = CM(q_a - Q_a) = 0' and 'V = (Q_a - Q_b)CM'; new sentence 'the contribution variance is the sum of the price, volume and efficiency variances' re-derived: CM = p_b - s pi; SP+V+E = (p_a-p_b)q_a + (q_a-q_b)CM - pi(kg_a - s q_a) = p_a q_a - pi kg_a - q_b CM = T. Numeric check (ledgers/AC4/scripts/AC4-c-r8/recheck.py): p_b 2500, p_a 2400, s 2, pi 500, q_b 600, q_a 650, kg_a 1350 gives SP -65,000, V +75,000, M 0, E -25,000, sum -15,000 = T.",
    },
    {
        "id": "AC4-c-mutants-new-r8",
        "check": "2.5 lab student-error mutants (round 8, new): s01-s05",
        "location": "ledgers/AC4/mutants/AC4-c-r8/s01..s05; tests/labs/AC4/lab-AC4-L06-1.py; tests/labs/AC4/lab-AC4-L05-1.py",
        "status": "PASS",
        "evidence": "Generated by ledgers/AC4/scripts/AC4-c-r8/make_r8_mutants.py (each replacement asserted to match once) and run by run_mutants.sh under python -I -W error. s01 mix share from actual total: ValueError residual 16,000. s02 volume at actual mix margin: ValueError 'sales volume variance is 5775000/23, which is not a whole number of cents'. s03 efficiency allowance on budget units: ValueError residual 200,000 (duplicates n02 in effect). s04 actual revenue at budget price: ValueError residual 40,000. s05 L05 flexed budget at budget units: printed flexible_variance 140,000 vs 125,000 in the embedded block. All five killed.",
    },
    {
        "id": "AC4-c-alt-impl-r8",
        "check": "2.5 alternative correct implementations (over-constraint check, round 8)",
        "location": "ledgers/AC4/mutants/AC4-c-r8/alt01..alt05",
        "status": "PASS",
        "evidence": "Five valid alternatives (mix as sum CM q_a minus Q_a CMbar; float mix rounded; CMbar with per-product weights; efficiency as a per-product loop; mix as sum minus total) all exit 0 with output identical to the embedded block. The lab does not over-constrain the implementation.",
    },
    {
        "id": "AC4-c-embedded-code-r8",
        "check": "2.5 embedded code blocks equal the twins (round 8)",
        "location": "course/modules/AC/AC4/L05.html and L06.html embedded code; tests/labs/AC4/lab-AC4-L05-1.py and L06-1.py",
        "status": "PASS",
        "evidence": "ledgers/AC4/scripts/AC4-c-r8/cmp_embedded.py: after stripping tags and unescaping, the embedded code block equals the twin (L05 True, L06 True; only trailing newline differs in the raw file).",
    },
]
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        if not FRESH[rid]:
            continue
        r = dict(r, status="PASS", evidence=FRESH[rid])
    elif rid in CARRY:
        r = dict(r, evidence=f"{CARRY_PREFIX} {r['evidence']}")
    elif rid == "AC4-c-L06-meta-desc":
        r = dict(r, status="PASS", evidence=FRESH["AC4-c-L06-meta-desc"])
    else:
        raise SystemExit(f"row {rid} has no disposition")
    r.pop("fix", None)
    rows.append(r)
rows.extend(NEW)
missing = [r["id"] for r in prev["rows"] if r["id"] not in {x["id"] for x in rows}]
print("previous ids missing from new fragment:", missing)
frag = {
    "unit": "AC4",
    "slice": "AC4-c",
    "round": 8,
    "verifier": "independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 8; did not build AC4",
    "pin": "2c8162b",
    "base": "de53f7e",
    "previous_ledger": "/tmp/fanout-frags/AC4-c.round7.json",
    "checkout": "/tmp/verify8-AC4-c (detached, pinned at 2c8162b)",
    "scratch": "/tmp/AC4-v/AC4-c-r8",
    "verified_at": "2026-10-28T00:00:00Z",
    "rows": rows,
}
frag["verdict"] = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag["mutants"] = [
    {"id": m["id"], "description": m["description"], "killed_by": m["killed_by"], "file": m["file"]}
    for m in prev["mutants"]
] + [
    {"id": "s01_L06_mix_share_from_actual_total", "description": "L06 mix share taken from actual total units", "killed_by": "ValueError: the four variances leave a residual of 16000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s01_L06_mix_share_from_actual_total.py"},
    {"id": "s02_L06_volume_at_actual_mix_margin", "description": "L06 volume variance uses the actual-mix average contribution margin", "killed_by": "ValueError: sales volume variance is 5775000/23, which is not a whole number of cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s02_L06_volume_at_actual_mix_margin.py"},
    {"id": "s03_L06_efficiency_allowance_on_budget_units", "description": "L06 efficiency allowance on budget units (same error class as n02)", "killed_by": "ValueError: the four variances leave a residual of 200000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s03_L06_efficiency_allowance_on_budget_units.py"},
    {"id": "s04_L06_actual_revenue_at_budget_price", "description": "L06 actual contribution uses budget price", "killed_by": "ValueError: the four variances leave a residual of 40000 cents", "file": "ledgers/AC4/mutants/AC4-c-r8/s04_L06_actual_revenue_at_budget_price.py"},
    {"id": "s05_L05_flexed_budget_at_budget_units", "description": "L05 flexed budget evaluated at budget units", "killed_by": "printed output differs from embedded block: flexible_variance 140000", "file": "ledgers/AC4/mutants/AC4-c-r8/s05_L05_flexed_budget_at_budget_units.py"},
    {"id": "m04_sales_price_uses_budget_units_SURVIVED", "description": "SURVIVOR (limitation, no FAIL row): sales price variance on budget units gives the same -40,000 on this case", "killed_by": "none: survives (printed output identical)", "file": "ledgers/AC4/mutants/AC4-c-r8/m04_sales_price_uses_budget_units.py"},
]
frag["registry_flags"] = prev.get("registry_flags", [])
frag["freshness_flags"] = []
frag["notes"] = [
    "Delta de53f7e..2c8162b for this slice: L05.html line 246 (section 4 bullet 1 rewrite); L06.html line 7 (meta, round-7 FAIL cleared), line 52 (why it matters), line 259 (interpretation), line 345 (P3 solution). cards.json changed only at c091 (L07, not this slice); L05/L06 cards identical. Lab twins and embedded code blocks unchanged.",
    "Carry-prefix deviation: L05.html and L06.html are not byte-identical to the previous pin, so the literal prefix 'byte-identical' is replaced by 'cited subject byte-identical', and the exception lines are named in the prefix. Every carried row cites none of the changed lines.",
    "Mutant copies: the r7 mutant files were copied from the round-7 scratch checkout (/tmp/verify7-AC4-c/ledgers/AC4/mutants/AC4-c-r7) and re-run here against the twins.",
    "s03 duplicates n02 in effect; it is kept as a recorded mutant, not counted as one of the four genuinely new ones (s01, s02, s04, s05).",
    "Hours: no pace estimate used. Lesson hours 6+7+6+6+7+6+6+6 = 50 equals index data-hours-lessons 50.",
]
frag["could_not_check"] = [
    "Full-repo mypy --no-incremental and full pytest not run (mypy on the two twins, pytest -k AC4 only).",
    "No external source consulted: neither lesson cites a registry key, so no published figure is checked.",
    "Browser rendering not run; page_smoke executes labs in Python, not in a browser.",
    "project.html, the hub index.html and the AC4 grader changed in this delta but belong to other slices and were not re-verified here.",
]
frag["summary"] = f"rows {len(rows)}: pass {sum(r['status']=='PASS' for r in rows)}, fail {sum(r['status']=='FAIL' for r in rows)}"
out_path = co / "ledgers/AC4/AC4-c.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(frag["summary"], frag["verdict"])
