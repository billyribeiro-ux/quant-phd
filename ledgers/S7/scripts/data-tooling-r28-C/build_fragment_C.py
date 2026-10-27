"""Round-28 part C: write the per-row decisions (row_decisions.json) and the fragment ledgers/S7/data-tooling-C.json.
Every row keeps its release id. Carried rows keep the architect's prefix with round 27 and 47bac8d. Cited rows use
'Covered by ledgers/S7/<slice>.json row <id> (PASS, re-derived on <pin>)'. Re-derived and re-run rows name their script
and output. Run: python -I build_fragment_C.py <checkout> (after the scripts it cites have run)."""
import json
import re
import sys
from datetime import UTC, datetime

CK = sys.argv[1]
SD = "ledgers/S7/scripts/data-tooling-r28-C"
import subprocess as _sp
# read the round-27 fragment from the pin (c9beb92), never from the file this script rewrites
src = json.loads(_sp.run(["git", "-C", CK, "show", "c9beb92:ledgers/S7/data-tooling-C.json"], capture_output=True, text=True, check=True).stdout)
rows = src["rows"]
by_id = {r["id"]: r for r in rows}
DEC = {}  # id -> (status, category, evidence, reason, [fix])


def old_of(rid):
    """The earlier evidence with its leading carry clause removed and the round-26 'NOT re-derived' lead cut
    (the round-24 record that follows it is kept)."""
    e = by_id[rid]["evidence"]
    e = re.sub(r"^Carried from the release ledger \([^)]*\):\s*", "", e)
    if "round-24 evidence:" in e:
        e = "round-24 evidence:" + e.split("round-24 evidence:", 1)[1]
    return e


def carry(rid, files, extra, reason):
    ev = (f"Carried from round 27 ({files} byte-identical since 47bac8d): {extra} "
          f"Earlier record (rounds 24-26, not re-run in round 28): {old_of(rid)}")
    DEC[rid] = ("PASS", "carry", ev, reason, None)


def cite(rid, cites, extra, reason):
    parts = [f"Covered by ledgers/S7/{ledger} row {row} (PASS, re-derived on {pin}): {why}" for ledger, row, pin, why in cites]
    DEC[rid] = ("PASS", "cite", " ".join(parts) + (" " + extra if extra else ""), reason, None)


def rerun(rid, text, reason, status="PASS", fix=None):
    DEC[rid] = (status, "rerun", text, reason, fix)


def rederive(rid, text, reason, status="PASS", fix=None):
    DEC[rid] = (status, "rederive", text, reason, fix)


L03 = "L03-L04.json"
L01 = "L01-L02.json"
L05 = "L05-L06.json"
L07 = "L07-L08.json"
SUBJ_L03 = "course/modules/S/S7/L03.html"
SUBJ_L07 = "course/modules/S/S7/L07.html"
SUBJ_L08 = "course/modules/S/S7/L08.html"
CARDS = "course/modules/S/S7/cards.json"
REFS = "references/references.json"
LOG = f"{SD}/logs"

# ---------- carried, subject byte-identical since 47bac8d (git diff --quiet), claim not toolchain numerics -------------
carry("r21-L03-s8-hxz", SUBJ_L03, "Crossref 10.1093/rfs/hhy131 re-read today, HTTP 200: title 'Replicating Anomalies', RFS 33(5) 2019-2133; the abstract contains '65%', '452 anomalies' and '1.96' (crossref_reread_C.py; logs in "
      f"{LOG}/crossref_C.out).", "Span bytes unchanged; Crossref record and phrases re-read today.")
carry("r21-L03-s8-chordia", SUBJ_L03, "Crossref 10.1093/rfs/hhaa018 re-read today, HTTP 200: 'Anomalies and False Rejections', RFS 33(5) 2134-2179; abstract contains '2 million', '45%', '3.8' and '3.4' (crossref_C.out).",
      "Span unchanged; Crossref re-read today.")
carry("r21-L03-s8-jkp", SUBJ_L03, "Crossref 10.1111/jofi.13249 re-read today, HTTP 200: JF 78(5) 2465-2518; abstract contains 'different conclusions' and '93 countries' (crossref_C.out).",
      "Span unchanged; Crossref re-read today.")
carry("r21-L03-s8-interpretation", SUBJ_L03, "No number in the sentences; the scope statements are checked against the two Crossref abstracts re-read today (crossref_C.out).",
      "Interpretive sentences unchanged.")
carry("r21-L03-s8-f5-crossref", SUBJ_L03 + ", curriculum/curriculum.json", "F5 is a module id in curriculum/curriculum.json, re-checked today (small_checks_C.py: 'F5 in curriculum modules: True').",
      "Cross-reference target exists today.")
carry("r21-card-c104", CARDS, "Card text unchanged; its three cite keys are checked in the registry rows below and the spans above.",
      "Card unchanged.")
carry("r21-cite-hou2018replicating", REFS, "Entry identical to 5e5da87 except used_by (registry_entries_C.py); Crossref re-read today (crossref_C.out).",
      "Registry entry identical; live Crossref record re-read.")
carry("r21-cite-chordia2020anomalies", REFS, "Entry identical to 5e5da87 except used_by (registry_entries_C.py); Crossref re-read today.",
      "Registry entry identical; live Crossref record re-read.")
carry("r21-cite-jensen2023there", REFS, "Entry identical to 5e5da87 except used_by (registry_entries_C.py); Crossref re-read today.",
      "Registry entry identical; live Crossref record re-read.")
carry("r21-cite-chen2025t", REFS, "Entry identical to 5e5da87 except used_by (registry_entries_C.py); Crossref 10.1287/mnsc.2023.03083 re-read today, HTTP 200, 'Do t-Statistic Hurdles Need to Be Raised?', Management Science 71(7) 5830-5848, abstract contains 'unobserved'.",
      "Registry entry identical; live Crossref record re-read.")
carry("r21-counter-hxz-search", SUBJ_L03, "No new search; the counter-sources named in the span (Jensen-Kelly-Pedersen, Chen) are re-read today in the rows above.",
      "Counter-evidence text unchanged; the named counter-sources re-read today.")
carry("r21-freshness-search", SUBJ_L03 + ", " + SUBJ_L08, "The search itself is not repeated in round 28; flagged in freshness_flags as a recorded lead, not a freshness verdict.",
      "Text unchanged; freshness leads carried as flags.")
carry("r21-L01-s6-sentence", "course/modules/S/S7/L01.html", "git diff -U0 5e5da87..c9beb92 for L01.html names only line 133 (@@ -133 +133 @@); line 255 is unchanged.",
      "Passage unchanged since the release; the only hunk is line 133.")
carry("r23-yaml-header-stale", "tools/data_sources.yaml", "Header lines 11-13 read today: MANIFEST records the H.10 zip retrieved 2026-10-19 (SHA-256 8f370f9c...) and the H.15 zip 2026-10-20 (334a7f88...); the live zips still differ (see r25-data-live-refetch).",
      "Header records the historical retrieval; still accurate.")
carry("counter-ggm1997", SUBJ_L07 + ", " + CARDS + ", " + REFS, "OpenCitations citing count for 10.1214/aop/1024404523 today: 183 rows, 181 with a DOI, identical to the recorded 183 (opencitations_C.out); Crossref re-read today, HTTP 200 (crossref_C.out).",
      "Population unchanged; the screen's record stands.")
carry("r23-gine-attribution", SUBJ_L07 + ", " + CARDS, "Crossref 10.1214/aop/1024404523 re-read today, HTTP 200: 'When is the Student t-statistic asymptotically standard normal?', AoP 25(3); abstract contains 'domain of attraction'.",
      "Span and card unchanged; Crossref re-read.")
carry("r23-gine-scope", SUBJ_L07 + ", " + CARDS, "Crossref 10.1214/aop/1015345757 re-read today, HTTP 200: 'Bootstrapping the Student t-Statistic', AoP 29(4); abstract reads 'if and only if X is in the domain of attraction of a normal random variable and EX = 0' (crossref2_C.out).",
      "Restatement and scope re-read today.")
carry("r23-counter-hlz-chen", SUBJ_L03, "Crossref 10.1287/mnsc.2023.03083 re-read today, HTTP 200; abstract contains 'unobserved' (crossref_C.out).",
      "Counter-source text unchanged; Crossref re-read.")
