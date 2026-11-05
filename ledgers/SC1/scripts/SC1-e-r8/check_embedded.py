"""For each SC1 lesson page: compare each data-run code block with its twin source, and each
class="expected" block with the twin's stdout captured under python -I -W error.

Usage: python -I check_embedded.py <out_dir_with_labs> <page> [<page> ...]
Expects <out_dir>/labs/<lab-id>.stdout written by running each twin.
"""
import html
import html.parser
import os
import sys


class Blocks(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.blocks: list[tuple[str, str]] = []  # (kind, raw text)
        self.cur: list[str] | None = None
        self.kind = ""
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "pre":
            cls = a.get("class") or ""
            if "expected" in cls:
                self.cur, self.kind = [], "expected"
            elif self.cur is None:
                self.cur, self.kind = [], "pre"
        elif tag == "code" and "data-run" in a:
            self.cur, self.kind = [], "run"

    def handle_endtag(self, tag: str) -> None:
        if tag in ("pre", "code") and self.cur is not None:
            self.blocks.append((self.kind, "".join(self.cur)))
            self.cur = None

    def handle_data(self, data: str) -> None:
        if self.cur is not None:
            self.cur.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.cur is not None:
            self.cur.append(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        if self.cur is not None:
            self.cur.append(html.unescape(f"&#{name};"))


def main() -> None:
    out_dir = sys.argv[1]
    for page in sys.argv[2:]:
        with open(page, encoding="utf-8") as fh:
            src = fh.read()
        p = Blocks()
        p.feed(src)
        lab_id = None
        for kind, text in p.blocks:
            if kind == "run":
                # The twin id is the lab id named in the section that contains this block.
                pass
        # Map each run/expected pair by order inside the page: run block then expected block per lab.
        runs = [t for k, t in p.blocks if k == "run"]
        exp = [t for k, t in p.blocks if k == "expected"]
        ids = []
        for line in src.split("\n"):
            if 'id="lab-SC1-' in line and 'class="lab' in line:
                start = line.index('id="lab-SC1-') + 4
                ids.append(line[start:line.index('"', start)])
        print(f"{os.path.basename(page)}: lab sections={ids} run blocks={len(runs)} expected blocks={len(exp)}")
        for i, (run, expected) in enumerate(zip(runs, exp)):
            lab = ids[i] if i < len(ids) else f"#{i}"
            twin_id = lab.replace("lab-SC1-", "lab-SC1-")
            stdout_path = os.path.join(out_dir, "labs", f"{twin_id}-1.stdout")
            if not os.path.exists(stdout_path):
                stdout_path = os.path.join(out_dir, "labs", f"{twin_id}.stdout")
            with open(stdout_path, encoding="utf-8") as fh:
                actual = fh.read()
            twin_path = os.path.join("tests", "labs", "SC1", f"{twin_id}.py")
            with open(twin_path, encoding="utf-8") as fh:
                twin = fh.read()
            code_equal = run.strip("\n") == twin.strip("\n")
            out_equal = expected.strip("\n") == actual.strip("\n")
            print(f"  {lab}: code==twin {code_equal}; expected==stdout {out_equal}")


if __name__ == "__main__":
    main()
