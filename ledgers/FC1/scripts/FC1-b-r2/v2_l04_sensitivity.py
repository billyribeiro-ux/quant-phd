# Round-2 sensitivity: the lab's counters must be live. Scratch copies of the L04 twin with (a) the traded term
# halved and (b) one resting bid withdrawn at event 100 (A2 violated); the conservation counter must become nonzero.
import subprocess, sys, tempfile, shutil
from pathlib import Path
src = (Path(sys.argv[1]) / "tests/labs/FC1/lab-FC1-L04-1.py").read_text(encoding="utf-8")
def run(text, label):
    d = Path(tempfile.mkdtemp(prefix="v2l04_"))
    f = d / "lab.py"; f.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=str(d))
    shutil.rmtree(d)
    lines = [l for l in r.stdout.splitlines() if l.startswith("events")]
    print(label, "| rc", r.returncode, "|", " ; ".join(lines), "|", r.stderr[-200:])
run(src, "baseline")
a = src.replace("            self.traded += fill\n", "            self.traded += fill // 2\n", 1)
assert a != src
run(a, "traded term halved")
b = src.replace("        stops_activated += book.activate()\n",
                "        stops_activated += book.activate()\n        if seq == 100 and book.bids:\n            book.bids.pop()\n", 1)
assert b != src
run(b, "one resting bid withdrawn at event 100 (A2 violated)")
