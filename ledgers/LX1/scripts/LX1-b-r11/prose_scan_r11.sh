#!/bin/sh
# LX1-b round 11: banned-phrase (BUILDER_RULES 1.3-1.4), process-word and ellipsis scan of L03 and L04 (fixed strings).
# Usage: sh ledgers/LX1/scripts/LX1-b-r11/prose_scan_r11.sh <checkout>
cd "$1" || exit 1
for f in course/modules/LX/LX1/L03.html course/modules/LX/LX1/L04.html; do
  echo "== $f"
  for p in TODO TBD lorem "for brevity" "details omitted" "beyond the scope" "left as an exercise" "you can add more" \
           "important to note" "studies show" "experts agree" "well known" obviously clearly "can be shown" roughly \
           historically "in conclusion" "let us" "we will" "you will" "by the end" "as we have seen" "it is worth" \
           builder verifier architect fixer planner campaign checkout ledger "build plan" "open item" \
           DATA_REQUEST REFERENCE_REQUEST "reference request" "data request"; do
    n=$(grep -c -i -F -- "$p" "$f"); [ "$n" != "0" ] && echo "HIT [$p] x$n"
  done
  echo "ellipsis lines (sequence notation only, checked by hand):"; grep -n -F -- "..." "$f" | cut -c1-120
done
echo "== notation: macros used in math vs notation/notation.json registered symbols"
python3 -I - "$PWD" <<'PY'
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered = {s["symbol"] for s in reg["symbols"]} | set(reg["macros"].keys())
print("registered macros/symbols:", len(registered))
for lesson in ("L03", "L04"):
    t = (root / f"course/modules/LX/LX1/{lesson}.html").read_text(encoding="utf-8")
    maths = [a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)]
    cmds = sorted({c for m in maths for c in re.findall(r"\\([A-Za-z]+)", m)})
    hits = [r for r in registered if any(("\\" + r.lstrip("\\")) in m for m in maths) and r.startswith("\\")]
    print(lesson, "math segments:", len(maths), "commands:", cmds)
    print(lesson, "registered macros used:", hits)
PY
