# AC4 open items (project, Builder E)

Scope: `course/modules/AC/AC4/project.html`, `course/modules/AC/AC4/grader/` (instance, reference, starter,
test suite), `tests/labs/AC4/lab-AC4-project-1.py` and `lab-AC4-project-2.py`. Written 2026-10-27. Nothing here is
committed or pushed.

## REFERENCE_REQUESTS

None from the project. The reading list names `datar2020horngrens` and `kaplan1998cost`, the two AC4 keys in the
registry, and no project claim depends on a locator in either. Cooper & Kaplan (1988) stays open for L04 under
architect decision Q6; the project does not need it.

## GLOSSARY_REQUESTS

None. The project uses plain terms (flexed budget, sales mix variance, contribution margin) that the lessons define;
it does not define any term with `<dfn>`.

## NOTATION_REQUESTS

None. The page writes its formulas in words and italic symbols (s, F, AQ, BU, AU, bp, ap, q, AT). It uses no KaTeX
macro, so no registry symbol is needed.

## DATA_REQUESTS

None requested. The project's cases are generated and labelled SIMULATED. No real plant data is embedded. A
real-company exercise would need a source whose issuer states that the data may be redistributed; none has been
identified for AC4. This is an honest gap, stated on the page.

## CONTRACT_CHANGE_REQUESTS

None. AC4 has no Atlas milestone (curriculum has no `atlas:` key on the AC4 project; no contract file is written).

## DAG_DEFECTS

None found. The project page defines no concept and links no concept. `check_projects --unit AC4` passes.

## KNOWN_LIMITATIONS

1. **No spending variance.** The case holds the input price and the fixed overhead at budget, so the engine returns
   four variances, not six. Stretch item 1 on the page asks the learner to add the two spending variances.
2. **One input.** The engine has one input type with a common standard price. Stretch item 2 covers two inputs.
3. **One rounding rule.** The flexed revenue and the flexed variable cost are each taken to the nearest cent, halves
   up. The sales mix variance is taken against the rounded flexed profit, so it can differ from the exact fraction by
   less than one cent. Lab 1 prints the difference (1/7 cent). Five correct implementations were checked on seeds
   0 to 49 (see the build report); the rule is stated on the page and in the specification, so none of them is
   tolerance-based.
4. **Suite is not secret.** Integrity comes from the seeded case (BUILDER_RULES §5.3). Expected values are computed in
   the suite from the case's numbers, by an oracle written independently of the reference.
5. **Exemplars are builder-written.** Exemplars A and B and their official scores were written by the builder, and an
   independent verifier has not yet scored them. The annotations describe the scoring; the verifier checks them.
6. **Reading list only.** Both registry sources are named without locators. The project makes no claim that depends
   on either, so no page or table of either source is cited.
7. **Hub hours cross-check.** `check_projects` compares the project's 20 hours with the hub's `data-hours-project`.
   The hub is Builder A's file; the cross-check reads it when it exists.
8. **Page-level check output.** `check_pages.py --unit AC4 --page project` also applies the lesson rules to
   `project.html` (missing sections, misconceptions, "mark complete"). The same messages appear for AC2's
   `project.html`, so they are a property of the tool's page filter, not of this page. The common checks (banned
   phrases, duplicate ids, the hours header, citations) report nothing for this page.
9. **Learner text checked for process words** (build, builder, round, verifier, REQUESTS, unit report) with no hit in
   the page or in the grader files as learner-visible text. The grader's type annotation `tuple[str, ...]` contains
   an ellipsis in code, not in prose.
