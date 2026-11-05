"""Round-7 checks for LX1-d cards: (1) MANIFEST facts cited by cards c047, c063, c064, c069, c070, c075;
(2) registered notation symbols (notation/notation.json) appearing in cards or in the L01-L04 text;
(3) scope words in card front/back, printed with context.

Usage: python3 -I manifest_notation_scope_r7.py <checkout> <lesson text dir>
"""
import csv, json, re, sys

base, txt = sys.argv[1], sys.argv[2]
man = json.load(open(f"{base}/course/assets/data/market/MANIFEST.json", encoding="utf-8"))
ds = {d["id"]: d for d in man["datasets"]}
print("(1) MANIFEST datasets:", sorted(ds))
fx = ds["fx_monthly"]
print("fx_monthly rows", fx["rows"], "first", fx["first"], "last", fx["last"], "retrieved", fx["retrieved"])
print("fx_monthly columns", fx["columns"])
print("fx_daily first", ds["fx_daily"]["first"], "ust_daily first", ds["ust_daily"]["first"])
rows = list(csv.DictReader(open(f"{base}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("csv header", list(rows[0].keys()), "rows", len(rows), rows[0]["month"], rows[-1]["month"])
print("csv has interest or forward column:", any(re.search(r"rate|forward|yield|interest", k, re.I) for k in rows[0]))
print("manifest transform inverts:", re.findall(r"CAD, CHF, DKK, JPY, NOK, SEK inverted", fx["transform"]))

print("(2) registered notation symbols:")
reg = [v["symbol"] for v in json.load(open(f"{base}/notation/notation.json", encoding="utf-8"))["symbols"]]
cards = json.load(open(f"{base}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
card_text = " ".join(c["front"] + " " + c["back"] for c in cards)
lesson_text = " ".join(open(f"{txt}/{L}.txt", encoding="utf-8").read() for L in ("L01", "L02", "L03", "L04"))
for sym in reg:
    key = sym.split(",")[0].strip()
    print(f"  {key!r}: in cards={key in card_text}; in lessons={key in lesson_text}")

print("(3) scope words in card front/back:")
pat = re.compile(r"\b(only|all|always|every|any|same|exactly|whenever|never)\b", re.I)
n = 0
for c in cards:
    for f in ("front", "back"):
        for m in pat.finditer(c[f]):
            n += 1
print("scope-word occurrences:", n)

# (2b) The bare letter T is a registered symbol (number of observations). Grade labels "(T)" and the word "Theorem"
# are not that symbol. Count math-like uses of T in the lesson text and in card fronts/backs.
t_math = re.compile(r"\\\(T[ _^=),]|\bT\s*=|\bT\s*(?:observations|periods)")
print("(2b) math-like uses of symbol T in lessons:", sum(len(t_math.findall(l)) for l in lesson_text.splitlines()))
print("(2b) math-like uses of symbol T in card front/back:", sum(len(t_math.findall(c["front"] + " " + c["back"])) for c in cards))
