"""Round-1 closing-delta verifier for E3 slice g: builds ledgers/E3/E3-g.json from the base fragment and the delta checks."""
import json
import datetime

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyG1-E3-g"
BASE = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round18.json", encoding="utf-8"))
base_rows = {r["id"]: r for r in BASE["rows"]}
OUT = "/Users/billyribeiro/.fanout/wt/verifyG1-E3-g/ledgers/E3/scripts/E3-g-r1/out"
PIN_BASE = "4540351dc664559cdfd371b908f2b4e644cf4297"
PIN_HEAD = "2a805c831410ab77c38c227f7e121e8537193ce9"

rows = []


def carry(rid, files):
    b = base_rows[rid]
    assert b["status"] == "PASS", rid
    rows.append({
        "id": rid,
        "check": b["check"],
        "location": b["location"],
        "status": "PASS",
        "evidence": f"Carried from round 18 ({files} byte-identical since the previous pin {PIN_BASE}): " + b["evidence"],
    })


def fresh(rid, status, check, location, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)


CARD_L05 = ("the cards.json entry and the L05.html blocks it cites; the only changed L05.html lines since "
            f"{PIN_BASE[:8]} are 499 (key-results row, Remark 3.4 summary) and 620 (footer), which this card does not cite")
CARD_L06 = ("the cards.json entry and the L06.html blocks it cites; the only changed L06.html line since "
            f"{PIN_BASE[:8]} is 545 (footer), which this card does not cite")
CARD_L07 = ("the cards.json entry and the L07.html blocks it cites; the changed L07.html lines since "
            f"{PIN_BASE[:8]} are 44 (legend), 80 (Section 1 attribution sentence), 462-463 (key-results row) and 570 (footer), none cited by this card")
CARD_L08 = ("the cards.json entry and the L08.html blocks it cites; the changed L08.html lines since "
            f"{PIN_BASE[:8]} are 44, 67, 133, 479, 619-620 and 723, none in the blocks this card cites")

# ---- delta rows (new subject checks) ----
fresh("E3g19-delta-inventory", "PASS",
      "2.9 delta 4540351d..2a805c83 inside slice g (L05-L08 pages, cards.json, twins)",
      "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html, cards.json; tests/labs/E3 (unchanged)",
      "git diff --stat 4540351d..2a805c83 -- course/modules/E/E3: L05.html 4 lines, L06.html 2, L07.html 7, L08.html 12, cards.json 20 (c037, c134, c157, c158 changed; 178 cards before and after). "
      "git diff --quiet 4540351d 2a805c83 -- tests/labs/E3 course/modules/E/E3/grader: unchanged, so no twin or grader changed. "
      "Outside slice g and recorded only, not rated: L03.html (Proposition 1.2 renamed b to Lambda, line 78 and proof line 83; interpretation text line 326) and project.html line 648.")
fresh("E3g19-c037", "PASS",
      "2.7 card E3-c037 (changed in the delta, cards.json is a slice path) against L03 Proposition 1.2",
      "course/modules/E/E3/cards.json E3-c037; course/modules/E/E3/L03.html lines 77-78 (Proposition 1.2 statement) and 82-83 (proof)",
      "Card back now reads 'For w > 0 and real iota and Lambda, (w^iota)^Lambda = w^(iota Lambda) (Proposition 1.2).' L03.html line 78 has \\(w > 0\\), real \\(\\iota\\), \\(\\Lambda\\): \\((w^{\\iota})^{\\Lambda} = w^{\\iota \\Lambda}\\), matching the card. "
      "Notation: Lambda is not in notation/notation.json (program-wide registry only, which lists no iota or Lambda); grep of course/modules/E/E3/*.html finds Lambda only at L03.html lines 78 and 83, so no other meaning is reused. Grade T matches the proposition's proof on line 83.")
fresh("E3g19-L05-remark34-row", "PASS",
      "2.2/2.3 changed key-results row 'deterministic MRS exponents ... so their marginal rates of substitution differ off psi = 1/gamma (Remark 3.4)' against Remark 3.4",
      "course/modules/E/E3/L05.html line 499 (row) against lines 220-221 (Remark 3.4) and the R3 solution line 640 (stripped L05 text)",
      "Remark 3.4 (L05.html line 221) gives MRS_U = (1-beta)/beta (c1/c0)^gamma and MRS_EZ = (1-beta)/beta (c1/c0)^(1/psi) (Proposition 2.2). They coincide at c1 = c0 (both equal (1-beta)/beta, R3 solution line 640) and differ at every plan with c1 != c0 unless 1/psi = gamma. "
      "So 'their marginal rates of substitution differ off psi = 1/gamma' is correct as a statement about the two functions (the earlier 'criteria differ' was the looser wording). Grade T with basis 'Proved in §3 from Proposition 2.2' is consistent.")

