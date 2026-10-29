import json, sys
root = sys.argv[1]
S = "ledgers/E3/scripts/E3-b-r5"
def row(i, check, loc, ev):
    return {"id": i, "check": check, "location": loc, "status": "PASS", "evidence": ev}
R = []
R.append(row("E3b-cmd-run_labs", "2.5 labs", "tools/run_labs.py --unit E3; tests/labs/E3/",
  f"`.venv/bin/python tools/run_labs.py --unit E3` -> 'run_labs E3: PASS (11/11)', exit 0 ({S}/run_labs_E3.out)."))
for n in ("04", "05", "06"):
    R.append(row(f"E3b-cmd-check_pages-L{n}", "2.9 structure", f"course/modules/E/E3/L{n}.html",
      f"`tools/check_pages.py --unit E3 --page L{n}` -> 'check_pages E3 L{n}: PASS', exit 0 ({S}/check_pages_L{n}.out)."))
R.append(row("E3b-cmd-check_dag", "2.9 DAG", "tools/check_dag.py --unit E3",
  f"'check_dag E3: PASS', exit 0 ({S}/check_dag.out). Anchors and prerequisite closure re-run on 04626e9."))
R.append(row("E3b-cmd-check_projects", "2.6 projects", "tools/check_projects.py --unit E3",
  "'check_projects E3: PASS', exit 0. No project page is in slice b; recorded as run, not as slice evidence."))
R.append(row("E3b-cmd-build_site", "gate", "tools/build_site.py --check",
  "'site data current: 6 outputs', exit 0."))
R.append(row("E3b-cmd-verify_refs-offline", "2.1 citations", "tools/verify_refs.py --offline",
  "'offline integrity: 560 entries, 0 problems', exit 0. The live --unit run was not repeated."))
R.append(row("E3b-cmd-page_smoke", "2.9 page_smoke", "tools/page_smoke.py --unit E3 --pages L04 L05 L06",
  "'page_smoke E3: PASS', exit 0."))
R.append(row("E3b-cmd-ruff-mypy-pytest", "gate", "ruff check; ruff format --check; mypy --no-incremental; pytest tests/test_labs.py tests/test_page_checks.py -k 'E3 or lab'",
  f"'All checks passed!'; '335 files already formatted'; 'Success: no issues found in 229 source files'; pytest dots only, exit 0 ({S}/ruff_check.out, ruff_format.out, mypy.out, pytest_labs.out)."))
for n in ("04", "05", "06"):
    R.append(row(f"E3b-lab-L{n}-twin-isolated", "2.5 labs", f"tests/labs/E3/lab-E3-L{n}-1.py",
      f"`.venv/bin/python -I -W error tests/labs/E3/lab-E3-L{n}-1.py` exit 0; output in {S}/twin_L{n}.out."))
    R.append(row(f"E3b-lab-L{n}-page-equals-twin-and-expected", "2.5 labs", f"course/modules/E/E3/L{n}.html (pre data-run; pre.expected)",
      f"{S}/lab_compare_r5.py (run with -I): 'embedded code == twin: True', 'expected == twin stdout: True' for L{n} ({S}/lab_compare_r5.out)."))
R.append(row("E3b-refs-epstein1989", "2.1 citations", "references/references.json epstein1989substitution; course/modules/E/E3/L05.html data-cite",
  "Key present in references.json (doi 10.2307/1913778, verified_by crossref); the page cites it at grade D with no locator or result."))
R.append(row("E3b-refs-kahneman1979", "2.1 citations", "references/references.json kahneman1979prospect; course/modules/E/E3/L06.html data-cite",
  "Key present (doi 10.2307/1914185, verified_by crossref); grade D, no locator or result."))
R.append(row("E3b-notation", "2.13 notation", "notation/notation.json; L04-L06 pages",
  "Macros used are only \\E, \\Prob, \\indic, \\R (all registered); standard TeX (\\tfrac, \\Bigl, \\blacksquare) is not a registry macro. No registered program symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears on the three pages."))
