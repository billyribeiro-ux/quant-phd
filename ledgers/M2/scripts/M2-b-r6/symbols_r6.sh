#!/bin/sh
# Round-6: fixed-string counts of the eight symbols registered in notation/notation.json, in the six slice pages.
cd /Users/billyribeiro/.fanout/wt/verifyS6-M2-b || exit 1
for f in L07 L08 L09 L10 L11 L12; do
  printf "%s " "$f"
  for s in '\Phi' '\gamma_3' '\gamma_4' 'R^\ast' 'R^{e\ast}' 'R_f' '\mathbb{Q}' '\Prob' '\E['; do
    printf "[%s]=%s " "$s" "$(grep -F -c -- "$s" course/modules/M/M2/$f.html)"
  done
  echo
done
