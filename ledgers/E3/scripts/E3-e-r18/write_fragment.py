"""Writes the round-18 E3 slice e fragment (ledgers/E3/E3-e.json). Rows and evidence are the verifier's own."""
import json, pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD18-E3-e")
OUT = "ledgers/E3/scripts/E3-e-r18/out/"
CARRY_IDX = "Carried from round 15 (course/modules/E/E3/index.html byte-identical since dde0486b; L01-L08 hours, h1 titles and dfn ids unchanged per E3e-r18-index-carry-basis):"
CARRY_L02 = "Carried from round 15 (course/modules/E/E3/L02.html byte-identical since dde0486b):"
CARRY_L07 = "Carried from round 15 (course/modules/E/E3/L07.html changed only at line 571, the footer, re-verified in E3e-r15-footers-registry-claim; the cited subjects below are byte-identical since dde0486b):"
CARRY_L04 = "Carried from round 15 (course/modules/E/E3/L04.html changed only at line 51, the why-it-matters paragraph, re-verified in E3e-r14-why-it-matters; the cited theorems and examples are byte-identical since dde0486b):"
CARRY_REF = "Carried from round 15 (references/ and notation/notation.json byte-identical since dde0486b):"
CARRY_PLAN = "Carried from round 15 (plans/E3-build-plan.md byte-identical since dde0486b):"

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates re-run on this pin
row("E3e-r14-gate-check-pages", "check_pages --all (static page rules) includes E3",
    "tools/check_pages.py; course/modules/E/E3/index.html, L01-L08.html",
    "PASS", f"ledgers/E3/scripts/E3-e-r18/{OUT}check_pages.out: 'check_pages E3: PASS', exit 0.")
row("E3e-r14-gate-check-dag", "check_dag --all (concept dfn/links, prerequisite closure) includes E3",
    "tools/check_dag.py; course/modules/E/E3", "PASS",
    f"{OUT}check_dag.out: 'check_dag E3: PASS', exit 0.")
row("E3e-r14-gate-check-projects", "check_projects --all includes E3 (project slice not judged here)",
    "tools/check_projects.py; unit E3", "PASS", f"{OUT}check_projects.out: 'check_projects E3: PASS', exit 0.")
row("E3e-r14-gate-run-labs-L05-L08", "run_labs --unit E3: every inline lab, twin byte-identity, twin run, expected block",
    "tools/run_labs.py --unit E3; lab sections in L01-L08.html", "PASS",
    f"{OUT}run_labs_E3.out: 'run_labs E3: PASS (11/11)', exit 0. Exact expected-block check of the changed labs in {OUT}lab_exact.out (L01, L03, L05, L06, L08: page code equals twin, stderr 0 bytes, expected block equals stdout character for character).")
row("E3e-r14-gate-page-smoke", "page_smoke --unit E3 --skip-sweep: console, KaTeX strict parse, layout at 360 px",
    "tools/page_smoke.py; index.html, L01-L08.html", "PASS",
    f"{OUT}page_smoke_E3.out: each of index.html and L01.html..L08.html PASS, 'page_smoke E3: PASS', exit 0. The figure sweep was skipped (E3 has no live figures; the rule of the round is targeted). KaTeX strict parsing accepts \\check, \\Xi, \\Omega, \\iota and \\mathrm{{PV}}.")
row("E3e-r14-twins-L05-L08-run", "Changed lab twins run alone under python -I -W error, exit 0, empty stderr",
    "tests/labs/E3/lab-E3-L01-1.py, lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py (and L03 twin, unchanged)", "PASS",
    f"{OUT}lab_exact.out: exit 0 and stderr_bytes 0 for each; stdout lines 23 (L01), 19 (L03), 23 (L05), 18 (L06), 25 (L08). L02, L04 and L07 twins are unchanged and run by run_labs (11/11).")
row("E3e-r14-twins-L05-L08-lint", "Changed twins pass ruff check, ruff format --check and mypy",
    "tests/labs/E3/lab-E3-L01-1.py, lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py", "PASS",
    f"{OUT}ruff_check_twins.out 'All checks passed!' exit 0; {OUT}ruff_format_twins.out '4 files already formatted' exit 0; {OUT}mypy_twins.out 'Success: no issues found in 4 source files' exit 0.")
row("E3e-r14-verify-refs-offline", "verify_refs --offline on references/references.json",
    "references/references.json; tools/verify_refs.py", "PASS",
    f"{OUT}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. references/ is not in the delta (git diff --stat dde0486b 4540351d -- references is empty).")
row("E3e-r14-registry-crossref-live", CARRY_REF[:0] + "Live Crossref check of the five E3 registry keys (carried; no live run this round)",
    "references/references.json (pratt1964risk, kahneman1979prospect, epstein1989substitution, ellsberg1961risk, gilboa1989maxmin)", "PASS",
    CARRY_REF + " the live Crossref result recorded in round 15 is not re-run here. A live run was not attempted this round.")
row("E3e-r14-pytest-relevant", "Relevant pytest: labs, run_labs, page checks, build_site, docs figures, page smoke, curriculum",
    "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_build_site.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py (-k 'E3 or L0 or lab or page or docs or site or curriculum')",
    "PASS", f"{OUT}pytest_relevant_summary.out: '474 passed in 68.69s'. build_site --check: {OUT}build_site_check.out 'site data current: 6 outputs', exit 0.")

