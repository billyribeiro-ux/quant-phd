"""Build the round-6 fragment for AC2 slice L01-L02 from the round-5 fragment and the round-6 re-checks."""
import json
import sys
from datetime import UTC, datetime

SRC = "/tmp/ac2-frags/L01-L02.round5.json"
OUT = "/tmp/verify-ac2r6-l12/ledgers/AC2/L01-L02.json"
L01_CARRY = "Carried from round 5 (course/modules/AC/AC2/L01.html, tests/labs/AC2/lab-AC2-L01-1.py byte-identical since 11b3477):"

FRESH = {
 "L01-L02-hub-hours": "R6 re-read index.html in full: data-hours-lessons=76 (line 29), data-hours-project=34, '110 hours' (line 31), card kickers 9, 10, 8, 9, 8, 10, 10, 12 h (lines 144-151) sum 76; 76+34=110; split 69.1%/30.9% (lines 39-42). L01.html line 2 data-hours=9 and L02.html line 2 data-hours=10 match their cards. The L05 card body (line 148) changed in the round-6 delta; its 8 h is unchanged. PASS.",
 "L01-L02-hub-prereqs": "R6 re-read index.html lines 35, 60-65: AC1, S0, S2 named; S2 carries S1 and M3 (line 60); L01 and L02 use only AC1/S0/S2 concepts (concept links resolve in check_dag and check_pages, run R6). PASS.",
 "L01-L02-hub-placement-count": "R6 re-read index.html lines 68-136: nine items: four AC1 (Pq1, gross-margin numeric, Pq3, Pq4), two S0 (median, Pq6), three skill checks (rung 1 as-of; rung 2 leverage 0.20/(0.10x0.50)=4.0; rung 2 ROIC 150/1000=0.15). 7/9=77.8%, 8/9=88.9%, so eight correct is the minimum at 80%. Line 70 states that no placement item tests S2 and says so. Answers recomputed. PASS.",
 "L01-L02-hub-links": "R6: check_pages --unit AC2 PASS (run R6); index.html L01/L02 card links and crumbs resolve to L01.html and L02.html, which exist. PASS.",
 "L01-L02-hub-objectives": "R6 re-read index.html lines 48-55: objective 1 (standardization, L01) and objective 2 (ratios and DuPont identity, L02 Theorem 3.2 and Lab 1) are taught on these pages. PASS.",
 "L01-L02-hub-honest-pending": "R6 re-read index.html lines 167-169: 'SIMULATED data only'; L01.html line 599 and L02.html line 613 label the filer SIMULATED. PASS.",
 "L01-L02-sec-reuse-statement-access": "R6 plain curl https://www.sec.gov/developer returned HTTP 403 (no bypass attempted). index.html line 169 says the statement was not read by automated access, which matches. PASS.",
 "L01-L02-data-request-open": "R6: plans/AC2-open-items.md exists (identical since 11b3477); index.html line 169 points to it. PASS.",
 "L01-L02-hub-core-reading": "R6 re-read index.html lines 172-180 (reading list keys penman2013financial, sloan1996stock, dechow1995detecting, piotroski2000value, beneish1999detection) and line 177 title 'Detecting Earnings Management' without authors; verify_refs --unit AC2 and --offline both report 0 problems (run R6). Rendered author list for dechow1995detecting is the registry's (ruling 1). PASS.",
 "L01-L02-check-pages-dag": "R6 run: check_pages --unit AC2: PASS; check_dag --unit AC2: PASS; check_projects --unit AC2: PASS.",
 "L01-L02-pagesmoke": "R6 run: page_smoke.py --unit AC2 --pages L01 L02 index: PASS for L01 (boot 1.1 s with numpy), L02 (lab 0.0 s), index; 'page_smoke AC2: PASS'.",
 "L01-L02-run-labs": "R6 run: run_labs.py --unit AC2 --page L01: PASS (1/1); --page L02: PASS (1/1).",
 "L01-L02-twins-isolated": "R6 run: python -I -W error on tests/labs/AC2/lab-AC2-L01-1.py rc 0 and lab-AC2-L02-1.py rc 0 (outputs in /tmp/ac2-v/l12/r6/).",
 "L01-L02-ruff-mypy-pytest": "R6 run: ruff check tests/labs/AC2 'All checks passed!' rc 0; ruff format --check: 11 files already formatted; mypy --no-incremental: no issues in 112 source files; pytest -q -k 'AC2 or lab': all passed.",
 "L01-L02-notation": "R6: the round-6 delta in L02.html is the Definition 4.1 title only (line 652); Definition 3.1 and 4.1 bodies use the same symbols (Rev, COGS, bar A, bar E). PASS.",
 "L01-L02-hub-penman-c": "R6 re-read index.html line 175 (data-cite penman2013financial) and the grade-C wording. The passage is not readable: registry entry is a bibliographic record; plain curl to its openlibrary URL returned HTTP 303. Judged on the page's own grade C with 'passage locator not confirmed' (ruling f). PASS.",
 "L01-L02-cards-changed": "R6 entry-level comparison of cards.json at 11b3477 and HEAD (script in ledgers/AC2/scripts/L01-L02-r6/): AC2-c014, c026, c031 and c120 are identical; the four changed entries are c075, c107, c123, c130 (L05, L08, L05, L07).",
 "L01-L02-cards-c134-c136": "R6 read c134, c135, c136 against Definition 4.1 (line 653): c134 year-end receivables over revenue times 365 and the 364/371-day remark; c135 current ratio and debt to assets on year-end balances; c136 gross margin. All match. Entries identical since 11b3477.",
 "L01-L02-process-jargon": "R6 grep over index.html, L01.html, L02.html for builder, this build, REQUESTS, unit report: no learner-text hits (the matches are code identifiers ITEMS and TAG_PRIORITY). PASS.",
 "L01-L02-lab-numbering": "R6: L01.html and L02.html each have one lab headed 'Lab 1' (L02.html line 86; L01 lab header). Hub and placement items reference 'Lesson N' labs by page. PASS.",
 "L01-L02-ladder-rungs": "R6 re-read index.html lines 155-163 and project.html lines 40-47: hub rung 1 worked example, rung 2 completion problem (dupont, roic, accrual with blanks), rung 3 independent project (modified_jones, piotroski_f_score, beneish_m_score named), rung 4 stretch. project.html says rungs 1 and 2 are Lab 1 and Lab 2 below and that placement-plus-skill-checks skip to rung 3, as the hub states. Consistent. PASS.",
 "L01-L02-placement-mastery": "R6: index.html line 68 data-mastery=0.8; line 70 '80% ... means eight correct, since seven is 78%' (7/9=77.8%). PASS.",
 "L01-L02-cards-duplicates": "R6 duplicate scan of cards.json: 140 entries, ids AC2-c001..c140 each once, fronts unique (case-insensitive). PASS.",
 "L01-L02-verify-refs": "R6 run: verify_refs.py --unit AC2 (live): 7 of 560 entries re-verified, 0 problems; verify_refs.py --offline: 560 entries, 0 problems.",
 "L01-L02-run-graders": "R6 run: run_graders.py --unit AC2: PASS (reference 50/50 seeds, slowest 0.3 s).",
 "L01-L02-companyfacts-fetch": "R6 plain curl https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json: HTTP 200, 3,789,099 bytes, entityName 'Apple Inc.', 503 us-gaap tags. Used only to confirm the company-facts shape; no real data is embedded (index.html line 169). PASS.",
 "L01-L02-lab-fidelity-sim": "R6 re-read L01.html key results (lines 754-760) and L02.html key results (lines 806-811): every simulated result is C with 'Lab 1 (SIMULATED)' named; T rows are proofs on the page. PASS.",
 "L01-L02-hub-ladder-seeds": "R6 re-read index.html line 161 ('Instances are generated from your workspace seed'). project.html line 239 says the same ('seeded by your workspace ID'); the grader's make_instance(seed) (course/modules/AC/AC2/grader/instance.py line 193) is deterministic per seed. The mapping from workspace ID to seed is outside this repository and is not checked here. PASS (claim matches the project page).",
 "L01-L02-hub-card-jones": "R6 re-read index.html line 149 (L06 card): it says the modified Jones model and 'the accrual-based models that Detecting Earnings Management evaluates'. That is a claim about the paper's content. Plain curl to the registry DOI 10.2308/tar-9505096112 returned HTTP 403 (no bypass attempted), so the paper body is not readable and the claim is UNVERIFIABLE here.",
 "L01-banned-about-90": "R6 grep over L01.html, L02.html, index.html for roughly, about, historically, typically, 'roughly half', '6%': no learner-prose hits; the only ellipsis is the quiz-stem cloze in index.html line 110.",
 "L01-cards": "R6 entry-level comparison: L01 entries AC2-c001..c016 and c120 are identical at 11b3477 and HEAD (none of the four changed cards is an L01 card). Cards read against L01.html. PASS.",
 "L01-lab-output-recomputed": "R6 compare: page code block equals tests/labs/AC2/lab-AC2-L01-1.py; L01 run output equals the expected block (18 of 18 lines verbatim) under python -I -W error.",
}
FAILS = {
 "L02-definition-4-1-title": "R6 re-read Definition 4.1 (line 652-653). The new title '(solvency, liquidity and margin ratios)' now names gross margin, so the round-5 defect (gross margin missing from the label) is fixed. The block still defines days sales outstanding (line 653, c134), which none of the three names covers, and the page never assigns DSO to a category. DSO is an activity-type ratio, so the label is incomplete for one of the four ratios it names. Minor, learner text only.",
 "L02-canon-section5": "R6 re-read Section 5 (lines 661-671). Bullet 1 (line 666) says 'The A15 engine's leverage factor is total assets over equity by contract'. The contract (atlas/A15.contract.md line 92) defines leverage as average total_assets / average equity, and Definition 3.1 (line 620) uses \\bar A/\\bar E. The bullet states the contract's factor without the averages. The other three bullets re-checked: 0.1838 vs 0.1925 (lab lines 602, 607) and the DSO and scale claims are correct.",
 "L02-quiz": "R6 re-read quiz (lines 822-885). The explanation of item L02q3 (line 842) says 'Section 5: the factor is total assets over equity', the same misstatement of the contract's average-based leverage factor (atlas/A15.contract.md line 92). The other items recomputed: 2.6786 (q2), 1.0909 (q4), 48 (q6), 0.3706 (q9, the 2024 row of the other-ratios table, line 599), and the q7 and q8 explanations match Example 4.2 and lab lines 610-611.",
}
GENERIC = {}
CARRY_IDS = {
 "L01-def1-1","L01-facts-shape","L01-tag-table","L01-real-tag-switch","L01-real-repeated-comparatives",
 "L01-real-10K-A-restatement","L01-real-ties","L01-fp-q4-real","L01-window-real","L01-def-2-1-M1",
 "L01-as-of-proofs","L01-tag-priority-proof","L01-numbers-prose","L01-M2-M3-cutoffs","L01-R2-growth",
 "L01-cross-ref-reference-request","L01-no-registry-edgar","L01-misconceptions","L01-quiz","L01-honest-data-page",
 "L01-problem-M2-lab-claim","L01-lab-365-comment","L01-key-tie-grade","L01-E3-l03-cross-ref",
}
L02_FRESH_TEXT = {
 "L02-lab-output-recomputed": "R6 compare (ledgers/AC2/scripts/L01-L02-r6/ and /tmp/ac2-v/l12/r6/l02_compare.py): the page code block (lines 88-586) equals tests/labs/AC2/lab-AC2-L02-1.py; python -I -W error run rc 0; output equals the expected block (lines 587-612): 26 of 26 lines verbatim. PASS.",
 "L02-hours": "R6 re-read L02.html line 2 data-hours=\"10\" and line 34 '10 study hours'; index.html card 'L02 · 10 h' (line 145). PASS.",
 "L02-defs": "R6 full re-read of L02.html: Definition 1.1 (lines 56-57), Definition 3.1 (619-622), Definition 4.1 (652-653, title changed in the delta, body unchanged). Definitions match the twin's code (dupont lines 431-446, current_ratio, gross_margin, debt_to_assets, days_sales_outstanding lines 449-472). PASS.",
 "L02-prop-1-2": "R6: Proposition 1.2 (lines 65-66) and proof (69-71) re-derived: ratio of money items unchanged by kappa; averages scale by kappa; shares excluded. The lab check 'ratios unchanged when every money item is multiplied by 1000: True' is printed at page line 609. PASS.",
 "L02-remark-2-1": "R6: Remark 2.1 (lines 81-82) re-derived: E_bar/E_t = (1+1/(1+g))/2, return ratio 2(1+g)/(2+g); at g=0.2 this is 1.0909 (9.1%). Problem R3 (lines 791-794) 0.9167 and 1.0909 recomputed. Lab FY2022 gap 0.1925 vs 0.1820 = 5.77% (lines 613, 682). PASS.",
 "L02-theorem-3-2": "R6: Definition 3.1 (619-622), Theorem 3.2 (625-627), proof (630-633) re-derived: the cancellations need one common average. Example 3.3 (635-637): 0.1179 x 0.8701 x 1.6936 = 0.17374, printed 0.1737; ROE 0.1738 (lab line 591). PASS.",
 "L02-prose-numbers": "R6 recomputed every number in L02 prose from the twin's raw filer values (twin functions imported without main; script in ledgers/AC2/scripts/L01-L02-r6/): restated FY2022 revenue 1,145,473,837 vs as-filed 1,131,891,143 (1131.9 x 1.012 = 1145.48); FY2022 receivables 135,826,937 = 0.12 x 1,131,891,143, giving DSO 43.80 on as-filed and 43.28 on restated revenue; net margin 0.1228 as filed, 0.1214 restated; FY2022 equity growth 12.26% (implied g 12.25% for the 5.77% gap, consistent with line 613). Line 637 product 0.17374; line 667 0.1838 vs 0.1925; line 682 5.77%; line 686; line 713 1.4%; line 755 -8.3%, -9.7%, -28.8%; line 794 0.9167, 1.0909. PASS.",
 "L02-E1-rounding-note": "R6: E1 solution (line 755) percentage changes -8.33%, -9.71%, -28.83% recomputed from the Lab 1 ROE column; 'the lesson reports the generator's shape' caveat present. PASS.",
 "L02-E2-E3": "R6: E2 (line 762) logs -0.2993 and -0.3400 from the four-digit values, and unrounded -0.2997, -0.0221, -0.0184 and total -0.3401 (lab lines 603-606), shares 88.1, 6.5, 5.4 summing to 100.0. E3 (line 769): 43.80 from 0.12 x 365; 43.28 = 43.80 x 1131.9/1145.5 recomputed. PASS.",
 "L02-M-problems": "R6: M1 (line 705): 750, 280, 0.6667, 2.6786, ROE 0.1786, ROA 0.0667 recomputed. M2 (line 712): 48.67 and 48.00, ratio 365/360 = 1.0139 (1.4%). M3 (line 719): 1.60 and 0.36. PASS.",
 "L02-P-problems": "R6: P1 (line 730), P2 (line 737: NI Abar/(A_t Ebar) form), P3 (line 744: log of a product is the sum; shares sum to one) re-derived step by step. PASS.",
 "L02-R-problems": "R6: R1 (line 780), R2 (line 787: the A15 table has no short-term debt item, as contract lines 117 and 171 state), R3 (line 794) re-derived. PASS.",
 "L02-twin-tie-rule": "R6: the _observation and _as_of_pick functions in tests/labs/AC2/lab-AC2-L02-1.py are identical to the L01 twin (sed-extracted diff empty). Tie rule (twin lines 246-257) matches the contract wording and the lab's tie output (page lines 607-608). PASS.",
 "L02-penman-grade-C": "R6 re-read lines 62, 669 and 811: each is graded C with 'passage locator not confirmed'. The Penman text is not readable (registry entry is a bibliographic record; plain curl to its openlibrary URL returned HTTP 303). Judged on the page's own C grade (ruling f). PASS.",
 "L02-cards": "R6: L02 cards c017-c031 and c134-c136 identical at 11b3477 and HEAD (entry-level comparison); c134-c136 re-read against Definition 4.1; c017-c031 read against their lessons' text (unchanged). PASS.",
 "L02-banned-phrases": "R6 grep over L02.html learner text for roughly, about, historically, typically, builder, this build, REQUESTS, unit report, ellipsis: no hits in prose; the one ellipsis is the quiz-stem cloze in index.html line 110. PASS.",
 "L02-definition-4-1": "R6 re-read Definition 4.1 body (line 653): three year-end ratios (current ratio, debt to assets, DSO) match lab header line 593 and code (current_ratio, debt_to_assets, days_sales_outstanding use year-end items); gross margin 'uses no balance' matches gross_margin(). PASS.",
 "L02-misconceptions": "R6 re-read lines 676-691. 'all fall together in each year pair' checked: all three factors fall between 2021-22, 2022-23 and 2023-24 in the printed table. 5.8% gap (line 682) and 0.1838 (line 686) checked. Line 678 says the factor is 'an accounting ratio of total assets to equity' without the averaging; no false fact is asserted, so it is noted, not failed. PASS.",
 "L02-example-4-2": "R6: DSO 43.28 (restated) and 43.80 (as filed) recomputed from the twin's raw values; net margin 0.1228 as filed (139,034,569 / 1,131,891,143) and 0.1214 restated. 'Receivables carry no restatement' holds: the 10-K/A row (twin line 383) is revenue-only. PASS.",
 "L02-quiz-Q7": "R6: item L02q7 (lines 864-870). The lab's standardize(filer) has no cut-off, so it includes the 10-K/A restated revenue filed 2024-03-01 (twin line 383). Explanation matches Example 4.2. PASS.",
 "L02-definition-4-1-note": "R6: cards AC2-c134 (DSO: year-end receivables over revenue times 365; 364/371-day remark) and AC2-c135 (current ratio and debt to assets) match Definition 4.1 body (line 653). PASS.",
 "L02-lab-header-gross-margin-basis": "R6: hypothesis (line 87) 'the other ratios ... of which the current ratio, debt to assets and DSO use year-end balances and gross margin uses no balance' and printed header (line 593) 'year-end balances, except gross margin, which uses only the year's flows' match gross_margin() and the table. PASS.",
}

