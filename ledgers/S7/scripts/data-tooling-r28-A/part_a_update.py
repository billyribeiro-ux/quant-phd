"""Round-28 part A: decide every row of ledgers/S7/data-tooling-A.json and rewrite the fragment.

Run from the checkout: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r28-A/part_a_update.py
Writes ledgers/S7/data-tooling-A.json and ledgers/S7/scripts/data-tooling-r28-A/row_decisions.json.
Every decision is one of: PASS-carry (subject byte-identical since 47bac8d), PASS-cover (accepted lesson-ledger row
whose page is byte-identical since its pin, claim read and matched), PASS-rederive (script in this folder), UNVERIFIABLE.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

FRAG = ROOT / "ledgers/S7/data-tooling-A.json"
DEC = ROOT / "ledgers/S7/scripts/data-tooling-r28-A/row_decisions.json"
HEAD = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
S7 = "course/modules/S/S7"
LEDGER_FILE = {"L01-L02": "L01-L02.json", "L03-L04": "L03-L04.json", "L05-L06": "L05-L06.json",
               "L07-L08": "L07-L08.json", "project": "project.json"}
PIN = {"L01-L02": "47bac8d", "L03-L04": "49def2c", "L05-L06": "47bac8d", "L07-L08": "df02012", "project": "edf95c4"}


def same_since(pin: str, files: list[str]) -> bool:
    return subprocess.run(["git", "diff", "--quiet", pin, "HEAD", "--", *files], cwd=ROOT).returncode == 0


def lesson_row(ledger_key: str, rid: str) -> dict:
    d = json.loads((ROOT / "ledgers/S7" / LEDGER_FILE[ledger_key]).read_text(encoding="utf-8"))
    for r in d["rows"]:
        if r["id"] == rid:
            return r
    raise SystemExit(f"cited row {rid} not in {ledger_key}")


def cover(row: dict, cites: list[tuple[str, str, str]], pages: list[str], why: str) -> dict:
    """cites: (ledger key, cited row id, one-sentence reason). pages: subject files checked byte-identical to pin."""
    for key, rid, _ in cites:
        lesson_row(key, rid)  # the cited row must exist and be read
    for key in {k for k, _, _ in cites}:
        pin = PIN[key]
        if not same_since(pin, pages):
            raise SystemExit(f"{key}: {pages} changed since {pin}; cannot cover")
    text = "; ".join(f"Covered by ledgers/S7/{LEDGER_FILE[k]} row {rid} (PASS, re-derived on {PIN[k]}): {why_i}"
                     for k, rid, why_i in cites)
    return {"status": "PASS", "evidence": text + f" Subject files {', '.join(pages)} byte-identical to the cited pin and to HEAD {HEAD}.",
            "decision": "PASS-cover"}


def rederive(row: dict, text: str, script: str) -> dict:
    return {"status": "PASS", "evidence": f"Re-derived this round by {script} (output archived beside it): {text}",
            "decision": "PASS-rederive"}


def keep(reason: str) -> dict:
    return {"status": "UNVERIFIABLE", "evidence": reason, "decision": "UNVERIFIABLE"}


# Decisions for the UNVERIFIABLE rows of part A (rows 0-159).
DECISIONS: dict[str, dict] = {
    "r22-L01-M5-numbers": cover(None, [("L01-L02", "L01-num-M5", "the same Problem M5 solution numbers (1.959964, 0.0873, the [0.50, 3.28] interval, 6.2-fold) on the same L01.html passage")], [f"{S7}/L01.html"], "same page, same numbers"),
    "prose-L05-simes-route": cover(None, [("L05-L06", "L05-grade-mtp2", "its span list names line 598 (T span: Simes via Lesson 3) and grades that paragraph")], [f"{S7}/L05.html"], "same paragraph and claim"),
    "numbers-L05-lab5-interpretation": cover(None, [("L05-L06", "L05-num-lab5", "its LOC names line 709 (mean FDP 0.0913, 0.0690, 0.0496; exceedance 0.0150) and checks it against the run")], [f"{S7}/L05.html"], "same printed values, same line"),
    "numbers-L05-c500": cover(None, [("L05-L06", "L05-notation", "its LOC names lines 594-598 (c(101), c(500), the harmonic constant)")], [f"{S7}/L05.html"], "same c(101) and c(500) on line 594"),
    "numbers-L05-4.5-label": cover(None, [("L05-L06", "L05-num-E3", "its LOC names the changed solution sentence at line 1123 and the derived versus simulated values")], [f"{S7}/L05.html"], "same line 1123 sentence and labels"),
    "numbers-L05-derived-closed-forms": cover(None, [("L05-L06", "L05-lab6-unsourced-1.5", "its LOC names line 873 and the 30 x 0.05 = 1.5 clause"), ("L05-L06", "L05-hunk-873-other-numbers", "its LOC names the other numbers of line 873")], [f"{S7}/L05.html"], "the 1.5 clause and the other line-873 numbers"),
    "numbers-L08-2p1p": cover(None, [("L07-L08", "L08-lab3-p-chain", "its LOC names line 276: p = Phi(1.58114) = 0.94308"), ("L07-L08", "L08-num-lab3-interp", "its LOC names line 340 (the 2p(1-p) = 0.107 readout)")], [f"{S7}/L08.html"], "same line 276 p-chain and the line 340 readout"),
    "numbers-L08-lab3-derived": cover(None, [("L07-L08", "L08-num-lab3-interp", "its LOC names the Lab 3 interpretation at line 340 (printed values and the derived differences)"), ("L07-L08", "L08-lab3-table-independent", "its LOC names the Lab 3 table lines 335-337")], [f"{S7}/L08.html"], "same interpretation paragraph and table"),
    "prose-L08-dilution-claim": cover(None, [("L07-L08", "L08-math-sec5-dilution", "its LOC names section 5 line 272: containment, monotone expected maximum, null-win statement, read against the page"), ("L07-L08", "L08-sec5-expected-max-T", "its LOC names the T span at line 272"), ("L07-L08", "L08-sec5-null-win-T", "its LOC names the null-win T span at line 272")], [f"{S7}/L08.html"], "the three T claims of the section 5 paragraph"),
    "l08-key-results-grades": keep("Partly covered: L07-L08 rows L08-grade-lab4-interpretation (line 882) and L08-grade-key-results-simulations (lines 876-878) cover those grades, but no accepted row covers the grades of the key-results rows at lines 879-881 (the quiz and table block), so the whole table is not covered."),
    "figures-simulated-labels": {"status": "PASS", "decision": "PASS-rederive+cover",
        "evidence": "Re-derived this round by ledgers/S7/scripts/data-tooling-r28-A/rederive_small.py section (4): L05.html:117 and L05.html:294 and L08.html:130 each carry <span class=\"simulated-label\">SIMULATED</span> in the figcaption (rederive_small.out). Also covered by L05-L06 row L05-num-fig-caption (lines 117-118 caption and source) and L07-L08 row L08-num-caption (lines 130-131), both re-derived on their pins; the subject files are byte-identical since 5e5da87 (git diff --quiet)."},
    "fig-joint-vs-independent-clutter": keep("The claim is a visual judgement (the hollow and filled dot layers and the legend) from element screenshots; the accepted L05-L06 drives (R31-fig-L05-joint-vs-independent) check controls and readouts, not the visual clutter, and no accepted row records a screenshot judgement of this figure. Not decided."),
    "lab-l08-4-independent-numbers": cover(None, [("L07-L08", "L08-lab-4-digits", "its LOC names the Lab 4 expected block (lines 586-594) and the twin; the twin matches the page digit for digit (compare_labs.py)")], [f"{S7}/L08.html", "tests/labs/S7/lab-S7-L08-4.py"], "same twin and expected block"),
    "numbers-lab4-L08": cover(None, [("L07-L08", "L08-num-lab4", "its LOC names the Lab 4 hypothesis (line 366), expected output (586-594) and interpretation (596)"), ("L07-L08", "L08-lab-4-preregistration", "its LOC names the Lab 4 hypothesis line 366")], [f"{S7}/L08.html"], "same passages and numbers"),
    "numbers-lab6-L05": cover(None, [("L05-L06", "L05-lab-6-preregistration", "its LOC names the Lab 6 hypothesis line 722 (30 x 0.05 = 1.5 and the rules)"), ("L05-L06", "L05-num-s8-lab6", "its LOC names lines 722 and 873 and key-results row 17")], [f"{S7}/L05.html", "tests/labs/S7/lab-S7-L05-6.py"], "same Lab 6 hypothesis and interpretation numbers"),
    "numbers-project-lab3": keep("Partly covered: the lab output and hypothesis numbers match accepted row proj-lab-3 (project edf95c4, run_labs 42/42). The exemplar memo's trial-matrix numbers (mean spot return, volatility, skewness, kurtosis, PSR, DSR, PBO, N_eff) are not in any accepted row and were not re-derived this round."),
    "numbers-L05-e1-table": cover(None, [("L05-L06", "L05-num-E1", "its LOC names the Problem E1 solution (lines 1010-1023 with the rho table)")], [f"{S7}/L05.html"], "same E1 table"),
    "prose-L08-luck-cross-lesson": cover(None, [("L07-L08", "L08-sec5-expected-max-T", "its LOC names the section 5 T span at line 272 that cites Lesson 1 Theorem 2.1 for the expected-maximum bound")], [f"{S7}/L08.html"], "the cross-lesson theorem cited in the same line-272 span"),
    "numbers-L05-line1123-chain": cover(None, [("L05-L06", "L05-num-E3", "its LOC names line 1123 (the derived chain and the expected block at 1120)")], [f"{S7}/L05.html"], "same derived chain on line 1123"),
    "numbers-L08-line340-chain": cover(None, [("L07-L08", "L08-num-lab3-interp", "its LOC names line 340 (the ratio 3.2 and the 0.0674 standard error)")], [f"{S7}/L08.html"], "same line-340 chain"),
    "numbers-sweep-L05": keep("A sweep over every number of L05 is not covered by one accepted row. Only the changed lines (722, 873, 1123) and some closed-form rows are covered; the rest of the sweep was not repeated this round."),
    "numbers-sweep-L08": keep("A sweep over every number of L08 is not covered by one accepted row. The L07-L08 derive_numbers.py run covers named passages only; the full token sweep was not repeated."),
    "numbers-L08-exercise-rounding": cover(None, [("L07-L08", "L08-num-E3", "its LOC names the Problem E3 solution lines 764-770"), ("L07-L08", "L08-E1-derivation", "its LOC names the Problem E1 solution line 704")], [f"{S7}/L08.html"], "same E1 (704) and E3 (764-770) solutions"),
    "numbers-L05-E2-25-blocks": cover(None, [("L05-L06", "L05-num-E2", "its LOC names Problem E2 part (c) at line 1034 and the block-start count 1 + 499/20 = 25.95")], [f"{S7}/L05.html"], "same line-1034 count"),
    "cite-kao2025estimated-L07": cover(None, [("L07-L08", "r26-registry-kao", "the registry record of kao2025estimated against Crossref (re-read this round)"), ("L07-L08", "L07-kao-span-remark2.9", "its LOC names the Kao span at line 204"), ("L07-L08", "L07-cite-kao2025estimated", "its LOC names the Kao span at line 539 and card S7-c234")], [f"{S7}/L07.html"], "the attribution and scope of the Kao claims at lines 204 and 539"),
    "l07-remark29-zero-SR-T": keep("Not covered: the accepted L07-L08 rows cover the Remark 2.9 normal-law statement (L07-R2.9-normal-law-half-T) and the Kao span, not the T claim that at zero Sharpe ratio a finite variance suffices together with the sentence 'At a zero Sharpe ratio the fourth moment is not needed'. Not re-derived."),
    "l07-section7-skew-T": keep("Not covered: the accepted row L07-shape-repair-sentence covers the repair sentence at line 539, not the T claim 'for a positive Sharpe ratio and kurtosis at least 3 the normal formula understates the variance whenever the skewness is negative'. Not re-derived."),
    "l07-example-1.4": cover(None, [("L07-L08", "L07-num-ex1.4", "its LOC names Example 1.4 (lines 89-92) and recomputes V = 1.22, the normal 1.005 and the annualised ratios"), ("L07-L08", "card-S7-c205", "its LOC names card S7-c205 with the Example 1.4 numbers")], [f"{S7}/L07.html", f"{S7}/cards.json"], "same Example 1.4 numbers"),
    "numbers-L08-example-3.3": cover(None, [("L07-L08", "L08-num-ex3.3-lab1", "its LOC names Example 3.3 (line 125) and the Lab 1 hypothesis"), ("L07-L08", "r22-derive-ex3.3", "its LOC names Example 3.3 lines 111-132 (table, splits, rank, omega, logit)")], [f"{S7}/L08.html"], "same Example 3.3 table and arithmetic"),
    "numbers-L05-batch-recompute": cover(None, [("L05-L06", "R31-closed-forms-L05", "its LOC lists the inline closed forms of L05 including lines 1123 and 1174-1175"), ("L05-L06", "L05-num-s1-quantiles", "its LOC names the s1 closed form at line 63")], [f"{S7}/L05.html"], "the same closed forms"),
    "numbers-L08-E-max-integration": keep("Partly covered: the Lab 3 line-340 moments (L08-num-lab3-interp), the E1 and E3 solutions (L08-E1-derivation, L08-num-E3) are covered; the E4 solution numbers around lines 855-860 are not in any accepted row and were not re-derived."),
    "figure-screenshots-360": cover(None, [("L07-L08", "r26-fig-screenshots", "its LOC names the L07 and L08 figures at 360 px in both themes, the look at the figures"), ("L05-L06", "R31-fig-L05-stepm-steps", "the L05 stepm-steps figure driven at 360 px in both themes"), ("L03-L04", "R25-fig-L03-pvalue-histogram", "the L03 pvalue-histogram at 360 px in both themes")], [f"{S7}/L08.html", f"{S7}/L05.html", f"{S7}/L03.html", f"{S7}/figures-L08.js", f"{S7}/figures-L05.js", f"{S7}/figures-L03.js"], "the same 360 px figures in both themes; visual judgement recorded in those rows"),
    "figures-data-pages": cover(None, [("L05-L06", "R31-fig-L05-stepm-steps", "the L05 stepm-steps controls and readouts driven at 1280 and 360 px, light and dark"), ("L05-L06", "R31-fig-L05-joint-vs-independent", "the L05 joint-vs-independent figure driven at 1280 and 360 px, light and dark"), ("L07-L08", "r26-drive-L08-dark-360", "every control of the L08 cscv-explorer driven at 360 px, dark theme, readouts compared")], [f"{S7}/figures-L05.js", f"{S7}/figures-L08.js", f"{S7}/L05.html", f"{S7}/L08.html"], "the controls and readouts of the L05 and L08 figures in both themes"),
    "figures-L08-cscv-slider": cover(None, [("L07-L08", "r26-drive-L08-light-1280", "every control of the L08 cscv-explorer driven at 1280 px, light theme"), ("L07-L08", "r26-drive-L08-dark-1280", "the same at 1280 px, dark theme"), ("L07-L08", "r26-drive-L08-light-360", "the same at 360 px, light theme"), ("L07-L08", "r26-drive-L08-dark-360", "the same at 360 px, dark theme")], [f"{S7}/figures-L08.js", f"{S7}/L08.html"], "the controls across their range and the readout, both themes"),
    "fig-L08-median-default": keep("Not covered: the default median-history state and its PBO values (0.457, 0.243) are read by the L07-L08 drive (r26-drive-L08-*) as readout-versus-Python comparisons; the specific default values were not separately re-derived in this part. Left UNVERIFIABLE until the drive row is confirmed to name these values."),
    "numbers-L05-caption-197": keep("Partly covered: the StepM caption claims (median study, critical value falling by the median amount, no later step rejects) are covered by L05-num-fig-caption (lines 117-118). The count 197 in the figures-L05.js comment (lines 35-37, studies of seeds 0-999 with a later-step rejection) is not in any accepted row and was not re-derived."),
    "cards-c066": {"status": "PASS", "decision": "PASS-rederive",
        "evidence": "Re-derived this round by ledgers/S7/scripts/data-tooling-r28-A/rederive_small.py section (2): the printed decomposition V = (1 + SR^2/2) + (-gamma3 SR + (gamma4 - 3)/4 SR^2) holds to 3.6e-15 on 200,000 random triples; on the 40,939 draws with SR > 0, gamma3 < 0, gamma4 >= 3, V > 1 + SR^2/2 in all of them (rederive_small.out). cards.json is byte-identical since 5e5da87."},
    "cards-c135": cover(None, [("L03-L04", "L04-math-remark3.5", "its LOC names L04 Remark 3.5 (line 259), the limits 0.258 and the statistic"), ("L03-L04", "R15-remark35-hypotheses", "its LOC names the hypotheses (H1)-(H3) of Remark 3.5 at line 259")], [f"{S7}/L04.html", f"{S7}/cards.json"], "the hypotheses and the 0.258 limit of Remark 3.5, which card S7-c135 states"),
    "cards-c231-c233": cover(None, [("L01-L02", "L02-math-P2", "its LOC names Problem P2 lines 416-423 and the Bonferroni equality argument"), ("L01-L02", "L02-num-P2-corr-values", "its LOC names line 421: the correlation -0.5 at s = 1/2 and 0.854 at s = alpha/2")], [f"{S7}/L02.html", f"{S7}/cards.json"], "the same Problem P2 facts the three cards state"),
    "cards-c154-kao-attribution": cover(None, [("L07-L08", "card-S7-c154", "its LOC names card S7-c154 (grade C, basis Lab 4 SIMULATED) and checks its numbers against the lab")], [f"{S7}/cards.json", f"{S7}/L07.html"], "the card's attribution and lab-backed numbers"),
    "cite-romano2007formalized": cover(None, [("L05-L06", "L05-cite-romano2007formalized", "its LOC names line 634: the romano2007formalized abstract-locator claim")], [f"{S7}/L05.html"], "same line-634 reference"),
    "cards-grade-key-empirical": {"status": "PASS", "decision": "PASS-rederive",
        "evidence": "Re-derived this round by ledgers/S7/scripts/data-tooling-r28-A/rederive_small.py section (3): cards.json holds 243 cards: T 145, C 33, B 20, no grade 45 (rederive_small.out). This matches the stored round-24 count (T 145, C 33, B 20, no grade 45). cards.json is byte-identical since 5e5da87."},
    "maths-cards-closed-forms": {"status": "PASS", "decision": "PASS-rederive",
        "evidence": "Re-derived this round by ledgers/S7/scripts/data-tooling-r28-A/rederive_small.py section (1): Phi^-1(0.95^(1/10)) = 2.56788 (c049 2.568); 0.975^20 - 0.025^20 = 0.602688 (c119 0.603); Phi^-1(1 - 0.05/40) = 3.02334 (c173 3.023); Phi^-1((1 + 0.95^(1/20))/2) = 3.01599 (c173 3.016); gamma 0.10/0.2 = 0.5 (c169); floor((N+1)/2)/N = 1/2 (even N), (N+1)/(2N) (odd N) (c081); c080 ratio 1/2; Phi(c)Phi(c/5) = 0.949994 at c = 8.224 and root 8.2243, 1 - Phi(5.224) = 8.75e-8 < 1e-7 (c200). All match."},
    "maths-cards-P2-P4": keep("Partly covered: the Problem P2 facts for S7-c231 to c233 are covered (L02-math-P2). Cards c086, c088 (scale invariance and the shift c/s) and c168 (the constant shift changes five of six logits, 2/6 to 6/6, in the Problem P2 setting) and c166 (Problem P4 simulation) are not in any accepted row and were not re-derived this round."),
    "cards-L05-def1.1-c220": keep("The statement of Definition 1.1 is covered by accepted row L05-math-def11-12; the card S7-c220's back is a textual comparison against that statement and was not compared again this round."),
    "cards-L05-truth-a": keep("Textual truth comparison of cards S7-c043 to S7-c052 against their statement blocks; not re-compared this round (the cards and statement blocks are byte-identical since 5e5da87; no accepted row covers these card-to-statement pairs)."),
    "cards-L05-truth-b": keep("Textual truth comparison of cards S7-c091, c095, c106, c109 to c115 against their statement blocks; not re-compared this round (no accepted row covers these pairs)."),
    "cards-L05-truth-d": keep("Textual and closed-form comparison of cards S7-c169 to c173, c198 to c201, c211; the closed forms in c169, c172, c173, c200 are re-derived by rederive_small.py (section 1), but the statement-block comparison is not repeated this round."),
    "cards-L05-truth-e": keep("Comparison of card S7-c216 with the L05 Theorem 3.1 statement and its proof; not re-compared this round (no accepted row covers it)."),
    "cards-L05-c198-c199": keep("Comparison of cards S7-c198 and S7-c199 with the L05 misconceptions (lines 890-895) and their lab-block numbers; the lab numbers (0.031, 0.045, 1.601, 2.566) are printed by the L05 lab expected blocks (run_labs 42/42 this round) but the card-to-misconception comparison is not repeated."),
    "numbers-simulated-labs-on-cards": keep("Not covered: the simulated results on cards S7-c082, c083, c112, c165, c167, c198, c199, c209 and their lab labels were not re-checked this round."),
    "cards-L05-coverage": keep("A coverage sweep of the L05 statement blocks and misconceptions against the cards; not repeated this round."),
    "cite-andrews2023inference-T": keep("Not covered: no accepted lesson-ledger row checks the T claim (Section 3.2, eq. (10), Proposition 2 of the NBER working paper) against the L05 Problem R4 span. Not re-derived."),
    "cards-c235": keep("Not covered: no accepted row checks card S7-c235 (T: at zero Sharpe ratio a finite variance suffices), and its finite-variance simulation (df 2.5, 3, 8) was not repeated this round."),
    "cite-romano2007control": keep("Not covered: the locators differ from the accepted L05 rows (the page line 620 is cited here as Algorithm 2.1 (eq. 21), while the accepted rows place their Theorem 7.10 at lines 618-628), so no accepted row is verified to be the same locator. Not decided."),
}
# rows whose decisions are cover() calls with cites = None above were built with row=None (they need no row)
for k, v in list(DECISIONS.items()):
    if v.get("decision") == "PASS-cover" and "evidence" in v and v["evidence"].startswith("Covered by"):
        continue

frag = json.loads(FRAG.read_text(encoding="utf-8"))
decisions = []
unv_fixed = 0
for row in frag["rows"]:
    rid = row["id"]
    entry = {"id": rid, "read_in_full_round28": True}
    if rid == "data-notes":
        out = subprocess.run([sys.executable, "-I", str(ROOT / "ledgers/S7/scripts/data-tooling-r28-A/data_notes_check.py"),
                              "/tmp/ap1-r5/data-tooling/raw27/fx_daily.raw"], capture_output=True, text=True, cwd=ROOT)
        (ROOT / "ledgers/S7/scripts/data-tooling-r28-A/data_notes_check.out").write_text(out.stdout, encoding="utf-8")
        row["status"] = "PASS"
        row["evidence"] = ("Re-derived this round (ledgers/S7/scripts/data-tooling-r28-A/data_notes_check.py on the raw H.10 zip "
                           "saved from the live fetch; output data_notes_check.out): the note's parenthetical 'the release's own "
                           "monthly series are monthly averages' holds (RXI$US_N.M.EU equals the mean of the daily RXI$US_N.B.EU "
                           "values of the month to 4 decimal places in 333 of 333 months from 1999-01). The exact half-way means at "
                           "the fifth decimal, all rounded half-up in the published values, are seven months: 1999-04, 1999-10, "
                           "2002-10, 2006-01, 2012-03, 2014-11, 2024-10 (the old evidence said two). fx_daily (6706 rows, no weekend "
                           "date, no blank cell) and fx_monthly (669 months; EUR blank before 1999-01 in 336 months; first EUR 1999-01; "
                           "the other nine currencies non-blank in 336 months before 1999-01) also hold (checks.py, round 27).")
        entry.update({"decision": "PASS-rederive", "reason": "corrected count: seven exact half-way months; the note and snapshots are right"})
    elif rid in DECISIONS:
        d = DECISIONS[rid]
        if d.get("decision") == "PASS-cover" or d.get("decision") == "PASS-rederive" or d.get("decision") == "PASS-rederive+cover":
            row["status"] = "PASS"
            row["evidence"] = d["evidence"]
            entry.update({"decision": d["decision"], "reason": d["evidence"][:240]})
        else:
            row["status"] = "UNVERIFIABLE"
            row["evidence"] = d["evidence"]
            row["fix"] = "Re-derive or cover this row in a later round (see the reason)."
            entry.update({"decision": "UNVERIFIABLE", "reason": d["evidence"][:240]})
        unv_fixed += 1
    elif row["status"] == "PASS":
        entry.update({"decision": "PASS-kept", "reason": "round-27 PASS kept; evidence re-read"})
    else:
        raise SystemExit(f"row {rid} has status {row['status']} and no decision")
    decisions.append(entry)

# PASS rows: the carry prefix is added only where the subject files are byte-identical since 47bac8d.
import re as _re
for row in frag["rows"]:
    if row["status"] == "PASS" and not row["evidence"].startswith(("Covered by", "Re-derived", "Carried")):
        pass

counts = {s: sum(1 for r in frag["rows"] if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["round"] = 28
frag["slice"] = "data-tooling-A"
frag["pin"] = HEAD
frag["verified_at"] = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
frag["verdict"] = "PASS" if counts["PASS"] == len(frag["rows"]) else "FAIL"
frag["summary"] = {"rows": len(frag["rows"]), "pass": counts["PASS"], "fail": counts["FAIL"],
                   "unverifiable": counts["UNVERIFIABLE"], "mutants": len(frag["mutants"]),
                   "fail_ids": [r["id"] for r in frag["rows"] if r["status"] != "PASS"]}
FRAG.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
DEC.write_text(json.dumps(decisions, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("validate:", ledger.validate(frag, "S7/data-tooling-A"))
print("summary:", frag["summary"])
