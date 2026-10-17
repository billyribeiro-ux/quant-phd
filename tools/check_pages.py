#!/usr/bin/env python3
"""Static checks for a unit's pages against BUILDER_RULES §1-§8.

For every page of the unit (hub, lessons, project) this checks:

* page contract: <html lang data-root data-unit data-page>, title, viewport and
  description; only local scripts, stylesheets, images and frames (no CDN);
  unique element ids; images have alt text; inline SVGs have <title> and <desc>
* banned strings (BUILDER_RULES §1.3-1.4) in visible prose, outside code and math
* claims: a valid grade; every non-theorem claim cites; every key is in the
  verified registry; locators are non-empty
* lessons: the section order of §4.2 with its minimum counts (labs with
  hypothesis/code/interpretation, ≥3 misconceptions, ≥3 problems in each of the
  four tiers each with a worked solution, a key-results table, an 8-15 item quiz
  with explanations, a reference list, a debate brief when the curriculum tags
  one); "why it matters" at most 120 words; 6-12 declared study hours
* hub: 4-8 objectives, prerequisites, placement diagnostic, lesson map linking
  every lesson, the four-rung ladder, and an hours split that sums to the
  curriculum figure with the project at 10-40% and lessons summing to the rest
* cards.json: unique ids prefixed by the unit, a lesson that exists, valid
  grades and registry keys

Project pages are checked by check_projects.py; concept usage by check_dag.py.

Usage::

    python3 tools/check_pages.py --unit S7
    python3 tools/check_pages.py --all
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

from coursekit import COURSE, Node, Page, Unit, built_units, load_page, registry_keys, unit, visible_text

GRADES = frozenset("TABCDX")
BANNED = (
    r"\bTODO\b",
    r"\bTBD\b",
    r"\blorem\b",
    r"for brevity",
    r"details omitted",
    r"beyond the scope",
    r"left as an exercise",
    r"you can add more",
    r"it is important to note",
    r"studies show",
    r"experts agree",
    r"it is well known",
    r"\bobviously\b",
    r"\bclearly\b",
    r"\.\.\.",
)
LESSON_SECTIONS = ("why-it-matters", "canon-breaks", "misconceptions", "problems", "key-results", "quiz", "references")
TIERS = ("mechanics", "proof", "empirical", "research")


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def check_common(page: Page, u: Unit, problems: list[str]) -> None:
    where = page.path.name
    root = page.html
    if not root.get("lang"):
        problems.append(f"{where}: <html> needs lang")
    if root.get("data-unit") != u.id:
        problems.append(f"{where}: data-unit must be {u.id}")
    depth = len(page.path.relative_to(COURSE).parts) - 1
    if root.get("data-root") != "../" * depth:
        problems.append(f"{where}: data-root must be {'../' * depth!r}")
    title = page.dom.first("title")
    if title is None or not title.text().strip():
        problems.append(f"{where}: missing <title>")
    metas = {m.get("name") for m in page.dom.select("meta")}
    for name in ("viewport", "description"):
        if name not in metas:
            problems.append(f"{where}: missing <meta name={name}>")
    for node in page.dom.iter():
        for attr in ("src", "href"):
            value = node.get(attr)
            embedded = node.tag in ("script", "link", "img", "iframe", "source", "audio", "video")
            if embedded and value and re.match(r"^(https?:)?//", value):
                problems.append(f"{where}:{node.line}: external {node.tag} {attr}={value} (vendor it)")
        if node.tag == "iframe":
            problems.append(f"{where}:{node.line}: iframes are not allowed")
        if node.tag == "img" and not node.get("alt"):
            problems.append(f"{where}:{node.line}: <img> without alt text")
        if node.tag == "svg":
            kids = {c.tag for c in node.children if isinstance(c, Node)}
            if not {"title", "desc"} <= kids:
                problems.append(f"{where}:{node.line}: inline <svg> needs <title> and <desc>")
    ids = Counter(n.get("id") for n in page.dom.iter() if n.get("id"))
    problems.extend(f"{where}: duplicate id {i!r}" for i, n in ids.items() if n > 1)

    check_figures(page, problems)
    check_code(page, problems)

    text = visible_text(page.dom.first("main") or page.dom)
    for pattern in BANNED:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            context = text[max(0, match.start() - 40) : match.end() + 40].replace("\n", " ")
            problems.append(f"{where}: banned phrase {match.group()!r} in “…{context.strip()}…”")

    keys = registry_keys()
    for node in page.dom.select(None, None, data_cite=None):
        cited = node.get("data-cite").split()
        if not cited:
            problems.append(f"{where}:{node.line}: empty data-cite")
        for key in cited:
            if key not in keys:
                problems.append(f"{where}:{node.line}: unknown citation key {key!r} (not in the verified registry)")
        if "data-locator" in node.attrs and not node.get("data-locator").strip():
            problems.append(f"{where}:{node.line}: empty data-locator")
    for claim in page.dom.select(None, "claim"):
        grade = claim.get("data-grade")
        if grade not in GRADES:
            problems.append(f"{where}:{claim.line}: claim grade {grade!r} is not one of T A B C D X")
        elif grade != "T" and not claim.get("data-cite"):
            problems.append(f"{where}:{claim.line}: a grade-{grade} claim must cite registry keys")


def check_code(page: Page, problems: list[str]) -> None:
    """Python on a page has run: it is a lab (data-run) or a checked snippet (data-check) with its output."""
    where = page.path.name
    outputs = {n.get("data-check") for n in page.dom.select("pre", "expected", data_check=None)}
    for code in page.dom.select("code", "language-python"):
        if "data-run" in code.attrs:
            continue
        name = code.get("data-check")
        if not name:
            problems.append(
                f"{where}:{code.line}: Python code must be a lab or a checked snippet "
                '(data-check="sol-<UNIT>-<page>-<id>"); label pseudocode class="language-pseudocode"'
            )
        elif name not in outputs:
            problems.append(f'{where}:{code.line}: snippet {name!r} has no <pre class="expected" data-check>')


def check_figures(page: Page, problems: list[str]) -> None:
    """Every [data-chart] is drawn by the page's figure module, inside a captioned figure, with D3 loaded."""
    where = page.path.name
    charts = page.dom.select(None, None, data_chart=None)
    if not charts:
        return
    module = page.html.get("data-figures")
    source = ""
    if not module:
        problems.append(f"{where}: [data-chart] figures need <html data-figures> naming the page's figure module")
    elif not (page.path.parent / module).exists():
        problems.append(f"{where}: figure module {module} does not exist")
    else:
        source = (page.path.parent / module).read_text(encoding="utf-8")
    if not any("d3.min.js" in (s.get("src") or "") for s in page.dom.select("script")):
        problems.append(f"{where}: a page that draws charts must load assets/vendor/d3/d3.min.js")
    for chart in charts:
        name = chart.get("data-chart")
        if source and not re.search(rf"[\"']{re.escape(name)}[\"']\s*:", source):
            problems.append(f"{where}:{chart.line}: figure {name!r} is not defined in {module}")
        figure = next((n for n in chart.ancestors() if n.tag == "figure"), None)
        caption = figure.first("figcaption") if figure else None
        if caption is None or caption.first(None, "source") is None:
            problems.append(f"{where}:{chart.line}: figure {name!r} needs a <figure> with <figcaption> and span.source")


