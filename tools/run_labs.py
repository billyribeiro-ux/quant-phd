#!/usr/bin/env python3
"""Run every in-page Python lab under CPython and check it against its expected output.

Labs are extracted directly from the HTML (``section.lab[data-runtime="python"]``):
the code in ``code[data-run]`` is executed in a fresh interpreter, and its stdout
is compared with ``pre.expected`` token by token, allowing numeric tokens to
differ by at most ``data-tolerance`` (absolute). This is the same rule the
browser applies (``course/assets/js/lab.js``), so a lab that passes here passes
in Pyodide, and the page is the single source of truth for its code.

CI runs this on CPython 3.14, matching the vendored Pyodide 314.x runtime.

Usage::

    python3 tools/run_labs.py                 # every page under course/
    python3 tools/run_labs.py course/dev/design-system.html
    python3 tools/run_labs.py --unit S7       # one module or studio
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "course"
TIMEOUT_SECONDS = 60
_NUMBER = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?$")


@dataclass
class Lab:
    page: Path
    lab_id: str
    code: str = ""
    expected: str | None = None
    tolerance: float = 0.0


@dataclass
class _Capture:
    kind: str  # "code" or "expected"
    depth: int
    chunks: list[str] = field(default_factory=list)


class LabExtractor(HTMLParser):
    """Collects Python labs from one HTML document."""

    def __init__(self, page: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.page = page
        self.labs: list[Lab] = []
        self._lab: Lab | None = None
        self._lab_depth = 0
        self._depth = 0
        self._capture: _Capture | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._depth += 1
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "section" and "lab" in classes and attributes.get("data-runtime") == "python":
            self._lab = Lab(self.page, attributes.get("id") or f"lab-{len(self.labs) + 1}")
            self._lab_depth = self._depth
        elif self._lab is not None and tag == "code" and "data-run" in attributes:
            self._capture = _Capture("code", self._depth)
        elif self._lab is not None and tag == "pre" and "expected" in classes:
            self._lab.tolerance = float(attributes.get("data-tolerance") or 0)
            self._capture = _Capture("expected", self._depth)

    def handle_endtag(self, tag: str) -> None:
        if self._capture is not None and self._depth == self._capture.depth and self._lab is not None:
            text = "".join(self._capture.chunks)
            if self._capture.kind == "code":
                self._lab.code = text
            else:
                self._lab.expected = text
            self._capture = None
        if self._lab is not None and self._depth == self._lab_depth:
            self.labs.append(self._lab)
            self._lab = None
        self._depth -= 1

    def handle_data(self, data: str) -> None:
        if self._capture is not None:
            self._capture.chunks.append(data)


def extract(page: Path) -> list[Lab]:
    parser = LabExtractor(page)
    parser.feed(page.read_text(encoding="utf-8"))
    parser.close()
    return parser.labs


def outputs_match(actual: str, expected: str, tolerance: float) -> bool:
    """Token-wise comparison; numeric tokens may differ by at most ``tolerance``. Mirrors lab.js."""
    a, e = actual.split(), expected.split()
    if len(a) != len(e):
        return False
    for got, want in zip(a, e, strict=True):
        if got == want:
            continue
        if (
            _NUMBER.match(got)
            and _NUMBER.match(want)
            and math.isclose(float(got), float(want), rel_tol=0, abs_tol=tolerance)
        ):
            continue
        return False
    return True


def run(lab: Lab) -> tuple[bool, str]:
    if not lab.code.strip():
        return False, "lab has no code[data-run] block"
    if lab.expected is None:
        return False, "lab has no pre.expected block"
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "lab.py"
        script.write_text(lab.code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-I", str(script)],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=tmp,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, f"exceeded {TIMEOUT_SECONDS}s"
    if proc.returncode != 0:
        return False, f"exit {proc.returncode}: {proc.stderr.strip().splitlines()[-1] if proc.stderr else ''}"
    if proc.stderr.strip():
        return False, f"wrote to stderr (labs must not emit warnings): {proc.stderr.strip()[:200]}"
    if not outputs_match(proc.stdout, lab.expected, lab.tolerance):
        return False, f"output differs from expected:\n{proc.stdout}"
    return True, "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="*", type=Path)
    parser.add_argument("--unit", help="module or studio ID: run only that unit's pages")
    args = parser.parse_args()
    if args.unit:
        pages = sorted([*SITE.glob(f"modules/*/{args.unit}/*.html"), *SITE.glob(f"studios/{args.unit}/*.html")])
        if not pages:
            print(f"no pages found for unit {args.unit}", file=sys.stderr)
            return 1
    else:
        pages = args.pages or sorted(p for p in SITE.rglob("*.html") if "vendor" not in p.parts)
    labs = [lab for page in pages for lab in extract(page)]
    failed = 0
    for lab in labs:
        ok, detail = run(lab)
        failed += not ok
        print(
            f"{'PASS' if ok else 'FAIL'} {lab.page.relative_to(ROOT)}#{lab.lab_id}" + ("" if ok else f"\n     {detail}")
        )
    print(f"labs: {len(labs) - failed}/{len(labs)} passed on Python {sys.version.split()[0]}")
    return 1 if failed or not labs else 0


if __name__ == "__main__":
    sys.exit(main())
