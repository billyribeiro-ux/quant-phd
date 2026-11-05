"""Round-10 E3-d: a set whose only mixed lotteries are A lotteries (every B lottery is a sure amount, so pure).
project.html:237 refuses a set only when no response has a lottery that mixes a gain and a loss, and project.html:223 says a pair
identifies lambda when one of its two lotteries mixes. Reference vs the B-only mutant d10_01."""
import importlib.util, sys
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as ref
spec = importlib.util.spec_from_file_location("mut", "/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/ledgers/E3/mutants/d10_01_identification_reads_only_the_b_lotteries.py")
mut = importlib.util.module_from_spec(spec); spec.loader.exec_module(mut)
SURE_B = [700, 1900, 0, 2600, -300, 1500, 900, 2100, -600, 1100, 400, 1800]
CHOICES = ["A", "B", "B", "A", "B", "A", "A", "B", "A", "A", "B", "B"]
A_MIXED = [([2000, -1500], ["1/2", "1/2"]), ([3000, -2500], ["2/5", "3/5"]), ([1500, -1000], ["3/4", "1/4"]),
           ([4000, -3000], ["1/3", "2/3"]), ([2500, -4000], ["1/2", "1/2"]), ([1000, -500], ["4/5", "1/5"]),
           ([3500, -2000], ["1/4", "3/4"]), ([800, -1200], ["1/2", "1/2"]), ([5000, -3000], ["3/10", "7/10"]),
           ([2200, -2800], ["3/5", "2/5"]), ([1200, -600], ["1/2", "1/2"]), ([4500, -5000], ["2/3", "1/3"])]
# mirror of the B-side set (sides swapped, choices flipped; same likelihood)
responses = [
    {"pair_id": i, "choice": ("B" if CHOICES[i] == "A" else "A"), "prizes_a": A_MIXED[i][0], "probs_a": A_MIXED[i][1],
     "prizes_b": [SURE_B[i]], "probs_b": ["1"]}
    for i in range(12)
]
for label, mod in (("reference", ref), ("B-only mutant d10_01", mut)):
    try:
        out = mod.estimate(responses)
        print(label, "returns", {k: round(v, 4) for k, v in out.items()})
    except Exception as e:
        print(label, "raises", type(e).__name__, str(e)[:100])
