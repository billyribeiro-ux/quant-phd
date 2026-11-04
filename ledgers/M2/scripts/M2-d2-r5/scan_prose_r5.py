# Prose scans for the M2 L22-L24 slice. Reads the pages and cards from the checkout; prints counts and contexts.
import html, re, subprocess
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD5-M2-d2"
PAGES = ("L22", "L23", "L24")

def visible(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<pre.*?</pre>", " ", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))

BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "as we saw", "in summary", "delve", "placeholder"]
PROCESS = [r"\bround\s+\d", r"\bbuilder\b", r"\bverifier\b", r"\bfixed in\b", r"\bcorrected\b", r"\brevision\b",
           r"\berratum\b", r"\bprevious draft\b"]
print("== banned phrases (visible prose, <pre> excluded)")
for p in PAGES:
    t = visible(f"{ROOT}/course/modules/M/M2/{p}.html").lower()
    print(p, {b: t.count(b.lower()) for b in BANNED if t.count(b.lower())})
print("== process words")
for p in PAGES:
    t = visible(f"{ROOT}/course/modules/M/M2/{p}.html")
    print(p, {r: len(re.findall(r, t, re.I)) for r in PROCESS if re.search(r, t, re.I)})
print("== dfn elements")
for p in PAGES:
    s = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    print(p, re.findall(r"<dfn[^>]*>", s))
print("== external references (src/href/url)")
for p in PAGES:
    s = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    print(p, sorted(set(re.findall(r'(?:src|href)="(https?:[^"]*)"', s))), len(re.findall(r"https?://", s)))
print("== single-letter symbols in math (macros removed)")
for p in PAGES:
    s = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S)
    letters = {}
    for a, b in maths:
        t = re.sub(r"\\[A-Za-z]+", "", a or b)
        for ch in re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", t):
            letters[ch] = letters.get(ch, 0) + 1
    print(p, sorted(letters))
print("== registered macros used on the pages")
for p in PAGES:
    s = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    print(p, sorted(set(re.findall(r"\\R(?![A-Za-z])", s))))
print("== 'prerequisite calculus' attributions (pages and cards)")
print(subprocess.run(["grep", "-n", "prerequisite calculus", f"{ROOT}/course/modules/M/M2/L22.html",
                      f"{ROOT}/course/modules/M/M2/L24.html", f"{ROOT}/course/modules/M/M2/cards.json"],
                     capture_output=True, text=True).stdout.replace(ROOT + "/", ""))
print("== what the curriculum and M1 say (derivative content in M1 lessons; M1 and P0.1 titles)")
for f in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    s = open(f"{ROOT}/course/modules/M/M1/{f}.html", encoding="utf-8").read()
    print("M1", f, "derivative/differentiat mentions:", len(re.findall(r"derivativ|differentiat", s, re.I)))
print(subprocess.run(["grep", "-n", "title:", f"{ROOT}/curriculum/01-foundations.yaml"], capture_output=True,
                     text=True).stdout.splitlines()[:6])