# ---- changed-subject FAIL rows ----
FOOTER_FIX = ("Make the L05-L08 footer true of the page, or restore the L01-L04 footer wording and make the grade legend and footer agree across E3. "
              "Restore each attribution as a graded claim (<span class=\"claim\" data-grade=\"C\" data-cite=\"<key>\" data-locator=\"registry record: title only; paper not read\">) "
              "with the registry key, or delete the sentence; restore grade C and cite on E3-c134, E3-c157 and E3-c158 (or delete them); do not weaken tools/check_pages.py.")
fresh("E3g18-grade-legend-footer", "FAIL",
      "2.3/2.9 grade C legend, grade-C rows and the site footer on L05-L08 against BLUEPRINT section 3 and the verifier evidence standard",
      "course/modules/E/E3/L05.html line 620, L06.html line 545, L07.html line 570, L08.html line 723 (footer); L07.html line 47 and L08.html line 47 (legend); L05.html lines 500-502 (grade-C lab rows); L07.html line 80; L08.html lines 67, 133, 479",
      "The footer on all four pages reads 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry' (the BLUEPRINT section 3 sentence). "
      "Measured at 2a805c83 (grep -c): claim spans 0/0/0/0 and data-cite attributes 0/0/0/0 on L05/L06/L07/L08; at 4540351d the same pages had 0/0/1/2 claim spans and 0/0/1/2 data-cite attributes. "
      "So no page satisfies the footer. Substantive claims with no grade and no key: L07.html line 80 (name in the title of the 1979 paper), L08.html line 67 (maxmin title sentence), L08.html line 133 (Ellsberg title sentence), L08.html line 479 (two named sources). "
      "Grade-C lab rows at L05.html lines 500-502 carry only a 'Lab 1' basis and no key. "
      "L07.html line 80 and L08.html lines 67 and 133 say the page 'cites it', but no citation key for kahneman1979prospect, gilboa1989maxmin or ellsberg1961risk appears in L07.html or L08.html, and their references lists are empty (`<ol data-references></ol>`). "
      "The footer differs from L01.html line 576, L02.html line 627, L03.html line 575 and L04.html line 728, which all still say 'Each graded result carries a proof or a lab result labelled C.' "
      "The legend on L05-L08 now reads 'single study or lab result' (L03-L06 line 46/47; L01 and L02 line 46 still say 'single study'). Lab results as C is consistent with verifier rule 9, so the legend itself is not the defect. "
      "Gates pass because tools/check_pages.py checks grades and keys only on <span class=\"claim\"> elements (lines 128-142), and the delta removed those spans. "
      "Re-verified by: grep -c and python count on the four pages; git show 4540351d:<page> counts; sed of the footer, legend and quoted sentences. Gate outputs in ledgers/E3/scripts/E3-g-r1/out/.",
      FOOTER_FIX)
fresh("E3g12-c134", "FAIL",
      "2.7 retrieval card E3-c134 against L07 (changed: grade and cite removed)",
      "course/modules/E/E3/cards.json E3-c134; course/modules/E/E3/L07.html line 80",
      "Card text agrees with L07.html line 80 and with the registry record kahneman1979prospect (title 'Prospect Theory: An Analysis of Decision under Risk', Kahneman and Tversky, 1979, references/references.json). "
      "The delta removed the card's grade C and cite kahneman1979prospect, so the card now states a bibliographic attribution with no grade and no key, contrary to BLUEPRINT section 3 which the L07 footer asserts. Shares root cause with E3g18-grade-legend-footer.",
      "Restore grade C and cite kahneman1979prospect on E3-c134 with the basis 'registry record: title only', or remove the attribution from the card and the page.")
fresh("E3g12-c157", "FAIL",
      "2.7 retrieval card E3-c157 against L08 (changed: grade and cite removed)",
      "course/modules/E/E3/cards.json E3-c157; course/modules/E/E3/L08.html line 133",
      "Card text agrees with L08.html line 133 and the registry record ellsberg1961risk (title 'Risk, Ambiguity, and the Savage Axioms', 1961). The delta removed grade C and the cite, so the card's attribution is ungraded and unkeyed, contrary to BLUEPRINT section 3. Shares root cause with E3g18-grade-legend-footer.",
      "Restore grade C and cite ellsberg1961risk with the basis 'registry record: title only', or remove the attribution.")
