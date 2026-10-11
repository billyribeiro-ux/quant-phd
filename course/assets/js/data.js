// Loads the site's generated data (published by tools/build_site.py) once per page.

const cache = new Map();

export function dataUrl(name) {
  return new URL(`../data/${name}`, import.meta.url);
}

export function loadJSON(name) {
  if (!cache.has(name)) {
    cache.set(
      name,
      fetch(dataUrl(name)).then((response) => {
        if (!response.ok) throw new Error(`Cannot load ${name}: HTTP ${response.status}. Run tools/build_site.py.`);
        return response.json();
      }),
    );
  }
  return cache.get(name);
}

/** Create an element: h("a", {href: "#x", class: "chip"}, "text", childNode). Text is never parsed as HTML. */
export function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") el.className = value;
    else if (key === "dataset") Object.assign(el.dataset, value);
    else if (key.startsWith("on") && typeof value === "function") el.addEventListener(key.slice(2), value);
    else el.setAttribute(key, value === true ? "" : String(value));
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return el;
}

export const fmt = new Intl.NumberFormat("en-US");
