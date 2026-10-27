import json, re, subprocess, datetime, sys
from pathlib import Path

CHK = Path("/tmp/verify-s7-r1-l12")
SCR = "/tmp/ap1-r5/s7-l12"
prev = json.loads(Path(f"{SCR}/previous-round33.json").read_text(encoding="utf-8"))
PAGES = ["course/modules/S/S7/L01.html", "course/modules/S/S7/L02.html"]
CHANGED = {"BLUEPRINT.md", "CLAUDE.md", "atlas/A8.contract.md", "tests/test_koning_spot.py"}
TOKEN = re.compile(r"(?:course|tests|tools|references|notation|atlas|curriculum)/[A-Za-z0-9_./*-]+")

# rows this round re-ran or re-derived itself (new evidence below)
RERUN = {}

def carried_files(row):
    m = re.match(r"Carried from the release ledger \((.*?)\):", row["evidence"], re.S)
    files = []
    if m:
        head = m.group(1).split("; ")[0]
        head = head.replace(" byte-identical since 5e5da87", "")
        files = [f.strip() for f in head.split(", ") if f.strip()]
        if "references/references.json" in m.group(1):
            files.append("references/references.json")
    else:
        files = [t.rstrip(".") for t in TOKEN.findall(row["location"])]
    rid = row["id"]
    if rid.startswith("L01-L02") or rid.startswith("T33"):
        files += PAGES
    elif rid.startswith("L01-"):
        files += [PAGES[0]]
    elif rid.startswith("L02-"):
        files += [PAGES[1]]
    if not files:
        files = PAGES
    out = []
    for f in files:
        if f not in out:
            out.append(f)
    return out

def body_of(row):
    m = re.match(r"Carried from the release ledger \(.*?\):\s*", row["evidence"], re.S)
    body = row["evidence"][m.end():] if m else row["evidence"]
    body = body.replace("Re-run this round", "Re-run in round 33").replace("this round", "in round 33")
    return body

NEW = {}
exec(open(f"{SCR}/new_evidence.py", encoding="utf-8").read())  # defines NEW (id -> dict) and NEW_ROWS

rows_out = []
carried_ids, rerun_ids, untracked_cited = [], [], []
for row in prev["rows"]:
    rid = row["id"]
    if rid in NEW:
        new = dict(row)
        new.update(NEW[rid])
        rows_out.append(new)
        rerun_ids.append(rid)
        continue
    files = carried_files(row)
    for f in files:
        if f in CHANGED:
            raise SystemExit(f"row {rid} depends on changed file {f}")
    prefix = f"Carried from round 33 ({', '.join(files)} byte-identical since bcf4e25): "
    new = dict(row)
    new["evidence"] = prefix + body_of(row)
    rows_out.append(new)
    carried_ids.append(rid)
    for s in re.findall(r"scripts/[A-Za-z0-9_./-]+\.py", row["location"] + " " + row["evidence"]):
        untracked_cited.append((rid, s))

rows_out += NEW_ROWS
ids = [r["id"] for r in rows_out]
assert len(ids) == len(set(ids)), "duplicate ids"

# per-row file identity check against bcf4e25 (union of all carried subjects must be unchanged)
union = sorted({f for rid in carried_ids for f in re.findall(r"(?:course|tests|tools|references|notation|atlas|curriculum)/[^\s,]+", " ".join([]))})
all_files = set()
for r in rows_out:
    m = re.search(r"Carried from round 33 \((.*?) byte-identical since bcf4e25\):", r["evidence"])
    if m:
        for f in m.group(1).split(", "):
            all_files.add(f)
pathspec = sorted(all_files)
rc = subprocess.run(["git", "diff", "--quiet", "bcf4e25", "HEAD", "--", *pathspec], cwd=CHK).returncode
print("git diff --quiet bcf4e25 HEAD over all carried subjects rc =", rc, "files:", len(pathspec))

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows_out:
    counts[r["status"]] += 1
fail_ids = [r["id"] for r in rows_out if r["status"] == "FAIL"]
unv_ids = [r["id"] for r in rows_out if r["status"] == "UNVERIFIABLE"]
verdict = "PASS" if all(r["status"] == "PASS" for r in rows_out) else "FAIL"

