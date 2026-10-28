"""Write ledgers/CF1/CF1-c.json (round 12). Round-11 PASS rows are carried only where the cited subject is unchanged."""
import json
from pathlib import Path

CHECKOUT = Path("/tmp/verify12-CF1-c")
PREV = json.loads(Path("/tmp/fanout-frags/CF1-c.round11.json").read_text(encoding="utf-8"))
D = "ledgers/CF1/scripts/CF1-c-r12"

FRESH = {
    "CF1-c-num-L06-E3-width": "Re-verified in round 12: L06.html Section 3 (line 211) was rewritten. Printed quantiles 14896.62 and 143406.13 give 128509.51 (recompute_r12.out). E3 solution width 128509.51 cents = 1285.10 currency units (1285.0951, recomputed). Misconception 2 '128509.50 from the unrounded ones': unrounded width 128509.5035 (recompute_r12.out), which rounds to 128509.50. PASS.",
    "CF1-c-scope-L06-section4-intro": "Round 11 FAIL re-verified and fixed: L06.html line 223 now reads 'The first and fourth limits below concern the model and its inputs. The second and third concern the sampling error of the estimator.' Bullets at lines 226-229: 1 independence across years (model assumption), 2 'Sampling error is not model error' (contrasts the estimator's error bar with wrong inputs), 3 sampling error of tail quantiles, 4 the discount rate as an input. The mapping matches the bullet subjects. PASS.",
    "CF1-c-num-recompute-r11": f"Recomputed in round 12 by {D}/recompute_r12.py and recompute_l05_r12.py (outputs in the same folder): L06 line 111 closed forms 79078.68 and 49379.84; E1 z 1.2419 (printed 1.242) and two-sided probability 0.2143; E2 band 0.0532 to 0.0572; se ratio 19.9 against sqrt(500) = 22.36 (22.4); sd ratio 1.0008; L05 gap 385535.69 equals the PV of years 4-6 (385535.6942); gap/NPV A = 133.23%; E1 range 5724.41; M2 discounted payback 3.019. PASS.",
    "CF1-c-cards-duplicates": f"Full scan of all 103 cards in course/modules/CF/CF1/cards.json ({D}/card_dupes.py, card_dupes.out): zero identical fronts and zero identical backs; near-duplicate pairs are distinct facts (see CF1-c-cards-dupes-r12-cross). The round-11 scan covered 100 cards. PASS.",
    "CF1-c-cards-L05": f"L05 cards CF1-c062 to c074, c096 to c098 and c102 re-checked against L05.html and lab-CF1-L05-1.out. Changed card CF1-c068 (front now simple payback only; back 2.750 years) matches 'project A simple_payback 2.750'. New card CF1-c102 matches 'discounted_payback 3.469'. Card-level diff ({D}/cards_delta.out): c068 is the only changed card in this slice. PASS.",
    "CF1-c-cards-L05-other": "Cards CF1-c062 to c067, c069 to c074, c096 to c098 re-checked: objects unchanged since 91946cf (cards_delta.out) except c068 (checked above), and each number on them (2.750, 3.469, 289367.40, -132231.40, 385535.69, 121251.71, 693692.91) appears in the L05 text or lab output. PASS.",
    "CF1-c-cards-L06": "Carried from round 11 (cards.json objects CF1-c075 to c087, c099, c100 byte-identical since the previous pin 91946cf, per the object-level diff in ledgers/CF1/scripts/CF1-c-r12/cards_delta.out): the card-level diff changed only c027, c042 (other lessons) and c068 (L05), and added c101 to c103 (L02, L03, L05).",
    "CF1-c-struct-L06": "Re-read all of L06.html (465 lines) in round 12, including the rewritten Section 3 and Section 4 intro. Template sections 1 to 9 present in order; Lab 1 pre blocks identical to the twin (CF1-c-cmd-twin-vs-page); nine quiz items (six multiple-choice, three numeric) with explain blocks; key-results table has seven rows (four T, three C); references via data-references; check_pages PASS (gates_r12.out). PASS.",
    "CF1-c-banned-scan": "Scanned L05.html and L06.html learner text (pre blocks removed, tags stripped) for banned and scope words (roughly, about, historically, typically, half, ellipsis, build, round, verifier, always, only, all, same, drives, offsets, raises, never). L06 'roughly as the square root of n' is the lab's stated prediction, tested by the 19.9 vs 22.4 output; 'about 0.0532 to 0.0572' and 'about 1.24' are computed (E2, E1); 'one half' is the Remark 3.1 example; 'round' occurs in the quantile-rounding sentences (checked numerically, CF1-c-num-L06-s3-quantile-unrounded). L05 'always' and 'never' occur in the Proposition 2.2 statement, the M2 computed 'never pays back', and misconceptions and distractors that are quoted or labelled as wrong. No banned phrase without a calculation. PASS.",
    "CF1-c-concepts": "check_dag --all PASS (gates_r12.out). L05 defines payback-period once (dfn at L05.html line 58) and uses net-present-value, incremental-cash-flow (L02), present-value, discount-factor, evidence-grade; L06 defines monte-carlo-npv once (dfn at L06.html line 63) and uses net-present-value, present-value, annuity, evidence-grade. Each prerequisite is defined in an earlier lesson or the concept index. PASS.",
    "CF1-c-hours": "data-hours=8 on L05.html and L06.html; index.html line 29 data-hours-lessons=48 and data-hours-project=12; six lessons x 8 h = 48 h; 48 + 12 = 60 module hours; 12/60 = 20.0% (index.html line 41). Consistent. Hours not failed on pace (architect ruling). PASS.",
    "CF1-c-prose-process-path": "Re-scan of L05.html and L06.html learner text and the L05/L06 card objects for process words (build, builder, round as a process word, verifier, unit report, REQUESTS): none in learner text. 'round' appears only in the rounding sentences of L06 Section 3 and misconception 2, which describe numbers. PASS.",
    "CF1-c-cmd-pin": "git rev-parse HEAD in /tmp/verify12-CF1-c: aebdc15b6e2d8f8d3da1ceb0949cb9f2d32dc427 (gates_r12.out).",
    "CF1-c-cmd-check_pages": "tools/check_pages.py --all: 'check_pages CF1: PASS', every unit PASS, exit 0 (gates_r12.out).",
    "CF1-c-cmd-check_dag": "tools/check_dag.py --all: 'check_dag CF1: PASS', exit 0 (gates_r12.out).",
    "CF1-c-cmd-run_labs": "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)', exit 0 (gates_r12.out).",
    "CF1-c-cmd-page_smoke": "tools/page_smoke.py --unit CF1 --pages L05 L06: 'page_smoke modules/CF/CF1/L05.html: PASS' (lab 0.0 s), 'page_smoke modules/CF/CF1/L06.html: PASS' (lab 0.3 s), 'page_smoke CF1: PASS', exit 0 (gates_r12.out).",
    "CF1-c-cmd-ruff-mypy-labs": "ruff check and ruff format --check on the two twins: 'All checks passed!', '2 files already formatted'; mypy --no-incremental on the two twins: 'Success: no issues found in 2 source files'; exit 0 (gates_r12.out).",
    "CF1-c-cmd-pytest-labs": "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: all dots, exit 0 (gates_r12.out).",
    "CF1-c-cmd-verify_refs": "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems'; both exit 0 (gates_r12.out).",
    "CF1-c-cmd-twin-vs-page": "twin_vs_page.py (twin_vs_page.out): the page data-run code equals each twin line for line (after unescaping; only a trailing newline differs), and each pre.expected equals the twin's -I -W error output. Both True.",
    "CF1-c-lab-L05-1-run": "python -I -W error tests/labs/CF1/lab-CF1-L05-1.py: exit 0 (lab-CF1-L05-1.out). A simple 2.750, discounted 3.469; B simple 2.750, discounted none; D simple 2.000; NPV A 289367.40, B -96168.29, D -132231.40; gap 385535.69; one distinct simple and one distinct discounted payback in 1000 tails; tail NPV 121251.71 to 693692.91. Equals the page expected block. PASS.",
    "CF1-c-lab-L06-1-run": "python -I -W error tests/labs/CF1/lab-CF1-L06-1.py: exit 0 (lab-CF1-L06-1.out). Closed forms 79078.68 and 49379.84; n=100 error_in_se +1.242; n=50000 mean 79216.82 (+0.625 se); sd ratio 1.0008; quantiles 14896.62, 79457.94, 143406.13; share 0.0552, se 0.0010. Equals the page expected block. PASS.",
    "CF1-c-twin-freshness": "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py are byte-identical to 91946cf (git diff 91946cf aebdc15 shows no change under tests/labs/CF1); the page code and expected blocks equal the twins run now (twin_vs_page.out). PASS.",
}