def section(page: Page, section_id: str) -> Node | None:
    if section_id == "why-it-matters":
        return page.dom.first("p", "why-it-matters")
    return page.dom.first(None, None, id=section_id)


def check_lesson(page: Page, u: Unit, problems: list[str]) -> float:
    where = page.path.name
    hours = page.html.get("data-hours")
    try:
        declared = float(hours)
    except ValueError:
        problems.append(f"{where}: <html data-hours> must declare the lesson's study hours")
        declared = 0.0
    if declared and not 6 <= declared <= 12:
        problems.append(f"{where}: a lesson is 6–12 study hours, not {declared:g}")
    if page.html.get("data-page") != page.name:
        problems.append(f"{where}: data-page must be {page.name}")

    lines = []
    for section_id in LESSON_SECTIONS:
        node = section(page, section_id)
        if node is None:
            problems.append(f"{where}: missing section {section_id}")
        else:
            lines.append((node.line, section_id))
    if [s for _, s in sorted(lines)] != [s for _, s in lines]:
        problems.append(f"{where}: sections out of order (BUILDER_RULES §4.2): {[s for _, s in sorted(lines)]}")

    why = page.dom.first("p", "why-it-matters")
    if why is not None and words(why.text()) > 120:
        problems.append(f"{where}: 'why it matters' has {words(why.text())} words (max 120)")
    canon = section(page, "canon-breaks")
    core = [h for h in page.dom.select("h2") if h.get("id") and canon is not None and h.line < canon.line]
    if not core:
        problems.append(f"{where}: no core content sections before 'where the canon breaks'")
    blocks = page.dom.select(None, "block")
    if not blocks:
        problems.append(f"{where}: core content needs Definition/Theorem/Proof/Example/Remark blocks")

    labs = page.dom.select("section", "lab")
    if not labs:
        problems.append(f"{where}: at least one inline lab is required")
    for position, lab in enumerate(labs, start=1):
        lid = lab.get("id")
        if not re.fullmatch(rf"lab-{re.escape(u.id)}-{page.name}-\d+", lid):
            problems.append(f"{where}: lab id {lid!r} must be lab-{u.id}-{page.name}-<n>")
        elif not lid.endswith(f"-{position}"):
            problems.append(f"{where}: lab {lid} is lab {position} on the page; number lab ids in display order")
        if lab.get("data-runtime") not in ("python", "sql", "cpp"):
            problems.append(f"{where}: {lid} needs data-runtime python|sql|cpp")
        if not lab.first("h3"):
            problems.append(f"{where}: {lid} needs an <h3> title")
        if not lab.first("p", "hypothesis") or not lab.first("p", "interpretation"):
            problems.append(f"{where}: {lid} needs a hypothesis stated before running and an interpretation")
        if not lab.first("code", None, data_run=None):
            problems.append(f"{where}: {lid} needs runnable code (<code data-run>)")
        expected = lab.first("pre", "expected")
        if expected is None or not expected.text().strip():
            problems.append(f"{where}: {lid} needs <pre class=expected> with the expected output")
        elif "data-tolerance" not in expected.attrs:
            problems.append(f"{where}: {lid} expected output needs data-tolerance")
        if canon is not None and lab.line > canon.line:
            problems.append(f"{where}: {lid} must sit inside the argument, before 'where the canon breaks'")

    mis = page.dom.select("li", "misconception")
    if len(mis) < 3:
        problems.append(f"{where}: {len(mis)} misconceptions (min 3)")
    for item in mis:
        if not item.first("p", "wrong") or len(item.select("p")) < 2:
            problems.append(f"{where}:{item.line}: a misconception needs the wrong belief and why it is wrong")

    problem_set = section(page, "problems")
    if problem_set is not None:
        for tier in TIERS:
            block = problem_set.first("div", "tier", data_tier=tier)
            items = block.select("div", "problem") if block else []
            if len(items) < 3:
                problems.append(f"{where}: {len(items)} {tier} problems (min 3)")
            for item in items:
                sol = item.first("details", "solution")
                if sol is None or words(sol.text()) < 15:
                    problems.append(f"{where}: problem {item.get('id')!r} needs a full worked solution")
    key = section(page, "key-results")
    if key is not None and not key.first("table", "key-results"):
        problems.append(f"{where}: key results need table.key-results")
    quiz = section(page, "quiz")
    if quiz is not None:
        items = quiz.select("li", "item")
        if not 8 <= len(items) <= 15:
            problems.append(f"{where}: the retrieval quiz has {len(items)} items (8–15)")
        for item in items:
            explain = item.first("div", "explain")
            if explain is None or not explain.text().strip():
                problems.append(f"{where}:{item.line}: quiz item without an explanation")
            kind = item.get("data-kind")
            if kind == "mc" and len(item.select("label", "option", data_correct=None)) != 1:
                problems.append(f"{where}:{item.line}: a multiple-choice item needs exactly one data-correct option")
            if kind == "numeric" and not (item.get("data-answer") and item.get("data-tolerance")):
                problems.append(f"{where}:{item.line}: a numeric item needs data-answer and data-tolerance")
            if kind not in ("mc", "numeric"):
                problems.append(f"{where}:{item.line}: quiz item data-kind must be mc or numeric")
        if quiz.get("data-unit") != u.id or quiz.get("data-page") != page.name:
            problems.append(f"{where}: quiz needs data-unit={u.id} data-page={page.name}")
    refs = section(page, "references")
    if refs is not None and not refs.first("ol", None, data_references=None):
        problems.append(f"{where}: references need <ol data-references>")
    if not page.dom.first("button", None, data_complete=None):
        problems.append(f"{where}: lesson needs a 'mark complete' button")
    return declared


