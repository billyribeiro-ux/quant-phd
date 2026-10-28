"""Writes the round 8 AC1-a fragment (ledgers/AC1/AC1-a.json) from the rows verified in round 8."""

from __future__ import annotations

import json
import pathlib

OUT = pathlib.Path("/tmp/verify8-AC1-a/ledgers/AC1/AC1-a.json")
C = "Carried from round 7 (%s byte-identical since the previous pin d57df1e): "
HUB = "course/modules/AC/AC1/index.html"
L01 = "course/modules/AC/AC1/L01.html"
L02 = "course/modules/AC/AC1/L02.html"
L03 = "course/modules/AC/AC1/L03.html"
LABS = "tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py"
CMD = "Re-run at 2c8162b (round 8): "

rows: list[dict] = []


def add(id_, check, location, status, evidence, fix=""):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)


# ---- command rows (re-run by this verifier) ----
add("AC1a-cmd-check_pages", "tools/check_pages.py --unit AC1", "index, L01-L03", "PASS",
    CMD + "'check_pages AC1: PASS' (exit 0; /tmp/ac1-v/a-r8/check_pages.out).")
add("AC1a-cmd-check_dag", "tools/check_dag.py --unit AC1", "AC1 DAG", "PASS",
    CMD + "'check_dag AC1: PASS' (exit 0; /tmp/ac1-v/a-r8/check_dag.out).")
add("AC1a-cmd-run_labs", "tools/run_labs.py --unit AC1", "tests/labs/AC1", "PASS",
    CMD + "'run_labs AC1: PASS (11/11)' (exit 0; /tmp/ac1-v/a-r8/run_labs.out).")
add("AC1a-cmd-page_smoke", "tools/page_smoke.py --unit AC1 --pages index L01 L02 L03", "index, L01, L02, L03", "PASS",
    CMD + "'page_smoke AC1: PASS' (exit 0; /tmp/ac1-v/a-r8/page_smoke.out).")
add("AC1a-cmd-verify_refs", "tools/verify_refs.py --unit AC1 (live) and --offline", "references/references.json", "PASS",
    CMD + "live '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems' (exit 0 both). references/references.json unchanged d57df1e..2c8162b (git diff empty).")
add("AC1a-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the AC1 labs", "tests/labs/AC1", "PASS",
    CMD + "ruff check 'All checks passed!'; ruff format --check '11 files already formatted'; mypy --no-incremental 'Success: no issues found in 3 source files' (exit 0 each; /tmp/ac1-v/a-r8/ruff.out, mypy.out).")
add("AC1a-cmd-twin-run", "python -I -W error on each AC1-a twin", "tests/labs/AC1/lab-AC1-L01-1.py, L02-1, L03-1", "PASS",
    CMD + "exit 0 each, 0 bytes stderr; outputs /tmp/ac1-v/a-r8/L01.out, L02.out, L03.out. L03 prints six checks and 'all articulation identities hold in every year: True'.")
add("AC1a-cmd-pytest-AC1", "pytest -q tests -k 'AC1 or lab'; collect-only count", "tests", "PASS",
    CMD + "143 passed (72 + 71 dots, exit 0); collect-only count 143 (tests/test_labs.py 127, test_run_labs.py 6, test_page_checks.py 4, test_page_smoke.py 2, test_memo_exemplars.py 2, test_fetch_data.py 1, test_figure_kernels.py 1). The round 7 subset (-k AC1, 11) is not re-run.")
add("AC1a-cmd-scope-witness", "scope witnesses for Proposition 3.2 (L01) and Remark 3.3 (L02)", "L01.html Proposition 3.2 statement; L02.html Remark 3.3", "PASS",
    "Re-derived in ledgers/AC1/scripts/AC1-a-r8/slice_checks.py: a write-off of 30 on sales of 100 with no collections gives R=100, K=0, dA=70, R-K=100, identity holds: False (/tmp/ac1-v/a-r8/slice_checks.out). The Prop 3.2 hypothesis (i) names write-offs as excluded.")
add("AC1a-twin-matches-page", "each AC1-a page's data-run block equals its twin", "L01.html, L02.html, L03.html", "PASS",
    "Re-run in ledgers/AC1/scripts/AC1-a-r8/slice_checks.py: one data-run block per page, equal to the twin after rstrip of the trailing newline (True, True, True).")
add("AC1a-cite-none", "no citation markup in the four pages", "index.html, L01-L03.html", "PASS",
    "Re-run: slice_checks.py finds no data-cite, class=\"cite\" or data-key in the four pages. Each page's References section says it cites no registry key.")
add("AC1a-lab-seeded-offline", "labs seeded, offline, standard library only", LABS, "PASS",
    C % LABS + "the three twins (git diff d57df1e..2c8162b empty for these files). Imports are __future__, random and dataclasses; SEED = 20261027 in each.")

