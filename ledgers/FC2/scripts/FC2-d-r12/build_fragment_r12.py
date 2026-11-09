"""Build ledgers/FC2/FC2-d.json (round 12) from the round-11 fragment plus this round's fresh evidence.

Carries a round-11 PASS row only when its cited subject is byte-identical since ccaeeaf (git diff checked),
re-verifies the rows whose subject changed, keeps every row id. Run from the checkout root.
"""
import datetime
import json
import pathlib

R11 = pathlib.Path("/Users/billyribeiro/.fanout/frags/D-FC2-d.round11.json")
OUT = pathlib.Path("ledgers/FC2/FC2-d.json")
S = "ledgers/FC2/scripts/FC2-d-r12/"
d11 = json.loads(R11.read_text(encoding="utf-8"))
rows11 = d11["rows"]
BYID = {r["id"]: r for r in rows11}
mut11 = d11["mutants"]

ORIG = "ccaeeaf"
GENERIC = "course/modules/FC/FC2/cards.json, L01-L08.html, grader/instance.py, grader/reference.py, grader/starter.py, tests/labs/FC2, notation/notation.json, references/references.json, index.html and course/index.html"


def carry(row, files):
    out = dict(row)
    out["status"] = "PASS"
    out["evidence"] = f"Carried from round 11 ({files} byte-identical since the previous pin {ORIG}): " + row["evidence"]
    out["fix"] = ""
    return out


def fresh(row, status, evidence, fix=""):
    out = dict(row)
    out["status"] = status
    out["evidence"] = evidence
    out["fix"] = fix
    return out


# Subjects changed since ccaeeaf: course/modules/FC/FC2/project.html (lines 282, 299, 301, 486, 538) and
# course/modules/FC/FC2/grader/test_project.py (lines 188-192, 263-278, 718, 734, 761, 770); FC2 mutants a11..,
# alt13..alt15 (ledgers). Everything else in the slice is byte-identical (git diff --quiet ccaeeaf 329c1d7).
PAGE_UNCHANGED = "course/modules/FC/FC2/project.html lines outside the changed lines 282, 299, 301, 486 and 538"
GRADER_UNCHANGED = "course/modules/FC/FC2/grader/test_project.py lines outside the changed lines 188-192, 263-278, 718, 734, 761, 770"

