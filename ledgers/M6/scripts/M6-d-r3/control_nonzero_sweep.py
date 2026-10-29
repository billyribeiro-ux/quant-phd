"""Sweep seeds for the grader's own preconditions on the reference: the control's stopped expectation is nonzero for both instances the suite draws (INST and INST2 = seed + 7919), and the reference's doubling expectations satisfy the suite's rounding tests. Seeds 0 to 20000 plus 338303287."""

from __future__ import annotations

import importlib.util
from fractions import Fraction as F
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyC3-M6-d/course/modules/M/M6/grader")
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
inst_mod = load("instance_m", GRADER / "instance.py")
ref = load("ref_m", GRADER / "reference.py")
CONTROL = F(1, 3)
zero_control = []
bad_identity = []
seeds = list(range(0, 20001)) + [338303287]
for seed in seeds:
    for s in (seed, seed + 7919):
        inst = inst_mod.make_instance(s)
        ctl = dict(inst, win_probability=CONTROL)
        if ref.stopped_value_expectation(ctl) == 0:
            zero_control.append(s)
        if ref.stopped_value_expectation(dict(inst, win_probability=F(1, 2))) != 0:
            bad_identity.append(s)
print("seeds checked:", len(seeds) * 2)
print("control stopped expectation equal to 0 (the suite's value != 0 test would fail the reference):", zero_control[:20], len(zero_control))
print("fair walk stopped expectation not 0 (would break optional stopping):", bad_identity[:20], len(bad_identity))
