"""Round 7 verifier: HTML tag balance and text-after-parse checks for L09-L11, and notation macro scan.
Reports every start tag name seen and each unclosed/unmatched tag; prints the text of the R1 solution after parsing."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB7-CS2-c")
VOID = {"meta", "link", "br", "input", "img", "hr", "source", "col", "area", "base", "wbr", "embed", "param", "track"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.tags = set()
        self.text_chunks = []
        self.in_data_run = False

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append(("mismatch", tag, self.getpos(), self.stack[-1] if self.stack else None))
            # pop to matching
            for k in range(len(self.stack) - 1, -1, -1):
                if self.stack[k][0] == tag:
                    del self.stack[k:]
                    break
        else:
            self.stack.pop()

    def handle_data(self, data):
        self.text_chunks.append((self.getpos()[0], data))


for lid in ("L09", "L10", "L11"):
    p = ROOT / f"course/modules/CS/CS2/{lid}.html"
    src = p.read_text(encoding="utf-8")
    c = Checker()
    c.feed(src)
    c.close()
    print(lid, "tag names:", sorted(c.tags))
    print(lid, "mismatch/unclosed errors:", len(c.errors), c.errors[:5], "unclosed at end:", c.stack[:5])
    # R1 solution text (lines 332-335) after parsing
    if lid == "L09":
        txt = " ".join(d for ln, d in c.text_chunks if 332 <= ln <= 336)
        print("L09 R1 text contains 'Check on one example':", "Check on one example" in txt, "| contains 'sum over':", "the sum over" in txt)
    # math span balance
    opens = len(re.findall(r"\\\(", src)); closes = len(re.findall(r"\\\)", src))
    print(lid, "inline math opens/closes:", opens, closes, "display \\[ / \\]:", len(re.findall(r"\\\[", src)), len(re.findall(r"\\\]", src)))
    # macros used that are not in notation.json
    macros = sorted(set(re.findall(r"\\[A-Za-z]+", src)))
    print(lid, "macros used:", macros)
    print(lid, "raw \\mathbb uses:", src.count("\\mathbb"), " \\E/\\Prob/\\R/\\N uses:", len(re.findall(r"\\(E|Prob|R|N)(?![A-Za-z])", src)))