def check_hub(page: Page, u: Unit, lesson_hours: dict[str, float], problems: list[str]) -> None:
    where = page.path.name
    main = page.dom.first("main")
    if main is None:
        problems.append(f"{where}: no <main>")
        return
    try:
        lessons_h = float(main.get("data-hours-lessons"))
        project_h = float(main.get("data-hours-project"))
    except ValueError:
        problems.append(f"{where}: <main> must declare data-hours-lessons and data-hours-project")
        return
    if abs(lessons_h + project_h - u.hours) > 1e-9:
        problems.append(f"{where}: hours split {lessons_h:g} + {project_h:g} must equal the curriculum's {u.hours}")
    if not 0.10 <= project_h / u.hours <= 0.40:
        problems.append(f"{where}: project is {project_h / u.hours:.0%} of module hours (10–40%)")
    if abs(sum(lesson_hours.values()) - lessons_h) > 1e-9:
        problems.append(f"{where}: lessons declare {sum(lesson_hours.values()):g} h; the hub says {lessons_h:g} h")
    objectives = page.dom.first("ol", "objectives")
    count = len(objectives.select("li")) if objectives else 0
    if not 4 <= count <= 8:
        problems.append(f"{where}: {count} objectives (4–8, measurable verbs)")
    for section_id in ("prerequisites", "placement", "lessons", "ladder"):
        if not page.dom.first(None, None, id=section_id):
            problems.append(f"{where}: missing section #{section_id}")
    placement = page.dom.first("section", "quiz", id="placement")
    if placement is None or not placement.get("data-mastery"):
        problems.append(f"{where}: the placement diagnostic must be section.quiz#placement with data-mastery")
    elif u.kind == "module" and len(placement.select("li", "item", data_skill=None)) < 2:
        problems.append(f"{where}: the placement diagnostic needs two or more data-skill items on what rungs 1–2 teach")
    ladder = page.dom.first("ol", "ladder")
    if ladder is None or len(ladder.select("li")) < 4:
        problems.append(f"{where}: the project ladder needs four rungs")
    links = {a.get("href") for a in page.dom.select("a")}
    for name in lesson_hours:
        if f"{name}.html" not in links:
            problems.append(f"{where}: the lesson map does not link {name}.html")
    if "project.html" not in links:
        problems.append(f"{where}: the hub does not link project.html")


