"""Structure, word-count and count checks for M2 lessons L13 to L18 (verifier scratch, round 1)."""
import html
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
for n in range(13, 19):
    s = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    hours = re.search(r'data-hours="(\d+)"', s).group(1)
    heads = re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)
    heads = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in heads]
    main = s
    why = re.search(r'<p class="why"[^>]*>(.*?)</p>', s, re.S)
    if why:
        why_words = len(html.unescape(re.sub(r"<[^>]+>", "", why.group(1))).split())
    else:
        # fallback: first paragraph in the first section
        m = re.search(r"<section[^>]*>\s*<p>(.*?)</p>", s, re.S)
        why_words = len(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split()) if m else -1
    sol = len(re.findall(r'<details class="solution"', s))
    quiz_items = len(re.findall(r'<fieldset', s)) or len(re.findall(r'class="quiz-item|data-quiz-item', s))
    misc = len(re.findall(r"<h3>Misconception|class=\"misconception", s))
    print(f"L{n}: data-hours={hours} why_words={why_words} solutions={sol} quiz_fieldsets={quiz_items} misconception_blocks={misc}")
    print(f"    h2 order: {heads}")
