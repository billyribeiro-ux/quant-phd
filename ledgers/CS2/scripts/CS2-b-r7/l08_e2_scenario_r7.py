"""E2 counterexample: a level that empties by cancellation after an earlier fill passed one of its dead entries.

Usage: python -I this.py <path-to-twin>. Loads the twin without its final main() call.
"""
import sys
import pathlib
import types

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").rstrip()
src = src[: -len("main()")]
mod = types.ModuleType("twin_noMain")
sys.modules["twin_noMain"] = mod
exec(compile(src, "twin", "exec"), mod.__dict__)
Book = mod.__dict__["Book"]
b = Book()
b.submit("S", 10000, 1, 1)   # oid 1 rests, qty 1
b.submit("S", 10000, 1, 2)   # oid 2 rests, qty 1
b.submit("S", 10000, 5, 3)   # oid 3 rests, qty 5
b.submit("B", 10000, 1, 4)   # fills oid 1 (dead at head, not yet passed)
print("after fill of oid 1: queue_steps", b.counts.queue_steps, "head", b.levels["S"][10000].head)
b.submit("B", 10000, 1, 5)   # head passes oid 1 (queue step), fills oid 2
print("after fill of oid 2: queue_steps", b.counts.queue_steps, "head", b.levels["S"][10000].head)
b.cancel(3)                  # level 10000 empties by cancellation and is deleted with its queue
print("after cancel of oid 3: level present", 10000 in b.levels["S"], "queue_steps", b.counts.queue_steps)
print("queue of deleted level is gone; oid 1 was passed by a queue step before the deletion")
