"""E4-c round 6: build ledgers/E4/E4-c.json from the round-5 fragment.

Usage: python -I build_fragment.py <checkout-root> <round5-fragment.json>

- Rows whose cited lines did not change between pins 7376a5e2 and 4bd8cb94 are carried. Their evidence is the innermost
  round-5 evidence with one round-6 prefix, and their locators are re-mapped with out/linemap.json.
- OVERRIDES holds rows re-verified in round 6 (their cited lines changed, or the round-5 evidence was wrong or stale).
- NEW holds rows added for round-6 findings. Every round-5 row id is kept.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

root, frag_path = sys.argv[1], sys.argv[2]
lm = json.load(open(os.path.join(root, "ledgers/E4/scripts/E4-c-r6/out/linemap.json")))
r5 = json.load(open(frag_path))
PIN = "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07"
BASE = "7376a5e216c1e6d99becc76b4cd64028f5b55d3f"
KEYS = {
    "lab-E4-L07-1.py": "tests/labs/E4/lab-E4-L07-1.py",
    "lab-E4-L08-1.py": "tests/labs/E4/lab-E4-L08-1.py",
    "lab-E4-L09-1.py": "tests/labs/E4/lab-E4-L09-1.py",
}
TOK = re.compile(r"(L0[6-9]\.html|lab-E4-L0[6-9]-1\.py|cards\.json|index\.html):((?:\d+(?:-\d+)?)(?:, ?\d+(?:-\d+)?)*)")


def fkey(f):
    return KEYS.get(f, "course/modules/E/E4/" + f)


def remap(text):
    def sub_list(m):
        f = m.group(1)
        mp = {int(k): v for k, v in lm[fkey(f)]["map"].items()}

        def num(n):
            a, _, b = n.partition("-")
            out = str(mp[int(a)])
            if b:
                out += "-" + str(mp[int(b)])
            return out

        parts = re.split(r"(, ?)", m.group(2))
        body = "".join(p if re.fullmatch(r", ?", p) else num(p) for p in parts)
        return f + ":" + body

    return TOK.sub(sub_list, text)


def innermost(s):
    while s.startswith("Carried from round "):
        i = s.index("(")
        depth = 0
        j = i
        for j in range(i, len(s)):
            if s[j] == "(":
                depth += 1
            elif s[j] == ")":
                depth -= 1
                if depth == 0:
                    break
        assert s[j + 1:j + 3] == ": ", s[:80]
        s = s[j + 3:]
    return s


def carry(row):
    prefix = ("Carried from round 5 (cited subject byte-identical between pins 7376a5e2 and 4bd8cb94; "
              "locators re-mapped with out/linemap.json): ")
    return {
        "id": row["id"],
        "check": row["check"],
        "location": remap(row["location"]).replace("this round", "in round 5"),
        "status": "PASS",
        "evidence": prefix + remap(innermost(row["evidence"])).replace("this round", "in round 5"),
    }


def fresh(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


OVERRIDES = {}
NEW = []
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rows_r6.py"), encoding="utf-8").read())

flagged = {l.split()[0] for l in open(os.path.join(root, "ledgers/E4/scripts/E4-c-r6/out/classify.out"))
           if " FLAG " in l}
rows = []
seen = set()
for row in r5["rows"]:
    rid = row["id"]
    if rid in OVERRIDES:
        rows.append(OVERRIDES[rid])
    elif rid in flagged:
        raise SystemExit(f"flagged row without an override: {rid}")
    else:
        rows.append(carry(row))
    seen.add(rid)
missing = [k for k in OVERRIDES if k not in seen]
if missing:
    raise SystemExit(f"overrides for unknown ids: {missing}")
rows.extend(NEW)

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
notes = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes_r6.txt"), encoding="utf-8").read().strip()
frag = {
    "unit": "E4",
    "slice": "c",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 6 (did not build E4)",
    "pin": PIN,
    "base": BASE,
    "checkout": root,
    "scratch": "/tmp (twin runs from an empty directory, env -i; removed after each run)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": r5["registry_flags"],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"Slice E4-c (L07, L08, L09, their lab twins and their cards). {len(rows)} rows: "
                f"{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE."),
}
out = os.path.join(root, "ledgers/E4/E4-c.json")
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, verdict, counts, len(rows))
