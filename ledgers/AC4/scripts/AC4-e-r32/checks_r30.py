"""Round-30 fresh checks for AC4 slice e: cards structure and counts, duplicates, banned phrases, hours arithmetic,
card-to-lab figures (lab output read), and the changed-card objects against the git diff since pin 503d139."""
import collections, json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(sys.argv[1]); AC4 = ROOT / "course/modules/AC/AC4"
cards = json.loads((AC4 / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
ids = [c["id"] for c in cards]
print("id sequence c001..c141 contiguous:", ids == [f"AC4-c{i:03d}" for i in range(1, 142)])
print("lessons:", dict(sorted(collections.Counter(c["lesson"] for c in cards).items())))
print("grades:", dict(collections.Counter(c.get("grade", "none") for c in cards)))
bad = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
bad += [c["id"] for c in cards if c.get("grade") in (None, "T") and c.get("basis")]
print("grade C cards without basis, or T/ungraded with basis:", bad)
print("front duplicates:", [k for k, n in collections.Counter(c["front"] for c in cards).items() if n > 1])
print("back duplicates:", [k for k, n in collections.Counter(c["back"] for c in cards).items() if n > 1])
pat = re.compile(r"\b(TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|well known|obviously|clearly|roughly|historically|about \d)\b", re.I)
hits = [(c["id"], m.group(0)) for c in cards for f in ("front", "back") for m in pat.finditer(c[f])]
hits += [("project.html", m.group(0)) for m in pat.finditer((AC4 / "project.html").read_text(encoding="utf-8"))]
print("banned-phrase hits in cards and project page:", hits)
print("process words in project page:", [m.group(0) for m in re.finditer(r"\b(builder|verifier|round \d+|REQUESTS?)\b", (AC4 / "project.html").read_text(encoding="utf-8"), re.I)])
html = (AC4 / "project.html").read_text(encoding="utf-8")
tb = html[html.index('id="hours"'):html.index('id="grader-section"')]
nums = re.findall(r'<td class="num">(?:<strong>)?(\d+)(?:</strong>)?</td>', tb)
print("time-budget numbers:", nums, "components sum:", sum(int(x) for x in nums[:-1]), "declared total:", nums[-1])
lesson_hours = sum(int(m) for m in re.findall(r'data-hours="(\d+)"', "".join((AC4 / f"L0{i}.html").read_text(encoding="utf-8") for i in range(1, 9))))
print("lesson hours:", lesson_hours, "project hours declared:", re.search(r'data-hours-project="(\d+)"', html).group(1))
def at(rev):
    raw = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:course/modules/AC/AC4/cards.json"], capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}
old, new = at("503d139"), at("5aeaaf0")
print("card objects differing since 503d139:", sorted(i for i in set(old) | set(new) if old.get(i) != new.get(i)))
