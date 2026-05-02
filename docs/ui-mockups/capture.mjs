import { chromium } from 'playwright';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 500, height: 850 } });
const page = await ctx.newPage();
await page.goto('file://' + process.cwd() + '/babygrow-ui-animated.html');
await page.waitForTimeout(2000);

// Screenshot 1: Welcome
await page.screenshot({ path: 'shot-01-welcome.png' });

// Click "开始使用" to go to Home
await page.click('.cta-btn');
await page.waitForTimeout(1500);
await page.screenshot({ path: 'shot-02-home.png' });

// Click "记录" tab
await page.click('.tab-item:nth-child(2)');
await page.waitForTimeout(1000);
await page.screenshot({ path: 'shot-03-records.png' });

// Click "AI助手" tab
await page.click('.tab-item:nth-child(3)');
await page.waitForTimeout(1000);
await page.screenshot({ path: 'shot-04-chat.png' });

// Click "里程碑" tab
await page.click('.tab-item:nth-child(4)');
await page.waitForTimeout(1000);
await page.screenshot({ path: 'shot-05-milestones.png' });

// Click "我的" tab
await page.click('.tab-item:nth-child(5)');
await page.waitForTimeout(1000);
await page.screenshot({ path: 'shot-06-profile.png' });

await browser.close();
console.log('All 6 screenshots captured!');
