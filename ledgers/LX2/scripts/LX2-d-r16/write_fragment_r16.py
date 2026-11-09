# Writes ledgers/LX2/LX2-d.json (round 16) from the verification record. Run: python -I write_fragment_r16.py
import json, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE16-LX2-d"
SC = "ledgers/LX2/scripts/LX2-d-r16"
CARDS = "course/modules/LX/LX2/cards.json"
SRC = "scratch-LX2-d-r16/src (govinfo USREPORTS-463-646.pdf md5 b8e00e9a..., USREPORTS-521-642.pdf md5 9178c6ff..., COMPS-1884.pdf md5 08e45c1f..., COMPS-1885.pdf md5 060c3af6..., SR2602a1.pdf, sr2602.htm, cfainstitute standards pages; fetched by plain curl 2026-11-09)"

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("d-cards-001-010", "2.7 card vs current lesson; 2.1/2.6 statute locators (LX2-c001..c010)",
    f"{CARDS} LX2-c001..c010; course/modules/LX/LX2/L01.html §2 (lines 29-41) and §3-§4 (lines 42-66)", "PASS",
    f"Read every card in full against the stripped lesson {SC}/L01.txt lines 29-66. Statute quotations checked against the GovInfo COMPS-1884 text ({SC}/stat.py output; 5(a), 5(c), 6(a), 6(c), 8(a), 8(b), 8(d)): c004 'filed on receipt, subject to the fee condition (section 6(c))' matches 6(c) ('deemed to have taken place upon the receipt thereof', not 'unless accompanied by ... the fee'); c007 matches 5(c); c009 matches 8(a) ('twentieth day after the filing thereof or such earlier date'); c010 matches 8(b) (ten days; 'refusing to permit such statement to become effective until it has been amended'). Numbers in these cards: card_numbers_r16.out reports 0 numbers absent from the card's own lesson.")

row("d-cards-011-020", "2.7 card vs current lesson; 2.4 Propositions 4.1-4.3; 2.2 model counts (LX2-c011..c020)",
    f"{CARDS} LX2-c011..c020; L01.html §3 (lines 43-53), §4 (lines 55-66, Propositions lines 217-232)", "PASS",
    f"Statute: 12(a), 12(b), 12(d) first and second sentences, 13(a) and 15(d)(1) checked against COMPS-1885 text (stat.py). Model counts recomputed independently: {SC}/card_arithmetic_r16.out lines 'L01 states 10', 'L01 transitions 22', 'L01 transitions from 1933 events 12', 'from 1934 events 10', 'reachable 10 of 10', 'both duties 0', 'sale-permitted 2', 'offer-permitted 4', 'R13 5', 'R15 2'. c017 hypothesis and conclusion match Proposition 4.1 text (lines 219-220); c018 matches Proposition 4.2 (224-225); c019 matches Proposition 4.3 (229-230).")

row("d-attrib-statute", "2.1 attribution; 2.6 statute locators (quotations on L01 claim spans and in cards c001-c027, c095, c096, c104)",
    "course/modules/LX/LX2/L01.html claim spans lines 21-54; cards.json LX2-c001..c027, c095, c096, c104", "PASS",
    f"Every quoted statute sentence on the lesson's claim spans was found in the GovInfo text: 6(a) first sentence; 5(a) first sentence; 5(c); 8(a) first sentence; 8(b) 'ten days' (both occurrences), 'refusing to permit such statement...', 'whichever date is the later'; 8(d) 'fifteen days', 'issue a stop order suspending the effectiveness', 'shall cease to be effective'; 12(a); 12(b) first sentence; 12(d) first and second sentences ('thirty days after the receipt of such certification', 'withdrawn or stricken from listing and registration in accordance with the rules of the exchange'); 13(a) first sentence; 15(d)(1) first sentence ('which has become effective pursuant to the Securities Act of 1933, as amended'), second sentence ('automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12'), third sentence (300 persons; 1,200 persons; 'other than the fiscal year within which such registration statement became effective'). Section 2(a)(5) defines 'Commission' (COMPS-1884 text). Not read this round: 2(a)(19), 5(d), 6(e)(1) (see d-l01-sec5-statute, carried).")

row("d-cards-021-030", "2.7 card vs current lesson; 2.1 attribution (LX2-c021..c030; c030 changed since round 15)",
    f"{CARDS} LX2-c021..c030 (c030 back changed in 56cc575a); course/modules/LX/LX2/L02.html lines 29-40 (Definition 2.1 and 3.1) and §3 claim span at line 80", "PASS",
    "c021-c029 checked against L01 and L02 text and the O'Hagan/Dirks PDFs (pdftotext; page map by pdfpage). c030 (changed): 'the tippee assumes a fiduciary duty to the shareholders only when the insider has breached his fiduciary duty by disclosing the information to the tippee and the tippee knows or should know that there has been a breach (Dirks, p. 660)' matches Dirks (463 U.S. 646) pdfpage 15 = printed p. 660, and matches the same quoted sentence on L02.html line 40 (verbatim). The lesson's own paraphrase on line 80 is a separate row (d-l02-derivative-sentence).")

row("d-attrib-opinions", "2.1 attribution; quotes and pinpoints (LX2-c028..c043, c105)",
    f"{CARDS} LX2-c028..c043, c105; Dirks and O'Hagan PDFs in {SC.replace('scripts/LX2-d-r16','')}scratch-LX2-d-r16/src", "PASS",
    "Each quotation located by pdftotext page search (pf2.py): O'Hagan p. 652 (classical theory 'not only to officers ... temporarily become fiduciaries', misappropriation definition 'in connection with ... duty owed to the source'), p. 653 n. 5 (O'Hagan 'was not an insider' of Pillsbury), p. 655 ('may remain liable under state law for breach of a duty of loyalty') and n. 7 ('the trader may still be liable under the misappropriation theory'), p. 656 ('without disclosure to his principal'). Dirks p. 651 n. 6 (10(b) text), p. 654 ('does not arise from the mere possession'), p. 660 ('only when the insider has breached ... knows or should know'), p. 662 ('Absent some personal gain'), p. 663 ('reputational benefit that will translate into future earnings'), p. 663 n. 23 ('a mental state embracing intent to deceive, manipulate, or defraud'; 'an independent element of a Rule 10b-5 violation'), p. 664 ('a question of fact', 'will not always be easy for courts', 'gift of confidential information to a trading relative or friend'). Pinpoints match the printed page of each passage. c035 and c042 paraphrase the quoted sentences, and their quoted fragments are verbatim.")

