"""Write the round-1 fragment for M4 slice b (L05-L07 and twins) and validate it with tools/ledger.py."""
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/tmp/verifyB1-M4-b")
S = "M4-b-r1/"
SC = "ledgers/M4/scripts/M4-b-r1/"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- mechanical gates
row("M4b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit M4 --page L05|L06|L07", "PASS",
    "Observed output: 'check_pages M4 L05: PASS', 'check_pages M4 L06: PASS', 'check_pages M4 L07: PASS'.")
row("M4b-cmd-check_dag", "DAG", "tools/check_dag.py --unit M4", "PASS",
    "Observed output: 'check_dag M4: PASS'. Each of correlation, covariance-matrix, normal-distribution, student-t-distribution, "
    "moment-generating-function, characteristic-function is defined once (grep of <dfn data-concept> across L01-L10: no duplicates).")
row("M4b-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit M4 --page L05 / L06 / L07", "PASS",
    "Observed: 'run_labs M4: PASS (1/1)' three times.")
row("M4b-lab-isolated", "2.5-lab", "tests/labs/M4/lab-M4-L05-1.py, lab-M4-L06-1.py, lab-M4-L07-1.py", "PASS",
    "python -I -W error <twin>: exit 0 for all three, stderr empty; wall time native 0.03 s, 0.48 s, 0.04 s. "
    "Output saved in /tmp/M4-v/b/ (lab_*.out).")
row("M4b-lab-embed", "2.5-lab", "course/modules/M/M4/L05.html, L06.html, L07.html <pre> code and <pre class=expected>",
    "PASS", f"{SC}embed_check.py: embedded code equals the twin (True x3); embedded expected output equals a fresh run "
    "stdout (True x3, byte-identical after strip).")
row("M4b-lab-page_smoke", "2.9-structure", "tools/page_smoke.py --unit M4 --pages L05 L06 L07 (full run, sweep included)",
    "PASS", "Observed: 'page_smoke modules/M/M4/L05.html: PASS', L06: PASS, L07: PASS, 'page_smoke M4: PASS', rc=0. "
    "Pyodide lab times: L05 0.0 s, L06 1.2 s (boot 1.1 s), L07 0.1 s, all under 10 s.")
row("M4b-lint-mypy", "2.9-structure", "ruff check / ruff format --check / mypy --no-incremental on the three twins", "PASS",
    "ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy: 'Success: no issues found in 3 source files'.")
row("M4b-refs-offline", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    "Observed: 'offline integrity: 560 entries, 0 problems', rc=0.")
row("M4b-refs-live-M4", "2.1-citations", "tools/verify_refs.py --unit M4 (live)", "PASS",
    "Observed: 'live re-verification of M4: 1 of 560 entries, 0 problems', rc=0. The L05-L07 pages cite no key "
    "('This lesson cites no outside source' in each references section; cards carry no cite field).")

# ---- numbers
row("M4b-num-L05-ratio", "2.2-numbers", "course/modules/M/M4/L05.html Part C interpretation and E3", "PASS",
    f"{SC}recompute.py: 0.0010539032/0.0002187758 = 4.817275, shown as 4.8173 and 4.82 (two places). Largest k=3, smallest k=7 match the printed values.")
row("M4b-num-L05-errors", "2.2-numbers", "L05.html interpretation, E1, E2, Part B", "PASS",
    "Recomputed from printed digits: sigma_11 entry error at n=20000 (0.00039491-0.0004)/0.0004 = -1.2725%, shown -1.27%; "
    "n=100 errors 0.0000151, 0.00002824, 0.00016257 (the (2,2) entry is largest); sample correlation error 0.592936-0.6 = -0.007064.")
