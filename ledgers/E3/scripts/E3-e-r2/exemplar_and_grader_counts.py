"""Word counts and data facts behind the project page's exemplar and instance claims (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/exemplar_and_grader_counts.py  (run from the checkout root)
"""

import re
from fractions import Fraction
from html.parser import HTMLParser

PAGE = "course/modules/E/E3/project.html"


class Memo(HTMLParser):
    """Collects the text of every div.memo-text (headings included), per exemplar article, one entry per memo block."""

    def __init__(self) -> None:
        super().__init__()
        self.article: str | None = None
        self.depth = 0
        self.memo_start: int | None = None
        self.current: list[str] = []
        self.blocks: dict[str, list[list[str]]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "article" and a.get("class") == "exemplar":
            self.article = a.get("id")
            self.blocks.setdefault(self.article or "", [])
        if tag == "div":
            if a.get("class") == "memo-text":
                self.memo_start = self.depth
                self.current = []
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "div":
            self.depth -= 1
            if self.memo_start is not None and self.depth == self.memo_start:
                self.blocks[self.article or ""].append(self.current)
                self.memo_start = None

    def handle_data(self, data: str) -> None:
        if self.memo_start is not None:
            self.current.append(data)


p = Memo()
text = open(PAGE, encoding="utf-8").read()
p.feed(text)
for name, blocks in p.blocks.items():
    counts = [len(" ".join(b).split()) for b in blocks]
    print(f"{name}: memo blocks {len(blocks)}, words per block {counts}, total {sum(counts)} (headings included)")

start = text.index("ANSWERS: list[")
end = text.index("\n]\n", start) + 3
ns: dict[str, object] = {"Fraction": Fraction}
exec(text[start:end], ns)
ans = ns["ANSWERS"]
assert isinstance(ans, list)
prizes = [x for a in ans for x in a[2] + a[4]]
print("lab-3 answers:", len(ans), "| prize range (cents):", min(prizes), max(prizes))
print("prizes per lottery:", sorted({len(a[2]) for a in ans} | {len(a[4]) for a in ans}))


def is_mixed(pz: list[int], pr: list[str]) -> bool:
    g = any(x > 0 and Fraction(q) > 0 for x, q in zip(pz, pr, strict=True))
    lo = any(x < 0 and Fraction(q) > 0 for x, q in zip(pz, pr, strict=True))
    return g and lo


print("pairs with a mixed lottery:", sum(is_mixed(a[2], a[3]) or is_mixed(a[4], a[5]) for a in ans))
print("every probability list sums to exactly 1:",
      all(sum(Fraction(q) for q in a[3]) == 1 and sum(Fraction(q) for q in a[5]) == 1 for a in ans))
print("pair 0 A:", ans[0][2], ans[0][3], "| pair 3 A:", ans[3][2], ans[3][3], "| pair 3 B:", ans[3][4], ans[3][5])

# Alternative method: TeX math spans removed (each span counted as nothing), to test whether 375 uses rendered text.
for name, blocks in p.blocks.items():
    raw = " ".join(" ".join(b) for b in blocks)
    no_math = re.sub(r"\\\((.*?)\\\)", " ", raw, flags=re.S)
    print(f"{name}: words with TeX math spans removed = {len(no_math.split())}")