# ---- hub index (byte-identical since dde0486b)
row("E3e-r14-hub-structure", "index.html structure (sections, headings, lesson list, skip links)",
    "course/modules/E/E3/index.html", "PASS",
    CARRY_IDX + " tag multiset identical at both pins (ledgers/E3/scripts/E3-e-r18/out/tag_structure.out, see E3e-r14-lesson-structure).")
row("E3e-r14-hub-placement-arithmetic", "Placement diagnostic: 8 items, mastery bar 80 percent, 7 of 8 is 87.5 percent",
    "course/modules/E/E3/index.html lines 66-122", "PASS", CARRY_IDX + " arithmetic re-read: 7/8 = 87.5 percent, 6/8 = 75 percent.")
row("E3e-r14-hub-data-and-labs-claims", "Hub claims about data and labs (no real data; labs draw no random numbers in Lessons 1 to 3)",
    "course/modules/E/E3/index.html lines 38 and 154; tests/labs/E3/lab-E3-L01-1.py:15; lab-E3-L03-1.py:4", "PASS",
    CARRY_IDX + " Re-checked this round: lab-E3-L01-1.py line 15 'No random draws are used'; lab-E3-L03-1.py line 4 'No random numbers are drawn'. The L01 twin changed only by the rho-to-Xi rename (E3e-r18-symbol-sweep).")
row("E3e-r14-hub-unlocks-and-titles", "Hub unlocks, project line and lesson titles",
    "course/modules/E/E3/index.html lines 29-36 and 129-136", "PASS", CARRY_IDX + " h1 tags of L01-L08 identical at both pins (checked this round).")
row("E3e-r14-hub-reading-list", "Hub core reading: Lessons 1 to 3 attribute no result to the five works; Pratt named for the name only",
    "course/modules/E/E3/index.html lines 157-167; L02.html references section", "PASS",
    CARRY_IDX + " L02.html byte-identical, so the Pratt reference is unchanged.")
row("E3e-r14-hub-ladder-rungs-3-4", "Hub project ladder (rungs 3 and 4) against project.html ladder and spec",
    "course/modules/E/E3/index.html lines 140-148 vs project.html ladder", "PASS",
    CARRY_IDX + " project.html changed in this delta only at its estimation and exemplar lines (other slice); the ladder rung wording did not change (the project.html hunks at lines 224, 648, 661 and 713 are outside the ladder).")
row("E3e-r14-hub-lesson-titles-match", "Hub lesson titles match the h1 of L01-L08", "course/modules/E/E3/index.html lines 129-136 vs L01-L08.html h1", "PASS",
    CARRY_IDX + " h1 tags identical at both pins (python check this round, ledgers/E3/scripts/E3-e-r18/out/hub_h1_check.out, from structure_compare.py).")
row("E3e-r14-hub-E1-M4-released-claim", "Hub sentence on concept-index status of E1 and M4 (index.html:63)",
    "course/modules/E/E3/index.html:63", "PASS",
    CARRY_IDX + " build_site --check current this round (site data current, 6 outputs).")
row("E3e-r14-hub-rung1-generated-participant", "Hub rung-1 description of the generated participant (index.html:144) against project.html:44",
    "course/modules/E/E3/index.html:144; project.html:44", "PASS", CARRY_IDX + " project.html:44 unchanged in this delta (project.html hunks are at lines 224, 648, 661 and 713 only).")

# ---- lessons: structure, prose, grades, numbers
row("E3e-r14-lesson-hours", "data-hours on L01-L08 and hub arithmetic (56 lesson hours, 14 project hours)",
    "L01-L08.html data-hours; course/modules/E/E3/index.html data-hours-lessons=56 data-hours-project=14", "PASS",
    "All eight data-hours are 7 at both pins (grep compare identical); 8 x 7 = 56; index data-hours-lessons=56 and data-hours-project=14 identical at both pins.")
row("E3e-r14-lesson-structure", "Lesson structure: sections, blocks, labs, quizzes present and in order",
    "L01-L08.html", "PASS",
    "Tag-count multisets, h1 tags, data-hours and dfn ids of index.html and L01-L08.html are identical at dde0486b and 4540351d (ledgers/E3/scripts/E3-e-r18/out/tag_structure.out, all nine files True). The delta changes text inside existing elements only (the diffs read in full: L01 33 lines, L03 6, L04 1, L05 24, L06 39, L07 1, L08 12 changed lines).")
row("E3e-r14-why-it-matters", "why-it-matters paragraphs match the lesson content",
    "L01-L08.html why-it-matters; L04.html:51 (changed)", "PASS",
    "L04.html:51 changed: 'the second test, second-order dominance, can rank a pair that the first test leaves unranked, and then every nondecreasing concave utility on the support agrees with that ranking (Theorem 2.3)'. Checked: Example 2.6 (L04.html:172-173) has equal means 3000 and no first-order ranking, and I_Y(t)=(t-3000)^+ <= I_X(t) at every t, so Y dominates X in the second order; Theorem 2.3 (L04.html:144-146) gives the concave-utility statement. L01 why-it-matters and the other lessons are byte-identical in that paragraph.")
