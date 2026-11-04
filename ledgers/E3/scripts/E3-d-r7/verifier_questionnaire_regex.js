const isProbability = (text) => typeof text === "string" && /^\d+(\/\d*[1-9]\d*)?$/.test(text);
const cases = ["1", "0", "1/2", "3/4", "10/20", "0/1", "1/0", "1/", "/2", "-1/4", "5/4", "1/01", "0.5", " 1", "1/00", "", "2/2"];
for (const c of cases) console.log(JSON.stringify(c), isProbability(c));
