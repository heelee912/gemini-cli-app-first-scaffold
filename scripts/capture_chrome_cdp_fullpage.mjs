#!/usr/bin/env node
// Capture full-page desktop and mobile screenshots through Chrome DevTools Protocol.

import { mkdir, rm, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import path from "node:path";

const CHROME_CANDIDATES = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
];

function usage() {
  throw new Error("Usage: node scripts/capture_chrome_cdp_fullpage.mjs <url> <out-dir> [--click-text <button text>] [--settle-ms <ms>]");
}

async function exists(file) {
  try {
    await import("node:fs/promises").then((fs) => fs.access(file));
    return true;
  } catch {
    return false;
  }
}

async function findChrome() {
  for (const candidate of CHROME_CANDIDATES) {
    if (await exists(candidate)) return candidate;
  }
  throw new Error("No supported Chrome or Edge executable found.");
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function waitForJson(url, timeoutMs = 5000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch {
      // Chrome is still starting.
    }
    await sleep(100);
  }
  throw new Error(`Timed out waiting for ${url}`);
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  const opened = new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      pending.get(message.id)(message);
      pending.delete(message.id);
    }
  };
  const send = async (method, params = {}) => {
    await opened;
    return await new Promise((resolve) => {
      const id = nextId++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  };
  return { ws, send };
}

function parseArgs(argv) {
  const url = argv[2];
  const outDir = path.resolve(argv[3] || "");
  if (!url || !outDir) usage();
  const clickIndex = argv.indexOf("--click-text");
  const settleIndex = argv.indexOf("--settle-ms");
  return {
    url,
    outDir,
    clickText: clickIndex >= 0 ? argv[clickIndex + 1] : "",
    settleMs: settleIndex >= 0 ? Number.parseInt(argv[settleIndex + 1], 10) : 5000,
  };
}

async function clickTextIfRequested(send, clickText) {
  if (!clickText) return;
  const expression = `(() => {
    const wanted = ${JSON.stringify(clickText)}.trim().toLowerCase();
    const candidates = [...document.querySelectorAll('button, a, [role="button"], [tabindex]')];
    const target = candidates.find((el) => (el.innerText || el.textContent || '').trim().toLowerCase().includes(wanted));
    if (!target) return { clicked: false, reason: 'not found', wanted };
    target.click();
    return { clicked: true, text: (target.innerText || target.textContent || '').trim().slice(0, 200) };
  })()`;
  await send("Runtime.evaluate", { expression, returnByValue: true });
}

async function capture({ chrome, url, outDir, name, width, height, mobile, clickText, settleMs }) {
  const port = 9400 + Math.floor(Math.random() * 1000);
  const profile = path.join(outDir, `${name}-profile`);
  await rm(profile, { recursive: true, force: true });
  await mkdir(profile, { recursive: true });
  const chromeProcess = spawn(chrome, [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    `--user-data-dir=${profile}`,
    `--remote-debugging-port=${port}`,
    `--window-size=${width},${height}`,
    "about:blank",
  ], { stdio: ["ignore", "ignore", "pipe"] });

  try {
    await waitForJson(`http://127.0.0.1:${port}/json/version`);
    const created = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(url)}`, { method: "PUT" }).then((r) => r.json());
    const cdp = connect(created.webSocketDebuggerUrl);
    await cdp.send("Runtime.enable");
    await cdp.send("Page.enable");
    if (mobile) {
      await cdp.send("Emulation.setDeviceMetricsOverride", {
        width,
        height,
        deviceScaleFactor: 2,
        mobile: true,
      });
      await cdp.send("Emulation.setTouchEmulationEnabled", { enabled: true });
    }
    await sleep(settleMs);
    await clickTextIfRequested(cdp.send, clickText);
    await sleep(settleMs);
    const metrics = await cdp.send("Page.getLayoutMetrics");
    const contentSize = metrics.result?.contentSize || metrics.result?.cssContentSize || { x: 0, y: 0, width, height };
    const shot = await cdp.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: true,
      clip: {
        x: contentSize.x || 0,
        y: contentSize.y || 0,
        width: Math.max(contentSize.width || width, width),
        height: Math.max(contentSize.height || height, height),
        scale: 1,
      },
    });
    const file = path.join(outDir, `${name}.png`);
    await writeFile(file, Buffer.from(shot.result.data, "base64"));
    const text = await cdp.send("Runtime.evaluate", {
      expression: "document.body ? document.body.innerText.slice(0, 1000) : ''",
      returnByValue: true,
    });
    cdp.ws.close();
    return {
      name,
      file,
      bytes: Buffer.byteLength(shot.result.data, "base64"),
      contentSize,
      textStart: text.result?.result?.value || "",
    };
  } finally {
    chromeProcess.kill();
  }
}

async function main() {
  const { url, outDir, clickText, settleMs } = parseArgs(process.argv);
  if (!url.startsWith("http://127.0.0.1") && !url.startsWith("http://localhost") && !url.startsWith("file:///")) {
    throw new Error("Only local HTTP and file URLs are supported.");
  }
  await mkdir(outDir, { recursive: true });
  const chrome = await findChrome();
  const captures = [
    await capture({ chrome, url, outDir, name: "desktop-fullpage", width: 1365, height: 768, mobile: false, clickText, settleMs }),
    await capture({ chrome, url, outDir, name: "mobile-fullpage", width: 390, height: 844, mobile: true, clickText, settleMs }),
  ];
  const manifest = { url, chrome, clickText, settleMs, captures };
  await writeFile(path.join(outDir, "capture-chrome-cdp-fullpage.json"), JSON.stringify(manifest, null, 2));
  console.log(JSON.stringify(manifest, null, 2));
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