R.append(row("E3b-DAG-closure", "2.14 DAG", "course/modules/E/E3/L04.html:37, L05.html:37, L06.html:37",
  "Uses lines name only L01-L03, M1, M2, M4; check_dag PASS. Cross-references to L01 Definition 1.1 (finite lottery), L02 (certainty equivalent), L07 (probability weighting), L08 (timing convention, 'four preference models') were read in the target pages."))
R.append(row("E3b-hours-and-template", "hours arithmetic", "course/modules/E/E3/L04.html:34, L05.html:34, L06.html:34; index.html hub chips",
  "Each page states '7 study hours'; hub index.html shows 'L04 · 7 h', 'L05 · 7 h', 'L06 · 7 h'. No inconsistency."))
R.append(row("E3b-L04-A1-A2-lemmas", "2.2 math", "course/modules/E/E3/L04.html:55-126",
  "Read every line. Definition 1.1, Lemma 1.2 (shortfall identity, checked: E(t-X)^+ = integral of P(X<=s) ds), Lemma 1.6 proof, Prop 1.8 and P2 re-derived. No gap found."))
R.append(row("E3b-L04-thm1.5", "2.2 math", "course/modules/E/E3/L04.html:88-99",
  "Only-if identity E u(X)-E u(Y) = sum_j d_j (F_Y(s_{j-1})-F_X(s_{j-1})) re-derived; if-direction indicator witness checked."))
R.append(row("E3b-L04-thm2.3", "2.2 math", "course/modules/E/E3/L04.html:133-160",
  "Re-derived: chord slopes of min(s-t,0) are 1, [0,1], 0 (concave); L representation with b1 = sigma_{m-1}, c_j = sigma_{j-1}-sigma_j >= 0; sign of I_Y - I_X term correct. Remark 2.4 and R3 consistent."))
R.append(row("E3b-L04-ex2.5-2.6-1.7", "2.3 numbers", "course/modules/E/E3/L04.html:112-173 (Examples 1.7, 2.5, 2.6)",
  "Recomputed all integrated values: X: 0,0,500,1000,2000; Y: 0,250,500,1250,2000 (Ex 2.5); Ex 1.7 F vectors and means 3000/3500; Ex 2.6 I_Y=(t-3000)^+ <= I_X. Match lab printed values exactly."))
R.append(row("E3b-L04-problems-M-P-E-R", "2.2 math/prose", "course/modules/E/E3/L04.html:521-616",
  "M1 means 2500/2000; M2 I_Y(3000)=500; M3 I_X(3000)=500; E1 I_Y(4000)=500 for pair B; E2 counts 3+10+1+10=24; R1-R3 re-derived (R3 b1 = sigma_{m-1}, I_X(s_m)=s_m-EX). No error."))
R.append(row("E3b-L04-lab-hypothesis-and-counts", "2.5 labs", "course/modules/E/E3/L04.html:438-506; tests/labs/E3/lab-E3-L04-1.py",
  "Read the code: 24 pairs (8 equal-mean), tolerance 1e-12, indicator/min/CRRA witnesses, exact Fractions. Printed counts 3/10/1/10, 24 of 24, 8 of 8, pairs 16 and 19 SOSD no ranking all match the output (twin_L04.out). Docstring claims (1/12 and 1/48 multiples) verified by code: match_mean moves in steps of 1/48."))
R.append(row("E3b-L04-named-pairs-hypothesis", "2.5 labs", "course/modules/E/E3/L04.html:178 (docstring); :485 (interpretation)",
  "Named pair lines verified: A spread no FOSD/SOSD X dominates Y; B shift Y dominates X first order; C equal means SOSD Y dominates X. Integrated CDF prints match Examples 2.5 and 1.7."))
R.append(row("E3b-L04-grades-and-prose", "2.2 prose", "course/modules/E/E3/L04.html:51, 490-493, 510, 611, 626-631",
  "Scope words checked: 'only' (A2), 'every', 'does not use monotonicity' (Remark 2.4 consistent with proof). Prose counts 10 of 24, 2 of 8 match lab. The misconception paragraph fix (closing </p>) is well-formed."))
