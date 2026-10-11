// Entry point for every page: theme, citations, math, labs.

import { initTheme } from "./theme.js";
import { initCitations } from "./refs.js";
import { initMath } from "./math.js";
import { initLabs } from "./lab.js";

initTheme();
initMath();
initLabs();
initCitations().catch((error) => console.error(error));
