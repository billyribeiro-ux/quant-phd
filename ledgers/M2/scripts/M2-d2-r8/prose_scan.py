"""Prose scan of L22-L24 pages: macros used vs notation.json, banned strings, process words, scope words,
registered symbols, and HTML-only checks (images, external URLs, inline style, script src)."""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(".").resolve()
PAGES = ["L22", "L23", "L24"]
notation = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered = set(notation["macros"].keys())
TAG = re.compile(r"<[^>]+>")
for pg in PAGES:
    raw = (ROOT / f"course/modules/M/M2/{pg}.html").read_text(encoding="utf-8")
    macros = Counter(re.findall(r"\\([A-Za-z]+)", raw))
    unreg = {m: n for m, n in macros.items() if "\\" + m not in registered}
    print(f"== {pg}: macros used (count), unregistered:")
    print("   all:", dict(macros.most_common()))
    print("   unregistered:", unreg)
    print("   \\mathbb/\\mathcal/\\mathrm present:", len(re.findall(r"\\mathbb|\\mathcal", raw)))
    print("   \\R count:", raw.count("\\R"), " literal \\\\mathbb{R}:", raw.count("\\mathbb{R}"))
    text = html.unescape(TAG.sub(" ", re.sub(r"<pre><code.*?</code></pre>", " ", raw, flags=re.S)))
    text = re.sub(r"<pre[^>]*>.*?</pre>", " ", text, flags=re.S)
    text = re.sub(r"\s+", " ", text)
    banned = ["TODO", "TBD", "lorem", "...", "…", "for brevity", "details omitted", "beyond the scope",
              "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
              "it is well known", "obviously", "clearly", "round-", "Round ", "builder", "Builder", "verifier",
              "Verifier", "architect", "Architect", "fixed in", "round 7", "round 8", "R7", "R8", "DAG_DEFECT",
              "NOTATION_REQUEST", "REFERENCE_REQUEST", "GLOSSARY_REQUEST", "Q1", "Q3", "Q8", "Open item", "open item",
              "the lab checks", "Pseudocode", "http://", "https://", "<img", "<iframe", "<script src", "style=\"", "style='"]
    hits = {b: text.count(b) for b in banned if b in text}
    print("   banned/process hits:", hits)
    for b in ["only", "all", "always", "every", "any", "same", "drives", "exactly", "most", "small", "about",
              "never", "no ", "none", "every"]:
        pass
    scope = Counter()
    for w in ["only", "all ", "always", "every", "any ", "same", "exactly", "most", "small", "never", "none"]:
        scope[w] = len(re.findall(r"\b" + re.escape(w.strip()) + r"\b", text))
    print("   scope word counts:", dict(scope))
    style = len(re.findall(r"style=", raw))
    print("   inline style attributes:", style, " external hrefs:", re.findall(r'(?:href|src)="(https?:[^"]+)"', raw))
    wtm = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    words = len(html.unescape(TAG.sub(" ", wtm.group(1))).split()) if wtm else -1
    print("   why-it-matters words:", words)
    cnt = len(re.findall(r'<li class="item"', raw))
    print("   quiz items:", cnt)
    mis = len(re.findall(r'<li class="misconception"', raw))
    print("   misconceptions:", mis)
    solutions = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    short = [i for i, s in enumerate(solutions) if len(html.unescape(TAG.sub(" ", s)).split()) < 15]
    print("   solutions:", len(solutions), " shorter than 15 words (index):", short)
    tiers = re.findall(r'<div class="tier" data-tier="(\w+)"', raw)
    print("   tiers:", tiers, " problems:", len(re.findall(r'<div class="problem"', raw)))
