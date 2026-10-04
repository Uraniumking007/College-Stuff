import { chromium } from "playwright-core";
import fs from "fs";
import path from "path";
const OUT = path.resolve("Practicals/screenshots/remix");
const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browser = await chromium.launch({
  executablePath: chromePath,
  headless: false,
  args: ["--window-size=1440,1000"],
});
const page = await (await browser.newContext({ viewport: { width: 1440, height: 1000 } })).newPage();
page.on("dialog", d => { console.log("DIALOG", d.type(), d.message().slice(0,300)); d.accept().catch(()=>{}); });
page.on("console", m => { const t=m.text(); if (/remixd|localhost|error|websocket/i.test(t)) console.log("B", t.slice(0,240)); });
await page.goto("https://app.remix.live", { waitUntil: "domcontentloaded", timeout: 180000 });
await page.waitForSelector("[data-id='workspacesMenuDropdown']", { timeout: 60000 });
await page.waitForTimeout(2500);
// close top toasts
await page.locator("button").filter({ hasText: /^×$|Close/ }).first().click({ timeout: 1500 }).catch(()=>{});
const xs = page.locator("[data-id*='close' i], button[aria-label='Close']");
console.log("close btns", await xs.count());

await page.locator("[data-id='workspacesMenuDropdown']").click();
await page.waitForTimeout(800);
await page.screenshot({ path: path.join(OUT, "probe_menu.png") });
const menu = await page.evaluate(() => {
  const els = [...document.querySelectorAll("[data-id], [role='menuitem'], li, button, a, span")];
  return els.map(el => ({
    id: el.getAttribute("data-id"),
    t: (el.innerText||"").trim().replace(/\s+/g," ").slice(0,80),
  })).filter(x => /local|workspace|connect|remixd|create|new/i.test((x.id||"")+" "+x.t)).slice(0,80);
});
console.log("MENU", JSON.stringify(menu, null, 2));
fs.writeFileSync(path.join(OUT,"probe_menu.json"), JSON.stringify(menu,null,2));
await page.keyboard.press("Escape");

// plugins
await page.locator("[data-id='verticalIconsKindpluginManager']").click();
await page.waitForTimeout(800);
const search = page.locator("[data-id='pluginManagerComponentSearchInput']");
if (await search.count()) {
  await search.fill("RemixD");
  await page.waitForTimeout(600);
}
await page.screenshot({ path: path.join(OUT, "probe_plugins.png") });
const act = page.locator("[data-id='pluginManagerComponentActivateButtonremixd']");
console.log("activate count", await act.count());
if (await act.count()) {
  await act.first().click();
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(OUT, "probe_remixd_modal.png") });
  const txt = await page.evaluate(() => document.body.innerText.slice(0, 2500));
  fs.writeFileSync(path.join(OUT,"probe_modal.txt"), txt);
  console.log("---MODAL TEXT---");
  console.log(txt.slice(0,1500));
  // try connect
  const connect = page.getByRole("button", { name: /^Connect$/i });
  console.log("connect buttons", await connect.count());
  if (await connect.count()) {
    await connect.first().click();
    await page.waitForTimeout(4000);
    await page.screenshot({ path: path.join(OUT, "probe_after_connect.png") });
    const tree = await page.evaluate(() => {
      const el = document.querySelector("[data-id='filePanelFileExplorerTree']");
      return el ? el.innerText : "no tree";
    });
    console.log("TREE", tree.slice(0,800));
  }
}
await browser.close();
console.log("probe2 done");
