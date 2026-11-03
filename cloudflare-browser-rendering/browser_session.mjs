import { chromium } from "playwright-core";
const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
const token = process.env.CLOUDFLARE_API_TOKEN;
if (!/^[a-f0-9]{32}$/i.test(accountId ?? "") || !token) throw new Error("Configure Cloudflare locally");
const browser = await chromium.connectOverCDP(
  `wss://api.cloudflare.com/client/v4/accounts/${accountId}/browser-run/devtools/browser`,
  { headers: { Authorization: `Bearer ${token}` }, timeout: 30000 }
);
try {
  const context = browser.contexts()[0] ?? await browser.newContext();
  const page = context.pages()[0] ?? await context.newPage();
  await page.goto("https://developers.cloudflare.com/browser-run/", { waitUntil: "domcontentloaded", timeout: 30000 });
  await page.locator("main").waitFor({ timeout: 30000 });
  console.log((await page.locator("main").innerText()).slice(0, 1000));
} finally { await browser.close(); }