row("E3e-r14-banned-strings", "Banned strings and check_pages static rules on index and L01-L08",
    "index.html, L01-L08.html", "PASS",
    f"check_pages --all PASS for E3 ({OUT}check_pages.out), which applies the BUILDER_RULES static checks to every E3 page; the process-word scan of the added lines is E3e-r14-process-words.")
row("E3e-r14-process-words", "No process words in learner text (round, verifier, builder, batch, todo, placeholder, reviewer, agent, ruling, fixer, architect)",
    "index.html, L01-L08.html; added lines of the delta (117 lines)", "PASS",
    "Regex scan of the 117 added lines (python, this round) and of the changed pages: no hit for round, verifier, builder, batch, todo, placeholder, reviewer, agent, ruling, fixer or architect.")
row("E3e-r14-filler-and-rhetoric", "No filler or rhetoric added in the delta",
    "L01-L08.html changed lines", "PASS",
    "All 117 added lines of the delta were read in full (diffs of L01, L03, L04, L05, L06, L07, L08 read hunk by hunk). The added prose is the rename, the L01 bullet on finitely many outcomes, the L01 bullet on final amounts, the L04 why-it-matters sentence and the footers. None adds rhetoric.")
row("E3e-r14-concept-dfn-and-links", "dfn[data-concept] and a.concept links resolve (index.html, L01-L08.html)",
    "L01-L08.html; check_dag --all", "PASS",
    f"The dfn ids in L01-L08 are identical at both pins (the only changed dfn-bearing lines, L05.html:65 and L06.html:69, keep id and data-concept); {OUT}check_dag.out 'check_dag E3: PASS'.")
row("E3e-r14-DAG-unlinked-names", "Concepts used outside the prerequisite closure by name or link",
    "index.html, L01-L08.html; check_dag --all", "PASS",
    f"{OUT}check_dag.out PASS. New in L01: the bullet at L01.html:334 names 'reference point' and points to Lesson L06 (Definition 1.1, L06.html:56), a forward pointer that states no result; allowed under the forward-pointer rule (E3e-r14-forward-pointers-allowed).")
row("E3e-r14-forward-pointers-allowed", "Forward mentions in index and L01-L08 are pointers only",
    "index.html, L01-L08.html", "PASS",
    "The delta adds one forward pointer: L01.html:334 to L06 Definition 1.1 (a pointer, no premise). Premise-type forward uses (L03, L07, L08) are deferred LOW (notes).")
row("E3e-r14-grades", "Evidence grades on claims: T with proof, C with lab or study",
    "L01-L08.html data-grade spans; key-results tables", "PASS",
    "No data-grade attribute changed in the delta (grep of added and removed lines: the only data-grade-bearing line changed is the L01 key-results row at L01.html:469, whose grade is still T). Grade counts unchanged: see E3e-r15-footers-registry-claim for the C-graded registry claims.")
row("E3e-r14-quiz-and-explanations", "Quiz answers and explanations match the lesson and the lab output",
    "L01 quiz/explain (L01.html:422, :469), L05 (:538, :547), L06 (:495, :518, :521-527), L08 (:586)", "PASS",
    f"Re-read every changed explanation. L01.html:422 'xi 1/3 utility quadratic mixture_eu 40000 linear_combination 40000 equal True' equals the stdout line in {OUT}lab_exact.out. L05 explanations for Omega give theta = -2 for psi = 2 and theta = 1 when psi = 1/gamma (checked). L06.html:518 gives PV = -100 and L06.html:521-527 describe Remark 2.4 correctly.")
row("E3e-r14-scope-words", "Scope words (only, all, every, always, exactly) in changed prose are computed or hypothesis-bearing",
    "L01.html:334 and :403; L04.html:51; L05.html:131; L06.html:123; L08.html:67", "PASS",
    "L01.html:334 'Every sum in this lesson is finite' (A1) and 'states no result for a lottery with a continuum of outcomes' (P3 at L01.html:403 shows the step that fails); L04.html:51 'every nondecreasing concave utility' is Theorem 2.3; L05.html:131 'exactly when' is the algebra of Remark 3.1; L06.html:123 'exactly when' follows from the monotone argument in the same remark. Each is computed or cited.")
row("E3e-r14-plan-rulings-6-8", "Plan section 10 Q6 to Q8 and section 4 symbol rules", "plans/E3-build-plan.md sections 4 and 10", "PASS",
    CARRY_PLAN + " plan section 4 table still says never rho, never R_f, never T; the renames (Xi for the mixture weight) follow it (E3e-r18-symbol-sweep).")
row("E3e-r14-notation-registry", "Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) absent from E3 pages; registered macros used",
    "notation/notation.json vs index.html, L01-L08.html", "PASS",
    f"{OUT}symbol_sweep.out: no hit for T, Phi, Q, R_f, gamma_3, gamma_4 or R^*. Raw forms of registered macros (\\mathbb{{E}}, \\mathbb{{R}}, \\mathbb{{Q}}, \\operatorname{{Var}}, \\operatorname{{Cov}}) absent (grep this round). \\mathcal{{P}} (priors, plan section 4) is not a registered macro and is not listed as forbidden. notation.json byte-identical since dde0486b.")
