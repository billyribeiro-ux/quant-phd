"""Round 2, slice c: page code vs twin, expected block vs twin output, for the three project labs (stdlib only).

Usage (checkout root): python3 -I ledgers/PC3/scripts/PC3-c-r2/labs_r2.py
"""

from __future__ import annotations

import html.parser
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGE = ROOT / "course/modules/PC/PC3/project.html"
PY = str(ROOT / ".venv/bin/python")


class Blocks(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_pre = False
        self.kind = ""
        self.lab = ""
        self.buf: list[str] = []
        self.out: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "section" and "id" in a and a["id"] and a["id"].startswith("lab-PC3-project-"):
            self.lab = a["id"]
        if tag == "section" and "class" in a and "lab" in (a["class"] or "").split() and "id" in a:
            self.lab = a["id"] or ""
        if tag == "pre":
            self.in_pre = True
            self.buf = []
            cls = a.get("class") or ""
            self.kind = "expected" if cls == "expected" else "code"

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.in_pre:
            self.in_pre = False
            self.out.append((self.lab, self.kind, "".join(self.buf)))

    def handle_data(self, data: str) -> None:
        if self.in_pre:
            self.buf.append(data)


def main() -> int:
    p = Blocks()
    p.feed(PAGE.read_text(encoding="utf-8"))
    code: dict[str, str] = {}
    expected: dict[str, str] = {}
    for lab, kind, text in p.out:
        if kind == "code" and lab not in code:
            code[lab] = text
        if kind == "expected" and lab not in expected:
            expected[lab] = text
    labs = {
        "lab-PC3-project-1": "lab-PC3-project-1.py",
        "lab-PC3-project-2": "lab-PC3-project-2.py",
        "lab-PC3-project-3": "lab-PC3-project-3.py",
    }
    rc = 0
    for lab, twin in labs.items():
        twin_text = (ROOT / "tests/labs/PC3" / twin).read_text(encoding="utf-8")
        page_lines = code[lab].rstrip("\n").split("\n")
        twin_lines = twin_text.rstrip("\n").split("\n")
        diffs = []
        if len(page_lines) != len(twin_lines):
            diffs.append(f"line count page {len(page_lines)} twin {len(twin_lines)}")
        for i, (pl, tl) in enumerate(zip(page_lines, twin_lines), start=1):
            if pl != tl and "___" not in pl:
                diffs.append(f"line {i}: page {pl!r} != twin {tl!r}")
        blanks = [pl for pl in page_lines if "___" in pl]
        print(f"{lab}: page-vs-twin differing lines (non-blank) = {len(diffs)}; blank lines = {blanks}")
        for d in diffs[:5]:
            print("   ", d)
        if diffs:
            rc = 1
        # expected block vs twin run, python -I -W error
        run = subprocess.run(
            [PY, "-I", "-W", "error", str(ROOT / "tests/labs/PC3" / twin)],
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"  twin exit={run.returncode} stderr_len={len(run.stderr)}")
        exp = expected[lab].rstrip("\n")
        got = run.stdout.rstrip("\n")
        same = exp == got
        print(f"  expected block == twin stdout: {same}")
        if not same:
            rc = 1
            for i, (e, g) in enumerate(zip(exp.split("\n"), got.split("\n")), start=1):
                if e != g:
                    print(f"    line {i}: expected {e!r} got {g!r}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
