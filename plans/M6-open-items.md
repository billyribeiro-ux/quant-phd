# M6 open items (Builder A: index, L01–L04)

Status as of Builder A's pass. Items are open until the named owner closes them.

1. **Lesson hours.** `index.html` declares 108 lesson hours. `check_pages.py --unit M6` reports 99 declared until L05–L12 are built (owner: Builders B–E).
2. **Dominated convergence theorem.** Stated in L04 (Theorem 3.1) with its assumptions and no grade, "not proved here", per the architect default for infinite-sample-space results. No locator is cited.
3. **Lab-result grades.** L01–L04 grade lab results C with the lab as basis (Lab 1–4). No registry key exists for a lab, so these C spans cite no key. Architect to confirm this reading of the grade-C rule.
4. **Registry locators.** `billingsley2012probability` and `williams1991probability` are cited at book level only. No locator has been read. The Billingsley edition string is not in the record (plan Q4).
5. **Macros.** L01–L04 use `\E`, `\Prob`, `\N` and `\indic` from `notation/notation.json`, and standard LaTeX commands (`\lfloor`, `\rfloor`, `\min`, `\sqrt`, `\setminus`, `\subseteq`, `\bigcup`, `\dots`, `\text`). The standard commands are not registry macros. Architect to confirm they are allowed.
6. **Lesson titles.** Hub cards for L05–L12 use the plan's working titles. Each lesson's `<h1>` must match its card.
7. **Concept coverage.** L01 defines `sigma-algebra`, L02 `probability-space`, L03 `lebesgue-integral`, L04 `monotone-convergence-theorem` and `dominated-convergence-theorem`. The remaining 10 concepts belong to L05–L12.
8. **Project and grader.** `project.html`, `grader/` and `cards.json` are not written by Builder A. `check_projects.py --unit M6` and the card checks fail until Builders D and E finish.
9. **Pyodide page smoke.** Run once after all lessons are built, not by Builder A beyond its own pages.

# M6 open items (Builder C: L09–L12)

Status as of Builder C's pass. Scope: `course/modules/M/M6/L09.html` to `L12.html` and `tests/labs/M6/lab-M6-L09-1.py` to `lab-M6-L12-1.py`.

1. **Lab-only results carry no grade span.** The plan asked for grade C with the lab as basis on finite enumerations. The C rule (a grade-C span needs a registry key) cannot be met by a computation, because no registry key is the source of a computed fact. The pages state each lab check as printed output and leave it ungraded; the key-results tables list only T rows. Architect to confirm (same question as Builder A item 3).
2. **General martingale convergence (L12, Result 12.6).** The statement for martingales bounded in first moment is stated with its assumptions, not proved, and carries no grade, per the architect default. The page cites no key and no locator. Only the second-moment case (Theorem 12.4) is proved. Architect to confirm that an uncited, ungraded statement is acceptable here.
3. **Infinite horizon.** L08 (Builder B) defines martingales over a finite horizon. L10 and L12 apply the definition for every k ≥ 0, and each says so in its text. Builder B's L08 must not contradict this reading.
4. **Dependencies on other builders' anchors.** L09 links `L08.html#def-filtration`, `L08.html#def-martingale`, `L02.html#def-probability-space`, `L01.html#def-sigma-algebra`. L10 and L12 link `L07.html#def-conditional-expectation-l2` and `concepts.html#expectation`, `cauchy-sequence`, `completeness-of-reals`. All anchors exist in the current tree. L07's residual-orthogonality statement must match the use in L11 and L12 (E[Y(X-Y)] = 0 for every G-measurable Y).
5. **Adaptedness.** L08 defines adaptedness through cells of a finite partition. L09 Proposition 9.5 and L11 use {X_k = b} ∈ F_k and {X_k ≥ λ} ∈ F_k for real-valued processes. The two readings agree on finite spaces, and L11 states the real-valued form in its own text.
6. **Hub and cards.** The hub's lesson map must link L09–L12 (checked by `check_pages --unit M6` once the hub exists). `cards.json` must include lessons L09–L12 (Builder E). Card basis strings for lab results must follow item 1.
7. **Project links.** L12's next-lesson link goes to `project.html`, which Builder D writes.
8. **Labs not in Pyodide.** Each twin runs under CPython in under 0.3 s. No Pyodide timing is claimed; `page_smoke` is the place for it.
9. **Rung text.** L09–L12 contain no rung or project content. Project grading is Builder D's concern.

# M6 open items (Builder D: project, grader, labs, mutants)

Status as of Builder D's pass. Scope: `course/modules/M/M6/project.html`, `course/modules/M/M6/grader/`, `tests/labs/M6/lab-M6-project-1..3.py`, `ledgers/M6/mutants/`, `ledgers/M6/scripts/alternatives/`.

1. **Lesson 12, Theorem 12.4 proof (Builder C's file, line 107).** The step "a bounded nondecreasing sequence converges to its supremum, so \(v_m \to L\)" holds only when \(L\) is the supremum of \(\E[M_n^2]\). The hypothesis gives only an upper bound \(L\). The project's P3 uses \(L^\ast = \lim_n \E[M_n^2] \le L\), which makes the step valid. Owner: Builder C (L12). Architect to decide whether L12 changes its statement or its proof step.
2. **Sixth engine function.** The plan's Q10 froze five signatures. The project adds `dyadic_martingale_value(instance, n, x)`, because the plan's check that path values approach \(Y\) cannot be made through the five functions. Architect to confirm or amend. Reference, tests and the report use it.
3. **Q5 and Q10 answers.** The architect decisions do not state Q5 (deliverable) or Q10 (signatures) explicitly. Builder D followed the plan's §6 as written under the decision "12 lessons and the 42 h project as in the plan". Architect to confirm. The deliverable is `proofs.html` plus `martingale_checks.py` and `report/run_report.py`.
4. **Doob's level is a count of steps.** The plan says the barrier \(\lambda\) is in cents. Doob's process is \(X_k = |S_k|\), a count of steps, so \(\lambda\) is a whole number of steps and no money is involved. Architect to confirm.
5. **Doob uses the fair walk.** `doob_max_probability` always uses \(p = 1/2\), because the bound needs a submartingale. The instance's win probability is not read there.
6. **Doubling stake schedule.** The plan says "a stake schedule in integer cents". The engine uses the doubling schedule \(s \cdot 2^{k-1}\) with one base stake \(s\) per instance. The control's expected final wealth is \(K + s - s\,(2(1-p))^J\), which is not an integer for \(p \ne 1/2\), so the half-up rounding rule is exercised.
7. **Mutants and alternatives were written by Builder D.** The plan (§6.5, §6.6, §16) assigns them to the verifier. The orchestrator's brief asked Builder D to write ten mutants into `ledgers/M6/mutants/` and to check the five alternatives. The verifier should re-derive them independently before the unit ledger. Result now: `mutate_graders.py --unit M6 --seeds 0-9` kills 10/10; all five alternatives pass seeds 0 to 49.
8. **Suite size.** `test_project.py` collects 64 tests. The page quotes 64.
9. **Page smoke.** Run for `project` alone at the end of Builder D's pass (see the report). Not run by Builders A to C for their pages.
10. **Proof of P3 cites Lemma 12.1 and Lemma 12.3 of Lesson 12**, and P2 is the Lesson 11 inequality. The project cites lessons only, and the reading list cites the two registry keys with no locator, as §8 of the plan requires.
11. **Exemplar B's Lab 3 numbers** are the illustrative case, not the seed-0 instance. The report asks students for seed 0. The exemplars say which case they use.