carry("r23-counter-hlz-omitted", SUBJ_L03, "Crossref re-reads today for 10.1093/rapstu/raz011 (156, 12.3%, 'different perspective'), 10.1111/jofi.13249 and 10.1093/rfs/hhy131, all HTTP 200 (crossref_C.out). The Lu (2025) RePEc abstract is not in Crossref and was not re-read today.",
      "Four counter-sources re-read on Crossref; Lu's RePEc abstract carried.")
carry("r24-L03-s8-cz-span", SUBJ_L03, "Crossref 10.1093/rapstu/raz011 re-read today, HTTP 200: 'Publication Bias and the Cross-Section of Stock Returns', RAPS 10(2) 249-289; abstract contains '156', '12.3%' and 'different perspective'.",
      "Span unchanged; Crossref re-read.")
carry("r24-L03-s8-lu-span", SUBJ_L03, "Lu (2025) has no Crossref abstract (crossref_C.out: 'abstract absent'); the RePEc abstract was not re-read today.",
      "Span unchanged; RePEc abstract carried (not re-read).")
carry("r24-L03-s8-two-estimates-sentence", SUBJ_L03, "See r21-L03-s8-interpretation (same sentence).", "Interpretive sentence unchanged.")
carry("r24-L08-section6-spans", SUBJ_L08, "Crossref re-reads today, HTTP 200: 10.1016/j.jfineco.2011.11.003 (Moskowitz, Ooi, Pedersen; JFE 104(2) 228-250), 10.1016/j.jfineco.2019.08.004 (Huang, Li, Wang, Zhou; JFE 135(3) 774-794), 10.3390/jrfm19010046 (Ahn, Hambusch, Hong; JRFM 19(1) 46, 2026) (crossref2_C.out); registry entries moskowitz2012time, huang2020time, ahn2026overlapping identical to 5e5da87 except used_by (registry_entries_C.py).",
      "Span bytes unchanged; the three records re-read; registry entries identical.")
carry("r24-L03-line-numbers", SUBJ_L03, "Lines 584 and 589 printed today; the Section 8 spans are on line 589 and the derivation on line 584 (checked this round).",
      "Locators unchanged.")
carry("r24-yaml-header-replaced-claim", "tools/data_sources.yaml", "Header line 14 read today: 'Both rebuild the same snapshots byte for byte' (true today: rebuilds from the live zips and from the saved raws are identical, see r25-cmd-fetch_data-fetch and r25-cmd-fetch_data-raw-dir).",
      "Header statement still true; historical 2026-10-17 statement stands as a record.")
carry("r24-test-admit-stores-the-identity-and-the-notes-of-a-new-book", "tests/test_refs.py, tools/add_reference.py", "The test exists (tests/test_refs.py) and passes in the full suite today (437 passed, pytest_full_summary.log).",
      "Test and tool unchanged; test passes today.")
for rid in ["r24-test-admit-keys-an-issuer-document-from-the-issuer-short-name", "r24-test-by-isbn-refuses-a-citation-of-another-edition",
            "r24-test-by-landing-refuses-a-page-that-declares-a-doi", "r24-test-by-landing-refuses-a-site-that-is-not-a-publisher",
            "r24-test-by-doi-resolves-only-articles-and-books", "r24-test-a-primary-document-is-admitted-only-from-its-issuer",
            "r24-test-a-primary-document-must-carry-its-own-title", "r24-test-an-isbn-admission-is-verified-by-open-library",
            "r24-test-a-landing-page-admission-is-verified-by-its-landing-page", "r24-test-a-primary-document-admission-is-verified-by-its-issuer",
            "r24-test-judged-refuses-a-citation-whose-string-differs-from-the-record", "r24-test-judged-says-why-a-record-does-not-match"]:
    carry(rid, "tests/test_refs.py, tools/add_reference.py", "The named test is defined in tests/test_refs.py (grep, round 28) and passes in the full suite today (437 passed).",
          "Test and tool unchanged; the named test exists and passes.")
carry("r23-mut-NB", "tools/add_reference.py, tests/test_refs.py", "Mutant NB1-NB6 killers (test_admit_stores_the_identity_and_the_notes_of_a_new_book) exist and pass today; the mutants were not re-created in round 28.",
      "Mutant rule: target and killer byte-identical; killer passes.")
carry("r23-mut-NK1", "tools/add_reference.py, tests/test_refs.py", "Killer test_admit_keys_an_issuer_document_from_the_issuer_short_name exists and passes today; mutant not re-created.", "Mutant rule carry.")
carry("r23-mut-IE1", "tools/add_reference.py, tests/test_refs.py", "Killer test_by_isbn_refuses_a_citation_of_another_edition exists and passes today; mutant not re-created.", "Mutant rule carry.")
carry("r23-mut-LD1-LA1", "tools/add_reference.py, tests/test_refs.py", "Killers test_by_landing_refuses_a_page_that_declares_a_doi and ..._a_site_that_is_not_a_publisher exist and pass today; mutants not re-created.", "Mutant rule carry.")
carry("r23-mut-KD1", "tools/add_reference.py, tests/test_refs.py", "Killer test_by_doi_resolves_only_articles_and_books exists and passes today; mutant not re-created.", "Mutant rule carry.")
carry("r23-mut-PA1-PR1", "tools/add_reference.py, tests/test_refs.py", "Killers test_a_primary_document_is_admitted_only_from_its_issuer and test_a_primary_document_must_carry_its_own_title exist and pass today; mutants not re-created.", "Mutant rule carry.")
carry("r23-mut-VB1-VB3", "tools/add_reference.py, tests/test_refs.py", "Killers test_an_isbn_admission_is_verified_by_open_library, test_a_landing_page_admission_is_verified_by_its_landing_page and test_a_primary_document_admission_is_verified_by_its_issuer exist and pass today; mutants not re-created.", "Mutant rule carry.")
carry("r23-mut-JC1-JN1", "tools/add_reference.py, tests/test_refs.py", "Killers test_judged_refuses_a_citation_whose_string_differs_from_the_record and test_judged_says_why_a_record_does_not_match exist and pass today; mutants not re-created.", "Mutant rule carry.")
carry("r23-mut-fix-block", "tests/test_refs.py", "The 13 test functions named in the block are defined in tests/test_refs.py and the file passes in full today.", "Test file unchanged; passes today.")
carry("r23-mut-TK1", "tools/add_reference.py, tests/test_refs.py", "Killer test_admit_does_not_reuse_a_key_the_registry_holds exists and passes today; mutant not re-created.", "Mutant rule carry.")

# ---------- re-run or re-derived this round ------------------------------------------------------------------------
rerun("r21-describe-no-container",
      f"Re-run in round 28: describe() on a book with no container gives \"Smith (1995) 'A Title',  None(None)\" and on an article \"Smith (1995) 'A Title', Journal 50(1)\" ({SD}/describe_check_C.py; {LOG}/describe_C.out). tools/add_reference.py is byte-identical since 47bac8d. The output keeps the two-space, trailing-comma form the row records; the line still names no venue or publisher for books, as the row notes.",
      "describe() output re-run; tool unchanged since 47bac8d.")
cite("r21-L03-s1-bonferroni", [(L03, "R21-num-s1", "49def2c", "the Bonferroni line on L03.html line 59 ('Phi^-1(1 - 0.05/1000) = 3.8906', '1 - Phi(3.8906 - 3) = 0.187', '1 - Phi(1.645 - 3) = 0.912') is the same claim, derived on the same page line.")],
     f"Round-28 re-derivation with the standard library ({SD}/closed_forms_C.py; output {LOG}/closed_forms_C.out): Phi^-1(1-0.05/1000) = 3.890592, 1-Phi(3.8906-3) = 0.186572, 1-Phi(1.645-3) = 0.912291 (page 3.8906, 0.187, 0.912). L03.html is byte-identical since 49def2c (git diff --quiet).",
     "Cited to the L03-L04 row and re-derived; both agree with the page.")
