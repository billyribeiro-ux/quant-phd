"""Writes ledgers/AC2/L05-L06.json (round 6). Row evidence is written by the verifier; scripts cited in it are in this folder."""
import json
import sys

ROOT = "/tmp/verify-ac2r6-l56"
C5 = "Carried from round 5 ("
CARD_OK = "course/modules/AC/AC2/cards.json records byte-identical since 11b3477 (scripts/L05-L06-r6/cards_compare.py)"
P = "PASS"
F = "FAIL"

rows = []


def add(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        row["fix"] = fix
    rows.append(row)


def carry(rid, check, location, evidence):
    add(rid, check, location, P, C5 + location + " byte-identical since 11b3477; no delta hunk touches it): " + evidence)


# ---- command rows (re-run this round) ----
add("L05-L06-cmd-pin", "2.9-structure", "repository; course/modules/AC/AC2/L05.html, L06.html, cards.json, tests/labs/AC2/lab-AC2-L05-1.py, lab-AC2-L06-1.py", P,
    "git rev-parse --short HEAD = ff9284f (round-6 pin); git status: only untracked .venv. Delta 11b3477..HEAD for the slice (scripts/L05-L06-r6/delta-11b3477-HEAD-L05-L06-cards-labs.diff): L05.html hunks at lines 184, 206, 254, 330-340, 348, 438; L06.html hunks at lines 230, 314-344, 356-364, 404-410, 454-460, 518-522; cards.json AC2-c075 and AC2-c123 (L05), AC2-c107 and AC2-c130 (outside slice); tests/labs/AC2/lab-AC2-L05-1.py (+3 print lines) and lab-AC2-L06-1.py (one print line renamed). Registry and notation.json byte-identical since 11b3477.")
add("L05-L06-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit AC2 --page L05; --page L06", P,
    "'check_pages AC2 L05: PASS' rc 0 and 'check_pages AC2 L06: PASS' rc 0. /tmp/ac2-v/L05-L06-r6/check_pages_L05.txt, check_pages_L06.txt.")
add("L05-L06-cmd-check-dag", "2.9-dag", "tools/check_dag.py --unit AC2", P,
    "'check_dag AC2: PASS' rc 0. /tmp/ac2-v/L05-L06-r6/check_dag.txt.")
add("L05-L06-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit AC2; pytest tests/test_labs.py -k AC2", P,
    "'run_labs AC2: PASS (11/11)' rc 0 (/tmp/ac2-v/L05-L06-r6/run_labs.txt); pytest -k AC2: 11 passed rc 0 (pytest_ac2.txt).")
add("L05-L06-cmd-twins-isolated", "2.5-labs", "tests/labs/AC2/lab-AC2-L05-1.py, tests/labs/AC2/lab-AC2-L06-1.py", P,
    "python -I -W error: L05 rc 0 (19 lines, lab05.out), L06 rc 0 (39 lines, lab06.out). scripts/L05-L06-r6/cmp_pre.py (run with -I): L05 page pre block 19/19 lines IDENTICAL, L06 39/39 IDENTICAL.")
add("L05-L06-cmd-page-smoke", "2.5-labs", "tools/page_smoke.py --unit AC2 --pages L05 L06", P,
    "'page_smoke modules/AC/AC2/L05.html: PASS', 'page_smoke modules/AC/AC2/L06.html: PASS', 'page_smoke AC2: PASS' rc 0 (/tmp/ac2-v/L05-L06-r6/page_smoke.txt).")
add("L05-L06-cmd-verify-refs-unit", "2.1-citations", "tools/verify_refs.py --unit AC2", P,
    "'live re-verification of AC2: 7 of 560 entries, 0 problems' rc 0 (/tmp/ac2-v/L05-L06-r6/verify_refs_live.txt).")
add("L05-L06-cmd-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", P,
    "'offline integrity: 560 entries, 0 problems' rc 0 (verify_refs_offline.txt).")
add("L05-L06-cmd-lint", "2.9-structure", "tests/labs/AC2/lab-AC2-L05-1.py, lab-AC2-L06-1.py", P,
    "ruff check tests/labs/AC2: 'All checks passed!' rc 0; ruff format --check: '11 files already formatted' rc 0; mypy on the two twins: 'Success: no issues found in 2 source files' rc 0; pytest -k AC2: 11 passed (ruff.txt, mypy.txt, pytest_ac2.txt).")

# ---- citations (subjects unchanged; registry byte-identical) ----
carry("L05-L06-cit-sloan-registry", "2.1-citations", "references/references.json key sloan1996stock",
      "registry: Sloan, Richard G., The Accounting Review 71(3), 1996, title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?'; L05 uses the key and its title only.")
carry("L05-L06-cit-sloan-claim-s1", "2.1-citations", "course/modules/AC/AC2/L05.html §1 (claim span after Definition 1.1, grade C, data-cite sloan1996stock)",
      "claim: Sloan (1996) investigates whether stock prices reflect information about future earnings in the accrual and cash-flow components. Matches the registry title and the Crossref abstract (locator not confirmed, grade C).")
carry("L05-L06-cit-sloan-claim-s3", "2.1-citations", "course/modules/AC/AC2/L05.html §3 (two claim spans, grade C) and §7 key-results",
      "the question Sloan (1996) asks is the price question; §3 text unchanged since 11b3477; the hub card (index.html L05 card body, changed this round) now reads 'the question Sloan (1996) asks', consistent with §3.")
carry("L05-L06-cit-dechow-registry", "2.1-citations", "references/references.json key dechow1995detecting",
      "registry: title 'Detecting Earnings Management.', The Accounting Review vol 70 issue 2, 1995, pages 193-225 (DOI 10.2308/tar-9505096112); the lesson string 'The Accounting Review 70(2), 1995' matches. Author list is the open question of ruling 1.")
carry("L05-L06-cit-dechow-scope", "2.1-citations", "course/modules/AC/AC2/L06.html line 61 claim span, §5 bullet 1 claim span, §8 key-results row 6",
      "claim span: 'evaluates alternative accrual-based models ... compares the specification and power of commonly used test statistics'; Crossref abstract (api.crossref.org, round 5 and this round's verify_refs live run) matches; no power figure quoted.")
add("L05-L06-r6-L06-s1-source-wording", "2.1-citations", "course/modules/AC/AC2/L06.html line 61 (§1 paragraph, sentence 'The A15 contract fits the model defined in Section 2. Its source is registry key dechow1995detecting')", F,
    "atlas/A15.contract.md line 123 cites the model to the 'accrual-model literature; see dechow1995detecting, Detecting Earnings Management'. The page's 'Its source is' states a stronger attribution than the contract's 'see' pointer, and the contract does not name the paper as the model's source.",
    "Replace 'Its source is registry key dechow1995detecting' with 'The contract cites the model to the accrual-model literature, see registry key dechow1995detecting' (or equivalent wording that keeps the contract's 'see').")
carry("L05-L06-cit-dechow-motivation", "2.1-citations", "course/modules/AC/AC2/L06.html §2 claim spans ('Jones's regression uses the change in revenue...')",
      "§2 paragraph unchanged; the rationale for the receivables term is stated as not sourced in the lesson.")
carry("L05-L06-cit-dechow-grouping", "2.1-citations", "course/modules/AC/AC2/L06.html §5 bullet 4 (claim span, grade C, data-cite dechow1995detecting)",
      "bullet 4 unchanged; the lesson makes no quantitative claim about grouping.")
add("L05-L06-cit-dechow-authors", "2.1-citations", "references/references.json dechow1995detecting (notes.authors); course/modules/AC/AC2/index.html L06 card; L05.html, L06.html, cards.json", P,
    "grep -c 'Dechow' (case-sensitive) = 0 in L05.html, L06.html and cards.json and in the L05/L06 hub cards; learner text names the key and the title only (ruling 1). The registry lists Dechow and Sloan (notes.authors) and the curriculum string differs; not resolved here.")
carry("L05-L06-cit-mclean", "2.1-citations", "course/modules/AC/AC2/L05.html §4 bullet 1 (claim span, grade C, data-cite mclean2016academic)",
      "title 'Does Academic Research Destroy Stock Return Predictability?' matches registry (The Journal of Finance 71(1), 2016, DOI 10.1111/jofi.12365); no finding stated.")
carry("L05-L06-cit-hou", "2.1-citations", "course/modules/AC/AC2/L05.html §4 bullet 2 (claim span, grade C, data-cite hou2018replicating)",
      "title 'Replicating Anomalies' matches registry (Review of Financial Studies 33(5), DOI 10.1093/rfs/hhy131); no finding stated.")
add("L05-L06-reg-used-by", "2.1-citations", "references/references.json entries mclean2016academic (used_by F4, S7) and hou2018replicating (used_by F5, S7)", P,
    "registry byte-identical since 11b3477; both keys list AC2 in used_by.")

# ---- numbers ----
add("L05-L06-num-L05-lab", "2.2-numbers", "course/modules/AC/AC2/L05.html lab-AC2-L05-1 expected output, interpretation, key-results, misconception 2", P,
    "Lab 1 run this round (run_labs and lab05.out, 19 lines): mean_z_gap_simulated -2.7937; planted_monthly_spread 0.00223; planted_spread_8dp 0.00223495; spread_sd_theory 0.01131; spread_sd_theory_7dp 0.0113137; se_mean_120_7dp 0.0010328; expected_t_at_planted 2.164; recovered 0.00219; null_false_positive_rate 0.060; effect_rejection_rate_power 0.590; effect_median_t 2.155; seed0_spread_mean 0.00075 seed0_t 0.676; seed0_distance_in_se -1.433. The page block is identical (cmp_pre.py). Interpretation numbers (0.6 SE, 41%, 0.00219 vs 0.00223) recomputed from these outputs.")
add("L05-L06-num-L05-derived", "2.2-numbers", "course/modules/AC/AC2/L05.html Prop 2.3, §2 text, §4 Lab text, M2, M3, E1, E2, E3, R1, misconception 2; cards AC2-c075, c123", P,
    "scripts/L05-L06-r6/recompute_r6.py: sd_exact 0.0113137085 (7dp 0.0113137, 5dp 0.01131); se 0.0010328; planted from displayed gap 0.0008 x 2.7937 = 0.00223496 (8dp lab 0.00223495); E2 0.0022350/(0.01131/sqrt120) = 2.16474 -> 2.1647; 0.00223495/(0.0113137/sqrt120) = 2.16398 -> 2.164; c123 0.00223495/(0.01131/sqrt120) = 2.16469 -> 2.1647; E3 (0.00075-0.00223)/0.0010328 = -1.4330 -> -1.433; with SE 0.00103 = -1.4369 -> -1.44; R1 sqrtT = 14.18, T = 201.1 -> 201; E1 sqrt(0.05*0.95/200)=0.01541, 0.010/0.01541=0.65; M2 c=0.01645, Phi(3.355)=0.9996 (checked); M3 0.0020/(0.0100/sqrt120)=2.191; E2 sweep distances from -2.7996: 0.0559, 0.0268, 0.0084, 0.0005; -2.7937 vs -2.7912 differ by 0.0025. All match the page.")
add("L05-L06-num-L06-lab", "2.2-numbers", "course/modules/AC/AC2/L06.html lab-AC2-L06-1 expected output, interpretation, misconceptions, key-results", P,
    "Lab 1 run this round (lab06.out, 39 lines): a1_all_minus_nm 0.2084 (strong), 0.0944 (weak); decomposition 0.1425 + 0.1965 - 0.1306 with residual -0.000000 (strong) and 0.000000 (weak); a1_conditional_mean_prediction 0.6223 and 0.1245; a2_nm_6dp 0.103076, se2_6dp 0.001467, z_a2_fp 2.096, two_sided_tail_a2_fp 0.036; flags_only 6/6, flags_differing 12; rates 0.9850/0.0017 and 0.3550/0.0717; se_mean 0.2781 and 0.0489. Page block identical (cmp_pre.py). The printed difference 0.2084 is the lab's own line (a1_all_minus_nm), not a page-side calculation.")
add("L05-L06-num-L06-derived", "2.2-numbers", "course/modules/AC/AC2/L06.html Remark 3.2, §4, M1, M2, M3, E1, E2, E3, R1; cards AC2-c083, c084, c085, c086, c125", P,
    "recompute_r6.py and in-line checks: M1 NDA -0.02295, DA -0.00705; M2 c 0.01645, detection 0.9996; M3 0.2084/0.2824 = 0.738 (0.2085 from printed values); E1 71/200 = 0.355, 0.0717 x 1800 = 129, 129/200 = 0.645; E2 197/200 = 0.985, 0.0017 x 1800 = 3.06; R1 0.2781 sqrt(1800/57600) = 0.0492, 1800 (0.2781/0.05)^2 = 55,690 -> 55,700, /0.9 = 61,900; 0.2824/0.05 = 5.6; Remark 3.2 b = 1.2, residuals (-0.2, 0.4). Card c083 0.738 correct; c125 0.2781 and 0.0489 printed by se_scaling.")
add("L05-L06-num-L06-roughly-4pct", "2.2-numbers", "course/modules/AC/AC2/L06.html E3 solution (tail sentences)", P,
    "E3 solution this round: z 2.097 (six-decimal inputs, recomputed 2.0968), lab z_a2_fp 2.096, tail 0.036 (lab), rounded-both 2.067 -> tail 0.0388 (0.039), rounded-SE-only 2.051 -> tail 0.0403 (0.040), rounded-difference-only 2.113 -> tail 0.0346 (0.035); all printed in recompute_r6.py.")

# ---- maths (subjects unchanged) ----
carry("L05-L06-math-L05-def-t", "2.4-math", "course/modules/AC/AC2/L05.html Definition 1.2 (t = S-bar / (s_S / sqrt T))", "definition text matches the lab's t_stat (mean over sd with ddof=1 over sqrt n).")
carry("L05-L06-math-L05-prop21", "2.4-math", "course/modules/AC/AC2/L05.html Proposition 2.1 and proof", "proof steps re-read; constant cancels, noise averages to zero given the sort.")
carry("L05-L06-math-L05-prop23", "2.4-math", "course/modules/AC/AC2/L05.html Proposition 2.3 and proof; P2", "phi(q) with q = Phi^-1(0.2) = -0.8416: recomputed phi(q) = 0.27996, gap -2 phi/0.2 = -2.7996 (approx -2.800); 1.4 per side.")
carry("L05-L06-math-L05-remark22-P1-P3", "2.4-math", "course/modules/AC/AC2/L05.html Remark 2.2, P1, P3", "statements re-read; P1 monotone invariance and P3 zero mean as proved.")
carry("L05-L06-math-L06-prop31", "2.4-math", "course/modules/AC/AC2/L06.html Proposition 3.1 (statement) and proof", "X'e = 0 and the ones-vector criterion; Remark 3.2 numbers recomputed (b = 1.2, residual sum 0.2).")
carry("L05-L06-math-L06-prop33-formula", "2.4-math", "course/modules/AC/AC2/L06.html Proposition 3.3 (formula for the mean error)", "E[b-hat|X] - b* = (X'X)^-1 X'd; proof re-derived.")
carry("L05-L06-math-L06-prop33-statement", "2.4-math", "course/modules/AC/AC2/L06.html Proposition 3.3 statement and proof; key-results row 2; card c079", "statement and proof re-derived; the conditional-mean reading is as stated.")
carry("L05-L06-math-L06-P3", "2.4-math", "course/modules/AC/AC2/L06.html P3 solution", "P3 solution re-derived; unchanged.")
carry("L05-L06-math-L06-remark32-P1-P2", "2.4-math", "course/modules/AC/AC2/L06.html Remark 3.2, P1, P2", "P2 scale invariance re-derived (1/(kA) rescales a1 by k; residuals unchanged).")
add("L05-L06-math-notation", "2.4-math", "notation/notation.json (macros and 8 symbols) against both pages", P,
    "notation.json byte-identical since 11b3477; the new sentences use \\E, \\mid, \\Phi, \\sqrt macros already defined there (\\E present, notation.json line match).")

# ---- labs ----
add("L05-L06-lab-L05-1-run", "2.5-labs", "course/modules/AC/AC2/L05.html Lab 1 (code twin tests/labs/AC2/lab-AC2-L05-1.py and expected block)", P,
    "twin run under python -I -W error rc 0; page code block and expected block match (cmp_pre.py 19/19). Lab is SIMULATED and labelled; runtime under page_smoke.")
add("L05-L06-lab-L05-1-interp", "2.5-labs", "course/modules/AC/AC2/L05.html Lab 1 interpretation and Misconceptions 1-3", P,
    "interpretation (0.00219 vs 0.00223; 0.060; 2.155 vs 2.164; power 0.590 'about 41%'; seed 0 t 0.676) matches the printed output. Misconception 2 now says 'computed at full precision; lab output seed0_distance_in_se -1.433', which matches lab line 200 ((effect_means[0] - planted_exact)/(sd_theory/sqrt120)).")
add("L05-L06-lab-L06-1-run", "2.5-labs", "course/modules/AC/AC2/L06.html Lab 1 (twin tests/labs/AC2/lab-AC2-L06-1.py)", P,
    "twin run under python -I -W error rc 0; the renamed print lines (a2_nm_6dp, se2_6dp, z_a2_fp, two_sided_tail_a2_fp) are in the page block (cmp_pre.py 39/39). The z is recomputed from the printed six-decimal values and matches within the rounding stated on the page.")
carry("L05-L06-lab-L06-1-overreach-sample", "2.5-labs", "course/modules/AC/AC2/L06.html §4 paragraph (the third choice, the scale of the regressors)",
      "the paragraph is outside every delta hunk; its numbers (0.1806, 0.2824, 5.6, 0.0489) recomputed in this round's rows.")
add("L05-L06-lab-L06-1-single-seed", "2.5-labs", "course/modules/AC/AC2/L06.html Lab 1 interpretation; §8 key-results rows 4-5 (basis 'Lab 1 (simulation, SIMULATED, seed 606)')", P,
    "interpretation states 'every flag score below is one simulated draw at seed 606, not an average over seeds' and 'two shifts at one seed describe that draw and establish no threshold'; key results carry grade C with the lab named; consistent with the lab header and output.")
carry("L05-L06-lab-L06-1-threshold-claim", "2.5-labs", "course/modules/AC/AC2/L06.html Misconception 3 ('identifies the manipulators only when the ...')",
      "Misconception 3 unchanged; its numbers 71/200 and 197/200 are the printed rates at seed 606.")
add("L05-L06-lab-L06-1-flag-count", "2.5-labs", "course/modules/AC/AC2/L06.html Lab 1 interpretation ('12 of the 200 flags differ' / 'so 12')", P,
    "lab prints flags_only_all_firms 6, flags_only_oracle 6, flags_differing_all_vs_oracle 12 (weak); strong 0/0/0. The interpretation's 12 firm-years change status is the printed flags_differing value.")

# ---- cards ----
carry("L05-L06-card-L05-defs", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c063, c065, c066, c067, c068", "records read this round; " + CARD_OK + ".")
add("L05-L06-card-L05-lab", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c069, c070, c071, c072, c073, c074, c075, c122, c123", F,
    "c069-c074 and c122 re-read, unchanged, consistent with the Lab 1 output. c123 is now correct (back text 2.164 from 0.00223495 and SD 0.0113137, displayed-SD quotient 2.1647: recomputed 2.16469). c075 is changed in this round's delta: its back text is right (0.00223495, 0.0113137, T about 201, recomputed 201.1), but its basis still reads \"Derivation from Lab 1's planted spread (0.0022350)\". Lab 1 prints planted_monthly_spread 0.00223 and planted_spread_8dp 0.00223495 (lab05.out); 0.0022350 is not printed by the lab. The basis cites a lab value the lab does not print.",
    "In cards.json AC2-c075 change the basis to \"Derivation from Lab 1's planted spread (0.00223495, printed as planted_spread_8dp) and the monthly standard deviation (Research problem R1)\". Then re-run tools/render or the card build if the cards are generated.")
carry("L05-L06-card-L05-sloan", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c064", "front and back re-read; the back matches §3 and the lesson's 'states no finding' sentence; basis = Crossref abstract, locator not confirmed.")
carry("L05-L06-card-L06-defs", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c076, c077, c080, c081, c088", "records re-read; " + CARD_OK + ".")
carry("L05-L06-card-L06-lab", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c082, c083, c085, c086, c125", "records re-read; " + CARD_OK + "; numbers recomputed (0.738, 197/200, 71/200, 0.2781, 0.0489).")
carry("L05-L06-card-L06-iff", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c078", "X'e = 0 and iff criterion match Proposition 3.1.")
carry("L05-L06-card-L06-projection", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c079", "matches Proposition 3.3.")
carry("L05-L06-card-L06-only-when", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c084", "matches the lab's precision 0.355 and §6 Misconception 3.")
carry("L05-L06-card-L06-dechow", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c087", "states the A15 contract definition and that the rationale is not sourced in the lesson.")
carry("L05-L06-card-L06-12of200", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c124", "twelve firm-years, six in and six out, matches flags_only_all_firms 6 and flags_only_oracle 6.")
add("L05-L06-cards-dup-scan", "2.7-cards", "course/modules/AC/AC2/cards.json (all 140 cards)", P,
    "scripts/L05-L06-r6/cards_compare.py and an inline scan: 140 records, 140 unique ids (AC2-c001..c140), no duplicate fronts or backs. Changed records this round: c075, c107 (outside slice), c123, c130 (outside slice).")
add("L05-L06-cards-coverage", "2.7-cards", "course/modules/AC/AC2/cards.json, L05 and L06 records", P,
    "32 records for these lessons: L05 15 (c063-c075, c122, c123) and L06 17 (c076-c088, c124, c125, c128, c138); all 32 read this round against their lesson text.")

# ---- structure and prose ----
add("L05-L06-struct-hours", "2.9-structure", "course/modules/AC/AC2/index.html data-hours-lessons=76, data-hours-project=34; L05.html data-hours=8; L06.html data-hours=10", P,
    "attributes re-read this round (unchanged); own estimates were 7.5 h and 9.5 h for L05 and L06 (round-4 note), within 30%.")
add("L05-L06-struct-sections", "2.9-structure", "course/modules/AC/AC2/L05.html, L06.html", P,
    "section order re-read: L05 why-it-matters, §1-§9 (claim, quintile arithmetic, lab, why accruals, canon breaks, misconceptions, problems, key results, quiz, references); L06 §1-§10 (definition, model, residual algebra, lab, choices, canon breaks, misconceptions, problems, key results, quiz, references). Template sections present.")
add("L05-L06-struct-banned", "2.9-structure", "course/modules/AC/AC2/L05.html, L06.html visible prose", P,
    "grep for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'left as an exercise', ellipses: no hit. Every 'about' number in the delta is derived on the page or from a printed value: about 1.43 SE, about 0.0010, about 41%, about 17 years, about 1.4 SD, about 0.001 (1/1000), about 129 (E1), about 61,900 (R1), about 0.015 (E1 binomial), about 59% (power 0.590). BUILDER_RULES 2 satisfied.")
carry("L05-L06-prose-unmarked-claims", "2.9-structure", "course/modules/AC/AC2/L05.html 'Why it matters' paragraph", "paragraph unchanged; claims point to Lab 1 or to a grade-C claim span.")
carry("L05-L06-prose-L04-xref", "2.9-structure", "course/modules/AC/AC2/L05.html §3 (cross-reference to L04 Proposition 3.1 and to L04 Section 1 Definition 1.3)", "§3 paragraph unchanged; the L04 cross-reference was checked against the L04 page in round 4.")
carry("L05-L06-prose-inversion", "2.9-structure", "course/modules/AC/AC2/L06.html §5 intro paragraph", "paragraph unchanged.")
add("L05-L06-prose-jargon", "2.9-structure", "course/modules/AC/AC2/L05.html §Honest pending; L06.html; cards.json; L05 hub card", P,
    "learner text grep (case-insensitive) for 'builder', 'this build', 'REQUESTS', 'unit report': no hit in L05.html, L06.html, cards.json or the L05 hub card (index.html line 149 and the L05 card body re-read). The honest-pending paragraph names plans/AC2-open-items.md once.")
carry("L05-L06-prose-concept-links", "2.9-structure", "course/modules/AC/AC2/L05.html (t-statistic linked in the meta row); L06.html ('b...' concept links)", "meta rows unchanged.")
add("L05-L06-dag", "2.9-dag", "course/modules/AC/AC2/L05.html, L06.html definitions and links", P,
    "check_dag AC2: PASS (rc 0). Concept definitions unchanged; the new sentences use only concepts defined earlier on the page or in L04 (accruals, t-statistic, OLS, least-squares projection).")
carry("L05-L06-figures", "2.9-structure", "course/modules/AC/AC2/L05.html, L06.html (no figure element changed)", "no figure was added or changed in the delta.")
carry("L05-L06-honest-data", "2.9-structure", "course/modules/AC/AC2/L05.html 'Honest pending' paragraph; L04 note", "paragraph unchanged; every number in Lab 1 is simulated and labelled.")
carry("L05-L06-r2-prop21-sigma0", "2.4-math", "course/modules/AC/AC2/L05.html Proposition 2.1 and proof", "unchanged; the sigma = 0.08 and 100-firm arithmetic is in E2 (recomputed).")
add("L05-L06-r2-lab-flags-only-lines", "2.5-labs", "tests/labs/AC2/lab-AC2-L06-1.py report() lines flags_only_all_firms, flags_only_oracle; course page", P,
    "the only L06 twin change is the a2 print line (renamed); the flags_only lines are unchanged and the page block still matches (cmp_pre.py 39/39).")
add("L05-L06-r2-attribution-sweep", "2.9-structure", "course/modules/AC/AC2/L05.html, L06.html, cards.json, index.html L05 card (every named source)", P,
    "named sources in the delta: Sloan (1996) (c075, c123 do not name it; L05 §3 and hub card 'the question Sloan (1996) asks', consistent with §3); Dechow (L06 §1, §5, §8 only, key and title); Beneish appears only in c107 (outside this slice). No new source name is introduced by the delta. Observation (not a row): the hub title 'The Accruals Anomaly (Sloan 1996)' labels the anomaly with Sloan's name; no page text in the slice says Sloan named the anomaly, and the Crossref abstract does not state the label; left for the architect.")
add("L05-L06-r2-num-L06-se-basis", "2.2-numbers", "course/modules/AC/AC2/L06.html §4 paragraph and R1 prompt", P,
    "§4 paragraph and R1 prompt are outside every delta hunk; the sentence 'the classical standard error ... 0.2824 ... 5.6 times the planted value' and 0.0489 recomputed (5.6, 0.0492 square-root rule).")
add("L05-L06-r2-lab-contamination-prop33", "2.5-labs", "course/modules/AC/AC2/L06.html Lab 1 interpretation; key-results row 2; Misconception 2; §5", P,
    "interpretation rewritten this round (0.2084 at full precision; 0.2085 from rounded coefficients): the claims that the difference is not the bias alone, that it mixes three printed components (0.1425 + 0.1965 - 0.1306 = 0.2084, residual 0.000000), and that the conditional-mean prediction 0.6223 is a different quantity all match the printed lines.")
add("L05-L06-r2-math-E2-zgap-cause", "2.4-math", "course/modules/AC/AC2/L05.html E2 solution (cause of -2.7937 vs -2.7996)", P,
    "E2 says the sweep values are 'consistent with a finite-sort effect that shrinks as the number of firms grows' and that four counts with 20 seeds do not establish the rate. The hedge matches the four printed values (-2.7437, -2.7728, -2.7912, -2.7991) and the 0.0025 seed-to-seed gap. No cause is asserted as established.")
carry("L05-L06-r2-math-L06-misc3-sentence", "2.4-math", "course/modules/AC/AC2/L06.html Misconception 3, first sentence", "sentence unchanged; the 'precision is the share of flagged firm-years that are manipulators' definition is consistent with the flag rule.")
carry("L05-L06-r2-prose-s4-lab-bears", "2.9-structure", "course/modules/AC/AC2/L06.html §4 opening paragraph", "paragraph unchanged.")
carry("L05-L06-r2-prose-A15-reference", "2.9-structure", "course/modules/AC/AC2/L06.html §3 units paragraph", "paragraph unchanged; atlas/A15.contract.md Scale row (line 190) matches.")
add("L05-L06-r3-num-L05-E2-printed", "2.2-numbers", "course/modules/AC/AC2/L05.html E2 solution and Lab 1 output lines mean_z_gap_*", P,
    "E2 now quotes planted_spread_8dp, spread_sd_theory_7dp and the sweep lines; each value is printed by lab05.out (cmp_pre IDENTICAL). Distances 0.0559, 0.0268, 0.0084, 0.0005 recomputed from the printed values and the analytic -2.7996.")
add("L05-L06-r3-num-L05-E3", "2.2-numbers", "course/modules/AC/AC2/L05.html E3 solution", P,
    "SE 0.0113137/sqrt120 = 0.0010328 (lab se_mean_120_7dp); distance -1.433 is the lab's seed0_distance_in_se, computed from full-precision values (lab line 200); rounded-input quotient -1.4330 and displayed-SE quotient -1.4369 -> -1.44 recomputed.")
add("L05-L06-r3-num-L06-decomp", "2.2-numbers", "course/modules/AC/AC2/L06.html Lab 1 interpretation, misconceptions, key-results row 2, lab output", P,
    "components 0.1425, 0.1965, 0.1306 printed; sum 0.2084 (recomputed); residual -0.000000 printed; weak residual 0.000000 printed.")
add("L05-L06-r3-num-L06-cond-mean", "2.2-numbers", "course/modules/AC/AC2/L06.html Lab 1 interpretation ('conditional-mean prediction for a1 is 0.6223')", P,
    "a1_conditional_mean_prediction 0.6223 printed (strong); E[d|X] = 0.05 x 0.10 = 0.005 stated and matches decompose_a1 (pred uses mean planted = 0.005).")
add("L05-L06-r3-num-L06-se-scaling", "2.2-numbers", "course/modules/AC/AC2/L06.html §4 and R1 solution; cards AC2-c125", P,
    "se_scaling output 0.2781 and 0.0489 printed; §4 and R1 unchanged in the delta; recomputed square-root rule 0.0492.")
add("L05-L06-r3-num-L06-a2z", "2.2-numbers", "course/modules/AC/AC2/L06.html Lab 1 interpretation ('lies 2.10 standard errors'), E3 solution", P,
    "interpretation: z = 2.096 at full precision (printed z_a2_fp), 2.097 from six-decimal values (recomputed 2.0968); both round to 2.10 at two decimals; tail 0.036 printed.")
add("L05-L06-r3-hyp-L06-shift", "2.5-labs", "course/modules/AC/AC2/L06.html 'Stated before running' hypothesis paragraph (Lab 1 hypothesis)", P,
    "hypothesis paragraph unchanged; its statements (a2 and a3 to within about two SE; a1 weakly identified; flags separate better at 0.05 than 0.01) match the printed output.")
add("L05-L06-r3-prose-L06-s2-purpose", "2.9-structure", "course/modules/AC/AC2/L06.html §2, paragraph after Definition 2.1, first sentence", P,
    "sentence unchanged; the description of the regressors and the no-intercept estimator matches the A15 contract's modified_jones (lab docstring and contract line 123).")
add("L05-L06-r3-prose-L06-s5-bullet", "2.9-structure", "course/modules/AC/AC2/L06.html §5 bullet 2 (receivables adjustment)", P,
    "bullet 2 rewritten this round; claims re-checked: the adjustment is a regressor whether or not manipulation runs through revenue (lab total = ... + C2 (drev - drec)/lag); C2 = 0.10 in C_TRUE; the planted manipulation enters DA directly (DA = SHIFT x manipulator + noise). No claim about a revenue channel is made beyond what the generator does.")
carry("L05-L06-r3-prose-L06-imprecise", "2.9-structure", "course/modules/AC/AC2/L06.html §4 (the 'too imprecise' sentence removed in round 5)", "the paragraph is unchanged since 11b3477; the removed sentence is absent (grep 'imprecise' finds none in L06.html).")
carry("L05-L06-r3-cards-c083-c087-c124-c125", "2.7-cards", "course/modules/AC/AC2/cards.json AC2-c083, c087, c124, c125", "records byte-identical; " + CARD_OK + "; numbers recomputed.")
carry("L05-L06-r3-cit-dechow-crossref-abstract", "2.1-citations", "course/modules/AC/AC2/L06.html §8 key-results row 6 and §5 claim span", "rows unchanged; the Crossref abstract matches the claim (verify_refs live run, this round).")
carry("L05-L06-r3-math-L06-misc2-first-term", "2.4-math", "course/modules/AC/AC2/L06.html Misconception 2 ('Only the first term is the effect of including manipulators')", "misconception 2 unchanged in the delta; the three-term decomposition it cites matches the printed lines.")
add("L05-L06-r3-cmd-validate", "2.9-structure", "ledgers/AC2/L05-L06.json (round 6 fragment)", P,
    "ledger.validate on the round-6 fragment (see the validation run in the final report) returned no problems; every non-PASS row carries a fix.")

# ---- round-4 rows ----
add("L05-L06-r4-arith-L05-E2", "2.4-math", "course/modules/AC/AC2/L05.html E2 solution (expected t sentence)", P,
    "expected t 2.1647 (displayed SD) and 2.164 (SD 0.0113137, planted 0.00223495) recomputed; 2.164 is the printed expected_t_at_planted.")
add("L05-L06-r4-arith-L06-E3", "2.4-math", "course/modules/AC/AC2/L06.html E3 solution (z sentence)", P,
    "z = 0.003076/0.001467 = 2.0968 -> 2.097 and the lab's full-precision 2.096 are both stated with their source; the rounding variants recomputed (2.067, 2.051, 2.113).")
add("L05-L06-r4-prose-L06-s5-reserves", "2.9-structure", "course/modules/AC/AC2/L06.html §5 bullet 2", P,
    "the reserves sentence is absent from bullet 2 (grep 'reserve' in §5 finds none); the bullet now makes only the revenue-channel claim checked above.")

# ---- round-5 FAIL rows, re-verified ----
add("L05-L06-r5-unrounded-sd-label", "2.2-numbers", "course/modules/AC/AC2/L05.html E2 and E3 solutions; course/modules/AC/AC2/cards.json AC2-c123", P,
    "grep for 'unrounded' in L05.html, L06.html and cards.json: no hit. E2 now writes 0.0113137 (full precision) and 0.011314 as the six-decimal rounding; E3 writes 0.0113137; c123 writes SD 0.0113137. The displayed results are unchanged (2.164, 0.0010328).")
add("L05-L06-r5-L06-E3-cause", "2.2-numbers", "course/modules/AC/AC2/L06.html E3 solution (sentence 'Using the rounded inputs 0.0031 and 0.0015 ...')", P,
    "the sentence now says the rounding of 'the inputs' moves z (2.067) and that rounding the SE alone gives 2.051 (tail 0.040) and rounding the difference alone gives 2.113 (tail 0.035). Recomputed in recompute_r6.py; the attribution to both inputs is the stated cause and the single-input values are given.")
add("L05-L06-r5-L06-s5-revenue-channel", "2.9-structure", "course/modules/AC/AC2/L06.html §5 bullet 2 (line 359)", P,
    "the bullet now states the lab plants no manipulation through revenue and that the revenue-less-receivables term enters the generator's true accruals with coefficient 0.10 (lab-AC2-L06-1.py make_sample: total = lag x (C1/lag + C2 (drev - drec)/lag + C3 ppe/lag + DA); C_TRUE[1] = 0.10). Verified true.")

# ---- ledger-level ----
PREV_IDS = [
    "L05-L06-cmd-pin", "L05-L06-cmd-check-pages", "L05-L06-cmd-check-dag", "L05-L06-cmd-run-labs", "L05-L06-cmd-twins-isolated",
    "L05-L06-cmd-page-smoke", "L05-L06-cmd-verify-refs-unit", "L05-L06-cmd-verify-refs-offline", "L05-L06-cmd-lint",
    "L05-L06-cit-sloan-registry", "L05-L06-cit-sloan-claim-s1", "L05-L06-cit-sloan-claim-s3", "L05-L06-cit-dechow-registry",
    "L05-L06-cit-dechow-scope", "L05-L06-cit-dechow-motivation", "L05-L06-cit-dechow-grouping", "L05-L06-cit-dechow-authors",
    "L05-L06-cit-mclean", "L05-L06-cit-hou", "L05-L06-reg-used-by", "L05-L06-num-L05-lab", "L05-L06-num-L05-derived",
    "L05-L06-num-L06-lab", "L05-L06-num-L06-derived", "L05-L06-num-L06-roughly-4pct", "L05-L06-math-L05-def-t",
    "L05-L06-math-L05-prop21", "L05-L06-math-L05-prop23", "L05-L06-math-L05-remark22-P1-P3", "L05-L06-math-L06-prop31",
    "L05-L06-math-L06-prop33-formula", "L05-L06-math-L06-prop33-statement", "L05-L06-math-L06-P3",
    "L05-L06-math-L06-remark32-P1-P2", "L05-L06-math-notation", "L05-L06-lab-L05-1-run", "L05-L06-lab-L05-1-interp",
    "L05-L06-lab-L06-1-run", "L05-L06-lab-L06-1-overreach-sample", "L05-L06-lab-L06-1-single-seed",
    "L05-L06-lab-L06-1-threshold-claim", "L05-L06-lab-L06-1-flag-count", "L05-L06-card-L05-defs", "L05-L06-card-L05-lab",
    "L05-L06-card-L05-sloan", "L05-L06-card-L06-defs", "L05-L06-card-L06-lab", "L05-L06-card-L06-iff",
    "L05-L06-card-L06-projection", "L05-L06-card-L06-only-when", "L05-L06-card-L06-dechow", "L05-L06-card-L06-12of200",
    "L05-L06-cards-dup-scan", "L05-L06-cards-coverage", "L05-L06-struct-hours", "L05-L06-struct-sections",
    "L05-L06-struct-banned", "L05-L06-prose-unmarked-claims", "L05-L06-prose-L04-xref", "L05-L06-prose-inversion",
    "L05-L06-prose-jargon", "L05-L06-prose-concept-links", "L05-L06-dag", "L05-L06-figures", "L05-L06-honest-data",
    "L05-L06-r2-prop21-sigma0", "L05-L06-r2-lab-flags-only-lines", "L05-L06-r2-attribution-sweep",
    "L05-L06-r2-num-L06-se-basis", "L05-L06-r2-lab-contamination-prop33", "L05-L06-r2-math-E2-zgap-cause",
    "L05-L06-r2-math-L06-misc3-sentence", "L05-L06-r2-prose-s4-lab-bears", "L05-L06-r2-prose-A15-reference",
    "L05-L06-r3-num-L05-E2-printed", "L05-L06-r3-num-L05-E3", "L05-L06-r3-num-L06-decomp", "L05-L06-r3-num-L06-cond-mean",
    "L05-L06-r3-num-L06-se-scaling", "L05-L06-r3-num-L06-a2z", "L05-L06-r3-hyp-L06-shift", "L05-L06-r3-prose-L06-s2-purpose",
    "L05-L06-r3-prose-L06-s5-bullet", "L05-L06-r3-prose-L06-imprecise", "L05-L06-r3-cards-c083-c087-c124-c125",
    "L05-L06-r3-cit-dechow-crossref-abstract", "L05-L06-r3-math-L06-misc2-first-term", "L05-L06-r3-cmd-validate",
    "L05-L06-r4-arith-L05-E2", "L05-L06-r4-arith-L06-E3", "L05-L06-r4-prose-L06-s5-reserves",
    "L05-L06-r5-unrounded-sd-label", "L05-L06-r5-L06-E3-cause", "L05-L06-r5-L06-s5-revenue-channel",
]
have = {r["id"] for r in rows}
missing = [i for i in PREV_IDS if i not in have]
if missing:
    sys.exit("missing previous ids: %s" % missing)

fails = [r["id"] for r in rows if r["status"] != P]
counts = {s: sum(1 for r in rows if r["status"] == s) for s in (P, F, "UNVERIFIABLE")}
frag = {
    "unit": "AC2",
    "slice": "L05-L06",
    "round": 6,
    "verifier": "AC2 independent verifier, round 6, slice L05-L06 (fresh verifier; did not build AC2; shares no context with the builders or the rounds 1-5 verifiers)",
    "pin": "ff9284f",
    "base": "11b3477",
    "checkout": ROOT,
    "scratch": "/tmp/ac2-v/L05-L06-r6",
    "verified_at": "2026-10-27T00:00:00+00:00",
    "verdict": "PASS" if not fails else "FAIL",
    "mutants": [],
    "registry_flags": [
        "dechow1995detecting: registry and Crossref list two authors (Dechow, Sloan); the curriculum string is three-author. Architect ruling 1; learner text names the key and the title only. Not resolved here.",
    ],
    "freshness_flags": [],
    "notes": [
        "Delta 11b3477..ff9284f read in full for the slice (scripts/L05-L06-r6/delta-11b3477-HEAD-L05-L06-cards-labs.diff): L05.html 6 hunks, L06.html 10 hunks, cards.json AC2-c075 and AC2-c123, both lab twins, index.html L05 card body (text only, 'the question Sloan (1996) asks').",
        "Both pages were read in full, line by line (L05.html 470 lines, L06.html 587 lines), and the 32 slice cards were read in full.",
        "Round-5 FAIL rows: L05-L06-r5-unrounded-sd-label, L05-L06-r5-L06-E3-cause and L05-L06-r5-L06-s5-revenue-channel are now PASS (fixed text re-verified). L05-L06-card-L05-lab is FAIL again because c075 was changed and its basis still cites 0.0022350, a value Lab 1 does not print.",
        "New FAIL row L05-L06-r6-L06-s1-source-wording: the page says the contract's source is dechow1995detecting; the contract cites the model to the accrual-model literature with 'see' dechow1995detecting.",
        "Lab 1 of L05 and L06 is SIMULATED; each lab number on the pages is labelled as such. No Beneish or other unconfirmed constant appears in these pages.",
        "Publisher pages were not fetched; the Crossref records were read through tools/verify_refs.py --unit AC2 (7 of 560 entries, 0 problems).",
        "Observation for the architect, not a row: the hub title 'The Accruals Anomaly (Sloan 1996)' names Sloan for the anomaly label, which the lesson text does not state.",
        "Observation, not a row: L05 R1 solution defines s = 0.01131 and then solves with 0.0113137; the two values agree at the printed precision and the result T = 201 is unchanged.",
        "Observation, not a row: L05 R3 solution names 'investor inattention to accrual persistence' as the mispricing mechanism; Section 3 names only 'mispricing'. Carried from round 5 (unchanged since 2607c60).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts[P],
        "fail": counts[F],
        "unverifiable": counts["UNVERIFIABLE"],
        "fail_ids": fails,
    },
    "rows": rows,
}
out = ROOT + "/ledgers/AC2/L05-L06.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "counts", counts, "fails", fails)
