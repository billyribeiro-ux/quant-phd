#!/bin/bash
cd "$(dirname "$0")/../../../../course/modules/SC/SC1" || exit 1
for p in 'TODO' 'TBD' 'lorem' 'for brevity' 'details omitted' 'beyond the scope' 'left as an exercise' 'you can add more' 'it is important to note' 'studies show' 'experts agree' 'it is well known' 'obviously' 'clearly' 'It can be shown' 'roughly' 'historically' 'Note that' 'As we saw' 'we will see' "Let's" 'trivially' '\.\.\.' '…' 'in this section we' 'the student' 'the learner' 'Important' 'remarkably' 'surprisingly' 'as expected' 'it is easy' 'we now' 'you will'; do
  for f in index.html L01.html L02.html L03.html cards.json; do
    c=$(grep -i -c -F -- "$p" "$f")
    if [ "$c" != "0" ]; then echo "HIT[$p] in $f: $c"; grep -i -n -F -- "$p" "$f" | cut -c1-200 | head -3; fi
  done
done
echo scan-done