cite("r21-figL02-holm-comment", [(L01, "T33-holm-states", "47bac8d", "the Holm figure's states and its published and recomputed rejections are checked from the figure's own code on L02.html."),
                                 (L01, "L02-fig-holm-staircase", "47bac8d", "the holm-staircase figure's controls and readouts were driven in Chromium at 360 and 1280 px, light and dark.")],
     f"Re-derived in round 28 ({SD}/small_checks_C.py; output small_checks_C.out) from figures-L02.js lines 37-38: test 6 has T = 2.64, recomputed p = 0.8291%, published p = 0.84%, Holm step-five threshold 0.05/6 = 0.8333%; so the decision turns on the second significant digit of test 6, as the comment at line 101 says. Test 6 is the fifth p-value in both the published and the recomputed order.",
     "Comment's claim re-derived from the figure's own arrays.")
rederive("r21-figure-L08-cscv-visual",
         f"Viewed in round 28: element screenshots of cscv-explorer at 360 and 1280 px in light and dark taken from the checkout's own course/ tree ({SD}/shots_C.py; PNGs in /tmp/ap1-r5/dt-C-r28/shots/, log.json: 0 console or page errors). All four were viewed: the block strip's strong cells (in-sample blocks A-D), both bar panels, the logit histogram and the captions read as intended; the in-sample strong cells are distinct from the out-of-sample cells in both themes. Observation (not a figure defect): at 360 px the sticky site header overlaps the top control row in the element capture. Also covered by L07-L08 rows r26-drive-L08-light-360, r26-drive-L08-light-1280, r26-drive-L08-dark-360 and r26-drive-L08-dark-1280 (every control driven, readout recomputed).",
         "Four states viewed today; drive rows cover controls.")
rederive("r21-figure-L03-histogram-visual",
         f"Viewed in round 28: element screenshots of pvalue-histogram at 360 and 1280 px in light and dark ({SD}/shots_C.py; PNGs in /tmp/ap1-r5/dt-C-r28/shots/). All four viewed: bars with the 0.75 fill, the dashed estimated pi0 line, the true pi0 line, the lambda rule, axes and the readout (401 of 1000, 0.802) are legible in each state. Also covered by L03-L04 R25-fig-L03-pvalue-histogram (every control driven in both themes, 884 states, 0 mismatches).",
         "Four states viewed today.")
rederive("r21-css-hunks",
         f"Re-derived in round 28 ({SD}/css_contrast_C.py; output css_contrast_C.out) from course.css's active tokens (light :root, dark data-theme block): strong-cell series 0 fill vs bg 3.1178 light / 3.1013 dark (comment 3.1 both); ink vs fill 5.2427 light / 5.0161 dark (5.2, 5.0); other series fill vs bg minimum 2.6430 (2.6); ink vs fill minimum 4.4276 dark (4.4); series 0 colour vs its fill 2.4413 light / 2.9422 dark (2.4, 2.9); .chart .bar at 0.75 minimum 3.3745 light (3.3 or more, series 5); at 0.55 minimum 2.3121 (2.3). The media-query and data-theme dark blocks carry the same values. course.css is byte-identical since 47bac8d.",
         "Every number in the three comments reproduced.")
rederive("r23-L03-hlz-numbers",
         f"Re-read in round 28: Harvey, Liu and Zhu's author PDF (https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF, HTTP 200, 969629 bytes; pdftotext in /tmp/ap1-r5/dt-C-r28/hlz/hlz.txt). Abstract: 'a t-statistic greater than 3.0' (line 17). Appendix A.1: 'Assuming independence, we model observed t-statistics as draws from an exponential distribution with mean parameter λ̂ and a known cutoff point of 2.57'; equation (A.1) P(unobserved) = 1 - exp(-2.57/λ̂) = 71.1%. The L03 span (line 589) states the 3.0 threshold and the extrapolation; the 71.1% figure is the paper's own number. L03.html is byte-identical since 47bac8d.",
         "3.0, 2.57 and 71.1% checked against the paper.")
cite("r23-b7-sweep", [(L01, "L01-L02-cards-coverage-e968af2", "47bac8d", "BUILDER_RULES 7 coverage of L01 and L02 (definitions, theorem statements, key formulas, key results, misconceptions) against cards.json."),
                      (L03, "R25-sweep-cards", "49def2c", "the 62 L03 and L04 cards scanned in full and each card's lesson item checked."),
                      (L05, "R31-cards-coverage", "47bac8d", "the 61 L05 and L06 cards against the definitions, theorem and lemma statements, key-results rows and misconceptions of both lessons."),
                      (L07, "r27-sweep-BR7-coverage", "47bac8d", "the card set of L07 and L08 against their definitions, theorem statements, key formulas, key results and misconceptions.")],
     f"cards.json is byte-identical since 5e5da87 (git diff --quiet); the four pins' lesson subjects are identical to c9beb92 (subject_check.sh output).",
     "Card-coverage sweep covered lesson by lesson by four accepted rows.")
cite("r23-b12-sweep-L03", [(L03, "R25-sweep-BR1.2", "49def2c", "the whole-lesson number sweep of L03 and L04 (visible numbers classed (a), (b), (c); every added or removed number has a row)."),
                           (L03, "R25-num-L03-line584-121", "49def2c", "the line-584 tail numbers 121, 2,524, 2,645 and 0.004."),
                           (L03, "L03-num-M4", "49def2c", "the Problem M4 solution numbers on lines 667-670."),
                           (L03, "R21-fig-L03-pvalue-captions", "49def2c", "the p-value histogram caption numbers on lines 352-353.")],
     f"Round-28 re-derivation of the line-584 and Problem M4 numbers ({SD}/closed_forms_C.py; output closed_forms_C.out): 121.4908, 2524.453, 2645.944 (2,645 is the sum of the displayed 121 and 2,524; the unrounded sum rounds to 2,646, a rounding convention the page's 'about' does not change), sqrt(121)/2645 = 0.004159; lfdr(2.5) = 0.309432, Fdr(2.5) = 0.07478, BH limit 0.08309. L03.html and cards.json are byte-identical since 49def2c.",
     "Whole-lesson sweep plus line-level rows and fresh closed forms.")
cite("r23-b12-sweep-L05-L08", [(L05, "R31-sweep-numbers-L05", "47bac8d", "every numeric token of the visible prose of L05.html was classed (round-35 procedure)."),
                               (L07, "r27-sweep-BR1.2-numbers", "47bac8d", "the whole of L07.html and L08.html read, every visible number checked by a derivation, a lab or card output, a registry value or a counted structure."),
                               (L07, "L08-num-kr-863-lab4", "47bac8d", "the key-results row for Lab 4 (line 882) and rows 857-863 numbers.")],
     "L05.html and L08.html are byte-identical since 47bac8d (subject_check.sh); the L08 hunks at lines 362, 366 and 882 are covered by the L08 rows cited.",
     "Two whole-lesson sweeps plus the L08 hunk rows.")
rerun("r24-yaml-rebuild-identical",
      "Re-run in round 28: a live tools/fetch_data.py --fetch in a scratch copy of c9beb92 ({LOG}/fetch_live.log: 3 datasets, 0 problems) rebuilt fx_daily.csv, fx_monthly.csv and ust_daily.csv byte-identical to the committed files (cmp); the --raw-dir rebuild from the saved raw downloads was also byte-identical ({LOG}/fetch_rawdir.log). The header statement on line 14 is true today.",
      "Live and raw-dir rebuilds byte-identical today.")
cite("r24-L03-e1-tail-derivation", [(L03, "R25-num-L03-line584-121", "49def2c", "the line-584 arithmetic 200 x 450 x 0.0013499 = about 121."),
                                    (L03, "R25-num-L03-line584-2524", "49def2c", "200 x 50 x 0.2524 = 2,524 on line 584."),
                                    (L03, "R25-num-L03-line584-2645", "49def2c", "121 + 2,524 = 2,645 on line 584."),
                                    (L03, "R25-num-L03-line584-se", "49def2c", "sqrt(121)/2645 = 0.004 on line 584.")],
     f"The claim sits in the pooled-check paragraph on line 584 (the interpretation of Lab 4; the release row labelled it 'E1', which is the wrong label). Round-28 re-derivation ({SD}/closed_forms_C.py): 121.4908, 2524.453, sqrt(121)/2645 = 0.004159.",
     "Same paragraph and numbers; locator label corrected.")
