"""LX2-d round 4: compare each lesson's printed-output <pre> block with the twin's real output.

Usage: python3 -I lab_output_vs_lesson.py <checkout-root> <outdir-with-twin-outputs>
For each lesson page, every <pre> block that does not contain Python code (no 'def ' / 'import ')
is compared line by line with the twin output (the lines of the twin output, stripped of trailing spaces).
A block PASSes when every one of its non-empty lines occurs, in order, in the twin output.
Prints one line per block with the lesson name, the block index and the result.
"""
import html.parser
import sys
from pathlib import Path


class Pre(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[str] = []
        self.buf: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "pre":
            self.buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre" and self.buf is not None:
            self.blocks.append("".join(self.buf))
            self.buf = None

    def handle_data(self, data: str) -> None:
        if self.buf is not None:
            self.buf.append(data)


def main() -> None:
    root = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    twins = {"L01": "lab-LX2-L01-1.py", "L02": "lab-LX2-L02-1.py", "L03": "lab-LX2-L03-1.py", "L04": "lab-LX2-L04-1.py"}
    for lesson, twin in twins.items():
        page = Pre()
        page.feed((root / f"course/modules/LX/LX2/{lesson}.html").read_text(encoding="utf-8"))
        out_lines = [ln.rstrip() for ln in (outdir / f"twin-{lesson}-1.out").read_text(encoding="utf-8").splitlines()]
        for idx, block in enumerate(page.blocks):
            if "def " in block or "import " in block or "class " in block:
                continue
            lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
            if not lines:
                continue
            pos = 0
            missing = []
            for ln in lines:
                try:
                    pos = out_lines.index(ln, pos) + 1
                except ValueError:
                    missing.append(ln)
            status = "PASS" if not missing else "FAIL"
            print(f"{lesson} pre#{idx} lines={len(lines)} {status} missing={missing[:3]}")


if __name__ == "__main__":
    main()
