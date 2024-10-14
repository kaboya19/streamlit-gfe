import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
while True:
    
    print("Çalışıyor...")
    bugün=datetime.now().strftime("%Y-%m-%d")


    
    dün=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

    
    data=pd.read_csv("C:/Users/Administrator/Documents/GitHub/streamlit-gfe/sepet.csv")
    data=data.set_index(data["Unnamed: 0"]).drop("Unnamed: 0",axis=1)
    data.index.name=""
    data=data.drop_duplicates()
    try:
        data=data.drop(f"{bugün}",axis=1)
    except:
        pass


    
    def veriekle(urun, data, urunler_df):
    # Ensure `data.loc[urun]` is a DataFrame, even if there's only one row (Series)
        if isinstance(data.loc[urun], pd.Series):
            data_for_urun = data.loc[urun].to_frame().T  # Convert Series to DataFrame
        else:
            data_for_urun = data.loc[urun]

        # Merge the data with urunler_df
        merged_df = pd.merge(data_for_urun, urunler_df, on='Ürün', how='outer')

        # Index'i doğru ürün ismiyle dolduruyoruz
        merged_df.index = len(merged_df) * [urun]

        # Eğer _x ve _y ile aynı tarihli sütunlar varsa birleştiriyoruz
        tarih_sutunlari = [col for col in merged_df.columns if col.endswith("_x") or col.endswith("_y")]
        
        for col in set([col.split("_")[0] for col in tarih_sutunlari]):
            if col + "_x" in merged_df.columns and col + "_y" in merged_df.columns:
                # Sütunları birleştiriyoruz, eğer birinde NaN varsa diğerini kullan
                merged_df[col] = merged_df[col + "_x"].combine_first(merged_df[col + "_y"])
                # _x ve _y sütunlarını kaldırıyoruz
                merged_df = merged_df.drop(columns=[col + "_x", col + "_y"])

        # Eski verileri (urun'e ait olan satırları) çıkarıyoruz
        data_without_urun = data.drop(index=urun, errors='ignore')  # Ignore error if the index doesn't exist

        # Yeni verileri ekliyoruz
        data = pd.concat([data_without_urun, merged_df])

        # Data'yı index'e göre sıralıyoruz
        data = data.sort_index()

        return data





    

    import re
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    import pandas as pd
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.headless = False  # Tarayıcı görünür modda çalışacak

    # WebDriver'ı başlat
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    def clean_price(price_text):
        # Remove any non-numeric characters except for commas and dots
        price_text = re.sub(r'[^\d,.]', '', price_text)
        # Replace commas with dots if needed (ensure it works with Turkish formatted numbers)
        price_text = price_text.replace(',', '.')
        try:
            return float(price_text)
        except ValueError:
            return None

    

    import re
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    import pandas as pd
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.headless = False  # Tarayıcı görünür modda çalışacak

    # WebDriver'ı başlat
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Function to clean and convert price text to float
    def clean_price(price_text):
        # Remove any non-numeric characters except for commas and dots
        price_text = re.sub(r'[^\d,.]', '', price_text)
        # Replace commas with dots if needed (ensure it works with Turkish formatted numbers)
        price_text = price_text.replace(',', '.')
        try:
            return float(price_text)
        except ValueError:
            return None

    # Function to scrape product names and prices from Migros for multiple URLs
    def scrape_migros_products(pages):
        product_data = []
        
        for page in pages:
            print(f"Scraping URL: {page}")
            driver.get(page)

            try:
                # Wait for the product names to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.product-name'))
                )

                # Get product names and prices
                products = driver.find_elements(By.CSS_SELECTOR, '.product-name')
                prices = driver.find_elements(By.CSS_SELECTOR, '.price-new')

                # Ensure we have matching names and prices
                if len(products) != len(prices):
                    print(f"Warning: Number of products and prices do not match on page {page}")

                for i in range(len(products)):
                    try:
                        product_name = products[i].text.strip()
                        product_price_text = prices[i].text.strip()
                        product_price = clean_price(product_price_text)  # Convert to float
                        product_data.append({"Product Name": product_name, "Price (TRY)": product_price})
                        print(f"Product: {product_name}, Price: {product_price} TRY")
                    except Exception as e:
                        print(f"Error scraping product {i} on page: {e}")

            except Exception as e:
                print(f"Error loading products on page: {e}")

            # Sleep to avoid being detected as a bot
            sleep(2)
        
        return product_data

    # Function to scrape product names and prices from Carrefour for multiple URLs
    def scrape_carrefour_products():
        pages = ["https://www.carrefoursa.com/pirinc/c/1134?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]

        
        carrefour_data = []
        for url in pages:
        
                # Send a GET request to fetch the HTML content
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Find all product cards
                product_cards = soup.find_all("div", class_="productCardData")
                
                # Loop through each product card and extract the product name and price
                for index, product_card in enumerate(product_cards):
                    # Extract product name
                    product_name = product_card.find("input", {"id": "productNamePost"})['value']
                    
                    # Extract product price (from the input tag with id="productPricePost")
                    product_price = product_card.find("input", {"id": "productPricePost"})['value']
                    
                    # Convert price to float
                    try:
                        product_price = float(product_price)
                    except ValueError:
                        product_price = None  # Handle cases where the price might not be convertible
                    
                    # Print product name and price
                    print(f"Product {index + 1}: {product_name}, Price: {product_price} TL")
                    carrefour_data.append({"Product Name": product_name, "Price (TRY)": product_price})

            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
        return carrefour_data


        def vericek(carrefour="",migros="",name=""):
            try:  

            # Function to clean and convert price text to float
                def clean_price(price_text):
                    # Remove any non-numeric characters except for commas and dots
                    price_text = re.sub(r'[^\d,.]', '', price_text)
                    # Replace commas with dots if needed (ensure it works with Turkish formatted numbers)
                    price_text = price_text.replace(',', '.')
                    try:
                        return float(price_text)
                    except ValueError:
                        return None



                # Function to scrape product names and prices from Carrefour for multiple URLs
                def scrape_carrefour_products(carrefour):
                    
                    pages = carrefour



                    
                    carrefour_data = []
                    
                    for url in pages:
                    
                            # Send a GET request to fetch the HTML content
                        response = requests.get(url)

                        # Check if the request was successful
                        if response.status_code == 200:
                            # Parse the HTML content
                            soup = BeautifulSoup(response.content, "html.parser")
                            
                            # Find all product cards
                            product_cards = soup.find_all("div", class_="productCardData")
                            
                            # Loop through each product card and extract the product name and price
                            for index, product_card in enumerate(product_cards):
                                # Extract product name
                                product_name = product_card.find("input", {"id": "productNamePost"})['value']
                                
                                # Extract product price (from the input tag with id="productPricePost")
                                product_price = product_card.find("input", {"id": "productPricePost"})['value']
                                
                                # Convert price to float
                                try:
                                    product_price = float(product_price)
                                except ValueError:
                                    product_price = None  # Handle cases where the price might not be convertible
                                
                                # Print product name and price
                                print(f"Product {index + 1}: {product_name}, Price: {product_price} TL")
                                carrefour_data.append({"Product Name": product_name, "Price (TRY)": product_price})

                        else:
                            print(f"Failed to retrieve the page. Status code: {response.status_code}")
                    
                    return carrefour_data

                # Define the list of pages to scrape from Migros
                migros_pages  = migros







                if migros:
                    migros_data = scrape_migros_products(migros)
                if carrefour:
                    carrefour_data = scrape_carrefour_products(carrefour)

                if migros and carrefour:

                    all_data = migros_data + carrefour_data
                elif migros and not carrefour:
                    all_data=migros_data
                else:
                    all_data=carrefour_data
                product_df = pd.DataFrame(all_data)

                # Close the browser
                driver.quit()





                urunler_df = product_df.copy()
                urunler_df.columns=["Ürün",str(bugün)]
                urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

                urunler_df.index=len(urunler_df)*[name]
                urunler_df=urunler_df.drop_duplicates()
                urunler_df=urunler_df.dropna()

                return urunler_df
            except:
                pass


        carrefour=["https://www.carrefoursa.com/search?q=%C3%BCz%C3%BCm%3AbestSeller%3AproductPrimaryCategoryCode%3A1017%3AinStockFlag%3Atrue&text=%C3%BCz%C3%BCm#"]
        migros=["https://www.migros.com.tr/arama?q=%C3%BCz%C3%BCm&sayfa=1&kategori=101"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Üzüm")


        data=veriekle("Üzüm",data,urunler_df)



        migros=["https://www.migros.com.tr/arama?q=beyaz%20lahana&sayfa=1&markalar=492&sirala=akilli-siralama&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Beyaz Lahana")
        urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Beyaz", regex=True)]


        data=veriekle("Beyaz Lahana",data,urunler_df)