"""Candidate fix test for the plain-float convexity gap (verifier round 17): run against each solution file.

Usage: candidate_test_r17.py <solution.py>. Loads the solution as a module and checks the candidate chain.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("sol", sys.argv[1])
sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sol)
chain = {"spot_cents": 0, "df_ppm": 1_000_000, "strikes_cents": [1, 2, 7], "call_cents": [7, 7, 4],
         "put_cents": [8, 9, 11], "cost": {"fee_cents_per_contract": 0, "half_spread_cents": 0}}
rows = [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in sol.scan(chain)]
print("PASS" if rows == [("convexity", 2, 1, 1)] else f"FAIL got {rows}")
