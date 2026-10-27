// Evaluate the page's own normCdf (course/assets/js/stats.js) at the points the figure test uses.
// Run: node ledgers/S7/scripts/data-tooling-r26/normcdf_compare.mjs <abs path to stats.js>
const mod = await import(process.argv[2]);
for (const x of [-3, -0.5, 0, 1.2, 4]) console.log(x, mod.normCdf(x).toPrecision(17), mod.normPdf(x).toPrecision(17));
