#!/bin/bash
# Round 16, FC1-c: every inline math token on the project page, and the added lines of this delta that contain math.
cd /Users/billyribeiro/.fanout/wt/verifyD16-FC1-c || exit 1
echo "== math tokens on the project page (all)"
grep -o '\\([^)]*\\)' course/modules/FC/FC1/project.html | sort | uniq -c
echo "== added delta lines containing math"
git diff dde0486b..HEAD -- course/modules/FC/FC1/project.html | grep '^+' | grep -o '\\([^)]*\\)' | sort | uniq -c