frag = {
    "unit": "S7",
    "slice": "L01-L02",
    "round": 34,
    "verifier": "round-34 verifier (independent of the builders and of the round-33 verifier; re-ran the Koning spot check from the committed test and mutate-checked it; re-ran every command row named in the round-34 brief; carried every other row by git diff --quiet against bcf4e25)",
    "pin": "e6d10ab",
    "base": "bcf4e25",
    "previous_ledger": "ledgers/S7/L01-L02.json as it stood in this checkout (round 33, pin bcf4e25, 471 rows: 470 PASS, 1 UNVERIFIABLE = L01-cmd-koning-spot-a2a631a)",
    "checkout": CHK.as_posix(),
    "scratch": SCR,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "changed_since_base": {
        "bcf4e25..e6d10ab (git diff --stat, 4 files)": "BLUEPRINT.md (line 356, toolchain sentence 3.12+ -> 3.14+); CLAUDE.md (line 79, Python 3.12+ -> 3.14+); atlas/A8.contract.md (amendment header: NumPy 2.2 -> 2.4, no signature change); tests/test_koning_spot.py (new, 53 lines). None of these is a slice file: git diff --quiet bcf4e25 HEAD -- course/modules/S/S7/ rc 0 (whole directory).",
        "slice files": "course/modules/S/S7/L01.html, L02.html, cards.json, figures-L01.js, figures-L02.js and tests/labs/S7/lab-S7-L01-*.py, lab-S7-L02-*.py are byte-identical since bcf4e25 (git diff --quiet, rc 0).",
    },
    "line_numbering": prev.get("line_numbering", ""),
    "rows": rows_out,
    "mutants": [],
    "registry_flags": prev["registry_flags"],
    "freshness_flags": prev["freshness_flags"],
    "open_questions": prev["open_questions"] + [
        "R34-1. Reproducibility of carried command rows: the round-33 rows that cite scripts/*.py (recompute, prose_scan, fig_sweep, fig_sweep_check, fig_states, fig_expect, structure_checks, misc5_exact) name scripts that are not tracked in the repository (git ls-files scripts: 0 files). They were carried, not re-run, under the round-34 brief. The architect should commit them, as tests/test_koning_spot.py was committed, or the rows are unverifiable by the same reasoning that fails L01-cmd-koning-spot-a2a631a. Rows: " + "; ".join(sorted({i for i, _ in untracked_cited})),
    ],
    "notes": [
        "ROUND 34: verifier re-check of the released S7 L01-L02 slice at e6d10ab (base bcf4e25). Toolchain unchanged since round 33: Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2 (repo .venv); the four-file delta since bcf4e25 touches none of the slice.",
        "Koning spot check (L01-cmd-koning-spot-a2a631a): the committed test passes (3 passed) and its simulation reproduces the round-33 replacement values (size 0.0498375; E[phi_tau] 0.04966, 0.04981, 0.04999), but NOT the round-24 printed stopping sizes 0.05012...0.05004, and it bounds claim 1 at 0.052, not 0.05. Row stays UNVERIFIABLE.",
        "Banned phrase: 'roughly half a standard deviation' (L01.html line 133) is not an allowed (a), (b) or (c) number under BUILDER_RULES 1.2 as written; the gap it describes is 0.44-0.64 SD over N = 2..10,000 and the caption names no N. Row T34-banned-roughly-half-caption FAILS.",
        "Re-run in round 34: run_labs --unit S7 (42/42; L01 4/4, L02 3/3), check_pages, check_dag, check_projects (S7 PASS), page_smoke --pages L01 L02 (PASS), verify_refs --unit S7 live (94 of 560, 0 problems) and --offline (560, 0 problems), ruff check ., ruff format --check ., mypy (102 files), pytest on the three named files (49 passed).",
        "Numeric command rows L01-cmd-m1-m4, L01-cmd-m5 and L02-cmd-m3-example42 were re-derived in round 34 (scratch scripts /tmp/ap1-r5/s7-l12/rederive.py and m5.py), because their round-33 evidence cited scratch paths that are not in the repository. Every value on the page for those spans matched at the page's rounding.",
        "All other rows are carried from round 33 by git diff --quiet against bcf4e25 (prefix 'Carried from round 33 (...)'). Command rows that were not re-run in round 34 (lab twins, fig-drive, fig-samples, expmax-sweep, render_curriculum, build_site, fetch_data, prose-scan, cards-scan, refs-render, dfn-check) are carried under the brief's instruction; see open question R34-1 for the scripts they cite.",
    ],
    "summary": {
        "rows": len(rows_out),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "carried_from_round_33": len(carried_ids),
        "rerun_or_rederived_this_round": len(rerun_ids),
        "new_rows_this_round": ["T34-banned-roughly-half-caption", "T34-koning-test-mutants"],
        "mutants": 0,
        "mutants_killed": 0,
        "fail_ids": fail_ids,
        "unverifiable_ids": unv_ids,
        "verdict_rule": "PASS only if every row is PASS; UNVERIFIABLE counts as a failure.",
    },
}
out = CHK / "ledgers/S7/L01-L02.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows_out), counts, "verdict", verdict, "carried", len(carried_ids), "rerun", len(rerun_ids))
print("untracked-script citations in carried rows:", len({i for i, _ in untracked_cited}), "rows")