row("M4b-num-L06-relerr", "2.2-numbers", "L06.html interpretation, E1, E2, E3, misconception 1", "PASS",
    "Unrounded recomputation with the twin's own functions: nu=5 variance 1.6691144893, relative error 0.00146869 -> printed 0.001469 "
    "(the lab value is the unrounded one, E1 says so and is right). From printed digits (1.669114-1.666667)/1.666667 = 0.001468, "
    "a one-unit difference that E1 attributes to the printing step. nu=10 relative error -0.0077402 -> -0.007740. "
    "E2 ratio 0.007740/0.001469 = 5.27. E3: (4.997415-5)/5 = -0.000517 = -0.0517%.")
row("M4b-num-L07-values", "2.2-numbers", "L07.html Part B interpretation, misconception, E1, E2, E3, quiz q9", "PASS",
    f"{SC}recompute.py: |phi(1)|^2 = 0.625 + 0.375 cos(2) = 0.4689449363, sqrt 0.6847955434 (printed 0.68479554); "
    "real part 0.25+0.75 cos 2 = -0.0621101274 (quiz tolerance accepts -0.0621101); E1 difference -0.062124 - (-0.062110) = -1.4e-5; "
    "E2 7.11e-13/244.69193226 = 2.9e-15; e^3 = 20.085537 -> 20.0855 (M2, quiz). "
    "sqrt(2/pi) = 0.7978845608 -> 0.7978846 (L06 quiz). e^(1/2) = 1.6487212707 -> 1.6487213 (L07 quiz).")
row("M4b-num-L07-simpson-claim", "2.2-numbers", "L07.html E2 solution: error 'not from the quadrature step size'", "PASS",
    f"{SC}simpson.py: Simpson error at t=2 is 8.5e-14 with 200 intervals, 4.3e-13 with 2000, 7.1e-13 with 20000; "
    "the error does not fall as the grid is refined, so it is not quadrature error. The page does not show this run; the claim is true.")

# ---- 2.4 math
row("M4b-math-L05-s1", "2.4-mathematics", "L05.html Prop 1.1, 1.2, 1.5, 1.6, Example 1.7, Remark 1.8", "PASS",
    "Re-derived each proof: bilinearity and symmetry; Cov(aX+b,cY+d)=ac Cov; Cauchy-Schwarz via A=Var(Y), B=2Cov, C=Var(X) and B^2<=4AC, "
    "the A=0 case handled by support positivity; rho invariant under a,c>0; Remark 1.8: Cov=0, Var(X)=2/3, Var(Y)=2/9 (checked by enumeration).")
row("M4b-math-L05-s2", "2.4-mathematics", "L05.html Prop 2.3, 2.4, Example 2.5", "PASS",
    "Prop 2.3 proof and Prop 2.4 proof re-derived. Example 2.5: Var(X2)=S2^2(rho^2+1-rho^2)=S2^2 and Cov(X1,X2)=rho S1 S2 hold "
    "under the example's stated assumption (Var Z_i=1, Cov(Z1,Z2)=0); the example labels the assumption as unproved (its own sentence).")
row("M4b-math-L06-s1", "2.4-mathematics", "L06.html Prop 1.2-1.5 and Remark 2.2 usage", "PASS",
    "Gaussian integral: polar-coordinate computation re-derived (r-integral = 1, times 2pi). Prop 1.3 substitution re-derived. "
    "Prop 1.5: integration by parts, boundary term z phi(z) -> 0, second moment 1. Hypotheses stated.")
row("M4b-math-L06-s2", "2.4-mathematics", "L06.html Lemma 2.3, Prop 2.4", "PASS",
    "Lemma 2.3: E[e^{-sZ^2}]=(1+2s)^{-1/2} re-derived; E[1/W]=integral (1+2s)^{-nu/2} ds; W>0 a.s. since P(Z1=0)=0. "
    "Prop 2.4: nu>2 antiderivative gives 1/(nu-2); nu<=2 comparison gives infinity.")
