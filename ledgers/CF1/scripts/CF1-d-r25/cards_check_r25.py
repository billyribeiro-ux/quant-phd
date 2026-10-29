"""Re-check cards.json of CF1: field presence, grade values, duplicates, counts, lesson ids, and the changed entry CF1-c110."""
import collections, json, pathlib, re
P = pathlib.Path("/tmp/verify25-CF1-d/course/modules/CF/CF1")
cards = json.loads((P / "cards.json").read_text(encoding="utf-8"))
print("entries", len(cards), "unique ids", len({c["id"] for c in cards}))
print("grades", dict(collections.Counter(c["grade"] for c in cards)))
bad_fields = [c["id"] for c in cards if not ({"id", "lesson", "front", "back", "grade"} <= set(c)) or not (c.get("cite") or c.get("basis"))]
print("entries missing fields or cite/basis:", bad_fields)
print("grade values not in {T,C}:", [c["id"] for c in cards if c["grade"] not in ("T", "C")])
print("lesson ids:", sorted(collections.Counter(c["lesson"] for c in cards).items()))
print("ids well formed:", all(re.fullmatch(r"CF1-c\d{3}", c["id"]) for c in cards))
fronts = collections.Counter(c["front"] for c in cards); backs = collections.Counter(c["back"] for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1], "duplicate backs:", [b for b, n in backs.items() if n > 1])
banned = re.compile(r"roughly half|about 6%|historically|\.\.\.|\bbuilder\b|\bverifier\b|\bround\b", re.I)
print("banned or process words in cards:", [(c["id"], m.group(0)) for c in cards for m in [banned.search(c["front"] + " " + c["back"])] if m])
c110 = [c for c in cards if c["id"] == "CF1-c110"][0]
print("c110:", c110["grade"], "|", c110["basis"])
# Every T card must carry a basis or cite; C cards must carry a basis naming a convention or an open item.
print("T cards with cite (not basis):", [c["id"] for c in cards if c["grade"] == "T" and c.get("cite") and not c.get("basis")][:10])