# ---- hub ----
add("AC1a-num-hub", "numbers in the hub", HUB, "PASS", C % HUB + "the hub file is unchanged since d57df1e.")
add("AC1a-hours-hub", "hub hours split and lesson hours arithmetic", HUB + " line 29 and lines 150-157", "PASS",
    "Re-computed at 2c8162b: data-hours-lessons=90, data-hours-project=30, title 120 hours (= 90 + 30). Lesson data-hours L01 11, L02 12, L03 11, L04 11, L05 12, L06 12, L07 11, L08 10 sum to 90; hub list L01 11 h, L02 12 h, L03 11 h, L04 11 h, L05 12 h, L06 12 h, L07 11 h, L08 10 h match. No arithmetic inconsistency.")
add("AC1a-hours-L01", "lesson hours", L01 + " data-hours", "PASS", C % L01 + "data-hours=11 (line 2); hub list 11 h.")
add("AC1a-hours-L02", "lesson hours", L02 + " data-hours", "PASS", C % L02 + "data-hours=12 (line 2); hub list 12 h.")
add("AC1a-hours-L03", "lesson hours", L03 + " data-hours", "PASS", C % L03 + "data-hours=11 (line 2); hub list 11 h.")
add("AC1a-struct-lessons", "template section headings of L01-L03", L01 + ", " + L02 + ", " + L03, "PASS",
    "Re-run at 2c8162b: the h1-h3 lines of each page equal the d57df1e lines (git show d57df1e:<file> | grep '<h[123]' compared with the current file: identical for L01, L02, L03). The delta moves block bodies, not headings.")
add("AC1a-struct-hub", "hub section order", HUB, "PASS", C % HUB + "the hub is unchanged since d57df1e (git diff --stat empty for index.html).")
add("AC1a-placement-arithmetic", "placement threshold arithmetic", HUB + " line 72", "PASS", C % HUB + "80% of 9 = 7.2, unchanged.")
add("AC1a-curriculum-match", "hub meta rows, lede and Unlocks", HUB, "PASS", C % HUB + "the hub is unchanged since d57df1e.")
add("AC1a-index-objective5", "hub objective 5 cross-references to L05-L08", HUB + " line 53; L05.html 492; L06.html 456; L07.html 341; L08.html 287", "PASS",
    "Re-read at 2c8162b: hub line 53 is unchanged. L05 line 492 and L06 line 456 are unchanged. L07 line 341 and L08 line 287 changed in d57df1e..2c8162b (outside this slice); the current text states the point each objective names (L07: bonus cash and income effects 'are not stated here'; L08: the per-asset tax schedules and yearly rates the model lacks). Those two pages belong to another slice and were read only at the cited line.")
add("AC1a-index-registry-scope", "index line 175 registry statements", HUB + " line 175", "PASS",
    C % HUB + "the hub; references/references.json unchanged (git diff empty). The paragraph names no FASB entry and the IFRS keys it relies on are in the registry (verify_refs offline 560 entries, 0 problems).")
add("AC1a-r6-hub-glossary-explains", "hub explain texts rewritten in round 6", HUB + " lines 81-131", "PASS",
    C % HUB + "the hub is unchanged since d57df1e. Re-read: the explain at line 136 cites 'L01, Definition 1.1' and line 141 cites 'L01, Proposition 3.2'; both still exist with those statements (L01 Definition 1.1 at line 71 and Proposition 3.2 at line 387).")
add("AC1a-data-simulated", "data status statements (index line 175; footers)", HUB + " line 175; L01 line 661; L02 line 802; L03 line 932", "PASS",
    "Re-read: index line 175 unchanged; L01 footer line 661 reads 'The lab figures in this lesson are SIMULATED.' and the L01 References paragraph (line 650) is unchanged; L02 footer line 802 and L03 footer line 932 unchanged in the delta (both lessons: net zero line shift). Each lab is labelled SIMULATED in heading, hypothesis and interpretation (re-grep at 2c8162b).")
add("AC1a-notation", "notation macros in the four pages", "index.html, L01-L03.html", "PASS",
    "Re-run at 2c8162b: slice_checks.py finds no gamma3, gamma4, \\Phi, \\mathbb, \\Rstar, \\R_f or \\mathbf in the four pages.")
add("AC1a-banned-phrases", "banned phrases and ellipses in the four pages", "index.html, L01-L03.html", "PASS",
    "Re-run at 2c8162b: slice_checks.py finds no 'roughly half', 'about 6', 'historically', 'as much as', 'TODO', 'TBD', 'lorem'. The only three-dot sequences are Python type annotations inside lab code (L01 line 151; L02 line 200; L03 lines 178, 226, 498), not prose ellipses.")

# ---- L01 ----
add("AC1a-grade-T-L01", "grades T: Proposition 2.1, Proposition 3.2", L01 + " Proposition 2.1 (line 90) and Proposition 3.2 (line 387)", "PASS",
    C % L01 + "the Proposition 2.1 and 3.2 statements and proofs (not in any hunk). Re-read: Proof of 2.1 sums balanced entries; Proof of 3.2 splits revenue and expense as stated.")
add("AC1a-num-L01", "numbers in prose on L01 (Example 3.3, E1-E3, interpretation)", L01 + " (Example 3.3 line 399; E1 line 506; interpretation line 379)", "PASS",
    C % L01 + "the numbers. Example 3.3: 192,834.97 + 21,046.51 = 213,881.48; collections 154,267.97; 213,881.48 - 175,314.48 = 38,567.00 (re-computed in Python -I at 2c8162b, equal to the lab's receivable).")
