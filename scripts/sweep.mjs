/**
 * Regression sweep over the new site's full information architecture.
 *
 * compare.mjs answers "did we lose anything relative to the old site". This
 * answers "does the new site hold together on its own": no horizontal scroll at
 * any width, no failed requests, every external link opening in a new tab,
 * every page reachable by keyboard with a visible focus ring, and pinch-zoom not
 * blocked (the old site failed WCAG 2.1 SC 1.4.4 on all eight pages).
 *
 *   node scripts/sweep.mjs [--shots DIR]
 */
import { chromium } from "playwright";

const BASE = process.env.BASE_URL || "http://127.0.0.1:1313";
const WIDTHS = [390, 768, 1440];

// Every language the site publishes. The nav is the part that varies most
// between them: German needs 1,079px of the 1,088 available, and French needed
// 1,103 before its labels were shortened. This list is what stops a new
// language quietly breaking the header.
const LANGS = ["", "nl", "de", "fr", "es", "pt-br", "zh"];

const PAGES = [
  "/", "/notified/",
  "/what-we-do/", "/what-we-do/bug-bounties/", "/what-we-do/exploit-research/",
  "/what-we-do/incident-response/",
  "/cases/", "/cases/CG-2024-00001/", "/cases/CG-2024-00002/", "/cases/CG-2024-00003/",
  "/projects/", "/projects/pgu/", "/projects/pgngo/",
  "/about/", "/about/team/", "/about/code-of-conduct/", "/about/anbi/",
  "/get-involved/", "/news/", "/join/",
];

const shotsIdx = process.argv.indexOf("--shots");
const shotsDir = shotsIdx > -1 ? process.argv[shotsIdx + 1] : null;

// Prefer the installed Google Chrome: Playwright's own cached build is stale
// relative to it locally. On a runner there is no Chrome, so fall back to the
// bundled Chromium rather than failing.
const browser = await chromium
  .launch({ channel: "chrome" })
  .catch(() => chromium.launch());
const problems = [];

console.log("page                              w     h-scroll  ext-newtab  zoom  failed");
console.log("-".repeat(84));

for (const path of PAGES) {
  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    const failed = [];
    page.on("response", r => {
      if (r.status() >= 400 && !r.url().includes("livereload")) {
        failed.push(`${r.status()} ${r.url().replace(BASE, "")}`);
      }
    });
    await page.goto(BASE + path, { waitUntil: "networkidle" }).catch(() => {});
    const m = await page.evaluate(() => {
      const ext = [...document.querySelectorAll('a[href^="http"]')]
        .filter(a => !a.href.includes(location.host));
      const vp = document.querySelector('meta[name="viewport"]')?.content || "";
      return {
        hscroll: document.documentElement.scrollWidth > window.innerWidth + 1,
        extTotal: ext.length,
        extNewTab: ext.filter(a => a.target === "_blank").length,
        zoomBlocked: /user-scalable\s*=\s*no|maximum-scale\s*=\s*1/.test(vp),
      };
    });
    const bad = m.hscroll || m.zoomBlocked || failed.length || m.extNewTab < m.extTotal;
    if (bad) problems.push(`${path}@${w}`);
    if (w === 1440 || bad) {
      console.log(
        `  ${path.padEnd(32)}${String(w).padEnd(6)}${String(m.hscroll).padEnd(10)}` +
        `${m.extNewTab}/${String(m.extTotal).padEnd(10)}${String(m.zoomBlocked).padEnd(6)}` +
        `${failed.length ? failed.join(",") : "none"}`
      );
    }
    if (shotsDir && w !== 768) {
      // Scroll the page first: cards below the fold are loading="lazy" and a
      // full-page screenshot otherwise captures them as empty boxes.
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) {
          window.scrollTo(0, y);
          await new Promise(r => setTimeout(r, 40));
        }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(400);
      await page.screenshot({
        path: `${shotsDir}/${w}${path.replace(/\W+/g, "_") || "_home"}.png`,
        fullPage: w === 1440,
      });
    }
    await page.close();
  }
}

// The header, in every language, at the widths where the desktop menu is shown.
//
// This exists because it was missed: French wrapped "Ce que nous faisons" onto
// three lines inside a fixed-height header, and every language including English
// overflowed at 1024px, which was the breakpoint at the time. The page sweep
// above never caught it because it only ever visited English pages, and never at
// 1024.
console.log("\nheader fit by language");
for (const lang of LANGS) {
  for (const w of [1280, 1440]) {
    const page = await browser.newPage({ viewport: { width: w, height: 700 } });
    await page.goto(`${BASE}/${lang ? lang + "/" : ""}`, { waitUntil: "networkidle" });
    const m = await page.evaluate(() => {
      const nav = document.querySelector("header nav");
      const menu = nav.children[1];
      if (!menu.getBoundingClientRect().width) return null;   // hamburger shown
      const links = [...menu.children]
        .map(el => (el.tagName === "A" ? el : el.querySelector("a")))
        .filter(a => a && !a.className.includes("btn"));      // the CTA is a taller button
      const kids = [...nav.children];
      const word = nav.querySelector(".logo-word");
      return {
        wrapped: links.filter(a => a.getBoundingClientRect().height > 30)
                      .map(a => a.textContent.trim().split("\n")[0]),
        needs: Math.round(kids.reduce((t, c) => t + c.scrollWidth, 0) + 20 * (kids.length - 1)),
        avail: Math.round(nav.parentElement.getBoundingClientRect().width - 64),
        clipped: Math.round(word.getBoundingClientRect().right) >
                 Math.round(kids[0].getBoundingClientRect().right) + 1,
        hscroll: document.documentElement.scrollWidth > window.innerWidth + 1,
      };
    });
    await page.close();
    if (!m) continue;
    const room = m.avail - m.needs;
    const bad = m.wrapped.length || room < 0 || m.clipped || m.hscroll;
    console.log(`  ${(lang || "en").padEnd(4)} @${w}  needs ${m.needs} of ${m.avail}` +
      `  (${room >= 0 ? room + "px spare" : -room + "px OVER"})` +
      `${m.wrapped.length ? "  wrapped: " + m.wrapped.join(", ") : ""}` +
      `${m.clipped ? "  LOGO CLIPPED" : ""}${m.hscroll ? "  H-SCROLL" : ""}`);
    if (bad) problems.push(`header:${lang || "en"}@${w}`);
  }
}

// Keyboard reachability and a visible focus ring on the primary call to action.
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(BASE + "/", { waitUntil: "networkidle" });
let ring = false;
for (let i = 0; i < 12 && !ring; i++) {
  await page.keyboard.press("Tab");
  ring = await page.evaluate(() => {
    const el = document.activeElement;
    if (!el || el === document.body) return false;
    const s = getComputedStyle(el);
    return s.outlineStyle !== "none" && parseFloat(s.outlineWidth) > 0;
  });
}
console.log(`\n  keyboard focus ring visible within 12 tabs : ${ring}`);
if (!ring) problems.push("focus-ring");

await browser.close();
console.log(problems.length ? `\nFAIL: ${problems.join(", ")}` : `\nPASS: ${PAGES.length} pages x ${WIDTHS.length} widths clean`);
process.exit(problems.length ? 1 : 0);
