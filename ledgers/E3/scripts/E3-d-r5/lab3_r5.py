"""Independent Lab 3 re-derivation and exemplar-B fact checks (round 5)."""
import sys
from fractions import Fraction
from pathlib import Path
import math
import numpy as np

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyC5-E3-d/ledgers/E3/scripts/E3-d-r5")
import importlib.util
spec = importlib.util.spec_from_file_location("r", "/Users/billyribeiro/.fanout/wt/verifyC5-E3-d/ledgers/E3/scripts/E3-d-r5/recompute_r5.py")
