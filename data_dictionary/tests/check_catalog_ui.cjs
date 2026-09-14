// Optional browser check. Supply a local Playwright module path as argv[2].
const {chromium} = require(process.argv[2] || 'playwright');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(path.resolve(__dirname, '../reports/catalog.html')).href);
    assert.equal(await page.locator('#count').textContent(), '111 matching catalog records');
    await page.locator('#scope').selectOption('Influenza challenge search');
    await page.locator('#eligibility').selectOption('challenge');
    assert.equal(await page.locator('#count').textContent(), '26 matching catalog records');
    await page.locator('#search').fill('GSE73072');
    assert.equal(await page.locator('#rows tr').count(), 1);
    assert.match(await page.locator('#rows').innerText(), /GSE73072/);
    await page.locator('#search').fill('<script>alert(1)</script>');
    assert.equal(await page.locator('#rows tr').count(), 0);
    await page.locator('#search').fill('');
    await page.locator('#scope').selectOption('');
    await page.locator('#eligibility').selectOption('');
    await page.screenshot({path: '/tmp/ikhis-dictionary-desktop.png', fullPage: false});
    const mobile = await browser.newPage({viewport: {width: 390, height: 844}});
    await mobile.goto(pathToFileURL(path.resolve(__dirname, '../reports/catalog.html')).href);
    await mobile.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await mobile.screenshot({path: '/tmp/ikhis-dictionary-mobile.png', fullPage: false});
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({status: 'ok', checks: ['initial render', 'collection and eligibility filters', 'accession search', 'literal search input', 'desktop and mobile render'], page_errors: errors}));
  } finally { await browser.close(); }
})().catch(e => {console.error(e.message);process.exitCode = 1;});
