"""Normalise pdftotext output: join hyphenated line breaks and collapse whitespace.

Usage: python3 -I norm.py <in.txt> <out.txt>
"""
import re
import sys


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    src = src.replace("\f", "\n")
    src = re.sub(r"-\n(?=[a-z])", "", src)
    src = re.sub(r"[ \t]+", " ", src)
    src = re.sub(r"\n\s*\n+", "\n", src)
    flat = " ".join(src.split())
    open(sys.argv[2], "w", encoding="utf-8").write(flat)


if __name__ == "__main__":
    main()