fresh("E3g12-c158", "FAIL",
      "2.7 retrieval card E3-c158 against L08 (changed: grade and cite removed)",
      "course/modules/E/E3/cards.json E3-c158; course/modules/E/E3/L08.html line 67",
      "Card text agrees with L08.html line 67 and the registry record gilboa1989maxmin (title 'Maxmin expected utility with non-unique prior', Gilboa and Schmeidler, 1989). The delta removed grade C and the cite, so the attribution is ungraded and unkeyed, contrary to BLUEPRINT section 3. Shares root cause with E3g18-grade-legend-footer.",
      "Restore grade C and cite gilboa1989maxmin with the basis 'registry record: title only', or remove the attribution.")
fresh("E3g15-attributions", "FAIL",
      "2.3/2.5 bibliographic attributions in L07 and L08 (title-only uses)",
      "references/references.json entries kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin (read directly); course/modules/E/E3/L07.html line 80; L08.html lines 67, 133, 479",
      "Every title, author and year stated in the four sentences matches references/references.json (Kahneman and Tversky 1979; Ellsberg 1961; Gilboa and Schmeidler 1989; 'Its two named sources' = Gilboa and Schmeidler and Ellsberg, L08 lines 67 and 133). "
      "But the delta moved these from claim spans with data-cite to plain prose, so they now carry no grade and no citation key, while the page says it cites them. Same defect as E3g18-grade-legend-footer; the facts themselves are correct.",
      "Use the claim span with data-grade C, data-cite and data-locator for each registry-title sentence, or delete them; make L07 and L08 references lists match what the text says.")
fresh("E3g18-page-structure-footers", "FAIL",
      "2.9 structure: page footers and the L05-L08 hub links after the delta",
      "course/modules/E/E3/L05.html line 620, L06.html line 545, L07.html line 570, L08.html line 723 (footers); the Previous/Next links and section order",
      "Structure passes: tools/check_pages.py --unit E3 --page L05..L08 printed 'PASS' for all four (ledgers/E3/scripts/E3-g-r1/out/check_pages_L0x.out), and the section order and links are untouched by the hunks. "
      "The footer text is the failing part: it asserts a standard that the page does not meet (see E3g18-grade-legend-footer, which holds the evidence).",
      "Fix the footer text as in E3g18-grade-legend-footer; the structure needs no change.")

# ---- changed-subject PASS rows (fresh) ----
fresh("E3g12-c137", "PASS", "2.7 retrieval card E3-c137 against L08 Definition 1.2 (block changed by one attribution sentence)",
      "course/modules/E/E3/cards.json E3-c137; course/modules/E/E3/L08.html line 67 (Definition 1.2)",
      "Card formula V_tau = tau min + (1 - tau) max and CE = u^-1(V_tau) match L08.html line 67 (\\(V_\\tau(f) = \\tau \\min ... + (1 - \\tau)\\max\\) and \\(\\mathrm{CE}(f) = u^{-1}(V_\\tau(f))\\)). The changed sentence is the attribution, which the card does not state.")
fresh("E3g12-c172", "PASS", "2.7 retrieval card E3-c172 against L08 Definition 1.2 (tau = 1 gives the minimum)",
      "course/modules/E/E3/cards.json E3-c172; course/modules/E/E3/L08.html line 67",
      "Card 'V_tau(f) at tau = 1 equals min over P of E_P u(f)' matches L08.html line 67 ('at \\(\\tau = 1\\), which equals \\(\\min_{P} \\E_P\\, u(f)\\)'). The changed sentence (the title attribution) is not stated on the card.")
fresh("E3g12-c144", "PASS", "2.7 retrieval card E3-c144 against L08 Example 2.5 (block changed in its second paragraph only)",
      "course/modules/E/E3/cards.json E3-c144; course/modules/E/E3/L08.html Example 2.5 first paragraph (line 132)",
      "Card '103125 cents' is in the first paragraph of Example 2.5, byte-identical since 4540351d. Recomputed by hand: CE = u^-1 of (1/3)u(110000) + (2/3)u(100000) with u = -1/w gives 1650000/16 = 103125 (ledgers/E3/scripts/E3-g-r1/out/numbers_L05_L08.out, identical to the base output). The changed second-paragraph sentence (the Ellsberg title, line 133) is not on the card.")