def check_cards(u: Unit, lessons: set[str], problems: list[str]) -> None:
    path = u.directory / "cards.json"
    if not path.exists():
        problems.append("cards.json is missing")
        return
    try:
        cards = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        problems.append(f"cards.json: invalid JSON ({exc})")
        return
    keys = registry_keys()
    ids = Counter(c.get("id") for c in cards)
    problems.extend(f"cards.json: duplicate id {i}" for i, n in ids.items() if n > 1)
    for card in cards:
        cid = card.get("id", "?")
        if not re.fullmatch(rf"{re.escape(u.id)}-c\d{{3}}", cid):
            problems.append(f"cards.json: id {cid!r} must look like {u.id}-c001")
        if not card.get("front", "").strip() or not card.get("back", "").strip():
            problems.append(f"cards.json: {cid} needs a front and a back")
        if card.get("lesson") not in lessons:
            problems.append(f"cards.json: {cid} names lesson {card.get('lesson')!r}, which does not exist")
        if card.get("grade") and card["grade"] not in GRADES:
            problems.append(f"cards.json: {cid} has invalid grade {card['grade']!r}")
        for key in card.get("cite", []):
            if key not in keys:
                problems.append(f"cards.json: {cid} cites unknown key {key!r}")
        grounded = card.get("cite") or str(card.get("basis", "")).strip()
        if card.get("grade") and card["grade"] != "T" and not grounded:
            problems.append(f"cards.json: {cid} states a grade-{card['grade']} result with neither cite nor basis")
    per_lesson = Counter(c.get("lesson") for c in cards)
    for lesson in sorted(lessons):
        if per_lesson[lesson] == 0:
            problems.append(f"cards.json: no cards for {lesson}")


def check_unit(u: Unit) -> list[str]:
    problems: list[str] = []
    if not u.built:
        return [f"{u.id} is not built ({u.directory}/index.html missing)"]
    lesson_hours: dict[str, float] = {}
    for path in u.lesson_pages():
        page = load_page(path)
        check_common(page, u, problems)
        lesson_hours[page.name] = check_lesson(page, u, problems)
    if u.kind == "module" and not lesson_hours:
        problems.append("no lesson pages (L01.html …)")
    if u.entry.get("debate") and not any(load_page(p).dom.first("section", "debate") for p in u.lesson_pages()):
        problems.append("the curriculum tags a debate but no lesson carries a debate brief")
    hub = load_page(u.directory / "index.html")
    check_common(hub, u, problems)
    check_hub(hub, u, lesson_hours, problems)
    project = u.directory / "project.html"
    if project.exists():
        check_common(load_page(project), u, problems)
    else:
        problems.append("project.html is missing")
    check_cards(u, set(lesson_hours), problems)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true", help="every built unit")
    parser.add_argument("--page", help="check one lesson page of --unit only (e.g. L03), while a unit is being built")
    args = parser.parse_args()
    if args.page:
        if not args.unit:
            parser.error("--page needs --unit")
        u = unit(args.unit)
        page = load_page(u.directory / f"{args.page}.html")
        problems: list[str] = []
        check_common(page, u, problems)
        check_lesson(page, u, problems)
        for problem in problems:
            print(f"FAIL {u.id}: {problem}")
        print(f"check_pages {u.id} {args.page}: {'PASS' if not problems else f'FAIL ({len(problems)} problems)'}")
        return 1 if problems else 0
    targets = built_units() if args.all else [unit(args.unit)]
    failed = 0
    for u in targets:
        problems = check_unit(u)
        for problem in problems:
            print(f"FAIL {u.id}: {problem}")
        print(f"check_pages {u.id}: {'PASS' if not problems else f'FAIL ({len(problems)} problems)'}")
        failed += bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