NEW = [
    {"id": "CF1-c-num-L06-s3-quantile-unrounded", "check": "2.2-numbers", "location": "L06.html Section 3 paragraph (line 211), quantile sentences",
     "status": "PASS",
     "evidence": "recompute_r12.out: unrounded q10 14896.623057, q50 79457.938852, q90 143406.126569. Unrounded width 128509.503511 rounds to 128509.50 at two decimals; printed width 143406.13 - 14896.62 = 128509.51; printed-minus-unrounded width difference 0.0065 cents, which is 0.01 at two decimals. The lab does not print a width (lab-CF1-L06-1.out). The sentences' claims (unrounded computation, two-decimal printing, 128509.50 from unrounded values, 0.01 rounding difference at printed precision) are true. Advisory only: 'Their difference from the unrounded values is 128509.50 cents' reads more clearly as 'the same difference computed from the unrounded quantiles is 128509.50 cents'. Not a numerical error."},
    {"id": "CF1-c-cards-L05-c102", "check": "2.7-cards", "location": "course/modules/CF/CF1/cards.json card CF1-c102 (lesson L05)",
     "status": "PASS",
     "evidence": "Card: 'In Lab 1, what discounted payback does Project A show at a 10 per cent rate?' back '3.469 years, for SIMULATED flows (Lab 1).' grade C, basis 'Lab 1 (SIMULATED flows)'. lab-CF1-L05-1.out 'discounted_payback 3.469'; recomputed payback of discounted A = 3.469333 (recompute_l05_r12.out). The number appears in L05.html (hypothesis, key results, misconception 2). Grade C matches the SIMULATED lab-result rule. PASS."},
    {"id": "CF1-c-cards-delta-r12", "check": "2.7-cards", "location": "course/modules/CF/CF1/cards.json, 91946cf to aebdc15",
     "status": "PASS",
     "evidence": "cards_delta.py (cards_delta.out): 100 cards before, 103 after; added CF1-c101 (L02), c102 (L05), c103 (L03); changed c027 (L02), c042 (L03), c068 (L05). For this slice only c068 changed and c102 was added. c027, c042, c101, c103 belong to other lessons and are not verified by this slice."},
    {"id": "CF1-c-cards-dupes-r12-cross", "check": "2.7-cards", "location": "course/modules/CF/CF1/cards.json, all 103 cards",
     "status": "PASS",
     "evidence": "card_dupes.py (card_dupes.out): zero exact duplicate fronts and backs. Highest front-similarity pairs: CF1-c042/c103 (0.99, L03, outside this slice; 3 vs 5 per cent inflation) and CF1-c068/c102 (0.92, L05; simple vs discounted payback of A). Each pair asks a different fact with a different back. PASS."},
    {"id": "CF1-c-registry-r12", "check": "2.1-citations", "location": "references/references.json entries graham2001theory and glasserman2003monte; L05.html line 233; L06.html line 106",
     "status": "PASS",
     "evidence": "Registry read: graham2001theory = Graham and Harvey, 'The theory and practice of corporate finance: evidence from the field', J Financial Economics 60(2-3) 187-243 (2001), verified by crossref; the L05 claim 'whose title names corporate finance practice' matches the title. glasserman2003monte = Glasserman, 'Monte Carlo Methods in Financial Engineering' (2003), verified by crossref; L06 Remark 2.4 names it and states no result from it. No passage was read or needed. Registry flag carried below."},
    {"id": "CF1-c-mutants-na-r12", "check": "2.5-labs", "location": "ledgers/CF1/mutants/ (not applicable to slice c)",
     "status": "PASS",
     "evidence": "Slice c is a lesson-and-lab slice, not a project slice; the round-12 brief requires new student-error mutants and alternative implementations for project slices only. Not run for this slice. The mutants committed in ledgers/CF1/mutants/ grade the project graders and are out of scope here."},
]

rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": ("Carried from round 11 (cited lines unchanged since the previous pin 91946cf: course/modules/CF/CF1/L05.html, "
                                  "tests/labs/CF1 twins, course/modules/CF/CF1/index.html, and the L06.html lines outside the aebdc15 hunks at lines 211 and 223): ")
                                  + r["evidence"]})
rows += NEW

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for old in PREV["rows"]:
    assert old["id"] in ids, old["id"]

from datetime import datetime, timezone
fragment = {
    "unit": "CF1",
    "slice": "CF1-c",
    "round": 12,
    "verifier": "independent verifier (Haiku), CF1 slice c (L05, L06 and their lab twins), round 12; did not build CF1; no shared context with builders or earlier verifiers",
    "pin": "aebdc15b6e2d8f8d3da1ceb0949cb9f2d32dc427",
    "base": "91946cfce0c3efe5a3c91215ab7b31faecf53061",
    "checkout": "/tmp/verify12-CF1-c (detached worktree at aebdc15; .venv symlinked)",
    "scratch": "/tmp/cf1-v/CF1-c-r12",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "mutants": [],
    "registry_flags": ["glasserman2003monte: registry used_by is ['M8'] but CF1 L06 cites this key; used_by not updated (generated registry, not edited by the verifier). Not a row failure."],
    "freshness_flags": [],
    "notes": ("Delta from the round-11 pin 91946cf to aebdc15 for this slice: L06.html Section 3 (line 211) and Section 4 intro (line 223); cards.json (CF1-c068 changed, CF1-c102 added; the other card changes and additions belong to L02/L03 and are noted but not verified here). "
              "L05.html, index.html and tests/labs/CF1 twins are byte-identical to 91946cf, so their rows are carried with the stated prefix. "
              "All command rows were re-run on aebdc15 (ledgers/CF1/scripts/CF1-c-r12/gates_r12.out). Mutants: not required for a lesson-and-lab slice (see CF1-c-mutants-na-r12). "
              "Not checked: the passages of Graham and Harvey (2001) and Glasserman (2003) were not read (no publisher access attempted), so no passage-level claim is verified; the pages make none beyond the registry record. "
              "Hours not failed on pace (architect ruling). The whole-page structure rows rest on a full re-read of L06 and of L05 in this round."),
    "summary": "CF1-c round 12: rows %d (pass %d, fail 0, unverifiable 0). The round-11 FAIL (L06 Section 4 intro) is fixed and re-verified. The changed L06 Section 3 quantile sentences and the changed card CF1-c068 are verified; new card CF1-c102 is verified." % (len(rows), len(rows)),
    "rows": rows,
}
out = CHECKOUT / "ledgers/CF1/CF1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows")
