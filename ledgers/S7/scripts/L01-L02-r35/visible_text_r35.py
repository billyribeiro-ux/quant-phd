"""Round-35 visible-text extractor for S7 L01/L02 (input for the archived prose and recompute scripts).

Usage: .venv/bin/python -I ledgers/S7/scripts/L01-L02-r35/visible_text_r35.py <git-rev> <out-dir>
Reads course/modules/S/S7/{L01,L02}.html from the given git revision (git show) and writes <out-dir>/{L01,L02}.txt.
Text inside <script> and <style> is dropped; entities are decoded; block tags become newlines.
"""

from __future__ import annotations

import html.parser
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "figcaption", "section", "pre", "br", "td", "th", "dt", "dd"}


class Visible(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def main() -> int:
    rev, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name in ("L01", "L02"):
        src = subprocess.run(
            ["git", "show", f"{rev}:course/modules/S/S7/{name}.html"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        parser = Visible()
        parser.feed(src)
        text = "".join(parser.parts)
        lines = [" ".join(ln.split()) for ln in text.split("\n")]
        (out / f"{name}.txt").write_text("\n".join(ln for ln in lines if ln) + "\n", encoding="utf-8")
        print(name, "written", len("".join(lines)), "chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