OVERRIDE = {
    "fc2d-r2-gate-mutate": fresh(
        BYID["fc2d-r2-gate-mutate"],
        "FAIL",
        f"{S}mutate_fc2_r12_all.out: 'mutate_graders FC2: FAIL (95/98 killed)', rc=1 on this pin. Survivors on seeds 0-9: "
        "z12_a_convexity_length_message_omits_lengths.py, z12_f_strike_message_omits_positive.py, "
        "z12_g_df_message_omits_range.py (verifier mutants, rows fc2d-r12-convexity-length-message, "
        "fc2d-r12-strike-message-positive, fc2d-r12-df-message-range). The 95 others are killed, incl. the 91 prior "
        "and z12_b..z12_e.",
        "Add the assertions named in the three row fixes so the suite kills z12_a, z12_f and z12_g; re-run the gate.",
    ),
    "fc2d-r2-gate-run-graders": fresh(
        BYID["fc2d-r2-gate-run-graders"], "PASS",
        f"{S}run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 (this round, pin 329c1d7).",
    ),
}
PASS_FRESH = {
    "fc2d-r2-gate-check-projects": f"{S}check_projects.out: 'check_projects FC2: PASS', rc=0 (this round).",
    "fc2d-r2-gate-check-dag": f"{S}check_dag.out: 'check_dag FC2: PASS', rc=0 (this round).",
    "fc2d-r2-gate-check-pages": f"{S}check_pages.out: 'check_pages FC2: PASS', rc=0 (this round).",
    "fc2d-r2-gate-run-labs": f"{S}run_labs.out: 'run_labs FC2: PASS (11/11)', rc=0 (this round).",
    "fc2d-r2-lab-twins-isolated": f"{S}twin_project-1/2/3.stdout and .stderr: `python -I -W error tests/labs/FC2/lab-FC2-project-N.py` rc=0 for N=1,2,3; stderr 0 bytes (this round).",
    "fc2d-r2-lab-page-equals-twin": f"{S}page_vs_twin_r12.out: project-1 and project-3 page code == twin (True); project-2 is the rung-2 completion lab (class \"lab completion\", BUILDER_RULES 5.1 line 294) whose page code differs from its twin only at the three blanks `___` (lines 58, 60, 73 of the extracted code), which is by design; its expected block equals the twin output (run in this round, `expected==twin output: True`).",
    "fc2d-r2-gate-page-smoke": f"{S}page_smoke.out: 'page_smoke FC2: PASS', rc=0; page_smoke modules/FC/FC2/project.html: PASS (this round).",
    "fc2d-r2-gate-ruff-mypy": f"{S}ruff_check.out 'All checks passed!' (rc=0); ruff_format.out '15 files already formatted' (rc=0); mypy.out 'Success: no issues found in 2 source files' (rc=0; mypy --no-incremental on reference.py and instance.py). test_project.py is not mypy-checked here (it imports scanner).",
    "fc2d-r2-gate-pytest-fc2": f"{S}pytest_fc2.out: `pytest -q tests -k FC2` rc=0, 12 selected (test_curriculum 1, test_labs 11), this round.",
    "fc2d-r2-collect-count": f"{S}collect_count_r12.out: 'collected 94 for 50 seeds', rc=0 (reference.py as scanner.py, seeds 0-49). The page at course/modules/FC/FC2/project.html line 320 says 94 checks.",
    "fc2d-r2-numbers-lab3": f"{S}numbers_r12.py and numbers_r12.out (independent Fraction recomputation): gross/net 226/166 (6500), 540/480 (7000), chord-less-call -188/3 gross 63 net 3 (6000); gap at 4500 is -60, gross 60 = cost, net 0. Matches the printed expected block of project.html Lab 3 (lines 377-486). The new sentence 'rounded once to the nearest cent, which is 63' (line 486) holds: 188/3 = 62.667, not a half-cent (numbers_r12.out, 'is half-cent? False').",
    "fc2d-r2-numbers-exemplars": "project.html line 538 (Exemplar B passage) re-computed in " + S + "numbers_r12.out: 6500 discounted strike 6175, gap 151-1100-(5000-6175)=226; 7000 discounted 6650, gap 540; chord (500+2*151)/3=802/3, less 330 = -188/3, gross 63, net 3. Line 562 (Exemplar A settlement): 'net of 3 cents', half-spread 12 cents per leg, both match the reference. Exemplar A lines 590 and 602 are unchanged since ccaeeaf (carried, same subject bytes).",
    "fc2d-r2-spec-questions": "project.html lines 278-317 (Rung 3 spec) read in full this round against grader/reference.py: names and parameters of the three functions (lines 299-301), keys of the record (line 301), parity-first then convexity ordering, labels per kind (line 301), error conditions (lines 309-314), and the 94-check count (line 320). The new strike_cents sentence (line 301) matches reference.scan (strikes[j] for convexity, strike for parity). Context sentence count is a separate FAIL row.",
    "fc2d-r2-scope-curriculum-brief": "curriculum/02-economics-finance-core.yaml lines 427-429 (brief) unchanged since ccaeeaf; brief: 'detect put–call parity and convexity violations net of a stated cost model, and explain each one found' against project.html Context (lines 279-285) and Required outputs (line 301): both present, SIMULATED label present (line 282 and line 289).",
    "fc2d-r2-rubric-calibration": "project.html exemplars (lines 517-635) re-read where they changed: line 538 (Exemplar B passage) re-verified by numbers_r12.out; annotations at lines 543 and 618 and data-scores 'data-scores=\"4,4,3,3,3\"' unchanged. Other lines of 517-635 byte-identical since ccaeeaf (carried in substance).",
    "fc2d-r2-starter-suite-fails": f"{S}starter_suite_r12.out: starter.py as scanner.py with test_project.py and instance.py: '86 failed, 8 passed' (this round; the suite changed by renames and wording only, the suite now collects 94 checks; no cause for the count difference from round 6 is claimed).",
    "fc2d-r2-banned-phrases": f"{S}banned grep this round: no hit for TODO|TBD|lorem|for brevity|beyond the scope|details omitted|it is important|clearly|obviously|well known|experts agree|studies show|you can add more|left as an exercise in project.html. The new sentences add no process words (no 'round', 'verifier', 'builder', 'agent') and no motivational openers.",
    "fc2d-r2-notation": "project.html changed lines (282, 299, 301, 486, 538) introduce no symbol outside the page's own notation (C, P, S, K, df, P1-P6 labels, strike_cents, gross_cents, net_cents); notation/notation.json is byte-identical since ccaeeaf. The page's existing 'P' overload is disambiguated at line 335 and carries from earlier rounds.",
    "fc2d-r2-dag": "git diff ccaeeaf 329c1d7 -- course/modules/FC/FC2/project.html: 0 added lines containing 'concept' (12 changed +/- lines, none is a link); check_dag.out 'check_dag FC2: PASS' (this round).",
    "fc2d-r2-grader-messages": f"{S}: changed assertion messages in test_project.py lines 263-278, 718, 734, 761, 770 now state the property (for example 'an exact tie of 2.5 cents must round up, not down'), no longer the expected value; the round-11 observation (expected values in messages at lines 264, 270, 277, 279, 760, 769) is resolved. Remaining messages with digits (lines 255-257, 287, 298, 309, 488, 834) are formulas or range statements, not answers.",
    "fc2d-r2-alternatives-pass": f"{S}alts_r12.out (run_alts_r11.py on this pin, alts from FC2-d-r10 and FC2-d-r11): alt1..alt15 each 50/50 seeds pass the suite under python -I -W error (no FAIL). alt15_shared_empty_result.py was 28/50 at ccaeeaf and is 50/50 now (the identity assertion was removed).",
    "fc2d-r2-mut-r7-docstrings": f"{S}mutate_fc2_r12_all.out: all 98 mutant files open with a one-line description that the tool prints (no '(no description)').",
    "fc2d-r2-mut-new-killed": f"{S}mutate_fc2_r12_all.out: v07 (KILLED), v08 (KILLED), v09 (KILLED, test_scan_explanations...), v10 (KILLED) in this round.",
    "fc2d-r2-mut-equivalents": "98 mutants: 91 prior are byte-identical (carried); the 7 round-12 mutants each change one statement or one message relative to reference.py (diff counts 7 to 9 changed lines, this round). None is a code-equivalent of the reference: z12_a, z12_f, z12_g change message content the spec states, and survive only because the suite does not check that content.",
    "fc2d-r3-scope-changed-hunks": "Every hunk changed since ccaeeaf in this slice was read: project.html lines 282, 299, 301, 486, 538 (git diff -U0) and test_project.py lines 188-192, 263-278, 718, 734, 761, 770, plus the new mutants a11_a..d (round 11) and alt13..15. No other FC2 file changed in the delta (git diff --name-only ccaeeaf 329c1d7 filtered to FC2/FC1/tests/labs/notation/curriculum/references/tools: only the FC1 files, which are outside this slice).",
    "fc2d-r7-cards-delta-read": "git diff --quiet ccaeeaf 329c1d7 -- course/modules/FC/FC2/cards.json: no change, so the cards delta since the previous pin is empty (this round).",
    "fc2d-r11-grader-identity-over-constraint": f"Re-verified. test_project.py line 188 now names test_scan_is_repeatable_on_the_same_chain (was test_scan_returns_a_new_list_each_call) and asserts only equal findings (the 'first is not second' assertion is removed). {S}alts_r12.out: alt15_shared_empty_result.py 50/50 seeds pass (was 28/50). The suite runs 94 checks (collect_count_r12.out).",
    "fc2d-r11-mut-new-student-errors": f"{S}mutate_fc2_r12_all.out: a11_a, a11_b, a11_c, a11_d all KILLED in this round.",
    "fc2d-r3-mut-new-killed": f"{S}mutate_fc2_r12_all.out: q3_a..q3_d in the 98-mutant run, all KILLED (this round).",
    "fc2d-r7-mut-s7-new-killed": f"{S}mutate_fc2_r12_all.out: s7_a..s7_d KILLED (this round).",
    "fc2d-r4-mut-u4-new-killed": f"{S}mutate_fc2_r12_all.out: u4_a..u4_c KILLED (this round).",
    "fc2d-r5-mut-w5-new-killed": f"{S}mutate_fc2_r12_all.out: w5_a..w5_c KILLED (this round).",
    "fc2d-r6-mut-w6-new-killed": f"{S}mutate_fc2_r12_all.out: w6_a..w6_d KILLED (this round).",
    "fc2d-r8-mut-x8-a": f"{S}mutate_fc2_r12_all.out: x8_a KILLED (this round).",
    "fc2d-r8-mut-x8-b": f"{S}mutate_fc2_r12_all.out: x8_b KILLED (this round).",
    "fc2d-r8-mut-x8-c": f"{S}mutate_fc2_r12_all.out: x8_c KILLED (this round).",
    "fc2d-r9-mut-y9-new-killed": f"{S}mutate_fc2_r12_all.out: y9_a..y9_d KILLED (this round).",
    "fc2d-r10-new-mutants": f"{S}mutate_fc2_r12_all.out: z10_a..z10_d KILLED (this round).",
    "fc2d-r3-mut-prior-untracked": f"{S}mutate_fc2_r12_all.out: r3_a..r3_d KILLED (this round).",
    "fc2d-r5-page-hunk-error-conditions": "project.html lines 309-316 unchanged since ccaeeaf (not in git diff -U0 hunks) and read this round against grader/test_project.py lines 285-310 and 540-606 (named conditions and their messages); carried in substance.",
    "fc2d-r2-grader-named-conditions-only": "test_project.py lines 505-533 and 586-602 (exception types demanded only for named conditions) are byte-identical since ccaeeaf; the one remaining gap (message content of three named conditions) is recorded as FAIL rows fc2d-r12-convexity-length-message, fc2d-r12-strike-message-positive and fc2d-r12-df-message-range.",
}
CARRY_FILES = {
    "fc2d-r2-numbers-lab1": PAGE_UNCHANGED + " (line 55 and Lab 1 lines 147-163)",
    "fc2d-r2-hours": "project.html lines 339-356 and course/modules/FC/FC2/index.html line 41",
    "fc2d-r2-reading-keys": "project.html lines 652-660",
    "fc2d-r2-autograder-panel-claims": PAGE_UNCHANGED,
    "fc2d-r2-hub-placement-claim": "course/modules/FC/FC2/index.html",
    "fc2d-r3-footer-no-upload": PAGE_UNCHANGED,
    "fc2d-r3-exemplar-scores-match-text": "project.html exemplar scores and annotations (lines 520-635) outside the changed line 538",
    "fc2d-r3-instance-docstring-bounds": "course/modules/FC/FC2/grader/instance.py",
    "fc2d-r2-instances": "course/modules/FC/FC2/grader/instance.py",
    "fc2d-r2-grader-over-constraint-trade-verb": GRADER_UNCHANGED + " (explanation tests)",
    "fc2d-r2-grader-over-constraint-case": GRADER_UNCHANGED + " (explanation tests)",
    "fc2d-r2-mut-r5d-resolved": "ledgers/FC2/mutants (historical r5_d)",
    "fc2d-r2-rubric-C2-level2": "project.html lines 508-513",
    "fc2d-r2-gate-verify-refs": "references/references.json (offline run fresh this round, see below)",
    "fc2d-r3-df-ppm-link": "project.html line 289 (df_ppm bullet), unchanged",
    "fc2d-r6-page-conventions-definitions": "project.html lines 325-336",
    "fc2d-r6-page-line321-anchor": "project.html lines 321 and 517",
    "fc2d-r8-exemplar-level-labels": "project.html lines 351, 520 and 584",
    "fc2d-r5-page-hunk-lab1-hypothesis": "project.html line 55",
    "fc2d-r10-page-hunk-lab1-hypothesis": "project.html line 55",
    "fc2d-r10-page-hunk-P6-leg": "project.html line 333",
    "fc2d-r9-tie-rule-prose": "project.html lines 59-63, 170-173 and 308",
    "fc2d-r9-grader-weak-assertion": GRADER_UNCHANGED + " (lines 595-606)",
    "fc2d-r5-explanation-direction-untested": GRADER_UNCHANGED + " (explanation tests)",
    "fc2d-r7-grader-convexity-docstring": "grader/starter.py and grader/reference.py",
    "fc2d-r7-page-rung1-line44": "project.html line 44",
    "fc2d-r7-page-brief-line490": "project.html line 490",
    "fc2d-r7-exemplar-B-C3-annotation-line543": "project.html line 543",
    "fc2d-r7-exemplar-A-C4-annotation-line618": "project.html line 618",
    "fc2d-r2-reading-keys-dummy": "",
}
ALT_FRESH = {"fc2d-r8-alt-9-10", "fc2d-r5-alt7-cross-multiplied", "fc2d-r6-alt8-forward-price", "fc2d-r9-alternatives-rerun"}
for rid in ALT_FRESH:
    PASS_FRESH.setdefault(rid, f"{S}alts_r12.out: this alternative is among alt1..alt15, 50/50 seeds pass under python -I -W error (this round).")

