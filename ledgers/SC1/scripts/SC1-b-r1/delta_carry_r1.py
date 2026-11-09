"""Closing-delta carry check for SC1 slice b (95f3f8cb..2a805c83).

Reads the base fragment, parses each row's cited file:line ranges and card ids,
and reports which rows cite a line or card changed in the delta.
"""
import json
import re
import subprocess
import sys

PIN_OLD = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
PIN_NEW = "2a805c831410ab77c38c227f7e121e8537193ce9"
BASE = "/Users/billyribeiro/.fanout/frags/F3-SC1-b.round1.json"
SC1 = "course/modules/SC/SC1/"
FILES = {
    "L01": SC1 + "L01.html", "L02": SC1 + "L02.html", "L03": SC1 + "L03.html",
    "L04": SC1 + "L04.html", "L05": SC1 + "L05.html", "L06": SC1 + "L06.html",
    "L07": SC1 + "L07.html", "L08": SC1 + "L08.html", "index": SC1 + "index.html",
    "project": SC1 + "project.html",
}


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def hunks(path):
    out = git("diff", "-U0", f"{PIN_OLD}..{PIN_NEW}", "--", path)
    changed = set()
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start = int(m.group(3))
        count = int(m.group(4)) if m.group(4) is not None else 1
        changed.update(range(start, start + max(count, 1)))
        # deletions also mark the old-side line; record new-side positions
    return changed


def card_objs(rev):
    raw = git("show", f"{rev}:{SC1}cards.json")
    return {c["id"]: json.dumps(c, sort_keys=True, ensure_ascii=False) for c in json.loads(raw)}


def main():
    base = json.load(open(BASE))
    changed_lines = {k: hunks(v) for k, v in FILES.items()}
    old_cards, new_cards = card_objs(PIN_OLD), card_objs(PIN_NEW)
    changed_cards = sorted(i for i in set(old_cards) | set(new_cards) if old_cards.get(i) != new_cards.get(i))
    print("changed new-side lines per file:")
    for k, v in changed_lines.items():
        if v:
            print(" ", k, sorted(v))
    print("changed card ids:", changed_cards)
    print("card ids in base:", len(old_cards), "new:", len(new_cards))
    for r in base["rows"]:
        loc = r["location"] + " " + r["evidence"]
        hits = []
        for m in re.finditer(r"\b(L0[1-8]|index|project)\.html:(\d+)(?:-(\d+))?", loc):
            key, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            lines = set(range(a, b + 1))
            if lines & changed_lines.get(key, set()):
                hits.append(f"{key}:{a}-{b}")
        for cid in re.findall(r"SC1-c(\d{3})", loc):
            if f"SC1-c{cid}" in changed_cards:
                hits.append(f"card SC1-c{cid}")
        whole = [k for k in FILES if changed_lines.get(k) and re.search(rf"\b{k}\.html\b(?![:\d])", loc)]
        if "cards.json" in loc and changed_cards:
            whole.append("cards.json")
        if hits or whole:
            print(r["id"], r["status"], "HITS:", hits, "WHOLE-FILE-CITE:", whole)


if __name__ == "__main__":
    main()