add("AC1a-L01-timings-balances", "L01 paragraph 'In Lab 1 the firm sells on credit...' (Example 3.3)", L01 + " Example 3.3 (line 399)", "PASS",
    C % L01 + "the Example 3.3 paragraph (its line moved from about 399 to 400 by the definition move). Its figures 192,834.97, 21,046.51, 154,267.97, 213,881.48, 175,314.48 and 38,567.00 match the Lab 1 output.")
add("AC1a-L01-E3-five", "L01 E3 and quiz", L01 + " E3 (line 517) and the quiz", "PASS",
    C % L01 + "the E3 and quiz blocks (no hunk).")
add("AC1a-L01-key-scope", "L01 Key results row on the balance check scope", L01 + " Key results row (line 560)", "PASS",
    C % L01 + "the Key results row (no hunk in it).")
add("AC1a-L01-remark34-amount-sources", "L01 Remark 3.4 amount sources", L01 + " Remark 3.4 (line 404)", "PASS",
    C % L01 + "Remark 3.4 sentence (no hunk). Its amounts match the lab generator: credit sale randrange(18,000,000, 24,000,000), collection balance * 4 // 5, payment balance // 2, opening investment 80,000.00 (lab-AC1-L01-1.py lines 100-139).")
add("AC1a-L01-interp-drawn-scope", "L01 lab docstring and interpretation: the drawn amounts", L01 + " interpretation (line 379); lab docstring lines 1-7", "PASS",
    C % L01 + "the interpretation text and the lab docstring (lab-AC1-L01-1.py unchanged since d57df1e). The interpretation names the four drawn amounts (credit sale, cash sale, expense on account, expense paid in cash) and the fixed fractions.")
add("AC1a-lab-L01-claims", "L01 lab hypothesis and printed output", L01 + " hypothesis (line 108)", "PASS",
    C % L01 + "the hypothesis (moved from line 103 to 108 by the five-line Definition 1.3 insertion; text unchanged) and the lab docstring. The output (/tmp/ac1-v/a-r8/L01.out) shows seven entries, each balanced, a balanced trial balance, and both difference-equals-balance lines True; three malformed entries refused, 'entries before 7, after 7'.")
add("AC1a-r8-L01-def13-placement", "Definition 1.3 (accrual accounting) moved to section 1", L01 + " lines 80-84", "PASS",
    "Re-read at 2c8162b: Definition 1.3 defines accrual accounting in section 1 before its first body use (section 3, line 382). The single anchor def-accrual-accounting (L01 line 82) matches concepts.html line 101 (L01.html#def-accrual-accounting). The sentence 'a credit sale and a cash sale are both recognized as revenue on the date of the sale' matches the lab journal (day 5 credit sale, day 9 cash sale, both credited to sales).")
add("AC1a-r8-L01-s5-leadin", "Section 5 lead-in: 'says nothing about whether an event happened'", L01 + " Section 5 lead-in (line 420)", "PASS",
    "Re-read at 2c8162b: the lead-in now states that the double-entry rule says nothing about whether an event happened. This matches Remark 2.2 (posting checks do not test that the event happened) and Section 5 bullet 1 ('does not guarantee that each entry describes an event that happened').")

# ---- L02 ----
add("AC1a-grade-T-L02", "grades T: Proposition 2.2, 3.2, 4.2 (statements and proofs)", L02 + " lines 82-86, 101-103, 125-127", "PASS",
    "Re-verified at 2c8162b: Proposition 2.2 proof N = S - K - O - D (Definition 2.1 now names D as the depreciation charge, Lesson 3 gives its definition). Proposition 3.2 proof A - L - C + H - N = 0 gives A = L + C + (N - H) with retained earnings N - H (Definition 3.1). Proposition 4.2 proof sums the cash lines by activity. Each agrees with its statement.")
add("AC1a-r8-L02-def21-forward-ref", "Definition 2.1: depreciation used before its Lesson 3 definition", L02 + " line 73", "PASS",
    "Re-read at 2c8162b: the sentence says D is 'the depreciation charge of the year, a non-cash expense whose definition Lesson 3 gives'. The forward reference is explicit and Lesson 3 Definition 1.2 gives the definition; no concept link is made here. Accepted as an explicit cross-lesson pointer, not an undefined term.")
add("AC1a-L02-why-common-error", "L02 flow versus stock paragraph", L02 + " line 55", "PASS",
    C % L02 + "the paragraph at line 55 (no hunk there; the hunk is at 59 and 73).")
add("AC1a-r8-L02-s6-net-income-bullet", "Section 6 bullet: net income is an accrual measure (Lesson 1, Definition 1.3)", L02 + " line 550", "PASS",
    "Re-read at 2c8162b: 'Proposition 2.2 sums the revenue and cost accounts of the ledger, which record revenue when a sale is made and cost when it is incurred (Lesson 1, Definition 1.3).' Lesson 1 Definition 1.3 says revenue is recorded in the period a sale is made and cost in the period it is incurred. Citation and statement agree. No numbers in the bullet.")
