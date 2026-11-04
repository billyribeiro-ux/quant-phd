"""Compare the page's draw_game(seed) (Lab 1 code) with grader instance.make_instance(seed) for seeds 0..49."""
import importlib.util
import sys

sys.path.insert(0, "/tmp/pc3c-r3-ws")
import instance  # noqa: E402

src = open("/tmp/pc3c-r3-lab-PC3-project-1-page.py", encoding="utf-8").read()
ns: dict = {}
exec(compile(src.replace("\nmain()", "\n"), "lab1", "exec"), ns)
bad = []
names = {"uninformed-buy": "uninformed-buy", "uninformed-sell": "uninformed-sell", "informed": "informed"}
for seed in range(0, 50):
    p, a = ns["draw_game"](seed)
    inst = instance.make_instance(seed)
    if p != inst["fair_path_cents"] or a != inst["arrivals"]:
        bad.append(seed)
print("seeds 0..49 page draw_game == make_instance:", 50 - len(bad), "of 50 equal; mismatches", bad)
print("seed-0 settlement", inst["settlement_cents"] if False else instance.make_instance(0)["settlement_cents"])
