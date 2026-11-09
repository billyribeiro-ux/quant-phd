"""Build ledgers/LX2/LX2-c.json for the LX2-c closing delta (round 1) from the base fragment.

Base: /Users/billyribeiro/.fanout/frags/F3-LX2-c.round1.json (pin 95f3f8cb). Rows are carried with the carry prefix
unless listed in REVERIFIED, whose evidence is rewritten from this round's commands. Mutant verdicts come from the
standing-set re-run (closing_out/standing_mutants_lab2.txt); descriptions are the base's.
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
BASE = Path("/Users/billyribeiro/.fanout/frags/F3-LX2-c.round1.json")
OUT = ROOT / "ledgers/LX2/scripts/LX2-c-r1/closing_out"
base = json.loads(BASE.read_text(encoding="utf-8"))

CARRY = (
    "Carried from round 1 (cited lines and files byte-identical since the previous pin 95f3f8cb; the delta changes "
    "project.html only at lines 363 and 535, and no other cited file): "
)

REVERIFIED: dict[str, str] = {
    "proj-gates-tooling": (
        "Re-run at 2a805c83 (closing_out/): check_pages --unit LX2 'PASS'; check_projects --unit LX2 'PASS'; "
        "check_dag --unit LX2 'PASS'; page_smoke --unit LX2 --pages project 'page_smoke modules/LX/LX2/project.html: PASS'; "
        "run_labs --unit LX2 'PASS (7/7)'; run_graders --unit LX2 'no autograder (grading: rubric)'; verify_refs --offline "
        "'offline integrity: 560 entries, 0 problems'; ruff check and ruff format --check on tests/labs/LX2 and "
        "tests/test_labs.py 'All checks passed!' / '7 files already formatted'; pytest -k 'LX2 or project or lab' over "
        "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py rc 0; twins alone under python -I -W error rc 0 "
        "for -1, -2, -3. Repo-wide ruff/mypy not re-run: no .py under LX2 changed (delta .py changes are LX1, E4, M3)."
    ),
    "proj-page-smoke": (
        "Re-run at 2a805c83: tools/page_smoke.py --unit LX2 --pages project -> 'page_smoke modules/LX/LX2/project.html: PASS' "
        "(closing_out/page_smoke_project.txt)."
    ),
    "proj-rung2-table-wrong-blank-claim": (
        "Re-verified from scratch at 2a805c83. Line 535 now reads: 'Two blanks; the check compares the printed output only, so a "
        "wrong expression that prints the same block passes (see the rung 2 note).' Checked against the page and the code: "
        "(a) line 45 (ladder rung 2): 'compares the printed output only'; (b) line 241 hypothesis: 'a blank typed as the value it "
        "prints passes too'; (c) line 332 interpretation: 'a blank typed as 0.6667 or 0.1667 prints the same block and passes'. "
        "(d) labs.js lines 133-138: completion problems are graded by compareOutput on stdout only. (e) Run by "
        "closing_out/rung2_check.txt (scripts/LX2-c-r1/closing_rung2_check.py, page code with the two code blanks filled, run "
        "under python -I -W error): 'page_completed_solution ... PASSES'; 'wrong_hardcoded_same_block: hit=Fraction(4, 6) "
        "bias=Fraction(1, 6) -> PASSES' (a wrong expression that prints the same block); 'wrong_hit_count_over_8 ... FAILS token "
        "70: 0.5000 vs 0.6667'; 'wrong_mean_abs_error ... FAILS token 74: 2.8333 vs 0.1667' (the page's two named examples). "
        "The table has two blanks (lines 241, 321-331). The cell's arithmetic is unchanged. The base defect is cured."
    ),
    "proj-source-supersession": (
        "Re-verified at 2a805c83. Line 363 now reads 'under the heading \"Supersedes:\"' (base had 'Supersedes.'). The source "
        "heading is 'Supersedes:' (SR 26-2 PDF text, /tmp/lx2c-r1-src-closing/combined.txt line 57, after the signature block "
        "'Randall D. Guynn / Director / Attachment:' block; htm line 1469 'Supersedes:'). The list under it names SR letter 11-7 and SR "
        "letter 21-8, so the sentence is true. The cover-letter sentence at line 363 ('which supersedes and replaces SR letter "
        "11-7 and SR letter 21-8') matches combined.txt lines 30-31 and htm line 1444. Fresh fetch: plain curl of "
        "https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm into /tmp/lx2c-r1-closing-fetch/ (sha256 "
        "b146339b...); its text equals the base scratch copy except a Cloudflare challenge-script nonce (a line of inline script)."
    ),
    "proj-source-applicability": (
        "Re-verified at 2a805c83 (line 364 unchanged). Applicability sentence: htm line 1440 and combined.txt lines 24-25 read "
        "'This letter is expected to be most relevant to banking organizations with over $30 billion in total assets regulated "
        "by the Federal Reserve.'; the span's paraphrase matches."
    ),
    "proj-source-attachment": (
        "Re-verified at 2a805c83: lines 347-360 unchanged; line 363 changed only in 'Supersedes:' (checked above). "
        "scripts/LX2-c-r1/closing_quote_check.py -> closing_out/quote_check.txt: all five attachment quotes at lines 350-353 "
        "and 364 are present in the SR2602.pdf text (pdf=Y for the five quotes, including 'This guidance does not set forth "
        "enforceable standards or prescriptive requirements')."
    ),
    "proj-claim-span-paraphrase": (
        "Re-verified at 2a805c83 (line 363 changed in one word). The span paraphrases the cover letter (combined.txt lines "
        "28-31: 'The Board of Governors ... the agencies are issuing the attached Revised Guidance ... which supersedes and "
        "replaces SR letter 11-7 ... and SR letter 21-8'); the paraphrase is not quoted and carries data-grade C with a locator. "
        "Content checked against combined.txt lines 28-31 and htm line 1444; no change in meaning."
    ),
    "proj-r8-delta-read": (
        "Re-verified at 2a805c83: the two lines the r8 row cites are 55 (unchanged) and 363 (changed; checked above). "
        "Hunk analysis: the 2 changed lines are 363 and 535 (git diff -U0 95f3f8cb..2a805c83); their digits are identical "
        "to the base lines (see proj-prose-numbers-rederived)."
    ),
    "r12-cover-letter-sentences": (
        "Re-verified at 2a805c83: line 363 (checked above: heading 'Supersedes:' and the supersession sentence); line 364 "
        "(Applicability sentence, htm line 1440, combined.txt lines 24-25); line 622 unchanged, span text checked in "
        "closing_quote_check.py (its cover-letter paraphrase 'the cover letter of sr 26-2 states that the revised guidance "
        "supersedes and replaces sr letter 11-7 and sr letter 21-8' is consistent with combined.txt lines 30-31). "
        "closing_out/quote_check.txt."
    ),
    "proj-rung3-sr26-standard": (
        "Re-verified at 2a805c83 (lines 347-360 and 363-367 include the changed line 363): attachment quotes present in "
        "SR2602.pdf (closing_out/quote_check.txt); the 'not stated here' statements and the attachment page numbers are "
        "unchanged; the source sentence at 363 was re-checked (heading 'Supersedes:')."
    ),
    "proj-r10-sources-refetch": (
        "Re-verified at 2a805c83. references/references.json frb2026fed url "
        "https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm; plain curl into /tmp/lx2c-r1-closing-fetch/ "
        "exits 0 and serves the page; the sentences cited at lines 363-364 are present (htm line 1444 supersession, 1440 applicability, "
        "1469 'Supersedes:'). The sha256 differs from the base scratch (d7ef6c9a... vs b146339b...) only by a Cloudflare nonce "
        "in an inline script (diff run this round); the page carries a challenge script but is served in full; no bypass was attempted."
    ),
    "proj-attachment-quote-locators": (
        "Re-verified at 2a805c83: spans at lines 350-353 and the quote at 364 are present in SR2602.pdf text (closing_out/quote_check.txt, pdf=Y); line 363 "
        "changed in one word (checked above). Lines 622 (paraphrases of the cover letter, consistent with combined.txt lines 24-31) "
        "and 686 (exemplar B sentence, which the C5 annotation at line 691 marks as an unread requirement; carried row "
        "proj-exemplar-b-unread-requirement) are unchanged."
    ),
    "proj-hours": (
        "Re-verified at 2a805c83: table#hours (lines 531-545) components 2, 2, 2, 3, 3, 2 sum to 14 (python recompute); "
        "the total cell is 14; the hub index.html line 175-176: 'the project is 14 hours, which is 28 percent of the 50-hour "
        "module' and line 31 'Tier U · 50 hours'; 14/50 = 28%. Only the rationale text of row 2 changed (line 535)."
    ),
    "proj-delta-time-budget": (
        "Re-verified at 2a805c83: the hours cell at line 535 is the changed line; its new rationale 'the check compares the "
        "printed output only, so a wrong expression that prints the same block passes (see the rung 2 note)' is true on the "
        "page's own lab 2 (closing_out/rung2_check.txt). Components and total unchanged (14)."
    ),
    "proj-hours-independent-estimate": (
        "Re-verified at 2a805c83: hours values in table#hours unchanged (2, 2, 2, 3, 3, 2 = 14); only row 2's rationale text "
        "changed (line 535). The independent-estimate judgment rests on the hours values, which are byte-identical in "
        "meaning; no new estimate was made."
    ),
    "r12-hours-independent-estimate": (
        "Re-verified at 2a805c83: lines 531-543 hours values unchanged (sum 14); only line 535's rationale changed; judgment "
        "carried on the same values."
    ),
    "proj-banned-and-process-words": (
        "Re-verified at 2a805c83: check_pages --unit LX2 PASS (banned strings in visible prose, outside code and math). Changed "
        "lines 363 and 535 contain no process words (round, delta, verifier, fix, ledger, closing, mutant); checked by "
        "regex on the hunks."
    ),
    "r12-banned-and-process-words": (
        "Re-verified at 2a805c83: check_pages --unit LX2 PASS; the changed lines 363 and 535 have no process words (hunk "
        "regex check)."
    ),
    "proj-scope-words": (
        "Re-verified at 2a805c83: the changed line 535 contains 'only' and 'same'. 'Only': the check compares the printed output "
        "only (labs.js lines 133-138 grade completion problems on stdout; rung 2 text line 45). 'Same': a wrong expression prints "
        "the same block (closing_out/rung2_check.txt, Fraction(4, 6) and Fraction(1, 6) pass). Both computed. Line 363 is "
        "the only other changed line; its word 'Supersedes:' contains no scope word."
    ),
    "proj-prose-numbers-rederived": (
        "Re-verified at 2a805c83: the changed lines 363 and 535 contain the same digits as the base lines (line 363: 26, 2, "
        "17, 2026, 11, 7, 21, 8, 11, 7; line 535: 2, 2). No number in the page changed. The rest of the numeric prose is in "
        "cited lines that are byte-identical (see carried rows); r10 and r12 rederive rows carried."
    ),
    "proj-counter-evidence-c-grade": (
        "Re-verified at 2a805c83: data-grade=\"C\" count in project.html is 12 (grep -c, 12 occurrences); the 12 frb2026fed "
        "claim spans are unchanged (the line 363 change is outside the span)."
    ),
    "proj-notation": (
        "Re-verified at 2a805c83: inline \\( ... \\) spans count 65 at both 95f3f8cb and 2a805c83 (grep -o); neither changed "
        "line contains math delimiters (hunk check). Notation unchanged."
    ),
    "r12-notation": (
        "Re-verified at 2a805c83: 65 inline math spans at both pins; changed lines 363 and 535 contain no math."
    ),
    "proj-dag-and-links": (
        "Re-verified at 2a805c83: check_dag --unit LX2 PASS; changed lines 363 and 535 contain no href, anchor, dfn or concept "
        "link (hunk check)."
    ),
    "proj-anchors-links": (
        "Re-verified at 2a805c83: check_pages --unit LX2 PASS (internal links and ids); changed lines add no href or id."
    ),
    "proj-data-and-figures-na": (
        "Re-verified at 2a805c83: the changed lines contain no img, svg, figure or data-files attribute (hunk check)."
    ),
    "proj-define-model-owner": (
        "Re-verified at 2a805c83: check_dag --unit LX2 PASS; the changed lines contain no dfn (hunk check)."
    ),
    "proj-studio-na": (
        "Re-verified at 2a805c83: check_projects --unit LX2 PASS (rung 3 and the grading mode of a project page)."
    ),
    "proj-atlas-na": (
        "Re-verified at 2a805c83: check_projects --unit LX2 PASS; the spec (Context, Constraints) is byte-identical (lines 337-358 "
        "not in the delta)."
    ),
    "proj-adversarial-na": (
        "Re-verified at 2a805c83: check_projects --unit LX2 PASS; line 357 is byte-identical."
    ),
    "proj-pytest-lx2": (
        "Re-run at 2a805c83: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'LX2 or project or lab' "
        "rc 0; no failure output."
    ),
    "proj-mutate-graders-na": (
        "Re-run at 2a805c83: tools/mutate_graders.py --unit LX2 printed nothing and exited 0 (closing_out/mutate_graders_LX2.txt); "
        "run_graders --unit LX2 'no autograder (grading: rubric)'."
    ),
    "proj-labs-twins-alone": (
        "Re-run at 2a805c83: tests/labs/LX2/lab-LX2-project-1.py, -2.py, -3.py under python -I -W error: rc 0 each. The "
        "twins are byte-identical (no LX2 twin in the delta)."
    ),
    "r12-gates-pages-dag-projects-labs": (
        "Re-run at 2a805c83: check_pages --unit LX2 PASS; check_dag --unit LX2 PASS; check_projects --unit LX2 PASS; run_labs "
        "--unit LX2 PASS (7/7) (closing_out/)."
    ),
    "r12-page-smoke-project": (
        "Re-run at 2a805c83: page_smoke --unit LX2 --pages project PASS (closing_out/page_smoke_project.txt)."
    ),
    "r12-twins-alone": (
        "Re-run at 2a805c83: the three LX2 project twins under python -I -W error rc 0 each."
    ),
    "r12-run-graders-mutate": (
        "Re-run at 2a805c83: run_graders --unit LX2 -> 'no autograder (grading: rubric)' rc 0; mutate_graders --unit LX2 rc 0, "
        "no output (closing_out/run_graders_LX2.txt, mutate_graders_LX2.txt)."
    ),
    "r12-verify-refs": (
        "Re-run at 2a805c83: verify_refs --offline -> 'offline integrity: 560 entries, 0 problems' rc 0. The live run "
        "(verify_refs --unit LX2 is a live-only mode; not repeated this round) is carried from the base round and not "
        "independently re-run here."
    ),
    "r12-ruff-mypy-pytest": (
        "Re-run at 2a805c83: ruff check and ruff format --check on tests/labs/LX2 and tests/test_labs.py clean; pytest subset "
        "rc 0. Repo-wide mypy and ruff not re-run (no LX2 .py changed; the delta's .py changes are LX1, E4 and M3)."
    ),
    "r12-delta-scope": (
        "Re-verified at 2a805c83: git diff --stat 95f3f8cb..2a805c83 over course/modules/LX/LX2, tests/labs/LX2, labs.js, "
        "tools, notation, references: course/modules/LX/LX2/project.html (lines 363, 535) and course/modules/LX/LX2/cards.json "
        "(see notes). No labs.js, tools, twin or reference change."
    ),
    "r12-attachment-quotes": (
        "Re-verified at 2a805c83: lines 350-353 and 364 quotes present in SR2602.pdf text (closing_out/quote_check.txt); "
        "printed-page locators unchanged."
    ),
    "r12-mutants-existing-rerun": (
        "Re-run at 2a805c83: scripts/LX2-c-r1/lab2_harness_r1.py over ledgers/LX2/mutants/*lab2*.py (62 files): 'KILLED 46 "
        "SURVIVED 16' (closing_out/standing_mutants_lab2.txt); identical to the base round."
    ),
    "proj-rung2-instant-check-mutants": (
        "Re-run at 2a805c83: the standing set (62 lab-2 files) gives KILLED 46, identical to the base; the 46 kills are "
        "compare failures on the printed block (no run exited non-zero) (closing_out/standing_mutants_lab2.txt). Lines 45 and 332 unchanged."
    ),
    "proj-rung2-student-error-mutants": (
        "Re-run at 2a805c83: standing set rerun (closing_out/standing_mutants_lab2.txt); the 9 student-error survivors are "
        "the base's 9 (r10_lab2_bias_absolute_error_sum, r10_lab2_bias_absolute_value_of_sum_per_H, r10_lab2_hit_band_three, "
        "r6_lab2_float_format_ties_even, r6_lab2_hard_coded_printed_values, r6_lab2_round_half_even_ties, "
        "r6_lab2_round_half_toward_plus_infinity, r7_lab2_rounds_through_python_round, r8_lab2_hit_rate_ceiling_four_places); "
        "their survival is the disclosed printed-output-only limit (lines 45 and 332), carried from the base."
    ),
    "proj-rung2-alternatives": (
        "Re-run at 2a805c83: the seven correct alternatives survive (over-constraint check passes): alt-lab2-float-division, "
        "alt_r10_lab2_decimal_half_up_quantize, alt_r10_lab2_squared_error_band, alt_r12_lab2_bias_sum_over_len, "
        "alt_r12_lab2_hit_rate_generator_sum, alt_r12_lab2_statistics_fmean_bias, alt_r9_lab2_fmean_bias_error_list_hits "
        "(closing_out/standing_mutants_lab2.txt)."
    ),
    "r12-alternatives-new": (
        "Re-run at 2a805c83: alt_r12_lab2_bias_sum_over_len, alt_r12_lab2_hit_rate_generator_sum, "
        "alt_r12_lab2_statistics_fmean_bias all SURVIVE (correct alternatives) (closing_out/standing_mutants_lab2.txt)."
    ),
    "r12-mutants-new-student-error": (
        "Re-run at 2a805c83: the four r12_lab2 student-error mutants are all KILLED (r12_lab2_bias_uses_mean_realised_value, "
        "r12_lab2_hit_count_adds_edge_months, r12_lab2_hit_count_counts_only_upper_side, "
        "r12_lab2_hit_rate_denominator_excludes_edge_months) (closing_out/standing_mutants_lab2.txt)."
    ),
}

# Rows re-verified above are rewritten; the others are carried (the calibration rows included: no LX2 blind scorer exists).
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in REVERIFIED:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": REVERIFIED[rid]})
    else:
        ev = r["evidence"]
        if r["status"] != "PASS":
            raise SystemExit(f"non-PASS base row not re-verified: {rid}")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": CARRY + ev})

# Mutants: base descriptions, verdicts from the standing-set re-run.
harness: dict[str, str] = {}
for line in (OUT / "standing_mutants_lab2.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVES)\s+(\S+)\s*(.*)$", line)
    if m:
        harness[m.group(2)] = (m.group(1), m.group(3).strip())
mutants = []
for m in base["mutants"]:
    name = m["name"]
    status, detail = harness[name]
    if status == "KILLED":
        killed_by = f"KILLED by the closing re-run (closing_out/standing_mutants_lab2.txt): {detail}"
    else:
        killed_by = f"SURVIVES (re-run at 2a805c83, closing_out/standing_mutants_lab2.txt): {m['killed_by'].split(':', 1)[-1].strip()}"
    mutants.append({"name": name, "description": m["description"], "killed_by": killed_by})

sr_note = (
    "sr2602.htm sha256 b146339b... on the closing fetch vs d7ef6c9a... in the base scratch: the difference is one Cloudflare "
    "challenge-script nonce (a line of inline script); the text cited is identical."
)
notes = [
    "Verdict PASS. The base FAIL row proj-rung2-table-wrong-blank-claim (project.html line 535) is cured: the cell now states the "
    "compare rule that the page and labs.js state, and the wrong-expression claim was run (closing_out/rung2_check.txt). "
    "No ruling-26 defect was found in the delta hunks.",
    "Delta: git diff 95f3f8cb..2a805c83 touches two LX2 slice files: course/modules/LX/LX2/project.html (lines 363 and 535, one "
    "word each: 'Supersedes.'->'Supersedes:' and the rung 2 hours cell) and course/modules/LX/LX2/cards.json (LX2-c065, c081, c088 "
    "back text reworded to cite Section 1/2; new LX2-c107, c108, c109 for L03). The cards are not in slice c's base scope "
    "(the base scope covers the project page, twins, graders and mutants); they are L03/L04 cards and must be covered by the "
    "lesson-slice closing deltas (slices a and b). Not checked here.",
    "Other deltas in the commit range do not touch LX2 (LX1 cards/L01/L02/project, E4 and M3 twins, tests/test_lx1_project_lab3.py, "
    "plans/FINAL-ARCHITECT-RULINGS.md rulings 38-39). labs.js, tools/, tests/labs/LX2, ledgers/LX2/mutants and references.json "
    "are byte-identical across the delta.",
    "Mutants: no new mutants written (ruling 37). Standing set re-run (62 files): KILLED 46, SURVIVED 16 (7 correct alternatives, 9 "
    "disclosed printed-output-only student-error survivors), identical to the base. The 9 survivors' judgment (lines 45 and 332) "
    "is carried; they are not re-litigated here.",
    "Calibration (ruling 23): no LX2 blind scorer exists in ~/.fanout/blind/ (files present: BK4, CS2, E1, E3, E4, FC2, LX1, M5, "
    "PC3). The base calibration rows (proj-exemplar-calibration, proj-r9-blind-exemplars, r12-blind-exemplar-scoring) are "
    "carried, with the base's caveat.",
    "Observation (LOW, not a row): the new cell cites '(see the rung 2 note)'. The page has no heading named 'rung 2 note'; the "
    "nearest matching text is the rung 2 ladder item (line 45) and the lab 2 interpretation (line 332). Both state the rule.",
    "Not checked this round: verify_refs live run (carried); browser run of the self-assessment form; repo-wide ruff/mypy (no "
    "LX2 .py changed); lesson pages, cards and twins of L01-L04 (other slices); no new defect hunting outside the listed rows "
    "(ruling 30).",
    sr_note,
]

fragment = {
    "unit": "LX2",
    "slice": "LX2-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-c, closing delta round 1 (did not build LX2)",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": (
        "F3-LX2-c.round1.json (pin 95f3f8cb21c2cd9fc904430bd30a6b734d01f672, verdict FAIL, 102 rows: 101 PASS, 1 FAIL "
        "proj-rung2-table-wrong-blank-claim). Delta 95f3f8cb..2a805c83."
    ),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-LX2-c (detached at 2a805c83; .venv symlinked)",
    "scratch": "/tmp/lx2c-r1-src-closing (base copies of SR2602.pdf, SR2602a1.pdf, sr2602.htm, a1.txt, combined.txt); "
    "/tmp/lx2c-r1-closing-fetch (fresh plain-curl copy of sr2602.htm)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "sr2602.htm sha256 changed again on 2026-11-09 (base scratch d7ef6c9a...; fresh fetch b146339b...); the only difference is a "
        "Cloudflare challenge-script nonce. The cited sentences and 'Supersedes:' heading are present in both. Scratch PDF "
        "sha256 (not compared with a recorded value this round): SR2602a1.pdf 209ce4c1..., SR2602.pdf 956b3bc6....",
    ],
    "notes": notes,
    "summary": (
        f"LX2-c closing delta round 1: PASS. Rows {len(rows)}: PASS {len(rows)}, FAIL 0. Re-verified this round: {len(REVERIFIED)} "
        f"rows; carried: {len(rows) - len(REVERIFIED)} rows. Mutants: 62 standing lab-2 files, KILLED 46, SURVIVED 16 (7 correct "
        "alternatives, 9 disclosed student-error survivors); none new."
    ),
}
(ROOT / "ledgers/LX2/LX2-c.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "reverified", len(REVERIFIED), "mutants", len(mutants))
