"""Probe (not a mutant file): does the suite notice a parity explanation whose trade direction is reversed?

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/direction_probe.py <repo_root>
Builds a copy of reference.py in which the direction clause of the parity explanation is swapped (the positive-gap
action is written for a negative gap, and the reverse), keeps every label, and runs the suite on seeds 0..9.
A survivor here is not a grader fault unless project.html or the spec states the direction; see the round-5 notes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

root = sys.argv[1]
grader = os.path.join(root, "course", "modules", "FC", "FC2", "grader")
text = open(os.path.join(grader, "reference.py"), encoding="utf-8").read()
old = (
    '        action = "sell the call, buy the put and the underlying, and borrow the discounted strike"\n'
    '        direction = "the call less the put exceeds the spot less the discounted strike"\n'
    "    else:\n"
    '        action = "buy the call, sell the put and the underlying, and lend the discounted strike"\n'
    '        direction = "the call less the put is below the spot less the discounted strike"\n'
)
new = (
    '        action = "buy the call, sell the put and the underlying, and lend the discounted strike"\n'
    '        direction = "the call less the put is below the spot less the discounted strike"\n'
    "    else:\n"
    '        action = "sell the call, buy the put and the underlying, and borrow the discounted strike"\n'
    '        direction = "the call less the put exceeds the spot less the discounted strike"\n'
)
assert text.count(old) == 1
mutant = text.replace(old, new, 1)
results = []
for seed in range(10):
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "scanner.py"), "w", encoding="utf-8") as fh:
            fh.write(mutant)
        for name in ("instance.py", "test_project.py"):
            shutil.copy(os.path.join(grader, name), tmp)
        env = dict(os.environ, QF_SEED=str(seed))
        out = subprocess.run(
            [os.path.join(root, ".venv", "bin", "python"), "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "--assert=plain", "-W", "error", "test_project.py"],
            cwd=tmp, env=env, capture_output=True, text=True,
        )
        results.append((seed, out.returncode))
print("direction-swapped parity explanation, seeds 0..9 (seed, pytest rc; 0 means the suite passes):")
print(results)
print("survives all seeds:", all(rc == 0 for _, rc in results))
