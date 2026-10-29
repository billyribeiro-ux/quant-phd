"""Scan the added lines of the M2 slice-d delta (ce7b382..b6865c7) for scope words and banned phrases."""
import re
import subprocess
import sys

repo = sys.argv[1]
out = subprocess.run(
    ["git", "-C", repo, "diff", "-U0", "ce7b382", "b6865c7", "--", "course/modules/M/M2/L19.html",
     "course/modules/M/M2/L20.html", "course/modules/M/M2/L24.html", "course/modules/M/M2/cards.json"],
    capture_output=True, text=True, check=True).stdout
scope = re.compile(r"\b(only|all|always|every|any|same|drives|exactly|none|never|must|proves?|shows?)\b", re.I)
banned = re.compile(r"TODO|TBD|lorem|for brevity|beyond the scope|details omitted|obviously|clearly|it is important to note|well known|left as an exercise", re.I)
file = None
for line in out.splitlines():
    if line.startswith("+++ "):
        file = line[6:]
    elif line.startswith("+") and not line.startswith("+++"):
        text = line[1:]
        hits = sorted({m.group(0).lower() for m in scope.finditer(text)})
        bad = sorted({m.group(0) for m in banned.finditer(text)})
        print(f"{file}: scope={hits} banned={bad} :: {text[:160]}")
