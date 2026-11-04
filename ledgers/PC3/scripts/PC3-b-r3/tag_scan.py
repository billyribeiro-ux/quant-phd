"""Tag-balance and raw-less-than scan for PC3 L04-L06 pages (stdlib only).

Usage: python -I tag_scan.py <checkout-root>
Reports start tags, end tags that do not match an open tag, and tags left open at end.
Also reports raw '<' followed by a letter or backslash in the file text (candidate markup breaks).
"""
import html.parser
import re
import sys

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Scan(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.bad_starts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        pass

    def handle_endtag(self, tag: str) -> None:
        line = self.getpos()[0]
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {line}: stray </{tag}>")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # search for matching open tag
        idx = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                idx = i
                break
        if idx is None:
            self.errors.append(f"line {line}: </{tag}> with no open <{tag}>")
        else:
            opened = self.stack[idx:]
            self.errors.append(f"line {line}: </{tag}> closes open " + ", ".join(f"<{t}>@{l}" for t, l in opened[1:]))
            del self.stack[idx:]


def main() -> int:
    root = sys.argv[1]
    total = 0
    for p in ("L04", "L05", "L06"):
        path = f"{root}/course/modules/PC/PC3/{p}.html"
        text = open(path, encoding="utf-8").read()
        s = Scan()
        s.feed(text)
        s.close()
        print(f"== {p}: parse errors={len(s.errors)} unclosed-at-end={len(s.stack)}")
        for e in s.errors:
            print("  ", e)
        for t, l in s.stack:
            print(f"   unclosed <{t}> opened at line {l}")
        total += len(s.errors) + len(s.stack)
        # raw less-than followed by letter or backslash, outside of tags
        for n, line in enumerate(text.splitlines(), 1):
            for m in re.finditer(r"<(?=[A-Za-z\\])", line):
                # skip genuine tags: a tag starts with <name followed by space, > or /
                seg = line[m.start():m.start() + 40]
                if re.match(r"<(?:[a-zA-Z][a-zA-Z0-9]*)(?:[\s/>])", seg) and not re.match(r"<\\", seg):
                    continue
                print(f"   raw '<' line {n} col {m.start() + 1}: {line[max(0, m.start() - 30):m.start() + 30]!r}")
    print(f"TOTAL structural issues: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
