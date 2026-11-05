"""SC1-c round 7: why-it-matters word counts, <dfn> inventory, and template counts for L07/L08 (stdlib only)."""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
for page in ("L07", "L08"):
    text = (ROOT / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    plain = re.sub(r"<[^>]+>", " ", m.group(1))
    plain = re.sub(r"\\\((.*?)\\\)", r" \1 ", plain)
    words = len(plain.split())
    print(f"{page} why-it-matters words (tags stripped, math source kept): {words}")
    one_token = re.sub(r"<[^>]+>", " ", re.sub(r"\\\(.*?\\\)", " M ", m.group(1)))
    print(f"{page} why-it-matters whitespace tokens, each math span one token: {len(one_token.split())}")
    no_math = re.sub(r"<[^>]+>", " ", re.sub(r"\\\(.*?\\\)", " ", m.group(1)))
    print(f"{page} why-it-matters prose words, math removed: {len(no_math.split())}")
    print(f"{page} dfn tags:", re.findall(r"<dfn[^>]*>", text))
    print(f"{page} problems:", len(re.findall(r'<div class="problem"', text)),
          "solutions:", len(re.findall(r'<details class="solution"', text)),
          "tiers:", re.findall(r'data-tier="(\w+)"', text),
          "misconceptions:", len(re.findall(r'<li class="misconception"', text)),
          "quiz items:", len(re.findall(r'<li class="item"', text)),
          "key-result rows:", len(re.findall(r"<tr><td>", text)))
    print(f"{page} data-hours:", re.findall(r'data-hours="(\d+)"', text), "explain blocks:", len(re.findall(r'class="explain"', text)))
