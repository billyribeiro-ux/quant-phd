import json, importlib.util, sys
spec = importlib.util.spec_from_file_location("gen", sys.argv[1])
src = open(sys.argv[1]).read().split("frag = {")[0]   # reuse row builders from the generator
ns = {}
exec(src, ns)
fresh = {r["id"]: r for r in ns["rows"]}
prev = json.load(open("/Users/billyribeiro/.fanout/frags/C-FC1-b.round6.json"))
mapping = {
 "FC1-b-r7-gate-check-pages": "FC1-b-r5-gate-check-pages",
 "FC1-b-r7-gate-check-dag": "FC1-b-r5-gate-check-dag",
 "FC1-b-r7-gate-run-labs": "FC1-b-r5-gate-run-labs",
 "FC1-b-r7-gate-page-smoke": "FC1-b-r5-gate-page-smoke",
 "FC1-b-r7-gate-ruff-mypy-pytest": "FC1-b-r5-gate-ruff-pytest",
 "FC1-b-r7-gate-verify-refs-offline": "FC1-b-r5-gate-verify-refs-offline",
 "FC1-b-r7-twin-page-equality": "FC1-b-r5-twin-page-equality",
 "FC1-b-r7-expected-equals-output": "FC1-b-r5-expected-equals-output",
 "FC1-b-r7-M3-separate-arrivals": "FC1-b-r6-M3-separate-arrivals",
 "FC1-b-r7-M3-stale-stop-rule": "FC1-b-r5-M3-stale-stop-rule",
 "FC1-b-r7-M3-examples-problems": "FC1-b-r6-L04-M3-examples-problems",
 "FC1-b-r7-cards-L04-L05-unchanged": "FC1-b-r6-cards-vs-changed-text",
 "FC1-b-r7-process-words": "FC1-b-r6-process-words",
}
out = []
done = set()
for r in prev["rows"]:
    rid = r["id"]
    if rid in mapping.values() or rid in ("FC1-b-r5-L04-process-words", "FC1-b-r6-no-banned-strings"):
        pass
    new_id = [k for k, v in mapping.items() if v == rid]
    if new_id:
        row = dict(fresh[new_id[0]]); row["id"] = rid; row["check"] = r["check"]
        out.append(row); done.add(rid); continue
    if rid in ("FC1-b-r5-L04-process-words", "FC1-b-r6-no-banned-strings"):
        row = {"id": rid, "check": r["check"], "location": "course/modules/FC/FC1/L04.html, L05.html, lab-FC1-L04-1.py, lab-FC1-L05-1.py",
               "status": "PASS", "evidence": "Re-run at 0d2d0f3: " + ("process words: 6 hits, all in lab docstrings or page text describing the lab's own checks (ledgers/FC1/scripts/FC1-b-r7/process_words.out)." if "process" in rid else "grep -i TODO|TBD|lorem and ellipsis in learner text: no hit outside code blocks.")}
        out.append(row); done.add(rid); continue
    if r["status"] != "PASS":
        # re-verified above (FAIL row) -> must be in mapping
        raise SystemExit("non-PASS row not re-verified: " + rid)
    row = dict(r)
    row["check"] = r["check"] if r["check"] != "" else "carried"
    row["evidence"] = ("Carried from round 6 (" + r["location"] + " byte-identical since the previous pin 9fd6aed, except that the delta hunks in L04.html (lines 59, 407-409) do not overlap the cited lines; L05.html, lab twins unchanged): " + r["evidence"])
    out.append(row); done.add(rid)
# extra new rows
for k, row in fresh.items():
    if k not in mapping and k not in [o["id"] for o in out]:
        out.append(row)
ids = [o["id"] for o in out]
assert len(ids) == len(set(ids)), "duplicate ids"
frag = {
 "unit": "FC1", "slice": "FC1-b", "round": 7,
 "verifier": "Claude Haiku 5.5, independent verifier for FC1-b round 7 (did not build FC1)",
 "pin": "0d2d0f3f8ffb68fc54bb854cb1d7bf28e6483e78",
 "base": "9fd6aed (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/C-FC1-b.round6.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC7-FC1-b",
 "scratch": "ledgers/FC1/scripts/FC1-b-r7/",
 "verified_at": "2026-10-29",
 "verdict": "PASS" if all(o["status"] == "PASS" for o in out) else "FAIL",
 "rows": out, "mutants": [], "registry_flags": [], "freshness_flags": [],
 "notes": ["Delta 9fd6aed..0d2d0f3 for the slice: L04.html line 59 (Definition 1.1 market-order sentence) and lines 407-409 (M3). L05.html, both twins and the L04/L05 cards are byte-identical. Round-6 FAIL FC1-b-r6-M3-separate-arrivals is fixed and re-verified. No grader in this slice, so no mutants."],
 "summary": "FC1-b round 7: %d rows, %d PASS, %d FAIL. The round-6 M3 FAIL (FC1-b-r6-M3-separate-arrivals) is fixed and re-verified. All gates pass at 0d2d0f3. Rows whose cited subject is unchanged are carried from round 6." % (len(out), sum(o["status"]=="PASS" for o in out), sum(o["status"]!="PASS" for o in out)),
}
json.dump(frag, open("ledgers/FC1/FC1-b.json", "w"), indent=1, ensure_ascii=False)
print(len(out), frag["verdict"])
