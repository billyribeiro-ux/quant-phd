#!/usr/bin/env python3
"""Check a unit's project page against BUILDER_RULES §5.

* the four-rung ladder in order (worked example, completion problem,
  independent project, stretch); studios carry rung 3 only
* rung 2 is graded instantly: a completion lab (``.lab.completion``) or a quiz
* the specification names context, inputs, required outputs, constraints and
  the grading mode, and the grading mode matches the curriculum: autograder,
  rubric, or both (BLUEPRINT §5.2), in which case the entry names both
* the time budget's components sum to the declared project hours, which equal
  the hub's figure
* autograded projects: a grader panel whose files exist, an instance generator
  exposing ``make_instance``, a reference solution and a starter
* rubric-graded projects: 4-7 criteria with four observable levels, exemplars
  at two or more levels, and, for adversarial projects, a question bank of at
  least 15 attack angles
* Atlas milestones: the contract ``atlas/<A-ID>.contract.md`` exists
* a reading list of registry keys

Usage::

    python3 tools/check_projects.py --unit S7
"""

from __future__ import annotations

import argparse
import re
import sys

from coursekit import ROOT, Unit, built_units, load_page, registry_keys, unit

RUNGS = ("worked example", "completion", "independent", "stretch")
SPEC_TERMS = ("context", "inputs", "required outputs", "constraints", "grading")


# What the spec's grading entry must say for each curriculum grading mode (BLUEPRINT §5.2).
GRADING_WORDS = {"autograder": ("autograd",), "rubric": ("rubric",), "both": ("autograd", "rubric")}


def grading_problems(grading: str, mode: str) -> list[str]:
    """The spec's grading entry must name the curriculum's mode; for "both", the autograder and the rubric."""
    text = mode.lower()
    missing = [word for word in GRADING_WORDS.get(grading, ()) if word not in text]
    if not missing:
        return []
    if grading == "both":
        named = " and ".join("autograder" if w == "autograd" else w for w in missing)
        return [f"the curriculum grades this project by both autograder and rubric; the spec must name the {named}"]
    return [f"the curriculum grades this project by {grading}; the spec must say so"]


def number(text: str) -> float | None:
    found = re.search(r"\d+(?:\.\d+)?", text)
    return float(found.group()) if found else None


def check_unit(u: Unit) -> list[str]:
    path = u.directory / "project.html"
    if not path.exists():
        return ["project.html is missing"]
    page = load_page(path)
    problems: list[str] = []
    project = u.entry["project"] if u.kind == "module" else u.entry
    grading = project["grading"]

    ladder = page.dom.first("ol", "ladder")
    titles = [n.text().lower() for n in ladder.select(None, "rung-title")] if ladder else []
    expected = RUNGS if u.kind == "module" else ("independent",)
    if len(titles) < len(expected) or any(r not in t for r, t in zip(expected, titles, strict=False)):
        problems.append(f"the ladder must list the rungs {expected} in order (found {titles})")
    if u.kind == "module" and not (page.dom.select("section", "completion") or page.dom.select("section", "quiz")):
        problems.append("rung 2 must be graded instantly: add a completion lab (section.lab.completion) or a quiz")

    spec = page.dom.first("dl", "spec")
    terms = [n.text().strip().lower() for n in spec.select("dt")] if spec else []
    for term in SPEC_TERMS:
        if not any(term in t for t in terms):
            problems.append(f"the specification has no '{term}' entry")
    pairs = zip(spec.select("dt"), spec.select("dd"), strict=False) if spec else iter(())
    mode = next((dd for dt, dd in pairs if "grading" in dt.text().lower()), None)
    if mode is not None:
        problems.extend(grading_problems(grading, mode.text()))

    main = page.dom.first("main")
    declared = float(main.get("data-hours-project") or "nan") if main else float("nan")
    hub = load_page(u.directory / "index.html").dom.first("main")
    if hub is not None and hub.get("data-hours-project") and float(hub.get("data-hours-project")) != declared:
        problems.append(f"project hours {declared:g} differ from the hub's {hub.get('data-hours-project')}")
    table = page.dom.first(None, None, id="hours")
    rows = table.select("tr")[1:] if table else []
    cells = [[c.text() for c in r.select("td")] for r in rows]
    components = [number(c[1]) for c in cells[:-1] if len(c) > 1]
    total = number(cells[-1][1]) if cells and len(cells[-1]) > 1 else None
    if not components or total is None:
        problems.append("the time budget (#hours) needs component rows with hours and a total row")
    else:
        if abs(sum(x or 0 for x in components) - total) > 1e-9:
            problems.append(f"time budget components sum to {sum(x or 0 for x in components):g}, total says {total:g}")
        if abs(total - declared) > 1e-9:
            problems.append(f"time budget total {total:g} differs from data-hours-project {declared:g}")
        if any(len(c) < 3 or not c[2].strip() for c in cells):
            problems.append("every time-budget row needs a one-line rationale")

    if grading in ("autograder", "both"):
        grader = page.dom.first("section", "grader-panel")
        if grader is None:
            problems.append("an autograded project needs a grader panel (section.grader-panel)")
        else:
            base = u.directory / grader.get("data-grader")
            for attr in ("data-unit", "data-grader", "data-suite", "data-solution", "data-starter"):
                if not grader.get(attr):
                    problems.append(f"the grader panel needs {attr}")
            names = [grader.get("data-suite"), grader.get("data-starter"), *grader.get("data-support").split()]
            for name in [n for n in names if n] + ["reference.py", "instance.py"]:
                if not (base / name).exists():
                    problems.append(f"grader file {base.relative_to(ROOT) / name} is missing")
            instance = base / "instance.py"
            if instance.exists() and "def make_instance(seed: int)" not in instance.read_text(encoding="utf-8"):
                problems.append("grader/instance.py must define make_instance(seed: int)")
    if grading in ("rubric", "both"):
        rubric = page.dom.first("table", "rubric")
        criteria = rubric.select("tr")[1:] if rubric else []
        if not 4 <= len(criteria) <= 7:
            problems.append(f"the rubric needs 4-7 criteria (found {len(criteria)})")
        for row in criteria:
            if len(row.select("td")) < 4:
                problems.append("every rubric criterion needs four performance levels")
        exemplars = page.dom.select(None, "exemplar")
        if len({e.get("data-level") for e in exemplars}) < 2:
            problems.append("rubric projects need annotated exemplars at two or more levels")
    bank = page.dom.first(None, None, id="question-bank")
    if bank is not None and len(bank.select("li")) < 15:
        problems.append("an adversarial project's question bank needs at least 15 attack angles")

    atlas = project.get("atlas")
    if atlas and not (ROOT / "atlas" / f"{atlas}.contract.md").exists():
        problems.append(f"Atlas milestone {atlas} has no contract atlas/{atlas}.contract.md")
    reading = page.dom.select("ol", "reading-list")
    keys = registry_keys()
    cited = [li.get("data-cite") for r in reading for li in r.select("li")]
    if not cited:
        problems.append("the project page needs a reading list of registry keys (ol.reading-list)")
    problems.extend(f"reading list cites unknown key {k!r}" for k in cited if k not in keys)
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
        print(f"check_projects {u.id}: {'PASS' if not problems else f'FAIL ({len(problems)} problems)'}")
        failed += bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