row("M4b-math-L06-prop26", "2.4-mathematics", "L06.html Proposition 2.6 (second clause), Key-results row, Misconception 2",
    "FAIL",
    "Proof shows E[T^2]=nu E[1/W]=infinity for nu<=2, then the statement says 'so the variance is infinite'. Var(T)=E[T^2]-(E T)^2 "
    "needs E|T| finite. Witness nu=1: T is standard Cauchy, E|T| = E|Z| E[1/|Z'|] = infinity, so E[T] does not exist and the page's "
    "variance identity fails. Only nu=2 has E[T] = 0 with E[T^2] infinite, so 'variance infinite' is established for nu=2 alone "
    "(via E|T| = E|Z| E[V] finite there).",
    "State the nu<=2 clause as E[T^2] = infinity; say the variance is infinite only for nu=2 (mean exists), and that for nu=1 the mean "
    "is undefined. Same fix for cards M4-c093, M4-c096 and the key-results row.")
row("M4b-math-L07-s1", "2.4-mathematics", "L07.html Prop 1.2-1.4, 2.4, 2.5, Problems R1-R3", "PASS",
    "Prop 1.3: exp(sz - z^2/2) <= exp(s^2 - z^2/4) via (z/2 - s)^2>=0 re-derived; completing the square re-derived. "
    "Prop 1.4: exponent sign change at t=1/2 re-derived. Prop 2.5 modulus identity re-derived numerically (0.46894494 vs 0.4689449363). "
    "R1 identity 1+2pq(cos t - 1) re-derived. R2 derivative p e^t > 0.")
row("M4b-math-L07-prop23", "2.4-mathematics", "L07.html Prop 2.3 statement and proof",
    "PASS", "Statement covers finitely many values or a density, and the proof (|E[Y]|<=E|Y| for |Y|=1) is valid for these classes; "
    "the scope overreach in the introduction is a separate row.")

# ---- problems and quizzes
row("M4b-problems-L05", "2.4-mathematics", "L05.html problems M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "Each solution re-derived: M1 rho=1; M2 w'Sw=7, rho=1/2; M3 Var=1.2; R1 Cov=0, Var(Y)=2/9; R3 diagonal-zero argument; "
    "E1-E3 values match printed Part A-C digits.")
row("M4b-problems-L06", "2.4-mathematics", "L06.html problems M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "M1 P(X<=3)=1/2, E X^2 = 13; M2 variances 3, 2, 5/3; M3 z=1; R1 E|Z|=sqrt(2/pi); R2 E[W/nu]=1; R3 T'=sign(Z), Var 1; "
    "E1 0.001468 from digits (lab value 0.001469); E2 5.27; E3 -0.0517%.")
row("M4b-problems-L07", "2.4-mathematics", "L07.html problems M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "M1 (1+e^{2t})/2 and (1+e^{2it})/2; M2 e^3; M3 phi(pi/2)=0; P3 product rule for finite-valued independent variables re-derived; "
    "R3 phi=cos t re-derived; E1-E3 match printed digits.")
row("M4b-quiz-L05-L07", "2.4-mathematics", "L05 (10), L06 (9), L07 (9) quiz items: data-answer and explain blocks (28 items)", "PASS",
    "Every data-answer re-derived: L05 1, 7, 0.5, 1.2, 4; L06 2, 5/3, 0.7978846, 1/2, 5; L07 1.6487213, 1, 1, 20.0855, 1, -0.0621101 "
    "(tolerances accept the printed digits). Correct options checked against the lesson propositions.")

# ---- cards
row("M4b-cards-L05", "2.7-cards", "course/modules/M/M4/cards.json M4-c067..c083", "PASS",
    "17 cards, each checked against its lesson statement. Grade C cards c082, c083 name Lab 1 Part A/B (SIMULATED) and their numbers "
    "(0.00002223, 0.00016257, 0.592936, -0.007064) appear in L05.html.")