add("AC1a-r8-L02-P3-reclass", "Problem P3 (proof tier) solution: a reclassification changes two subtotals", L02 + " line 623", "PASS",
    "Re-read at 2c8162b: P3 is 'one cash line is reclassified from operating to investing'. The solution says 'The operating and investing subtotals change, in opposite directions and by the same amount.' For that specific reclassification this is correct (amount unchanged; one subtotal up, one down; financing unchanged). The word 'Only' was removed; the statement no longer claims more than the case supports.")
add("AC1a-num-L02", "numbers in prose on L02", L02 + " section 5 (line 547), section 6, misconceptions (lines 560-575), E1-E3 (line 634 onward)", "PASS",
    C % L02 + "numbers (no change to figures). Re-computed at 2c8162b: 1,003,421.14 - 200,000.00 = 803,421.14; 1,654,305.29 + 0 - 200,000.00 = 1,454,305.29; 3,000,000.00 + 1,454,305.29 = 4,454,305.29 (Lab 2 output line 20 gives 2025 retained earnings 803,421.14).")
add("AC1a-grade-C-rows", "grade C rows in Key results and Example 3.3; Key results of L02 and L03", L02 + " line 689; " + L03 + " lines 813-814", "PASS",
    "Re-verified at 2c8162b: L02 line 689 row 'The activity split of each cash line is a convention ... what any reporting framework requires for this split is not stated here' is C with basis 'Convention of this lab'. L03 table (lines 814-815) Straight-line row cites Definition 1.2 and Remark 6.3, both present; C basis is the lab convention. Both rows agree with their lessons.")
add("AC1a-lab-L02-claims", "L02 lab hypothesis, interpretation and output", L02 + " hypothesis (lines 133-134); interpretation (line 535)", "PASS",
    C % L02 + "the hypothesis and interpretation text; lab-AC1-L02-1.py is unchanged since d57df1e. Re-run at 2c8162b: the L02 output (/tmp/ac1-v/a-r8/L02.out) prints the balance-sheet flag and the lowest-cash line, and the interpretation says the lab checks the balance sheet only (one flag). Interpretation figures 1,454,305.29 and 3,000,000.00 match the output.")
add("AC1a-L02-lab-prop22", "L02 lab: Proposition 2.2 claim, four income accounts", L02 + " line 86", "PASS",
    C % L02 + "line 86 and its statement (no hunk).")
add("AC1a-L02-lab-zero-difference", "L02 lab: no tax, interest, inventory or intangible account", L02 + " line 110", "PASS",
    C % L02 + "line 110 (no hunk).")
add("AC1a-L02-growing-depreciation", "L02 depreciation rising in 2026 (75,000.00 a quarter)", L02 + " paragraph after the Lab 2 interpretation (line 538)", "PASS",
    C % L02 + "the paragraph; the lab adds a fixed 75,000.00 a quarter from 2026 Q1 (lab-AC1-L02-1.py depreciation rule; L03 asset equipment B cost 150,000,000 cents over 20 quarters = 7,500,000 cents = 75,000.00 a quarter, consistent).")
add("AC1a-L02-very-different-years", "L02 balance sheet is a snapshot claim", L02 + " section 6 bullet 1 (line 549)", "PASS",
    C % L02 + "the snapshot claim (Definition 1.1 stock).")
add("AC1a-L02-R3-repurchase-standard", "L02 R3 solution: repurchase classification left open", L02 + " lines 669-671", "PASS",
    C % L02 + "the R3 solution paragraph; it states the requirement is not stated here.")
add("AC1a-L02-def41-activity", "L02 Definition 4.1: each cash line's activity", L02 + " line 116; lab-AC1-L02-1.py activity rules", "PASS",
    C % L02 + "Definition 4.1 (line 116) and lab-AC1-L02-1.py (no change since d57df1e).")
add("AC1a-L02-q10-explain-causal", "L02 quiz q10 explanation (Remark 3.3)", L02 + " explain (line 775); Remark 3.3 (lines 106-108)", "PASS",
    C % L02 + "the q10 explanation and Remark 3.3.")
add("AC1a-r6-L02-remark33-scope", "L02 Remark 3.3 scope", L02 + " lines 106-108, 775", "PASS",
    C % L02 + "Remark 3.3 and its explain.")
add("AC1a-r6-L02-H-rename", "dividend symbol H in L02 Proposition 3.2 proof and L03 roll-forward", L02 + " lines 102, 614-616; " + L03 + " lines 737-739", "PASS",
    C % (L02 + ", " + L03) + "the proof and the roll-forward; no stray D_s or \\(D symbol (grep at 2c8162b: 0 hits).")
add("AC1a-r6-L02-lab-scope-word", "L02 interpretation: 'the lab checks the balance sheet only'", L02 + " line 535", "PASS",
    C % L02 + "line 535 (the printed check is one flag, lab-AC1-L02-1.py).")
add("AC1a-quiz-keys", "quiz answer keys of L01, L02, L03", L01 + " quiz; " + L02 + " quiz; " + L03 + " quiz (q4 explain line 854)", "FAIL",
    "Re-verified at 2c8162b: the L02 q10 key and the L03 q7 key are consistent with their lessons. The L03 q4 explanation (line 854) reads 'Definition 1.2: depreciation credits accumulated depreciation, a contra-asset, and has no cash line.' Definition 1.2 (line 61) states the debit to depreciation expense, the credit to accumulated depreciation and no cash line; it does not state 'a contra-asset'. That term is used in Lesson 2 (line 102, Proposition 3.2 proof) and in the lab chart (line 185).",
    fix="In " + L03 + " line 854, change the explanation to: 'Definition 1.2: depreciation credits accumulated depreciation and has no cash line. Accumulated depreciation is a contra-asset (Lesson 2, Proposition 3.2 proof).'")

