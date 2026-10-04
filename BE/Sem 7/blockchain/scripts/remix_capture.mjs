import { chromium } from "playwright-core";
import fs from "fs";
import path from "path";

const ROOT = path.resolve("contracts");
const OUT = path.resolve("Practicals/screenshots/remix");
fs.mkdirSync(OUT, { recursive: true });
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const jobs = [
  { p: 6, file: "SimpleStorage.sol", name: "SimpleStorage", ctor: null, calls: [{ m: "set", a: ["42"] }, { m: "get", a: [] }] },
  { p: 7, file: "DataTypesDemo.sol", name: "DataTypesDemo", ctor: null, calls: [{ m: "readAll", a: [] }] },
  { p: 8, file: "Counter.sol", name: "Counter", ctor: "0", calls: [{ m: "increment", a: [] }, { m: "getCount", a: [] }] },
  { p: 9, file: "Voting.sol", name: "Voting", ctor: null, calls: [{ m: "addCandidate", a: ["Alice"] }, { m: "addCandidate", a: ["Bob"] }, { m: "vote", a: ["1"] }, { m: "getVotes", a: ["1"] }] },
  { p: 10, file: "SimpleWallet.sol", name: "SimpleWallet", ctor: null, value: "1", unit: "ether", calls: [{ m: "deposit", a: [], value: "1", unit: "ether" }, { m: "getBalance", a: [], value: "0", unit: "wei" }] },
  { p: 11, file: "StudentRecordSystem.sol", name: "StudentRecordSystem", ctor: "1000000000000000", value: "1000000000000000", unit: "wei", calls: [{ m: "registerStudent", a: ["Bhavesh", "IT"], value: "1000000000000000", unit: "wei" }, { m: "updateMarks", a: ["1", "85"], value: "0", unit: "wei" }, { m: "getStudent", a: ["1"] }] },
];

const browser = await chromium.launch({
  executablePath: CHROME, headless: false, args: ["--window-size=1500,1000"],
});
let context;
let page;
const log = (...a) => console.log("STEP", ...a);
async function shot(name) { await page.screenshot({ path: path.join(OUT, name + ".png") }); log("shot", name); }
async function modals() {
  await page.evaluate(() => document.querySelectorAll("#nudge-widget-container,.nudge-modal-backdrop").forEach((n) => n.remove()));
  for (const name of ["Accept", "Save Preferences"]) {
    const b = page.getByRole("button", { name, exact: true });
    if (await b.count()) await b.first().click({ timeout: 2000 }).catch(() => {});
  }
}
function sideButtons() { return page.locator("[data-id='remixIdeSidePanel'] button"); }

async function openCode(source) {
  const b64 = Buffer.from(source).toString("base64");
  await page.goto("https://app.remix.live/?#activate=solidity,udapp&theme=Dark&code=" + b64, { waitUntil: "domcontentloaded", timeout: 180000 });
  await page.waitForSelector("[data-id='verticalIconsKindsolidity']", { timeout: 90000 });
  await page.waitForTimeout(2500);
  await modals();
  await page.locator("[data-id='close_home']").click({ force: true, timeout: 1500 }).catch(() => {});
  await page.locator("[data-id='hideRightSidePanel']").click({ force: true, timeout: 1500 }).catch(() => {});
  await page.waitForTimeout(500);
}

async function compile(n) {
  const btn = page.locator("button").filter({ hasText: /Compile.*sol/i }).first();
  log("compile count", await btn.count());
  if (await btn.count()) await btn.evaluate((el) => el.click());
  await page.waitForTimeout(4500);
  const width = await page.evaluate(() => {
    const el = document.querySelector("[data-id='remixIdeSidePanel']");
    return el ? Math.round(el.getBoundingClientRect().width) : 0;
  });
  log("panel", width);
  if (width < 100) {
    await page.locator("[data-id='verticalIconsKindsolidity']").click({ force: true });
    await page.waitForTimeout(800);
  }
  const text = await page.locator("[data-id='remixIdeSidePanel']").innerText().catch(() => "");
  await shot(`p${n}_compile`);
  log("compile", /successful/i.test(text) ? "OK" : text.replace(/\s+/g, " ").slice(0, 180));
}

async function setValue(v, unit) {
  if (v == null) return;
  await page.evaluate(({ v, unit }) => {
    const setNative = (el, value) => {
      const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
      proto.set.call(el, value);
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    };
    const selects = [...document.querySelectorAll("select")];
    const sel = selects.find((s) => [...s.options].some((o) => /wei|gwei|ether/i.test(o.textContent)));
    if (!sel) return "no sel";
    if (unit) {
      const opt = [...sel.options].find((o) => new RegExp(unit, "i").test(o.textContent));
      if (opt) { sel.value = opt.value; sel.dispatchEvent(new Event("change", { bubbles: true })); }
    }
    let inp = null;
    if (sel) {
      const parent = sel.closest("div");
      inp = parent ? parent.querySelector("input") : null;
    }
    if (!inp) {
      const root = document.querySelector("[data-id='remixIdeSidePanel']") || document.body;
      const lab = [...root.querySelectorAll("div, span, label")].find((el) => el.childNodes.length && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim() === "Value"));
      if (lab) {
        const box = lab.parentElement || lab;
        inp = box.querySelector("input") || box.parentElement?.querySelector("input");
      }
    }
    if (inp) setNative(inp, String(v));
    return inp ? "filled" : "no inp";
  }, { v, unit }).then((r) => log("value", r, v, unit));
}

