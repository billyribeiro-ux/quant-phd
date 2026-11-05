"""Verifier structure counts (E4 slice a, round 7): why-it-matters words, solution words, misconceptions, quiz items, banned strings and process words."""
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(sys.argv[1])
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "round", "builder", "verifier", "unit report", "REQUEST"]
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    p = ROOT / "course/modules/E/E4" / name
    raw = p.read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", " ", raw, flags=re.S)  # code and expected blocks are allowed to hold "..."
    text = unescape(re.sub(r"<[^>]+>", " ", text))
    hits = [b for b in BANNED if b.lower() in text.lower()]
    print(name, "banned/process hits (outside code blocks):", hits)
    if name != "index.html":
        wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
        words = len(unescape(re.sub(r"<[^>]+>", " ", wim.group(1))).split())
        print(name, "why-it-matters words:", words)
        sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
        counts = [len(unescape(re.sub(r"<[^>]+>", " ", s)).split()) for s in sols]
        print(name, "solutions:", len(sols), "min words:", min(counts))
        mis = len(re.findall(r'<li class="misconception">', raw))
        print(name, "misconceptions:", mis)
        probs = re.findall(r'<div class="problem" id="([A-Z]\d)">', raw)
        print(name, "problems:", len(probs), probs)
        quiz = len(re.findall(r'<li class="item"', raw.split('id="quiz"')[1]))
        expl = len(re.findall(r'<div class="explain" hidden>', raw.split('id="quiz"')[1]))
        print(name, "quiz items:", quiz, "explanations:", expl)
        print(name, "data-references entries:", len(re.findall(r"<li", raw.split('data-references')[1].split('</ol>')[0])))
