const isProbability = (text) => typeof text === "string" && /^(0|1|\d+\/\d*[1-9]\d*)$/.test(text);
const cases = {"0":1,"1":1,"1/2":1,"9/10":1,"0/5":1,"2/1":1,"1/0":0,"0/0":0,"-1/2":0,"1.0":0,"1/2/3":0,"":0,"01":0,"10/20":1,"1/":0,"1/01":1};
let bad = [];
for (const [s, want] of Object.entries(cases)) { const got = isProbability(s) ? 1 : 0; if (got !== want) bad.push([s, got, want]); }
console.log(JSON.stringify({mismatches: bad}));
