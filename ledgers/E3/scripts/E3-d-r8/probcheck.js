const isProbability = (text) => typeof text === "string" && /^\d+(\/\d*[1-9]\d*)?$/.test(text);
const cases = ["0", "1", "1/2", "499/1000", "2/0", "1/0", "1/05", "00", "-1/4", "5/4", "1/", "1/2/3", " 1", "1.0", "01", "0/1", "1/00"];
for (const c of cases) console.log(JSON.stringify(c), isProbability(c));
