"""Extract readable text from a lesson page, one block per line (read-only, stdlib only).

Usage: extract_text.py <page.html>   (prints to stdout; drops script and style bodies)
"""
import html.parser
import re
import sys


class Extract(html.parser.HTMLParser):
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "table", "dt", "dd", "figcaption",
             "details", "summary", "blockquote", "pre", "ul", "ol", "dl", "caption", "th", "td"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.buf: list[str] = []
        self.skip = 0

    def flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in self.BLOCK:
            self.flush()
        attr = dict(attrs)
        if tag == "span" and "class" in attr and attr["class"] and "katex" in str(attr["class"]):
            pass
        if tag == "br":
            self.flush()
        self.tag_stack_marks(tag, attr)

    def tag_stack_marks(self, tag: str, attr: dict) -> None:  # type: ignore[type-arg]
        if tag in ("h1", "h2", "h3", "h4"):
            self.buf.append(f"[{tag}] ")
        if tag == "math" or tag == "annotation":
            pass

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in self.BLOCK:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.skip == 0:
            self.buf.append(data)


def main() -> None:
    parser = Extract()
    parser.feed(open(sys.argv[1], encoding="utf-8").read())
    parser.flush()
    for line in parser.out:
        print(line)


if __name__ == "__main__":
    main()


def page_text(path: str) -> str:
    """Return the extracted visible text of a page as one string (used by the check scripts)."""
    parser = Extract()
    parser.feed(open(path, encoding="utf-8").read())
    parser.flush()
    return "\n".join(parser.out)
