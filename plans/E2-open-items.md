# E2 open items (Builder B: L04, L05, L06)

- Cross-links to unbuilt pages: L04 links `L03.html#def-adverse-selection`, L05 links `L03.html#def-adverse-selection` and `L04.html#def-signaling`, L06 links `L05.html#def-screening`, and L06 Next links `L07.html`. These resolve once Builder A (L03) and Builder C (L07) write their pages. `check_dag.py --unit E2` reports `adverse-selection` as never defined, which is Builder A's gap.
- Cards (`cards.json`) for L04-L06 are Builder F's work; none are written here.
- References section is an empty `<ol data-references>`, as in M1. Entries come from `data-cite` at integration.
- Registry attributions are title and year only: `spence1973job` (L04), `rothschild1976equilibrium` (L05), `holmstrom1979moral` (L06), all grade C.
- Fudenberg & Tirole, Akerlof, Nash and Vickrey are not cited by these three lessons.

# E2 open items (Builder C: L07, L08, L09)

- Cross-links to unbuilt pages: L07 links `L01.html#def-nash-equilibrium`, `L02.html#def-bayesian-nash-equilibrium`, `L04.html#def-signaling` and `L05.html#def-screening`; L08 links `L02.html#def-bayesian-nash-equilibrium`; L09 links `L01.html#def-nash-equilibrium`. These anchors must exist when Builders A and B finish. The L07 Assumption 3 text says the one-agent equilibrium condition is the L02 Bayesian-Nash condition with no other players; the verifier should confirm that against the L02 page.
- Concepts defined here: `mechanism-design`, `revelation-principle` (L07); `common-value-auction`, `winners-curse`, `bid-shading` (L08); `uniform-vs-discriminatory-auction` (L09). `check_dag.py --unit E2` reports these as defined; the remaining failures are concepts owned by Builders A, B and D.
- Lessons L07-L09 link `L06.html` (L07 Previous) and `project.html` (L09 Next); both pages are unbuilt at this point.
- Cards (`cards.json` for L07-L09) are Builder F's work; none are written here.
- References sections are empty `<ol data-references>`, as in M1. No outside source is cited. Vickrey (1961) and Milgrom & Weber (1982) are named in L08 §9 by title and year only; no result is attributed to them.
- Grade C rows: the L08 simulation row and the L09 fixed-profile enumeration row are C with the lab as their only basis. Under BUILDER_RULES §2.2 and the M1 L06 precedent, a C row needs a registry key; no key covers these model results. The architect decides whether to accept the lab as the basis.
- REFERENCE_REQUESTS (topics, from the architect's §8.1): empirical evidence on winner's curse behaviour (L08 makes no empirical claim); revelation-principle primary literature for several agents (L07 states only the one-agent finite case).

# E2 open items (Builder A: index, L01, L02, L03)

- `adverse-selection` is now defined on L03 (`<dfn id="def-adverse-selection" data-concept="adverse-selection">`), which resolves the check_dag gap noted above. `check_dag.py --unit E2` passes.
- Lab results are graded C with grade badges (`span.grade`) in the interpretation and key-results table, not as `span.claim` spans with a registry key. No registry key supports a lab result. The architect decides whether the lab is an accepted basis (the same question as the Builder C note above; BUILDER_RULES §2.2).
- Plain `<dfn>` terms without `data-concept` (glossary requests): two-player game in strategic form, profile, best response, strictly dominant action (L01); Bayesian game, pure strategy, interim expected payoff (L02); offered mix, market-consistent price (L03).
- Registry: `fudenberg1991game` has no `print_year` in `references/references.json`, so the hub reading list and L02 give no year for it. The record is cited by key only, with no locator.
- L02 Proposition 2.5 proves the first-price expected revenue and the mean of the second-highest value. It does not claim a second-price revenue, because the second-price rule is not proved in this unit's lessons.
- Hub cards for L04 to L09 use the h1 titles of those pages as of this build. The card summaries were written from the plan outline, not from those pages' text, and the verifier should check them.
- Placement items rely on the payment rule in project.html (uniform price is the (units+1)-th highest bid; discriminatory winners pay their own bid). Both match the current project page.
- `cards.json` is Builder F's work and is missing, which is the only `check_pages.py --unit E2` failure.

# E2 open items (Builder F: cards.json for L01-L09)

- `course/modules/E/E2/cards.json` has 121 cards (E2-c001 to E2-c121), covering every definition, proposition, lemma, remark used as a result, misconception and key-results row of L01-L09. `tools/check_pages.py --unit E2` reports PASS, and `tools/check_dag.py --unit E2` reports PASS.
- Cards carry a `cite` key only where the lesson cites a registry key for a graded claim: `spence1973job` (L04), `rothschild1976equilibrium` (L05), `holmstrom1979moral` (L06), all grade C, title and year only.
- Lesson-text defect, L05 Empirical solution (variant with p_H = 1/3): the menu profit is 6,750,000 cents, not 6,666,667, and the gap to the first best is 2,250,000 cents, not 2,333,333. Recomputed with exact Fractions: menu profit 6750000, first best 9000000, gap 2250000, best low-type quantity 1500. The lab would print these values.
- Lesson-text defect, L08 key-results row 4 (graded T): the discrete E[M] = 1333.67 cents (1333.6666 unrounded) is not derived on the page. Recomputed exactly, E[M] = 1333.66656 (the closed form of Proposition 2.2 summed for n = 5, a = 2000). The card for it is grade C with basis Lab 1, Parts B and C. Remarks 2.3 and 3.2 use the same value. The architect should either show the sum on the page or keep the row at grade C.
- Lab-docstring defect, L07 Lab 1 Part A (twin `tests/labs/E2/lab-E2-L07-1.py` line 8 and line 72): the docstring says "one infeasible menu" and the function says "three feasible-looking menus and one menu that fails individual rationality". The output shows two menus that pass both checks, one that fails IR (`pool_at_high_value`), and one that fails IC (`high_price_for_H_only_trade`). The lesson prose at L07 is correct.
- Lesson-text defect, L07 Remark 1.3: it says IC "compares the truthful report with the other reports of the same type" and "does not compare one type with another type's outcome in isolation". Definition 1.2 quantifies IC over every report r in Theta, which are other types' outcomes. The Remark conflicts with the Definition. No card was written on this sentence.
- Gap, L07 Proposition 3.2: the statement covers c < 0 and c > 0 and is silent on c = 0, where both q_L = 0 and q_L = 1 are optimal (both give revenue p_H v_H = v_L). No card states the c = 0 case.
- Gap, L09 Definition 3.1: the efficiency ratio is undefined when the k highest values sum to 0. The lesson does not say so. No card covers it.
- Plain-prose terms used on cards (no `data-concept`, no new `dfn`): none beyond those the lessons already define.
- Requests: none. No DATA_REQUESTS, REFERENCE_REQUESTS, CONTRACT_CHANGE_REQUESTS or DAG_DEFECTS arise from the cards.
