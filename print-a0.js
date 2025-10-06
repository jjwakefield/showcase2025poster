const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Resolve poster.html in the same directory as this script
  const posterPath = path.resolve(__dirname, 'poster.html');
  const filePath = 'file://' + posterPath;

  if (!fs.existsSync(posterPath)) {
    console.error('poster.html not found at', posterPath);
    await browser.close();
    process.exit(1);
  }

  // Use a large viewport and a deviceScaleFactor that matches Chromium's print rasterization
  await page.setViewport({ width: 1600, height: 2400, deviceScaleFactor: 2 });

  await page.goto(filePath, { waitUntil: 'networkidle0' });

  // Tell Chromium to apply print styles (@media print)
  await page.emulateMediaType('print');

  // Give fonts and print styles a moment to settle (portable sleep)
  await new Promise(resolve => setTimeout(resolve, 500));

  await page.pdf({
    path: 'poster-A0.pdf',
    printBackground: true,
    preferCSSPageSize: true,
    width: '841mm',
    height: '1189mm',
    scale: 1
  });

  await browser.close();
  console.log('Saved poster-A0.pdf');
})();