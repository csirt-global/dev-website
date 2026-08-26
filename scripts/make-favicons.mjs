/**
 * Regenerate every favicon from assets/images/logo-mark.svg.
 *
 * The icons that were here before used #fffb00, a brighter yellow than either
 * the old palette or the mark itself, so the browser tab never matched the
 * site. Rendering them from the one SVG means there is a single source for the
 * mark and the tab icon cannot drift from it again.
 *
 * Chrome does the rasterising, so this needs no image library. Run it after
 * changing the mark:
 *
 *   npm run favicons
 */
import { chromium } from "playwright";
import { readFileSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";

const SVG = "assets/images/logo-mark.svg";

// name, size, background. A null background keeps the transparent corners.
// apple-touch-icon must be opaque: iOS composites a transparent one onto white,
// and the mark sits on a black disc.
const ICONS = [
  ["static/favicon-16x16.png", 16, null],
  ["static/favicon-32x32.png", 32, null],
  ["static/android-chrome-192x192.png", 192, null],
  ["static/android-chrome-512x512.png", 512, null],
  ["static/mstile-150x150.png", 270, null],
  ["static/apple-touch-icon.png", 180, "#000000"],
];
const ICO = [16, 32, 48];

const svg = readFileSync(SVG);
const server = createServer((_, res) => {
  res.writeHead(200, { "Content-Type": "image/svg+xml" });
  res.end(svg);
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());

async function render(size, background) {
  const page = await browser.newPage({
    viewport: { width: size, height: size },
    deviceScaleFactor: 1,
  });
  await page.setContent(
    `<body style="margin:0;background:${background ?? "transparent"}">
       <img src="http://127.0.0.1:${port}/" width="${size}" height="${size}">
     </body>`,
    { waitUntil: "networkidle" }
  );
  const buf = await page.screenshot({ omitBackground: !background });
  await page.close();
  return buf;
}

for (const [path, size, bg] of ICONS) {
  writeFileSync(path, await render(size, bg));
  console.log(`  ${size}x${size}`.padEnd(12) + path);
}

// ICO container. Since Vista an .ico entry may hold a whole PNG, so the sizes
// above can be embedded directly rather than re-encoded as bitmaps.
const pngs = [];
for (const s of ICO) pngs.push([s, await render(s, null)]);

const header = Buffer.alloc(6);
header.writeUInt16LE(0, 0);           // reserved
header.writeUInt16LE(1, 2);           // 1 = icon
header.writeUInt16LE(pngs.length, 4);

let offset = 6 + 16 * pngs.length;
const dir = [];
for (const [s, buf] of pngs) {
  const e = Buffer.alloc(16);
  e.writeUInt8(s === 256 ? 0 : s, 0); // width
  e.writeUInt8(s === 256 ? 0 : s, 1); // height
  e.writeUInt8(0, 2);                 // palette
  e.writeUInt8(0, 3);                 // reserved
  e.writeUInt16LE(1, 4);              // colour planes
  e.writeUInt16LE(32, 6);             // bits per pixel
  e.writeUInt32LE(buf.length, 8);
  e.writeUInt32LE(offset, 12);
  offset += buf.length;
  dir.push(e);
}
writeFileSync("static/favicon.ico", Buffer.concat([header, ...dir, ...pngs.map(p => p[1])]));
console.log(`  ${ICO.join("/")}      static/favicon.ico`);

await browser.close();
server.close();
