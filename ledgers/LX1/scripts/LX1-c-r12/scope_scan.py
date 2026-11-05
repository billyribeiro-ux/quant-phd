"""Lists sentences of learner-visible prose (outside <pre>, <script>, <style>) containing scope words, with line numbers."""
import html
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
masked = re.sub(r"<(pre|script|style)\b.*?</\1>", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
text = re.sub(r"<[^>]+>", " ", masked)
scope = re.compile(r"\b(only|all|always|every|any|same|drives|exactly|never|Every|Only|All|Any)\b")
lines = masked.split("\n")
for i, line in enumerate(lines, 1):
    plain = html.unescape(re.sub(r"<[^>]+>", " ", line))
    for sent in re.split(r"(?<=[.;:])\s+", plain):
        if scope.search(sent):
            print(f"L{i}: {sent.strip()[:220]}")