fresh("E3g12-c164", "PASS", "2.7 retrieval card E3-c164 against L08 Example 2.5 and Proposition 2.4",
      "course/modules/E/E3/cards.json E3-c164; course/modules/E/E3/L08.html Example 2.5 (line 132) and Proposition 2.4",
      "Card's 100000 cents for red and black and worst priors P_0 and P_90 match the first paragraph of Example 2.5 (byte-identical). numbers_L05_L08.out does not print the ambiguous-urn 100000 values, so they were re-derived by hand: under P_0 (no red balls) the red bet pays 0, so final wealth is 100000 surely, and under P_90 (no black balls) the black bet pays 0, so final wealth is 100000 surely; these are the worst priors (Proposition 2.4), so maxmin gives 100000 for both colours. The changed sentence (line 133) is not on the card.")
fresh("E3g12-c165", "PASS", "2.7 retrieval card E3-c165 against L08 Example 2.5",
      "course/modules/E/E3/cards.json E3-c165; course/modules/E/E3/L08.html Example 2.5 (line 132)",
      "Card 'the known urn's certainty equivalent exceeds 100000 cents for red and for black' matches the first paragraph of Example 2.5, byte-identical; the known-urn CE values 103125 and 106451.6129 are recomputed in numbers_L05_L08.out (identical to base). The changed sentence (line 133) is not on the card.")
fresh("E3g12-c182", "PASS", "2.7 retrieval card E3-c182 against L08 Example 2.5 (black bet)",
      "course/modules/E/E3/cards.json E3-c182; course/modules/E/E3/L08.html Example 2.5 first paragraph",
      "Card '106451.6129 cents' matches the first paragraph of Example 2.5; recomputed 3300000/31 = 106451.6129 in numbers_L05_L08.out (identical to base). The changed sentence is not on the card.")
fresh("E3g12-L05-L08-key-results", "PASS", "2.3 grades in the Key results tables of L05-L08 against proofs and lab output (rows changed in the delta)",
      "course/modules/E/E3/L05.html line 499 (changed row), section 7 lines 489-507; L07.html lines 462-463 (removed row), section 6 lines 451-467; L08.html lines 619-620 (removed rows), section 8 lines 607-624",
      "The changed L05 row is re-verified in E3g19-L05-remark34-row. The L07 row removed (C, 'Registry record kahneman1979prospect (title only)') and the two L08 rows removed (C, ellsberg1961risk and gilboa1989maxmin, title only) leave the remaining rows byte-identical per the diff hunks, and every remaining row's grade is unchanged. "
      "The removal leaves the title sentences ungraded in prose, which is the defect in E3g18-grade-legend-footer, not a key-results error.")
fresh("E3g15-L07-changes", "PASS", "2.2/2.3 L07 changed text (why-it-matters, Remark 1.6, Example 1.4 reference, section 4 third misconception, section 6 key results)",
      "course/modules/E/E3/L07.html Remark 1.6, section 4 misconceptions (328-345), section 6 key results (451-467)",
      "Delta changes to L07 within these items: only the removed key-results row (lines 462-463) and the legend and footer; Remark 1.6, the Example 1.4 reference, and the section 4 misconceptions are byte-identical since 4540351d. The key-results change is re-verified in E3g12-L05-L08-key-results.")
fresh("E3g12-L05-prose-numbers", "PASS", "2.2 numbers in L05 prose after the delta",
      "course/modules/E/E3/L05.html Remark 1.5, Definition 2.1, Proposition 2.2 proof, Remark 2.3, Remark 3.4, Problems P1-E3 (stripped L05 text)",
      "numbers_L05_L08.py (run in the checkout) reproduces the base output (diff of 98 lines empty; ledgers/E3/scripts/E3-g-r1/out/numbers_L05_L08.out). The numeric tokens added in the L05 hunks (1/2, 2.5, 3.4, 2.2, 1.2, 1979, 1961, 1989 and 0) all appear in the base text; the L05 added line at 499 carries no new number.")
fresh("E3g12-L06-prose-numbers", "PASS", "2.2 numbers in L06 prose after the delta",
      "course/modules/E/E3/L06.html (the only changed line is the footer, 545)",
      "numbers_L05_L08.py output identical to base for the L06 items; the only L06 change is the footer (no number).")
fresh("E3g12-L07-prose-numbers", "PASS", "2.2 numbers in L07 prose after the delta",
      "course/modules/E/E3/L07.html lines 44, 80, 462-463, 570 (changed); Example 1.4, Observation 1.5, Remarks 1.6, 2.3, Proposition 2.2, section 4",
      "numbers_L05_L08.py output identical to base (ledgers/E3/scripts/E3-g-r1/out/numbers_L05_L08.out). The changed L07 sentences carry no computed number (only the year 1979, which the registry record gives as 1979, references/references.json kahneman1979prospect).")