row("d-cards-031-040", "2.7 card vs current lesson (LX2-c031..c040)", f"{CARDS} LX2-c031..c040; course/modules/LX/LX2/L02.html lines 30-65 and 66-82 (lab), 357-363 (misconceptions)", "PASS",
    f"Read against L02.txt. c038 names P1, P3, P4, P6 as firing and P2, P5, P7, P8 as failing one element; matches the printed table in run-lab output (twin-lab-LX2-L02-1.out lines 'fired: P1, P3, P4, P6 (4 of 8)'; each deciding element matches). c039 (P8 not fired), c040 (P5 fails knowledge), c041 (P2 not fired, P4 fired on the gift), c042 (P6 fires; footnote 5 at p. 653), c043 (footnote 7 at p. 655 n. 7) match the lesson's misconception and Remark 4.3 text.")

row("d-cards-041-050", "2.7 card vs current lesson (LX2-c041..c050)", f"{CARDS} LX2-c041..c050; course/modules/LX/LX2/L03.html §1 (lines 24-32)", "PASS",
    "c044-c050 read against L03 Definition 1.1 (lines 25-26), Remark 1.2 (line 28), Definition 1.3 (line 30), Assumption A1 (line 34). Each card restates the lesson's wording with no added claim. c050 matches A1 (distinct orders, q-share execution, whole-order cancel, resting limit, market never rests).")

row("d-cards-051-060", "2.7 card vs current lesson; 2.4 Proposition 2.2 hypotheses (LX2-c051..c054, c058..c063)", f"{CARDS} LX2-c051..c054, c058..c063; course/modules/LX/LX2/L03.html §2 (lines 35-43), §4 (lines 271-277), lab output (lines 246-263)", "PASS",
    f"c051 identity G = R + 2X + C_m + C_t matches Proposition 2.2 (line 37). c053 numbers recomputed by flow_recheck_r16.py ({SC}/flow_recheck_r16.out: trader 0 6/97 at cancel rate 5; trader 1 3/104 at 10; 3 x 97 = 291 < 624 = 6 x 104). c058 (crossed book 0), c059 (none flagged; 21/37 < 2) match the printed output. c055-c057 are absent from the id sequence; check_pages does not require contiguity (noted, not a defect).")

row("d-cards-061-070", "2.7 card vs current lesson; 2.2 numbers; 2.1 attribution (LX2-c061..c070)", f"{CARDS} LX2-c061..c070; course/modules/LX/LX2/L03.html §4, L04.html §1-§4", "PASS",
    f"c061-c063 match L03 §4 (lines 273-277). c064-c065 quotes checked against the CFA Standard III(A) and VI(A) subpages (fetched this round; see d-attrib-cfa). c066-c067 checked against SR 26-2 attachment (SR2602a1.pdf: model definition p. 3 lines 114-124; model risk p. 3 lines 134-136). c068 'responsible for adopting model risk management practices ...' runs from p. 1 to p. 2 (lines 44-51). c069 outcomes analysis p. 9 (lines 401-411). c070 h_t = 1 when |e_t| <= 2 (inclusive) matches L04 Definition 4.1 (line 60).")

row("d-cards-071-080", "2.7 card vs current lesson; 2.4 Theorems 4.2-4.3, Proposition 4.4 hypotheses; 2.2 numbers (LX2-c071..c080)", f"{CARDS} LX2-c071..c080; course/modules/LX/LX2/L04.html §4 (lines 58-74)", "PASS",
    f"Definitions 4.1 and the rounding rule (c071-c073) match line 60. c074-c075 match Assumptions A1 and A2 (line 62). Theorem 4.2 and proof (lines 64-66), Theorem 4.3 and equality case (lines 68-70), Proposition 4.4 and proof (lines 72-74). Numbers recomputed independently ({SC}/card_arithmetic_r16.out): P(hit)=44/117 exact, rounded 0.3761; E[error]=1; 8 x 5 + 4 = 44; the hit set -3 <= V-U <= 1 equals |e| <= 2 over all 117 pairs.")

row("d-cards-081-089", "2.7 card vs current lesson; 2.1 attribution; 2.2 numbers (LX2-c081..c089)", f"{CARDS} LX2-c081..c089; course/modules/LX/LX2/L04.html §1-§3, §6 (lines 23-31, 32-39, 40-56, 262-270)", "PASS",
    "c080-c081 quotes checked against Standard III(A) The Standard and the guidance paragraph beginning 'Fiduciary duties are often imposed' ('must comply with any legally imposed fiduciary duty'). c082 SR 26-2 letter body: 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8' (sr2602.htm, Supersedes list). c083 Applicability line: 'over $30 billion in total assets regulated by the Federal Reserve' (sr2602.htm). c084: a full-text search of SR2602a1.pdf for 'hit' and 'bias' returns no match (grep exit 1). c086: 'does not set forth enforceable standards or prescriptive requirements' and 'will not result in supervisory criticism' on p. 2 (lines 67-71); footnote 1 (lines 94-96). c087: Example 3 'At minimum ... Best practice is to avoid the conflict by asking his employer to assign another analyst' (Standard VI(A) page). c088: 'does not render all members and candidates fiduciaries' and 'neither impose such a legal responsibility nor require all members or candidates to act as fiduciaries'. c089 verified as c086.")

