"""Build the round-12 fragment ledgers/E4/E4-d.json (slice d, unit E4) from the logs of this round.

Row statuses are written from evidence in ledgers/E4/scripts/E4-d-r12/logs and the round-12 scripts;
the round-11 row ids are all kept (VERIFIER_RULES: keep all row ids).
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LOG = ROOT / "ledgers/E4/scripts/E4-d-r12/logs"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round11.json").read_text())
prev_ids = [r["id"] for r in prev["rows"]]

CARRY = "Carried from round 11 ({files} byte-identical since the previous pin): "

# ---- mutants: gate log (seeds 0-9) + round-12 new mutants
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in (LOG / "mutate_graders_seeds0-9.txt").read_text().splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc, "killed_by": None if status == "SURVIVED" else killed,
                    "status": status})
new_kill = (LOG / "new_mutants_r12_seeds0-9.txt").read_text().splitlines()
for line in new_kill:
    m = re.match(r"^(KILLED|PASS) (\S+): (.*)$", line)
    name = m.group(2)
    doc = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-c",
                          "import ast,sys;print(ast.get_docstring(ast.parse(open(sys.argv[1]).read())))",
                          str(ROOT / "ledgers/E4/mutants" / name)], capture_output=True, text=True).stdout.strip()
    if m.group(1) == "KILLED":
        mutants.append({"name": name, "description": doc, "killed_by": m.group(3).split(" after ")[0],
                        "status": "KILLED"})
    else:
        mutants.append({"name": name, "description": doc, "killed_by": None, "status": "SURVIVED"})
assert len(mutants) == 102, len(mutants)

M = "ledgers/E4/scripts/E4-d-r12/logs/"
rows = {}


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or "see evidence"
    rows[rid] = r


# ---- commands (re-run this round)
row("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/", "PASS",
    f"`.venv/bin/python tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 ({M}check_projects.txt).")
row("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html", "PASS",
    f"`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 ({M}check_pages.txt); its banned-phrase and link checks cover the changed prose.")
row("E4d-cmd-check-dag", "2.9-dag", "course/modules/E/E4/project.html", "PASS",
    f"`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 ({M}check_dag.txt).")
row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    f"`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)', exit 0 ({M}run_labs.txt).")
row("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py", "PASS",
    f"`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({M}run_graders.txt); the starter-fails check is part of the same run.")
row("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html", "PASS",
    f"`tools/page_smoke.py --unit E4 --pages project` alone -> 'in-browser grader: All 46 tests pass on seed 1027666447', 'page_smoke E4: PASS', exit 0 ({M}page_smoke_project.txt).")
row("E4d-cmd-ruff", "gate", "course/modules/E/E4 and tests/labs/E4", "PASS",
    f"`.venv/bin/python -m ruff check course/modules/E/E4 tests/labs/E4` -> 'All checks passed!' (exit 0); `ruff format --check` -> '16 files already formatted' ({M}ruff_check.txt, {M}ruff_format.txt).")
row("E4d-cmd-mypy-workspace", "gate", "tests/labs/E4 and course/modules/E/E4/grader", "PASS",
    f"`.venv/bin/python -m mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files', exit 0 ({M}mypy.txt).")
row("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader", "PASS",
    f"Same mypy run as E4d-cmd-mypy-workspace ({M}mypy.txt).")
row("E4d-cmd-pytest-relevant", "gate", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py", "PASS",
    f"`.venv/bin/python -m pytest -q` on the four files -> all dots, exit 0 ({M}pytest_relevant.txt).")
row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys: muth1961rational, milgrom1982information)", "PASS",
    f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({M}verify_refs_offline.txt). references.json is unchanged between the pins.")
row("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    f"`pytest --collect-only -q test_project.py` in a scratch copy (instance.py, test_project.py, solver.py = reference.py) -> '46 tests collected' ({M}collect.txt). Equals the page's '46 checks' (project.html:320).")

# ---- labs
row("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
    f"`python -I -W error tests/labs/E4/lab-E4-project-1.py` exit 0; page code equals twin line for line (98 lines); expected block equals twin stdout ({M}twin_vs_page.txt, {M}twin_p1.out).")
row("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", "PASS",
    f"Twin runs exit 0 under -I -W error; page code equals twin except line 41, the blank '___' for the return of indifference_gap (allowed completion blank); expected block equals twin stdout ({M}twin_vs_page.txt).")
row("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
    f"Page code equals twin (114 lines); twin under -I -W error exit 0; expected block equals twin stdout; 9 grid rows re-derived by closed form, largest difference 2.134e-13 ({M}rederive_r12.txt).")

# ---- numbers, math, prose (re-derived this round)
row("E4d-num-lab-hypotheses", "2.2-numbers", "course/modules/E/E4/project.html:57, :176, :376", "PASS",
    f"Re-derived in {M}rederive_r12.txt: Lab 1 gap(0+)=+0.053092, gap(1)=-0.080731, root 0.5793752461 = closed form, tau_y=tau_bar=0.18904110, informativeness 0.15898618 = 1-e^(2ac)/2. Lab 2 gap(0+)=+0.037435, gap(1)=-0.071386, root 0.5705226300, informativeness 0.12466375. Lab 3 values 0.5582/0.6978/0.8373, 0.1920/0.1420/0.0889, |gap|<=3.55e-14<1e-13, 484 of 484 box points.")
row("E4d-num-exemplar-table", "2.2-numbers", "course/modules/E/E4/project.html Exemplar B table and passage (:629-641)", "PASS",
    f"Table rows equal the Lab 3 output ({M}twin_vs_page.txt; rederive_r12.txt). Ratios unrounded: lambda(0.625)/lambda(0.5)=1.250000000000, lambda(0.75)/lambda(0.5)=1.500000000001 at cost 0.120. Gaps printed as max 3.55e-14 < 4e-14 (project.html:629).")
row("E4d-num-box-bounds", "2.2-numbers", "course/modules/E/E4/project.html:314; course/modules/E/E4/grader/instance.py:14-17", "PASS",
    "tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836 (Decimal check 0.097623272188, 0.237566783612), tau_y(1) at sigma=0.75 = 0.3076923077; 0 < tau_bar < 0.237567 < 0.30769 < tau_y(1). Printed figures match (project.html:314; instance.py:14-17).")
row("E4d-prose-lede-directional", "2.3-grades", "course/modules/E/E4/project.html:37 (lede)", "PASS",
    "The lede's directional claims (fraction rises with the noise on the interior; informativeness does not depend on the noise) are Proposition 4 and 5 (project.html:295-301); checked by the closed form and by Lab 3 (informativeness constant across noise volumes, fraction proportional to noise at cost 0.120).")
row("E4d-math-lemmas", "2.4-mathematics", "course/modules/E/E4/project.html:265-273 (Lemmas 1-3)", "PASS",
    "Lemma 1: E[exp(-a x(v-p))|F]=exp(-a x(m-p)+a^2 x^2 V/2) gives g(x)=x(m-p)-(a/2)x^2V, x*=(m-p)/(aV), g(x*)=(m-p)^2/(2aV), -a g(x*)=-(m-p)^2/(2V) (hand derivation, checked). Lemma 2: integral equals (V/(V+S))^(1/2) (checked). Lemma 3: law of total variance with p F-measurable (checked).")
row("E4d-math-prop1", "2.4-mathematics", "course/modules/E/E4/project.html:276-283", "PASS",
    "Proposition 1 re-derived: y=p/b_s=s+kappa u, precision of eps+kappa u gives tau_y=lam^2 tau_e^2/(lam^2 tau_e+a^2 sd^2); clearing gives b_s=(lam tau_e+(1-lam)tau_y)/D and -lam tau_e kappa = a (steps 2-3 of the page's proof). Uniqueness via the independence of s and u (step 4). Numerically the oracle fixed-point agrees (E4d-grader tests).")
row("E4d-math-prop2", "2.4-mathematics", "course/modules/E/E4/project.html:285-287", "PASS",
    "Cov(v,p)=b_s/tau_v, Var(p)=b_s^2(1/tau_v+1/tau_y): Corr^2 = tau_y/(tau_v+tau_y) (re-derived). At lam=0, b_s=0 and p=-a u/tau_v, Corr=0 (re-derived).")
row("E4d-math-prop3", "2.4-mathematics", "course/modules/E/E4/project.html:288-293", "PASS",
    "E[U_I]=-e^{ac}(V_I/Omega)^{1/2} and E[U_U]=-(V_U/Omega)^{1/2} via Lemma 2 and 3 (re-derived). Sign rule: sign(V_U-e^{2ac}V_I)=sign(tau_bar-tau_y) (multiply by (tau_v+tau_y)(tau_v+tau_e)e^{-2ac}). G(0+) formula with Omega(0+)=1/tau_v+a^2sd^2/tau_v^2 and V_U(0+)=1/tau_v re-derived; its sign is the sign of tau_bar.")
row("E4d-math-prop4", "2.4-mathematics", "course/modules/E/E4/project.html:295-298", "PASS",
    "Case split re-derived: lam^2(tau_e^2-tau_bar tau_e)=tau_bar a^2 sd^2 gives lam=a sd sqrt(tau_bar/(tau_e(tau_e-tau_bar))); boundary cases from G(0+) and tau_y(1); informativeness tau_bar/(tau_v+tau_bar)=1-tau_v e^{2ac}/(tau_v+tau_e) (re-derived).")
row("E4d-math-prop5", "2.4-mathematics", "course/modules/E/E4/project.html:300-301", "PASS",
    "d lam*/d sigma = lam*/sigma (lam* proportional to sigma, k(t) free of sigma); tau_bar strictly decreasing in c; k strictly increasing on (0,tau_e); informativeness free of sigma (re-derived; Lab 3 grid shows it).")
row("E4d-math-assumptions", "2.4-mathematics", "course/modules/E/E4/project.html:257-262 (A1-A5)", "PASS",
    "A1-A5 as used: A1 in Props 1-3 (step 1 uses v independent of u given s); A3 wealth factor exp(-a w0) (checked); A4 b_s != 0 for lam>0 used in step (2); A5 price taking. Text unchanged in the round-12 delta (project.html hunks at 244, 318, 320, 397, 618 only).")
row("E4d-notation", "2.4-notation", "course/modules/E/E4/project.html:266-267 (Lemma 1: x^\\ast = (m-p)/(aV)); notation/notation.json (symbol R^\\ast)", "FAIL",
    "notation/notation.json registers R^\\ast as 'the return on the SDF in the payoff space (defined in AP1 Lesson 4, where it is written x^\\ast)'. The page uses x^\\ast for the optimal demand of an informed investor (project.html:266-267). A registered symbol's written form takes another meaning. Other E4 lesson pages (L08) use the same x^\\ast for demand, so the collision is course-wide. Macros used are all registered or standard TeX (\\operatorname appears twice and is not a registry macro). T, Phi, gamma_3, gamma_4, R_f, Q, R^{e\\ast} do not appear on the page.",
    "Rename the optimal demand in Lemma 1 and its proof (project.html:266-267) to a symbol the registry does not reserve, e.g. \\hat{x}, or have the notation owner register the local use; apply the same change to L08 if the rename is adopted.")
row("E4d-banned-phrases", "2.9-prose", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py", "PASS",
    f"`tools/check_pages.py --unit E4` PASS ({M}check_pages.txt) covers the banned-phrase list on the page.")
row("E4d-process-words", "2.9-prose", "course/modules/E/E4/project.html; grader/*.py; labs", "PASS",
    "Process-word scan covered by tools/check_pages.py PASS (same log); the round-12 new prose (grader docstrings, page sentences at 244, 318, 320, 618) contains no process words.")
row("E4d-dag-links", "2.9-dag", "course/modules/E/E4/project.html", "PASS",
    f"`tools/check_dag.py --unit E4` PASS ({M}check_dag.txt). Anchors resolve: L06.html:169 id=def-noisy-rational-expectations-equilibrium, L07.html:62 id=def-price-informativeness, concepts.html:447 id=expected-utility.")
row("E4d-registry-muth", "2.1-citations", "course/modules/E/E4/project.html:684; references/references.json", "PASS",
    "data-cite='muth1961rational' at project.html:684; key present in references/references.json (line 17660); verify_refs offline 0 problems.")
row("E4d-registry-milgrom", "2.1-citations", "course/modules/E/E4/project.html:685; references/references.json", "PASS",
    "data-cite='milgrom1982information' at project.html:685; key present in references/references.json (line 17292).")
row("E4d-cites-only-registry", "2.1-citations", "course/modules/E/E4/project.html data-cite (:684-685)", "PASS",
    "The page's only data-cite attributes are the two registry keys (project.html:684-685); no bibliographic data typed in the page (grep).")
row("E4d-spec-context-sentences", "2.6-spec", "course/modules/E/E4/project.html:312 (Context)", "PASS",
    "The Context paragraph describes the model in the terms of Propositions 1-4; the one T-graded claim (Inputs, :314) is derived (see E4d-num-box-bounds).")
row("E4d-spec-questions", "2.6-spec", "course/modules/E/E4/project.html:314-322 (Inputs, Required outputs, Constraints, Grading mode, Reading list)", "PASS",
    "Each named output and condition is tested: keys (test_project.run), boundary rule, exception table (must_raise), 1e-14 gap at 0 and interior, 1e-10 root accuracy, 46 checks. Constraint wording on the sign-change assumption is a separate FAIL row (E4d12-bisection-assumption).")
row("E4d-spec-ladder", "2.6-spec", "course/modules/E/E4/project.html:40-49, :51-305, :308, :669-675", "PASS",
    "Rung headings and the ladder list match the sections (read in full this round).")
row("E4d-prose-scope-words", "2.4-scope", "course/modules/E/E4/project.html:326 (Exception table paragraph)", "PASS",
    f"Solver run at noise volumes 1e150 and 1e-50 and costs 0 and 350: finite floats, no exception, three keys ({M}tiny_noise_probe_r12.txt; the sigma=1e150 and c=350 runs were run inline this round). The scope statements hold on this range; the accuracy problem below sigma=1e-80 is separate (E4d12-tiny-noise-informativeness).")
row("E4d-prose-simulated-labs", "2.5-labs", "course/modules/E/E4/project.html:57, :176, :314, :375", "PASS",
    "Lab inputs are stated as SIMULATED and are not read from a file (project.html:53, :57, :176, :376); no real dataset is used.")
row("E4d-prose-simulated-exemplars", "2.8-data", "course/modules/E/E4/project.html:530 (exemplar intro)", "PASS",
    "The exemplar intro says the numbers are the lab's printed numbers on a SIMULATED instance; the numbers match Lab 3 (see E4d-num-exemplar-table).")
row("E4d-hours-project", "2.9-hours", "course/modules/E/E4/project.html:33, :35, :341-352; course/modules/E/E4/index.html:29", "PASS",
    "index.html:29 data-hours-lessons=72, data-hours-project=28; index.html:31 says 100 hours; 9 lessons x 8 = 72, 72+28=100; project.html:33 and :35 say 28 hours (checked this round).")
row("E4d-hours-estimate", "2.6-hours", "course/modules/E/E4/project.html #hours (:344-351)", "PASS",
    "Hour column sums: 1+1+5+8+5+5+3 = 28, equal to the Total row (project.html:351). Declared hours are design targets (plan ruling), so no estimate comparison is made.")
row("E4d-rubric-observable", "2.6-rubric", "course/modules/E/E4/project.html:517-527 (#rubric)", "PASS",
    "Five criteria (C1-C5), four levels each, each level names an observable descriptor (read in full this round).")
row("E4d-exemplar-A-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A, data-scores 2,2,1,2,1)", "UNVERIFIABLE",
    "Blind scoring is impossible: this verifier has read the annotations (project.html:544-597) in this round and in earlier rounds. Not scored.",
    "An independent verifier who has not read the annotations must score Exemplar A blind, within one level per criterion.")
row("E4d-exemplar-B-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B, data-scores 4,4,4,4,4)", "UNVERIFIABLE",
    "Same reason: annotations read (project.html:609-661). Not scored.",
    "An independent verifier who has not read the annotations must score Exemplar B blind.")
row("E4d-exemplar-annotations-hidden", "2.6-rubric", "course/modules/E/E4/project.html reveal markup (:538, :603); course/assets/js/rubric.js:147-150", "PASS",
    "The verdict paragraphs carry data-reveal (project.html:538, :603); rubric.js is unchanged between the pins and hides annotations until reveal (rubric.js:147-150, round 11 read).")
row("E4d-grader-exceptions", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:191-234, :242-280; reference.py:26-34", "PASS",
    "Carried from round 11 (test_project.py:191-280 and reference.py:26-34 byte-identical since the previous pin): both named conditions have isolated tests in both directions (noise 0, negative, inf, nan; cost -0.01, -1e-12); reference.py:26-34 unchanged.")
row("E4d-grader-messages", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (every expect() and pytest.fail call)", "PASS",
    "Read in full this round: every hint is a fixed string with no value (expect/must_raise); the round-12 new messages (test_project.py:401-417 and :555-565) contain no value.")
row("E4d-grader-oracle", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-170", "PASS",
    "Carried from round 11 (test_project.py:79-170 byte-identical since the previous pin): the oracle is independent (fixed-point price, quadrature); its values checked against reference.py at the grid points (gap at 0 difference <= 1.1e-16).")
row("E4d-grader-instances", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py:37-40", "PASS",
    "Carried from round 11 (instance.py and test_project.py:37-40 byte-identical since the previous pin); run_graders check_instances PASS (determinism and distinctness).")
row("E4d-grader-instance-docstring", "2.6-autograder", "course/modules/E/E4/grader/instance.py:1-21", "PASS",
    "Carried from round 11 (instance.py byte-identical since the previous pin): the box bounds and the tau_bar values in the docstring re-computed this round (E4d-num-box-bounds).")
row("E4d-grader-test-docstring", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (gap-at-zero docstring; tiny-root docstring)", "PASS",
    f"Gap-at-zero docstring numbers: |gap(1e-12)-limit| = 1.02e-13 to 3.54e-13 (stated 1e-13 to 4e-13); |oracle(0)-limit| <= 1.11e-16 (stated at most 1.1e-16) ({M}test_doc_numbers.txt). Tiny-root docstring (noise volumes 1e-11..1e-40 at cost 0.15) consistent with the closed form.")
row("E4d-grader-reference-docstring", "2.6-autograder", "course/modules/E/E4/grader/reference.py:21-23", "FAIL",
    "reference.py:23 says '(2^-240 is about 6.2e-73)'. Computed: 2^-240 = 5.6598e-73 (python Decimal). The sentence's other figures are right: 240 halvings reach 1e-12 relative for roots above 5.66e-61 ('about 6e-61'), and 200 halvings do not reach it near 2e-51.",
    "Change '6.2e-73' to '5.7e-73' on reference.py:23 (and in the four ledgers/E4/equivalent/ files and the four round-12 mutant copies that repeat the comment).")
row("E4d-grader-stdlib", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_solver_imports_only_the_standard_library); ledgers/E4/alternatives/*.py", "PASS",
    "The stdlib test passes for reference.py and for all eleven alternatives (run_variants: 50/50 each).")
row("E4d-runtime", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    f"run_graders slowest seed 0.2 s; page_smoke in-browser run of 46 tests 0.8 s ({M}page_smoke_project.txt). Limit per test 5 s and suite 60 s are met locally; Pyodide itself not run (see notes).")
row("E4d-browser-local-parity", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; tools/page_smoke.py", "PASS",
    "page_smoke runs the same suite through the repo's in-browser harness (46 passes, PASS); the local run uses the same file.")
row("E4d2-exemplar-B-C1-annotation", "2.3-grades", "course/modules/E/E4/project.html:604-607 (Exemplar B Model passage, annotation :611)", "PASS",
    "The annotation's claim (lists each assumption with its number and names the results that use it) holds. The sentence 'the volume sigma appears in Proposition 4' in the same passage is a separate FAIL (E4d12-exemplar-B-sigma).")
row("E4d3-cara-defined-twice", "2.9-prose", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:57, :66",
    "PASS", "Carried from round 11 (project.html:259 and L06.html:57, :66 byte-identical since the previous pin): both pages define CARA once, as Definition 6.2 in L06 and as A3 here, with the same form -a w.")
row("E4d3-anchors-links", "2.9-structure", "course/modules/E/E4/project.html (href targets)", "PASS",
    "tools/check_pages.py PASS (link checks); anchors #brief, #rubric, #self-assessment, #exceptions, #lab-E4-project-1..3, #grader, #stretch resolve (grep, this round).")
row("E4d3-no-figures-no-data", "2.8-data", "course/modules/E/E4/project.html", "PASS",
    "grep for img, svg, canvas, figure in project.html: 0 matches. No figure, no data file, no kernel is used.")
row("E4d3-spec-stop-rule-and-constraints", "2.6-spec", "course/modules/E/E4/project.html:318 (Constraints); grader/test_project.py (accuracy and gap tests)", "FAIL",
    "project.html:318 now states the stop rule ('no wider than 1e-12 times its upper end', 'at most 240 halvings') and an accuracy clause (1e-10 times the root for sigma >= 1e-50 and tau-bar >= 1e-2). The suite enforces the accuracy clause only at costs 0.13, 0.15 and 0.1707691121 (test_project.py:534-565). mutant_r12_04 (gap-based stop) passes every test on seeds 0-49 and violates the clause at sigma=1e-50, cost 1e-6 (relative error 5.7e-8) and at sigma=1e-40, cost 1e-4 (4.6e-10) (ledgers/E4/scripts/E4-d-r12/logs/tau_near_one_probe_r12.txt).",
    "Add a relative-accuracy test at a cost near zero, e.g. closed_form_root(1e-50, 1e-6) with the 1e-10 bound and closed_form_root(1e-40, 1e-4); the reference passes both (relative errors 1.1e-11 and 1.1e-13).")
row("E4d3-atlas-studios-na", "2.6-atlas", "atlas/, studios", "PASS",
    "Carried from round 11 (atlas/ byte-identical since the previous pin): the unit has no atlas path (plans/E4-build-plan.md, 'No Atlas path').")
row("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/ (98 pre-existing files at 5db69a9)", "PASS",
    f"tools/mutate_graders.py --unit E4 --seeds 0-9 ({M}mutate_graders_seeds0-9.txt): 98 of the 98 pre-existing mutants KILLED, each by a named test.")
row("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", "PASS",
    "Both KILLED in the seeds 0-9 gate (test_noise_volume_far_above_one_is_accepted, test_info_cost_above_one_is_accepted).")
row("E4d2-mutants-r2", "2.6-mutation", "ledgers/E4/mutants/mutant_r2_*.py", "PASS", "All five r2 mutants KILLED in the seeds 0-9 gate.")
row("E4d3-mutants-r3", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_*.py", "PASS", "All five r3 mutants KILLED in the seeds 0-9 gate.")
row("E4d3-mutant-tolerance-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", "PASS",
    "KILLED by test_fraction_is_the_oracle_root[first] (seed 0), gate log.")
row("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (102 files at 5db69a9)", "FAIL",
    f"`tools/mutate_graders.py --unit E4 --seeds 0-9` -> 'mutate_graders E4: FAIL' (101 of 102 KILLED, exit 1 in the gate's own rule). The survivor is mutant_r12_04_stops_when_midpoint_gap_is_tiny.py (E4d12-mutant-gap-stop).",
    "Resolve E4d12-mutant-gap-stop: add the cost-near-zero accuracy test, or record the mutant with an architect-approved README proof under ledgers/E4/equivalent/ (it is not output-equivalent on the page's domain, so the test is the fix).")
row("E4d-equivalent", "2.6-mutation", "ledgers/E4/equivalent/literal_price_sign.py; mutant_r6_08_*; mutant_r7_01_*; mutant_v9_02_*", "PASS",
    f"All four pass seeds 0-49 (50/50 each; {M}equivalent_seeds0-49.txt). literal_price_sign vs reference on 3000 random inputs: max abs difference 0.0 ({M}literal_price_sign_random.txt).")
row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py .. alt_5.py", "PASS",
    f"run_variants on seeds 0-49: PASS 50/50 for alt_1 to alt_5 ({M}alternatives_seeds0-49.txt). The round-12 alternatives (alt_r12_a, _b, _c) and round-11 alt_r11_a also pass 50/50 ({M}alt_r12_0-49.txt, {M}alt_r11_a_0-49.txt).")
row("E4d-starter", "2.6-autograder", "course/modules/E/E4/grader/starter.py", "PASS",
    "run_graders starter check (the starter fails the suite on seed 0): PASS in run_graders.txt.")
row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py", "PASS",
    "alt_4 (secant with sign-change bracket, relative stop) passes seeds 0-49 50/50 (alternatives_seeds0-49.txt); the round-4 concern is closed at this pin.")
row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1-3", "PASS",
    "Docstring says 'at most 240 halvings'; code at alt_1.py:80 uses 240 (round-12 delta line). Consistent.")
row("E4d4-equivalent-price-slope", "2.6-mutation", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py; ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    "Script present (unchanged between the pins); literal_price_sign outputs equal the reference on 3000 random inputs (max 0.0, re-run this round).")
row("E4d4-calibration-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A)", "UNVERIFIABLE",
    "Same blind-scoring limit as E4d-exemplar-A-calibration. Not scored.",
    "Independent blind scoring of Exemplar A (see E4d-exemplar-A-calibration).")
row("E4d4-proposed-test-validated", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (small-noise and corner tests)", "PASS",
    "The 1e-10 relative tests pass the reference (run_graders 50/50) and kill the 200-halving mutants (mutant_f11_01 and mutant_r6_09 KILLED by test_corner_root_meets_the_relative_accuracy_at_the_domain_edge; mutant_r8_01 KILLED).")
row("E4d4-mutants-killed-r4", "2.6-mutation", "ledgers/E4/mutants/mutant_r4*.py", "PASS", "All mutant_r4* files KILLED in the seeds 0-9 gate.")
row("E4d4-exemplar-B-results-numbers", "2.2-numbers", "course/modules/E/E4/project.html:629-641", "PASS",
    "Re-checked this round (E4d-num-exemplar-table).")
row("E4d5-mutant-bracket-floor", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", "PASS", "KILLED (test_tiny_noise_root_is_relatively_accurate[1e-12], gate log).")
row("E4d5-mutant-sixty-halvings", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", "PASS", "KILLED (test_small_noise_root_is_relatively_accurate[1e-09], gate log).")
row("E4d5-mutant-uninformed-precision", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", "PASS", "KILLED (test_indifference_holds_at_an_interior_fraction[first], gate log).")
row("E4d5-calibration-B-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B)", "UNVERIFIABLE",
    "Same blind-scoring limit as E4d-exemplar-B-calibration. Not scored.",
    "Independent blind scoring of Exemplar B (see E4d-exemplar-B-calibration).")
row("E4d6-mutant-06", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py", "PASS", "KILLED (test_unit_fraction_is_reported_with_a_positive_cost, gate log).")
row("E4d6-mutant-07", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py", "PASS", "KILLED (test_unit_fraction_is_reported_with_a_positive_cost, gate log).")
row("E4d6-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_0*.py", "PASS",
    "All r6 mutants in mutants/ KILLED in the gate; mutant_r6_08 is in equivalent/ and passes (E4d6-spec-variants-08-09).")
row("E4d6-spec-variants-08-09", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py", "PASS",
    "r6_08 passes seeds 0-49 (equivalent; reports the lower end, within the final width 1e-12 times the root). r6_09 is in mutants/ and KILLED by the corner test (gate log).")
row("E4d6-stop-rule-measured", "2.6-autograder", "course/modules/E/E4/grader/reference.py:22-23, :138; ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_*", "PASS",
    f"Re-run this round: the round-11 corner scan reproduces exactly: cap 200 -> 11598 of 90000 over 1e-10, max 1.5322e-10; cap 240 -> 0 over, max 5.142e-13 ({M}corner_cap200_grid_r12.txt, {M}r11_corner_script_rerun.txt).")
row("E4d6-alt-extra-damped", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", "PASS",
    "Carried from round 11 (ledgers/E4/scripts/E4-d-r6/ byte-identical since the previous pin): the candidate is a script record, not a suite member; no change.")
row("E4d6-rung1-why", "2.9-prose", "course/modules/E/E4/project.html:171 (Lab 1 interpretation)", "PASS",
    "Carried from round 11 (project.html:171 byte-identical since the previous pin): the 2^-53 = 1.110e-16 width and the floating-point argument re-checked (Lab 1 output 1.110e-16).")
row("E4d7-midpoint-untested", "2.6-autograder", "course/modules/E/E4/project.html:318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", "PASS",
    "The Constraints (:318) do not say 'midpoint'; the exemplar method (:618) does, but an exemplar is not the solver's specification. The lower-end variant passes seeds 0-49 (equivalent_seeds0-49.txt), so the midpoint is not a spec item here.")
row("E4d7-cost-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_info_cost_above_one_is_accepted, far-above-one tests); project.html:326", "PASS",
    "Exception table names only negative cost; the cost-above-one mutants are KILLED (r7_03, r8_03 in the gate log).")
row("E4d7-noise-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_noise_volume_far_above_one_is_accepted)", "PASS",
    "Noise above one accepted by the reference and killed mutants (r7_02, r8_02, r4f_rejects_noise_above_one) in the gate log.")
row("E4d7-alt5-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_5.py:1-2", "PASS",
    "Docstring 'same model parameterised by the noise precision, with the same bracket [0, 1]' matches the code; alt_5 passes 50/50.")
row("E4d7-lab1-bracket-width", "2.5-labs", "course/modules/E/E4/project.html:171", "PASS",
    "Lab 1 prints 'after 60 halvings the bracket width is 1.110e-16' (re-run this round, twin_p1.out); the interpretation's 2^-53 claim matches.")
row("E4d7-lab2-blank", "2.5-labs", "course/modules/E/E4/project.html:244 (Lab 2 interpretation); :217 blank", "PASS",
    "Only the return line differs from the twin (line 41); the interpretation 'The blank is the only line that changes' holds (twin_vs_page.txt).")
row("E4d7-instance-bound", "2.8-data", "course/modules/E/E4/grader/test_project.py; grader/instance.py:1-21; project.html:314", "PASS",
    "The bound 0 < tau_bar < tau_y(1) on the box is verified by the closed-form bounds (E4d-num-box-bounds) and by a 22 x 22 grid (484 of 484, rederive_r12.txt).")
row("E4d7-lab3-closed-form-sentence", "2.5-labs", "course/modules/E/E4/project.html:376 (Lab 3 hypothesis)", "PASS",
    "'the bisection agrees with the closed form of Proposition 4 to within 1e-12': largest difference 2.134e-13 (rederive_r12.txt, Lab 3 output 2.1e-13).")
row("E4d7-test-count", "2.6-autograder", "course/modules/E/E4/project.html:320 (Grading mode); grader/test_project.py", "PASS",
    "'runs 46 checks' (project.html:320, changed in this delta from 43): collect-only 46 (collect.txt); page_smoke 'All 46 tests pass'.")
row("E4d8-no-upper-bound", "2.4-scope", "course/modules/E/E4/project.html:326; grader/reference.py:122-151; grader/test_project.py (far-above-one tests)", "PASS",
    "No upper bound is named (:326); the reference accepts noise 1e150 and cost 350 with finite outputs (probe this round); far-above-one tests pass.")
row("E4d8-cap-100-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py; project.html:318", "PASS",
    "KILLED by test_tiny_noise_root_is_relatively_accurate[1e-30] (gate log).")
row("E4d8-noise-cap-10-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py; project.html:326", "PASS",
    "KILLED by test_noise_volume_far_above_one_is_accepted[50.0] (gate log).")
row("E4d8-cost-cap-5-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py; project.html:326", "PASS",
    "KILLED by test_info_cost_far_above_one_is_accepted[10.0] (gate log).")
row("E4d8-mutants-r8-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_04_integer_zero_fraction.py; mutant_r8_05_informativeness_at_unit_precision.py", "PASS",
    "Both KILLED (gate log).")
row("E4d8-alternatives-r8", "2.6-alternatives", "ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py (cited by round 8)", "UNVERIFIABLE",
    "The files are absent at this pin (ls ledgers/E4/alternatives: alt_1 to alt_5 only). The round-8 claim cannot be read.",
    "Either restore alt_r8_a and alt_r8_b at a pin, or delete the round-8 citation; the round-12 alternatives (alt_r12_a/b/c, in scripts) pass 50/50 and can be promoted.")
row("E4d8-tiny-root-reference", "2.6-autograder", "course/modules/E/E4/grader/reference.py", "PASS",
    "Relative errors at sigma 1e-40, 1e-50, 1e-55, 1e-60 are 3.6e-13, 6.5e-14, 2.2e-13, 1.6e-13 (tiny_noise_probe_r12.txt). Below 1e-65 the reference fails (E4d12-tiny-noise-informativeness), which is outside the stated accuracy domain.")
row("E4d8-lab3-twin-page", "2.5-labs", "course/modules/E/E4/project.html:377-503; tests/labs/E4/lab-E4-project-3.py", "PASS",
    "Page code equals the twin (114 lines, twin_vs_page.txt); the expected block equals the twin's stdout.")
row("E4d9-mutant-v9-02", "2.6-mutation", "ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py (moved from mutants/ in round 10)", "PASS",
    "Passes seeds 0-49 (50/50). Recorded as equivalent: its final bracket lies inside the reference's, so its midpoint differs by at most the final width (equivalent/README.md).")
row("E4d9-mutant-v9-06", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py", "PASS", "KILLED by test_gap_at_zero_fraction_is_the_limit_to_full_precision (gate log).")
row("E4d9-equivalent-r6-08-09-docstrings", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py", "PASS",
    "Docstrings match the code (r6_08 reports the lower end; r6_09 takes 200 halvings and never applies the relative rule).")
row("E4d9-mutants-v9-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_01, _03, _05, _07", "PASS", "All four KILLED (gate log).")
row("E4d9-mutant-docstrings", "2.6-mutation", "ledgers/E4/mutants/*.py (98 + 4 round-12 files) against grader/reference.py", "PASS",
    "Each mutant's one-line docstring names the error the code makes (checked against the gate log descriptions, 102 entries; mutant_r12_04 description matches its code).")
row("E4d9-alternatives-v9", "2.6-alternatives", "ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_grid_then_bisect.py", "UNVERIFIABLE",
    "These files are absent at this pin (ls ledgers/E4/alternatives: alt_1 to alt_5 only). Cannot be read.",
    "Restore the files at a pin or remove the citation.")
row("E4d10-delta-A1-prior-mean", "2.4-mathematics", "course/modules/E/E4/project.html:257-262 (A1)", "PASS",
    "Carried from round 11 (project.html:257-262 byte-identical since the previous pin): the A1 shift argument re-checked (demand depends on E[v|F]-p; utility on v-p).")
row("E4d10-delta-inputs-interior-root", "2.6-spec", "course/modules/E/E4/project.html:314 (Inputs)", "PASS",
    "Carried from round 11 (project.html:314 byte-identical since the previous pin); its numbers re-computed this round (E4d-num-box-bounds).")
row("E4d10-delta-constraints-gap-at-zero", "2.6-spec", "course/modules/E/E4/project.html:318 (gap at zero clause)", "PASS",
    "The 1e-14 relative clause for the gap at fraction 0 is unchanged in wording; test_gap_at_zero_fraction_is_the_limit_to_full_precision passes the reference and kills mutant_r10_01 (gate log).")
row("E4d10-delta-grading-mode-43", "2.6-autograder", "course/modules/E/E4/project.html:320 (Grading mode)", "PASS",
    "Round-10 text said 43; the page now says 46 and the collect-only count is 46 (collect.txt).")
row("E4d10-delta-results-ratio", "2.2-numbers", "course/modules/E/E4/project.html:629-641", "PASS",
    "Carried from round 11 (project.html:629-641 byte-identical since the previous pin): ratios 1.2501 and 1.5000 from the displayed values, and 1.250000000000 / 1.500000000001 unrounded (rederive_r12.txt).")
row("E4d10-new-test-numbers", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test docstrings with numbers)", "PASS",
    "The collect-only count matches the page; the gap-at-zero docstring numbers match (test_doc_numbers.txt).")
row("E4d10-mutants-new-r10", "2.6-mutation", "ledgers/E4/mutants/mutant_r10_01..04 (7 files)", "PASS",
    "All seven KILLED in this round's gate, including mutant_r10_02_cost_factor_relative_error.py (killed by test_gap_at_an_interior_fraction_is_the_oracle_gap_to_full_precision[first]).")
row("E4d10-alternatives-r10", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_5", "PASS", "alt_1 to alt_5 each 50/50 seeds (alternatives_seeds0-49.txt).")
row("E4d10-l06-dependency", "2.9-dag", "course/modules/E/E4/L06.html:57, :66, :169; course/modules/E/E4/L07.html:62", "PASS",
    "L06.html:66 'Definition 6.2 (CARA utility)'; L06.html:169 id=def-noisy-rational-expectations-equilibrium; L07.html:62 id=def-price-informativeness; all three anchors present at this pin (grep this round). L06 changed in the delta at other lines only.")
row("E4d10-lab3-numbers", "2.5-labs", "course/modules/E/E4/project.html:376-503", "PASS",
    "Lab 3 output re-run this round: nine rows equal the page; largest difference 2.1e-13 (twin_vs_page.txt; rederive_r12.txt).")
row("E4d11-delta-hunks", "2.6-delta", "project.html:244, :318, :320, :397, :618; test_project.py:401-418, :534-553; reference.py:22-23; alt_1.py:1, :80; alt_5.py:101; lab-E4-project-3.py:21; index.html:63; equivalent/README.md, literal_price_sign.py, mutant_r6_08, mutant_r7_01, mutant_v9_02; mutants added/moved", "PASS",
    "git diff -U0 11d7077a 5db69a9b over the slice: every hunk read (listed in this row's location). The hunks are the 240 cap, the stop rule wording, the interior-gap test, the corner test, the 1e-10 tests, the test count 46, the Exemplar B method sentence, and the mutant files. index.html:63 is the prerequisite prose only (hours at :29 unchanged).")
row("E4d11-constraints-accuracy", "2.6-spec-vs-suite", "course/modules/E/E4/project.html:318; grader/test_project.py:534-565", "FAIL",
    "The accuracy clause (1e-10 times the root for interior roots when sigma >= 1e-50 and tau-bar >= 1e-2) is held by the reference, but the suite tests it at three costs only (0.13, 0.15, 0.1707691121), all with tau-bar in [0.01, 0.19]. mutant_r12_04 violates the clause at tau-bar near 1 (cost 1e-6 and 1e-4) and passes every test (E4d12-mutant-gap-stop).",
    "Add the cost-near-zero relative-accuracy test described in E4d12-mutant-gap-stop.")
row("E4d11-constraints-wording", "2.2-prose-numbers", "course/modules/E/E4/project.html:318", "PASS",
    "Numbers in the Constraints clause re-checked: 1e-14 (test_project.py:395, :413), 1e-12 and 240 halvings (reference.py:21-22, :138), 1e-10 (test :538, :563), sigma >= 1e-50 (test corner). The sign-change wording is a separate FAIL (E4d12-bisection-assumption).")
row("E4d11-oracle-precision", "2.6-grader", "course/modules/E/E4/grader/test_project.py:79-170", "PASS",
    "Carried from round 11 (test_project.py:79-170 byte-identical since the previous pin): the oracle's fixed point is run to 1e-13 and its quadrature to the trapezoid rule over 1001 nodes; agreement with reference.py at 1.1e-16 (test_doc_numbers.txt).")
row("E4d11-mutants-new-r11", "2.6-mutation", "ledgers/E4/mutants/mutant_r11_01..04", "PASS",
    "All eight r11 mutant files KILLED in the seeds 0-9 gate (gate log).")
row("E4d11-alt-closed-form", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py", "PASS",
    f"Closed-form alternative: PASS 50/50 seeds ({M}alt_r11_a_0-49.txt).")
row("E4d11-literal-price-sign-open", "2.2-math", "ledgers/E4/equivalent/literal_price_sign.py; project.html:276-283 (Proposition 1 sign)", "PASS",
    "Outputs equal the reference (3000 random inputs, max 0.0); the Proposition 1 sign is untestable by outputs. Open architect item (ruling 9) recorded in equivalent/README.md; this verifier does not decide it.")
row("E4d11-lab-page-twin", "2.5-labs", "project.html lab blocks vs tests/labs/E4/lab-E4-project-{1,2,3}.py", "PASS",
    "Re-run this round: Lab 1 equal, Lab 2 equal except the blank, Lab 3 equal (twin_vs_page.txt).")
row("E4d11-plan-tolerance-documented", "2.2-spec-vs-plan", "course/modules/E/E4/project.html:318; plans/E4-build-plan.md:389 and :182-184 (rule 12)", "PASS",
    "project.html:318 now states the bisection tolerance (1e-12 times the upper end) and the stop rule (at most 240 halvings) as documented constants, and the bracket. This meets plan line 389 and rule 12 for tolerance and stop rule. The unnumbered sign-change assumption is a separate FAIL (E4d12-bisection-assumption).")
row("E4d11-mutant-r10-02", "2.6-grader", "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py vs grader/test_project.py:401-418", "PASS",
    "KILLED in this round's gate by test_gap_at_an_interior_fraction_is_the_oracle_gap_to_full_precision[first] (seed 0), added in the round-12 delta.")

# ---- new round-12 rows
row("E4d12-mutant-gap-stop", "2.6-grader", "ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py; grader/test_project.py:534-565; project.html:318", "FAIL",
    f"The new student-error mutant (stop when |gap at the midpoint| <= 1e-12, not the bracket rule) is SURVIVED on seeds 0-9 and 0-49 (gate log; {M}mutant_r12_04_seeds0-49.txt). It violates a page-stated behaviour: project.html:318 accuracy clause. Measured relative errors vs the Proposition 4 closed form: sigma=1e-50, cost 1e-6: mutant 5.71e-8 (reference 1.13e-11); sigma=1e-40, cost 1e-4: mutant 4.56e-10 (reference 1.09e-13) ({M}tau_near_one_probe_r12.txt). Across 6040 cases the outputs differ by up to 4.5e-9 relative ({M}mutant_r12_04_equivalence.txt), so it is not output-equivalent on the domain.",
    "Add a relative-accuracy test at tau-bar near 1, e.g. closed_form_root(1e-50, 1e-6) and closed_form_root(1e-40, 1e-4) with the 1e-10 bound. The reference passes both (1.1e-11, 1.1e-13).")
row("E4d12-tiny-noise-informativeness", "2.4-scope", "course/modules/E/E4/project.html:326 (exception table range), :314 and :316 (Required outputs); grader/reference.py:26-44, :122-151", "FAIL",
    f"The exception table (:326) makes every positive noise volume up to 1e150 valid and returns 'the three keys'; Required outputs (:316) define price_informativeness as Corr(v,p)^2 at lambda* (Proposition 2), and Proposition 4 says the interior informativeness is tau-bar/(tau_v+tau-bar), free of sigma. The reference returns lambda=2.83e-73 and informativeness 0.500000 for sigma <= 1e-80 at cost 0.13, where the closed form is 9.656e-81 (or smaller) and the informativeness 0.158986 ({M}tiny_noise_probe_r12.txt). At sigma=1e-65 the relative error is 1.7e-8. The page states an accuracy requirement only for sigma >= 1e-50 (:318), so the failure is outside the stated accuracy domain but inside the stated validity range.",
    "Either state the accuracy domain (sigma >= 1e-50) in the exception table and Required outputs, or make the solver scale-invariant (work with lambda/sigma so that lambda^2 does not underflow and the 240-halving cap is not absolute) and add a test at sigma = 1e-80 with the closed form.")
row("E4d12-bisection-assumption", "2.2-spec-vs-plan", "course/modules/E/E4/project.html:318 ('the sign-change assumption'); plans/E4-build-plan.md:168, :328 (D4), :685-686 (Q14 RECOMMENDED)", "FAIL",
    "Constraints (project.html:318) cites 'the sign-change assumption' but no numbered Assumption on the page defines it (the model section has A1 to A5 only; grep 'A6' and 'sign change' finds only :171 and :318). The plan's binding Q14 recommendation (plan :685-686) and D4 (:328) require the sign-change and continuity condition to be stated as a numbered Assumption (A-bisect). Continuity of the gap on (0,1] is not stated anywhere on the page.",
    "Add a numbered Assumption (A6, bisection) to the model section stating that the gap is continuous on (0,1] and changes sign between its ends, and cite it from :318 and from the Lab 1/Lab 2 hypothesis text.")
row("E4d12-prose-2pow240", "2.2-prose-numbers", "course/modules/E/E4/grader/reference.py:23; ledgers/E4/equivalent/literal_price_sign.py:15; ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py:15; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py:15; ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py:15; ledgers/E4/mutants/mutant_r12_0*.py:13", "FAIL",
    "'(2^-240 is about 6.2e-73)'. Computed 2^-240 = 5.6598e-73 (rederive_r12.txt, Decimal). Same error repeated in the equivalent files and in this round's four mutant copies. Other figures in the same comments are right (6e-61 threshold; 2^-200 = 6.2e-61; 200 halvings do not reach 1e-12 relative near 2e-51).",
    "Replace 6.2e-73 with 5.7e-73 in reference.py:23 and each listed comment (regenerate the equivalent files from the reference).")
row("E4d12-exemplar-B-sigma", "2.3-grades", "course/modules/E/E4/project.html:607 (Exemplar B Model passage)", "FAIL",
    "The passage says 'the volume sigma appears in Proposition 4'. sigma also appears in Proposition 1 (tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sigma^2), project.html:277) and in Proposition 3 (G(0+), :291). The sentence reads as if sigma enters only at Proposition 4, and it sits in the exemplar students are asked to emulate.",
    "Change the clause to 'the volume sigma appears in Propositions 1, 3 and 4' (or list the propositions where it enters).")
row("E4d12-corner-test-docstring", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:555-558 (test_corner_root docstring)", "PASS",
    "The docstring's root of about 2e-51 (computed 2.022e-51) and the 200-halving failure (cap 200 relative error 1.295e-10 at cost 0.1707691121, computed this round) are right.")
row("E4d12-alt-variants-new", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r12/alts/alt_r12_a.py, alt_r12_b.py, alt_r12_c.py", "PASS",
    f"Three new correct alternatives (closed form with the gap by formula; bisection on the sign of tau-bar - tau_y; Illinois regula falsi): each PASS 50/50 seeds ({M}alt_r12_0-49.txt). No over-constraint found.")
row("E4d12-equivalent-readme-numbers", "2.2-numbers", "ledgers/E4/equivalent/README.md (round-11 numbers)", "PASS",
    f"Reproduced: 11598 of 90000 over 1e-10 at cap 200, max 1.5322e-10 at sigma 1e-50, cost 0.17076911209; with cap 240, 0 over, max 5.142e-13 ({M}corner_cap200_grid_r12.txt). The 209-halving figure: 2^-209 = 1.2e-63 <= 1e-12 * 2e-51 = 2e-63 (checked; 208 halvings give 2.4e-63, not enough).")

# ---- assemble
ids_prev = set(prev_ids)
out_rows = []
for rid in prev_ids:
    out_rows.append(rows.pop(rid))
out_rows += [rows[k] for k in sorted(rows)]
missing = [i for i in prev_ids if i not in {r["id"] for r in out_rows}]
assert not missing, missing
n_pass = sum(r["status"] == "PASS" for r in out_rows)
n_fail = sum(r["status"] == "FAIL" for r in out_rows)
n_un = sum(r["status"] == "UNVERIFIABLE" for r in out_rows)
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if n_pass == len(out_rows) and killed == len(mutants) else "FAIL"
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 12,
    "verifier": "Haiku independent verifier, E4 slice d, round 12 (did not build E4; checkout at 5db69a9)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin). Delta in the slice: project.html 244, 318, 320, 397, 618; test_project.py 401-418, 534-565; reference.py 22-23; alt_1.py 1, 80; alt_5.py 101; lab-E4-project-3.py 21; index.html 63 (prose only); equivalent/README.md and four equivalent files; mutants r11 and f11 added; mutant_r6_09 moved to mutants/. Every hunk read.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-E4-d",
    "scratch": "scratch copies in /tmp (mktemp -d /tmp/e4d12-*), removed after use; scripts and logs in ledgers/E4/scripts/E4-d-r12/",
    "verified_at": "2026-11-05T13:57:19+00:00",
    "verdict": verdict,
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 12 re-ran every command row (check_pages, check_dag, check_projects, run_labs, run_graders 0-49, page_smoke project alone, ruff check and format, mypy --no-incremental, relevant pytest, verify_refs --offline, collect-only) and the mutation gate tools/mutate_graders.py --unit E4 --seeds 0-9.",
        "Gate result: 101 of 102 mutants KILLED. The survivor is the round-12 mutant mutant_r12_04_stops_when_midpoint_gap_is_tiny.py (E4d12-mutant-gap-stop); the gate exits 1.",
        "Round-11 FAIL rows E4d11-plan-tolerance-documented and E4d11-mutant-r10-02 and E4d10-mutants-new-r10 are resolved and now PASS. E4d-grader-reference-docstring, E4d3-spec-stop-rule-and-constraints, E4d11-constraints-accuracy, E4d-notation and E4d-mutants-total are FAIL at this pin.",
        "Calibration rows (Exemplars A and B blind scoring) remain UNVERIFIABLE: this verifier has read the annotations, so no blind score is possible.",
        "The round-8 and round-9 alternative files (alt_r8_*, alt_v9_*) are still absent at this pin.",
        "Open architect item, not a fail: literal_price_sign.py is output-equivalent (equivalent/README.md); whether Proposition 1's sign is enough to keep it there is the architect's call (ruling 9).",
        "Not checked: the Pyodide interpreter itself (page_smoke runs the suite through the repo's in-browser harness); the lesson files L01-L05 and L07-L09 and cards.json (outside slice d); the Exemplar calibration (blind scoring) and the round-8/9 alternatives (absent).",
        "Round-12 new mutants mutant_r12_01..03 (cost factor squared, uninformed pays cost, informed variance uses b_s) are KILLED; mutant_r12_04 SURVIVED. All four copy reference.py and therefore carry its 6.2e-73 comment (E4d12-prose-2pow240).",
    ],
    "summary": {
        "rows": len(out_rows),
        "pass": n_pass,
        "fail": n_fail,
        "unverifiable": n_un,
        "mutants": len(mutants),
        "mutants_killed": killed,
    },
}
Path(ROOT / "ledgers/E4/E4-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), "pass", n_pass, "fail", n_fail, "unverifiable", n_un, "mutants", len(mutants), "killed", killed, "verdict", verdict)
