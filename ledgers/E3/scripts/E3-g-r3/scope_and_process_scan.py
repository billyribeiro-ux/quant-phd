"""Scan the 85 L05-L08 cards for scope words and process words; list card words absent from the own lesson dump.

Run: python -I ledgers/E3/scripts/E3-g-r3/scope_and_process_scan.py
"""
import json
import re

TXT = "ledgers/E3/scripts/E3-g-r3/text"
LESSONS = ("L05", "L06", "L07", "L08")
lessons = {L: open(f"{TXT}/{L}.txt", encoding="utf-8").read().lower() for L in LESSONS}
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in LESSONS]
scope = re.compile(r"\b(every|all|any|only|never|always|exactly|same|each|general|in general|most|people|none)\b", re.I)
proc = re.compile(r"\b(TODO|TBD|lorem|builder|verifier|round|REQUEST|checked directly|verified|fixed|defect)\b", re.I)
print("SCOPE/PROCESS HITS")
for c in sl:
    t = c["front"] + " || " + c["back"]
    hits = sorted({m.group(0).lower() for m in scope.finditer(t)})
    ph = sorted({m.group(0) for m in proc.finditer(t)})
    if hits or ph:
        print(c["id"], c["lesson"], "SCOPE:", hits, "PROC:", ph)
print("WORDS ABSENT FROM OWN LESSON (length >= 6)")
for c in sl:
    lt = lessons[c["lesson"]]
    words = set(re.findall(r"[a-z][a-z\-]{5,}", (c["front"] + " " + c["back"]).lower()))
    miss = sorted(w for w in words if w not in lt)
    if miss:
        print(c["id"], c["lesson"], miss)
