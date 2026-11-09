#!/usr/bin/env bash
# LX1-c round 19: plain curl of the licence page named in MANIFEST fx_monthly (licence_url), then a quote search.
# Usage: bash licence_check_r19.sh <scratch_dir>   (the scratch dir must be new and empty)
set -u
DIR="$1"
curl -s -m 60 -o "$DIR/disclaimer.htm" -w "HTTP %{http_code} from https://www.federalreserve.gov/disclaimer.htm\n" \
  https://www.federalreserve.gov/disclaimer.htm
/usr/bin/python3 -I - "$DIR/disclaimer.htm" <<'PY'
import html, re, sys
text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", open(sys.argv[1], encoding="utf-8", errors="replace").read())))
quote = "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information."
print("quote found verbatim:", quote in text)
PY
