# usage: output_in_lesson_r16.py <twin-output-file> <stripped-lesson-txt>
# For every non-empty line the twin prints, report whether that line (whitespace-normalised) occurs in the stripped lesson text.
import re, sys
out = open(sys.argv[1], encoding="utf-8").read().splitlines()
lesson = re.sub(r"\s+", " ", open(sys.argv[2], encoding="utf-8").read())
missing = []
for line in out:
    norm = re.sub(r"\s+", " ", line).strip()
    if not norm:
        continue
    if norm not in lesson:
        missing.append(norm)
print(f"output lines: {sum(1 for l in out if l.strip())}; not found verbatim in lesson: {len(missing)}")
for m in missing:
    print("  MISSING:", m)
