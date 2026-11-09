"""Banned-phrase, process-word, scope-word and rhetorical-question scan over the visible text of slice-b pages and their cards."""
import re, html, json, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS4-M2-b")
PAGES = ["L07", "L08", "L09", "L10", "L11", "L12"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "roughly", "historically", "about 6%", "in practice",
          "motivat", "let us", "we will see", "in this lesson we", "this lesson will", "by now you",
          "as we saw", "ruling", "builder", "verifier", "ledger", "fixer", "round ", "lab output shows that"]
SCOPE = ["only", "all ", "always", "every", "any ", "same", "exactly", "small", "fast", "smooth", "most", "typically", "drives"]
PROCESS = ["builder", "verifier", "ledger", "ruling", "architect", "plan ", "fanout", "checkout", "pin "]
def visible(raw):
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))
for L in PAGES:
    raw = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    t = visible(raw)
    low = t.lower()
    hits = {b: low.count(b.lower()) for b in BANNED if b.lower() in low}
    scope = {s.strip(): low.count(s) for s in SCOPE if s in low}
    qs = [m.start() for m in re.finditer(r"\?", t)]
    qctx = [re.sub(r"\s+", " ", t[max(0, q - 60):q + 1]) for q in qs]
    print(f"{L}: banned_hits={hits} process_hits={[p for p in PROCESS if p in low]} question_marks={len(qs)}")
    print("   scope words:", scope)
    for c in qctx:
        print("   ?", c)
cards = json.loads((ROOT / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
for c in cards:
    if c["lesson"] in PAGES:
        s = (c["front"] + " " + c["back"]).lower()
        h = [b for b in BANNED if b.lower() in s] + [p for p in PROCESS if p in s]
        if h or "?" in c["back"]:
            print("CARD", c["id"], h, c["front"][:80])
