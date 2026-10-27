"""Case-insensitive scan of L07/L08 learner text (tags stripped) for banned strings and process words."""
import re, sys, html
PHRASES = ["todo", "tbd", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
           "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
           "obviously", "clearly", "roughly half", "about 6%", "historically", "it can be shown that", "…", "...",
           "this build", "builder", "requests", "unit report", "recall", "dechow", "mohanram", "lee", "nichols",
           "bot check", "jstor"]
for path in sys.argv[1:]:
    raw = open(path, encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    low = text.lower()
    hits = {p: [m.start() for m in re.finditer(re.escape(p), low)] for p in PHRASES}
    print(path.split("AC2/")[-1], {p: len(v) for p, v in hits.items() if v})
    for p, v in hits.items():
        for pos in v[:3]:
            if p in ("lee", "recall", "requests", "clearly", "...") or p.startswith("…"):
                print("   ", repr(p), "::", re.sub(r"\s+", " ", text[max(0, pos - 60):pos + 60]))