R.append(row("E3b-L04-cards", "2.4 cards", "course/modules/E/E3/cards.json E3-c056..E3-c077 (L04 cards)",
  "Each L04 card matches the current lesson text and carries its theorem/lab grade (C for lab counts, T for proved items); numbers in cards appear in the lesson."))
R.append(row("E3b-L05-def-thm1.3-cor1.4", "2.2 math", "course/modules/E/E3/L05.html:63-96",
  "Re-derived Theorem 1.3(a),(b) sign handling for a>0 and a<0; Corollary 1.4 proof for sure consumption k=CE1."))
R.append(row("E3b-L05-prop2.2", "2.2 math", "course/modules/E/E3/L05.html:110-120",
  "MRS = (1-beta)/beta (c0/c1)^(a-1) = (1-beta)/beta (c1/c0)^(1/psi); EIS = psi. Re-derived; lab closed-form check True."))
R.append(row("E3b-L05-remark1.5-mean-regression", "2.2 numbers", "course/modules/E/E3/L05.html:100",
  "Example lotteries {1,4} and {2,3}, mean 5/2 each, CE at gamma=2 = 8/5 and 12/5 (E c^-1 = 5/8 and 5/12). Recomputed; matches. Added example is correct."))
R.append(row("E3b-L05-remark3.4-slope-sign", "2.2 math", "course/modules/E/E3/L05.html:157",
  "MRS_U = (1-beta)/beta (c1/c0)^gamma; agreement iff r^gamma = r^(1/psi) with r != 1 iff gamma = 1/psi; diagonal slope -(1-beta)/beta. Re-derived. Lab pair (4,4) vs (1,10) at psi=2 confirmed by output."))
R.append(row("E3b-L05-remark2.3-gamma-claim", "2.5 labs / prose", "course/modules/E/E3/L05.html:124; tests/labs/E3/lab-E3-L05-1.py:67-84 (eis_numeric fixes gamma = 2.0 in mrs_numeric)",
  "Delta fix re-verified: 'estimates the EIS ... at gamma = 2 only' matches the code (ez_value(..., 2.0, psi) inside mrs_numeric). Previous FAIL resolved."))
R.append(row("E3b-L05-cards-c078-c091", "2.4 cards", "course/modules/E/E3/cards.json E3-c078..E3-c091",
  "Each card matches the current lesson; theorem cards graded T; statements about psi=1/gamma carry A1-A4."))
R.append(row("E3b-L05-cards-c092-c093-grade", "2.4 cards", "course/modules/E/E3/cards.json:627-638 (E3-c092, E3-c093)",
  "Delta fix re-verified: E3-c093 (exact tree values) now grade C with basis 'Lab 1 (exact Fraction arithmetic on one tree); Problem E1 by hand', matching the lesson's C grade on that result. E3-c092 is a T theorem card. Previous FAIL resolved."))
R.append(row("E3b-L05-cards-c094-c097", "2.4 cards", "course/modules/E/E3/cards.json:642-660 (E3-c094..E3-c097)",
  "c094 EIS values 0.5000/2.0000/0.2500 match twin output; c095 U and V0 values match; c096 CE1 2.2500/1.6000/1.3720 recomputed by hand (1.5^2, sqrt(32/17)). c097 D grade matches the page."))
R.append(row("E3b-L05-lab-numbers", "2.5 labs", "course/modules/E/E3/L05.html:162, 328-350, 351, 500-502; twin_L05.out",
  "Exact tree: V0=80/49, U=-49/80, CE1=8/5, sure plan value 80/49 (hand-checked), theta=1; ranking True; EIS 0.5000/2.0000/0.2500; psi=1 refused. All match twin output."))
R.append(row("E3b-L05-problems", "2.2 math", "course/modules/E/E3/L05.html:389-483",
  "M2 V0=3/2 (checked), M3 theta=-2, P1 revised wording, P2, P3, R1-R3, E2 (V0=160/71, CE1=16/7) recomputed; all correct. R2 revised 'given beta' wording is correct."))
