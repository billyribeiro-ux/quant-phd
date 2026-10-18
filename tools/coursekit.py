"""Shared model of the course site for the checking tools.

Parses course pages into a small DOM (no third-party HTML library), locates
units (modules and studios) on disk, and loads the curriculum, registry and
concept graph that every check is judged against. check_pages.py,
check_dag.py, check_projects.py, run_labs.py, run_graders.py and
page_smoke.py all build on this module, so they agree on what a page is.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "course"
LAB_TWINS = ROOT / "tests" / "labs"
# Embedded market data (tools/fetch_data.py). A lab lists the files it reads in data-files and opens them as
# data/<file>: the browser writes exactly those files there in Pyodide, and a twin runs in a scratch directory
# whose data/ holds copies of the same files (twin_workdir).
MARKET_DATA = COURSE / "assets" / "data" / "market"
LEDGERS = ROOT / "ledgers"

_VOID = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
)
_NUMBER = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?%?$")


@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    children: list[Node | str] = field(default_factory=list)
    parent: Node | None = None
    line: int = 0

    def get(self, name: str, default: str = "") -> str:
        return self.attrs.get(name, default)

    @property
    def classes(self) -> set[str]:
        return set(self.get("class").split())

    def text(self) -> str:
        """Concatenated text content, entities decoded."""
        parts: list[str] = []
        for child in self.children:
            parts.append(child if isinstance(child, str) else child.text())
        return "".join(parts)

    def iter(self) -> Iterator[Node]:
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.iter()

    def find_all(self, predicate: Callable[[Node], bool]) -> list[Node]:
        return [n for n in self.iter() if predicate(n)]

    def select(self, tag: str | None = None, cls: str | None = None, **attrs: str | None) -> list[Node]:
        """Descendants (and self) matching a tag, a class and attribute values (None = attribute present)."""

        def ok(n: Node) -> bool:
            if tag and n.tag != tag:
                return False
            if cls and cls not in n.classes:
                return False
            for key, value in attrs.items():
                name = key.replace("_", "-")
                if name not in n.attrs or (value is not None and n.attrs[name] != value):
                    return False
            return True

        return self.find_all(ok)

    def first(self, tag: str | None = None, cls: str | None = None, **attrs: str | None) -> Node | None:
        found = self.select(tag, cls, **attrs)
        return found[0] if found else None

    def ancestors(self) -> Iterator[Node]:
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class _Builder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#document", {})
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {k: v or "" for k, v in attrs}, parent=self.stack[-1], line=self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in _VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {k: v or "" for k, v in attrs}, parent=self.stack[-1], line=self.getpos()[0])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def parse_html(text: str) -> Node:
    builder = _Builder()
    builder.feed(text)
    builder.close()
    return builder.root


@dataclass
class Page:
    path: Path
    source: str
    dom: Node

    @property
    def name(self) -> str:
        return self.path.stem

    @property
    def html(self) -> Node:
        node = self.dom.first("html")
        if node is None:
            raise ValueError(f"{self.path}: no <html> element")
        return node


def load_page(path: Path) -> Page:
    source = path.read_text(encoding="utf-8")
    return Page(path=path, source=source, dom=parse_html(source))


# ---------------------------------------------------------------- program data


@cache
def curriculum() -> dict[str, Any]:
    data: dict[str, Any] = json.loads((ROOT / "curriculum" / "curriculum.json").read_text(encoding="utf-8"))
    return data


@cache
def registry_keys() -> frozenset[str]:
    data = json.loads((ROOT / "references" / "references.json").read_text(encoding="utf-8"))
    return frozenset(e["key"] for e in data["entries"] if e.get("status") == "verified")


@cache
def market_files(directory: Path = MARKET_DATA) -> frozenset[str]:
    """The snapshot files listed in the directory's MANIFEST.json (tools/fetch_data.py): what data-files may name."""
    manifest = directory / "MANIFEST.json"
    if not manifest.exists():
        return frozenset()
    return frozenset(e["file"] for e in json.loads(manifest.read_text(encoding="utf-8"))["datasets"])


@dataclass(frozen=True)
class Unit:
    id: str
    part: str
    kind: str  # "module" or "studio"
    entry: dict[str, Any]

    @property
    def directory(self) -> Path:
        base = "modules" if self.kind == "module" else "studios"
        return COURSE / base / self.part / self.id if self.kind == "module" else COURSE / base / self.id

    @property
    def built(self) -> bool:
        return (self.directory / "index.html").exists()

    @property
    def hours(self) -> int:
        return int(self.entry["hours"])

    @property
    def introduces(self) -> dict[str, str]:
        value = self.entry.get("introduces") or {}
        return dict(value)

    def lesson_pages(self) -> list[Path]:
        return sorted(self.directory.glob("L[0-9][0-9].html"))

    def pages(self) -> list[Path]:
        names = ["index.html", *(p.name for p in self.lesson_pages()), "project.html"]
        return [self.directory / n for n in names if (self.directory / n).exists()]


@cache
def units() -> dict[str, Unit]:
    out: dict[str, Unit] = {}
    for part in curriculum()["parts"]:
        for module in part["modules"]:
            out[module["id"]] = Unit(module["id"], part["code"], "module", module)
        if part.get("studio"):
            studio = part["studio"]
            out[studio["id"]] = Unit(studio["id"], part["code"], "studio", studio)
    return out


