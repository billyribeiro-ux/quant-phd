"""Round 10 verifier probe: a direct call on a hand-built state (no earlier engine game) separates mutant v39 from the reference."""

import importlib.util
import sys

MUT = sys.argv[1]
REF = sys.argv[2]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def turn_record(turn, filled, price):
    return {"turn": turn, "bid_cents": 9990, "ask_cents": 10010, "size": 1, "arrival": "informed",
            "filled": filled, "fill_price_cents": price, "inventory_after": 0, "cash_after_cents": 0}


history = [turn_record(1, False, None), turn_record(2, True, 10020), turn_record(3, False, None),
           turn_record(4, False, None)]
state = {"turn": 5, "inventory": 0, "cash_cents": 0, "max_size": 5, "limit": 10, "history": history}
ref = load(REF, "ref_mod").quote(dict(state))
mut = load(MUT, "mut_mod").quote(dict(state))
print("reference quote on turn 5 with a fill at 10020 on turn 2:", ref)
print("mutant v39 quote on the same state, fresh module:", mut)
print("differ:", ref != mut)
