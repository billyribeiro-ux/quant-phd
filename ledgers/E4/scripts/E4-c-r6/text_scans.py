"""E4-c round 6: text scans of L07, L08 and L09 (stdlib only). Usage: python -I text_scans.py <checkout-root>.

1. Banned phrases (BUILDER_RULES 1.3-1.4, check_pages BANNED) and process words, in body text with tags, math spans,
   code blocks and scripts removed.
2. Registered symbols (notation/notation.json) used bare inside math spans.
3. Unlinked uses of the DAG terms D1-D10 of the plan (section 4) by name.
4. Figure count (data-chart).
5. A4/A5 numbering: every 'A5' in the three lesson pages and in cards.json (card lesson shown).
"""
import html
import json
import re
import sys

root = sys.argv[1]
PAGES = ["L07", "L08", "L09"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = ["builder", "verifier", "requests", "unit report", "round 5", "round 6", "round 4"]
DAG = ["state price", "stochastic discount", "law of one price", "martingale", "noise-trader risk", "Bayes",
       "Banach", "fixed point", "two-fund", "diagnostic expectations", "determinacy", "informed trading",
       "Walras", "CARA", "market clearing", "common knowledge", "informationally efficient"]
reg = json.load(open(root + "/notation/notation.json", encoding="utf-8"))
syms = ["T", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"]

for p in PAGES:
    raw = open(f"{root}/course/modules/E/E4/{p}.html", encoding="utf-8").read()
    t = re.sub(r"<pre.*?</pre>", " ", raw, flags=re.S)
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    spans = [m.group(1) or m.group(2) for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)]
    body = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", " ", t, flags=re.S)
    body = html.unescape(re.sub(r"<[^>]+>", " ", body)).lower()
    hits = [b for b in BANNED + PROCESS if b.lower() in body]
    print(p, "banned/process hits:", hits)
    dag = {d: body.count(d.lower()) for d in DAG if d.lower() in body}
    print(p, "DAG-term uses (plain text):", dag)
    for s in syms:
        bare = 0
        for sp in spans:
            if s.startswith("\\"):
                bare += sp.count(s)
            else:
                bare += len(re.findall(r"(?<![\\A-Za-z])" + re.escape(s) + r"(?![A-Za-z])", sp))
        if bare:
            print(p, "registered symbol", s, "used", bare, "times in math")
    print(p, "data-chart count:", raw.count("data-chart"))
    print(p, "A5 occurrences:", len(re.findall(r"\bA5\b", raw)))

cards = json.load(open(root + "/course/modules/E/E4/cards.json", encoding="utf-8"))
print("cards.json A5 in lessons:", sorted({c["lesson"] for c in cards if re.search(r"\bA5\b", c["front"] + c["back"])}))
