"""Round-1 card scan for E4 slice e: ids, exact and near duplicates, per-lesson counts, changed-card diff."""

import difflib
import json
import sys
from collections import Counter
from pathlib import Path


def main(base_path: Path, new_path: Path) -> None:
    base = json.loads(base_path.read_text(encoding="utf-8"))
    new = json.loads(new_path.read_text(encoding="utf-8"))
    ids = [c["id"] for c in new]
    print(f"cards {len(new)} unique_ids {len(set(ids))}")
    fronts = Counter(c["front"] for c in new)
    backs = Counter(c["back"] for c in new)
    print("exact duplicate fronts", [f for f, n in fronts.items() if n > 1])
    print("exact duplicate backs", [b for b, n in backs.items() if n > 1])
    by_id_base = {c["id"]: c for c in base}
    by_id_new = {c["id"]: c for c in new}
    changed = sorted(k for k in by_id_base if k in by_id_new and by_id_base[k] != by_id_new[k])
    added = sorted(set(by_id_new) - set(by_id_base))
    removed = sorted(set(by_id_base) - set(by_id_new))
    unchanged = len(by_id_base) - len(changed) - len(removed)
    print(f"changed {len(changed)} added {len(added)} removed {len(removed)} unchanged {unchanged}")
    print("changed ids", changed)
    print("added ids", added)
    print("removed ids", removed)
    print("per lesson (new)", sorted(Counter(c["lesson"] for c in new).items()))
    print("per lesson (base)", sorted(Counter(c["lesson"] for c in base).items()))
    touched = set(changed) | set(added)
    for i, a in enumerate(new):
        for b in new[i + 1 :]:
            if a["id"] not in touched and b["id"] not in touched:
                continue
            fr = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
            bk = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
            if fr >= 0.75 or bk >= 0.75:
                print(f"near {a['id']} {b['id']} front {fr:.2f} back {bk:.2f}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
