"""Round-5: (a) 20 sampled seeds: every instance valid (21 positive ints, 20 arrivals from the three names, +-5 moves),
and materially different (distinct fair paths, distinct arrival strings, distinct settlements); (b) the starter file
raises NotImplementedError under the suite (suite must fail on it, checked in a scratch copy by the caller).
Usage: python3 -I <this> <grader_dir>."""
import random
import sys

grader = sys.argv[1]
sys.path.insert(0, grader)
import instance  # noqa: E402

seeds = sorted(random.Random(20260311).sample(range(0, 100000), 20))
rows = []
for s in seeds:
    i = instance.make_instance(s)
    p, a = i["fair_path_cents"], i["arrivals"]
    valid = (len(p) == 21 and p[0] == 10000 and all(type(v) is int and v > 0 for v in p)
             and all(abs(p[k + 1] - p[k]) == 5 for k in range(20)) and len(a) == 20
             and set(a) <= {"uninformed-buy", "uninformed-sell", "informed"} and i["settlement_cents"] == p[20])
    rows.append((s, valid, p[20], sum(x == "informed" for x in a), sum(x == "uninformed-buy" for x in a),
                 sum(x == "uninformed-sell" for x in a)))
for r in rows:
    print("seed %6d valid=%s settlement=%d informed=%d buy=%d sell=%d" % r)
print("all valid:", all(r[1] for r in rows))
print("distinct paths:", len({tuple(instance.make_instance(r[0])["fair_path_cents"]) for r in rows}), "of", len(rows))
print("distinct settlements:", len({r[2] for r in rows}), "of", len(rows))
print("distinct arrival strings:", len({tuple(instance.make_instance(r[0])["arrivals"]) for r in rows}), "of", len(rows))
