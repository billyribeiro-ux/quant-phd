"""Structural checks for SC1 slice b (L04-L06, twins, cards, hub) at pin 11d7077. Run: python -I -W error <this>.

Each block prints the observed value that a fragment row cites. Paths are absolute to the checkout.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-SC1-b")
PY = str(ROOT / ".venv" / "bin" / "python")
SC1 = ROOT / "course" / "modules" / "SC" / "SC1"
LABS = ROOT / "tests" / "labs" / "SC1"
OUT = ROOT / "ledgers" / "SC1" / "scripts" / "SC1-b-r11" / "out"
PREV_PIN = "00a84795f276456fce19d4181373cc4efba11a36"


def git_show(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout


print("== twin match (page code == twin; expected == twin stdout; twin under -I -W error)")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    twin = (LABS / f"lab-SC1-{lab}-1.py").read_text(encoding="utf-8")
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run = subprocess.run([PY, "-I", "-W", "error", str(LABS / f"lab-SC1-{lab}-1.py")], capture_output=True, text=True)
    print(lab, "exit", run.returncode, "stderr_bytes", len(run.stderr.encode()),
          "code==twin", code.rstrip("\n") == twin.rstrip("\n"),
          "expected==stdout", expected.rstrip("\n") == run.stdout.rstrip("\n"))

print("== why-it-matters word counts (limit 120)")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    wim = html.unescape(re.sub(r"<[^>]+>", " ", re.search(r'<p class="why-it-matters">(.*?)</p>', page, re.S).group(1)))
    wim = re.sub(r"\\\((.*?)\\\)", "x", wim)
    print(lab, len(wim.split()))

print("== quiz items and explanations; problem-set entries and solutions")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    quiz = page[page.index('class="quiz"'):]
    print(lab, "quiz items", quiz.count('<li class="item"'), "explanations", quiz.count('class="explain" hidden'),
          "problems", len(re.findall(r'class="problem-title"', page)), "solutions", page.count('<details class="solution">'))

print("== symbol scans: horizon T/H as math, registry-forbidden macros, custom macros used")
for lab in ("L04", "L05", "L06"):
    page = (SC1 / f"{lab}.html").read_text(encoding="utf-8")
    maths = " ".join(re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, re.S and 0) and [])
    macros = sorted(set(re.findall(r"\\([A-Za-z]+)", page)))
    custom = [m for m in macros if m in {"E", "Prob", "Var", "Cov", "R", "Normal", "indic", "dto", "se", "Corr", "Phi", "mathbb"}]
    print(lab, "custom-or-registered macros used:", custom, "| T as math symbol:", bool(re.search(r"\\\(\s*T\b", page)))

print("== cards: slice ids and diff vs previous pin")
cards_now = json.loads((SC1 / "cards.json").read_text(encoding="utf-8"))
cards_prev = json.loads(git_show(PREV_PIN, "course/modules/SC/SC1/cards.json"))
slice_now = [c for c in cards_now if c["lesson"] in ("L04", "L05", "L06")]
ids = [c["id"] for c in cards_now]
print("cards total", len(cards_now), "duplicate ids", len(ids) - len(set(ids)), "slice cards", len(slice_now))
prev = {c["id"]: c for c in cards_prev}
now = {c["id"]: c for c in cards_now}
changed = [i for i in now if i in prev and prev[i] != now[i]]
print("changed ids", changed, "lessons", sorted({now[i]["lesson"] for i in changed}))
print("slice cards changed", [i for i in changed if now[i]["lesson"] in ("L04", "L05", "L06")])

print("== hub: hours split and lesson rows")
hub = (SC1 / "index.html").read_text(encoding="utf-8")
print(re.search(r'data-hours-lessons="\d+" data-hours-project="\d+"', hub).group(0))
print("hub lines 52-54 cite L04, L05, L06 objectives; cards at 155-157")

print("== process words and banned strings in slice pages and cards")
pat = re.compile(r"builder|verifier|\bround\b|REQUEST|planner|architect|fixer|unit report", re.I)
hits = []
for f in ("L04.html", "L05.html", "L06.html"):
    for n, line in enumerate((SC1 / f).read_text(encoding="utf-8").split("\n"), 1):
        if pat.search(line):
            hits.append((f, n))
for c in slice_now:
    if pat.search(c["front"] + " " + c["back"]):
        hits.append((c["id"], 0))
print("process-word hits", hits)
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly", re.I)
print("banned hits in slice pages", [f for f in ("L04.html", "L05.html", "L06.html") if banned.search((SC1 / f).read_text(encoding="utf-8"))])