fresh("E3g12-L08-prose-numbers", "PASS", "2.2 numbers in L08 prose after the delta",
      "course/modules/E/E3/L08.html lines 44, 67, 133, 479, 619-620, 723 (changed); Example 1.4, Example 2.5, Remark 2.3, section 4 models, Remark 4.2",
      "numbers_L05_L08.py output identical to base. The changed L08 sentences keep every numeric value (the tau values, 1/2, lambda = 2, gamma = 2, 1961, 1989) and add none; 1961 and 1989 match references/references.json ellsberg1961risk and gilboa1989maxmin.")
fresh("E3g12-scope-words-cards", "PASS", "2.9 scope words (only, all, always, every, any, same, exactly) in changed cards",
      "course/modules/E/E3/cards.json E3-c134, E3-c157, E3-c158",
      "'used for its title only' (c134), 'Only its registry title' (c157), 'Only the name' (c158) are each backed by the registry record title and by the L07/L08 sentences that state no result from the work. The word 'every' in the L05-L08 footer is the scope word checked in E3g18-grade-legend-footer.")
fresh("E3g12-process-words-cards", "PASS", "2.9 process words in learner text (changed cards and L05-L08 changed lines)",
      "cards.json E3-c134, c157, c158; L05.html 499-620; L06.html 545; L07.html 44-80, 462-463, 570; L08.html 44-133, 479, 619-620, 723",
      "Scan of the added lines (git diff -U0 4540351d 2a805c83, grep -i for ledger, verif, round, builder, agent, audit, fixed, revis, changed, correct, draft, reviewer, delta, now) found no process narration. 'this page has not read the paper' is an evidence-basis disclosure. The footer uses 'verified registry', the BLUEPRINT term, not a process word.")
fresh("E3g12-notation", "PASS", "2.4/2.9 notation: symbols in changed L05-L08 text and cards against notation/notation.json",
      "notation/notation.json (program-wide symbols only); course/modules/E/E3/*.html; cards.json E3-c037",
      "notation.json is unchanged in the delta (git diff quiet). The only new symbol is Lambda in E3-c037 and L03 (local to L03, not registered, not used with another meaning in E3 pages). The changed L05-L08 text reuses psi, gamma, beta, c0, c1, MRS and CE with their existing meanings.")
fresh("E3g18-omega-notation", "PASS", "2.4/2.9 notation: Omega and PV against notation/notation.json and the E3 unit",
      "course/modules/E/E3/L05.html, L06.html, L08.html; cards.json E3-c078, c080, c145; tests/labs/E3 (unchanged)",
      "grep -n 'Omega|PV' over L05-L08.html gives 64 matching lines; grep -c Omega: cards.json 3, twin lab-E3-L05-1.py 3, lab-E3-L08-1 0, lab-E3-L06-1 0; the delta touched no Omega line (hunks at 499, 620, 545, 44, 67, 133, 479, 619-620, 723). Omega is local to E3 L05 and L08 and is not registered; no program-wide meaning is reused.")
fresh("E3g18-rename-complete", "PASS", "2.4 renames complete: a -> Omega (L05-L08, cards, twins) and W -> PV (L06, cards c100-c116)",
      "course/modules/E/E3/L05.html, L06.html, L08.html, cards.json; tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py",
      "grep for residual 'a = 1 - 1/psi' and '\\(a\\)' in L05/L08 returns only Omega text (false positives on 'Omega = 1 - 1/psi'); no residual W = sum in L06 (grep). PV matches 38 lines in L06.html. The delta changed none of these renamed lines.")
fresh("E3g12-check-pages-dag-projects", "PASS", "2.9 structure and DAG: check_pages (L05-L08), check_dag, check_projects for E3",
      "tools/check_pages.py --unit E3 --page L05..L08; tools/check_dag.py --unit E3; tools/check_projects.py --unit E3",
      "Re-run at 2a805c83 (ledgers/E3/scripts/E3-g-r1/gates.sh; out/check_pages_L05..L08.out, check_dag_unit.out, check_projects_unit.out): 'check_pages E3 L05: PASS' (and L06-L08), 'check_dag E3: PASS', 'check_projects E3: PASS'. Note that check_pages does not test the footer or claims that are not claim spans (see E3g18-grade-legend-footer).")
fresh("E3g12-verify-refs", "PASS", "2.1 citations: offline integrity (verify_refs --offline); references/references.json unchanged",
      "tools/verify_refs.py --offline; references/references.json (kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin, epstein1989substitution)",
      "Re-run at 2a805c83: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out, rc 0). references/references.json and tools/ are byte-identical across the delta, so the live Crossref run is carried, not repeated.")