row("E3e-r14-cross-lesson-anchors", "Definition ids used by later lessons still exist and keep their text", "L01-L08.html def-ids", "PASS",
    "The dfn ids are identical at both pins; check_dag --all PASS (above). The only dfn-bearing changes keep ids (def-epstein-zin-preferences, def-prospect-theory).")
row("E3e-r14-open-items-deviations", "Lessons 7 and 8 against plans/E3-open-items.md sections 1 to 6", "L07.html, L08.html; plans/E3-open-items.md", "PASS",
    CARRY_L07 + " plans/E3-open-items.md byte-identical; L08 changes are symbol renames only (E3e-r18-symbol-sweep).")
row("E3e-r14-plan-lesson-guidance", "Lesson guidance (plan section 5) and the ban on convex or convexity in L06 (ruling 29)", "L01-L08.html; plans/E3-build-plan.md section 5", "PASS",
    CARRY_PLAN + " grep -i convex over L06.html: no match (ledgers/E3/scripts/E3-e-r18/out/symbol_sweep.out has the scan basis).")
row("E3e-r14-L01-numbers", "L01 numbers: Example 1.4, Example 3.4, Misconceptions, Problems, quiz, lab expected block",
    "course/modules/E/E3/L01.html; tests/labs/E3/lab-E3-L01-1.py", "PASS",
    f"numeric_delta: L01 changed-line numeric tokens unchanged (added-only tokens '1.1' x2 and '6' are the new cross-references, all on L01.html:334). Lab expected block equals stdout ({OUT}lab_exact.out). Mixture algebra re-derived: weights sum to Xi + (1-Xi) = 1 (Proposition 2.2 proof).")
row("E3e-r14-L02-numbers", "L02 numbers (carried)", "course/modules/E/E3/L02.html", "PASS",
    CARRY_L02 + " L02 is not in the delta. Its numbers are the same as in round 15 and in the lab output.")
row("E3e-r14-L02-lab-claims", "L02 lab section claims (carried)", "course/modules/E/E3/L02.html lab section", "PASS",
    CARRY_L02 + " L02 twin and page not changed.")
row("E3e-r14-L03-numbers", "L03 numbers: Example 2.5, Proposition 2.6 examples, Problems, Lab expected block",
    "course/modules/E/E3/L03.html; tests/labs/E3/lab-E3-L03-1.py", "PASS",
    f"numeric_delta: no numeric token changed in L03. Lab expected block equals stdout exactly ({OUT}lab_exact.out, L03: 19 lines). The L03 twin is unchanged.")
row("E3e-r14-L03-proofs-and-citations", "L03 definitions, propositions, theorem and remark after the iota and check-u renames",
    "L03.html:66-67 (F2), :72-73 (Definition 1.1), :77-83 (Proposition 1.2), :121-122 (proof), :133-134 (Theorem 2.1 proof), :183-184 (Remark 2.8)", "PASS",
    "Re-derived: Proposition 1.2 (w^iota)^b = e^{iota b ln w} = w^{iota b} from ln(e^y)=y; the power rule with iota; the CRRA derivative and Arrow-Pratt measure (proof at :122); Theorem 2.1: g' = 0 gives g = c, K = e^c, u' = K w^{-gamma}, and \\check u = K u_gamma has the same derivative as u by Proposition 1.7, so u = K u_gamma + C. The renamed symbols carry the same meaning in each use. The exponent letter b of Proposition 1.2 is a separate finding (E3e-r18-notation-b).")
row("E3e-r14-L04-theorems", "L04 theorems, lemmas and examples (carried)", "course/modules/E/E3/L04.html", "PASS",
    CARRY_L04)
row("E3e-r14-L05-math", "L05 Definition 1.1, Theorem 1.3, Corollary 1.4, Proposition 2.2 (EIS), Remark 3.1, Theorem 3.2, Corollary 3.3 after the Omega rename",
    "course/modules/E/E3/L05.html:64-86, :116-119, :130-131, :141-142", "PASS",
    "Re-derived with the page's own formulas: Omega = 1 - 1/psi; dV0/dc0 over dV0/dc1 = ((1-beta)/beta)(c0/c1)^{Omega-1} = ((1-beta)/beta)(c1/c0)^{1/psi} since 1 - Omega = 1/psi; so d ln MRS / d ln(c1/c0) = 1/psi and EIS := d ln(c1/c0)/d ln MRS = psi (Definition 2.1 at L05.html:106). Remark 3.1: theta = (1-gamma)/Omega = 1 iff Omega = 1-gamma iff psi = 1/gamma. Theorem 3.2 proof: V0^{1-gamma} = (1-gamma) U under psi = 1/gamma. No numeric token changed (numeric_delta).")
row("E3e-r14-L05-lab-claims", "L05 lab claims and expected block after the Omega rename", "course/modules/E/E3/L05.html lab; tests/labs/E3/lab-E3-L05-1.py", "PASS",
    f"Page code equals twin; twin run exit 0 with empty stderr; expected block equals stdout exactly ({OUT}lab_exact.out, L05: 23 lines). The refusal message 'the exponent Omega = 1 - 1/psi is zero' is printed as the expected block shows.")