cite("r24-L03-M4-derivation", [(L03, "L03-math-M4", "49def2c", "Problem M4 (lines 663-672): pi0 = 0.9, f0 = N(0,1), f1 = N(3,1), lfdr(2.5) = 0.309, Fdr(2.5) = 0.0748, 'four times' the tail rate."),
                              (L03, "L03-num-M4", "49def2c", "the solution's numbers on lines 667-670.")],
     f"Round-28 re-derivation ({SD}/closed_forms_C.py; output closed_forms_C.out): phi(2.5) = 0.017528, phi(-0.5) = 0.352065, lfdr(2.5) = 0.309432, S0 = 0.00621, S1 = 0.69146, pi0 S0 = 0.005589, pi1 S1 = 0.069146, Fdr(2.5) = 0.07478, BH limit S0/S = 0.08309 (= Fdr/pi0), lfdr/Fdr = 4.14; all as printed on lines 667-670.",
     "Every printed M4 number re-derived.")
cite("r24-L03-histogram-caption-readout", [(L03, "R25-fig-L03-pvalue-histogram", "49def2c", "every control of pvalue-histogram across its range at 360 and 1280 px, light and dark; readout and desc compared with the Python port in 884 states, 0 mismatches."),
                                           (L03, "R21-fig-L03-pvalue-captions", "49def2c", "the caption's leak and sd numbers (0.0005, 0.028, 0.018, 0.008, 2.39) at lambda 0.5 and 0.05."),
                                           (L03, "L03-num-s6", "49def2c", "the Storey span and the caption's default-seed values (seed 22: 401 of 1000, 0.802).")],
     "L03.html, figures-L03.js, multitest.js, stats.js are byte-identical since 49def2c (subject_check.sh). Viewed again today: pvalue-histogram at 360 and 1280 px, light and dark (see r21-figure-L03-histogram-visual).",
     "Readout and caption numbers covered by three accepted rows; visuals viewed today.")
rederive("r24-L03-figure-360-screenshot",
         f"Viewed in round 28: pvalue-histogram at 360 px in dark ({SD}/shots_C.py -> {LOG}/shots_log.json (PNGs kept in the scratch folder)). Axes labelled (p-value; Density (1 = uniform)), legend, lambda rule, pi0 line, source line and caption legible; no clutter or overlap in the figure itself. Also R25-fig-visual (L03-L04, five screenshots viewed at 190cd51).",
         "Screenshot viewed today at 360 px dark.")
carry("r24-L07-c071", SUBJ_L07 + ", " + CARDS, "Card S7-c071 (grade T) and its lesson passage are unchanged; the accepted L07-L08 row r24-card-S7-c071 records the card check (cards.json identical since 47bac8d).",
      "Card unchanged; grade and lesson passage re-checked by the L07-L08 ledger.")
cite("r24-L07-c205", [(L07, "card-S7-c205", "47bac8d", "S7-c205 (grade T, formula (1) and the normal formula), the card's numbers and its lesson's Example 1.4.")],
     f"Re-derived in round 28 ({SD}/small_checks_C.py; output small_checks_C.out): V = 1 - (-2)(0.1) + (9-1)/4 (0.1)^2 = 1.22; normal 1 + 0.1^2/2 = 1.005; 1 - 1.005/1.22 = 0.1762, the '18%' of the card.",
     "Card claim and its arithmetic reproduced.")
cite("r24-L08-jiang-span", [(L07, "r23-jiang-attribution", "47bac8d", "the Jiang, Peng, Qin and Yang span on line 362 (data-cite jiang2025endogeneity, locator Abstract, grade B); the same span text and citation.")],
     "Crossref 10.1214/24-aoas1983 re-read today, HTTP 200 (crossref_C.out): 'Endogeneity and moments in time series momentum's predictability test', AoAS 19(1) 701-719; abstract contains 'size distortion' and 'endogeneity'. L08.html and the registry entry jiang2025endogeneity are identical to 5e5da87 except used_by.",
     "Span re-read today against the live Crossref record.")
cite("r24-L08-table-row-simulated", [(L07, "L08-num-kr-863-lab4", "47bac8d", "the Lab 4 key-results row numbers (DSR 0.489 and 0.228, PBO 0.733, 21% null share) on line 882 and rows 857-863."),
                                    (L07, "L08-kr-lab4", "47bac8d", "the same row's grade C and its SIMULATED basis.")],
     "L08.html is byte-identical since 47bac8d; the row is at line 882.", "Row numbers and grade covered by two accepted rows.")
cite("r24-L08-lab4-hypothesis-simulated", [(L07, "r24-label-simulated-lab4-null", "47bac8d", "the SIMULATED label on the resampled null in the Lab 4 hypothesis at line 366 (BUILDER_RULES 1.7 and 6.7)."),
                                           (L07, "L08-lab-4-preregistration", "47bac8d", "the hypothesis and its expected output checked against the twin.")],
     f"Read in round 28: tests/labs/S7/lab-S7-L08-4.py lines 194-199: rng = np.random.default_rng(4008); draw = changes[rng.integers(0, len(changes), size=len(changes))] (whole months, with replacement, seeded), as the sentence says. The twin and L08.html are byte-identical since 47bac8d.",
     "Sentence matches the seeded twin code.")
cite("r24-L08-c167", [(L07, "card-S7-c167", "47bac8d", "S7-c167 (grade C, basis 'Lab 4 (H.10 spot rates ...; SIMULATED resampled null)'), the back's numbers DSR 0.489, 0.228, PBO 0.733 and 21 of 100."),
                      (L07, "L08-grade-lab4-interpretation", "47bac8d", "the Lab 4 interpretation's grades and the card's basis.")],
     "cards.json and L08.html are byte-identical since 47bac8d.", "Card grade and basis covered by two accepted rows.")
carry("r24-L08-lab3-twin-unchanged", "tests/labs/S7/lab-S7-L08-3.py, " + SUBJ_L08, "run_labs --all in round 28: 'run_labs S7: PASS (42/42)', 'run_labs AP1: PASS (22/22)' (logs/run_labs_all.log), which compares each page block with its twin.",
      "Twin and page block re-run today.")
DEC["r24-L08-lab3-twin-unchanged"] = ("PASS", "rerun", DEC["r24-L08-lab3-twin-unchanged"][2], "run_labs re-run today; the twin is byte-identical since 47bac8d.", None)
cite("r24-counter-cz-screen", [], "OpenCitations citing count for 10.1093/rapstu/raz011 re-read today: 83 citing rows, 32 created 2024-2026, 83 with a DOI, identical to the screen's 83 and 32 (opencitations_C.out); the 15 recent citing DOIs read by title in round 24 are the recorded screen; the population is unchanged.",
     "Screened population unchanged; screen result carried.")
DEC["r24-counter-cz-screen"] = ("PASS", "carry", "Carried from round 27 (" + SUBJ_L03 + ", " + REFS + " byte-identical since 47bac8d): " + DEC["r24-counter-cz-screen"][2] + " Earlier record (rounds 24-26): " + old_of("r24-counter-cz-screen"), "Screened population unchanged today; screen result carried.", None)
DEC["r24-counter-jkp-screen"] = ("PASS", "carry", "Carried from round 27 (" + SUBJ_L03 + ", " + SUBJ_L08 + " byte-identical since 47bac8d): OpenCitations citing count for 10.1111/jofi.13249 today: 408 rows, 297 created 2024-2026, 405 with a DOI, identical to the recorded 408 and 297 (opencitations_C.out). The round-24 title screen covered the first 70 distinct recent citing DOIs of 297; that partial scope is stated, not extended. Earlier record (rounds 24-26): " + old_of("r24-counter-jkp-screen"), "Population unchanged; the partial title screen is carried with its scope stated.", None)
DEC["r24-counter-jiang-lu-screen"] = ("PASS", "carry", "Carried from round 27 (" + SUBJ_L08 + " byte-identical since 47bac8d): OpenCitations returns 0 citing rows today for 10.1214/24-aoas1983 and for 10.1016/j.frl.2025.108491, as recorded (opencitations_C.out). Earlier record (rounds 24-26): " + old_of("r24-counter-jiang-lu-screen"), "Index counts unchanged (zero); the statement about the index holds today.", None)
rederive("r24-test-labs-l08-lab3",
         f"Independent recomputation in round 28 ({SD}/l08_lab3_pbo_C.py; output {LOG}/l08_lab3_pbo_C.out): the test's 8 x 3 matrix, 4 blocks, C(4,2) = 6 splits, performance = Sharpe (mean / sd, ddof 1) as in the twin, mid-rank for ties. Every split: the in-sample winner (configuration 2 or 3) ranks 2 of 3 out of sample, omega = 0.5, logit exactly 0; PBO = 1.0. The docstring's claims hold. The test passes today (pytest tests/test_labs.py -k test_l08_lab3..., 1 passed).",
         "Test docstring's claims recomputed independently; test passes.")
