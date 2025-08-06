from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=False ile tarayıcıyı görerek izleyebilirsin
    page = browser.new_page()
    page.goto("https://www.carrefoursa.com/dana/c/1046", timeout=60000)
    page.wait_for_selector("div.product-card", timeout=30000)  # ürün kartları yüklensin

    # Ürün adlarını ve fiyatlarını çek
    product_elements = page.query_selector_all("div.product-card")
    data = []
    for product in product_elements:
        name = product.query_selector("span.product-name")
        price = product.query_selector("span.price-tag") or product.query_selector("span.final-price")
        data.append({
            "Ürün Adı": name.inner_text().strip() if name else None,
            "Fiyat": price.inner_text().strip() if price else None
        })

    browser.close()

# Sonuçları yazdır veya DataFrame'e dönüştür
df = pd.DataFrame(data)
print(df)