row("E3e-r14-L06-math", "L06 Definition 1.2-1.3, Propositions 2.1-2.2, Examples, Remarks 2.4-2.5 and 3.1-3.2 after the PV rename",
    "course/modules/E/E3/L06.html:63-69, :93-123, :127-131, :284-290", "PASS",
    "Re-derived: PV(lambda) = p g - (1-p) lambda l, slope -(1-p) l < 0, zero at lambda* = p g/((1-p) l), Example 2.3 gives lambda* = 5/3 and PV = 200, 50, -100 at lambda 1, 3/2, 2. Remark 2.5: combined 700 - 300 lambda (= 100 at lambda 2), separate 2(500 - 300 lambda) (= -200). Remark 3.2: for p = 1/2 and 800/800 the threshold is 1. Only the symbol changed (numeric_delta: no numeric token changed).")
row("E3e-r14-L06-lab-claims", "L06 lab claims and expected block after the PV rename", "course/modules/E/E3/L06.html lab; tests/labs/E3/lab-E3-L06-1.py", "PASS",
    f"Page code equals twin; twin exit 0, empty stderr; expected block equals stdout exactly ({OUT}lab_exact.out, L06: 18 lines). The hypothesis paragraph (L06.html:133) predicts the printed PV values.")
row("E3e-r14-L07-numbers", "L07 numbers (carried)", "course/modules/E/E3/L07.html", "PASS", CARRY_L07 + " numeric_delta: no number changed in L07.")
row("E3e-r14-L07-prop-and-examples", "L07 Proposition 2.2, Remark 1.3, Remark 1.6, examples (carried)", "course/modules/E/E3/L07.html", "PASS", CARRY_L07)
row("E3e-r14-L07-lab-claims", "L07 lab claims (carried)", "course/modules/E/E3/L07.html lab", "PASS", CARRY_L07 + " L07 twin not changed; run_labs PASS for L07 this round.")
row("E3e-r14-L08-numbers", "L08 numbers: Model 1 and Model 3 (101951.2195), examples, Section 4 table, Problems",
    "course/modules/E/E3/L08.html; tests/labs/E3/lab-E3-L08-1.py", "PASS",
    f"numeric_delta: no L08 numeric token changed. Model 3 text ('Here Omega = 1 - 1/psi = -1') is consistent with psi = 1/2. Lab expected block equals stdout exactly ({OUT}lab_exact.out, L08: 25 lines), including the 101951.2195 value.")
row("E3e-r14-L08-math", "L08 Definition 3.1, assumptions, Proposition 3.2 proof, Remark 3.3 and the Problem solution after the Omega rename",
    "course/modules/E/E3/L08.html:141-160, :585-587", "PASS",
    "Proof re-read: the sure plan and the gamble give V0 = [(1-beta)c0^Omega + beta c^Omega]^{1/Omega} and [(1-beta)c0^Omega + beta K]^{1/Omega}; since Omega != 0 and the bases are positive, c^Omega = K and c = (E c1^{1-gamma})^{1/(1-gamma)}. The Problem solution's Z1 formula is the same with Omega (checked).")
row("E3e-r14-L08-lab-claims", "L08 lab claims and expected block after the omega rename of ez_value", "course/modules/E/E3/L08.html lab; tests/labs/E3/lab-E3-L08-1.py", "PASS",
    f"Page code equals twin; twin exit 0, empty stderr; expected block equals stdout exactly ({OUT}lab_exact.out).")
row("E3e-r14-L02-prop3.1-undefined-q", "L02 Proposition 3.1 and the undefined q (carried)", "course/modules/E/E3/L02.html:195-199", "PASS", CARRY_L02)
row("E3e-r14-notation-v", "Symbol v: one meaning across E3 (value function v in L06-L08; affine transform is tilde u in L01-L03)",
    "L01.html:148, L02.html:149, L03.html:174 (now tilde u); L03.html:184, :432 (generic real argument); L06-L08 value function", "PASS",
    f"{OUT}symbol_sweep.out: v no longer names the affine transform in L01 to L03 (they use tilde u = a + b u and tilde u = phi u + varsigma). v is the value function in L06 (Definition 1.2), L07 (Definition 1.2) and L08 (Model 2). L03 Remark 2.8 uses v for a generic real number to be rounded (L03.html:184, :432); that is a local letter and is recorded as a note, not a FAIL.")
row("E3e-r14-notation-eps", "Symbol epsilon: EIS is psi; the wealth scale is varepsilon only in L02",
    "L05.html (EIS = psi), L02.html:164-217 (varepsilon scale)", "PASS",
    f"{OUT}symbol_sweep.out and greek_sweep.out: \\varepsilon appears only in L02 (63 math-segment hits; the sampled uses at L02.html:51 and :164 are the wealth scale); L05 uses psi for the EIS (L05.html:131, :142). No collision remains.")
row("E3e-r14-DAG-convexity-term", "L06 says u'' >= 0 as L02 states concavity; no convex or convexity term (ruling 29)", "L06.html:74, :133, :247, :272, :431, :438, :460", "PASS",
    "grep -i 'convex' over L06.html: no match (this round). The u'' >= 0 statements are the same as in round 15.")
row("E3e-r14-contested-counter-side", "Contested-claim sentences name the open question and cite no magnitude (carried)", "L06.html:298; L07.html:52, :324", "PASS", CARRY_L07 + " L06.html:298 is not in the delta hunks.")