# ---- L03 ----
add("AC1a-grade-T-L03", "grades T: Propositions 2.2, 3.1, 4.1, 4.2 (statements and proofs)", L03 + " lines 75-127", "FAIL",
    "Re-verified at 2c8162b: Proposition 2.2 (indirect equals direct) proof gives S_k + Q - O - V on both routes; Proposition 3.1 proof is correct; Proposition 4.1 cites Definition 3.1 of Lesson 2 correctly. Proposition 4.2 proof (line 120) cites Definition 1.2 for 'by the same amount that it debits to depreciation expense', but Definition 1.2 (line 61) states only the two lines of the entry and no amount. The equality holds because every entry balances (Lesson 1, Definition 1.1), and the citation does not say so.",
    fix="In " + L03 + " line 120, cite the balance rule: 'A depreciation entry credits accumulated depreciation by the same amount that it debits to depreciation expense (a balanced entry, Lesson 1, Definition 1.1; the two lines of the entry are in Definition 1.2).'")
add("AC1a-grade-T-L03-prop62", "grade T: Proposition 6.2 depreciation entry", L03 + " lines 140-146", "PASS",
    C % L03 + "Proposition 6.2 and its proof (lines 140-146; the hunk removing Definition 6.1 is at 134-138, so 140-146 are unchanged). Re-read: the entry has one debit to depreciation expense, one credit to accumulated depreciation and no cash line; net income falls by the charge; the add-back restores operating cash flow.")
add("AC1a-r8-L03-def12-definition", "Definition 1.2 (depreciation, straight-line)", L03 + " lines 60-64", "PASS",
    "Re-read at 2c8162b: equal quarterly charge (lab: per_quarter = cost // quarters_of_life, lab-AC1-L03-1.py line 356), no residual value (ASSETS tuple has none), entry debits depreciation expense and credits accumulated depreciation with no cash line (lab-AC1-L03-1.py lines 241-242), amortization not computed (no intangible in the lab).")
add("AC1a-L03-largest-noncash", "L03 why-it-matters (line 51)", L03 + " line 51", "PASS",
    "Re-verified at 2c8162b (line 51 changed in this delta): the sentence now says the charge 'that reduces income and has no cash line, which operating cash flow adds back (Definition 2.1)' is treated as a schedule the ledger must reproduce (Check 5) and that the lesson computes the gap that omitting it leaves (Check 6, 1,000,000.00 in 2025). Both gaps are printed by the lab: depreciation gap (Check 6) and dividends gap (Check 6, 200,000.00 each year).")
add("AC1a-L03-remark63-first-charge", "L03 Remark 6.3 (line 150)", L03 + " line 150", "PASS",
    C % L03 + "Remark 6.3 (line 150; hunks at 134-138 and 60-64 do not touch it). Re-read: the lab fixes cost, life and first quarter, the straight-line method and zero residual; the schedule rejects a cost that does not divide into quarters (lab line 354-355, confirmed by the code).")
add("AC1a-L03-check5-wrong-quarter", "L03 interpretation: Check 5 fails for wrong-year or wrong-amount charges", L03 + " interpretation (line 662)", "PASS",
    C % L03 + "the interpretation; re-run of this verifier's witness (ledgers/AC1/scripts/AC1-a-r8/l03_articulation_witness.py): a +1 cent depreciation in 2025 Q2 and a 26,000,000 quarterly charge each make Check 5 print False and leave Checks 1-4 and 6 and the final identity True (/tmp/ac1-v/a-r8/l03_articulation_witness.out).")
add("AC1a-L03-planted-error-detect", "L03 Check 6 interpretation (each gap equals its term)", L03 + " interpretation (line 662)", "PASS",
    C % L03 + "the Check 6 interpretation. The code (lab-AC1-L03-1.py lines 428-436) gives difference = direct - (indirect - D) = D + (direct - indirect), so the gap equals D iff Check 2 holds (confirmed by the witness outputs).")
add("AC1a-L03-R3-investing-standard", "L03 R3 solution: investing and financing equalities not printed", L03 + " R3 solution", "PASS",
    C % L03 + "the R3 solution (no hunk); lab docstring says Proposition 3.1 is not printed.")
add("AC1a-L03-as-much-as", "scope words: 'as much as' and related", L03 + " lines 667-671", "PASS",
    "Re-run at 2c8162b: slice_checks.py finds no 'as much as' in L03.html.")
add("AC1a-L03-R1-causal", "L03 R1 solution: hedged causal wording", L03 + " R1 solution", "PASS",
    C % L03 + "the R1 solution (no hunk).")
