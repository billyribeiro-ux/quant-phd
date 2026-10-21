#!/usr/bin/env python3
"""Generate the course site's derived data and its program map.

Everything this writes is derived from a source of truth, so it is generated,
committed, and checked current in CI (never hand-edited):

* ``course/assets/data/program.json``    curriculum graph for the program map, with
  each module's credential and track closures and whether it is built
* ``course/assets/data/references.json`` display form of every verified registry entry
* ``course/assets/data/notation.json``   the notation registry (notation/notation.json)
* ``course/assets/data/glossary.json``   every ``<dfn data-concept>`` on a built page,
  i.e. where each concept is actually defined
* ``course/index.html``                  the program map page
* ``course/concepts.html``               every concept, under the module that introduces it

Usage::

    python3 tools/build_site.py            # write outputs
    python3 tools/build_site.py --check    # non-zero if any output is stale
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from string import Template
from typing import Any

from refs.registry import display_year

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "course"
DATA = COURSE / "assets" / "data"
CURRICULUM = ROOT / "curriculum" / "curriculum.json"
REGISTRY = ROOT / "references" / "references.json"
NOTATION = ROOT / "notation" / "notation.json"
TEMPLATES = ROOT / "tools" / "site_templates"

_SMALL_WORDS = frozenset(
    {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor", "of", "on", "or", "per"}
    | {"the", "to", "vs", "via", "with"}
)


# ---------------------------------------------------------------- citation display


_INITIALS = re.compile(r"(?:[A-Z]\.-?)+")


def _fix_case(word: str) -> str:
    """'HARVEY' -> 'Harvey', 'MCLEAN' -> 'McLean', 'COLLIN-DUFRESNE' -> 'Collin-Dufresne'; mixed case and
    initials ('P.B.', 'J.-P.') are kept."""
    if not word.isupper() or len(word) <= 1 or _INITIALS.fullmatch(word):
        return word
    lowered = word.lower()
    if lowered.startswith("mc") and len(lowered) > 3:
        return "Mc" + lowered[2:].capitalize()
    return "-".join(part.capitalize() for part in lowered.split("-"))


def family_name(family: str, source_strings: list[str]) -> str:
    """Display spelling of a family name; all-caps Crossref names take the curriculum's spelling.

    Crossref sometimes files given names with the family name ('GORDON LAN' for K. K. Gordon Lan). When the
    whole name is not in a citation string's author list but its last words are, those words are the surname.
    """
    if not family.isupper():
        return family
    for source in source_strings:
        match = re.search(re.escape(family), source, flags=re.IGNORECASE)
        if match and not match.group().isupper():
            return match.group()
    words = family.split()
    for start in range(1, len(words)):
        tail = " ".join(words[start:])
        for source in source_strings:
            authors = source.split("(", 1)[0]
            match = re.search(rf"(?<![\w-]){re.escape(tail)}(?![\w-])", authors, flags=re.IGNORECASE)
            if match and not match.group().isupper():
                return match.group()
    return " ".join(_fix_case(w) for w in words)


def title_case(title: str) -> str:
    """Records that shout (all-caps titles) are shown in title case; others are left exactly as recorded."""
    letters = [c for c in title if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) / len(letters) < 0.8:
        return title
    words = title.lower().split(" ")
    out: list[str] = []
    for i, word in enumerate(words):
        if i and word in _SMALL_WORDS and not out[-1].endswith(":"):
            out.append(word)
        else:
            out.append(word[:1].upper() + word[1:])
    return " ".join(out)


_TEX_INLINE_MATH = re.compile(r"\$(\S|\S[^$]*\S)\$")  # TeX math hugs its delimiters; prices do not


def plain_title(title: str) -> str:
    """Crossref keeps TeX inline math in titles ('the Student $t$-statistic'); the reference list is plain text."""
    return _TEX_INLINE_MATH.sub(r"\1", title)


def short_cite(entry: dict[str, Any]) -> str:
    names = [family_name(a["family"], entry["source_strings"]) for a in entry["authors"]]
    year = display_year(entry)
    when = f" ({year})" if year else ""
    if entry.get("type") == "primary":
        return f"{names[0]}{when}"
    if len(names) == 1:
        return f"{names[0]}{when}"
    if len(names) == 2:
        return f"{names[0]} & {names[1]}{when}"
    if len(names) == 3:
        return f"{names[0]}, {names[1]} & {names[2]}{when}"
    return f"{names[0]} et al.{when}"


def full_cite(entry: dict[str, Any]) -> str:
    people = []
    for author in entry["authors"]:
        family = family_name(author["family"], entry["source_strings"])
        given = " ".join(_fix_case(g) for g in (author.get("given") or "").split())
        people.append(f"{family}, {given}" if given else family)
    if len(people) > 10:
        people = [*people[:10], "et al."]
    authors = "; ".join(people)
    year = display_year(entry)
    title = title_case(plain_title(entry["title"])).rstrip(".")
    parts = [f"{authors} ({year})." if year else f"{authors}.", title if title.endswith(("?", "!")) else f"{title}."]
    container = entry.get("container")
    if container:
        where = container
        if entry.get("volume"):
            where += f" {entry['volume']}"
            if entry.get("issue"):
                where += f"({entry['issue']})"
        if entry.get("pages"):
            where += f", {entry['pages'].replace('-', '–')}"
        parts.append(f"{where}.")
    elif entry.get("publisher") and entry.get("type") != "primary":
        parts.append(f"{entry['publisher']}.")
    if entry.get("type") == "primary" and entry.get("resolved_at"):
        parts.append(f"Retrieved {entry['resolved_at'][:10]}.")
    return " ".join(parts)


def references_payload(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        e["key"]: {
            "short": short_cite(e),
            "full": full_cite(e),
            "doi": e.get("doi"),
            "url": e.get("url"),
            "type": e.get("type"),
        }
        for e in sorted(entries, key=lambda e: e["key"])
        if e.get("status") == "verified"
    }


# ---------------------------------------------------------------- program


def module_dir(part: str, module_id: str) -> Path:
    return COURSE / "modules" / part / module_id


def closure(targets: list[str], prereqs: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    stack = list(targets)
    while stack:
        current = stack.pop()
        if current not in seen:
            seen.add(current)
            stack.extend(prereqs[current])
    return sorted(seen)


def program_payload(curriculum: dict[str, Any]) -> dict[str, Any]:
    prereqs = {m["id"]: m["prereqs"] for p in curriculum["parts"] for m in p["modules"]}
    parts = []
    for part in curriculum["parts"]:
        modules = []
        for m in part["modules"]:
            built = (module_dir(part["code"], m["id"]) / "index.html").exists()
            project = m["project"]
            modules.append(
                {
                    "id": m["id"],
                    "title": m["title"],
                    "tier": m["tier"],
                    "hours": m["hours"],
                    "prereqs": m["prereqs"],
                    "core": " ".join(m["core"].split()),
                    "introduces": list(m["introduces"].values()),
                    "project": {
                        "title": project["title"],
                        "brief": " ".join(project["brief"].split()),
                        "grading": project["grading"],
                        "atlas": project.get("atlas"),
                    },
                    "debate": m.get("debate"),
                    "href": f"modules/{part['code']}/{m['id']}/index.html" if built else None,
                }
            )
        studio = part.get("studio")
        parts.append(
            {
                "order": part["order"],
                "code": part["code"],
                "title": part["title"],
                "studio": (
                    {k: studio[k] for k in ("id", "title", "tier", "hours", "requires", "grading")} if studio else None
                ),
                "modules": modules,
            }
        )
    stats = curriculum["stats"]
    return {
        "program": curriculum["program"],
        "tiers": curriculum["tiers"],
        "stats": {k: stats[k] for k in ("modules", "parts", "projects", "studios", "concepts", "total_hours")},
        "credentials": [
            {"id": c["id"], "name": c["name"], "closure": c["closure"], "hours": c["hours"]}
            for c in stats["credentials"]
        ],
        "tracks": [
            {"id": t["id"], "name": t["name"], "closure": closure(t["targets"], prereqs), "hours": t["hours"]}
            for t in stats["tracks"]
        ],
        "parts": parts,
    }


# ---------------------------------------------------------------- glossary


class _DfnParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[tuple[str, str, str]] = []
        self._stack: list[tuple[str, str]] = []
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "dfn":
            values = {k: v or "" for k, v in attrs}
            self._stack.append((values.get("data-concept", ""), values.get("id", "")))
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "dfn" and self._stack:
            concept, anchor = self._stack.pop()
            self.found.append((concept, anchor, " ".join("".join(self._text).split())))

    def handle_data(self, data: str) -> None:
        if self._stack:
            self._text.append(data)


def glossary_payload(curriculum: dict[str, Any]) -> dict[str, Any]:
    names = {cid: c["name"] for cid, c in curriculum["concepts"].items()}
    owners = {cid: c["module"] for cid, c in curriculum["concepts"].items()}
    entries: dict[str, Any] = {}
    for page in sorted((COURSE / "modules").glob("*/*/*.html")):
        parser = _DfnParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for concept, anchor, term in parser.found:
            if concept in names:
                entries[concept] = {
                    "name": names[concept],
                    "term": term,
                    "module": owners[concept],
                    "href": f"{page.relative_to(COURSE).as_posix()}#{anchor}"
                    if anchor
                    else page.relative_to(COURSE).as_posix(),
                }
    return dict(sorted(entries.items()))


# ---------------------------------------------------------------- program map page


def esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def render_index(program: dict[str, Any], curriculum: dict[str, Any]) -> str:
    stats = program["stats"]
    tiers = {t["code"]: t for t in curriculum["tiers"]}
    built = [m for p in program["parts"] for m in p["modules"] if m["href"]]
    years = curriculum["stats"]["full_time_years"]
    cred_rows = "\n".join(
        f'          <tr><td>{esc(c["name"])}</td><td class="num">{c["modules"]}</td>'
        f'<td class="num">{c["projects"]}</td><td class="num">{c["hours"]:,}</td>'
        f'<td class="num">≈{c["credit_equivalent"]}</td><td class="num">{c["full_time_years"]:.2f}</td></tr>'
        for c in curriculum["stats"]["credentials"]
    )
    options = ['            <option value="">Whole program</option>']
    options += [
        f'            <option value="credential:{esc(c["id"])}">Credential · {esc(c["name"])}</option>'
        for c in program["credentials"]
    ]
    options += [
        f'            <option value="track:{esc(t["id"])}">Career track · {esc(t["name"])}</option>'
        for t in program["tracks"]
    ]
    options += [
        f'            <option value="tier:{esc(code)}">Tier {esc(code)} · {esc(t["name"])}</option>'
        for code, t in tiers.items()
    ]
    part_blocks = []
    for part in program["parts"]:
        hours = sum(m["hours"] for m in part["modules"]) + (part["studio"]["hours"] if part["studio"] else 0)
        chips = []
        for m in part["modules"]:
            dot = '<span class="built" aria-hidden="true"></span>' if m["href"] else ""
            label = f"{m['id']} {m['title']}, tier {m['tier']}, {m['hours']} hours" + (
                ", available" if m["href"] else ""
            )
            chips.append(
                f'            <li><button type="button" class="chip" data-id="{esc(m["id"])}" aria-pressed="false" '
                f'aria-label="{esc(label)}"><span class="tier">{esc(m["tier"])}</span>{esc(m["id"])} · '
                f"{esc(m['title'])}{dot}</button></li>"
            )
        studio = ""
        if part["studio"]:
            s = part["studio"]
            studio = (
                f'\n          <p class="eyebrow">Studio · {esc(s["title"])} · {s["hours"]} h · '
                f"integrates {esc(', '.join(s['requires']))}</p>"
            )
        part_blocks.append(
            f'        <section class="map-part" aria-labelledby="part-{esc(part["code"])}">\n'
            f'          <h3 id="part-{esc(part["code"])}">'
            f'<span class="code">{part["order"]:02d} · {esc(part["code"])}</span>'
            f'{esc(part["title"])}<span class="hours">{hours:,} h</span></h3>\n'
            f'          <ul class="chips">\n' + "\n".join(chips) + "\n          </ul>" + studio + "\n        </section>"
        )
    available = (
        ", ".join(f'<a href="{esc(m["href"])}">{esc(m["id"])} · {esc(m["title"])}</a>' for m in built)
        if built
        else "none yet"
    )
    values = {
        "program_name": esc(program["program"]["name"]),
        "version": esc(program["program"]["version"]),
        "modules": stats["modules"],
        "projects": stats["projects"],
        "parts": stats["parts"],
        "studios": stats["studios"],
        "concepts": f"{stats['concepts']:,}",
        "total_hours": f"{stats['total_hours']:,}",
        "years": years,
        "released": len(built),
        "available": available,
        "cred_rows": cred_rows,
        "options": "\n".join(options),
        "part_blocks": "\n".join(part_blocks),
    }
    return Template((TEMPLATES / "index.html").read_text(encoding="utf-8")).substitute(values)


def render_concepts(program: dict[str, Any], curriculum: dict[str, Any], glossary: dict[str, Any]) -> str:
    """Every concept in the program, grouped by the one module that introduces it (concept links land here)."""
    modules = {m["id"]: (part, m) for part in program["parts"] for m in part["modules"]}
    by_module: dict[str, list[tuple[str, str]]] = {}
    for concept_id, concept in curriculum["concepts"].items():
        by_module.setdefault(concept["module"], []).append((concept_id, concept["name"]))
    sections = []
    for module_id in curriculum["topological_order"]:
        part, m = modules[module_id]
        title = (
            f'<a href="{esc(m["href"])}">{esc(module_id)} · {esc(m["title"])}</a>'
            if m["href"]
            else f"{esc(module_id)} · {esc(m['title'])}"
        )
        rows = []
        for concept_id, name in sorted(by_module.get(module_id, []), key=lambda c: c[1].lower()):
            entry = glossary.get(concept_id)
            where = f'<a href="{esc(entry["href"])}">defined here</a>' if entry else "not yet released"
            rows.append(f'          <li id="{esc(concept_id)}"><strong>{esc(name)}</strong> · {where}</li>')
        sections.append(
            f'      <section aria-labelledby="c-{esc(module_id)}">\n'
            f'        <h3 id="c-{esc(module_id)}">{title} <span class="eyebrow">tier {esc(m["tier"])}</span></h3>\n'
            f"        <ul>\n" + "\n".join(rows) + "\n        </ul>\n      </section>"
        )
    values = {
        "concepts": f"{len(curriculum['concepts']):,}",
        "modules": len(modules),
        "defined": len(glossary),
        "sections": "\n".join(sections),
    }
    return Template((TEMPLATES / "concepts.html").read_text(encoding="utf-8")).substitute(values)


# ---------------------------------------------------------------- main


def outputs() -> dict[Path, str]:
    curriculum = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))["entries"]
    program = program_payload(curriculum)

    def dump(payload: Any) -> str:
        return json.dumps(payload, indent=1, ensure_ascii=False) + "\n"

    glossary = glossary_payload(curriculum)
    return {
        DATA / "program.json": dump(program),
        DATA / "references.json": dump(references_payload(registry)),
        DATA / "notation.json": dump(json.loads(NOTATION.read_text(encoding="utf-8"))),
        DATA / "glossary.json": dump(glossary),
        COURSE / "index.html": render_index(program, curriculum),
        COURSE / "concepts.html": render_concepts(program, curriculum, glossary),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if any generated output is stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(path.relative_to(ROOT).as_posix())
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if args.check and stale:
        print("stale generated files (run tools/build_site.py):\n  " + "\n  ".join(stale), file=sys.stderr)
        return 1
    print(f"site data {'current' if not stale else 'written'}: {len(outputs())} outputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