fresh("E3g12-card-numbers", "PASS", "2.7 every number on a card appears in its lesson (token match)",
      "course/modules/E/E3/cards.json (178 cards); stripped L05-L08 text",
      "Re-run at 2a805c83: ledgers/E3/scripts/E3-g-r1/card_numbers.py <checkout> printed 'cards 178 unique ids True', 'duplicate fronts []', and no 'numbers not in lesson text' line (out/card_numbers.out).")
fresh("E3g12-dup-scan", "PASS", "2.7 full scan for duplicate cards (all 178 E3 cards)",
      "course/modules/E/E3/cards.json (178 cards)",
      "Re-run at 2a805c83: 178 cards, 178 unique ids, no duplicate fronts (out/card_numbers.out). Card count unchanged from 4540351d.")
fresh("E3g12-lab-twins-run", "PASS", "2.5 labs: twins alone under python -I -W error (lessons whose cards are in this slice)",
      "tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py",
      "Re-run alone: python3 -I -W error on each twin exits 0 with empty stderr (out/twin_L05..L08.stdout/.stderr). twin_check.py <checkout>: page_code_equals_twin=True and expected_equals_stdout=True for all four (out/twin_check.out, identical to base). tests/labs/E3 is byte-identical across the delta.")
fresh("E3g18-twins-run", "PASS", "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout",
      "tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py; course/modules/E/E3/L05-L08.html lab sections",
      "Same run as E3g12-lab-twins-run: exit 0, empty stderr, and page_code_equals_twin and expected_equals_stdout True for L05-L08 (out/twin_check.out). run_labs.py --unit E3 --page L05..L08 printed 'run_labs E3: PASS (1/1)' for each (out/run_labs_L0x.out).")
fresh("E3g14-page-smoke", "PASS", "2.5 lab timing and 2.9 render checks", "tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08",
      "Re-run at 2a805c83: 'page_smoke modules/E/E3/L08.html: PASS' and 'page_smoke E3: PASS' (out/page_smoke_L05_L08.out, rc 0).")
fresh("E3g14-ruff-mypy", "PASS", "2.9 gates: ruff, ruff format, mypy", "tests/labs/E3; course/modules/E/E3/grader; mypy strict config",
      "Re-run: ruff check tests/labs/E3 course/modules/E/E3/grader 'All checks passed!'; ruff format --check tests/labs/E3 rc 0; mypy --no-incremental 'Success: no issues found in 386 source files' (out/ruff_check.out, ruff_format.out, mypy.out).")
fresh("E3g14-pytest-relevant", "PASS", "2.9 gates: relevant pytest",
      "tests/test_docs_figures.py, tests/test_refs.py (re-run); tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py (carried)",
      "Re-run: pytest -q tests/test_docs_figures.py tests/test_refs.py rc 0 (out/pytest_docs.out) and pytest -q tests -k 'E3 or e3' rc 0 (out/pytest_labs_E3.out). The other four modules and tools/ are byte-identical across the delta (git diff --quiet), so they are carried.")
for lesson in ("L05", "L06", "L07", "L08"):
    fresh(f"E3g14-lab-{lesson}-printed", "PASS", "2.5 lab printed values recomputed",
          f"tests/labs/E3/lab-E3-{lesson}-1.py; course/modules/E/E3/{lesson}.html expected block",
          f"Re-run: run_labs.py --unit E3 --page {lesson} 'run_labs E3: PASS (1/1)' (out/run_labs_{lesson}.out); twin run alone exit 0 and expected block equals stdout (out/twin_check.out).")
fresh("E3g15-numbers", "PASS", "2.2/2.5 independent recomputation of the numbers printed or stated in the slice (L05-L08)",
      "ledgers/E3/scripts/E3-g-r1/numbers_L05_L08.py; out/numbers_L05_L08.out",
      "Re-run at 2a805c83: output byte-identical to the round-18 base (diff empty).")
fresh("E3g15-gate-check-and-build", "PASS", "2.9 build and render gates for the slice",
      "tools/build_site.py --check; tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
      "Re-run: build_site --check 'site data current: 6 outputs'; render_curriculum rc 0; git diff exit 0 (out/build_site_check.out, render_curriculum_diff.out).")
fresh("E3g15-gate-run-labs", "PASS", "2.5 run_labs for L05-L08 (program-wide lab runner)",
      "tools/run_labs.py --unit E3 --page L05..L08", "Re-run: 'run_labs E3: PASS (1/1)' for L05, L06, L07, L08 (out/run_labs_L0x.out).")