# ---- round-15 FAIL and notation rows
row("E3e-r15-footers-registry-claim",
    "Footer claim on L05-L08: 'Each graded result carries a proof or a lab result labelled C.' holds for every graded result",
    "course/modules/E/E3/L07.html:571 (footer), L08.html:725 (footer); C-graded registry-title claims at L07.html:80 and :463, L08.html:67, :133, :620-621",
    "FAIL",
    "L05.html:620 and L06.html:545 satisfy the sentence: their C results are lab results (L05.html:351, :500-502; L06.html:278, :441) and their T results carry a Proof block or an inline argument (ledgers/E3/scripts/E3-e-r18/out/graded_claims.out). L07 and L08 do not: L07.html:80 ('The name prospect theory appears in the title of the 1979 paper by Kahneman and Tversky', data-grade C, data-cite kahneman1979prospect, data-locator 'registry record: title only; paper not read'), L08.html:67 (gilboa1989maxmin) and L08.html:133 (ellsberg1961risk) are the same kind of claim, and L07.html:463, L08.html:620-621 repeat them in the grade tables. None is a proof or a lab result. The grade legend defines C as 'single study' (L07.html:47, L08.html:47). So the footer is false on L07 and L08.",
    "On L07 and L08, either (a) regrade the registry-title claims as ungraded naming sentences, as L05.html:609 and L06.html:534 already do ('this page has not read the paper and cites it for no result'), removing data-grade and data-cite from the three claims and the C rows from the two grade tables, or (b) change the L07 and L08 footers to name the registry-title exception. Then re-run check_pages, page_smoke for L07 and L08, and run_labs.")
row("E3e-r15-notation-a", "Symbol a: one meaning across E3 after the Omega and iota renames",
    "L01.html:133-153, :326, :397, :470, :503, :512; L02.html:149, :407, :525, :582, :586; L07.html:323, :429-431",
    "PASS",
    f"{OUT}symbol_sweep.out: a occurs only as the affine constant of tilde u = a + b u (L01, L02) and of the weighting function omega(p) = a + bp (L07, :429-431). The Epstein-Zin exponent is now Omega (L05, L08) and the generic real exponent of L03 is iota (L03.html:67-122), so the three-meaning collision of round 15 is gone. a is absent from L03, L05 and L08 (sweep).")
row("E3e-r15-notation-W", "Symbol W: one meaning across E3 after the L06 rename to PV",
    "L02.html:136, :164, :209, :214, :217, :319, :420-422, :558; L06.html:69-133 (now PV)", "PASS",
    f"{OUT}symbol_sweep.out: W occurs only in L02 (wealth lottery W = w + eps X, W pays 40, 100, 160 CU, etc.). L06 uses \\mathrm{{PV}} throughout (30 hits, Definition 1.3 onward); no W remains in L06. The word 'present value' (index.html placement question, 100/1.1) is a phrase, not the symbol; noted, not a FAIL.")

# ---- new rows for this round
row("E3e-r18-lab-exact", "Changed labs: page code equals twin, twin output exact, expected block equals stdout",
    "course/modules/E/E3/L01.html, L03.html, L05.html, L06.html, L08.html; tests/labs/E3/lab-E3-L01-1.py, L03, L05, L06, L08", "PASS",
    f"{OUT}lab_exact.out: for each lab, page code == twin True, exit 0, stderr_bytes 0, expected[0] == stdout True (L01 1479 chars, L03 1319, L05 1222, L06 1050, L08 1987).")
row("E3e-r18-numeric-delta", "Numeric tokens in the delta: removed versus added",
    "course/modules/E/E3/L01, L03-L08 and the four changed twins", "PASS",
    f"{OUT}numeric_delta.out: no numeric token removed in any changed file. Added-only tokens: L01 '1.1' x2 and '6' (new cross-references, all on L01.html:334), L04 '2.3' (Theorem 2.3, L04.html:51); all checked. L08 removed 12 added 13 lines, a docstring rewrap with no number changed.")
row("E3e-r18-symbol-sweep", "Renamed symbols: Xi (L01), Omega (L05, L08), PV (L06), iota and check u (L03), rho/tau/eta/epsilon/W/tilde-u collisions gone",
    "ledgers/E3/scripts/E3-e-r18/out/symbol_sweep.out and greek_sweep.out over index.html and L01-L08.html math segments", "PASS",
    "rho: no hit in any E3 page. tau: only L08 (alpha-MEU weight, L08.html:65-80). eta: only L07 (weighting exponent). epsilon: only L02. W: only L02. The new names occur only where the lesson uses them (Xi: L01 only, 23 hits; Omega: L05 32 and L08 15; PV: L06 30; iota: L03 11; \\check: L03:134 only). \\tilde u is the affine transform in L01 to L03 (L03.html:174-179, :393). The collisions the rulings named are gone; the residual letter b and the case pair Xi/xi, Omega/omega are separate FAIL rows.")
