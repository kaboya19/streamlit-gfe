import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time

# Generate dates
tarihler = pd.date_range(start="2024-01-01", end="2025-03-08", freq="D")
tarihler = tarihler.strftime("%d.%m.%Y").values

async def fetch_data_for_date(tarih, browser):
    page = await browser.new_page()

    try:
        # Navigate to the page
        await page.goto("https://www.hal.gov.tr/Sayfalar/FiyatDetaylari.aspx")

        # Clear and set the date input field for each iteration
        await page.fill("#ctl00_ctl37_g_7e86b8d6_3aea_47cf_b1c1_939799a091e0_dateControl_dateControlDate", "")
        await page.fill("#ctl00_ctl37_g_7e86b8d6_3aea_47cf_b1c1_939799a091e0_dateControl_dateControlDate", tarih)

        # Click the 'Fiyat Bul' button
        await page.click("#ctl00_ctl37_g_7e86b8d6_3aea_47cf_b1c1_939799a091e0_btnGet")

        # Click the 'All Pages' radio button
        await page.click("#ctl00_ctl37_g_7e86b8d6_3aea_47cf_b1c1_939799a091e0_rblExcelOptions_1")

        # Click the 'Excel Indir' button
        await page.click("#ctl00_ctl37_g_7e86b8d6_3aea_47cf_b1c1_939799a091e0_btnExcel")

        # Wait for a few seconds to ensure the download starts
        await asyncio.sleep(2)

        print(f"{tarih} çekildi!")
    finally:
        # Close the page after processing
        await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch browser in headless mode

        tasks = []
        for tarih in tarihler:
            task = asyncio.create_task(fetch_data_for_date(tarih, browser))
            tasks.append(task)

        await asyncio.gather(*tasks)

        # Close the browser after all tasks are done
        await browser.close()

# Run the asyncio event loop
asyncio.run(main())
