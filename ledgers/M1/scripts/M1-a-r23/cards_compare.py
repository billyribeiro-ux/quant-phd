"""Compare L01-L03 cards between the previous pin 7143726 and the checkout (run with -I)."""
import json
import subprocess

old = subprocess.run(["git", "-C", "/tmp/verify23-M1-a", "show", "7143726:course/modules/M/M1/cards.json"],
                     capture_output=True, check=True, text=True).stdout
a = json.loads(old)
b = json.load(open("/tmp/verify23-M1-a/course/modules/M/M1/cards.json", encoding="utf-8"))
ca = [c for c in a if c["lesson"] in ("L01", "L02", "L03")]
cb = [c for c in b if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards old/new", len(ca), len(cb), "equal", ca == cb)
print("total", len(b), "unique", len({c["id"] for c in b}))
