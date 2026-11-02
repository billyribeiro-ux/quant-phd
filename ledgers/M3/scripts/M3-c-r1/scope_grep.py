# Lists banned phrases (BUILDER_RULES 1.3-1.4, 1.1-12 process words) and scope words with context, per page text.
import re, sys
root = sys.argv[1]
banned = r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|it can be shown|builder|verifier|ledger|\bround [0-9]|\bpin\b|agent|historically|roughly|\babout [0-9]|typically|almost always|generic|in practice|stable|robust|\bonly\b|exactly|\bevery\b|\ball\b|\balways\b|\bany\b|\bsame\b|\bdrives\b|\.\.\."
for L in ["L07", "L08", "L09"]:
    txt = open(f"{root}/{L}.txt" if False else f"{root}/ledgers/M3/scripts/M3-c-r1/{L}.txt", encoding="utf-8").read()
    print("==", L)
    for m in re.finditer(banned, txt, re.I):
        s = max(0, m.start() - 70); e = min(len(txt), m.end() + 50)
        print(f"  [{m.group(0)}] ...{txt[s:e]!r}")
