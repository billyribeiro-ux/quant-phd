"""Blind extraction of the memo prose of each exemplar (VERIFIER ruling 15, round 15).

Drops: aside.annotation (annotation elements), p.exemplar-verdict (verdict lines), h4 (exemplar titles),
and every data-score / data-scores / data-level / data-criterion attribute (attributes are never printed).
Prints only the remaining text of each <article class="exemplar">, one line per <p>, <li>, <h5>, <td>, <th>.
Usage: python -I strip_exemplars.py <project.html>
"""

import sys
from html.parser import HTMLParser

VOID = {"br", "img", "input", "meta", "link", "hr", "col", "source", "wbr"}
BLOCK = {"p", "li", "h5", "td", "th", "h4", "h3", "h2", "div", "aside", "ul", "ol", "table", "tr"}


class Stripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        # one entry per open element: (tag, dropped?, is_exemplar_article)
        self.stack: list[tuple[str, bool, bool]] = []
        self.out: list[str] = []
        self.buf: list[str] = []
        self.exemplar_depth = 0

    def _flush(self) -> None:
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.append(text)
        self.buf = []

    def _dropped(self) -> bool:
        return any(d for _, d, _ in self.stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in VOID:
            return
        a = {k: (v or "") for k, v in attrs}
        cls = a.get("class", "").split()
        in_ex = self.exemplar_depth > 0
        drop = self._dropped()
        is_article = tag == "article" and "exemplar" in cls
        if is_article:
            self._flush()
            self.out.append(f"=== article {a.get('id', '?')} ===")
            self.exemplar_depth += 1
            is_article_flag = True
        else:
            is_article_flag = False
        if in_ex and not drop and (
            (tag == "aside" and "annotation" in cls) or (tag == "p" and "exemplar-verdict" in cls) or tag == "h4"
        ):
            self._flush()
            drop = True
        if in_ex and not drop and tag in BLOCK:
            self._flush()
        self.stack.append((tag, drop, is_article_flag))

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, _, was_article = self.stack[i]
                del self.stack[i:]
                if was_article:
                    self._flush()
                    self.exemplar_depth -= 1
                    self.out.append("=== end article ===")
                elif self.exemplar_depth > 0 and not self._dropped() and tag in BLOCK:
                    self._flush()
                break

    def handle_data(self, data: str) -> None:
        if self.exemplar_depth > 0 and not self._dropped():
            self.buf.append(data)


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8").read()
    s = Stripper()
    s.feed(src)
    s._flush()
    print("\n".join(s.out))


if __name__ == "__main__":
    main()
