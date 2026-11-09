"""For each card, every numeric token in its back must appear in its lesson HTML, or in the output of a lab twin of E5."""
import glob, html, json, os, re, subprocess, sys
root = sys.argv[1]
os.chdir(root)
cards = json.load(open("course/modules/E/E5/cards.json", encoding="utf-8"))
lesson_text = {}
for f in sorted(glob.glob("course/modules/E/E5/L0*.html")):
    lesson_text[os.path.basename(f)[:3]] = html.unescape(re.sub(r"<[^>]+>", " ", open(f, encoding="utf-8").read()))
outs = {}
for tw in sorted(glob.glob("tests/labs/E5/*.py")):
    if "project" in tw:
        continue
    env = {"PYTHONHASHSEED": "0"}
    r = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", os.path.join(root, tw)], capture_output=True, text=True, cwd="/tmp")
    outs[os.path.basename(tw)] = r.stdout
    print("twin", os.path.basename(tw), "exit", r.returncode, file=sys.stderr)
allout = "\n".join(outs.values())
bad = 0
for c in cards:
    nums = re.findall(r"(?<![A-Za-z(])-?\d+(?:\.\d+)?", c["back"])
    for n in nums:
        m = n.lstrip("-")
        if m in ("1", "0", "2", "3", "4", "5", "10", "12", "6", "100", "40", "20", "24"):
            pass
        in_lesson = m in lesson_text.get(c["lesson"], "") or any(m in t for t in lesson_text.values())
        in_out = m in allout
        if not (in_lesson or in_out):
            bad += 1
            print("NOT FOUND", c["id"], repr(n), "|", c["back"][:120])
print("checked", len(cards), "cards; unmatched numeric tokens:", bad)