row("d-cards-090-094", "2.5 lab output vs card; 2.7 card vs lesson (LX2-c090..c094; c094 changed)", f"{CARDS} LX2-c090..c094; course/modules/LX/LX2/L01.html §8-§9 and L03.html §2 lab (lines 44-45)", "PASS",
    f"Twin runs under python -I -W error exit 0 with empty stderr; every output line appears verbatim in the lesson ({SC}/output_in_lesson_r16.py: 39/22/17/48 lines, 0 missing). c090 '10 of 10', c091 'states where both reporting duties apply: 0', c092 'states where a sale is permitted and an offer is not: 0' match the L01 twin output. c093 'events where entered != resting + 2 * traded + ...: 0' and c094 'tally from the event log disagrees with the book in 0 trader counts' match the L03 output. c094 changed in 56cc575a to 'rebuilds'; the lesson line 45 uses 'rebuilds' verbatim.")

row("d-cards-095", "2.7 card vs current lesson (LX2-c095)", f"{CARDS} LX2-c095; course/modules/LX/LX2/L01.html §2 (line 39), §5 (line 235)", "PASS",
    "8(b) 'whichever date is the later' rule quoted verbatim in the statute (COMPS-1884 text: 'the registration shall become effective at the time provided in subsection (a) or upon the date of such declaration, whichever date is the later'); the model treats the declaration as an event with no date (L01 line 235).")

row("d-cards-096-097", "2.7 card vs current lesson; 2.1 attribution (LX2-c096, LX2-c097; c097 changed in 56cc575a)", f"{CARDS} LX2-c096, LX2-c097; course/modules/LX/LX2/L01.html §3 (line 54), L02.html §3 Assumption A1 (lines 41-42)", "PASS",
    "c096: 15(d)(1) third sentence 'other than the fiscal year within which such registration statement became effective' (COMPS-1885); lesson §3 agrees. c097 (front reworded in 56cc575a): 'a value of none ... means that the insider received no direct or indirect personal benefit from the disclosure' matches L02.html Assumption A1 text (line 42) verbatim in substance, and the 'does not state this reading' clause matches line 42.")

row("d-cards-098-099", "2.7 card vs current lesson (LX2-c098, LX2-c099; c099 changed in 56cc575a)", f"{CARDS} LX2-c098, LX2-c099; course/modules/LX/LX2/L02.html lines 32, 64-65", "PASS",
    "c098 matches Assumption A2 (line 64: facts stated are true; materiality, confidentiality, benefit, knowledge and disclosure read as stated). c099 (changed): lesson line 32 says the lab reads issuer_insider to include a temporary fiduciary and the pattern must state that the person is one; line 65 (A3) says the same. Classifier code (L02.txt lines 76-79) does not test that statement. Both consistent.")

row("d-cards-101-103", "2.7 cards for Dodd-Frank and MiFID II vs plan §9; 2.6 no provision stated (LX2-c101..c103)",
    f"{CARDS} LX2-c101..c103; plans/LX2-build-plan.md §9 (line 495)", "FAIL",
    f"Plan §9 states: 'Cards for Dodd–Frank and MiFID II are not written until B1 and B2 are resolved.' B1 (no source for either instrument) is not resolved: references/references.json, references/review_queue.json and references/authorities.yaml contain no Dodd-Frank, MiFID or EU-issuer record (grep -c -i 'esma|europa|eur-lex' returns 0 for references/authorities.yaml, references.json and review_queue.json; {SC}/verify_refs_offline_r16.out shows 560 entries and 0 integrity problems). B2 (no allow-listed EU domain) is not resolved: authorities.yaml has no europa, eur-lex or esma entry. The architect's binding decisions (plan, 'Architect decisions') confirm L03 names both instruments with content not stated, but they do not lift the §9 rule on cards. The card text itself is accurate: each says only that the lesson names the instrument and states no provision (L03.html lines 265-270).",
    "Remove LX2-c101, LX2-c102 and LX2-c103 from cards.json, or obtain an architect ruling recorded in plans/FINAL-ARCHITECT-RULINGS.md that lifts plan §9 for LX2 cards naming the two instruments with content not stated. No other change.")

row("d-attrib-sr2026", "2.1 attribution; 2.2 numbers and locators (LX2-c066..c069, c082..c084, c089)", f"{CARDS} LX2-c066..c069, c082..c084, c089; course/modules/LX/LX2/L04.html §3-§4 (lines 40-56)", "PASS",
    "Quotations and locators checked against SR2602a1.pdf (22,794 bytes text, {SC}/src/SR2602a1.txt): 'does not set forth enforceable standards' p. 2 (lines 67-69); 'will not result in supervisory criticism' p. 2 (lines 69-71); footnote 1 p. 2 (lines 94-96); model definition p. 3 (lines 114-124); model risk p. 3 (lines 134-136); 'responsible for adopting' pp. 1-2 (lines 44-51); outcomes analysis p. 9 (lines 401-411); Ongoing Model Monitoring p. 9. sr2602.htm: supersedes SR 11-7 and SR 21-8; Applicability over $30 billion.")

row("d-attrib-cfa", "2.1 attribution; quotes and locators (LX2-c061, c064, c065, c077..c081, c087, c088)", f"{CARDS} LX2-c061, c064, c065, c077, c078, c079, c080, c081, c087, c088; course/modules/LX/LX2/L04.html §1-§2 (lines 23-39)", "PASS",
    "Quotations checked against the Standard III(A) page (cfa-standards-of-practice-iii-a.txt, 'Updated April 2024': 'The Standard' duty of loyalty; Guidance 'Understanding the Application of Loyalty, Prudence, and Care': 'Fiduciary duties are often imposed by law or regulation ...', 'does not render all members and candidates fiduciaries', 'neither impose such a legal responsibility', 'must comply with any legally imposed fiduciary duty') and the Standard VI(A) page (cfa-standards-of-practice-vi-a.txt, 'Updated January 2024': The Standard; Guidance 'A conflict of interest is any matter that could reasonably be expected to impair independence and objectivity or raise a question about whether actions, judgment, or decision making is free from bias'; Example 3 'At minimum ... Best practice is to avoid the conflict by asking his employer to assign another analyst'). The registry record cfandcode points to the Code landing page, which contains links but none of these sentences (see registry_flags).")

