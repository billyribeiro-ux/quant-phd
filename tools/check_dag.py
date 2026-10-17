#!/usr/bin/env python3
"""Concept-level checks on built pages: nothing used before it is defined, nothing defined twice.

The curriculum assigns every concept to exactly one module (render_curriculum.py
enforces that). This tool checks that the pages honour the assignment:

* every concept a module introduces is defined on its pages exactly once, with
  ``<dfn data-concept="<id>" id="...">``
* no page defines a concept that its module does not introduce
* every concept link ``<a class="concept" data-concept="<id>">`` points at a
  concept introduced by the module itself or by its prerequisite closure
* a link to one of the module's own concepts never precedes its definition: a
  lesson may not rely on a concept defined in a later lesson

A concept used by name without a link cannot be detected statically; the
verifier reads for it (VERIFIER_RULES §2.9).

Usage::

    python3 tools/check_dag.py --unit S7
    python3 tools/check_dag.py --all
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict

from coursekit import Unit, built_units, concept_owner, load_page, prerequisite_closure, unit


def check_unit(u: Unit) -> list[str]:
    problems: list[str] = []
    owners = concept_owner()
    closure = prerequisite_closure(u.id)
    introduces = set(u.introduces)
    order = [p.stem for p in u.lesson_pages()]
    position = {name: i for i, name in enumerate(order)}
    defined_at: dict[str, list[str]] = defaultdict(list)
    uses: list[tuple[str, str, int]] = []

    for path in u.pages():
        page = load_page(path)
        for dfn in page.dom.select("dfn"):
            concept = dfn.get("data-concept")
            if not concept:
                continue  # plain emphasis of a term that is not a registered concept
            if not dfn.get("id"):
                problems.append(f"{path.name}:{dfn.line}: <dfn data-concept={concept}> needs an id to link to")
            if concept not in owners:
                problems.append(f"{path.name}:{dfn.line}: unknown concept {concept!r}")
            elif concept not in introduces:
                problems.append(
                    f"{path.name}:{dfn.line}: defines {concept!r}, which {owners[concept]} introduces (define once)"
                )
            defined_at[concept].append(path.stem)
        for link in page.dom.select("a", "concept"):
            concept = link.get("data-concept")
            if not concept:
                problems.append(f"{path.name}:{link.line}: concept link without data-concept")
                continue
            uses.append((concept, path.stem, link.line))
            if concept not in owners:
                problems.append(f"{path.name}:{link.line}: unknown concept {concept!r}")
            elif concept not in introduces and owners[concept] not in closure:
                problems.append(
                    f"{path.name}:{link.line}: uses {concept!r} from {owners[concept]}, which is not a prerequisite "
                    "(DAG_DEFECT)"
                )

    for concept in sorted(introduces):
        places = defined_at.get(concept, [])
        if not places:
            problems.append(f"{concept!r} is introduced by {u.id} but never defined with <dfn> on its pages")
        elif len(places) > 1:
            problems.append(f"{concept!r} is defined {len(places)} times ({', '.join(places)}); define it once")
    for concept, page_name, line in uses:
        if concept in introduces and defined_at.get(concept):
            home = defined_at[concept][0]
            if page_name in position and home in position and position[page_name] < position[home]:
                problems.append(f"{page_name}.html:{line}: uses {concept!r} before {home} defines it")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true")
    args = parser.parse_args()
    targets = built_units() if args.all else [unit(args.unit)]
    failed = 0
    for u in targets:
        problems = check_unit(u)
        for problem in problems:
            print(f"FAIL {u.id}: {problem}")
        print(f"check_dag {u.id}: {'PASS' if not problems else f'FAIL ({len(problems)} problems)'}")
        failed += bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
