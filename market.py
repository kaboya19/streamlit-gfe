"""
import asyncio
from playwright.async_api import async_playwright
import re
from typing import List, Dict, Any
import time
from datetime import datetime
import pandas as pd

class AsyncMarketPriceAnalyzer:
    def __init__(self, urls: List[str], max_concurrent_pages: int = 5):
        self.base_urls = urls
        self.max_concurrent_pages = max_concurrent_pages
        self.results = []
        self.semaphore = None
        self.browser = None
        self.context = None

    async def extract_price(self, price_text: str) -> float:
        match = re.search(r'([\d,.]+)', price_text)
        if match:
            return float(match.group(1).replace(',', '.'))
        return 0.0

    async def setup(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.semaphore = asyncio.Semaphore(self.max_concurrent_pages)

    async def get_total_pages(self, url: str) -> int:
        try:
            page = await self.context.new_page()
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            # Sayfa numaralarını içeren tüm elementleri bul
            page_numbers = await page.query_selector_all("li.ng-star-inserted a span:not(.show-for-sr)")
            
            max_page = 1
            for num_element in page_numbers:
                try:
                    num_text = await num_element.text_content()
                    if num_text.isdigit():
                        page_num = int(num_text)
                        max_page = max(max_page, page_num)
                except:
                    continue
            
            await page.close()
            print(f"Toplam sayfa sayısı: {max_page}")
            return max_page
                
        except Exception as e:
            print(f"Sayfa sayısı alınırken hata: {str(e)}")
            return 1

    async def process_product(self, product, page_number: int, url: str, category: str):
        async with self.semaphore:
            try:
                product_page = await self.context.new_page()
                await product_page.goto(url)
                await product_page.wait_for_load_state('networkidle')
                
                for _ in range(page_number - 1):
                    next_button = await product_page.query_selector("li.pagination-next.ng-star-inserted a")
                    if next_button:
                        await next_button.click()
                        await product_page.wait_for_load_state('networkidle')

                products = await product_page.query_selector_all("tubitak-product-summary")
                if product >= len(products):
                    await product_page.close()
                    return None

                current_product = products[product]
                
                name_element = await current_product.query_selector(".product-name")
                price_element = await current_product.query_selector(".product-price")
                
                product_name = await name_element.text_content()
                product_price = await price_element.text_content()
                
                market_info = await current_product.query_selector("span.caption-10.secondary-600")
                has_multiple_markets = False
                market_count = ""
                prices = []

                if market_info:
                    market_count = await market_info.text_content()
                    if "+" in market_count:
                        has_multiple_markets = True
                        
                        await current_product.scroll_into_view_if_needed()
                        await current_product.click()
                        await product_page.wait_for_load_state('networkidle')
                        await asyncio.sleep(1)
                        
                        price_elements = await product_page.query_selector_all("dl.ng-star-inserted dd span.ng-star-inserted")
                        
                        for price_elem in price_elements:
                            price_text = await price_elem.text_content()
                            if '₺' in price_text:
                                price_value = await self.extract_price(price_text)
                                if price_value > 0:
                                    prices.append(price_value)

                result = {
                    'category': category,
                    'name': product_name,
                    'main_price': await self.extract_price(product_price),
                    'has_multiple_markets': has_multiple_markets,
                    'market_count': market_count,
                    'prices': prices,
                    'page': page_number
                }

                if prices:
                    result.update({
                        'average_price': sum(prices) / len(prices),
                        'min_price': min(prices),
                        'max_price': max(prices)
                    })

                await product_page.close()
                return result
                
            except Exception as e:
                print(f"Ürün işlenirken hata: {str(e)}")
                if 'product_page' in locals():
                    await product_page.close()
                return None

    async def analyze_category(self, url: str, category: str):
        print(f"\n=== {category} kategorisi analiz ediliyor ===")
        total_pages = await self.get_total_pages(url)
        print(f"Toplam sayfa sayısı: {total_pages}")
        
        category_results = []

        for page_number in range(1, total_pages + 1):
            print(f"\nSayfa {page_number}/{total_pages} işleniyor...")
            
            temp_page = await self.context.new_page()
            await temp_page.goto(url)
            await temp_page.wait_for_load_state('networkidle')
            
            for _ in range(page_number - 1):
                next_button = await temp_page.query_selector("li.pagination-next.ng-star-inserted a")
                if next_button:
                    await next_button.click()
                    await temp_page.wait_for_load_state('networkidle')
            
            products = await temp_page.query_selector_all("tubitak-product-summary")
            products_count = len(products)
            await temp_page.close()

            tasks = [
                self.process_product(product_index, page_number, url, category)
                for product_index in range(products_count)
            ]
            
            page_results = await asyncio.gather(*tasks)
            valid_results = [r for r in page_results if r is not None]
            category_results.extend(valid_results)
            
            for result in valid_results:
                print(f"\nÜrün: {result['name']}")
                print(f"Ana Fiyat: {result['main_price']:.2f} TL")
                if result['has_multiple_markets']:
                    print(f"Market Sayısı: {result['market_count']}")
                    if result['prices']:
                        print("\nFiyatlar:")
                        for price in result['prices']:
                            print(f"{price:.2f} TL")
                        print(f"Ortalama Fiyat: {result['average_price']:.2f} TL")
                        print(f"En Düşük Fiyat: {result['min_price']:.2f} TL")
                        print(f"En Yüksek Fiyat: {result['max_price']:.2f} TL")
                print("-" * 50)
                
        return category_results

    async def analyze(self):
        start_time = time.time()
        print(f"Analiz başladı: {datetime.now()}")
        
        await self.setup()
        
        for url in self.base_urls:
            category = url.split('/')[-1].replace('%20', ' ')
            category_results = await self.analyze_category(url, category)
            self.results.extend(category_results)
            
            # Her kategori sonrası CSV'ye kaydet
            df = pd.DataFrame(self.results)
            df.to_csv(f"market_fiyatlari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

        end_time = time.time()
        print(f"\nAnaliz tamamlandı: {datetime.now()}")
        print(f"Toplam süre: {end_time - start_time:.2f} saniye")
        print(f"Toplam ürün sayısı: {len(self.results)}")
        
        await self.browser.close()
        return self.results

async def main():
    # Analiz edilecek URL'ler
    urls = [
        "https://marketfiyati.org.tr/category/Meyve%20ve%20Sebze",
        "https://marketfiyati.org.tr/category/Et,%20Tavuk%20ve%20Bal%C4%B1k",

        "https://marketfiyati.org.tr/category/S%C3%BCt%20%C3%9Cr%C3%BCnleri%20ve%20Kahvalt%C4%B1l%C4%B1k",
        "https://marketfiyati.org.tr/category/Temel%20G%C4%B1da",
        "https://marketfiyati.org.tr/category/%C4%B0%C3%A7ecek",
        "https://marketfiyati.org.tr/category/At%C4%B1%C5%9Ft%C4%B1rmal%C4%B1k%20ve%20Tatl%C4%B1"
        # Diğer URL'leri buraya ekleyebilirsiniz
    ]
    
    analyzer = AsyncMarketPriceAnalyzer(urls=urls, max_concurrent_pages=10)
    results = await analyzer.analyze()
    results=pd.DataFrame(results)
    results.to_csv("market.csv")
    return results

if __name__ == "__main__":
    asyncio.run(main())
    """

