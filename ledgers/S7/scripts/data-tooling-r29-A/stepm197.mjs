// Round 29: count the studies (seeds 0-999) in which a later StepM step adds a rejection, with the figure's own code
// (course/modules/S/S7/figures-L05.js study(seed), which calls the repository's multitest.js stepdown). Also the median
// checks the comment states (seeds 0-299: single-step count, StepM count, first critical-value fall).
// Run: node ledgers/S7/scripts/data-tooling-r29-A/stepm197.mjs <repo root>
const root = process.argv[2];
const fig = await import(`${root}/course/modules/S/S7/figures-L05.js`);
const N = Number(process.env.N || 1000);
let later = 0;
const rows = [];
const t0 = Date.now();
for (let seed = 0; seed < N; seed++) {
  const { result } = fig.study(seed);
  const single = result.steps[0].rejected.length;
  const total = result.mask.filter(Boolean).length;
  if (total > single) later++;
  if (seed < 300) rows.push({ seed, single, total, c1: result.steps[0].critical, c2: result.steps.length > 1 ? result.steps[1].critical : null });
}
const med = (xs) => { const s = [...xs].sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };
const s300 = rows.map((r) => r.single), t300 = rows.map((r) => r.total);
const falls = rows.filter((r) => r.c2 !== null).map((r) => r.c1 - r.c2).sort((a, b) => a - b);
const study101 = rows.find((r) => r.seed === 101);
console.log(JSON.stringify({ seeds: N, studies_with_later_step_adding_a_rejection: later, seconds: (Date.now() - t0) / 1000,
  seeds_0_299: { median_single_step: med(s300), median_stepm: med(t300), studies_with_second_step: falls.length,
    median_fall_middle_two: [falls[falls.length / 2 - 1], falls[falls.length / 2]], study101: study101 } }, null, 1));