row("M4b-cards-L06", "2.7-cards", "cards.json M4-c084..c098", "FAIL",
    "Cards c093 ('If nu <= 2, E[T^2] is infinite, so the variance is infinite') and c096 ('For nu <= 2 ... the variance is infinite') "
    "repeat the Proposition 2.6 overclaim (see M4b-math-L06-prop26); the other 13 cards match. c098 numbers 1.669114, 1.666667, 0.001469 appear in L06.html.",
    "Make c093 and c096 agree with the corrected Proposition 2.6 (E[T^2] infinite; variance infinite only for nu=2).")
row("M4b-cards-L07", "2.7-cards", "cards.json M4-c099..c113", "PASS",
    "15 cards checked against L07 text. c112 (7.11e-13 at t=2, 244.69193226) and c113 (-0.062124, -0.062110) appear in L07.html; "
    "non-T cards carry basis naming the lab.")
row("M4b-cards-dup", "2.7-cards", "cards.json, all 163 cards", "PASS",
    "Scripted scan: no duplicate ids, no duplicate fronts, no duplicate backs.")

# ---- DAG and definitions
row("M4b-dag-forward-normal", "DAG", "course/modules/M/M4/L05.html Example 2.5 (line 160) and Lab 1 hypothesis (line 165)", "FAIL",
    "L05 uses 'standard normal' (L06 concept normal-distribution, defined at L06 Definition 1.1) before L06: Example 2.5 says "
    "'Let Z1 and Z2 be independent standard normal draws, which L06 defines', and the lab hypothesis says 'the standard normal draws come "
    "from random.gauss, whose law L06 defines'. BUILDER_RULES §1.10 bans a concept used before it is introduced; check_dag passes "
    "because there is no link. grep: 'standard normal' first occurs in L05 (L01-L04 have none).",
    "Rewrite Example 2.5 with independent variables Z1, Z2 with mean 0 and variance 1 and Cov 0 (the assumption the example already "
    "states), and drop 'standard normal' and the 'L06 defines' pointer from L05, or move the normal definition to L05.")
row("M4b-dag-links", "DAG", "L05-L07 concept links (data-concept)", "PASS",
    "Links point to earlier definitions only: L05 to L02 (expectation, variance), L04 (independence); L06 to L01, L02, L04, "
    "concepts.html (definite/multiple integral, M2); L07 to L01, L02, L04, L06 normal-distribution, concepts.html (M1 exponential, M2 integral).")

# ---- lab twin statements
row("M4b-lab-L05-docstring", "2.5-lab", "tests/labs/M4/lab-M4-L05-1.py line 3 (docstring) and L05.html Lab 1 hypothesis (line 165) and code (line 168)",
    "FAIL",
    "Docstring and hypothesis say 'Two standard normal streams come from random.Random(20260501).gauss' / 'come from a seeded generator'. "
    "The code (draws(), line 30) makes ONE generator rng = random.Random(seed) and takes z1 then z2 from it for each observation. "
    "Two streams is a claim about the code that is false.",
    "Write: 'One seeded stream, random.Random(20260501).gauss, supplies Z1 and Z2 in turn for each observation.' Apply to the twin "
    "docstring and to the hypothesis paragraph; run tools/embed_labs.py --refresh if the twin changes.")
row("M4b-lab-L06-docstring-seed", "2.5-lab", "tests/labs/M4/lab-M4-L06-1.py line 5 (docstring), code lines 47 and 58; L06.html line 178",
    "FAIL",
    "Docstring says 'The generator is random.Random(20260602)'. The code uses random.Random(SEED + nu) for Part A "
    "(20260607 for nu=5, 20260612 for nu=10) and random.Random(SEED + 500) = random.Random(20261102) for Part B. "
    "Printed numbers are reproducible, but the stated generator is not the one used.",
    "Replace with: 'Part A uses random.Random(20260602 + nu) for nu = 5 and 10; Part B uses random.Random(20261102).'")
