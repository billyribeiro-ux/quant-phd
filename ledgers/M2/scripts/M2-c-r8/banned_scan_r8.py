import html, json, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
pats = [r"\bTODO\b", r"\bTBD\b", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
        r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
        r"it is well known", r"\bobviously\b", r"\bclearly\b", r"\broughly\b", r"\bhistorically\b", r"\bapprox", r"\bverifier\b",
        r"\bbuilder\b", r"\bround\b", r"\bprevious(ly)?\b", r"\brevised\b", r"\bcorrected\b", r"\bfixed in\b", r"\bnow\b",
        r"\bwas added\b", r"\bchanged\b", r"\bthe earlier\b", r"\bwe changed\b", r"\bround-?\d", r"\bdraft\b", r"\bplaceholder\b",
        r"\bdeferred\b", r"\bfor now\b", r"\bsimply\b", r"\bjust\b", r"\bindeed\b", r"\bnote that\b"]
def visible(s):
    s = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)
hits = []
for n in range(13, 19):
    t = visible((root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8"))
    t = re.sub(r"\s+", " ", t)
    for p in pats:
        for m in re.finditer(p, t, re.I):
            hits.append((f"L{n}", p, t[max(0, m.start()-60):m.end()+60]))
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
for c in cards:
    if c["lesson"] in {f"L{n}" for n in range(13, 19)}:
        txt = c["front"] + " " + c["back"]
        for p in pats:
            for m in re.finditer(p, txt, re.I):
                hits.append((c["id"], p, txt[max(0, m.start()-60):m.end()+60]))
for h in hits:
    print(h)
print("total hits", len(hits))