fresh("E3g18-c106-basis", "PASS", "2.3 grade and basis fields of card E3-c106", "cards.json E3-c106", "Card unchanged in the delta (cards.json diff lists only c037, c134, c157, c158); carried below as well.") if False else None

# ---- carried rows (subject byte-identical) ----
L05_CARDS = ["E3g12-c078", "E3g12-c079", "E3g12-c080", "E3g12-c081", "E3g12-c082", "E3g12-c083", "E3g12-c084",
             "E3g12-c085", "E3g12-c086", "E3g12-c087", "E3g12-c088", "E3g12-c089", "E3g12-c090", "E3g12-c091",
             "E3g12-c093", "E3g12-c094", "E3g12-c095", "E3g12-c096", "E3g12-c169", "E3g12-c170", "E3g12-c184",
             "E3g12-c185"]
L06_CARDS = ["E3g12-c098", "E3g12-c099", "E3g12-c100", "E3g12-c101", "E3g12-c102", "E3g12-c103", "E3g12-c104",
             "E3g12-c105", "E3g12-c106", "E3g12-c107", "E3g12-c108", "E3g12-c109", "E3g12-c110", "E3g12-c111",
             "E3g12-c112", "E3g12-c113", "E3g12-c116", "E3g12-c117", "E3g12-c163"]
L07_CARDS = ["E3g12-c118", "E3g12-c119", "E3g12-c120", "E3g12-c121", "E3g12-c122", "E3g12-c123", "E3g12-c124",
             "E3g12-c125", "E3g12-c126", "E3g12-c127", "E3g12-c128", "E3g12-c129", "E3g12-c130", "E3g12-c132",
             "E3g12-c133", "E3g12-c135", "E3g12-c187"]
L08_CARDS = ["E3g12-c136", "E3g12-c138", "E3g12-c139", "E3g12-c140", "E3g12-c141", "E3g12-c142", "E3g12-c143",
             "E3g12-c145", "E3g12-c146", "E3g12-c147", "E3g12-c148", "E3g12-c149", "E3g12-c150", "E3g12-c151",
             "E3g12-c152", "E3g12-c153", "E3g12-c154", "E3g12-c155", "E3g12-c166", "E3g12-c179"]
for rid in L05_CARDS:
    carry(rid, CARD_L05)
for rid in L06_CARDS:
    carry(rid, CARD_L06)
for rid in L07_CARDS:
    carry(rid, CARD_L07)
for rid in L08_CARDS:
    carry(rid, CARD_L08)
carry("E3g12-c131-basis-note", "cards.json (E3-c131 absent) and L07.html")
carry("E3g12-r11-c130-grade-resolved", "cards.json E3-c130 and its cited L07.html blocks")
carry("E3g12-delta-round12", "history of the slice (ccaeeaf4..329c1d7f); no subject changed in this delta")
carry("E3g12-L04-theorem-cross-lesson", "L04.html (no change in the delta), L07.html Section 0 and Section 2, cards.json E3-c129")
carry("E3g12-L05-L08-problem-solutions", "the problem sets of L05-L08 (no changed line falls in any problem set)")
carry("E3g12-L05-L08-quiz-keys", "the quiz sections of L05-L08 (no changed line falls in any quiz section; no quiz item mentions a title)")
carry("E3g14-delta-round14", "history 329c1d7f..1431aa1d; no subject changed in this delta")
carry("E3g14-hours-arithmetic", "course/modules/E/E3/index.html, the L01-L08 eyebrow and header lines (the eyebrow line 35 of L07 is unchanged; changed lines are not header lines), project.html hours line")
carry("E3g15-delta", "history 1431aa1d..dde0486b; no subject changed in this delta")
carry("E3g15-L05-changes", "L05.html Remark 1.5, Definition 2.1, Proposition 2.2 proof and quiz item L05q9 (none changed in the delta)")
carry("E3g15-L06-changes", "L06.html Proposition 1.4 and proof, Remark 3.2, section 4-5, section 7 rows, quiz item L06q2 (the delta changed only the L06 footer line 545)")
carry("E3g15-L08-changes", "L08.html section 6 first misconception and the A3 reference; cards.json E3-c154 (the delta changed L08 section 5 and section 8, not section 6)")
carry("E3g15-lab-twin-L06", "tests/labs/E3/lab-E3-L06-1.py and L06.html section 3 Lab 1 (tests/labs/E3 byte-identical across the delta)")
carry("E3g18-delta-inventory-r18", "history dde0486b..4540351d; no subject changed in this delta") if False else None
carry("E3g18-delta-inventory", "history dde0486b..4540351d; no subject changed in this delta") if False else None