row("M4b-lab-L06-nu2-not-run", "2.5-lab", "L06.html line 269 (Lab 1 interpretation) vs twin line 74", "FAIL",
    "Interpretation: 'The lab does not run the case nu <= 2.' The twin's main() calls t_variance(2) inside try/except ValueError "
    "(line 74) and prints 'nu 2 raises ValueError ...'. The guard IS run at nu=2; only the variance branch for nu <= 2 is not simulated.",
    "Replace with: 'The lab calls the guard at nu = 2 and does not simulate any law with nu <= 2.'")
row("M4b-lab-L05-L07-printed-claims", "2.5-lab", "L05.html Part A-C interpretation; L06.html Part A-C; L07.html Part A-C",
    "PASS", "Every printed value quoted in the interpretations and misconceptions matches a fresh run (checked against lab_*.out).")

# ---- prose and claims
row("M4b-scope-L06-simplest", "2.9-structure", "L06.html line 52 (why-it-matters)", "FAIL",
    "'the Student-t distribution is the simplest symmetric alternative to it that has a different tail shape': a superlative with no "
    "computation or witness on the page (scope rule, plan 'Scope words need a computation').",
    "Delete 'simplest' (for example: 'a symmetric alternative to it with a different tail shape').")
row("M4b-claim-L06-not-settle", "2.4-mathematics", "L06.html line 276 (Where the canon breaks, bullet 2)", "FAIL",
    "'a sample variance from such a law does not settle': asserted, not proved (Proposition 2.6 gives only E[T^2] = infinity), and the "
    "lab runs only nu = 5 and 10. Ungraded claim.",
    "Either prove or label the claim as an unproved remark, or delete the words 'does not settle'.")
row("M4b-remark22-unproved", "2.4-mathematics", "L06.html line 119 (Remark 2.2) and proof of Prop 2.6 (line 159)", "FAIL",
    "Remark 2.2 says 'Functions of independent variables are independent' with no proof, grade or citation; Proposition 2.6's proof "
    "uses it for V=(nu/W)^{1/2} independent of Z. The fact is immediate from the remark's own definition (preimages of Borel sets are sets), "
    "but the page does not give that step, so the T grade of Prop 2.6 rests on an unproved sentence. Low severity.",
    "Add the one-line proof: P(f(X) in A, g(Y) in B) = P(X in f^-1 A, Y in g^-1 B) = P(f(X) in A) P(g(Y) in B).")
row("M4b-scope-L07-always", "2.9-structure", "L07.html line 52 (why-it-matters) vs Proposition 2.3 (line 123)", "FAIL",
    "Intro says the characteristic function 'always exists' and that it 'shows that the characteristic function of any variable has modulus "
    "at most one'. Proposition 2.3 covers only finitely many values or a density. 'always' and 'any' need a computation or the hypothesis.",
    "Write 'for a variable with finitely many values or a density' in the introduction, or extend the proposition with its proof.")
row("M4b-scope-L07-product", "2.4-mathematics", "L07.html line 52 (why-it-matters)", "FAIL",
    "Intro: 'It also shows that the moment-generating function of a sum of independent variables is the product'. Problem P3 (and "
    "the key-results row) prove this only for independent variables with finitely many values.",
    "Add 'with finitely many values' to the introduction sentence.")
row("M4b-num-L07-digits-claim", "2.2-numbers", "L07.html line 377 (Problem E3 solution, modulus at t = 1)", "FAIL",
    "'agrees with the printed 0.68479554 to the six places shown': the printed value shows eight places and the agreement is to seven "
    "(0.6847955 vs 0.68479554). Wording misstates the displayed precision.",
    "Replace 'six places shown' with 'seven places'.")
row("M4b-undefined-simpson", "2.9-structure", "L07.html line 165 (hypothesis) and line 173 (twin docstring)", "FAIL",
    "'Simpson's rule' is used at first mention without a definition in the prose; its weights 1, 4, 2 appear only in twin code. Plan §5: "
    "undeclared terms are defined inline by their formula at first use.",
    "Add one sentence with the formula: h/3 times the sum of weights 1, 4, 2, ..., 4, 1 times the values.")
