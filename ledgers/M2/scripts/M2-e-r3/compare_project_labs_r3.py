"""Round-3 check of the project labs: page code equals twin, twin runs clean, expected block equals output."""

import difflib
import html
import pathlib
import subprocess
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(sys.argv[1])
PAGE = ROOT / "course/modules/M/M2/project.html"


class Pres(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.blocks: list[tuple[dict[str, str], str]] = []
        self.current: list[str] = []
        self.attrs: dict[str, str] = {}
        self.section_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "section":
            self.section_stack.append(a.get("id", ""))
        if tag == "pre":
            self.depth += 1
            self.attrs = dict(a, _section=self.section_stack[-1] if self.section_stack else "")
            self.current = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.depth:
            self.depth -= 1
            self.blocks.append((self.attrs, "".join(self.current)))
        if tag == "section" and self.section_stack:
            self.section_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.current.append(data)


p = Pres()
p.feed(PAGE.read_text(encoding="utf-8"))
print("pre blocks:", len(p.blocks))
for attrs, text in p.blocks:
    print("  section", attrs.get("_section"), "| class", attrs.get("class", ""), "| first line", repr(text.splitlines()[0][:60]) if text else "")

labs = {1: "lab-M2-project-1", 2: "lab-M2-project-2", 3: "lab-M2-project-3"}
code_blocks = [t for a, t in p.blocks if t.lstrip().startswith(('"""', "from", "import"))]
expected = [t for a, t in p.blocks if t.lstrip()[:20].startswith(("unrounded", "second difference", "AD derivative", "rounded", "step h"))]
for n, name in labs.items():
    twin = (ROOT / "tests/labs/M2" / f"{name}.py").read_text(encoding="utf-8")
    page_code = code_blocks[n - 1]
    diff = [l for l in difflib.unified_diff(twin.splitlines(), page_code.splitlines(), lineterm="") if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    print(f"{name}: page code vs twin differing lines = {len(diff)}")
    for l in diff[:8]:
        print("    ", l)
    r = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(ROOT / "tests/labs/M2" / f"{name}.py")], capture_output=True, text=True)
    print(f"{name}: twin rc={r.returncode} stderr={r.stderr.strip()[:200]!r}")
    out_expected = expected[n - 1].strip("\n") if n - 1 < len(expected) else None
    print(f"{name}: twin stdout == expected block: {r.stdout.strip() == (out_expected or '').strip()}")
    print("   expected block first line:", repr((out_expected or "").splitlines()[0][:70]) if out_expected else None)
