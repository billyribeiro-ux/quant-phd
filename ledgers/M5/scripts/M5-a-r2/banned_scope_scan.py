"""Slice a round 2: banned-phrase, process-word, figure, data and scope-word scan over the hub, L01-L04 pages and their cards."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = ["index", "L01", "L02", "L03", "L04"]
banned = ["TODO", "TBD", "lorem", "for brevity", "beyond the scope", "important to note", "studies show",
          "well known", "obviously", "clearly", "left as an exercise", "you can add more", "details omitted",
          "experts agree", "builder", "verifier", "ledger", "architect", "planner"]
scope = re.compile(r"\b(always|never|exactly|only|same|drives|every|all|any)\b", re.I)
for p in pages:
    raw = (root / f"course/modules/M/M5/{p}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    hits = {b: len(re.findall(re.escape(b), text, re.I)) for b in banned}
    print(p, "banned hits:", {k: v for k, v in hits.items() if v} or "none",
          "| svg/chart/figures:", len(re.findall(r"<svg|class=\"chart|figures-", raw)),
          "| data-files:", raw.count("data-files"), "| unexpanded markers:", len(re.findall(r"@@(LAB|OUT):", raw)),
          "| scope-word hits:", len(scope.findall(text)))
cards = json.load(open(root / "course/modules/M/M5/cards.json", encoding="utf-8"))
ctext = " ".join(c["front"] + " " + c["back"] for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04"))
print("cards L01-L04 banned hits:", {b: len(re.findall(re.escape(b), ctext, re.I)) for b in banned if re.search(re.escape(b), ctext, re.I)} or "none")