row("d-l03-dodd-mifid", "2.6 / 2.9 L03 §3 and definitions 3.1 and 3.2 (lesson text)", "course/modules/LX/LX2/L03.html §3 (lines 264-270), key results (lines 353-358)", "PASS",
    "L03 §3 states that both instruments are named and that no provision, scope or duty is stated. The registry holds no primary text (grep, see d-cards-101-103). No lesson sentence states what either instrument requires: grep -i require on the stripped L03 text returns two lines, 265 and 284, both saying that nothing is stated (output in ledgers/LX2/scripts/LX2-d-r16/L03.txt). The lesson-level wording is not in dispute; the card row is.")

row("d-c058-grade", "2.3 grade of LX2-c058 vs lesson key results", f"{CARDS} LX2-c058; course/modules/LX/LX2/L03.html §7 (lines 344-352)", "PASS",
    "Card grade C with basis 'Lab 1 printed output (SIMULATED flow, seed 2026)'. Key results row 'Lab 1: zero crossed-book events ...' is graded C (SIMULATED basis). Consistent.")

row("d-c059-grade", "2.3 grade of LX2-c059 vs lesson key results", f"{CARDS} LX2-c059; course/modules/LX/LX2/L03.html §7 (line 350-352)", "PASS",
    "Card grade C with 'demonstration threshold' basis. Key results row 'no trader flagged at the demonstration threshold 2' is graded C with the same caveat. Consistent.")

row("d-c085-grade", "2.3 grade of LX2-c085 and LX2-c100 vs lesson key results", f"{CARDS} LX2-c085, LX2-c100; course/modules/LX/LX2/L04.html §8 (lines 346-347)", "PASS",
    "Both cards C with basis 'Lab 1, Part A (SIMULATED path, seed 20261103)'. Key results row 'Exact hit rate 3/8 and bias 41/12 ... C (SIMULATED path, seed 20261103)' is consistent.")

row("d-c100-new", "2.5 card vs printed block (LX2-c100)", f"{CARDS} LX2-c100; course/modules/LX/LX2/L04.html Lab 1 printed block (lines 208-256)", "PASS",
    "Printed 'bias = 41/12 (rounded 3.4167)' and 'sum of errors = 82' (twin-lab-LX2-L04-1.out); independent recomputation gives 82/24 = 41/12 and rounds to 3.4167 (card_arithmetic_r16.out 'L04 bias exact', 'bias rounded').")

row("d-card-labels-current", "2.7 card labels agree with current lesson labels", f"{CARDS}; course/modules/LX/LX2/L01..L04.html key-results tables", "PASS",
    "Labels on cards (T for proved results c017-c021, c051, c076-c079, c086; C for statute and doctrine and lab-derived results; SIMULATED or HYPOTHETICAL basis where required) agree with the lessons' key-results tables (L01 lines 306-338; L02 lines 419-445; L03 lines 340-358; L04 lines 325-357).")

row("d-c054-hypothesis", "2.4 hypothesis of the cited proposition (LX2-c054)", f"{CARDS} LX2-c054; course/modules/LX/LX2/L03.html Proposition 2.2 and Remark 2.3 (lines 35-41)", "PASS",
    "Remark 2.3: without C_t the identity fails whenever a trader cancels a resting order. Card states the same under A1. Consistent.")

row("d-grade-legend", "2.9 grade legend in each lesson header", "course/modules/LX/LX2/L01.html..L04.html header lines 15-20 (stripped)", "PASS",
    "Each lesson header carries the grade legend T/A/B/C/D/X with the same wording (L01.txt..L04.txt lines 15-20). Consistent.")

row("d-l03-hypothesis-claims", "2.4 lab hypothesis and interpretation claims (L03)", "course/modules/LX/LX2/L03.html Lab 1 lead-in (line 45) and interpretation (line 263)", "PASS",
    "Lead-in predicts zero crossed-book events, zero identity failures and zero tally disagreements; printed output shows 0, 0 and 0 (twin-lab-LX2-L03-1.out). Flow parameters (400 events, seed 2026, six traders, cancel rates 5/10/25/40/60/85) match the twin's constants. Independent flow re-run (flow_recheck_r16.out) reproduces every printed count.")

row("d-l04-e3-arithmetic", "2.2 numbers in Problem E3 (L04)", "course/modules/LX/LX2/L04.html Problem E3 (around line 310)", "PASS",
    "Recomputed: Var(V)=(81-1)/12=20/3, Var(U)=(169-1)/12=14, Var(e)=62/3; se = sqrt((62/3)/24) = sqrt(31/36) = 0.92796; gap 41/12 - 1 = 29/12 = 2.41667; ratio 2.604, stated 'about 2.60'. Consistent (python -I run, this round).")

row("d-l01-sec5-statute", "2.6 L01 §5 statute statements (carried; not re-read this round)", "course/modules/LX/LX2/L01.html lines 235-241 (§5)", "PASS",
    "Carried from round 15 (course/modules/LX/LX2/L01.html byte-identical since the previous pin d1e65a02; the 6(e)(1), 5(d) and 2(a)(19) statements were not re-read this round): the parts that were re-read (8(a) 'except as hereinafter provided', 12(d) thirty days, 'treats the declaration of effectiveness as an event with no date') agree with the statute text.")

row("d-l01-line63-s3-defined", "2.9 section 3 defined before use (L01) and card LX2-c005", "course/modules/LX/LX2/L01.html lines 44-45 (Definition 3.1) and 96; cards.json LX2-c005", "PASS",
    "Carried from round 15 (L01.html byte-identical since d1e65a02). Card c005 'As the term the statute uses in sections 12, 13 and 15(d). It is not defined further.' matches Definition 3.1's sentence 'A national securities exchange is the term the statute uses in those sections; the lesson does not define it further.' (L01.txt line 45).")

row("d-l01-line88-spacing", "2.9 prose spacing and structure (L01)", "course/modules/LX/LX2/L01.html (round-15 line 88 location)", "PASS",
    "Carried from round 15 (L01.html byte-identical since d1e65a02). Not a card subject; no change this round.")

