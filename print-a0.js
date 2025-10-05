const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const file = 'file:///f:/Coding/Projects/showcase2025-poster/poster.html';

  // Use a large viewport and a deviceScaleFactor that matches Chromium's print rasterization
  await page.setViewport({ width: 1600, height: 2400, deviceScaleFactor: 2 });

  await page.goto(file, { waitUntil: 'networkidle0' });

  // Tell Chromium to apply print styles (@media print)
  await page.emulateMediaType('print');

  // Give fonts and print styles a moment to settle (portable sleep)
  await new Promise(resolve => setTimeout(resolve, 500));

  await page.pdf({
    path: 'poster-A0.pdf',
    printBackground: true,
    preferCSSPageSize: true, // prefer @page when possible
    // explicit size fallback/enforcer (guarantee A0 if preferCSSPageSize is ignored)
    width: '841mm',
    height: '1189mm',
    scale: 1
  });

  await browser.close();
})();