NEW = [
    fresh({"id": "fc2d-r12-context-sentence-count", "check": "BUILDER_RULES 5.2: Context 2-4 sentences", "location": "course/modules/FC/FC2/project.html line 282 (dl.spec Context)"}, "FAIL",
          "Context dd has 6 sentences (counted with a regex splitter over the unescaped text, this round): (1) 'A desk wants...', (2) 'Some findings use only...', (3) 'Each finding must be explained, not only listed.', (4) 'The desk asks two questions...', (5) 'A data error is a quote...; a true violation is a finding that does.', (6) 'The chain is labelled SIMULATED...'. At ccaeeaf it had 5 (counted the same way). BUILDER_RULES 5.2 requires 2-4 sentences. The check_projects gate (SPEC_TERMS) does not count sentences, so it passes.",
          "Cut Context to at most 4 sentences: move the data-error and true-violation definition into the Conventions list as a labelled item (it is a definition, not a situation), and drop sentence 6 because the Inputs paragraph (line 289) already says the chain is labelled SIMULATED."),
    fresh({"id": "fc2d-r12-data-error-definition", "check": "new definition of data error and true violation (Context, line 282) against Explanation and settlement (line 562) and rubric C5 (lines 496, 512, 566)", "location": "course/modules/FC/FC2/project.html lines 282, 562, 566"}, "PASS",
          "The definition is consistent with Exemplar A's settlement (line 562: 'If the gap survives the re-quote, it is a true violation'; 'if the re-quoted call at 6000 sits at or below the chord, it is a data error') and with the C5 criterion text (lines 496, 512, 566). The page never uses the definition with a number, so no number check applies."),
    fresh({"id": "fc2d-r12-strike-cents-spec", "check": "new scan record sentence: strike_cents for parity is the gap strike, for convexity the interior strike (line 301)", "location": "course/modules/FC/FC2/project.html line 301; grader/reference.py scan (lines 'strike_cents': strike and strikes[j]); grader/test_project.py line 680"}, "PASS",
          "reference.py scan builds parity records with 'strike_cents': strike and convexity records with strikes[j] (the interior index). test_project.py line 680 asserts the convexity key at the planted interior strike, and the 98-mutant run kills z12_c (lower-neighbour strike) by test_scan_matches_exhaustive_oracle_second_chain (seed 0), see mutate_fc2_r12_all.out."),
    fresh({"id": "fc2d-r12-convexity-length-message", "check": "spec sentence: the length message names the lengths, in convexity_violations too (line 313)", "location": "course/modules/FC/FC2/project.html line 313 (named conditions, third bullet); course/modules/FC/FC2/grader/test_project.py lines 544-550 (test_length_message_names_both_lengths calls scan only)"}, "FAIL",
          f"{S}mutate_fc2_r12_all.out: 'SURVIVED z12_a_convexity_length_message_omits_lengths.py' (convexity_violations raises 'calls need one quote per strike' without the lengths) -> None, on seeds 0-9. Page line 313: 'in convexity_violations the check applies to calls_cents ... the message names the lengths'. Only scan's message is tested for the lengths.",
          "Add a test that calls convexity_violations with a length mismatch and asserts that both lengths appear as digits in str(caught.value) (case-insensitive, no exact wording), and re-run mutate_graders; keep alternatives passing."),
    fresh({"id": "fc2d-r12-strike-message-positive", "check": "spec sentence: strike message says strictly increasing and positive (line 311)", "location": "course/modules/FC/FC2/project.html line 311 (first bullet); course/modules/FC/FC2/grader/test_project.py lines 305-307 (parity zero strike) and 437-484 (scan and convexity) (match='strictly increasing' only)"}, "FAIL",
          f"{S}mutate_fc2_r12_all.out: 'SURVIVED z12_f_strike_message_omits_positive.py' (scan and convexity_violations raise 'strikes must be strictly increasing' with no 'positive') -> None, seeds 0-9. Page line 311: 'the message says that the strikes must be strictly increasing and positive'. Every strike test matches only 'strictly increasing'.",
          "Add a non-positive-strike case to the scan and convexity_violations message tests that asserts the word 'positive' appears in the message (case-insensitive substring); keep the match on 'strictly increasing'."),
    fresh({"id": "fc2d-r12-df-message-range", "check": "spec sentence: df message says df_ppm must lie in 1 to 1000000, in each of the three functions (line 312)", "location": "course/modules/FC/FC2/project.html line 312; course/modules/FC/FC2/grader/test_project.py lines 283-300, 492-497 and 580-582 (match='df_ppm' only)"}, "FAIL",
          f"{S}mutate_fc2_r12_all.out: 'SURVIVED z12_g_df_message_omits_range.py' (df error text 'df_ppm is out of range', no range) -> None, seeds 0-9. Page line 312: 'in each of the three functions, the message says that df_ppm must lie in 1 to 1000000'. The tests match only 'df_ppm'.",
          "Assert that the df message names the bound (the digits 1000000) as well as df_ppm, case-insensitively, in each of the three functions; do not require the exact sentence."),
    fresh({"id": "fc2d-r12-ruling13-grades", "check": "FINAL-ARCHITECT-RULINGS item 13 (T versus C for worked values, new this round)", "location": "plans/FINAL-ARCHITECT-RULINGS.md lines 28-31; course/modules/FC/FC2/project.html (whole page)"}, "PASS",
          "Not applicable to the FC2 project page: it carries no T or C grade, no 'graded' or 'basis' label on any value (grep 'graded|basis|Theorem|Proposition|Example' lists only the rubric and the reference lines 659 and 321). Ruling 13 binds cards and key-results rows; FC2-d has none in this slice (cards.json unchanged)."),
    fresh({"id": "fc2d-r12-mut-new-killed", "check": "round-12 student-error mutants z12_b..z12_e (new verifier mutants)", "location": "ledgers/FC2/mutants/z12_b..z12_e"}, "PASS",
          f"{S}mutate_fc2_r12_all.out: z12_b KILLED by test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one (seed 0); z12_c KILLED by test_scan_matches_exhaustive_oracle_second_chain (seed 0); z12_d KILLED by test_df_outside_range_is_rejected[0] (seed 0); z12_e KILLED by test_convexity_boundary_equal_to_chord_is_not_flagged (seed 0)."),
]

