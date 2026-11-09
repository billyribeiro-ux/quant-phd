"""Time one alternative solver on each seed 0-49 directly (no pytest), with a per-seed alarm.

Usage: python -I -W error time_alts_r12.py <repo-root> <alt-file> [limit-seconds]
Prints seed, elapsed seconds, and 'ok' or the exception kind. Used to locate solver cycling, not to grade.
"""

import importlib.util
import json
import signal
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
alt_path = Path(sys.argv[2]).resolve()
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
sys.path.insert(0, str(root / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("alt_under_test", alt_path)
assert spec is not None and spec.loader is not None
alt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = alt
spec.loader.exec_module(alt)


class Slow(Exception):
    pass


def on_alarm(signum: int, frame: object) -> None:
    raise Slow()


signal.signal(signal.SIGALRM, on_alarm)
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    signal.alarm(limit)
    started = time.perf_counter()
    try:
        alt.allocate(case)
        status = "ok"
    except Slow:
        status = "TIMEOUT"
    except Exception as exc:  # report, do not hide
        status = f"exception {type(exc).__name__}: {str(exc)[:80]}"
    finally:
        signal.alarm(0)
    print(f"seed {seed:2d} {time.perf_counter() - started:7.2f}s {status}", flush=True)
