/**
 * Compare the Hugo rebuild against the current site (with our merged PRs).
 *
 *   REFERENCE  http://127.0.0.1:8899   the live site plus PRs #52-#59
 *   NEW        http://127.0.0.1:1313   this rebuild
 *
 * Usage:
 *   node scripts/compare.mjs                 measure both, print a table
 *   node scripts/compare.mjs --shots DIR     also write side-by-side screenshots
 *
 * Requires playwright installed in the scratchpad and Google Chrome present:
 * Playwright's own cached browsers are stale relative to the installed version,
 * so we drive the installed Chrome via channel: "chrome".
 */
import { chromium } from "playwright";

const REF = "http://127.0.0.1:8899";
const NEW = "http://127.0.0.1:1313";

// path on the reference -> path on the new site
const PAGES = [
  ["/", "/"],
  ["/cases/", "/cases/"],
  ["/cases/CG-2024-00001/", "/cases/CG-2024-00001/"],
  ["/projects/", "/projects/"],
  ["/projects/pgu/", "/projects/pgu/"],
  ["/projects/pgngo/", "/projects/pgngo/"],
];

const WIDTHS = [390, 768, 1440];

async function measure(page, url) {
  const failed = [];
  page.on("response", r => {
    if (r.status() >= 400 && !r.url().includes("livereload")) failed.push(r.status() + " " + r.url().split("/").pop());
  });
  await page.goto(url, { waitUntil: "networkidle" }).catch(() => {});
  await page.waitForTimeout(500);
  return {
    ...(await page.evaluate(() => {
      const txt = document.body.innerText.replace(/\s+/g, " ").trim();
      const heads = [...document.querySelectorAll("h1,h2")].map(h => h.textContent.trim()).filter(Boolean);
      const para = document.querySelector("main p, p");
      const socials = [...document.querySelectorAll("ul[role=list] a svg")];
      return {
        words: txt.split(" ").length,
        headings: heads,
        bodySize: para ? getComputedStyle(para).fontSize : "?",
        socialColours: [...new Set(socials.map(s => getComputedStyle(s).color))],
        socialCount: socials.length,
        hscroll: document.documentElement.scrollWidth > window.innerWidth + 1,
        height: document.body.scrollHeight,
        extTotal: [...document.querySelectorAll('a[href^="http"]')].filter(a => !a.href.includes(location.host)).length,
        extNewTab: [...document.querySelectorAll('a[href^="http"]')].filter(a => !a.href.includes(location.host) && a.target === "_blank").length,
      };
    })),
    failed,
  };
}

const shotsIdx = process.argv.indexOf("--shots");
const shotsDir = shotsIdx > -1 ? process.argv[shotsIdx + 1] : null;

const browser = await chromium.launch({ channel: "chrome" });
let problems = 0;

console.log("page                     side  body   social            h-scroll  ext-newtab  failed-req");
console.log("-".repeat(96));

for (const [refPath, newPath] of PAGES) {
  for (const [label, base, path] of [["ref", REF, refPath], ["new", NEW, newPath]]) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const m = await measure(page, base + path);
    const bad = m.hscroll || m.failed.length || (m.extTotal && m.extNewTab < m.extTotal);
    if (label === "new" && bad) problems++;
    console.log(
      `  ${newPath.padEnd(24)}${label.padEnd(6)}${String(m.bodySize).padEnd(7)}` +
      `${(m.socialColours[0] || "-").padEnd(18)}${String(m.hscroll).padEnd(10)}` +
      `${m.extNewTab}/${String(m.extTotal).padEnd(10)}${m.failed.length ? m.failed.join(",") : "none"}`
    );
    if (shotsDir) {
      await page.screenshot({ path: `${shotsDir}/${label}-${newPath.replace(/\W+/g, "_")}.png`, fullPage: false });
    }
    await page.close();
  }
}

// horizontal-scroll sweep on the new site only
console.log("\nresponsive sweep (new site)");
const hs = [];
for (const [, newPath] of PAGES) {
  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    await page.goto(NEW + newPath, { waitUntil: "domcontentloaded" }).catch(() => {});
    await page.waitForTimeout(300);
    if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) {
      hs.push(`${newPath}@${w}`);
    }
    await page.close();
  }
}
console.log(hs.length ? `  H-SCROLL: ${hs.join(", ")}` : `  clean across ${PAGES.length} pages x ${WIDTHS.length} widths`);

await browser.close();
process.exit(problems || hs.length ? 1 : 0);
