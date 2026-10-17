// S7 hub figure: which claim each tool in the module licenses, with links to the lessons.
// Drawn as SVG at the container's width: two columns on wide screens, one on phones.

import { drawAll, mountFigure, multilineText, svgFrame, wrapLines } from "../../../assets/js/chart.js";

const ROOT = "You tried many strategies on one history. Lesson 1: the best of them overstates its skill. Which claim do you want to make?";
const ROWS = [
  { claim: "At least one strategy beats the benchmark.", tools: "White's Reality Check and Hansen's SPA (L04)", lesson: "L04", series: 0 },
  { claim: "These particular strategies beat it, with no false positive among them at level α.", tools: "Bonferroni and Holm (L02); Romano–Wolf StepM (L05)", lesson: "L02", series: 1 },
  { claim: "Most of my discoveries are real: the false discovery rate is at most q.", tools: "Benjamini–Hochberg and Benjamini–Yekutieli (L03); literature-wide hurdles (L06)", lesson: "L03", series: 2 },
  { claim: "The strategy I selected has a positive Sharpe ratio, after the search.", tools: "Probabilistic and deflated Sharpe ratios (L07)", lesson: "L07", series: 3 },
  { claim: "My selection process picks winners that hold up out of sample.", tools: "Probability of backtest overfitting via CSCV (L08)", lesson: "L08", series: 4 },
];
const FOOT = "The project assembles all five into one call: atlas.integrity.integrity_report (Atlas A8).";

function toolMap(el) {
  mountFigure(el, {
    draw(area, _s, width) {
      const wide = width >= 620;
      const pad = 10;
      const gap = wide ? 34 : 10;
      const charW = 6.7;
      const line = 15;
      const claimW = wide ? Math.floor((width - gap) * 0.56) : width;
      const toolW = wide ? width - gap - claimW : width - 24;
      const toolX = wide ? claimW + gap : 24;
      const rootLines = wrapLines(ROOT, Math.floor((width - 2 * pad) / charW));
      const rows = ROWS.map((r) => ({
        ...r,
        claimLines: wrapLines(r.claim, Math.floor((claimW - 2 * pad) / charW)),
        toolLines: wrapLines(`${r.tools} →`, Math.floor((toolW - 2 * pad) / charW)),
      }));
      const rootH = rootLines.length * line + 2 * pad;
      let y = rootH + 18;
      const layout = rows.map((r) => {
        const claimH = r.claimLines.length * line + 2 * pad;
        const toolH = r.toolLines.length * line + 2 * pad;
        const block = wide ? { claimY: y, toolY: y, h: Math.max(claimH, toolH) } : { claimY: y, toolY: y + claimH + 8, h: claimH + 8 + toolH };
        const out = { ...r, ...block, claimH: wide ? block.h : claimH, toolH: wide ? block.h : toolH };
        y += block.h + (wide ? 12 : 16);
        return out;
      });
      const footLines = wrapLines(FOOT, Math.floor((width - 2 * pad) / charW));
      const footY = y + 4;
      const height = footY + footLines.length * line + 2 * pad + 2;
      const svg = svgFrame(area, {
        width,
        height,
        title: "Which claim each tool in this module licenses",
        desc:
          "A map of the module. After a search over many strategies, five different claims are possible, each with its own tools: " +
          ROWS.map((r) => `${r.claim} Tools: ${r.tools}.`).join(" ") +
          " " +
          FOOT,
      });
      svg.append("rect").attr("class", "box").attr("x", 1).attr("y", 1).attr("width", width - 2).attr("height", rootH).attr("rx", 6);
      multilineText(svg, ROOT, { x: pad, y: pad + 11, chars: Math.floor((width - 2 * pad) / charW), lineHeight: line, cls: "title-text" });
      for (const r of layout) {
        const g = svg.append("g").attr("class", `series-${r.series}`);
        g.append("path").attr("class", "edge").attr("d", wide ? `M14,${rootH + 1} V${r.claimY + r.claimH / 2} H18` : `M12,${r.claimY - 14} V${r.claimY}`);
        g.append("rect").attr("class", "box accent").attr("x", wide ? 18 : 1).attr("y", r.claimY).attr("width", (wide ? claimW - 18 : width - 2)).attr("height", r.claimH).attr("rx", 6);
        multilineText(svg, r.claim, { x: (wide ? 18 : 1) + pad, y: r.claimY + pad + 11, chars: Math.floor((claimW - 2 * pad) / charW), lineHeight: line });
        const ax = wide ? claimW : 12;
        const ay = wide ? r.claimY + r.claimH / 2 : r.claimY + r.claimH;
        g.append("path").attr("class", "edge").attr("d", wide ? `M${ax},${ay} H${toolX - 6}` : `M${ax},${ay} V${r.toolY + r.toolH / 2} H${toolX - 6}`);
        g.append("path").attr("class", "arrowhead").attr("d", `M${toolX - 7},${(wide ? ay : r.toolY + r.toolH / 2) - 4} l7,4 l-7,4 z`);
        const link = svg.append("a").attr("href", `${r.lesson}.html`);
        link.append("title").text(`Go to ${r.lesson}`);
        link.append("rect").attr("class", "box").attr("x", toolX).attr("y", r.toolY).attr("width", toolW - 1).attr("height", r.toolH).attr("rx", 6);
        multilineText(link, r.toolLines.join(" "), { x: toolX + pad, y: r.toolY + pad + 11, chars: Math.floor((toolW - 2 * pad) / charW), lineHeight: line, cls: "link-text" });
      }
      svg.append("rect").attr("class", "box").attr("x", 1).attr("y", footY).attr("width", width - 2).attr("height", footLines.length * line + 2 * pad).attr("rx", 6).attr("style", "stroke-dasharray:5 4");
      multilineText(svg, FOOT, { x: pad, y: footY + pad + 11, chars: Math.floor((width - 2 * pad) / charW), lineHeight: line });
      return "";
    },
  });
}

const FIGURES = { "tool-map": toolMap };

export function drawFigures() {
  drawAll(FIGURES);
}