def unit(unit_id: str) -> Unit:
    try:
        return units()[unit_id]
    except KeyError as exc:
        raise SystemExit(f"unknown unit {unit_id}") from exc


def built_units() -> list[Unit]:
    return [u for u in units().values() if u.built]


@cache
def concept_owner() -> dict[str, str]:
    return {cid: c["module"] for cid, c in curriculum()["concepts"].items()}


def prerequisite_closure(unit_id: str) -> set[str]:
    modules = {m["id"]: m for p in curriculum()["parts"] for m in p["modules"]}
    entry = units()[unit_id].entry
    stack = list(entry.get("prereqs") or entry.get("requires") or [])
    seen: set[str] = set()
    while stack:
        current = stack.pop()
        if current not in seen:
            seen.add(current)
            stack.extend(modules[current]["prereqs"])
    return seen


# ---------------------------------------------------------------- labs


@dataclass(frozen=True)
class Lab:
    page: Path
    id: str
    runtime: str
    code: str
    expected: str | None
    tolerance: float
    packages: tuple[str, ...]
    completion: bool = False  # project rung 2: page code has ___ blanks; the twin is the solution
    snippet: bool = False  # checked solution code (data-check): run locally, not in the page's lab runner
    files: tuple[str, ...] = ()  # data-files: snapshots under MARKET_DATA, read as data/<file>

    @property
    def unit(self) -> str:
        return self.id.split("-")[1]

    @property
    def twin(self) -> Path:
        return LAB_TWINS / self.unit / f"{self.id}.py"


def labs_in(page: Page) -> list[Lab]:
    found: list[Lab] = []
    for section in page.dom.select("section", "lab"):
        code = section.first("code", None, data_run=None)
        expected = section.first("pre", "expected")
        found.append(
            Lab(
                page=page.path,
                id=section.get("id"),
                runtime=section.get("data-runtime"),
                code=code.text() if code else "",
                expected=expected.text() if expected else None,
                tolerance=float(expected.get("data-tolerance", "0") or 0) if expected else 0.0,
                packages=tuple(section.get("data-packages").split()),
                completion="completion" in section.classes,
                files=tuple(section.get("data-files").split()),
            )
        )
    return found


def snippets_in(page: Page) -> list[Lab]:
    """Checked code in solutions: <code class="language-python" data-check="<id>"> and its
    <pre class="expected" data-check="<id>">, held to a twin tests/labs/<UNIT>/<id>.py like a lab."""
    outputs = {n.get("data-check"): n for n in page.dom.select("pre", "expected", data_check=None)}
    found: list[Lab] = []
    for code in page.dom.select("code", None, data_check=None):
        name = code.get("data-check")
        expected = outputs.get(name)
        found.append(
            Lab(
                page=page.path,
                id=name,
                runtime="python",
                code=code.text(),
                expected=expected.text() if expected else None,
                tolerance=float(expected.get("data-tolerance", "0") or 0) if expected else 0.0,
                packages=("numpy",),
                snippet=True,
            )
        )
    return found


def compare_output(actual: str, expected: str, tolerance: float) -> tuple[bool, str]:
    """The page's comparison rule (labs.js): numbers within tol*(1+|expected|), other tokens exact."""
    a, e = actual.split(), expected.split()
    if len(a) != len(e):
        return False, f"expected {len(e)} tokens, got {len(a)}"
    for i, (x, y) in enumerate(zip(a, e, strict=True)):
        if _NUMBER.match(x) and _NUMBER.match(y):
            xv, yv = float(x.rstrip("%")), float(y.rstrip("%"))
            if not abs(xv - yv) <= tolerance * (1 + abs(yv)):
                return False, f"token {i + 1}: {x} differs from {y} beyond tolerance {tolerance}"
        elif x != y:
            return False, f"token {i + 1}: {x!r} differs from {y!r}"
    return True, ""


def visible_text(node: Node) -> str:
    """Text a reader sees as prose: code, scripts, styles and math delimiters removed."""
    parts: list[str] = []

    def walk(n: Node) -> None:
        if n.tag in ("script", "style", "code", "pre", "textarea"):
            return
        for child in n.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                walk(child)

    walk(node)
    text = html.unescape(" ".join(parts))
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.DOTALL)
    return re.sub(r"\\\(.*?\\\)", " ", text, flags=re.DOTALL)


@contextmanager
def twin_workdir(files: tuple[str, ...] = (), source: Path = MARKET_DATA) -> Iterator[Path]:
    """A fresh working directory for running a lab twin: data/ holds copies of exactly the lab's data-files.

    The browser runtime writes the same files, and only those, to data/ before a lab runs (py-worker.js), so a twin
    that opens a file its section does not declare fails here as it would on the page. Copies, not links, so a twin
    cannot alter a committed snapshot. A name with no snapshot is skipped; the twin's open() then fails.
    """
    with tempfile.TemporaryDirectory(prefix="lab-") as tmp:
        work = Path(tmp)
        (work / "data").mkdir()
        for name in files:
            if Path(name).name == name and (source / name).is_file():
                shutil.copyfile(source / name, work / "data" / name)
        yield work
