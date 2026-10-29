import json, re, html, sys
cards = json.load(open("course/modules/M/M5/cards.json", encoding="utf-8"))
changed = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
def text_of(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)
for c in cards:
    if changed and c["id"] not in changed:
        continue
    lesson = text_of(f"course/modules/M/M5/{c['lesson']}.html")
    lesson_compact = re.sub(r"\s+", " ", lesson)
    nums = set(re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?|\d+/\d+", c["back"]))
    missing = [n for n in sorted(nums) if n not in lesson_compact]
    print(c["id"], c["lesson"], "nums", sorted(nums), "missing_in_lesson", missing)