def main() -> int:
    frag = json.load(open(SRC, encoding="utf-8"))
    rows = []
    for row in frag["rows"]:
        rid = row["id"]
        new = dict(row)
        body = row["evidence"]
        if rid in FAILS:
            new["status"] = "FAIL"
            new["evidence"] = FAILS[rid]
            new["fix"] = {
                "L02-definition-4-1-title": "Use '(solvency, liquidity, activity and margin ratios)', or name the four ratios without a category label, in L02.html line 652.",
                "L02-canon-section5": "In L02.html line 666 replace 'total assets over equity' with 'average total assets over average equity (the contract's leverage factor, Definition 3.1)'; keep the one-plus-liabilities-over-equity argument for year-end values, labelled as such.",
                "L02-quiz": "In L02.html line 842 replace 'the factor is total assets over equity' with 'the factor is average total assets over average equity', matching Definition 3.1.",
            }[rid]
        elif rid == "L01-L02-hub-card-jones":
            new["status"] = "UNVERIFIABLE"
            new["evidence"] = FRESH[rid]
            new["fix"] = "Verify the paper's content with a readable source (the DOI returned HTTP 403 to plain curl), or reword the L06 card to cite the paper by key and title for the claim it makes without asserting what it evaluates."
        elif rid in FRESH:
            new["evidence"] = FRESH[rid]
        elif rid.startswith("L02-"):
            new["evidence"] = L02_FRESH_TEXT[rid]
        elif rid in CARRY_IDS or (rid.startswith("L01-") and rid not in ("L01-cards", "L01-lab-output-recomputed", "L01-banned-about-90", "L01-L02-lab-fidelity-sim", "L01-L02-cards-changed") and not rid.startswith("L01-L02")):
            # L01 subject unchanged since 11b3477: carry the round-5 evidence body under the exact prefix.
            marker = "): "
            cut = body.find(marker)
            tail = body[cut + len(marker):] if body.startswith("Carried from round 4 (") and cut >= 0 else body
            new["evidence"] = L01_CARRY + " " + tail
        else:
            raise SystemExit(f"row {rid} has no round-6 treatment")
        assert new["status"] in ("PASS", "FAIL", "UNVERIFIABLE")
        rows.append(new)
    ids = [r["id"] for r in rows]
    assert ids == [r["id"] for r in frag["rows"]], "row ids must be kept in order"
    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in rows:
        counts[r["status"]] += 1
    out = {
        "unit": "AC2",
        "slice": "L01-L02",
        "round": 6,
        "verifier": "independent round-6 verifier for AC2 slice L01-L02 (fresh context; round-5 fragment used as context only; L02.html read in full; index.html read in full; L01 subject carried by byte-identity)",
        "pin": "ff9284f",
        "base": "11b3477",
        "checkout": "/tmp/verify-ac2r6-l12 (detached at ff9284f)",
        "scratch": "/tmp/ac2-v/l12/r6",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "FAIL",
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Delta 11b3477..ff9284f for this slice: L02.html line 652 (Definition 4.1 title only); cards.json entries c075, c107, c123, c130 (not L01/L02 cards); index.html line 148 (L05 card body only). L01.html, the L01 and L02 twins, plans/, references/, course/assets/, tools/, atlas/ are byte-identical since 11b3477.",
            "The L02.html delta is a single title line, but L02 rows were re-verified from a full re-read rather than carried, because round 5 carried several L02 rows across changed hunks.",
            "The round-5 FAIL L02-definition-4-1-title is re-verified: the gross-margin defect is fixed, but the new label still omits DSO. Still FAIL, minor.",
            "New FAILs: L02-canon-section5 (line 666) and L02-quiz (line 842) state the engine's leverage factor as total assets over equity; the contract's factor uses averages.",
            "L01-L02-hub-card-jones is UNVERIFIABLE: the paper body is not readable (DOI plain curl 403).",
            "Honest gaps carried: the dechow1995detecting body, the Penman passage locator, and the workspace-ID-to-seed mapping are not checkable from the repository.",
            "The hub's claim about what no placement item tests (S2) is confirmed by reading all nine items (ruling 6).",
        ],
        "rows": rows,
        "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]},
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(out["summary"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
