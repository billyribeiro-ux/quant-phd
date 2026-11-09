#!/bin/sh
# Round-12 verifier (M3 slice d): process-word, external-link and local-target scans over the slice's learner-facing files.
# Run from the checkout root.
echo "== process words (project.html, cards.json, grader, labs)"
grep -n -i -o "verifier\|ledger\|fixer\|builder\|round [0-9]\|round-[0-9]\|agent\|revised\|audit" course/modules/M/M3/project.html course/modules/M/M3/cards.json course/modules/M/M3/grader/*.py tests/labs/M3/lab-M3-project-*.py || echo "none"
echo "== external http(s) references in project.html"
grep -n -o "https\?://[^\"' )<]*" course/modules/M/M3/project.html || echo "none"
echo "== href/src targets in project.html that are neither anchors nor relative paths"
grep -o 'href="[^"]*"\|src="[^"]*"' course/modules/M/M3/project.html | grep -v 'href="#' | grep -v '"\.\./\|"[a-zA-Z0-9_.-]*\.html\|"grader/\|"review' || echo "none"