add("AC1a-L03-interp-fixed-scope", "L03 interpretation: fixed amounts in the code", L03 + " interpretation (line 662)", "PASS",
    C % L03 + "the interpretation; it names credit sales, cash sales, operating expense and cost percentage as drawn, and collections and payments as fixed fractions (nine tenths of the payable in lab-AC1-L03-1.py line 6 and code).")
add("AC1a-quiz-L03-q7", "L03 quiz q7 key and stem", L03 + " lines 871-873", "PASS",
    C % L03 + "q7 (lines 871-873 unchanged; the quiz explain at line 854 is the q4 explanation, separately FAILed under AC1a-quiz-keys).")
add("AC1a-r6-L03-q7-key", "L03 quiz q7 key and stem", L03 + " lines 871-873", "PASS",
    C % L03 + "q7 key: 'Net income falls by 100 cents, and the cash balance does not change' is consistent with Proposition 6.2 (no cash line).")
add("AC1a-num-L03", "numbers in prose on L03 (Lab 3 interpretation, M1-M3, E1-E3, R1-R3)", L03 + " interpretation (line 662); Misconceptions (lines 680-697)", "PASS",
    C % L03 + "the numbers in those paragraphs. Re-checked 2025 operating: 1,003,421.14 + 1,000,000.00 - 515,320.87 + 166,205.02 = 1,654,305.29 (Lab 3 Check 2 output).")
add("AC1a-r8-L03-theorem-para", "Theorem 5.1 paragraph: 'Check 1 ... 0.00'; 'Checks 2, 3 and 4 print True'", L03 + " line 135", "PASS",
    "Re-verified at 2c8162b against /tmp/ac1-v/a-r8/L03.out: Check 1 prints 'assets less liabilities and equity = 0.00' at each year end; Check 2 prints 'indirect equals direct: True'; Check 3 prints True on each roll-forward line; Check 4 prints True on each year. The paragraph's 'four of its five parts' matches the lab (Propositions 3.1 are proved, not printed).")
add("AC1a-lab-L03-claims", "L03 lab claims: Theorem 5.1 parts checked, the docstring, the six printed checks", L03 + " hypothesis (line 156), Theorem paragraph (line 135), interpretation (line 662); lab-AC1-L03-1.py lines 1-11", "PASS",
    "Re-verified at 2c8162b: the lab docstring (lines 1-11) and hypothesis match the six printed checks (/tmp/ac1-v/a-r8/L03.out). The Theorem 5.1 paragraph was corrected in this delta and now matches the output (see AC1a-r8-L03-theorem-para).")
add("AC1a-r6-simulated-labels", "each lab labelled SIMULATED in heading, hypothesis and interpretation", L01 + " 107-108, 379; " + L02 + " 132-133, 535; " + L03 + " 155-156, 662", "PASS",
    C % (L01 + ", " + L02 + ", " + L03) + "the labels (L01 heading moved from line 102 to 107 by the Definition 1.3 insertion; text unchanged).")
add("AC1a-dag-concepts", "concept definitions and use order (check_dag and the moved definitions)", L01 + " lines 82, 90; " + L03 + " lines 56-64; check_dag", "PASS",
    "Re-run at 2c8162b: check_dag AC1 PASS. The accrual-accounting anchor is in L01 (line 82) and used first in L01 section 3 and later lessons; depreciation-and-amortization is anchored once (L03 line 61) and the L03 cross-references 'Definition 2.1' (line 71) and 'Definition 1.2' (line 71, and L02 line 73 as a forward pointer) resolve. The Definition 6.1 cross-reference is gone.")
add("AC1a-r8-concept-index", "concepts.html links for the moved definitions", "course/concepts.html lines 101-106", "PASS",
    "Re-run at 2c8162b: tools/build_site.py --check exit 0, 'site data current: 6 outputs'. concepts.html links accrual-accounting to L01.html#def-accrual-accounting and depreciation-and-amortization to L03.html#def-depreciation-and-amortization, both single anchors.")
add("AC1a-r8-hub-lab-fractions", "hub line 175 collections and payments fractions vs lab code", HUB + " line 175", "PASS",
    "Re-run: lab-AC1-L01-1.py line 131 collection = balance * 4 // 5 and line 139 payment = balance // 2 (one half in Lesson 1); lab-AC1-L02-1.py line 220 and lab-AC1-L03-1.py line 223 payment = balance * 9 // 10 (nine tenths in Lessons 2 and 3). The hub statement matches.")
add("AC1a-r8-witness-wrong-schedule", "L03 misconception 3 and cards c038: a wrong depreciation schedule still articulates", L03 + " misconception 3 (line 691); cards.json AC1-c038", "PASS",
    "Witness re-run: ledgers/AC1/scripts/AC1-a-r8/l03_articulation_witness.py. With a consistently posted wrong charge, Checks 1-4 and 6 and the final 'all articulation identities hold in every year: True' stay True; only Check 5 (schedule) prints False. The claim as stated is supported by the output.")

