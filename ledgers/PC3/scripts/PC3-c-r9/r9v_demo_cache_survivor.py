import sys
sys.path.insert(0, "/tmp/pc3c-r9/demo-cache")
import engine, market_maker as sol, importlib
alone = engine.play(sol.quote, 0)            # seed 0 in a fresh module state
importlib.reload(sol)
engine.play(sol.quote, 3)                    # another game first
after = engine.play(sol.quote, 0)            # seed 0 after another game
print("seed 0 alone == seed 0 after seed 3 (same log)?", alone == after)
print("quotes alone  :", [(t["bid_cents"], t["ask_cents"]) for t in alone["turns"]][:8])
print("quotes after :", [(t["bid_cents"], t["ask_cents"]) for t in after["turns"]][:8])
