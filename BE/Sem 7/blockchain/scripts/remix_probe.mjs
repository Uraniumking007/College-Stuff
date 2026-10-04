import { chromium } from "playwright-core";
import fs from "fs";
import path from "path";

const OUT = path.resolve("Practicals/screenshots/remix");
fs.mkdirSync(OUT, { recursive: true });
const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const browser = await chromium.launch({
  executablePath: chromePath,
  headless: false,
  args: ["--window-size=1440,960", "--disable-features=Translate"],
});
const context = await browser.newContext({ viewport: { width: 1440, height: 960 } });
const page = await context.newPage();
page.setDefaultTimeout(20000);
page.on("dialog", (d) => { console.log("DIALOG", d.message()); d.accept().catch(() => {}); });

console.log("goto");
await page.goto("https://app.remix.live", { waitUntil: "domcontentloaded", timeout: 180000 });
await page.waitForTimeout(14000);
console.log("url", page.url());
await page.screenshot({ path: path.join(OUT, "probe_1.png") });

async function dump(name) {
  const data = await page.evaluate(() => {
    const items = [];
    const nodes = document.querySelectorAll("button, a, [role='button'], [data-id], [title], [aria-label], span, div");
    let n = 0;
    for (const el of nodes) {
      const t = (el.innerText || "").trim().replace(/\s+/g, " ").slice(0, 90);
      const id = el.getAttribute("data-id");
      const title = el.getAttribute("title");
      const aria = el.getAttribute("aria-label");
      if (!id && !title && !aria && (!t || t.length > 70 || el.children.length > 3)) continue;
      if (!id && !title && !aria && !t) continue;
      items.push({ tag: el.tagName, id, title, aria, t });
      if (++n > 800) break;
    }
    return { title: document.title, items };
  });
  fs.writeFileSync(path.join(OUT, name), JSON.stringify({ url: page.url(), ...data }, null, 2));
  console.log("dumped", name, data.items.length);
}

// dismiss banners
for (const sel of [
  "button[aria-label='Close']",
  "button[aria-label='close']",
  "button:has-text('×')",
]) {
  const loc = page.locator(sel);
  const c = await loc.count();
  for (let i = 0; i < Math.min(c, 6); i++) {
    try { await loc.nth(i).click({ timeout: 800 }); } catch {}
  }
}
await page.keyboard.press("Escape").catch(() => {});
await page.waitForTimeout(800);
await page.screenshot({ path: path.join(OUT, "probe_2.png") });
await dump("probe_dom.json");

// click workspace name if present
const ws = page.locator("text=default_workspace").first();
if (await ws.count()) {
  await ws.click().catch((e) => console.log("ws click", e.message));
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(OUT, "probe_ws.png") });
  await dump("probe_ws.json");
}

// try gear / menu near workspace
const gear = page.locator("[title*='workspace' i], [aria-label*='workspace' i], [data-id*='workspace' i]").first();
console.log("gear count", await page.locator("[title*='workspace' i], [aria-label*='workspace' i], [data-id*='workspace' i]").count());

await browser.close();
console.log("probe done");
