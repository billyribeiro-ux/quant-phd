"""Mechanical checks for M2 slice c (L13-L18) at pin edbb7aa8 versus previous pin 8196077d.

Reads the two cards.json snapshots and the six lesson pages from the checkout (HEAD) and from git
(previous pin). Prints: grade-bearing items (claim titles, grades, key-results rows, concept links,
block counts, misconception counts, quiz item counts, data-hours) per page and whether each is identical.
Run from the checkout root with the repo venv: .venv/bin/python -I <path>.
"""
import json
import re
import subprocess
import sys

ROOT = sys.argv[1]
OLD = "8196077d5f56c3919d33e69888176d197d378ad4"
NEW = "edbb7aa8"
PAGES = ["L13", "L14", "L15", "L16", "L17", "L18"]


def git_show(rev: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True
    ).stdout


def items(html: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    out["claim_titles"] = re.findall(r'<span class="block-title claim"[^>]*>.*?</span>', html)
    out["grades"] = re.findall(r'<span class="grade" data-grade="[^"]*">[^<]*</span>', html)
    out["concept_links"] = sorted(set(re.findall(r'data-concept="([^"]+)"', html)))
    out["dfn"] = re.findall(r'<dfn id="[^"]*"', html)
    out["blocks"] = re.findall(r'<div class="block (definition|theorem|proposition|corollary|example|remark|proof)"', html)
    out["misconceptions"] = re.findall(r'<li class="misconception">', html)
    out["quiz_items"] = re.findall(r'<li class="item"', html)
    out["problems"] = re.findall(r'<div class="problem" id="[^"]*"', html)
    out["data_attrs"] = re.findall(r'data-hours="[^"]*"|data-files="[^"]*"|data-chart="[^"]*"', html)
    out["data_correct_count"] = [str(len(re.findall(r"data-correct", html)))]
    out["why_it_matters_words"] = [str(len(re.sub(r"<[^>]+>", " ", m).split())) for m in re.findall(r'<p class="why-it-matters">(.*?)</p>', html, re.S)]
    return out


for p in PAGES:
    path = f"course/modules/M/M2/{p}.html"
    new = items(open(f"{ROOT}/{path}", encoding="utf-8").read())
    old = items(git_show(OLD, path))
    for k in new:
        same = old[k] == new[k]
        print(f"{p} {k}: {'IDENTICAL' if same else 'CHANGED'} (count new={len(new[k])}, old={len(old[k])})")
        if not same and k in ("claim_titles", "grades", "concept_links", "dfn", "blocks", "misconceptions", "quiz_items", "problems", "data_attrs", "why_it_matters_words", "data_correct_count"):
            so, sn = set(old[k]), set(new[k])
            print("   only_old:", sorted(so - sn)[:10])
            print("   only_new:", sorted(sn - so)[:10])
            if len(new[k]) == len(old[k]) and k in ("data_correct_count", "why_it_matters_words"):
                print("   old:", old[k], "new:", new[k])

oc = json.loads(git_show(OLD, "course/modules/M/M2/cards.json"))
nc = json.loads(open(f"{ROOT}/course/modules/M/M2/cards.json", encoding="utf-8").read())
oi = {c["id"]: c for c in oc}
ni = {c["id"]: c for c in nc}
changed = sorted(i for i in ni if i in oi and oi[i] != ni[i])
print("cards removed:", sorted(i for i in oi if i not in ni))
print("cards added:", sorted(i for i in ni if i not in oi))
print("cards changed:", changed)
print("changed cards in slice lessons:", [i for i in changed if ni[i]["lesson"] in PAGES])
print("slice card count:", sum(1 for c in nc if c["lesson"] in PAGES))
print("unit card count:", len(nc), "duplicate ids:", len(nc) - len({c["id"] for c in nc}))
fronts = [c["front"].strip().lower() for c in nc]
print("duplicate fronts:", len(fronts) - len(set(fronts)))
