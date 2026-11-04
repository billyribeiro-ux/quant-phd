"""Round 5 verifier (FC1-c): plain text of each FC1 lesson, with tags removed, plus the data-grade and data-card-like attributes."""
import html.parser, pathlib, re, sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-FC1-c/course/modules/FC/FC1")
OUT = pathlib.Path("/tmp/fc1c_r5_text")
OUT.mkdir(parents=True, exist_ok=True)


class Text(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
        self.attrs_seen: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        for k, v in attrs:
            if k and (k.startswith("data-grade") or k.startswith("data-card") or k == "data-cite" or k.startswith("data-concept") or k.startswith("data-hours")):
                self.attrs_seen.append(f"<{tag} {k}={v!r}>")
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "div", "pre", "dd", "dt", "section"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


for name in ["L01", "L02", "L03", "L04", "L05", "project", "index"]:
    p = ROOT / f"{name}.html"
    t = Text()
    t.feed(p.read_text(encoding="utf-8"))
    text = "".join(t.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    (OUT / f"{name}.txt").write_text(text, encoding="utf-8")
    (OUT / f"{name}.attrs.txt").write_text("\n".join(t.attrs_seen) + "\n", encoding="utf-8")
    print(name, len(text), "chars;", len(t.attrs_seen), "grade/card attrs")
