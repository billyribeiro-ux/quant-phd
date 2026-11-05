"""Round 11: scan the rendered E4 lessons, the project page and the cards for phrases banned by BUILDER_RULES section 1
(placeholders, filler, process words). Prints every hit with its file and line. Run from the checkout root with -I."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BANNED = re.compile(
    r"TODO|TBD|lorem|left as an exercise|it is important to note|studies show|experts agree|it is well known|"
    r"obviously|clearly|it can be shown|of course|let us|let's|in today's|rapidly evolving|round \d|verifier|builder",
    re.I,
)
hits = 0
pages = ["index", "project"] + [f"L0{i}" for i in range(1, 10)]
for p in pages:
    html = f"course/modules/E/E4/{p}.html"
    txt = subprocess.run([sys.executable, "-I", os.path.join(HERE, "html_to_text.py"), html],
                         capture_output=True, text=True, check=True).stdout
    for n, line in enumerate(txt.splitlines(), 1):
        for m in BANNED.finditer(line):
            hits += 1
            print(f"{html}:{n}: {m.group(0)!r}")
cards = json.load(open("course/modules/E/E4/cards.json", encoding="utf-8"))
for c in cards:
    for f in ("front", "back", "basis"):
        for m in BANNED.finditer(c.get(f) or ""):
            hits += 1
            print(f"cards.json {c['id']} {f}: {m.group(0)!r}")
print(f"banned-phrase hits: {hits}")