row("d-r2-lesson-delta", "2.9 L02 delta lines (round-2 record)", "course/modules/LX/LX2/L02.html (round-2 record lines)", "PASS",
    "Carried from round 15 (L02.html byte-identical since d1e65a02). Historical record; no change this round.")

row("d-c003-locator", "2.1 card locator vs statute (LX2-c003)", f"{CARDS} LX2-c003; course/modules/LX/LX2/L01.html line 30 (registration statement defined; section 2(a)(5))", "PASS",
    "c003 has no locator (definition card). Its statement ('the document an issuer files with the Commission to register a security under the 1933 Act') matches the lesson's sentence on line 30, which cites section 2(a)(5), and section 2(a)(5) defines 'Commission' (COMPS-1884 text).")

row("d-proposition-hypotheses-r13", "2.4 proposition hypotheses carried into cards", f"{CARDS} LX2-c017..c019, c051, c076..c079; L01.html Section 4; L03.html Section 2; L04.html Section 4", "PASS",
    "Each card's hypothesis clause matches the lesson's H1/hypothesis text word for word or in substance: Proposition 4.1 (H1 = 10 states, start state, 22 transitions); 4.2 (R13, R15 and 'whatever its condition on the status'); 4.3 (R5a and R5c); 2.2 (A1 and the five quantities); Theorem 4.2 (window n >= 1, 0 <= b1 <= b2); Theorem 4.3 (window n >= 1); Proposition 4.4 (under A1).")

row("d-basis-simulated-hypothetical", "2.3 / 2.5 SIMULATED and HYPOTHETICAL labels in card basis fields", f"{CARDS} basis fields of c038, c053, c058, c059, c085, c093, c094, c100", "PASS",
    "Each lab-derived card on a seeded or generated flow names SIMULATED in its basis; c038 names HYPOTHETICAL. c086 (hand-built Part C) and c023 and c090-c092 (model enumeration) are not generated results and are labelled by their lab part.")

row("d-numbers", "2.2 numbers in cards: computed, quoted or derived; every card number in its lesson", f"{CARDS} (102 cards); {SC}/card_numbers_r16.py; card_arithmetic_r16.py; flow_recheck_r16.py", "PASS",
    "card_numbers_r16.out: 102 cards checked, 0 cards with a number absent from their own lesson. card_arithmetic_r16.out: ALL OK (every quoted figure recomputed independently: 10/22/12/10 counts, reachability, 0/0/2/4/5/2 model counts, 9/24 hits, 82/24 bias, 3.4167, 3.6667, 3.1667, 44/117, 0.3761, E[error]=1, MAE 3 for Part C, 291 vs 624, 21x50 vs 17x37, 59/986). flow_recheck_r16.out reproduces the L03 lab's printed counts (orders 331, executions 207, traded 4060, trader cancels 69, trader shares cancelled 2020, ratios 6/97, 3/104, 5/34, 6/29, 17/50, 21/37).")

row("d-cards-no-grade", "2.7 grade and citation coverage", f"{CARDS} (cards without a grade field)", "PASS",
    "31 cards carry no grade field: definition, assumption and limit cards (c001, c002, c003, c005, c008, c022, c044-c050, c052, c054, c060-c063, c070-c075, c097-c099) and the two named-only cards c101-c103. Plan §9 requires grade C for doctrine and statute results; the first group are definitions and the previous round flagged them for architect confirmation (see notes). c101-c103 are covered by d-cards-101-103. Cards with a cite key and no grade: c001, c002, c003, c005 (definitions). Cards with neither cite nor basis: none (check_pages.py check_cards passed).")

row("d-cards-schema", "2.7 card schema (tools/check_pages.py cards rules)", "tools/check_pages.py --unit LX2", "PASS",
    f"check_pages.py --unit LX2: 'check_pages LX2: PASS' ({SC}/check_pages_LX2_r16.out). Ids match LX2-c\\d{{3}}; no duplicate ids; every lesson has cards; every cite key exists in references.json.")

row("d-cards-coverage", "2.7 coverage of lesson definitions, propositions, assumptions, misconceptions, key results by cards", f"{CARDS} vs L01.html..L04.html", "PASS",
    "Definitions: L01 2.1 (c001), 3.1 (c002); L02 2.1 (c028), 3.1 (c030), 4.1 (c031); L03 1.1 (c044-c047), 1.3 (c049), 3.1/3.2 (c101, c102: see d-cards-101-103); L04 1.1 (c064), 2.1 (c065), 3.1 (c066-c067), 3.2 (c068), 3.3 (c069), 4.1 (c070-c073). Propositions/theorems: L01 4.1-4.3 (c017-c019); L03 2.2 (c051); L04 4.2-4.4 (c076-c079). Assumptions: L01 A1 (c022); L02 A1-A3 (c097-c099); L03 A1 (c050); L04 A1-A2 (c074-c075). Misconceptions: L01 (c024-c027); L02 (c039-c043); L03 (c053, c054, c103); L04 (c086-c089). Key results: L01 (c020, c021, c023, c090-c092); L03 (c058, c059, c093, c094); L04 (c085, c100).")

row("d-dup-scan", "2.7 duplicate cards", f"{CARDS} (102 cards)", "PASS",
    "No duplicate ids and no duplicate fronts (scripted). c037 and c105 both concern scienter but state different facts (the element in Dirks n. 23 vs the definition in n. 23); not duplicates. Ids c055, c056, c057 absent (no check requires contiguity).")

row("d-atomic-split", "2.7 one fact per card", f"{CARDS} LX2-c030, c053, c086, c094, c100", "PASS",
    "Multi-clause backs were read individually: c030 states one derivative rule with its two conditions (one fact, quoted from Dirks p. 660); c053 states one comparison; c086 states one bias/MAE example; c094 one count; c100 one exact value. No card asserts two independent results.")