# ---- rows carried that are not card/lesson-specific
FRESH_IDS = {r["id"] for r in rows}
for rid, b in base_rows.items():
    if rid in FRESH_IDS:
        continue
    if b["status"] == "PASS":
        carry(rid, {
            "E3g12-c131": "cards.json (E3-c131 absent) and the L07.html blocks it named (Lab 1 part C, Problem E2)",
            "E3g18-delta-inventory": "history dde0486b..4540351d (round-18 inventory); no subject of it changed in 4540351d..2a805c83",
            "E3g18-c106-basis": "cards.json entry E3-c106 (the delta changed only c037, c134, c157, c158)",
        }[rid])
    else:
        raise SystemExit(f"base non-PASS row not re-verified: {rid}")

# base rows that changed subject but were not re-verified above must not be silently carried
# (checked by the reviewer: every base row id appears once)
ids = [r["id"] for r in rows]
missing_base = [rid for rid in base_rows if rid not in ids]
assert not missing_base, missing_base

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 1,
    "verifier": "Haiku 5.5 independent verifier, unit E3 slice g, round 1 (closing delta 4540351d..2a805c83)",
    "pin": PIN_HEAD,
    "base": f"{PIN_BASE} (base fragment ~/.fanout/frags/D-E3-g.round18.json, round 18, verdict FAIL with one row)",
    "checkout": CHECKOUT,
    "scratch": "ledgers/E3/scripts/E3-g-r1/out",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice g = E3 L05-L08 lesson pages, cards.json (all 178 E3 cards, of which the L05-L08 cards are in scope), and the L05-L08 lab twins. Lessons, cards and twins are not a project slice: no grader mutation applies, mutants: none (the ruling that lab twins are demonstrations).",
        "Delta 4540351d..2a805c83 inside the slice: L05.html (line 499 key-results row; line 620 footer), L06.html (545 footer), L07.html (44 legend, 80 Section 1 attribution sentence, 463 removed key-results row, 570 footer), L08.html (44 legend, 67 Definition 1.2 sentence, 133 Example 2.5 sentence, 479 bullet, 620-621 removed key-results rows, 723 footer), cards.json (E3-c037 Lambda, E3-c134, E3-c157, E3-c158 grade and cite removed). tests/labs/E3 and the grader are byte-identical.",
        "The only non-PASS subject is the L05-L08 footer, legend and the ungraded registry-title attributions: at 2a805c83 L05-L08 contain no claim span and no data-cite attribute (4540351d had 1 in L07 and 2 in L08). The gates still pass because check_pages checks only claim spans. Six rows are FAIL for this one root cause plus its card and footer surfaces.",
        "Base round-18 FAIL row E3g18-grade-legend-footer is re-verified from scratch and remains FAIL (new footer text; the legend change on L07/L08 is consistent with L03-L06 and verifier rule 9).",
        "Outside slice g, observed and not rated: L01.html and L02.html legend 'single study' and footer 'Each graded result carries a proof or a lab result labelled C.' (inconsistent with L05-L08); L03.html Proposition 1.2 (b renamed Lambda; card E3-c037 checked as E3g19-c037) and interpretation text line 326; project.html line 648 exemplar text.",
        "Carried rows: the subject named is byte-identical since 4540351d for the cards and blocks cited, per the git diff hunk list in E3g19-delta-inventory.",
        "Gates re-run at 2a805c83 (ledgers/E3/scripts/E3-g-r1/gates.sh, all rc 0): check_pages L05-L08, check_dag, check_projects, run_labs L05-L08, page_smoke L05-L08, ruff check and format, mypy --no-incremental, verify_refs --offline, build_site --check, render_curriculum with empty diff, pytest tests/test_docs_figures.py tests/test_refs.py, pytest -k 'E3 or e3' over tests.",
        "Not checked: live Crossref (verify_refs without --offline; references unchanged); run_graders and mutate_graders (no grader in slice g; E3 grader unchanged); browser screenshots beyond page_smoke; the Epstein-Zin lab grid beyond the printed values and stated tolerances; the L01, L02, L03 and project hunks as subjects.",
    ],
    "summary": {},
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["summary"] = {"rows": len(rows), "pass": counts.get("PASS", 0), "fail": counts.get("FAIL", 0),
                       "unverifiable": counts.get("UNVERIFIABLE", 0), "mutants": 0, "mutants_killed": 0}
json.dump(fragment, open(f"{CHECKOUT}/ledgers/E3/E3-g.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(fragment["summary"])