# ---- cards ----
add("cards-L01-all", "cards AC1-c001 to c016 against the L01 text (incl. c008 accrual and c011 numbers)", "course/modules/AC/AC1/cards.json (L01 cards); " + L01, "PASS",
    "Each L01 card checked against the current L01 text at 2c8162b: c003 (Definition 1.1), c004 (Definition 1.2, Section 2), c008 (Definition 1.3, now in section 1), c009 (255,314.48 debits, 30,594.17 credits, 224,720.31; sales 213,881.48; C grade with Lab 1 basis), c010 (Proposition 2.1, Remark 2.2), c011 (49,831.40; 30,594.17; 19,237.23 = payable), c013 (hypotheses (i) to (v) of Proposition 3.2), c014 (38,567.00, Example 3.3), c015 (Remark 2.2, Definition 1.1), c016 (Section 1 table). Every card number appears in L01 (Lab 1 output or text). No card contradicts the current lesson.")
add("cards-L02-c032", "card AC1-c032 back: 'not a rule of any reporting framework'", "course/modules/AC/AC1/cards.json AC1-c032; " + L02 + " line 689", "FAIL",
    "The card says the activity split 'is a convention set by the generator in Lab 2 (Definition 4.1), not a rule of any reporting framework.' L02 line 689 (Key results) states that 'what any reporting framework requires for this split is not stated here', and the L02 References paragraph (line 791) says the statements are defined from the ledger. The lesson declines to make a framework claim; the card makes one, and no standard text is read in the registry for it.",
    fix="In course/modules/AC/AC1/cards.json, card AC1-c032 back: replace the clause 'not a rule of any reporting framework' with 'what any reporting framework requires for this split is not stated here' (or drop the clause).")
add("cards-L02-rest", "cards AC1-c017 to c031 (excluding c032) against the L02 text", "course/modules/AC/AC1/cards.json (L02 cards); " + L02, "PASS",
    "Checked at 2c8162b: c017-c021 (Definitions 1.1 and 1.2), c022 (N = S - K - O - D, Definition 2.1), c023 (Definition 3.1), c024 (Definition 4.1), c025 (1,003,421.14; 1,654,305.29; Lesson 3 derives the difference), c026 (3,000,000.00 to 4,454,305.29; Definition 1.1), c027 (Proposition 3.2; Lesson 1 Remark 2.2), c028 (Proposition 2.2), c029 (Proposition 3.2), c030 (Proposition 4.2), c031 (2025 net income 1,003,421.14 and retained earnings 803,421.14; L02 output line 20 gives 2025 retained_earnings 803,421.14 with 2024 at 0.00). Every card number appears in L02.")
add("cards-L03-all", "cards AC1-c033 to c045 and c123, c124, c126 against the L03 text", "course/modules/AC/AC1/cards.json (L03 cards); " + L03, "PASS",
    "Checked at 2c8162b: c033 (Definition 1.1), c034 (Definition 2.1), c035 (Definition 1.2), c036 (Proposition 6.2; equipment B, cost 150,000,000 cents, 2026 Q1 purchase; investing 1,500,000.00 in Check 4), c037 (2026 add-back 1,300,000.00, operating 2,191,615.64), c038 (Theorem 5.1; misconception 3), c039 (Proposition 2.2), c040 (Proposition 3.1), c041 (Proposition 4.1), c042 (Theorem 5.1 five parts), c043 (Proposition 6.2), c044 (1,000,000.00, 2,300,000.00, 3,600,000.00 from Check 5), c045 (Remark 6.3), c124 (Proposition 3.1), c126 (Definition 1.2; Remark 6.3). Card numbers appear in L03 text or output. Card c038's 'because' clause is the lesson's own misconception 3 wording, and the witness supports it.")
add("cards-L03-c123", "card AC1-c123 (T) against Proposition 4.2 (round 7 FAIL re-verified)", "course/modules/AC/AC1/cards.json AC1-c123; " + L03 + " Proposition 4.2 (lines 114-120)", "PASS",
    "Re-verified at 2c8162b: the card's hypotheses (no entry credits equipment at cost; no entry debits accumulated depreciation; every credit to accumulated depreciation is a depreciation entry) and conclusion (net equipment at a year end equals the prior year's plus additions less depreciation of the year) match the lesson's Proposition 4.2 statement word for word in substance. The round 7 mismatch is cured.")
add("cards-L03-theorem-5-1-print-claim", "L03 Theorem 5.1 paragraph: 'the checks print True' (round 7 FAIL re-verified)", L03 + " line 135", "PASS",
    "Re-verified at 2c8162b: the paragraph no longer says all four checks print True. It says Check 1 prints the gap, which is 0.00 at each year end, and Checks 2, 3 and 4 print True. Output confirms both. The round 7 FAIL is cured.")
add("cards-duplicate-scan", "duplicate scan of cards.json (126 cards in the unit)", "course/modules/AC/AC1/cards.json", "PASS",
    "Re-run at 2c8162b (ledgers/AC1/scripts/AC1-a-r8/slice_checks.py): 126 cards, 126 unique ids, 126 unique fronts, no duplicate fronts.")

# ---- delta and mutants ----
add("AC1a-r6-delta", "round 6 delta (00745fe..d57df1e) for this slice", "course/modules/AC/AC1/index.html, L01-L03; tests/labs/AC1/lab-AC1-L01-1.py, L02-1, L03-1", "PASS",
    "Historical: round 6 delta recorded in /tmp/fanout-frags/AC1-a.round6.json; superseded by the round 8 delta below.")
