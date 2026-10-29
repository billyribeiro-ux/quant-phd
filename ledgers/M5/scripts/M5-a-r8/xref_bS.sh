#!/bin/sh
# Re-derive: where is the bounded-function symbol B(S) / B(N) used after the L04 rename to l^infty(S)?
cd "$1" || exit 1
echo "== definitions in L04 (expect none for B(S), l^infty present)"
grep -n 'B(S)\|ell^{\\infty}' course/modules/M/M5/L04.html | cut -c1-140
echo "== remaining B(S)/B(N) uses in M5 pages and cards"
grep -n 'B(S)\|B(\\mathbb{N})\|B(\\mathbb' course/modules/M/M5/*.html course/modules/M/M5/cards.json | cut -c1-160
