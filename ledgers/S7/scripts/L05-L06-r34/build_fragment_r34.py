"""Round-34 update of the S7 L05-L06 fragment (round 33 -> round 34). Keeps every row id.

Reads the round-33 fragment (saved as /tmp/ap1-r5/L05-L06/r34/round33_fragment.json before this round), replaces the
evidence and status of the rows this round re-ran or re-derived, recomputes the summary, validates with ledger.validate
and writes ledgers/S7/L05-L06.json. Scripts and outputs are cited by repository path in each row.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/build_fragment_r34.py
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

S = "ledgers/S7/scripts/L05-L06-r34/"
OUT_DIR = "/tmp/ap1-r5/L05-L06/r34/"
frag = json.loads(Path(OUT_DIR, "round33_fragment.json").read_text(encoding="utf-8"))

VAR = (f"variant_runs.py (archived {S}variant_runs.py; each variant is the repository twin with one stated parameter "
       f"changed, run python -I -W error in a scratch copy; outputs {OUT_DIR}variants/<name>.out)")
E3 = f"e3_quadrature_and_se.py ({S}e3_quadrature_and_se.py; output {OUT_DIR}e3.out)"
MC = f"mc_checks.py ({S}mc_checks.py; output {OUT_DIR}mc_checks.out)"
QZ = f"quiz_keyresults_check.py ({S}quiz_keyresults_check.py; output {OUT_DIR}quiz_keyresults.out)"
DN = "ledgers/S7/scripts/L05-L06-r33/derive_numbers.py (output /tmp/ap1-r5/L05-L06/derive_numbers.out, 121 checks OK)"
TIME = f"time_snippets.sh ({S}time_snippets.sh; output {OUT_DIR}timings.out)"
L6NULL = f"lab6_null_and_search.py ({S}lab6_null_and_search.py; output {OUT_DIR}lab6_null.out)"
TOK = f"token_reconciliation.py ({S}token_reconciliation.py; output {OUT_DIR}token_recon.out)"
DRIVE = "round-33 figure drive (ledgers/S7/scripts/L05-L06-r33/drive_figures.py)"

UPD: dict[str, tuple[str, str, str]] = {}


def pas(rid: str, text: str) -> None:
    UPD[rid] = ("PASS", text, "")


def unv(rid: str, text: str, fix: str) -> None:
    UPD[rid] = ("UNVERIFIABLE", text, fix)


# (a) variant lab runs
variant_text = ("Round 34 (fresh): {what}; {script}. Page values reproduced: {vals}.")
for rid in ("L06-lab2-universes-line423", "R29-lab-prose-L06-2-universes"):
    pas(rid, variant_text.format(what="Lab 2 twin with the stated change universes = (slice(0, 60),) (pre-specified test unchanged), and the base twin",
                                  script=VAR,
                                  vals="12 specifications; best-of-search rate 0.240 (page 0.240); median smallest p 0.1108 (page 0.111); effective number 5.4 (page 5.4); base run 0.493, 0.0517, 13.3 match the page's expected block. Monte Carlo error sqrt(0.24 x 0.76 / 300) = 0.0246 (page 0.025, derived in the prose)"))
for rid in ("L06-lab1-m1000-line430", "R29-lab-prose-L06-1-BHY"):
    pas(rid, variant_text.format(what="Lab 1 twin with the real-effect share changed to 0.05 and to 0.5 (full M loop, M = 1000 row read; base share 0.2 full loop)",
                                  script=VAR,
                                  vals="M = 1000 row: Bonferroni 4.06, Holm 4.05 at every share; BHY 4.08 at share 0.05 (page 4.08), 3.19 at 0.5 (page 3.19), 3.54 at 0.2 (page 3.54, the expected block)"))
pas("R29-lab-prose-L05-1-table", variant_text.format(what="Lab 1 twin with rho changed to 0.0 and 0.9 (seed 505 kept); base rho 0.3 expected block",
                                  script=VAR,
                                  vals="rho 0.0: first step 2.788, single 5.481, step-down 5.691, gain 0.210, FWER 0.041 (page row 0.0: 2.788 5.481 5.691 0.210 0.041); rho 0.9: 2.173, 6.791, 6.852, gain 0.061, FWER 0.052 (page 2.173 6.791 6.852 0.061 0.052); rho 0.3: 2.743, 5.596, 5.798, 0.202, 0.045 (expected block)"))

# (b) E1-E3 seeded and simulated values
pas("L05-num-E1", f"Round 34 (fresh): the Problem E1 table reproduced by {VAR} (rho 0.0, 0.9, seed 505) and by the expected block (rho 0.3); the derived first-step values 2.799 (rho 0) and 2.705 (n = 15) are derived in {DN}. The FWER 0.052 at rho 0.9 is within one Monte Carlo standard error (0.0034) of 5%: |0.052 - 0.05| = 0.002.")
pas("L05-num-E2", f"Round 34 (fresh): closed-form values 13/7 = 1.857, sqrt = 1.363, 1 - Phi(1.645/1.363) = 0.114, 1 + 499/20 = 25.95 are re-derived in {DN} (all OK). The simulation of sol-S7-L05-E2 (seed 52, 300 replications, output {OUT_DIR}base/sol-S7-L05-E2.out) gives rejection rates 0.113, 0.063, 0.067 at mean block 1, 5, 20: consistent with the page's 0.114, 'roughly 11%' and 'toward 5%' (SE about 0.018 at 0.114).")
pas("L05-num-E3", f"Round 34 (fresh): sol-S7-L05-E3 run (seed 503; {OUT_DIR}base/sol-S7-L05-E3.out): pair critical value 8.213 (derived 8.224), studentized critical 1.959 (derived 1.955), first-step rates 0.0000 (derived 9e-8) and 0.8486 (derived 0.852, MC SE 0.0025), StepM 0.0447 (derived 0.0456 = 0.050 x 0.912) and 0.8499 (derived 0.8536). {E3} gives 1 - Phi(5.224) = 8.7549e-8, P(N(0,1) > 1.9545) = 0.0253, P(1.6449 < N(3,1) < 1.9545) = 0.0602, 0.8521 + 0.0253 x 0.0602 = 0.8536, 0.050 x 0.912 = 0.0456; every page value agrees within its simulation SE.")
pas("L06-num-E3", f"Round 34 (fresh): {E3}: P(|N(3,1)| > 1.96) by quadrature 0.850830 (page 0.851); truly-null share among published 0.345914, 0.120577, 0.037697 (page 0.346, 0.121, 0.038). sol-S7-L06-E3 (seed 64, 400 replications) re-run with per-replication SE: null shares 0.344 (SE 0.0031), 0.119 (SE 0.0015), 0.037 (SE 0.0007) vs 0.3459, 0.1206, 0.0377, i.e. within 0.6, 1.1 and 0.0 SE; Holm unrejected share 0.844, 0.784, 0.763 and hurdle 3.83, 3.82, 3.80 reproduced (page 0.844, 0.784, 0.763; 3.80 to 3.83); Phi^-1(1 - 0.05/800) = 3.836107 (page 3.836).")
pas("L06-math-E3-formula", f"Round 34 (fresh): the E3 formula's integral evaluated by scipy.integrate.quad in {E3}: P(|N(3,1)| > 1.96) = 0.850830; the page's Phi(1.04) + Phi(-4.96) = 0.85081 agrees.")
pas("R29-num-L06-lab-quotes", f"Round 34 (fresh): P-solution values 0.346, 0.121, 0.038 and the 0.851 reproduced by {E3} (see L06-num-E3); the seeded run sol-S7-L06-E3 re-run with its SE (seed 64).")
pas("L06-num-E1", f"Round 34 (fresh): E1 variant (Lab 2 with the universe choice dropped, {VAR}): rate 0.240 (page 0.240), effective number 5.4 (page 5.4), median 0.1108 (page 0.111). The page's prediction 1 - 0.95^4.5 = 0.21 and the MC error 0.025 (sqrt(0.24 x 0.76/300) = 0.0246) are reproduced arithmetically.")
pas("L06-num-E2", f"Round 34 (fresh): E2 variant (Lab 1 with the real-effect share 0.05 and 0.5, M = 1000, {VAR}): BHY 4.08 and 3.19 (page 4.08, 3.19); Bonferroni 4.06 and Holm 4.05/4.04 at both shares; base 3.54 for share 0.2 (page 3.54).")
pas("L05-num-misconceptions-new", f"Round 34 (fresh): misconception 5's 0.950 and 0.455 are the Lab 4 expected-block outputs at rho = 0.3 (lab-S7-L05-4 run this round, {OUT_DIR}base/lab-S7-L05-4.out). Misconception 6: the Problem M1 values (t = 4.1, 2.9, 2.2, 1.0; c = 2.5, 2.1, 1.7; single-step rejects {{1,2}}, step 2 rejects {{3}}; with t3 = 2.0 nothing) re-derived by {DN} (the 'L05 M1 ...' checks, all OK). The inequality c_alpha(band) >= c_alpha({{1,2,3,4}}) is Proposition 6.4(b), a theorem, not a number.")
pas("L05-num-key-results-new", f"Round 34 (fresh): key-results rows 8-17 (page lines 1196-1205): 0.603 re-derived ({DN}, 'R4'); 45.5% and 84.8% are the Lab 4 outputs (0.455, 0.848); 0.3% and 17% are the ratios 3.031/3.023 and 1 - 2.508/3.023 of the Lab 4 mean critical values (band half-width = c x SE with a common SE), 0.26% and 17.04%; 0.2% below Bonferroni = (3.023 - 3.016)/3.023 = 0.23%; 10.08 = 2 x 5.04, the Lab 6 output line 'band half-widths from 5.04 to 7.26' ({OUT_DIR}base/lab-S7-L05-6.out). Script {S}quiz_keyresults_check.py (all OK).")
pas("L05-num-M4-table-values", f"Round 34 (fresh): the table at page line 952 re-read: estimates and SEs (A 6.8 (2.0) ... J -0.6 (2.0)); z = estimate/SE = 3.4, 3.0, 2.7, 2.5, 2.2, 1.6, 1.2, 0.8, 0.4, -0.3 equal the page's line 954 list (checked in {QZ}); two-sided p-values equal 0.00067 ... 0.76418 (same script); BH R = 5 and the intervals (derive_numbers.py, 'L05 M4 ...' checks, all OK).")
pas("L05-num-quiz", f"Round 34 (fresh): the quiz's numbers recomputed in {QZ}: ceil(0.95 x 999) = 950; Phi^-1(0.95^(1/10)) = 2.568 and its argument 0.99488; k-FWER alpha_10 = 0.15/93 = 0.001613; 8.224 (unstudentized c); 1.955 (studentized c). All OK.")
pas("R26-quiz-L05-explanations", f"Round 34 (fresh): the 14 items' visible numbers (950, 2.568, 0.99488, 0.001613, 8.224, 1.955, 1 - Phi(5.224) ~ 9e-8) recomputed in {QZ}; the explanation texts are carried (page lines 1216-1327 unchanged).")
pas("R27-quiz-explanations-L06", f"Round 34 (fresh): the L06 quiz's numbers (3.78; 0.842; 0.59 = 0.493/0.842; e^-2 = 0.1353; e^-4.5 = 0.0111; x = 1.0998; 0.5238) recomputed in {QZ}: all OK.")
pas("L05-num-E2-runtime", f"Round 34 (fresh): {TIME}: sol-S7-L05-E2 under python -I -W error, three runs, 1.87-1.91 s wall. No runtime claim is printed in the current text of L05 lines 1029-1075 (grep for seconds, minutes, runs in, runtime: none), so there is no claim to contradict; the time is far under the 10 s lab budget.")
pas("L06-num-E3-runtime", f"Round 34 (fresh): {TIME}: sol-S7-L06-E3, three runs, 0.17 s wall each. No runtime claim is printed in L06 lines 433-437 or the solution (grep: none).")

unv("L05-lab6-unsourced-1.5", f"Round 34 (fresh): the derivation 30 x 0.05 = 1.5 is linearity of expectation (exact). {L6NULL}: skill-free null on the twin's demeaned rule returns, stationary bootstrap of whole dates (mean block 10), 2000 repetitions, one-sided t > 1.645 per rule: mean per-rule rejection rate 0.0463 (SE of one rate 0.0047), expected false rejections among 30 rules 1.388 (SE 0.026) vs the page's 1.395 (|diff| 0.007, inside 0.3 SE): REPRODUCED. NOT reproduced: the page's per-rule range 0.046 to 0.048; this run's per-rule rates span 0.033 to 0.058, which is sampling noise at 2000 repetitions (SE 0.0047), and the page's 40-repetition design is not stated, so the range cannot be re-derived.", "Give the null simulation's procedure, seed and repetition count (or quote only the mean rate and the expected count, which are reproduced), so the per-rule range can be re-run.")

# (c) Monte Carlo rows
pas("L06-math-prop32", f"Round 34 (fresh): {MC}: iid K = 36 p-values, P(min <= 0.05) = 0.84279 by 200,000 draws vs 1 - 0.95^36 = 0.84222 (SE 0.00082, 0.7 SE); mean of the minimum 0.027013 vs 1/37 = 0.027027 (SE 0.000059). Dependent (equicorrelated normal) FWER at rho = 0, 0.5, 0.9, 0.99: 0.8412, 0.5474, 0.1791, 0.0784, each inside [0.05, min(1, 36 x 0.05)] with the six-SE tolerance. The page states no tolerance; six standard errors used.")
pas("R32-prop32-proof-and-mc", f"Round 34 (fresh): {MC} (the Proposition 3.2 Monte Carlo; the FWER values and the independence value 0.8422 reproduced; all inside the bounds within six SE).")
pas("R27-lemma76-mc", f"Round 34 (fresh): {MC}: 40 random cases (t <= 11, M <= t, valid dependent p-values from an equicorrelated normal copula, rho in {{0, 0.3, 0.8}}, 100,000 draws each): no case has P(union) above t times the sum of (beta_l minus beta_(l-1)) over l by more than six SE; Hommel case t = M = 20: LHS 0.05007 <= RHS 0.17989 = alpha H_20 (SE 0.00049).")
pas("R27-diff-L05-582", f"Round 34 (fresh): {MC} (Lemma 7.6 inequality, as above) and the summation-by-parts identity sum over j of w_j beta_j = sum over l of (beta_l - beta_(l-1)) divided by l checked on 3000 random beta: max difference 1.1e-16 ({QZ}).")
pas("R29-math-def66-fcr-line499", f"Round 34 (fresh): {MC}: K = 20 band at level 0.95 (Bonferroni critical value 3.0233), selections 'R largest |z|' for R = 1, 3, 10, 20, 200,000 replications: FCR 0.01128, 0.00699, 0.00404, 0.00250, all below alpha = 0.05; P(V >= 1) at most 0.04889. Page line 499's bound FCR <= alpha is consistent (six-SE tolerance; the page states no tolerance).")
pas("R32-L05-333-reversal-sentence", f"Round 34 (fresh): Phi^-1(0.975) = 1.960 and Phi^-1(0.95^(1/2)) = 1.955 ({DN}); {MC}: Monte Carlo 95% quantile of max(X, -X) = 1.9616 over 4,000,000 draws vs 1.960 (SE of the quantile about 0.0009). The sentence's direction (independent resampling understates the critical value, 1.955 < 1.960) holds.")
pas("R32-L05-333-E1-sentence", f"Round 34 (fresh): {VAR}: first-step critical values 2.788 (rho 0.0), 2.743 (rho 0.3), 2.173 (rho 0.9), falling as rho rises as the sentence says; the independent value 2.799 at rho = 0 derived ({DN}).")
pas("L05-lab6-search-bound", f"Round 34 (fresh): {L6NULL}: the 95% quantile of the centred bootstrap maximum over the first m rules is 2.1404 (m = 5), 2.4525 (10), 2.6475 (15), 2.8040 (20), 2.8178 (25), 2.8371 (30) = nondecreasing (the sentence's claim), and the value 2.8371 equals the Lab 6 StepM first step 2.837 (expected block).")

# (d) bracket
pas("R30-edit-L06-line95-bracket", f"Round 34 (fresh): {MC} (section 4): the two Mills-ratio roots of alpha/(2M) = phi(x)/x and = x phi(x)/(1+x^2) at M = 316, alpha = 0.05 give 3.7760361676 and 3.7927784742 (page 3.7760 and 3.7928 to four decimals); Phi^-1(1 - 0.05/632) = 3.7777874 (page 3.7778).")
pas("R30-num-L06-mills-M316", f"Round 34 (fresh): {MC} (section 4): bracket [3.7760, 3.7928] and t* = 3.7778 reproduced from scratch.")

# (f) token sweeps
unv("R31-sweep-numbers-L05", f"Round 34: {TOK}. L05 has 1,972 visible numeric tokens: locator 250, year 15, lab-output 493, re-run output 194, derived 1 (by precedence), unclassed 1,020 (integers below 10 and one-decimal values, which collide with too many outputs to match by value; they were read in context: indices, item and step numbers, twin parameters such as rho, drift and sd, and the one-decimal prose values checked in the derived and lab-output rows above). Every integer or one-decimal token with two decimals or a value of 10 or more is classed; the eight residue tokens are index labels (1234, 34, 31, from set subscripts and pi_1) and Phi(1.04) pieces in L06, not L05.",
    "Match each of the 1,020 unclassed L05 integer and one-decimal tokens to its role (index, count, parameter or output), or reduce the sweep's class of small numbers to a recorded rule, and record the derived tokens with their derivation.")
unv("R31-sweep-numbers-L06", f"Round 34: {TOK}. L06 has 878 visible numeric tokens: locator 74, year 4, lab-output 188, re-run output 144, unclassed 468 (integers below 10 and one-decimal values, classed by context, not matched by value). Tokens with two decimals or a value of 10 or more are all classed; the residue of that kind is the index labels and the Phi(1.04) / Phi(-4.96) pieces of the E3 formula, which are derived in {E3}.",
    "Match each of the 468 unclassed L06 integer and one-decimal tokens to its role, and record the derived tokens with their derivation.")
pas("R31-vague-quantities", f"Round 34 (fresh): every use of a vague quantity word in L05 and L06 visible text that qualifies a number was listed (vague_contexts.py, {S}vague_contexts.py; output {OUT_DIR}vague_contexts.txt): about 0.2 and about 0.003 (L05 l.184, derived and lab output), about 3.5% and about 1.4 SE (l.273, derived), about 95% (l.420, Lab 4), 'about half' (l.709: 9.0-11.2 against 18.0-19.5 in the Lab 5 output, ratio about 0.5), about 1.6 and about 2.6 (l.898, Lab 3), less than one in ten million (l.902, 8.75e-8), about 26 blocks and roughly 11% (l.1034), about 0.013 (l.1075), about 0.0025 (l.1123), about 0.013, about 4%, about 0.025 and 3.836 in L06 (l.244, 380, 423, 470); the rest are source quotations (carried with their span) or qualitative. Limits: 'many' and 'some' used as qualitative words were not judged individually.")

# (g) round-32 spot-check sample (all values in the rows above and in derive_numbers / mc / quiz checks)
pas("R32-numbers-spotcheck", f"Round 34 (fresh): the round-32 sample (3.7778; 0.8422; 0.0126; 1.96 to 5.0792 bounds and hurdles; 2.4267, 3.2068, 3.8832; 3.8361; 0.0382 and 7.47; MC SE 0.0034 and 0.0109 and the 1.38 SE gap; 2.5679, 2.7992, 2.5758, 2.8070; 1.9600; 1.959964; 1.9545; 0.6027) re-derived in {DN}, {MC} and {QZ}; all agree with the page's printed digits.")

# registry / unchanged rows keep their round-33 decisions
ids = [r["id"] for r in frag["rows"]]
rows = []
for r in frag["rows"]:
    if r["id"] in UPD:
        status, text, fix = UPD[r["id"]]
        new = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": text}
        if status != "PASS":
            new["fix"] = fix
        rows.append(new)
    else:
        rows.append(r)
missing = set(UPD) - set(ids)
assert not missing, missing
assert len(rows) == len(ids) == len({r["id"] for r in rows})

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag2 = dict(frag)
frag2.update({
    "round": 34,
    "verifier": "verifier round 34 (S7 L05-L06, ROUND 2 of the toolchain re-confirmation: the round-33 UNVERIFIABLE rows re-run; independent of the builders and of round 32)",
    "pin": "47bac8d",
    "base": "5e5da87",
    "previous_ledger": "round 33 fragment (copied at /tmp/ap1-r5/L05-L06/r34/round33_fragment.json before this round); round 32 at 47bac8d:ledgers/S7/L05-L06.json",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts["PASS"] == len(rows) else "FAIL",
    "rows": rows,
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": 0,
        "mutants_killed": 0,
        "mutants_note": "lessons only; no grader or project in L05 or L06, so 0/0",
        "round34_rows_rerun": len(UPD),
        "carried_byte_identical_since_5e5da87": sum(1 for r in rows if r["evidence"].startswith("Carried from the release ledger")),
        "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    },
})
frag2["notes"] = list(frag.get("notes", [])) + [
    "ROUND 34 (second pass, coordinator request): 'not re-run' rows were re-run or re-derived. Variant lab runs: L06 lab 2 (universes), L06 lab 1 (share 0.05, 0.5, M = 1000 and the full loop), L05 lab 1 (rho 0.0, 0.9); seeded solution runs: sol-S7-L05-E2, sol-S7-L05-E3, sol-S7-L06-E3 (also per-replication SEs); Monte Carlo: Prop 3.2, Lemma 7.6, FCR band (line 499), reversal quantile; quadrature: E3 integral (L06), bracket 3.7760-3.7928; quiz and key-results arithmetic; M4 table; timings of the three snippets; token and vague-word sweeps.",
    "ROUND 34 REMAINING: L05 Lab 6 null count's per-rule range 0.046-0.048 (the page's 40-replication design not reproducible; my mean 0.0463, count 1.388 agree with 1.395), and the two token sweeps (small integers and one-decimal tokens not matched by value).",
]
frag2["registry_flags"] = list(frag.get("registry_flags", []))
problems = ledger.validate(frag2, "S7/L05-L06")
Path(ROOT / "ledgers/S7/L05-L06.json").write_text(json.dumps(frag2, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "rerun", len(UPD), "validate:", problems)