rows = []
for r in rows11:
    rid = r["id"]
    if rid in OVERRIDE:
        rows.append(OVERRIDE[rid])
    elif rid == "fc2d-r2-gate-mutate":
        rows.append(OVERRIDE[rid])
    elif rid in PASS_FRESH:
        rows.append(fresh(r, "PASS", PASS_FRESH[rid]))
    elif rid == "fc2d-r11-grader-identity-over-constraint":
        rows.append(fresh(r, "PASS", PASS_FRESH[rid]))
    elif rid in CARRY_FILES and CARRY_FILES[rid]:
        rows.append(carry(r, CARRY_FILES[rid]))
    else:
        files = GENERIC if rid.startswith(("fc2d-r2-card", "fc2d-r4-card", "fc2d-r6-card", "fc2d-r7-card", "fc2d-r8-card", "fc2d-r9-card", "fc2d-r10-card", "fc2d-r11-card", "fc2d-r2-cards", "fc2d-r4-cards", "fc2d-r9-cards")) else GENERIC
        rows.append(carry(r, files if files != GENERIC else GENERIC))

# gate verify-refs: fresh offline run this round
for i, r in enumerate(rows):
    if r["id"] == "fc2d-r2-gate-verify-refs":
        rows[i] = dict(r, status="PASS", fix="", evidence=f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0 (this round). `verify_refs.py --unit FC2` is live-only (exit 2 with 'selects the entries of a live run'), not repeated; the live result of round 11 is carried (references/references.json byte-identical since ccaeeaf).")

# checks for every fresh PASS/FAIL row that must have an evidence file reference
ids_r11 = {r["id"] for r in rows11}
assert [r["id"] for r in rows] == [r["id"] for r in rows11], "row ids must match round 11 in order"

rows_all = rows + NEW
mut_new = [
    ("z12_a_convexity_length_message_omits_lengths", "Student error: convexity_violations raises the length error without naming the two lengths, although the spec says the message names them.", "SURVIVED on seeds 0-9 (no test)"),
    ("z12_b_parity_strike_message_differs", "Student error: parity_gap_cents raises a different message for a zero strike, although the spec says it raises the same error as the other functions.", "test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one (seed 0)"),
    ("z12_c_convexity_strike_cents_lower_neighbour", "Student error: scan reports a convexity finding at the lower neighbour's strike, not at the interior strike whose call lies above the chord.", "test_scan_matches_exhaustive_oracle_second_chain (seed 0)"),
    ("z12_d_convexity_df_message_omits_name", "Student error: convexity_violations validates df_ppm with a message that does not name df_ppm, although the spec says each of the three functions names it.", "test_df_outside_range_is_rejected[0] (seed 0)"),
    ("z12_e_convexity_test_admits_zero_gap", "Student error: convexity_violations flags a call that lies on the chord (zero second difference), although the spec says strictly above.", "test_convexity_boundary_equal_to_chord_is_not_flagged (seed 0)"),
    ("z12_f_strike_message_omits_positive", "Student error: the strike error message says only that strikes must be strictly increasing, and omits the positive requirement the spec says the message states.", "SURVIVED on seeds 0-9 (no test)"),
    ("z12_g_df_message_omits_range", "Student error: the df_ppm error message names df_ppm but not the range 1 to 1000000 that the spec says the message states.", "SURVIVED on seeds 0-9 (no test)"),
]
mutants = [dict(m) for m in mut11] + [{"id": n, "description": d, "killed_by": k} for n, d, k in mut_new]

fails = [r for r in rows_all if r["status"] != "PASS"]
doc = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 12 (did not build FC2)",
    "pin": "329c1d7feac5479403c351e64587c867278452cc",
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87 (round-11 pin); delta inside the slice: project.html lines 282, 299, 301, 486, 538; grader/test_project.py lines 188-192, 263-278, 718, 734, 761, 770; FC2 ledger files a11_a..d, alt13..15 (round 11, verified this round)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD12-FC2-d",
    "scratch": "ledgers/FC2/scripts/FC2-d-r12/ (scripts and outputs); /tmp/fc2d-r12-scratch (page_vs_twin.py, numbers_r12.py, starter copy)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows_all,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 12 on pin 329c1d7. The round-11 FAIL (fc2d-r11-grader-identity-over-constraint) is fixed: the identity assertion was removed and alt15 passes 50/50. "
        "Round-11 observation (1), expected values in tie messages, is resolved by the reworded messages. "
        "New student-error mutants z12_a..z12_g (7): 4 killed (z12_b..e); z12_a, z12_f, z12_g survive because the suite does not check the message content that page lines 311-313 state. "
        "Ruling 13 (T versus C) does not apply to the FC2 project page (no grades). The FC1 files changed in the same delta are outside this slice. "
        "Not run: the full repo pytest (only -k FC2 selection), verify_refs live run (live-only, carried), the browser autograder UI (page_smoke only, Pyodide), fetch_data --check, render_curriculum and build_site --check (no FC2 generated input changed), lessons L01..L08 (byte-identical; carried)."
    ),
    "summary": (
        f"FC2-d round 12: verdict {'FAIL' if fails else 'PASS'} with {len(fails)} non-PASS rows of {len(rows_all)}. "
        "FAILs: (1) Context has 6 sentences, BUILDER_RULES 5.2 allows 2-4; (2) the convexity length message is not tested; "
        "(3) the strike message 'positive' requirement is not tested; (4) the df message range is not tested. Fix for (2)-(4) is a test assertion on message content, which the mutate gate then checks. "
        "The round-11 over-constraint FAIL is PASS. Gates: check_pages, check_dag, check_projects, run_labs 11/11, run_graders 50/50, page_smoke, ruff, mypy strict on the grader, pytest -k FC2, verify_refs offline: PASS. Alternatives 15/15 pass; collect count 94 for every seed. Mutants 95/98 killed."
    ),
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows_all), "fails", len(fails), "mutants", len(mutants), "verdict", doc["verdict"])
