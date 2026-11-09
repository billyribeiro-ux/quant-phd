#!/bin/sh
# Lab-level sensitivity: does the L04 twin's own check (Prop 2.2 / 2.3 counters) detect a broken book?
ROOT="$1"; SCR="$2"; mkdir -p "$SCR"; TWIN="$ROOT/tests/labs/FC1/lab-FC1-L04-1.py"
mut() { name="$1"; expr="$2"; python3 - "$TWIN" "$SCR/$name.py" "$expr" <<'PY'
import sys
src = open(sys.argv[1], encoding="utf-8").read()
old, new = sys.argv[3].split("|||")
assert src.count(old) == 1, ("anchor count", src.count(old), old)
open(sys.argv[2], "w", encoding="utf-8").write(src.replace(old, new))
PY
"$ROOT/.venv/bin/python" -I -W error "$SCR/$name.py" > "$SCR/$name.out" 2>&1; echo "== $name rc=$?"; grep -E "crossed|submitted !=" "$SCR/$name.out"; }
mut m_rest_limit_without_cross_check 'if order.kind == "limit" and order.price is not None:|||if False:'
mut m_traded_once 'self.traded += fill|||self.traded += fill // 2 if fill > 1 else fill'