carry("r24-reg-jiang2025endogeneity", REFS, "Entry jiang2025endogeneity identical to 5e5da87 except used_by (registry_entries_C.py); verify_refs --offline today: 560 entries, 0 problems.",
      "Registry entry identical to the release.")
rerun("r24-site-jiang2025endogeneity", "Re-run in round 28: tools/build_site.py --check -> 'site data current: 6 outputs' (exit 0). course/assets/data/references.json is byte-identical since 5e5da87 (git diff --quiet).",
      "build_site --check re-run; generated site data current.")
rederive("r23-b12-sweep-L07",
         f"Re-derived in round 28 ({SD}/closed_forms_C.py and mc_example55_C.py; outputs closed_forms_C.out and mc_example55_C.out): theta = 50217/500000 = 0.100434; SE = sqrt(0.100434/1259) = 0.008932; Z = 2.2392 (2.239); two-sided p = 0.0251 (0.025); naive variance 2.0026, naive SE 0.03988, naive Z 0.5015, p 0.616 (0.62); SE ratio 4.465 (4.5); annual SE 0.4478 (0.448); E4 mean 2.2392, rejection 0.60989 (0.61), naive sd 0.2239, (1.960 - 0.50)/0.224 = 6.52. Seeded Monte Carlo (seed 20281028, 40000 replications, T = 1260): paired rejection 0.6107 (MC SE 0.0024), naive 0 of 40000. Lines 437-443 and 707-713 are byte-identical since 47bac8d. Also L07-L08 rows L07-num-ex5.5 and r27-sweep-BR1.2-numbers.",
         "Every displayed Example 5.5 and E4 number re-derived; MC run independently.")
cite("r24-L07-ex55-se", [(L07, "r26-hunk-L07-440", "47bac8d", "the standard-error sentence on line 440: sqrt(0.100434/1259) = 0.008932 replaces sqrt(0.10043/1259), and every dependent value.")],
     f"Re-derived in round 28 ({SD}/closed_forms_C.py): sqrt(0.100434/1259) = 0.008932, Z = 0.02/0.008932 = 2.2392, p = 0.0251, naive SE 0.03988 (sqrt(2.0026/1259)), naive Z 0.5015, ratio 4.465.",
     "SE expression and its consequences re-derived.")
cite("r24-L07-ex55-theta", [(L07, "L07-num-ex5.5", "47bac8d", "every displayed quantity of Example 5.5 (lines 438-440, display on line 439) and its dependents.")],
     f"Re-derived in round 28 ({SD}/closed_forms_C.py): theta = 2(0.05) + (0.0036+0.0016)/2 - 0.0024 x 0.9025 = 50217/500000 = 0.100434 exactly, as the display on line 439 states.",
     "Theta display re-derived in exact arithmetic.")
cite("r25-L07-l710-e4", [(L07, "r27-E4-derivation", "47bac8d", "the Problem E4 setup and its solution (lines 707-710), re-derived from scratch with the mean 2.239 and the rejection probability about 0.61."),
                         (L07, "r27-hunk-L07-710", "47bac8d", "the one changed line 710, its numbers (0.100434 in three places).")],
     f"Re-derived in round 28 ({SD}/closed_forms_C.py and mc_example55_C.py): mean 0.02 sqrt(1259)/sqrt(0.100434) = 2.2392 (2.239); Phi(2.239 - 1.960) + Phi(-2.239 - 1.960) = 0.60989 (0.61); naive sd 0.2239 (0.224); 4000-replication MC error sqrt(0.61 x 0.39/4000) = 0.0077 (0.008); Monte Carlo paired rejection 0.6107.",
     "E4 solution numbers re-derived and simulated.")
rederive("r25-L07-mc-setting",
         f"Independent seeded Monte Carlo in round 28 ({SD}/mc_example55_C.py; output {LOG}/mc_example55_C.out): seed 20281028, 40000 replications of T = 1260 days, r1 = 0.06 + x0, r2 = 0.04 + 0.95 x0 + sqrt(1 - 0.95^2) x1 with x0, x1 iid N(0,1); paired rejection rate 0.6107 (MC SE 0.0024; page 'about 0.61'); naive rejection 0 of 40000 (page 'none'); mean paired Z 2.2415 (closed form 2.239); mean naive Z 0.5023 (0.50). Setting on lines 437-443 and 707-713 (byte-identical since 47bac8d).",
         "Page's rejection rates reproduced by an independent seeded run.")
rederive("r25-hours-S7",
         f"Re-summed in round 28 ({SD}/hours_S7_C.py; output {LOG}/hours_S7_C.out): curriculum/curriculum.json (parts[3].modules: S7 hours 100); hub data-hours-lessons 70 + data-hours-project 30 = 100; lesson data-hours L01-L08 = 10, 7, 8.5, 8.5, 11, 7, 10, 8 = 70; project.html data-hours-project = 30; project share 30%.",
         "Hub, lessons, project and curriculum hours re-summed: all equal.")
rerun("r25-diff-scope",
      "Re-run in round 28: git diff --stat 5e5da87 c9beb92: 380 files changed (79 outside ledgers/). git diff -U0 5e5da87 c9beb92 over course/modules/S/S7 and project.html: exactly two single-line hunks (@@ -133 +133 @@ in L01.html; @@ -195 +195 @@ in project.html), each named by R26-L01-caption-numbers and R26-project-line195. The coverage of the 79 non-ledger files by the data-tooling rows is R26-diff-coverage (FAIL).",
      "S7 page hunks re-listed; the repository-wide coverage claim is in R26-diff-coverage.")
rerun("r25-banned-phrases",
      f"Re-run in round 28 ({SD}/banned_added_C.py): the 16 lines added since 5e5da87 in course/modules/S/S7 and tools/data_sources.yaml contain none of the banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly half, the ellipsis character). Observation: 26 ellipsis tokens ('...' or the character) in L01-L08 HTML (not changed lines; the earlier '30' count was not reproduced); BUILDER_RULES 1.3 bans an ellipsis standing for omitted content, so these are reported, not decided.",
      "Banned-phrase scan of every added line re-run; no hit.")
rerun("r25-data-live-refetch",
      "Re-run in round 28: live tools/fetch_data.py --fetch in a scratch copy (fetch_live.log): fx_daily 6706 rows, fx_monthly 669, ust_daily 6690; the three CSVs are byte-identical to the committed files. Today's raw zips: H.10 sha256 17d087d0... (MANIFEST 8f370f9c..., retrieved 2026-10-19); H.15 sha256 0a5685bd... (MANIFEST 334a7f88..., retrieved 2026-10-20). Per VERIFIER_RULES 2.8 the snapshot criterion passes; the raw-hash divergence is a freshness flag, unchanged since round 26.",
      "Snapshots rebuild byte-identically; raw-hash divergence recorded as a flag.")
rerun("r25-licence-disclaimer",
      "Re-read in round 28 with plain curl (no bot check or block met): https://www.federalreserve.gov/disclaimer.htm HTTP 200, 85130 bytes, the sentence 'may be copied and distributed without permission. Please cite to the Board as the source of the information' present; it grants redistribution.",
      "Licence page re-read today, quoted sentence present.")
rerun("r25-registry-live-S7",
      "Re-run in round 28: tools/verify_refs.py --unit S7 (live): 'live re-verification of S7: 94 of 560 entries, 0 problems' (exit 0; logs/verify_refs_unit_S7_live.log). Whole-registry live run: 'live re-verification: 560 entries, 0 problems' (logs/verify_refs_whole_live.log). verify_refs --offline: 560 entries, 0 problems.",
      "S7 scope and whole registry re-verified live today.")
rerun("r25-collect-identical",
      f"Re-run in round 28: pytest --collect-only -q (five slice files) twice with -o addopts='': the two outputs are byte-identical ({SD}/logs/collect_slice5_a.txt and _b.txt; '331 tests collected').",
      "Collection identical across two runs; 331 tests.")