row("d-labs-run", "2.5 labs: run, deterministic, twin under python -I -W error", "tests/labs/LX2/lab-LX2-L01..L04-1.py; tools/run_labs.py --unit LX2", "PASS",
    f"run_labs.py --unit LX2: 'run_labs LX2: PASS (7/7)' ({SC}/run_labs_LX2_r16.out). Each twin run as python -I -W error exits 0 with empty stderr ({SC}/twin-lab-LX2-L0*-1.out). Outputs are reproduced verbatim by the lessons.")

row("d-dag", "2.9 check_dag; no concept used before definition or outside closure (cards)", "tools/check_dag.py --unit LX2", "PASS",
    f"check_dag.py --unit LX2: PASS ({SC}/check_dag_LX2_r16.out). Cards use no concept link.")

row("d-gates-structure", "2.9 structure gates run on this pin", "tools/check_pages.py --unit LX2; tools/check_dag.py --unit LX2; tools/run_labs.py --unit LX2; tools/verify_refs.py --offline; ruff; mypy", "PASS",
    "check_pages LX2 PASS; check_dag LX2 PASS; run_labs LX2 PASS (7/7); verify_refs --offline: 560 entries, 0 problems; ruff check . passes; mypy --no-incremental: 'Success: no issues found in 385 source files'. Not run: check_projects and page_smoke (no LX2 project page changed since d1e65a02; the delta touches cards.json only); pytest (no tool or test changed).")

row("d-notation", "2.4 notation: cards' symbols against notation/notation.json", f"{CARDS}; notation/notation.json", "PASS",
    "notation/notation.json byte-identical since d1e65a02 (no change in the delta). The changed cards c030, c094, c097, c099, c105 contain no symbol; the other cards' symbols (T, H, n, R, G, X, C_m, C_t, V_t, U_t, e_t, b1, b2) follow the lesson's use. No new symbol introduced.")

row("d-process-banned", "2.9 process words and banned phrases in learner text (cards)", f"{CARDS} (all fronts, backs and basis fields)", "PASS",
    "Scripted scan with word boundaries: no 'build', 'builder', 'verifier', 'fixer', 'round', 'REQUEST', 'unit report'; no BANNED phrase from check_pages.py (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipsis). 'rebuilds' (c094) is a normal word, not the process word 'build'. The word 'process' in c066 is a quotation of SR 26-2 (its model definition).")

row("d-mutants-r14", "2.7 mutation check of the cards by planted errors (r13..r16)", f"ledgers/LX2/mutants/r16_card_mut1..7*.json; ledgers/LX2/mutants/transplant_r13..r15_*.json; {SC}/card_claims_r16.py; {SC}/card_numbers_r16.py", "PASS",
    f"Seven new planted card errors (r16_card_mut1..7) are each killed by card_claims_r16.py (71 assertions); mut7 is also killed by card_numbers_r16.py. Earlier planted errors (r13 mut1-4, r14 mut2-4, r15 mut1-4) were re-planted on the current cards by transplant_old_card_mutants_r16.py ({SC}/transplant_r16.out): each killed by card_claims_r16.py, and the numeric ones also by card_numbers_r16.py. r13_card_mut5 is moot (the current LX2-c003 carries no locator). The older complete-file mutants were not counted as kills on their own: they are 97-101-card baselines that differ from the current cards.")

row("d-registry-keys-r14", "2.1 cite keys exist; no primary text invented for Dodd-Frank, MiFID II, SR 11-7/21-8", "references/references.json; references/review_queue.json; references/authorities.yaml; cards.json cite fields", "PASS",
    "Cited keys (cfandcode, frb2026fed, gpo1983dirks, gpo1997united, gpondsecurities, gpondsecuritiesb) exist; all six fetched this round with plain curl (HTTP 200): the govinfo PDFs for USREPORTS-463-646, USREPORTS-521-642, COMPS-1884 and COMPS-1885 (content/pkg paths), federalreserve.gov sr2602.htm and SR2602a1.pdf, and the cfainstitute.org code landing page. grep: no record or source string for SR 11-7, SR 21-8, Dodd-Frank or MiFID II (only unrelated matches: 'Graham & Dodd', 'Franklin').")

row("d-quote-fidelity", "2.1 quotations in cards match the sources", f"{CARDS} curly-quoted passages; {SC}/src (fetched texts)", "PASS",
    "Every curly-quoted passage in the cards was located in the fetched source by pdftotext page search or the sources' HTML text (see d-attrib-statute, d-attrib-opinions, d-attrib-sr2026, d-attrib-cfa). No quotation mismatched.")

row("d-delta-read", "delta read: every hunk of the LX2 slice since the round-15 pin d1e65a02", "git diff d1e65a02 56cc575a -- course/modules/LX/LX2 references notation tools tests/labs/LX2 curriculum", "PASS",
    "Delta read in full: course/modules/LX/LX2/cards.json only (16 lines: c030 back, c094 back ('rebuilds'), c097 front reworded, c099 back, c105 added). Lessons, labs, registry, notation, tools and curriculum: no change for LX2. plans/FINAL-ARCHITECT-RULINGS.md gained rulings 17-18 (E4 and alternative files, not LX2). ledgers/LX2 mutant and script files added in the round-15 commit.")

row("d-grade-key-consistency", "2.3 grades: card grades vs lesson key-results tables", f"{CARDS} grade fields; L01..L04 key-results tables", "PASS",
    "T cards (c017-c021, c051, c076-c079, c086) match the proved results in the key-results tables. C cards match the statute/doctrine and lab-result rows. c020 and c021 (state and transition counts) are derivations on the page graded T, as the L01 key-results table grades them; a finite enumeration graded C would be the stricter reading (see notes).")

row("d-c027-changed", "2.7 card vs current lesson (LX2-c027)", f"{CARDS} LX2-c027; course/modules/LX/LX2/L01.html lines 53 and 250", "PASS",
    "Back: '13(a) applies to an issuer of a security registered pursuant to section 12; the duty for an issuer with only an effective 1933 registration comes from section 15(d)(1)'. Matches L01 lines 53 and 250 and the statute.")

