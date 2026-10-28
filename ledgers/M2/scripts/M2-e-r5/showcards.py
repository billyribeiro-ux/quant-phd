import json, sys
d = json.load(open("/tmp/verifyB5-M2-e/course/modules/M/M2/cards.json"))
for lesson in sys.argv[1:]:
    for c in d:
        if c["lesson"] == lesson:
            print(f'{c["id"]} [{c.get("grade")}] {c.get("basis","")!s}'.strip())
            print("  F:", c["front"])
            print("  B:", c["back"])
