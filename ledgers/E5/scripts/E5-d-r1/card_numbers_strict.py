"""For each E5 card, each numeric token in front/back must occur in the card's own lesson text (tags stripped,
entities unescaped). Tokens found only in lab output are listed separately. Usage: card_numbers_strict.py <checkout>"""
import html, json, re, subprocess, sys, os
root = sys.argv[1]
os.chdir(root)
cards = json.load(open("course/modules/E/E5/cards.json", encoding="utf-8"))
def plain(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))
lesson = {}
for n in range(1, 9):
    lesson[f"L0{n}"] = plain(f"course/modules/E/E5/L0{n}.html")
lesson["project"] = plain("course/modules/E/E5/project.html")
outs = {}
for tw in sorted(os.listdir("tests/labs/E5")):
    if tw.endswith(".py") and "project" not in tw:
        r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", os.path.join(root, "tests/labs/E5", tw)], capture_output=True, text=True, cwd="/tmp")
        outs[tw] = r.stdout
allout = "\n".join(outs.values())
tok = re.compile(r"(?<![A-Za-z_\\\\])\d+(?:[./,]\d+)*")
not_in_lesson = []
in_out_only = []
for c in cards:
    text = c["front"] + " " + c["back"]
    for m in tok.findall(text):
        m2 = m.replace(",", "")
        if m2 in ("1",):
            pass
        if m2 in lesson[c["lesson"]] or m in lesson[c["lesson"]] or m2 in lesson[c["lesson"]].replace(",", ""):
            continue
        if m in allout or m2 in allout:
            in_out_only.append((c["id"], m))
        else:
            not_in_lesson.append((c["id"], m))
print("cards", len(cards))
print("tokens not in own lesson, not in any twin output:", not_in_lesson)
print("tokens in own-lesson-absent but in twin output:", len(in_out_only))
for x in in_out_only:
    print("  ", x)
