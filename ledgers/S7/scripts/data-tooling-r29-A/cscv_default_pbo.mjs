// Round 29: the default state of the L08 cscv-explorer figure, recomputed with the figure's own kernels
// (figures-L08.js simulate and multitest.js cscv, S = 8 blocks, seed 501 = DEFAULT_CSCV_SEED), and the seed-median check:
// the default must be a median history (its PBO equals the median of PBO over seeds 1-200).
// Run: node ledgers/S7/scripts/data-tooling-r29-A/cscv_default_pbo.mjs <repo root>
const root = process.argv[2];
const fig = await import(`${root}/course/modules/S/S7/figures-L08.js`);
const mt = await import(`${root}/course/assets/js/multitest.js`);
const S = 8;
const pbo = (seed, edge) => mt.cscv(fig.simulate(seed, edge), S).pbo;
const out = { default_seed: fig.DEFAULT_CSCV_SEED, pbo_default_edge_off: pbo(fig.DEFAULT_CSCV_SEED, false), pbo_default_edge_on: pbo(fig.DEFAULT_CSCV_SEED, true) };
const offs = [], ons = [];
for (let s = 1; s <= 200; s++) { offs.push(pbo(s, false)); ons.push(pbo(s, true)); }
const med = (xs) => { const a = [...xs].sort((x, y) => x - y); return [a[99], a[100]]; };
out.median_seeds_1_200_edge_off = med(offs);
out.median_seeds_1_200_edge_on = med(ons);
console.log(JSON.stringify(out, null, 1));
