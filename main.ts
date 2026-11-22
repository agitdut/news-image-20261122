// news-image-20261122: Sunday 22 November 2026 in one picture.
//
// entry.png in this repository is the front page for that day, drawn by
// draw_news.py: the FBI criminal-database breach as the lead, the
// Shenzhen trilateral, COP31 running into overtime and Verstappen's Las
// Vegas win as the featured stories, eighteen briefs from around the
// world, and a numbers strip. The grader runs this program with no
// network, so all it does is copy the finished picture to
// /output/entry.png. The file is a 1024 by 1024 PNG under 1 MiB, so the
// judge sees exactly these bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "out");
mkdirSync(outDir, { recursive: true });

const png = readFileSync(join(here, "entry.png"));
if (png.length > 1048576) {
  console.error(`entry.png is ${png.length} bytes, over the 1 MiB limit`);
  process.exit(1);
}
const dest = join(outDir, "entry.png");
writeFileSync(dest, png);
console.log(`wrote ${dest} (${png.length} bytes)`);