R.append(row("E3b-L05-quiz-numeric", "2.2 numbers", "course/modules/E/E3/L05.html:567-568 (item 8)",
  "Delta fix re-verified: data-tolerance 0.0000005 now admits |80/49 - 1.632653| = 6.1e-8. Six-decimal prompt consistent. Previous FAIL resolved."))
R.append(row("E3b-L05-quiz-mc", "2.2 prose", "course/modules/E/E3/L05.html:508-605",
  "MC items and explanations checked: CE1 = 2, theta=-2, psi=1/gamma restriction, Corollary 3.3, EIS definition, CE=8/5 corollary, lab (4,4)/(1,10) values 4.0000 and 4.3311 recomputed."))
R.append(row("E3b-L05-canon-misconceptions", "2.2 prose", "course/modules/E/E3/L05.html:354-381",
  "Canon bullets: 'Four limits' (four bullets), 'Lesson L08 timing convention' verified in L08 text, misconception claims match Corollary 3.3, Remark 2.3 and Corollary 1.4."))
R.append(row("E3b-L05-key-results", "2.2 prose", "course/modules/E/E3/L05.html:494-502",
  "Each key result matches its theorem/remark, grade T or C as labelled; lab-based rows are graded C."))
R.append(row("E3b-L05-references", "2.1 citations", "course/modules/E/E3/L05.html:607-611",
  "Grade D, no locator, no result attributed; consistent with references.json entry."))
R.append(row("E3b-L06-def-prop1.4", "2.2 math", "course/modules/E/E3/L06.html:55-90",
  "Re-derived v' and v'' on both sides (lambda delta (1-delta)(-x)^(delta-2) > 0); continuity at 0; concave on [0,inf), convex on (-inf,0]."))
R.append(row("E3b-L06-prop2.1-2.2-ex2.3", "2.2 numbers", "course/modules/E/E3/L06.html:96-119",
  "Example 2.3: EV 200, lambda* 5/3, W = 200/50/-100 re-derived; Prop 2.2 with alpha=delta=1/2 gives lambda* = sqrt(5/3) = 1.2910 and W(2) = -8.6835 (recomputed)."))
R.append(row("E3b-L06-remark2.4-2.5", "2.2 numbers", "course/modules/E/E3/L06.html:122-129",
  "Remark 2.5: combined 700-300 lambda, separate 1000-600 lambda; at lambda=2: 100 and -200 (recomputed). Remark 2.4 CE sign claim re-derived (v strictly increasing, v(0)=0, onto R)."))
R.append(row("E3b-L06-remark3.1", "2.2 math", "course/modules/E/E3/L06.html:282-288",
  "Remark 3.1: Props 1.4, 2.1, 2.2 use only lambda > 0 (verified in proofs)."))
R.append(row("E3b-L06-remark3.2", "2.2 numbers", "course/modules/E/E3/L06.html:286-288",
  "Re-derived lambda_R: EV=400/3 for p=1/3, g=1000, l=300; ratio 2; lambda_R = (1/2) sqrt 2 = 0.7071; alpha=1 gives lambda_R=1; example gamble gives 1/2 * 800^alpha (1-lambda)."))
R.append(row("E3b-L06-remark3.2-reference-scope", "2.4 prose", "course/modules/E/E3/L06.html:287 vs lines 296, 410-412, 495-501",
  "Claim 'the reference point of this remark is used only here, in Section 4, in Problem R2 and in quiz item 7' matches: Section 4 bullet 2, R2 (line ~ 410-412) and quiz item 7 (the reference-point question)."))
R.append(row("E3b-L06-lab-numbers", "2.5 labs", "course/modules/E/E3/L06.html:133, 257-274, 275, 307-315, 438; twin_L06.out",
  "Twin output: lam* 5/3; W 200/50/-100; combined 100; separate -200; power threshold 1.2910; W(2) -8.6835; concave/convex/increasing True; ratio 2 True. Page hypothesis, interpretation and expected block match the output."))
R.append(row("E3b-L06-problems", "2.2 math", "course/modules/E/E3/L06.html:326-416",
  "M1 lambda*=3/2 and W(2)=-100; M2 EV 0, W -50; M3 v(16)=4, v(-16)=-8, ratio 2; P1-P3; E1-E3 (E3 signs differ on (5/3, 7/3)); R1-R3 (R3 non-additivity 2 + (-2) = 0 vs v(1)=1) re-derived."))