rerun("r25-cmd-ruff-check", "Re-run in round 28: .venv/bin/ruff check . -> 'All checks passed!' (exit 0; logs/ruff_check.log).", "Lint gate re-run.")
rerun("r25-cmd-ruff-format", "Re-run in round 28: .venv/bin/ruff format --check . -> '124 files already formatted' (exit 0; logs/ruff_format.log).", "Format gate re-run (124 files; the earlier 125 count is a changed file count).")
rerun("r25-cmd-mypy", "Re-run in round 28: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 101 source files' (exit 0; logs/mypy.log).", "Strict mypy re-run (101 files; the earlier 102 is a changed file count).")
rerun("r25-cmd-pytest-slice", "Re-run in round 28: the 11 slice test files (test_fetch_data, test_labs, test_page_checks, test_refs, test_build_site, test_run_labs, test_page_smoke, test_fetch_vendor, test_koning_spot, test_figure_kernels, tests/js): '391 passed in 46.29s' (exit 0; logs/slice_tests_summary.log).", "Slice tests re-run: 391 passed.")
rerun("r25-cmd-run_labs", "Re-run in round 28: tools/run_labs.py --all -> 'run_labs S7: PASS (42/42)', 'run_labs AP1: PASS (22/22)' (exit 0; logs/run_labs_all.log).", "run_labs re-run.")
rerun("r25-cmd-check_pages-unit", "Re-run in round 28: tools/check_pages.py --all -> 'check_pages S7: PASS', 'check_pages AP1: PASS' (exit 0; logs/check_pages_all.log).", "check_pages re-run (S7 unit included).")
rerun("r25-cmd-check_pages-all", "Re-run in round 28: tools/check_pages.py --all -> S7 and AP1 PASS (exit 0; logs/check_pages_all.log).", "check_pages --all re-run.")
rerun("r25-cmd-check_dag", "Re-run in round 28: tools/check_dag.py --all -> S7 and AP1 PASS (exit 0; logs/check_dag_all.log).", "check_dag re-run.")
rerun("r25-cmd-check_projects", "Re-run in round 28: tools/check_projects.py --all -> S7 and AP1 PASS (exit 0; logs/check_projects_all.log).", "check_projects re-run.")
rerun("r25-cmd-verify_refs-unit-S7", "Re-run in round 28, live, unmodified tool: tools/verify_refs.py --unit S7 -> 'live re-verification of S7: 94 of 560 entries, 0 problems' (exit 0; logs/verify_refs_unit_S7_live.log).", "Live S7 registry run re-run.")
rerun("r25-cmd-verify_refs-offline", "Re-run in round 28: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (exit 0; logs/verify_refs_offline.log).", "Offline whole-registry integrity re-run.")
rerun("r25-cmd-build_site-check", "Re-run in round 28: tools/build_site.py --check -> 'site data current: 6 outputs' (exit 0; logs/build_site_check.log).", "build_site --check re-run.")
rerun("r25-cmd-fetch_data-check", "Re-run in round 28: tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems' (exit 0; logs/fetch_data_check.log).", "fetch_data --check re-run.")
rerun("r25-cmd-fetch_data-fetch", "Re-run in round 28: tools/fetch_data.py --fetch in a scratch copy of c9beb92 (live, saved raws to /tmp/ap1-r5/dt-C-r28/fetch/raw): 'fetch_data: 3 datasets, 0 problems' (exit 0); the three CSVs byte-identical to the committed files (cmp).", "Live fetch re-run in scratch; CSVs identical.")
rerun("r25-cmd-fetch_data-raw-dir", "Re-run in round 28: tools/fetch_data.py --fetch --raw-dir on the raws saved by the live run: 'fetch_data: 3 datasets, 0 problems' (exit 0; fetch_rawdir.log); CSVs byte-identical.", "Raw-dir rebuild re-run; identical.")
rerun("r25-cmd-render_curriculum", "Re-run in round 28: tools/render_curriculum.py, then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json (exit 0; logs/curriculum_diff.log).", "render_curriculum re-run; no diff.")
rerun("r25-cmd-pytest-full", "Re-run in round 28: .venv/bin/python -m pytest (whole suite, addopts cleared for the summary): '437 passed in 51.28s' ({LOG}/pytest_full_summary.log). The earlier 434 count is not reproduced; the test count grew with the vendor tests (11 in test_fetch_vendor.py).", "Full suite re-run: 437 passed.")
rerun("r25-cmd-run_graders-S7", "Re-run in round 28: tools/run_graders.py --all --seeds 0-49 -> 'run_graders S7: PASS (reference 50/50 seeds, slowest 1.6 s)' and AP1 PASS 50/50 (exit 0; logs/run_graders_all.log).", "run_graders re-run.")
carry("r25-cmd-mutant-run", "tools/add_reference.py, tests/test_refs.py", "The 66 add_reference mutants are not re-created in round 28; their killing tests in tests/test_refs.py pass today (full suite 437 passed; the 83 distinct killers from part A pass, run_killers_C.py).",
      "Mutant rule: target and killer byte-identical since 47bac8d; killers pass.")
rerun("r25-cmd-page_smoke-S7", "Re-run in round 28: tools/page_smoke.py --unit S7 --pages L01 L02 L03 L05 L06 L07 L08 project -> 'page_smoke S7: PASS' (exit 0; logs/page_smoke_S7.log); tools/page_smoke.py --all -> 'page_smoke all: PASS' (exit 0; logs/page_smoke_all.log).", "page_smoke re-run (S7 and all units).")
rerun("r25-cmd-git-status", "Re-run in round 28 at the end of the work: git status --short in the verifier checkout shows '?? .venv' (the pre-existing symlink) and '?? ledgers/S7/scripts/data-tooling-r28-C/' (this round's archived scripts and logs); the only tracked file modified is ledgers/S7/data-tooling-C.json (this part fragment).", "git status clean apart from the archived scripts.")
cite("r25-cmd-page_smoke-dark-sweep", [(L01, "L02-fig-holm-staircase", "47bac8d", "the five live figures of L01 and L02 driven at 360 and 1280 px, light and dark (every control)."),
                                       (L03, "R25-cmd-chromium-drive", "49def2c", "the five live figures of L03 and L04 driven in Chromium at 360 and 1280 px, light and dark."),
                                       (L05, "R31-fig-L05-stepm-steps", "47bac8d", "drive_figures.py drove every control of every figure on L05 and L06 at 1280 and 360 px, light and dark."),
                                       (L07, "r25-fig-drive-L07", "47bac8d", "dsr-explorer driven across its range at 360 and 1280 px, light and dark."),
                                       (L07, "r25-fig-drive-L08", "47bac8d", "cscv-explorer driven across its range at 360 and 1280 px, light and dark.")],
     "project.html has no data-chart element (grep, round 28), so it carries no interactive figure. Every figure control of L01-L08 is therefore covered in both themes at 360 and 1280 px by these accepted rows; the page_smoke tool itself sweeps the light theme only (its docstring), which these drives supplement.",
     "Dark-theme figure coverage established by the lesson ledgers.")
rerun("R26-vendor-two-systems",
      "Re-verified in round 28 at c9beb92: tools/vendor.py, course/assets/vendor/SPEC.yaml and tests/test_vendor.py are absent (git cat-file); tools/fetch_vendor.py is the one vendoring path and reads tools/vendor_spec.yaml; tools/fetch_vendor.py --check -> 'vendor: 56 files, 0 problems' (exit 0; logs/fetch_vendor_check.log); the default mode also returns 'vendor: 56 files, 0 problems'; tests/test_fetch_vendor.py is in the slice run (391 passed). The retired-name grep is clean (see R27-stale-spec-pointer).",
      "One vendoring path confirmed; retired files absent; check passes.")
rerun("R26-ci-gates-commands",
      "Re-run in round 28 at c9beb92, each CI step's command as written: ruff check ., ruff format --check . (124 files), mypy --no-incremental (101 files), pytest (437 passed), render_curriculum + git diff --exit-code (exit 0), build_site --check (6 outputs), verify_refs --offline (560, 0), fetch_data --check (3 datasets, 0 problems), check_pages / check_dag / check_projects --all (S7 and AP1 PASS), fetch_vendor (56 files, 0 problems), run_labs --all (S7 42/42, AP1 22/22), run_graders --all --seeds 0-49 (S7 and AP1 PASS), mutate_graders --all --seeds 0-9 (S7 164/164 killed, AP1 69/69 killed), playwright install --dry-run chromium (exit 0), fetch_data --fetch in a scratch copy (CSVs identical). All exit 0. Logs under " + LOG + ".",
      "Every CI command re-run at the pin.")
