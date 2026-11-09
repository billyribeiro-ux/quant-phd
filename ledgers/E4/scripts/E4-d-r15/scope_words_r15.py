"""Round-15 scope-word scan of the E4 project page prose (fixer rule: only, all, always, every, any, same, drives,
offsets, as much as, exactly). Prints each occurrence with its line and the 100 characters around it.
Usage: python -I scope_words_r15.py <page.html>"""
import re
import sys

WORDS = r"\b(only|all|always|every|any|same|drives?|offsets?|exactly|never|no|none|always|each)\b"
src = open(sys.argv[1], encoding="utf-8").read()
text = re.sub(r"<[^>]+>", " ", src)
for n, line in enumerate(src.split("\n"), 1):
    plain = re.sub(r"<[^>]+>", " ", line)
    for m in re.finditer(WORDS, plain, flags=re.I):
        s = max(0, m.start() - 60)
        print(f"L{n} [{m.group(0)}] ...{' '.join(plain[s:m.end() + 60].split())}...")
