"""Round-3 verifier (E3-d): validity and materiality of the autograder instances, on 20 seeds.

Checks, per seed: 200 pairs; each lottery has 2 or 3 integer-cent prizes with exact Fraction probabilities that are
positive and sum to exactly 1; at least 100 pairs mixed; the reported true parameters lie in the ranges that the
instance docstring states; the answers are A or B. Across the 20 seeds: the true parameters, wealth, the choice
vectors and the reference estimates must differ (not only the labels).

Usage: PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/instances_20_seeds_r3.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E3/grader"
sys.path.insert(0, str(GRADER))
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

SEEDS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 42, 7, 11, 17, 23, 29, 31, 37, 44, 47, 49]


def mixed(prizes, probs):
    gain = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    loss = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    return gain and loss


def main() -> int:
    rows = []
    problems = []
    for seed in SEEDS:
        inst = make_instance(seed)
        resp = json.loads(inst["responses_json"])
        if len(resp) != 200:
            problems.append((seed, "pair count", len(resp)))
        n_mixed = 0
        for r in resp:
            lots = []
            for side in ("a", "b"):
                prizes = r[f"prizes_{side}"]
                probs = [Fraction(s) for s in r[f"probs_{side}"]]
                if not all(isinstance(x, int) and not isinstance(x, bool) for x in prizes):
                    problems.append((seed, r["pair_id"], "non-int prize"))
                if len(prizes) not in (2, 3) or len(probs) != len(prizes):
                    problems.append((seed, r["pair_id"], "prize count"))
                if any(p <= 0 for p in probs) or sum(probs) != 1:
                    problems.append((seed, r["pair_id"], "probability"))
                if not all(500 <= abs(x) <= 50_000 for x in prizes):
                    problems.append((seed, r["pair_id"], "magnitude"))
                lots.append((prizes, probs))
            if r["choice"] not in ("A", "B"):
                problems.append((seed, r["pair_id"], "choice"))
            if any(mixed(*lot) for lot in lots):
                n_mixed += 1
        if n_mixed < 100:
            problems.append((seed, "mixed pairs", n_mixed))
        g, lam, k = inst["gamma"], inst["lambda"], inst["kappa"]
        if not (0.10 <= g <= 0.80 and 1.0 <= lam <= 3.0 and 0.5 <= k <= 5.0):
            problems.append((seed, "true parameters outside stated ranges", (g, lam, k)))
        if not (5_000_000 <= inst["wealth_cents"] <= 20_000_000):
            problems.append((seed, "wealth outside stated range", inst["wealth_cents"]))
        fit = ref.estimate(resp)
        rows.append(
            {
                "seed": seed,
                "mixed_pairs": n_mixed,
                "true": (g, lam, k),
                "wealth": inst["wealth_cents"],
                "chose_A": sum(1 for r in resp if r["choice"] == "A"),
                "est": (round(fit["gamma_hat"], 4), round(fit["lambda_hat"], 4), round(fit["kappa_hat"], 4)),
                "choice_string_hash": int(hashlib.sha256("".join(r["choice"] for r in resp).encode()).hexdigest()[:8], 16),
            }
        )
    for row in rows:
        print(json.dumps(row))
    print("validity problems:", problems if problems else "none")
    print("distinct true-parameter triples:", len({r["true"] for r in rows}), "of", len(rows))
    print("distinct wealth values:", len({r["wealth"] for r in rows}), "of", len(rows))
    print("distinct choice vectors:", len({r["choice_string_hash"] for r in rows}), "of", len(rows))
    print("distinct reference estimates:", len({r["est"] for r in rows}), "of", len(rows))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