R.append(row("E3b-L06-quiz-numeric", "2.2 numbers", "course/modules/E/E3/L06.html:466-507",
  "Quiz numeric answers 5/3 = 1.6667, W=-100, sqrt(5/3)=1.2910 and the Example 2.3 integrated values recomputed; correct."))
R.append(row("E3b-L06-cards", "2.4 cards", "course/modules/E/E3/cards.json E3-c098..E3-c117",
  "Each card matches current text. Duplicate card E3-c115 (first block of Lab 1, same content as E3-c106) was removed in this delta; no duplicate fronts remain (checked). E3-c106, c116, c117 graded C with lab basis; c113 value sqrt(2)/2 correct."))
R.append(row("E3b-L06-canon-breaks-misconceptions", "2.2 prose", "course/modules/E/E3/L06.html:291-318",
  "Four limits and three misconceptions checked: 'λ > 1 is not used by Sections 1-2' supported by Remark 3.1; bundle sign claim supported by Remark 2.5 numbers."))
R.append(row("E3b-L06-prose-claims", "2.2 prose", "course/modules/E/E3/L06.html (whole page); L05.html (whole page)",
  "Read all text. Process words absent (grep of extracted text). Scope words checked; no unsupported 'all/every' claim found beyond the stated finite grids and Propositions 1.4, 2.1, 2.2."))
R.append(row("E3b-L06-key-results", "2.2 prose", "course/modules/E/E3/L06.html:431-438",
  "Key results: T/C grades match proofs and lab output; grid results marked C with finite-grid basis."))
R.append(row("E3b-delta-round5", "delta", "b276325..04626e9 for course/modules/E/E3/L04-L06.html, tests/labs/E3/lab-E3-L04-1.py, cards.json",
  "Every hunk in these files read; each changed claim re-verified (L04 proof and lab docstring/interpretation, L05 Remark 1.5, 2.3, two-dates bullet, P1, R2, quiz tolerance, L06 hypothesis and references, cards c093/c094/c106/c115-removal)."))
R.append(row("E3b-previous-round-rows", "carry check", "/Users/billyribeiro/.fanout/frags/C-E3-b.round4.json",
  "Round-4 rows re-run from scratch in round 5 (no carries). The three round-4 FAIL rows (E3b-L05-remark2.3-gamma-claim, E3b-L05-cards-c092-c093-grade, E3b-L05-quiz-numeric) now verified PASS. Mutation testing not applicable to lesson pages and lab twins."))
frag = {
 "unit": "E3", "slice": "E3-b", "round": 5,
 "verifier": "Haiku independent verifier, unit E3 slice b, round 5; did not build E3",
 "pin": "04626e9", "base": "b276325 (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/C-E3-b.round4.json)",
 "checkout": root, "scratch": S + "/",
 "verified_at": "2026-10-28T12:00:00+00:00", "verdict": "PASS",
 "rows": R, "mutants": [],
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Mutation testing not applicable: slice b is lesson pages and lab twins only (mutation testing applies to project graders).",
  "Not checked: live Crossref / verify_refs --unit run (only offline integrity run); pytest full suite and render_curriculum gate (no generator input touched by slice); Pyodide-vs-CPython output identity beyond page_smoke PASS; hub course/modules/E/E3/index.html E3 total of 70 hours was not re-derived (outside slice), only the L04-L06 7 h entries were checked.",
  "Lab EIS values are finite-difference outputs checked to 4 decimals against psi; labs are SIMULATED or exact as labelled."
 ],
 "summary": "E3-b round 5: 60 rows, 60 PASS, 0 non-PASS. Round-4 FAIL rows fixed and re-verified (L05 remark 2.3 gamma scope, c093 grade, quiz tolerance). No defects found in L04-L06 prose, math, labs or cards on pin 04626e9."
}
json.dump(frag, open("ledgers/E3/E3-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(R))