rerun("R26-ci-not-run-here",
      "Run in round 28 at c9beb92: tools/page_smoke.py --all -> 'page_smoke all: PASS' (exit 0; logs/page_smoke_all.log, 23 pages reported PASS); tools/verify_refs.py with no unit (whole registry, live) -> 'live re-verification: 560 entries, 0 problems' (exit 0; logs/verify_refs_whole_live.log).",
      "Both steps CI cannot run here were run today.")
rerun("R26-data-rebuild-live",
      "Re-run in round 28: live rebuild in a scratch copy of c9beb92 (tools/fetch_data.py --fetch): fx_daily 6706 rows, fx_monthly 669 rows, ust_daily 6690 rows; all three CSVs byte-identical to the committed ones (cmp). Raw hashes divergence from MANIFEST persists (H.10 17d087d0... vs 8f370f9c...; H.15 0a5685bd... vs 334a7f88...), recorded as freshness, not a failure (VERIFIER_RULES 2.8).",
      "Live snapshot rebuild identical today.")
rerun("R26-licence-pages",
      "Re-read in round 28 with plain curl (default user agent; no bypass): https://www.federalreserve.gov/disclaimer.htm HTTP 200 (85130 bytes); /releases/h10/about.htm HTTP 200 (84844 bytes; 'Last Update: February 06, 2023'; 'certified by the Federal Reserve Bank of New York for customs purposes'); /releases/h15/default.htm HTTP 200 (105950 bytes; 'Source: U.S. Treasury'); /data/data-download-fred-information.htm HTTP 200 (85993 bytes; 'Build Your Package' removal 'the week of November 9, 2026'). Sizes and text match the round-26 record.",
      "All four pages re-read today.")
rederive("R26-L01-caption-numbers",
         f"Re-derived in round 28 by the archived round-26 script on scipy 1.18.0 / numpy 2.4.6 ({SD}/../data-tooling-r26/l01_figcaption_gaps.py; output {LOG}/l01_caption_C.out): N=10 bound 2.145966 (2.146), exact 1.538753 (1.539), gap 0.607213 (0.61); N=100 bound 3.034854 (3.035), exact 2.507594 (2.508), gap 0.527261 (0.53); N=10000 bound 4.291932 (4.292), exact 3.851616 (3.852), gap 0.440316 (0.44). Every figure matches line 133.",
         "Caption numbers re-derived on the new toolchain.")
rederive("R26-project-line195",
         "Verified in round 28: course/modules/S/S7/project.html line 195 reads 'Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs.'; course/assets/vendor/pyodide/pyodide-lock.json: info.python 3.14.2, numpy 2.4.6, pytest 9.0.2 (python -I read). The versions match.",
         "Sentence matches the Pyodide lock.")
rederive("R26-figure-kernel-tolerance",
         f"Re-derived in round 28 with the page's own normCdf (node 24.22.0 importing course/assets/js/stats.js; {SD} uses ledgers/S7/scripts/data-tooling-r26/normcdf_compare.mjs): normCdf(-3) = 0.0013498980316301150, NormalDist(0,1).cdf(-3) = 0.0013498980316300957, relative difference 1.43e-14; at -0.5, 0, 1.2, 4 the values agree to 1e-16. The tolerance rel = max(1e-12, 5e-14(n-1)) at lines 355-361 covers it; tests/test_figure_kernels.py passes in the full suite.",
         "Relative difference 1.43e-14 reproduced; tolerance covers it.")
rerun("R26-koning-spot-test", "Re-run in round 28: tests/test_koning_spot.py (53 lines) passes in the slice run (391 passed) and the full suite (437 passed).", "Spot-check test passes today.")
rerun("R26-page-smoke-changes", "Re-run in round 28: tools/page_smoke.py --unit S7 PASS (logs/page_smoke_S7.log); tests/test_page_smoke.py and tests/js (katex_strict.test.mjs) pass in the slice run (391 passed).", "page_smoke changes exercised today.")
rerun("R26-run-labs-tool", "Re-run in round 28: tools/run_labs.py --all -> S7 42/42, AP1 22/22 (exit 0); tests/test_run_labs.py passes in the slice run.", "run_labs tool re-run; tests pass.")
rerun("R26-requirements-pins", "Re-run in round 28 (importlib.metadata under python -I): ruff 0.17.2, mypy 2.4.0, pytest 9.0.2, numpy 2.4.6, scipy 1.18.0, playwright 1.64.1, pyyaml 6.0.3; requirements.txt and requirements-dev.txt pins match.", "Installed versions match the pins.")
rerun("R26-mypy-excludes", "Re-run in round 28: pyproject.toml [tool.mypy] exclude = ['^tests/labs/S7/lab-S7-L08-4\\.py$', '^tests/labs/S7/lab-S7-L03-2\\.py$'] with the reason in the comment on lines 33-35; mypy --no-incremental passes (101 files).", "Exclusion and its stated reason confirmed.")
rerun("R26-killer-ids", "Re-run in round 28: the 83 distinct killing node ids from the 152 tooling mutants (ledgers/S7/data-tooling-A.json mutants[].killed_by; the file is now part A, not data-tooling.json): pytest on all 83 -> exit 0 (run_killers_C.py; killers_C.out).", "All 83 killer ids collect and pass today.")
carry("R26-mutants-152-rerun", "tools/add_reference.py, tools/verify_refs.py, tools/refs/match.py, tools/fetch_data.py, tests/test_fetch_data.py, tools/check_pages.py, tests/test_page_checks.py, tests/labs/S7, tests/test_labs.py, tools/build_site.py", "The mutant entries are in ledgers/S7/data-tooling-A.json (152, not in this part); their 83 distinct killers pass today (run_killers_C.py). Targets and killers are byte-identical since 47bac8d; mutants not re-created in round 28.",
      "Mutant rule carry with killers re-run.")
rederive("R26-test-memo-exemplars", "Verified in round 28: tests/test_memo_exemplars.py line 133 reads 'n_obs, _n_trials = trials.shape' (the renamed unused count); the file passes in the full suite (437 passed); ruff clean.", "One-line rename confirmed; test passes.")
rederive("R27-stale-spec-pointer",
         "Verified in round 28 by reading and grepping. course/assets/css/tokens.css line 6 now reads '/* ---------- Fonts (vendored; see tools/vendor_spec.yaml) ---------- */' (commit d72d273), and tools/vendor_spec.yaml is the spec that lists the @fontsource packages (its lines 21-44). A grep for 'SPEC.yaml' (uppercase) and 'tools/vendor.py' over the repository, excluding ledgers/ and the vendored library folders, finds no retired name; the only remaining match of 'vendor.py' is tools/fetch_vendor.py, which is the live tool. check_pages and page_smoke (S7) pass.",
         "Stale pointer fixed; grep clean; checks pass.")

# ---------- the one FAIL ---------------------------------------------------------------------------------------------
DEC["R26-diff-coverage"] = ("FAIL", "fail",
    "Computed in round 28 (" + SD + "/diff_coverage_C.py): git diff --name-only 5e5da87 c9beb92 lists 79 non-ledger files; 44 are named by a row of data-tooling-A/B/C (path or basename); 35 are not named. Of the 35, three are in this slice's scope and have no row: course/assets/data/glossary.json, course/assets/data/program.json (generated by tools/build_site.py; covered in substance by build_site --check, which is not named) and tests/js/rubric.test.mjs (run by pytest's JS test; not named). The other 32 are outside the data-tooling scope: AP1 pages, labs, grader and curriculum source (ledgers for AP1), README.md, atlas/A8.contract.md (the S7 project's contract), site-wide CSS base.css and components.css, course/concepts.html, course/dev/design-system.html, curriculum/03-markets.yaml. The unnamed list is printed by the script.",
    "A changed file in scope is not named by any row; the claim 'every changed file is named' is not met.",
    "Add a row naming course/assets/data/glossary.json, course/assets/data/program.json and tests/js/rubric.test.mjs (checked by build_site --check and the JS tests), and have the AP1, project and site owners name their files; then re-run diff_coverage_C.py.")