row("d-c081-changed", "2.1 attribution; 2.7 card vs lesson (LX2-c081)", f"{CARDS} LX2-c081; course/modules/LX/LX2/L04.html §1 (line 29)", "PASS",
    "'Comply with it. The Code does not set a legal fiduciary duty, and members must comply with any legally imposed one' matches L04 line 29 and the guidance text ('must comply with any legally imposed fiduciary duty').")

row("d-c104-new", "2.1 statute quotation; 2.7 card vs lesson (LX2-c104)", f"{CARDS} LX2-c104; course/modules/LX/LX2/L01.html line 52", "PASS",
    "15(d)(1) second sentence 'automatically suspended if and so long as any issue of securities of such issuer is registered pursuant to section 12' (COMPS-1885). Card matches L01 line 52.")

row("d-c105-new", "2.1 attribution; 2.7 card vs lesson (LX2-c105, new in 56cc575a)", f"{CARDS} LX2-c105; course/modules/LX/LX2/L02.html line 27 and §5 (line 350)", "PASS",
    "Dirks p. 663 n. 23 (pdfpage 18): 'Scienter—\"a mental state embracing intent to deceive, manipulate, or defraud,\" ... is an independent element of a Rule 10b-5 violation.' The card's definition sentence matches the quotation; the lab-does-not-check statement matches L02 line 27 and line 347.")

row("d-c094-changed", "2.7 card vs current lesson (LX2-c094; 'rebuilds' wording, changed in 56cc575a)", f"{CARDS} LX2-c094; course/modules/LX/LX2/L03.html line 45", "PASS",
    "Lesson line 45: 'A tally is the per-trader count of orders and cancels that the lab rebuilds from its event log.' Card now reads the same. Printed output line 'tally from the event log disagrees with the book in 0 trader counts' matches.")

row("d-l02-derivative-sentence", "2.1 attribution; 2.3 grade (lesson sentence behind c030; carried FAIL, re-verified)", "course/modules/LX/LX2/L02.html line 80 (Definition 3.1 claim span, data-cite gpo1983dirks, loc pp. 659-660)", "FAIL",
    "Re-verified this round: the claim span reads 'In Dirks it is derivative: the tippee's duty comes from the insider's breach, and it arises only when the breach is established.' Dirks p. 660 (pdfpage 15) states that a tippee assumes the duty only when the insider has breached AND the tippee knows or should know of the breach. The span omits the knowledge condition, which the same page of the lesson quotes on line 81 (L02.html line 40 in the stripped text). The card c030 now carries both conditions, so the card is correct; the lesson sentence is incomplete.",
    "In L02.html line 80, replace 'it arises only when the breach is established' with 'it arises only when the insider has breached by disclosing the information and the tippee knows or should know of the breach (p. 660)', keeping the same claim span and locator.")

row("d-l01-sec2-registration-ungraded", "2.6 / 2.9 statute-content sentence needs a claim span with a locator (carried FAIL, re-verified)", "course/modules/LX/LX2/L01.html line 69 (Section 2, 'This lesson reads in effect as ...' paragraph)", "FAIL",
    "Re-verified: 'The definitions in section 2 do not define the phrase.' sits outside every claim span. The statement is true (COMPS-1884 section 2 defines no 'in effect'), and card LX2-c004 repeats it ('Section 2 does not define the phrase.') with cite gpondsecurities and no locator. The sentence is a statement about the statute with no locator.",
    "Wrap 'The definitions in section 2 do not define the phrase.' in a claim span with data-cite=\"gpondsecurities\" and data-locator=\"section 2 (definitions)\" in L01.html line 69.")

mutants = [
    {"name": "r16_card_mut1_c070_inclusive_to_exclusive", "description": "LX2-c070 back: inclusive band '|e_t| <= 2' changed to exclusive '|e_t| < 2'", "killed_by": "card_claims_r16.py (c070 assertion: inclusive band)"},
    {"name": "r16_card_mut2_c051_drop_2X", "description": "LX2-c051 back: identity G = R + 2X + C_m + C_t changed to G = R + X + C_m + C_t", "killed_by": "card_claims_r16.py (c051 assertion)"},
    {"name": "r16_card_mut3_c063_reprice_adds_zero", "description": "LX2-c063 back: 'No. Each adds 1 to cancels' changed to 'Yes. A reprice adds 0 to cancels'", "killed_by": "card_claims_r16.py (c063 assertion)"},
    {"name": "r16_card_mut4_c018_R15_listed", "description": "LX2-c018 back: 'R15 requires it to be not_listed' changed to 'R15 requires it to be listed'", "killed_by": "card_claims_r16.py (c018 assertion)"},
    {"name": "r16_card_mut5_c076_at_least", "description": "LX2-c076 back: Theorem 4.2 'at most' changed to 'at least'", "killed_by": "card_claims_r16.py (c076 assertion)"},
    {"name": "r16_card_mut6_c099_need_not_state", "description": "LX2-c099 back: 'must state that the person is one' changed to 'need not state that the person is one'", "killed_by": "card_claims_r16.py (c099 assertion)"},
    {"name": "r16_card_mut7_c079_45_117", "description": "LX2-c079 back: 44/117 and 0.3761 changed to 45/117 and 0.3846", "killed_by": "card_numbers_r16.py (45/117 absent from L01-L04 text); card_claims_r16.py (c079 assertion)"},
    {"name": "transplant_r13_card_mut2_c100_bias_41_12_to_41_13", "description": "LX2-c100 back bias 41/12 changed to 41/13 (earlier round, re-planted on current cards)", "killed_by": "card_claims_r16.py (c100 assertion); card_numbers_r16.py"},
    {"name": "transplant_r13_card_mut3_c016_300_to_250", "description": "LX2-c016 back holder count 300 changed to 250 (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c016 assertion)"},
    {"name": "transplant_r13_card_mut4_c053_3_104_to_3_105", "description": "LX2-c053 back ratio 3/104 changed to 3/105 (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c053 assertion); card_numbers_r16.py"},
    {"name": "transplant_r14_card_mut2_c010_ten_to_fifteen", "description": "LX2-c010 back notice 'not later than ten days' changed to fifteen days (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c010 assertion)"},
    {"name": "transplant_r14_card_mut3_c096_no_to_yes", "description": "LX2-c096 back answer 'No.' changed to 'Yes.' (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c096 assertion)"},
    {"name": "transplant_r14_card_mut4_c085_3_8_to_3_9", "description": "LX2-c085 back hit rate 3/8 changed to 3/9 (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c085 assertion); card_numbers_r16.py"},
    {"name": "transplant_r15_card_mut1_c104_automatically_to_on_application", "description": "LX2-c104 back 'Automatically' changed to on the issuer's application (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c104 assertion)"},
    {"name": "transplant_r15_card_mut2_c027_15d_to_13a", "description": "LX2-c027 back: 15(d)(1) attribution changed to 13(a) (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c027 assertion)"},
    {"name": "transplant_r15_card_mut3_c081_comply_to_optional", "description": "LX2-c081 back: 'must comply' changed to 'may comply' (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c081 assertion)"},
    {"name": "transplant_r15_card_mut4_c086_mae_3_to_2", "description": "LX2-c086 back: MAE 3 index units changed to 2 (earlier round, re-planted)", "killed_by": "card_claims_r16.py (c086 assertion)"},
]

