#!/usr/bin/env python3
"""Embed lab code and its real output into a course page (authoring helper).

A builder writes each lab once, as its local twin ``tests/labs/<UNIT>/<lab-id>.py``,
and puts two markers in the page:

    <pre><code class="language-python" data-run>@@LAB:<lab-id>.py@@</code></pre>
    <pre class="expected" data-tolerance="1e-6">@@OUT:<lab-id>.py@@</pre>

This tool replaces ``@@LAB`` with the twin's HTML-escaped source (so page and twin
are byte-identical after unescaping) and ``@@OUT`` with the output the twin
actually prints under ``python -I -W error``. Expected outputs are therefore never
typed by hand. Pages without markers are left untouched; run_labs.py then keeps
page and twin in agreement.

After editing a twin, ``--refresh`` turns the page's embedded labs and checked
solution snippets (``data-check``) back into markers and embeds them again: all
of them, or only the listed ids. A completion lab keeps its blanked code; only its expected output (the
completed twin's) is refreshed.

Usage::

    python3 tools/embed_labs.py course/modules/S/S7/L01.html [more pages...]
    python3 tools/embed_labs.py course/modules/S/S7/L04.html --refresh lab-S7-L04-3
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = re.compile(r"@@(LAB|OUT):([A-Za-z0-9_.-]+\.py)@@")
LAB_SECTION = re.compile(r'<section class="lab(?P<cls>[^"]*)" id="(?P<id>[^"]+)".*?</section>', re.S)
CODE = re.compile(r'(<code class="language-python" data-run>).*?(</code>)', re.S)
EXPECTED = re.compile(r'(<pre class="expected"[^>]*>).*?(</pre>)', re.S)
SNIPPET_CODE = re.compile(r'<code class="language-python" data-check="([^"]+)">')


def _marker(kind: str, name: str) -> Callable[[re.Match[str]], str]:
    """A substitution that keeps the opening and closing tags and puts a marker between them."""
    return lambda m: f"{m.group(1)}@@{kind}:{name}.py@@{m.group(2)}"


def remark(text: str, twins: Path, only: set[str] | None = None) -> str:
    """Replace embedded lab code and output with markers, for every lab with a twin (or only the listed ids)."""

    def one(section: re.Match[str]) -> str:
        lab_id, body = section.group("id"), section.group(0)
        if (only and lab_id not in only) or not (twins / f"{lab_id}.py").exists():
            return body
        if "completion" not in section.group("cls").split():
            body = CODE.sub(lambda m: f"{m.group(1)}@@LAB:{lab_id}.py@@{m.group(2)}", body, count=1)
        return EXPECTED.sub(lambda m: f"{m.group(1)}@@OUT:{lab_id}.py@@{m.group(2)}", body, count=1)

    text = LAB_SECTION.sub(one, text)
    for name in {m.group(1) for m in SNIPPET_CODE.finditer(text)}:
        if (only and name not in only) or not (twins / f"{name}.py").exists():
            continue
        text = re.sub(
            rf'(<code class="language-python" data-check="{re.escape(name)}">).*?(</code>)',
            _marker("LAB", name),
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            rf'(<pre class="expected" data-check="{re.escape(name)}"[^>]*>).*?(</pre>)',
            _marker("OUT", name),
            text,
            count=1,
            flags=re.S,
        )
    return text


def run_twin(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(path)],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if result.returncode != 0 or result.stderr:
        raise RuntimeError(f"{path.name} failed or wrote to stderr:\n{result.stderr}")
    return result.stdout.rstrip("\n")


def embed(page: Path, refresh: set[str] | None = None) -> int:
    unit = re.search(r'data-unit="([^"]+)"', page.read_text(encoding="utf-8"))
    if not unit:
        raise RuntimeError(f"{page}: <html> has no data-unit")
    twins = ROOT / "tests" / "labs" / unit.group(1)
    text = page.read_text(encoding="utf-8")
    if refresh is not None:
        text = remark(text, twins, refresh or None)
    outputs: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        kind, name = match.group(1), match.group(2)
        twin = twins / name
        if not twin.exists():
            raise RuntimeError(f"{page.name}: no twin {twin.relative_to(ROOT)}")
        if kind == "LAB":
            return html.escape(twin.read_text(encoding="utf-8").rstrip("\n"), quote=False)
        if name not in outputs:
            outputs[name] = run_twin(twin)
        return html.escape(outputs[name], quote=False)

    new, count = MARKER.subn(replace, text)
    if count:
        page.write_text(new, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="+", type=Path)
    parser.add_argument("--refresh", nargs="*", metavar="LAB_ID", help="re-embed labs from their twins (all, or these)")
    args = parser.parse_args()
    refresh = None if args.refresh is None else set(args.refresh)
    try:
        for page in args.pages:
            print(f"{page}: embedded {embed(page, refresh)} markers")
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