import asyncio
from playwright.async_api import async_playwright
import re
from typing import List, Dict, Any
import time
from datetime import datetime
import pandas as pd

class AsyncMarketPriceAnalyzer:
    def __init__(self, urls: List[str], max_concurrent_pages: int = 10):
        self.base_urls = urls
        self.max_concurrent_pages = max_concurrent_pages
        self.results = []
        self.semaphore = None
        self.browser = None
        self.context = None

    async def extract_price(self, price_text: str) -> float:
        match = re.search(r'([\d,.]+)', price_text)
        if match:
            return float(match.group(1).replace(',', '.'))
        return 0.0

    async def setup(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.semaphore = asyncio.Semaphore(self.max_concurrent_pages)

    async def get_total_pages(self, url: str) -> int:
        try:
            page = await self.context.new_page()
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            # Sayfa numaralarını içeren tüm elementleri bul
            page_numbers = await page.query_selector_all("li.ng-star-inserted a span:not(.show-for-sr)")
            
            max_page = 1
            for num_element in page_numbers:
                try:
                    num_text = await num_element.text_content()
                    if num_text.isdigit():
                        page_num = int(num_text)
                        max_page = max(max_page, page_num)
                except:
                    continue
            
            await page.close()
            print(f"Toplam sayfa sayısı: {max_page}")
            return max_page
        except Exception as e:
            print(f"Sayfa sayısı alınırken hata: {str(e)}")
            return 1

    async def process_products(self, page: Any, url: str, category: str, page_number: int) -> List[Dict[str, Any]]:
        try:
            await page.goto(url)
            await page.wait_for_load_state('networkidle')

            for _ in range(page_number - 1):
                next_button = await page.query_selector("li.pagination-next.ng-star-inserted a")
                if next_button:
                    await next_button.click()
                    await page.wait_for_load_state('networkidle')

            products = await page.query_selector_all("tubitak-product-summary")
            tasks = [
                self.process_product(product_index, page, url, category)
                for product_index in range(len(products))
            ]
            page_results = await asyncio.gather(*tasks)
            return [r for r in page_results if r is not None]
        except Exception as e:
            print(f"Sayfa işlenirken hata: {str(e)}")
            return []

    async def process_product(self, product_index: int, page: Any, url: str, category: str) -> Dict[str, Any]:
        try:
            products = await page.query_selector_all("tubitak-product-summary")
            current_product = products[product_index]

            name_element = await current_product.query_selector(".product-name")
            price_element = await current_product.query_selector(".product-price")
            product_name = await name_element.text_content()
            product_price = await price_element.text_content()

            market_info = await current_product.query_selector("span.caption-10.secondary-600")
            has_multiple_markets = False
            market_count = ""
            prices = []

            if market_info:
                market_count = await market_info.text_content()
                if "+" in market_count:
                    has_multiple_markets = True
                    await current_product.scroll_into_view_if_needed()
                    await current_product.click()
                    await page.wait_for_load_state('networkidle')
                    await asyncio.sleep(1)
                    price_elements = await page.query_selector_all("dl.ng-star-inserted dd span.ng-star-inserted")
                    for price_elem in price_elements:
                        price_text = await price_elem.text_content()
                        if '₺' in price_text:
                            price_value = await self.extract_price(price_text)
                            if price_value > 0:
                                prices.append(price_value)

            result = {
                'category': category,
                'name': product_name,
                'main_price': await self.extract_price(product_price),
                'has_multiple_markets': has_multiple_markets,
                'market_count': market_count,
                'prices': prices
            }

            if prices:
                result.update({
                    'average_price': sum(prices) / len(prices),
                    'min_price': min(prices),
                    'max_price': max(prices)
                })

            return result
        except Exception as e:
            print(f"Ürün işlenirken hata: {str(e)}")
            return None

    async def analyze_category(self, url: str, category: str):
        print(f"\n=== {category} kategorisi analiz ediliyor ===")
        total_pages = await self.get_total_pages(url)
        print(f"Toplam sayfa sayısı: {total_pages}")
        
        category_results = []
        page = await self.context.new_page()

        for page_number in range(1, total_pages + 1):
            print(f"\nSayfa {page_number}/{total_pages} işleniyor...")
            page_results = await self.process_products(page, url, category, page_number)
            category_results.extend(page_results)
            
            for result in page_results:
                print(f"\nÜrün: {result['name']}")
                print(f"Ana Fiyat: {result['main_price']:.2f} TL")
                if result['has_multiple_markets']:
                    print(f"Market Sayısı: {result['market_count']}")
                    if result['prices']:
                        print("\nFiyatlar:")
                        for price in result['prices']:
                            print(f"{price:.2f} TL")
                        print(f"Ortalama Fiyat: {result['average_price']:.2f} TL")
                        print(f"En Düşük Fiyat: {result['min_price']:.2f} TL")
                        print(f"En Yüksek Fiyat: {result['max_price']:.2f} TL")
                print("-" * 50)
                
        await page.close()
        return category_results

    async def analyze(self):
        start_time = time.time()
        print(f"Analiz başladı: {datetime.now()}")
        
        await self.setup()
        
        for url in self.base_urls:
            category = url.split('/')[-1].replace('%20', ' ')
            category_results = await self.analyze_category(url, category)
            self.results.extend(category_results)
            
            # Her kategori sonrası CSV'ye kaydet
            df = pd.DataFrame(self.results)
            df.to_csv(f"market_fiyatlari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)

        end_time = time.time()
        print(f"\nAnaliz tamamlandı: {datetime.now()}")
        print(f"Toplam süre: {end_time - start_time:.2f} saniye")
        print(f"Toplam ürün sayısı: {len(self.results)}")
        
        await self.browser.close()
        return self.results

async def main():
    # Analiz edilecek URL'ler
    urls = [
        "https://marketfiyati.org.tr/category/Meyve%20ve%20Sebze",
        "https://marketfiyati.org.tr/category/Et,%20Tavuk%20ve%20Bal%C4%B1k",
        "https://marketfiyati.org.tr/category/S%C3%BCt%20%C3%9Cr%C3%BCnleri%20ve%20Kahvalt%C4%B1l%C4%B1k",
        "https://marketfiyati.org.tr/category/Temel%20G%C4%B1da",
        "https://marketfiyati.org.tr/category/%C4%B0%C3%A7ecek",
        "https://marketfiyati.org.tr/category/At%C4%B1%C5%9Ft%C4%B1rmal%C4%B1k%20ve%20Tatl%C4%B1"
        # Diğer URL'leri buraya ekleyebilirsiniz
    ]
    
    analyzer = AsyncMarketPriceAnalyzer(urls=urls, max_concurrent_pages=10)
    results = await analyzer.analyze()
    results=pd.DataFrame(results)
    results.to_csv("market.csv")
    return results

if __name__ == "__main__":
    asyncio.run(main())