row("E3e-r18-katex-render", "KaTeX strict parse of every changed expression (\\check, \\Xi, \\Omega, \\iota, \\mathrm{PV})",
    f"{OUT}page_smoke_E3.out", "PASS",
    "page_smoke E3 PASS for index.html and L01-L08.html: 'zero unrendered math' and every rendered expression re-parses with KaTeX throwOnError strict (BUILDER_RULES page_smoke contract). No .katex-error reported.")
row("E3e-r18-footers-L05-L06", "Footers on L05 and L06 with the new sentence",
    "course/modules/E/E3/L05.html:620, L06.html:545", "PASS",
    f"The sentence is true for L05 and L06 ({OUT}graded_claims.out). L05: its 6 T claims (Theorem 1.3, Corollary 1.4, Proposition 2.2, Remark 3.1, Theorem 3.2, Corollary 3.3) each have a Proof block after them; its 4 C-graded results (L05.html:351, :500, :501, :502) are Lab 1 results. L06: its 8 T claims are Proposition 1.4, Remark 1.5, Propositions 2.1 and 2.2 (each followed by a Proof block) and Remarks 2.4, 2.5, 3.1, 3.2 (no Proof block; inline arguments at L06.html:123, :127-131, :284-287, :289-291, which compute or cite the proved Propositions); its 2 C-graded results (L06.html:278, :441) are Lab 1. Judgment: an inline argument that cites or computes counts as the proof. No registry-title C claim on L05 or L06; the naming sentences at L05.html:609 and L06.html:534 are ungraded.")
row("E3e-r18-footers-L01-L04", "Footers on L01 to L04 unchanged and still true",
    "course/modules/E/E3/L01.html:576, L02.html:627, L03.html:575, L04.html:728", "PASS",
    "Footer sentence identical to the L05 to L08 footers (grep). L01 and L02 have no C-graded claim (only the legend at L01.html:46 and L02.html:46). L03's C-graded results are L03.html:326 and :476 and L04's are L04.html:485 and :633, each a Lab 1 result (grep); no data-cite attribute appears in L03 or L04.")
row("E3e-r18-L01-prose", "L01 new prose: finitely many outcomes (P3), final amounts (Definition 1.1, L06 Definition 1.1 pointer)",
    "course/modules/E/E3/L01.html:334; L01.html:58-60 (Definition 1.1); L01.html:403-410 (P3); L06.html:56-58 (Definition 1.1)", "PASS",
    "P3 (L01.html:403, 'Why the sums are finite under A1') gives the countable counterexample x_i = 2^i, p_i = 2^{-i}, u(x)=x with divergent sum, which is the step the sentence names. Definition 1.1 (L01.html:58-60) fixes outcomes as final amounts in CU, so the bullet is accurate. L06 Definition 1.1 (L06.html:56-58) is the reference-point definition, so the pointer is accurate.")
row("E3e-r18-index-carry-basis", "Hub carry basis: index.html and every fact the hub cites are unchanged since dde0486b",
    "course/modules/E/E3/index.html", "PASS",
    "git diff --stat dde0486b 4540351d -- course/modules/E/E3/index.html: empty (byte-identical). The hub's cited facts (hours, h1 titles, dfn ids, definition numbers used in the skill checks: L01 Definition 1.3, L02 Definition 1.2) are identical at both pins (python compare this round).")

# ---- notation FAILs found this round
row("E3e-r18-notation-b",
    "Symbol b: one meaning across E3 (affine slope in L01-L02, L07; generic real exponent in L03 Proposition 1.2)",
    "affine slope: L01.html:133, :138, :148, :153, :397-399; L02.html:149, :154, :159, :407; L07.html:431 (a + b = 1). Exponent: L03.html:78 (Proposition 1.2: 'For w > 0 and real iota, b: (w^iota)^b = w^{iota b}') and :83 (proof)",
    "FAIL",
    f"{OUT}symbol_sweep.out: b has 32 hits in L01, 11 in L02, 4 in L03, 10 in L04, 3 in L07. In L01 and L02 b is the slope of an affine transform (tilde u = a + b u, b > 0). In L03 Proposition 1.2 and its proof b is a real exponent, and L03.html:90 in the same lesson cites b = 1 for the L02 slope. Same pattern as the round-15 row E3e-r15-notation-a, which FAILed the affine constant a against the generic exponent (L03.html:78). Ruling 29 and 33 did not rename b, so it stays open under the one-meaning rule.",
    "Rename the exponent b of Proposition 1.2 and of its proof (L03.html:78, :83) to a letter used nowhere in E3 pages, cards and twins (grep -i for the candidate first). No lab twin uses the exponent. Re-run check_pages for L03 and page_smoke for L03.")