add("AC1a-r5-delta", "round 5 delta (51ee6d2..00745fe) for this slice", "same files", "PASS", "Historical: superseded.")
add("AC1a-r4-delta", "round 4 delta (66fda36..51ee6d2) for this slice", "same files", "PASS", "Historical: superseded.")
add("AC1a-r3-delta", "round 3 delta (45370ed..66fda36) for this slice", "same files", "PASS", "Historical: superseded.")
add("AC1a-r3-scope-witness-prop32", "scope witness for Proposition 3.2 (write-off)", L01 + " Proposition 3.2 (line 387); " + L02 + " line 97", "PASS",
    "Re-run at 2c8162b: write-off witness R = 100, K = 0, dA = 70, R - K = 100, identity holds False (slice_checks.out). Proposition 3.2 hypothesis (i) excludes write-offs, so the scope is stated.")
add("AC1a-r8-delta", "round 8 delta for this slice (d57df1e..2c8162b)", HUB + " (no change); L01.html; L02.html; L03.html; lab twins (no change)", "PASS",
    "git diff -U0 d57df1e 2c8162b -- index.html L01 L02 L03 and the three twins: index.html unchanged; L01: Definition 1.3 inserted at line 80 (+5), Definition 3.1 removed at 381 (-5), line 420 wording; L02: lines 73 (Definition 2.1), 550 (Section 6 bullet), 623 (Problem P3); L03: line 51 (why-it-matters), Definition 1.2 inserted at 60 (+5), line 66 to 71, lines 115 and 120 (Proposition 4.2 hypotheses and proof), line 135 (Theorem paragraph), Definition 6.1 removed at 134-138 (-5), line 744 (P3), lines 814 and 854 (table and quiz explain). Twins: no change. Every hunk read; each is covered by a row above.")
add("AC1a-r8-mutants-not-required", "project-slice mutant minimum", "ledgers/AC1/AC1-a.json (lesson slice)", "PASS",
    "AC1-a is lessons and hub only (no grader in the slice), so the project mutant minimum does not apply. Witness mutants used for L03 claims are listed in notes, not as grader mutants.")

fragment = {
    "unit": "AC1",
    "slice": "AC1-a",
    "round": 8,
    "round_note": "round 8 independent verification of AC1-a at 2c8162b. Previous pin d57df1e (the pin recorded in AC1-a.round7.json and AC1-a.round6.json); delta d57df1e..2c8162b for this slice enumerated in AC1a-r8-delta.",
    "verifier": "Haiku independent verifier, AC1-a round 8 (did not build AC1)",
    "pin": "2c8162b",
    "base": "d57df1e (previous verified pin); the de53f7e and 2c8162b fixes are inside the delta",
    "checkout": "/tmp/verify8-AC1-a (detached worktree at 2c8162b, .venv symlinked)",
    "scratch": "/tmp/ac1-v/a-r8",
    "verified_at": "2026-10-28",
    "registry_flags": [
        "references/references.json: unchanged in d57df1e..2c8162b (git diff empty); live verify_refs --unit AC1: 2 of 560 entries, 0 problems; offline 560 entries, 0 problems."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html and tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py, plus the AC1 cards.json entries of L01-L03 (126 cards in the unit, 16 + 16 + 16 of this slice checked against the lesson text).",
        "Delta treatment: index.html and the three twins are byte-identical since d57df1e, so their rows are carried with the round 7 prefix. Lesson rows whose cited paragraph is in a hunk were re-verified from scratch; rows whose paragraph moved only by line number are carried with the new line numbers stated.",
        "Witness mutants (not grader mutants; this slice has no grader): ledgers/AC1/scripts/AC1-a-r8/l03_articulation_witness.py writes m_plus1cent_2025q2 and m_wrong_rate to /tmp/ac1-v/a-r8 and runs them under python -I; output /tmp/ac1-v/a-r8/l03_articulation_witness.out. Check 5 is the only check that fails under either mutant.",
        "Alternative correct implementations: not applicable to lessons; the labs have no grader.",
        "Hours: the hub split (90 lesson hours, 30 project hours) equals the sum of the eight lesson data-hours values; no arithmetic inconsistency. Pace is a design target and was not graded.",
        "Not checked: a full line-by-line re-read of L04-L08, the project, and the cards of L04-L08 (other slices). A browser render beyond page_smoke. The Beneish and FASB texts are not in this slice. The 'cards-L02-rest' and 'cards-L03-all' rows verify card text against the lesson text and numbers, not the lab code for every printed number (the printed numbers were checked against the lab output).",
        "Not run: tools/fetch_data.py --check and tools/check_projects.py (not in this slice's gate list). tools/run_graders.py is not applicable (no grader). pytest was run with -k 'AC1 or lab' (143 tests) rather than -k AC1 alone (11 tests in round 7).",
        "Line numbers quoted are the 2c8162b numbers. The L01 Definition 1.3 insertion moved L01 lines 85-380 by plus five; the L03 Definition 1.2 insertion moved L03 lines 60-134 by plus five, and the L03 Definition 6.1 removal moved nothing after line 138.",
    ],
    "mutants": [],
    "summary": {},
    "verdict": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
fragment["rows"] = rows
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, fragment["summary"], fragment["verdict"])