row("M4b-hub-L07-identify", "2.9-structure", "course/modules/M/M4/index.html line 147 (hub Lessons paragraph)", "FAIL",
    "Hub says Lessons 6 to 8 cover 'the transforms that identify a law'. L07 says the opposite of what is shown: 'Whether either function "
    "determines the law is not shown here' (L07 canon-breaks bullet 3), and no result uses uniqueness.",
    "Change 'the transforms that identify a law' to 'the transforms that summarize a law'.")
row("M4b-hub-L06-card", "2.9-structure", "course/modules/M/M4/index.html line 154 (L06 card body)", "FAIL",
    "'the Student-t as a normal over an independent chi-square root': 'chi-square root' is not a defined object; L06 Definition 2.1 is a chi-square variable.",
    "Write 'an independent chi-square variable'.")
row("M4b-prose-banned-process", "2.9-structure", "L05-L07 visible prose", "PASS",
    "Scan: no process words (build, builder, round, verifier, REQUEST); no bibliographic locators (no theorem numbers from outside, no page "
    "numbers); banned phrases pass check_pages. 'through' appears only inside formulas or as list ellipsis in cards.")
row("M4b-hours", "hours", "L05-L07 data-hours; index.html data-hours-lessons=90, lesson text 'Ten lessons of nine study hours'", "PASS",
    "Each page has data-hours=9 and 'M4 · Lesson n of 10 · 9 study hours'. 10 x 9 = 90 = data-hours-lessons. No pace claim checked (architect ruling).")
row("M4b-mutants-na", "2.5-lab", "lab twins L05-L07", "PASS",
    "Architect ruling: lab twins are demonstrations and mutation testing applies to project graders only. No mutants written for this slice.")
row("M4b-hub-DAG-note", "DAG", "L05 why-it-matters names 'multivariate normal distribution' (L08 concept)", "PASS",
    "Roadmap mention, not a use: the sentence says L08 defines it. Recorded for the record; not a defect under BUILDER_RULES §1.10.")

fragment = {
    "unit": "M4",
    "slice": "M4-b",
    "round": 1,
    "verifier": "independent round-1 verifier for M4 slice b (L05-L07 and their lab twins); did not build M4; Haiku",
    "pin": "c11ae01",
    "base": "none",
    "checkout": "/tmp/verifyB1-M4-b (detached at c11ae01; .venv symlinked)",
    "scratch": "/tmp/M4-v/b/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 1, first independent verification of M4 slice b. The brief names pin b4590f6; the checkout was given at c11ae01 and was used as pinned.",
        "Not run: the Pyodide run of page_smoke is the real Chromium run from the checkout (done); no separate Pyodide-only run.",
        "Not checked: the M4 project grader and tests/graders alternatives (other slice). Hours: only arithmetic checked, no pace.",
        "Architect Q5 (Blitzstein only, stable-limit claim unproved) does not bear on L05-L07: no locator and no citation in these pages.",
    ],
    "summary": "L05-L07 and twins: all mechanical gates pass and every displayed number re-derives, but 15 rows FAIL: an unproved infinite-variance clause for nu=1 (Prop 2.6, carried to two cards), a forward use of 'standard normal' in L05, two lab docstrings that misstate the code, a lab sentence that contradicts the code, scope overreach in L06 and L07 introductions, one hub overclaim, and minor wording defects.",
}

out = ROOT / "ledgers/M4/M4-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
check = subprocess.run(
    [str(ROOT / ".venv/bin/python"), "-c",
     "import sys,json; sys.path.insert(0,'tools'); import ledger; "
     "print(ledger.validate(json.load(open('ledgers/M4/M4-b.json')), 'M4-b'))"],
    cwd=ROOT, capture_output=True, text=True)
print(check.stdout, check.stderr)
from collections import Counter
print(Counter(r["status"] for r in rows), len(rows))
