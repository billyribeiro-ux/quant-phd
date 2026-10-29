"""Round-8 process-word scan over all M2 lesson pages, project.html and cards.json (visible text only)."""
import html, json, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
pats = [r"\bTODO\b", r"\bTBD\b", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
        r"left as an exercise", r"it is important to note", r"studies show", r"experts agree", r"it is well known",
        r"\bobviously\b", r"\bclearly\b", r"\broughly\b", r"\bhistorically\b", r"\bapprox", r"\bverifier\b", r"\bbuilder\b",
        r"\bround\b", r"\bprevious(ly)?\b", r"\brevised\b", r"\bcorrected\b", r"\bfixed in\b", r"\bnow\b", r"\bwas added\b",
        r"\bchanged\b", r"\bthe earlier\b", r"\bwe changed\b", r"\bround-?\d", r"\bdraft\b", r"\bplaceholder\b",
        r"\bdeferred\b", r"\bfor now\b", r"\bsimply\b", r"\bjust\b", r"\bindeed\b", r"\bnote that\b", r"\bstill\b", r"\bnew\b"]
def visible(s):
    s = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))
files = [(f"L{n:02d}", root / f"course/modules/M/M2/L{n:02d}.html") for n in range(1, 25)] + [("project", root / "course/modules/M/M2/project.html")]
hits = []
for name, p in files:
    t = visible(p.read_text(encoding="utf-8"))
    for pat in pats:
        for m in re.finditer(pat, t, re.I):
            hits.append((name, pat, t[max(0, m.start() - 60):m.end() + 60]))
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
for c in cards:
    txt = c["front"] + " " + c["back"]
    for pat in pats:
        for m in re.finditer(pat, txt, re.I):
            hits.append((c["id"], pat, txt[max(0, m.start() - 60):m.end() + 60]))
for h in hits:
    print(h)
print("total hits", len(hits))