carry("r23-L03-hlz-attribution-scope", SUBJ_L03, "HLZ author PDF re-read today (HTTP 200): Appendix A.1, 'Assuming independence, we model observed t-statistics as draws from an exponential distribution with mean parameter λ̂ and a known cutoff point of 2.57'; the 3.0 threshold is the abstract's conclusion ({LOG}/hlz_pdftotext.txt lines 17, 2250-2251).",
      "Model and conclusion re-read in the paper today.")
rerun("r25-collect-identical", f"Re-run in round 28: pytest --collect-only -q on the five slice files, twice, with -o addopts='': the two outputs are byte-identical; '331 tests collected' ({SD}/logs/collect_slice5_a.txt, _b.txt).", "Collection identical across two runs.")
rerun("r25-cmd-collect-identical", f"Re-run in round 28: the same two collections as r25-collect-identical ({SD}/logs/collect_slice5_a.txt and _b.txt; byte-identical; 331 tests).", "Collection command re-run; identical outputs.")

# ---------- assemble ----------------------------------------------------------------------------------------------------
missing = [r["id"] for r in rows if r["id"] not in DEC]
extra = [k for k in DEC if k not in by_id]
print("decision keys not in the fragment:", extra)
if missing:
    print("NO DECISION FOR:", missing)
    raise SystemExit(1)
out_rows, decisions = [], []
for i, r in enumerate(rows):
    status, cat, ev, reason, fix = DEC[r["id"]]
    nr = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    if status != "PASS":
        nr["fix"] = fix or "Re-derive this row in a verifier round and cite the script under ledgers/S7/scripts/<slice>-r<round>/."
    out_rows.append(nr)
    decisions.append({"index": i, "id": r["id"], "status": status, "category": cat, "decision_note": reason, "prior_status": r["status"]})
open(f"{CK}/{SD}/row_decisions.json", "w", encoding="utf-8").write(json.dumps(decisions, indent=1, ensure_ascii=False) + "\n")
from collections import Counter
cnt = Counter(r["status"] for r in out_rows)
cats = Counter(d["category"] for d in decisions)
print("rows", len(out_rows), dict(cnt), "categories", dict(cats))

# ---------- write the fragment -----------------------------------------------------------------------------------------
import subprocess
pin = subprocess.run(["git", "-C", CK, "rev-parse", "c9beb92"], capture_output=True, text=True, check=True).stdout.strip()
passed = sum(1 for r in out_rows if r["status"] == "PASS")
failed = sum(1 for r in out_rows if r["status"] == "FAIL")
unv = sum(1 for r in out_rows if r["status"] == "UNVERIFIABLE")
fail_ids = [r["id"] for r in out_rows if r["status"] != "PASS"]
verdict = "PASS" if passed == len(out_rows) else "FAIL"
registry_flags = [
    "Registry: 560 entries at 5e5da87 and at c9beb92; no entry added or removed; content identical except used_by for four entries (hansen1991implications, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone) (registry_entries_C.py). Live verify_refs: whole registry 560 entries, 0 problems; S7 scope 94 of 560, 0 problems (round 28).",
    "Counter-screen populations (OpenCitations) unchanged today: 10.1093/rapstu/raz011 83 rows (32 recent); 10.1111/jofi.13249 408 (297 recent); 10.1214/24-aoas1983 and 10.1016/j.frl.2025.108491 0; 10.1214/aop/1024404523 183 (181 with DOI).",
]
freshness_flags = [
    "Live Federal Reserve zips still differ from MANIFEST raw_sha256 (H.10 now 17d087d0..., MANIFEST 8f370f9c...; H.15 now 0a5685bd..., MANIFEST 334a7f88...); the snapshots rebuild byte-identically from the live zips and from the saved raws (round 28).",
    "Lu (2025) RePEc abstract not re-read in round 28 (not in Crossref); the Jensen-Kelly-Pedersen counter-screen covers the first 70 of 297 recent citing DOIs (round 24 scope, stated).",
    "The freshness search of r21-freshness-search is not repeated (a recorded lead, not a freshness verdict).",
    "Crossref records re-read today (HTTP 200): 10.1093/rfs/hhy131, 10.1093/rfs/hhaa018, 10.1111/jofi.13249, 10.1287/mnsc.2023.03083, 10.1093/rapstu/raz011, 10.1214/aop/1024404523, 10.1214/aop/1015345757, 10.1214/24-aoas1983, 10.1016/j.jfineco.2011.11.003, 10.1016/j.jfineco.2019.08.004, 10.3390/jrfm19010046 (crossref_C.out, crossref2_C.out).",
]
notes = (
    "ROUND 28 (part C of the data-tooling split; verifier checkout /tmp/verify-s7-r2-C at c9beb92). Scope: rows 300-429 of the 430-row fragment, "
    "the round-26 rows R26-* and the round-27 row R27-*. Every row's evidence string was read in full before its decision "
    "(in batches; the 130 decisions are in ledgers/S7/scripts/data-tooling-r28-C/row_decisions.json). Counts: "
    f"{len(out_rows)} rows; carried on byte-identity since 47bac8d (carry, cited by name): {sum(1 for d in decisions if d['category']=='carry')}; "
    f"covered by an accepted lesson-ledger row (cite): {sum(1 for d in decisions if d['category']=='cite')}; "
    f"re-derived or re-viewed by this verifier's own scripts (rederive): {sum(1 for d in decisions if d['category']=='rederive')}; "
    f"re-run at the pin (rerun): {sum(1 for d in decisions if d['category']=='rerun')}; FAIL: {failed}. "
    "Full gate re-runs at c9beb92 (gates.sh, gates2.sh logs): ruff check and format, mypy --no-incremental, pytest 437 passed, run_labs --all, check_pages/dag/projects --all, verify_refs --offline and live (S7 94/560 and whole 560), build_site --check, fetch_data --check, fetch_vendor --check, render_curriculum diff, run_graders --all, mutate_graders --all (164/164 and 69/69), page_smoke --unit S7 and --all, collect-only twice, slice tests 391 passed, playwright dry-run. "
    "Live: fetch_data --fetch and --raw-dir in scratch (CSVs identical); four Federal Reserve pages (HTTP 200); Crossref and OpenCitations re-reads (HTTP 200). "
    "Not re-created this round: the 66 add_reference mutants, the 10 build_site mutants and the three fetch_vendor mutants (carried under the mutant rule; their targets and killers are byte-identical since 47bac8d and the killers pass). "
    "Verified fixes: R27-stale-spec-pointer is PASS (tokens.css line 6 names tools/vendor_spec.yaml; retired names absent). "
    "Corrections: r24-L03-e1-tail-derivation's paragraph is the Lab 4 interpretation on line 584 (labelled E1 in the release row); R26-killer-ids and R26-mutants-152-rerun now refer to ledgers/S7/data-tooling-A.json; "
    "the ellipsis count in L01-L08 is 26 (not 30). "
    "Observations (not row failures): the sentence on L03 line 584 'about 121 + 2,524 = 2,645' sums displayed integers (the unrounded sum is 2,645.9); "
    "at 360 px the sticky site header overlaps the top of the cscv-explorer controls in element captures (screenshot artifact, not verified as a site defect); "
    "the twin-level PBO docstring of test_l08_lab3 holds only under the twin's Sharpe ranking (mean-return ranking gives different logits)."
)
ledger = {
    "unit": "S7",
    "slice": "data-tooling-C",
    "round": 28,
    "verifier": "round 28, independent verifier of the S7 data-tooling slice, part C (rows 300-429; R26-* and R27-* rows). Not the builder, not the round-26 or round-27 verifier.",
    "pin": pin,
    "base": "47bac8d (rows re-run in round 27) and 5e5da87 (release)",
    "previous_ledger": "ledgers/S7/data-tooling-C.json as of c9beb92 (round 27 part C, 100 PASS, 29 UNVERIFIABLE, 1 FAIL)",
    "checkout": "/tmp/verify-s7-r2-C",
    "scratch": "/tmp/ap1-r5/dt-C-r28",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "rows": out_rows,
    "mutants": [],
    "summary": {"rows": len(out_rows), "pass": passed, "fail": failed, "unverifiable": unv, "mutants": 0, "fail_ids": fail_ids},
}
with open(f"{CK}/ledgers/S7/data-tooling-C.json", "w", encoding="utf-8") as fh:
    json.dump(ledger, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("fragment written:", verdict, ledger["summary"])
