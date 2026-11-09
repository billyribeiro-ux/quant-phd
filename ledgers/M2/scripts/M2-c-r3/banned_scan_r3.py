"""Banned-phrase, process-word and scope-word scan of L13-L18 pages, cards and twins (verifier round 3). Standard library only."""
import json, re
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more",
          "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly"]
process = ["architect", "builder", "verifier", "planner", "ledger", "fanout", "round 2", "round 3", "page_smoke", "run_labs", "check_pages"]
scope = ["only", "always", "every", "all", "exactly", "same", "small", "most", "typically", "smooth", "in practice", "any", "never"]
files = [f"course/modules/M/M2/L{n:02d}.html" for n in range(13, 19)] + [f"tests/labs/M2/lab-M2-L{n:02d}-1.py" for n in range(13, 19)]
for f in files:
    raw = open(f, encoding="utf-8").read()
    text = re.sub(r"<script.*?</script>|<[^>]+>", " ", raw, flags=re.S).lower()
    b = [w for w in banned if w.lower() in text]
    p = [w for w in process if w in text]
    counts = {w: len(re.findall(r"\b%s\b" % re.escape(w), text)) for w in scope}
    print(f, "banned:", b, "process:", p, "scope:", {k: v for k, v in counts.items() if v})
cards = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in ("L13", "L14", "L15", "L16", "L17", "L18")]
ctext = " ".join(c["front"] + " " + c["back"] for c in sl).lower()
print("cards slice banned:", [w for w in banned if w.lower() in ctext], "process:", [w for w in process if w in ctext])