async function deploy(job) {
  await page.locator("[data-id='verticalIconsKindudapp']").click({ force: true });
  await page.waitForTimeout(800);
  const card = page.locator("[data-id='remixIdeSidePanel'] button:visible").filter({ hasText: /^Compile$/ });
  if (await card.count()) {
    log("card compile");
    await card.first().click({ timeout: 5000 }).catch((e) => log("card", e.message.split("\n")[0]));
    await page.waitForTimeout(4000);
  }
  if (job.ctor != null) {
    const r = await page.evaluate((ctor) => {
      const root = document.querySelector("[data-id='remixIdeSidePanel']");
      const setNative = (el, value) => {
        const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
        proto.set.call(el, value);
        el.dispatchEvent(new Event("input", { bubbles: true }));
        el.dispatchEvent(new Event("change", { bubbles: true }));
      };
      const inputs = [...root.querySelectorAll("input")].filter((el) => {
        const box = el.getBoundingClientRect();
        const blob = (el.id || "") + (el.placeholder || "") + (el.getAttribute("data-id") || "");
        return box.width > 0 && box.height > 0 && el.type !== "checkbox" && el.type !== "file" && !/search|value|gas/i.test(blob);
      });
      if (!inputs.length) return "none visible";
      setNative(inputs[0], ctor);
      return "filled " + (inputs[0].placeholder || inputs[0].id || "input");
    }, String(job.ctor));
    log("ctor", r);
  }
  await setValue(job.value, job.unit);
  const dep = sideButtons().filter({ hasText: /^Deploy$/ });
  log("deploy btns", await dep.count());
  if (await dep.count()) await dep.last().evaluate((el) => el.click());
  await page.waitForTimeout(2800);
  await shot(`p${job.p}_deploy`);
}

async function callMethod(c) {
  const trans = await page.locator("button:visible").filter({ hasText: /^Transact$|^Call$/ }).count();
  log("tx buttons", trans);
  if (!trans) {
    await page.getByText("Deployed contracts").first().click({ force: true, timeout: 2500 }).catch(() => {});
    await page.waitForTimeout(400);
  }
  await setValue(c.value, c.unit);
  const result = await page.evaluate(({ method, args }) => {
    const root = document.querySelector("[data-id='remixIdeSidePanel']");
    if (!root) return "no root";
    const setNative = (el, value) => {
      const proto = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
      proto.set.call(el, String(value));
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    };
    const all = [...root.querySelectorAll("*")];
    const labels = all.filter((el) => {
      const raw = (el.innerText || "").trim();
      return (raw === method || raw.startsWith(method + " ") || raw.startsWith(method + "(")) && raw.length < 40;
    }).sort((a, b) => a.innerText.length - b.innerText.length);
    const label = labels[0];
    if (!label) return "no label";
    const li = all.indexOf(label);
    const kind = args.length ? "transact" : "call";
    const buttons = all.filter((el) => el.tagName === "BUTTON" && el.innerText.trim().toLowerCase() === kind && all.indexOf(el) > li);
    const btn = buttons[0];
    if (!btn) return "no btn after " + label.innerText.slice(0, 30);
    const bi = all.indexOf(btn);
    const inputs = all.filter((el) => el.tagName === "INPUT" && all.indexOf(el) > li && all.indexOf(el) < bi && !/file|checkbox/i.test(el.type || ""));
    args.forEach((a, idx) => { if (inputs[idx]) setNative(inputs[idx], a); });
    btn.click();
    return "clicked " + btn.innerText.trim() + " n=" + inputs.length;
  }, { method: c.m, args: c.a });
  log("invoke", c.m, result);
  await page.waitForTimeout(1400);
  return String(result).startsWith("clicked");
}

for (const job of jobs) {
  if (job.p < 10) continue;
  log("JOB", job.name);
  context = await browser.newContext({ viewport: { width: 1500, height: 1000 } });
  page = await context.newPage();
  page.setDefaultTimeout(15000);
  page.on("dialog", (d) => d.accept().catch(() => {}));
  try {
    const src = fs.readFileSync(path.join(ROOT, job.file), "utf8");
    await openCode(src);
    const loaded = await page.evaluate((n) => (window.monaco?.editor?.getModels?.() || []).some((m) => (m.getValue() || "").includes("contract " + n)), job.name);
    log("loaded", job.name, loaded);
    await shot(`p${job.p}_code`);
    await compile(job.p);
    await deploy(job);
    let any = false;
    for (const c of job.calls) {
      const ok = await callMethod(c);
      log("call", c.m, ok);
      if (ok) any = true;
    }
    const side = await page.locator("[data-id='remixIdeSidePanel']").innerText().catch(() => "");
    fs.writeFileSync(path.join(OUT, `side_p${job.p}.txt`), side.slice(0, 2500));
    await shot(any ? `p${job.p}_interact` : `p${job.p}_interact_missing`);
  } catch (e) {
    log("FAIL", job.name, e.message.split("\n")[0]);
    await shot(`p${job.p}_error`).catch(() => {});
  }
  await context.close().catch(() => {});
}
await browser.close();
log("DONE");
