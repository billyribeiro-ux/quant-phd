#!/bin/sh
# Lesson and hub hours for M5 (run from the checkout root).
for f in course/modules/M/M5/L0*.html course/modules/M/M5/L10.html; do grep -o 'data-hours="[0-9.]*"' "$f" | head -1 | sed "s|^|$(basename $f) |"; done
grep -o 'data-hours-[a-z]*="[0-9.]*"' course/modules/M/M5/index.html course/modules/M/M5/project.html