row("E3e-r18-notation-ruling33-letters",
    "Ruling 33 asks for letters used nowhere else in E3: Xi (L01) and Omega (L05, L08) share their lowercase letters with xi (L02) and omega (L07)",
    "L01.html:86-119, :390-392, :406, :422, :469 (Xi); L05.html:65-173, :400-547 and L08.html:142-160, :447, :587 (Omega); L02.html:113, :115, :131 (xi, point in the proof of Proposition 1.3); L07.html:60-84, :379, :429-431 (omega, weighting function)",
    "FAIL",
    f"{OUT}greek_sweep.out and symbol_sweep.out. The uppercase Xi and Omega are new, but the lowercase xi (L02.html:113) and omega (L07.html:60-84) are in use in E3, and ruling 33 asks for letters used nowhere else in E3 (grep pages, cards and twins first). Read exactly as glyphs, Xi and Omega appear nowhere else as symbols, and this row would be PASS. Judgment: the verdict follows the wording of ruling 33. The architect decides.",
    "If the architect keeps the ruling wording, choose letters with no upper or lower case in E3 pages, cards and twins (grep -i), rename Xi in L01 (Definition 2.1, Propositions 2.2 and 2.3, their proofs, Problem P1 and E2, and the key-results table) and Omega in L05 and L08 (including the L05 lab docstring and the expected block, which carries the refusal message), and re-embed the L05 lab with tools/embed_labs.py --refresh. If the architect accepts glyph-level distinctness, record that decision in plans/FINAL-ARCHITECT-RULINGS.md and this row is PASS.")

rows_sorted = rows
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows_sorted:
    counts[r["status"]] += 1
ids = [r["id"] for r in rows_sorted]
assert len(ids) == len(set(ids)), "duplicate ids"

notes = [
    "Delta dde0486b..4540351d inside the slice: L01.html (rho to Xi, notation, two prose bullets, Problem P3 and E2 text), L03.html (F2, Definition 1.1, Proposition 1.2, proof of its derivative and of Theorem 2.1: iota and check u), L04.html:51 (why-it-matters), L05.html (Omega rename, footer), L06.html (W to PV rename, footer), L07.html:571 (footer), L08.html (Omega rename, footer), and the twins tests/labs/E3/lab-E3-L01-1.py, lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py. index.html and L02.html are byte-identical to dde0486b; so are references/, notation/notation.json and plans/E3-build-plan.md.",
    "Rows re-run this round on the pin: check_pages, check_dag, check_projects, run_labs (E3 11/11), page_smoke (E3 PASS), the exact expected-block check of L01, L03, L05, L06, L08, ruff and mypy on the four changed twins, verify_refs --offline (560 entries, 0 problems), build_site --check, and the relevant pytest subset (474 passed). Outputs are in ledgers/E3/scripts/E3-e-r18/out/.",
    "Carried rows (prefix 'Carried from round 15'): hub index rows, L02 rows, L04 theorem rows, L07 content rows, references and plan rows, and the live Crossref row. Each carry names its byte-identical subject; for L04 and L07 the changed line is re-verified in its own row.",
    "Deferred LOW forward-premise notes (architect ruling 29; plans/KNOWN-ISSUES.md), not rows and not in the verdict, carried from round 15 and not re-counted this round: L03.html:90 cites Proposition 2.7 (stated at L03.html:173); L03.html:107 cites Proposition 1.7 (stated at L03.html:116); L07.html:101 uses lotteries A and B defined at L07.html:109-110; L08.html:85, :90, :113, :132, :138 use the Section 4 gamble defined at L08.html:432.",
    "Judgment note, not a FAIL (same class as K, c, M, L of round 14): the exponent c of Proposition 1.2 (L03.html:78) and the constant c of the Theorem 2.1 proof (L03.html:134) and the certainty equivalent c (L03.html:144, :179, :393) are local letters within L03. The letter v of L03 Remark 2.8 (L03.html:184, :432) is a generic real argument; the value function v is used in L06 to L08. Recorded for the architect under ruling 29.",
    "Judgment note: PV is also the usual abbreviation of present value. The hub placement question (index.html, the 100/1.1 item) uses the words 'present value'; no page uses the symbol PV for it.",
    "Stale document (not in slice e, not edited): plans/KNOWN-ISSUES.md lines 25 to 28 still list W, a, tau and eta as open collisions. W, a (Epstein-Zin), eta and tau are resolved in the pages now; tau in L01 is Xi. The architect may want the list updated.",
    "Outside slice e, observed only: project.html and course/modules/E/E3/grader/reference.py changed in this delta; cards.json changed (renamed symbols are consistent with the pages: E3-c005, c008, c037, c078, c100, c145). Not judged here.",
    "Not checked: run_graders (project grader; another slice); mutate_graders (slice e has no grader and no grader mutants); live verify_refs and live Crossref (references unchanged, not re-run online); the full pytest suite and the full ruff/mypy run (targeted subsets only, as the rule of the round asks); page_smoke figure sweep (skipped with --skip-sweep; E3 has no live figure); the 97 T-grade proofs were not each re-read this round, only the changed ones and the footer-relevant grade structure.",
    "Mutants: none. Slice e has no grader, so the mutation rule does not apply to it.",
]

fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 18,
    "verifier": "Haiku independent verifier, E3-e round 18 closing delta (did not build E3)",
    "pin": "4540351d (detached checkout /Users/billyribeiro/.fanout/wt/verifyD18-E3-e)",
    "base": "dde0486b (round-15 pin; round-15 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round15.json, verdict FAIL with 3 rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD18-E3-e",
    "scratch": "/tmp/e3e_r18/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows_sorted,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {"pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": 0, "mutants_killed": 0,
                "rows": len(rows_sorted), "deferred_low_notes": ["E3e-r14-L03-forward-premise", "E3e-r14-L07-forward-premise", "E3e-r14-L08-forward-gamble"]},
}
out = ROOT / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(counts, len(rows_sorted))
