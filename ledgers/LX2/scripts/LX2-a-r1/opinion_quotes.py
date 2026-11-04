"""Check every quoted passage in a lesson page against the opinion text, and report the printed page where it starts.

Usage: python3 -I opinion_quotes.py <page.html> <gpo1983dirks-text> <gpo1997united-text>
The quoted passages are the text between curly double quotes inside each span.claim whose data-cite names the key.
Bracketed alterations ("[A]n") and the ellipsis are matched loosely. Prints one line per quoted passage:
FOUND <printed page(s)> data-locator=<locator> | MISSING <passage prefix>
"""

import html
import re
import sys
from pathlib import Path

HEADER_PATTERNS = [
    re.compile(r"(\d{3})\s+OCTOBER TERM"),
    re.compile(r"DIRKS v\. SEC\s+(\d{3})"),
    re.compile(r"Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})"),
    re.compile(r"(\d{3})\s+UNITED STATES v\. O.HAGAN"),
]


def fold(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("‐", "-")
    text = re.sub(r"-\n\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def page_texts(path: str) -> list[tuple[str, str]]:
    raw = Path(path).read_text(encoding="utf-8")
    out: list[tuple[str, str]] = []
    for chunk in raw.split("\f"):
        number = ""
        for pat in HEADER_PATTERNS:
            m = pat.search(chunk)
            if m:
                number = m.group(1)
                break
        out.append((number, fold(chunk)))
    return out


def passage_regex(passage: str) -> re.Pattern[str]:
    parts = re.split(r"\s*(?:…|\. \. \.)\s*", passage)
    pieces = []
    for part in parts:
        esc = re.escape(part.strip())
        esc = re.sub(r"\\\[[^\]]*\\\]", lambda m: ".{0,40}?", esc)  # bracketed alterations
        esc = esc.replace(r"\ ", r"\s+")
        pieces.append(esc)
    return re.compile(r".{0,400}?".join(pieces), flags=re.S)


def main() -> None:
    page = Path(sys.argv[1]).read_text(encoding="utf-8")
    sources = {"gpo1983dirks": page_texts(sys.argv[2]), "gpo1997united": page_texts(sys.argv[3])}
    pattern = re.compile(
        r'<span class="claim"[^>]*data-cite="([^"]+)"[^>]*data-locator="([^"]*)"[^>]*>(.*?)</span>', re.S
    )
    total = missing = 0
    for m in pattern.finditer(page):
        keys, locator, body = m.group(1), html.unescape(m.group(2)), html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))
        for key in keys.split():
            if key not in sources:
                continue
            for q in re.findall(r"“(.+?)”", body):
                total += 1
                rx = passage_regex(fold(q))
                hits = [num for num, txt in sources[key] if rx.search(txt)]
                if hits:
                    print(f"FOUND {key} pages {sorted(set(hits))} data-locator={locator} | {fold(q)[:60]}")
                else:
                    missing += 1
                    print(f"MISSING {key} data-locator={locator} | {fold(q)[:110]}")
    print(f"total passages {total} missing {missing}")


if __name__ == "__main__":
    main()