fragment = {
    "unit": "LX2",
    "slice": "d",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2-d, round 16 (did not build LX2; shares no context with the builders)",
    "pin": "56cc575a774a66e9580d3182969eb7d6aa413731",
    "base": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa (round-15 pin). Delta d1e65a02..56cc575a for the LX2 slice: course/modules/LX/LX2/cards.json only (c030, c094, c097, c099 changed; c105 added).",
    "checkout": ROOT,
    "scratch": "/Users/billyribeiro/.fanout/scratch-LX2-d-r16 (src/ holds the fetched sources; L01..L04.txt stripped lessons also copied into ledgers/LX2/scripts/LX2-d-r16/)",
    "verified_at": "2026-11-09T03:04:09+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "cfandcode: references/references.json record url is https://www.cfainstitute.org/standards/professionals/code-ethics-standards (the Code landing page). That page contains links to the standards and no quoted sentence. Every quoted sentence in cards c061, c064, c065, c077-c081, c087, c088 sits on /standards/professionals/code-ethics-standards/standards-of-practice-iii-a (Updated April 2024) or /standards-of-practice-vi-a (Updated January 2024). Architect to decide whether the record url or the locator convention should change; no builder edits a record.",
        "gpo1983dirks: title field reads 'Dirks v. SEC, 463 U.S. 646 (1982)' and year 1983 (carried from round 15; the opinion reads 'Decided July 1, 1983'). No year is typed in LX2 cards or lessons.",
        "cfandcode: record type 'primary' against the curriculum's '(practitioner)' label (carried from round 15, plan N2)."
    ],
    "freshness_flags": [],
    "notes": [
        "Checkout: detached at 56cc575a (no git operation, no commit, no push). .venv used as provided; vendor copied by the harness.",
        "Line numbers: 'lines N' under a course/modules/LX/LX2/*.html label refer to the stripped text of that page (ledgers/LX2/scripts/LX2-d-r16/L0n.txt, markup removed, one block per line), except where an HTML line is stated explicitly (d-l02-derivative-sentence line 80 and d-l01-sec2-registration-ungraded line 69, both confirmed by grep on the HTML).",
        "Round-16 scripts are in ledgers/LX2/scripts/LX2-d-r16/ (strip_lessons_r16.py, output_in_lesson_r16.py, card_numbers_r16.py, card_arithmetic_r16.py, flow_recheck_r16.py, card_claims_r16.py, make_card_mutants_r16.py, transplant_old_card_mutants_r16.py, write_fragment_r16.py, plus the fetch-side helpers ctx.py, pagefind.py, pf2.py, stat.py and the output files).",
        "Fetched this round with plain curl (no bot check, login or paywall encountered): govinfo USREPORTS-463-646.pdf, USREPORTS-521-642.pdf, COMPS-1884.pdf, COMPS-1885.pdf; federalreserve.gov sr2602.htm and SR2602a1.pdf; cfainstitute.org code landing page and standards-of-practice-iii-a and -vi-a. Text extracted with pdftotext and html parsing into scratch-LX2-d-r16/src.",
        "Two lesson-level FAIL rows are carried from round 15 and re-verified because cards rest on them: d-l02-derivative-sentence (L02.html line 80) and d-l01-sec2-registration-ungraded (L01.html line 69). Both are fixes to the lesson, not to cards.",
        "Card row d-cards-101-103 is FAIL on plan §9 (cards for Dodd-Frank and MiFID II not to be written until B1 and B2 are resolved). The card text is accurate; the rule is the issue. Round 15 passed these cards without citing §9; this round cites it.",
        "Grade observations (not rows): c020 and c021 are graded T as derivations on the page (matches L01 key results); plan §2.1 item 4 would grade a finite enumeration C. Lab-derived cards are graded C naming the lab (verifier rule 9); plan §9 says T. Architect to confirm both.",
        "Card ids c055, c056, c057 are absent; no check requires contiguity. Card basis 'Lab 1' is used in all four lessons (each lesson's own lab); the review deck mixes lessons, so the basis is ambiguous outside its lesson. Observation for the builder.",
        "Mutants: the planted-error set is 7 new (r16) plus 9 earlier planted errors re-planted on the current cards; r13_card_mut5 is moot. Earlier complete-file mutants are not counted as kills because they were built on older baselines.",
        "Not checked: check_projects.py and page_smoke.py (no LX2 project page or project file changed in this delta); pytest (no tool or test changed); verify_refs live run (network-dependent; the offline integrity pass was run and the six cited sources were fetched directly); the statute text was read from the GovInfo compilations as published (amendment through P.L. 119-60 and P.L. 119-27 per each record); the grades of the lesson prose outside the cited claim spans were not re-graded.",
    ],
    "summary": {
        "slice": "LX2-d (all 102 cards.json cards against L01-L04)",
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": len(mutants),
        "mutants": len(mutants),
    },
}

out = os.path.join(ROOT, "ledgers/LX2/LX2-d.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
