"""Structural counts for the E4 slice pages: why-it-matters words, solution lengths, quiz items, problem tiers, misconceptions."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for name in ["index", "L01", "L02", "L03"]:
    text = (root / f"course/modules/E/E4/{name}.html").read_text(encoding="utf-8")
    if name != "index":
        m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
        plain = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
        plain = re.sub(r"\\\((.*?)\\\)", r"\1", plain)
        print(f"{name} why-it-matters words: {len(plain.split())}")
        sols = re.findall(r'<details class="solution">(.*?)</details>', text, re.S)
        lens = [len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split()) for s in sols]
        print(f"{name} solutions: {len(sols)}; shortest {min(lens)} words; min is at least 15: {min(lens) >= 15}")
        print(f"{name} problem ids:", re.findall(r'class="problem" id="([A-Z]\d)"', text))
        print(f"{name} misconceptions:", text.count('class="misconception"'))
        items = re.findall(r'<li class="item"', text)
        print(f"{name} quiz items: {len(items)}")
        print(f"{name} explain blocks: {text.count('class=\"explain\"')}")
    else:
        print("index data-hours:", re.findall(r'data-hours-[a-z]+="\d+"', text))
        print("index placement items:", text.count('<li class="item"'), "skill items:", text.count("data-skill"))
        print("index lesson cards:", text.count('class="card"'))
