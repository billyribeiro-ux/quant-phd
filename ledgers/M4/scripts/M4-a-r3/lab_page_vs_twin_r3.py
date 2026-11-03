"""Compare each slice-a lab section (code and expected block) with its twin and with the twin's stdout."""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
REPORT = Path(sys.argv[3])
PAGES = {"L01": "L01", "L02": "L02", "L03": "L03", "L04": "L04"}


class Labs(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_lab = False
        self.lab_depth = 0
        self.labs: list[dict[str, str]] = []
        self.cur: dict[str, str] | None = None
        self.capture: str | None = None
        self.buf: list[str] = []
        self.depth_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "section" and "lab" in cls.split() and a.get("data-runtime") == "python":
            self.cur = {"id": a.get("id") or "", "code": "", "expected": "", "runtime": a.get("data-runtime") or ""}
            self.labs.append(self.cur)
            self.lab_depth = 1
            self.in_lab = True
            return
        if self.in_lab:
            if tag == "section":
                self.lab_depth += 1
            if tag == "code" and "data-run" in a:
                self.capture = "code"
                self.buf = []
            if tag == "pre" and "expected" in cls.split():
                self.capture = "expected"
                self.buf = []

    def handle_endtag(self, tag: str) -> None:
        if self.in_lab:
            if tag == "section":
                self.lab_depth -= 1
                if self.lab_depth == 0:
                    self.in_lab = False
                    self.cur = None
            if tag in ("code", "pre") and self.capture is not None:
                assert self.cur is not None
                if self.capture == "code" and tag == "code":
                    self.cur["code"] = "".join(self.buf)
                    self.capture = None
                elif self.capture == "expected" and tag == "pre":
                    self.cur["expected"] = "".join(self.buf)
                    self.capture = None

    def handle_data(self, data: str) -> None:
        if self.capture is not None:
            self.buf.append(data)


lines: list[str] = []
for page in PAGES:
    p = ROOT / "course/modules/M/M4" / f"{page}.html"
    text = p.read_text(encoding="utf-8")
    parser = Labs()
    parser.feed(text)
    lines.append(f"{page}: python labs={len(parser.labs)} ids={[l['id'] for l in parser.labs]}")
    for lab in parser.labs:
        lab_id = lab["id"]
        twin_name = lab_id.replace("lab-M4-", "lab-M4-") + ".py"
        twin = (ROOT / "tests/labs/M4" / twin_name).read_text(encoding="utf-8")
        code = lab["code"]
        code_eq = code.rstrip("\n") == twin.rstrip("\n")
        out_path = OUT / f"{page}.out"
        stdout = out_path.read_text(encoding="utf-8")
        exp = lab["expected"]
        exp_norm = exp.strip("\n")
        out_norm = stdout.strip("\n")
        lines.append(f"  {lab_id}: code_equals_twin={code_eq} expected_equals_stdout={exp_norm == out_norm} "
                     f"code_len={len(code)} twin_len={len(twin)} exp_len={len(exp)} out_len={len(stdout)}")
        if exp_norm != out_norm:
            import difflib
            for d in difflib.unified_diff(out_norm.splitlines(), exp_norm.splitlines(), "stdout", "expected", lineterm=""):
                lines.append("    " + d)
        if not code_eq:
            import difflib
            for d in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
                lines.append("    " + d)
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
