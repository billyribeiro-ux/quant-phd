"""For every card in course/modules/BK/BK4/cards.json, list each number in the front and back that does not
appear as a token in the card's own lesson page text (extracted by extract_text.py).

Usage: python -I card_numbers.py <cards.json> <lesson_text_dir>
Lesson text files are named L01.txt ... L05.txt.
"""
import json
import re
import sys

NUM = re.compile(r"(?<![A-Za-z_])\d+(?:[.,]\d+)*(?:/\d+)?")


def norm(text: str) -> str:
    text = text.replace("\\(", " ").replace("\\)", " ").replace("\\[", " ").replace("\\]", " ")
    text = text.replace("{", " ").replace("}", " ").replace("\\", " ")
    return text


def main() -> None:
    cards = json.load(open(sys.argv[1], encoding="utf-8"))
    textdir = sys.argv[2]
    lessons: dict[str, str] = {}
    for c in cards:
        lid = c["lesson"]
        if lid not in lessons:
            lessons[lid] = norm(open(f"{textdir}/{lid}.txt", encoding="utf-8").read())
    misses = 0
    for c in cards:
        text = lessons[c["lesson"]]
        nums = set(NUM.findall(c["front"] + " " + c["back"]))
        for n in sorted(nums):
            if n.rstrip(".,") == n:
                pat = re.escape(n)
            else:
                pat = re.escape(n.rstrip(".,"))
            if not re.search(r"(?<![\d.])" + pat + r"(?![\d])", text):
                misses += 1
                print(f"{c['id']} {c['lesson']} number {n!r} not in lesson text")
    print(f"total misses {misses}")


if __name__ == "__main__":
    main()
