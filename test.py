
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import pandas as pd
import numpy as np


while True:
    try:

        bugün=datetime.now().strftime("%Y-%m-%d")



        dün=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")


        data=pd.read_csv("sepet.csv")
        data=data.set_index(data["Unnamed: 0"]).drop("Unnamed: 0",axis=1)
        data.index.name=""
        try:
            data=data.drop(f"{bugün}",axis=1)
        except:
            pass



        def veriekle(urun, data, urunler_df):

            try:

                if urunler_df is None or urunler_df.empty:
                    return data

                elif isinstance(data.loc[urun], pd.Series):
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
                        # Sütunları birleştiriyoruz
                        merged_df[col] = merged_df[col + "_x"].combine_first(merged_df[col + "_y"])
                        # _x ve _y sütunlarını kaldırıyoruz
                        merged_df = merged_df.drop(columns=[col + "_x", col + "_y"])

                # Eski verileri (urun'e ait olan satırları) çıkarıyoruz
                data_without_urun = data.drop(index=urun)

                # Yeni verileri ekliyoruz
                data = pd.concat([data_without_urun, merged_df])

                # Data'yı index'e göre sıralıyoruz
                data = data.sort_index()


                return data
            except:
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

        # Define the list of pages to scrape from Migros
        migros_pages  = [
            "https://www.migros.com.tr/arama?q=pirin%C3%A7&kategori=5&sirala=indirim-yuzdesine-gore&sayfa=","https://www.migros.com.tr/arama?q=pirin%C3%A7&kategori=5&sirala=indirim-yuzdesine-gore&sayfa=2"
        ]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        if not migros_data:
            all_data =   carrefour_data
        elif not carrefour_data:
            all_data=migros_data
        else:
            all_data=migros_data+carrefour_data

        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Pirinç"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            data=veriekle("Pirinç",data,urunler_df)


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
                            print(f"Error scraping product {i} on page : {e}")

                except Exception as e:
                    print(f"Error loading products on page : {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data

        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=bu%C4%9Fday+unu%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1276"]

            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=bu%C4%9Fday%20unu"]

        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        all_data = migros_data + carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()




        if urunler_df is not None:
            urunler_df = product_df.copy()
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Buğday Unu"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Buğday Unu",data,urunler_df)


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

        # Function to scrape product names and prices from Migros
        def scrape_migros_products(base_url, total_pages):
            product_data = []
            
            for page in range(1, total_pages + 1):
                url = f"{base_url}{page}"
                print(f"Scraping page {page}: {url}")
                driver.get(url)

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
                            print(f"Error scraping product {i} on page : {e}")

                except Exception as e:
                    print(f"Error loading products on page : {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data


        def scrape_carrefour_products():
            carrefour_data=[]
            pages=["https://www.carrefoursa.com/search?q=devam+s%C3%BCt%C3%BC%3AbestSeller%3AproductPrimaryCategoryCode%3A1848&show=All"]
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

        # Define base URL and total pages to scrape for Migros
        migros_base_url = "https://www.migros.com.tr/arama?q=bebek%20s%C3%BCt%C3%BC&kategori=70507&sirala=akilli-siralama&sayfa="
        migros_total_pages = 2

        migros_data = scrape_migros_products(migros_base_url, migros_total_pages)


        carrefour_data = scrape_carrefour_products()

        

        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)


        driver.quit()
        if urunler_df is not None:
            urunler_df = product_df.copy()
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Bebek Sütü (Toz Karışım)"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Bebek Sütü (Toz Karışım)",data,urunler_df)


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

        # Function to scrape product names and prices from Migros
        def scrape_migros_products(base_url, total_pages):
            product_data = []
            
            for page in range(1, total_pages + 1):
                url = f"{base_url}{page}"
                print(f"Scraping page {page}: {url}")
                driver.get(url)

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
                            print(f"Error scraping product {i} on page : {e}")

                except Exception as e:
                    print(f"Error loading products on page : {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data

        # Function to scrape product names and prices from Carrefour
        def scrape_carrefour_products():
            carrefour_data=[]
            pages = ["https://www.carrefoursa.com/bulgur/c/1142?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
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

        # Define base URL and total pages to scrape for Migros
        migros_base_url = "https://www.migros.com.tr/arama?q=bulgur&kategori=1062&sirala=akilli-siralama&sayfa="
        migros_total_pages = 2

        # Scrape Migros products
        migros_data = scrape_migros_products(migros_base_url, migros_total_pages)

        # Scrape Carrefour products
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        all_data = migros_data+carrefour_data
        product_df = pd.DataFrame(all_data)


        driver.quit()

        urunler_df = product_df.copy()
        if urunler_df is not None:
                urunler_df.columns=["Ürün",str(bugün)]
                urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

                urunler_df.index=len(urunler_df)*["Bulgur"]
                urunler_df=urunler_df.drop_duplicates()
                urunler_df=urunler_df.dropna()





                #data=pd.concat([data,urunler_df],axis=0)


                data=veriekle("Bulgur",data,urunler_df)


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

        # Function to scrape product names and prices from Migros
        def scrape_migros_products(base_url, total_pages):
            product_data = []
            
            for page in range(1, total_pages + 1):
                url = f"{base_url}{page}"
                print(f"Scraping page {page}: {url}")
                driver.get(url)

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
                            print(f"Error scraping product {i} on page : {e}")

                except Exception as e:
                    print(f"Error loading products on page : {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data

        # Function to scrape product names and prices from Carrefour
        def scrape_carrefour_products():
            carrefour_data=[]
            pages = ["https://www.carrefoursa.com/search?q=ekmek%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1398","https://www.carrefoursa.com/search?q=ekmek%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1401"]
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

        # Define base URL and total pages to scrape for Migros
        migros_base_url = "https://www.migros.com.tr/arama?q=ekmek&kategori=1109&markalar=492&sirala=akilli-siralama&sayfa="
        migros_total_pages = 1

        # Scrape Migros products
        migros_data = scrape_migros_products(migros_base_url, migros_total_pages)

        # Scrape Carrefour products
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)


        driver.quit()

        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Ekmek"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()




            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Ekmek",data,urunler_df)


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

        def scrape_migros_products(base_url, total_pages):
            product_data = []
            
            for page in range(1, total_pages + 1):
                url = f"{base_url}{page}"
                print(f"Scraping page {page}: {url}")
                driver.get(url)

                try:
                    # Wait for the product names to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.product-name'))
                    )

                    # Get all product cards
                    product_cards = driver.find_elements(By.CSS_SELECTOR, 'sm-list-page-item')

                    for product_card in product_cards:
                        # Check if the product is sponsored by looking for a specific sponsored class or attribute
                        if "external-list-item" in product_card.get_attribute('class').lower():
                            print("Skipping sponsored product.")
                            continue  # Skip this sponsored product

                        try:
                            # Extract the product name
                            product_name = product_card.find_element(By.CSS_SELECTOR, '.product-name').text.strip()

                            # Try to extract the price from multiple possible locations
                            price_element = None
                            try:
                                # First attempt using the primary price selector
                                price_element = product_card.find_element(By.CSS_SELECTOR, '.price-new')
                            except Exception:
                                try:
                                    # If not found, try another potential selector for the price
                                    price_element = product_card.find_element(By.CSS_SELECTOR, '.price .amount')
                                except Exception:
                                    print(f"Price not found for product: {product_name}")
                                    continue  # Skip if no price is found

                            if price_element:
                                product_price_text = price_element.text.strip()
                                product_price = clean_price(product_price_text)  # Convert price to float
                                # Append product name and price to the list
                                product_data.append({"Product Name": product_name, "Price (TRY)": product_price})
                                print(f"Product: {product_name}, Price: {product_price} TRY")

                        except Exception as e:
                            print(f"Error scraping a product on page: {e}")

                except Exception as e:
                    print(f"Error loading products on page : {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data

        # Function to scrape product names and prices from Carrefour
        def scrape_carrefour_products():
                carrefour_data=[]
                url = "https://www.carrefoursa.com/search?q=bisk%C3%BCvi%3AbestSeller%3AproductPrimaryCategoryCode%3A1529%3AinStockFlag%3Atrue&show=All"

            
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

        # Define base URL and total pages to scrape for Migros
        migros_base_url = "https://www.migros.com.tr/arama?q=bisk%C3%BCvi&kategori=1084&sayfa="
        migros_total_pages = 8

        # Scrape Migros products
        migros_data = scrape_migros_products(migros_base_url, migros_total_pages)

        # Scrape Carrefour products
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)


        driver.quit()
        
        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df[urunler_df['Ürün'].str.contains("Bisküvi", case=False)]

            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Bisküvi"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()




            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Bisküvi",data,urunler_df)



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
            
            for url in pages:
                driver.get(url)

                try:
                    # Wait for the product names to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.product-name'))
                    )

                    # Get all product cards
                    product_cards = driver.find_elements(By.CSS_SELECTOR, 'sm-list-page-item')

                    for product_card in product_cards:
                        # Check if the product is sponsored by looking for a specific sponsored class or attribute
                        if "external-list-item" in product_card.get_attribute('class').lower():
                            print("Skipping sponsored product.")
                            continue  # Skip this sponsored product

                        try:
                            # Extract the product name
                            product_name = product_card.find_element(By.CSS_SELECTOR, '.product-name').text.strip()

                            # Try to extract the price from multiple possible locations
                            price_element = None
                            try:
                                # First attempt using the primary price selector
                                price_element = product_card.find_element(By.CSS_SELECTOR, '.price-new')
                            except Exception:
                                try:
                                    # If not found, try another potential selector for the price
                                    price_element = product_card.find_element(By.CSS_SELECTOR, '.price .amount')
                                except Exception:
                                    print(f"Price not found for product: {product_name}")
                                    continue  # Skip if no price is found

                            if price_element:
                                product_price_text = price_element.text.strip()
                                product_price = clean_price(product_price_text)  # Convert price to float
                                # Append product name and price to the list
                                product_data.append({"Product Name": product_name, "Price (TRY)": product_price})
                                print(f"Product: {product_name}, Price: {product_price} TRY")

                        except Exception as e:
                            print(f"Error scraping a product on page: {e}")

                except Exception as e:
                    print(f"Error loading products on page: {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data

        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=kraker%3AbestSeller%3AinStockFlag%3Atrue&show=All"]


            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=kraker&sayfa=1&kategori=10218&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=kraker&sayfa=2&kategori=10218&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=kraker&sayfa=3&kategori=10218&sirala=akilli-siralama"]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Kraker"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Kraker",data,urunler_df)


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


        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=gofret%3AbestSeller%3AinStockFlag%3Atrue&text=gofret#"]


            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=gofret&sayfa=1&kategori=1082&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=gofret&sayfa=2&kategori=1082&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=gofret&sayfa=3&kategori=1082&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=gofret&sayfa=4&kategori=1082&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=gofret&sayfa=5&kategori=1082&sirala=akilli-siralama"]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Gofret"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()







            #data=pd.concat([data,urunler_df],axis=0)





            data=veriekle("Gofret",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/pastalar/c/1289?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=pasta&sayfa=1&kategori=1113",
                        "https://www.migros.com.tr/arama?q=pasta&sayfa=1&kategori=1111"]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Pasta"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()









            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Pasta",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=kek%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=kek&sayfa=1&kategori=1085"]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Kek"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()









            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Kek",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=baklava%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1294"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=baklava&sayfa=1&kategori=126"
        ]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Baklava"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()










            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Baklava",data,urunler_df)


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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/baliklar/c/1099?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=yufka"
        ]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)


        # Combine both datasets into one DataFrame
        all_data = migros_data 
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Ekmek Hamuru (Yufka)"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()










            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Ekmek Hamuru (Yufka)",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/makarna/c/1122?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=makarna&sayfa=1&kategori=10112&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=makarna&sayfa=2&kategori=10112&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=makarna&sayfa=3&kategori=10112&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=makarna&sayfa=4&kategori=10112&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=makarna&sayfa=5&kategori=10112&sirala=akilli-siralama"
                        
        ]



        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Şehriye", regex=True)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Makarna"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()











            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Makarna",data,urunler_df)



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


        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=%C5%9Fehriye%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1122"]



            
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
        migros_pages  = ["https://www.migros.com.tr/arama?q=%C5%9Fehriye&sayfa=1&kategori=5"
        ]

        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Makarna", regex=True)]
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Bulgur", regex=True)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Şehriye"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()











            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Şehriye",data,urunler_df)



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


        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/musli-hububat-urunleri/c/1378?q=%3AbestSeller%3Acategory%3A1310%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/kahvaltilik-gevrek-c-422?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/kahvaltilik-gevrek-c-422?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/kahvaltilik-gevrek-c-422?sayfa=3&sirala=onerilenler",
                        "https://www.migros.com.tr/kahvaltilik-gevrek-c-422?sayfa=4&sirala=onerilenler"
                        

        ]


        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Tahıl Gevreği"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()













            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Tahıl Gevreği",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/search?q=dana+eti%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1046"]



            
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
            return carrefour_data

        # Define the list of pages to scrape from Migros
        migros_pages  =  ["https://www.migros.com.tr/dana-eti-c-3fa?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/dana-eti-c-3fa?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/dana-eti-c-3fa?sayfa=3&sirala=onerilenler",

        ]



        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Dana Eti"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()














            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Dana Eti",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/kuzu/c/1054?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/kuzu-eti-c-3fb?sayfa=1"

        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Kuzu Eti"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Kuzu Eti",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/pilic/c/1061?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/pilic-c-3fe?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/pilic-c-3fe?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/pilic-c-3fe?sayfa=3&sirala=onerilenler",

        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Tavuk Eti"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()




















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Tavuk Eti",data,urunler_df)



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




        # Define the list of pages to scrape from Migros
        migros_pages  =  ["https://www.migros.com.tr/sakatat-c-3fd"

        ]






        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)


        # Combine both datasets into one DataFrame
        all_data = migros_data 
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Sakatat"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()




















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Sakatat",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            pages = ["https://www.carrefoursa.com/sucuk/c/1077?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  = ["https://www.migros.com.tr/sucuk-c-404?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/sucuk-c-404?sayfa=1&sirala=onerilenler",

        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Sucuk"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()





















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Sucuk",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/sosis/c/1084?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/sosis-c-405?sayfa=1"


        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Salam", regex=True)]
            urunler_df.index=len(urunler_df)*["Sosis"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Sosis",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/salam-jambon-ve-fume/c/1092?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/salam-c-112d6?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/salam-c-112d6?sayfa=2&sirala=onerilenler",
                

        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Salam"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Salam",data,urunler_df)



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




        # Define the list of pages to scrape from Migros
        migros_pages  = ["https://www.migros.com.tr/pratik-yemek-c-44f?sayfa=1&90=503&sirala=onerilenler"
        ]




        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)


        # Combine both datasets into one DataFrame
        all_data = migros_data 
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Hazır Et Yemekleri"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()
























            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Hazır Et Yemekleri",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/baliklar/c/1099?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/mevsim-baliklari-c-402?sayfa=1"]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Balık"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






















            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Balık",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/paketli-urunler/c/1068?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  = ["https://www.migros.com.tr/dondurulmus-deniz-urunleri-c-2830?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/dondurulmus-deniz-urunleri-c-2830?sayfa=2&sirala=onerilenler"



        ]




        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Konserve Balık"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()
























            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Konserve Balık",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/sut/c/1311?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/sut-c-6c?sayfa=1&109=1020&sirala=onerilenler",
                        "https://www.migros.com.tr/sut-c-6c?sayfa=2&109=1020&sirala=onerilenler"




        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})
            urunler_df.index=len(urunler_df)*["Süt"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()







            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Süt",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/yogurt/c/1389?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  = ["https://www.migros.com.tr/yogurt-c-6e?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/yogurt-c-6e?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/yogurt-c-6e?sayfa=3&sirala=onerilenler",
                        "https://www.migros.com.tr/yogurt-c-6e?sayfa=4&sirala=onerilenler"




        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Yoğurt"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()



























            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Yoğurt",data,urunler_df)




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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/sutlu-tatli-puding/c/1962?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/geleneksel-sutlu-tatlilar-c-2765?sayfa=1&sirala=onerilenler"
        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Hazır Sütlü Tatlılar"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()



























            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Hazır Sütlü Tatlılar",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/beyaz-peynir/c/1319?q=%3AbestSeller&show=All"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/inek-peyniri-c-2731?sayfa=1",
                        "https://www.migros.com.tr/koyun-peyniri-c-2732?sayfa=1",
                        "https://www.migros.com.tr/suzme-peynir-c-2733?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/suzme-peynir-c-2733?sayfa=2&sirala=onerilenler",
                        "https://www.migros.com.tr/keci-peyniri-c-2735?sayfa=1"
                




        ]




        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Beyaz Peynir"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()




























            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Beyaz Peynir",data,urunler_df)




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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/kasar-/c/1324?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/kasar-peyniri-c-40d?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/kasar-peyniri-c-40d?sayfa=2&sirala=onerilenler"
                
        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Kaşar Peyniri"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()































            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Kaşar Peyniri",data,urunler_df)




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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/krem-peynir/c/1336?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/arama?q=krem%20peynir&sayfa=1&kategori=10039&sirala=akilli-siralama",
                        "https://www.migros.com.tr/arama?q=krem%20peynir&sayfa=2&kategori=10039&sirala=akilli-siralama"

                




        ]





        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Krem Peynir"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()
































            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Krem Peynir",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/yumurta/c/1349?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =   ["https://www.migros.com.tr/yumurta-c-70"

                




        ]






        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Yumurta"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Yumurta",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/tereyag/c/1350?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/tereyagi-c-413?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/tereyagi-c-413?sayfa=2&sirala=onerilenler"


                




        ]







        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Tereyağı (Kahvaltılık)"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Tereyağı (Kahvaltılık)",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/margarin/c/1351?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/margarin-c-414?sayfa=1"]







        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Margarin"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()






            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Margarin",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/zeytinyagi/c/1114?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  =  ["https://www.migros.com.tr/zeytinyagi-c-433?sayfa=1&sirala=onerilenler",
                        "https://www.migros.com.tr/zeytinyagi-c-433?sayfa=2&sirala=onerilenler"


                




        ]







        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Zeytinyağı"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()







            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Zeytinyağı",data,urunler_df)



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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/aycicek/c/1112?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/aycicek-yagi-c-42d?sayfa=1"


                




        ]







        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()

        # Combine both datasets into one DataFrame
        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Ayçiçek Yağı"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()















            #data=pd.concat([data,urunler_df],axis=0)



            data=veriekle("Ayçiçek Yağı",data,urunler_df)





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



        # Function to scrape product names and prices from Carrefour for multiple URLs
        def scrape_carrefour_products():
            
            pages = ["https://www.carrefoursa.com/search?q=portakal%3AbestSeller%3AproductPrimaryCategoryCode%3A1016%3AinStockFlag%3Atrue&text=portakal#"]



            
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
        migros_pages  = ["https://www.migros.com.tr/narenciye-c-3ec?sayfa=1&93=652&sirala=onerilenler"


                




        ]








        # Scrape products from Migros and Carrefour
        migros_data = scrape_migros_products(migros_pages)
        carrefour_data = scrape_carrefour_products()


        if migros_data and carrefour_data:

                    all_data = migros_data + carrefour_data
        elif migros_data and not carrefour_data:
                    all_data=migros_data
        else:
                    all_data=carrefour_data
        product_df = pd.DataFrame(all_data)

        # Close the browser
        driver.quit()





        urunler_df = product_df.copy()
        if urunler_df is not None:
            urunler_df.columns=["Ürün",str(bugün)]
            urunler_df=urunler_df.groupby("Ürün", as_index=False).agg({str(bugün): 'mean'})

            urunler_df.index=len(urunler_df)*["Portakal"]
            urunler_df=urunler_df.drop_duplicates()
            urunler_df=urunler_df.dropna()





            #data=pd.concat([data,urunler_df],axis=0)


            data=veriekle("Portakal",data,urunler_df)


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
                if urunler_df is not None:
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


        carrefour=["https://www.carrefoursa.com/search?q=armut%3AbestSeller%3AproductPrimaryCategoryCode%3A1018%3AinStockFlag%3Atrue&text=armut#"]
        migros=["https://www.migros.com.tr/arama?q=armut&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Armut")


        data=veriekle("Armut",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=ayva%3AbestSeller%3AproductPrimaryCategoryCode%3A1018%3AinStockFlag%3Atrue&text=ayva#"]
        migros=["https://www.migros.com.tr/arama?q=ayva&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Ayva")


        data=veriekle("Ayva",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=%C3%A7ilek%3AbestSeller%3AproductPrimaryCategoryCode%3A1017%3AinStockFlag%3Atrue&text=%C3%A7ilek#"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour=carrefour,name="Çilek")


        data=veriekle("Çilek",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=elma%3AbestSeller%3AproductPrimaryCategoryCode%3A1018%3AinStockFlag%3Atrue&text=elma#"]
        migros=["https://www.migros.com.tr/arama?q=elma&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Elma")


        data=veriekle("Elma",data,urunler_df)



        """carrefour=["https://www.carrefoursa.com/search/?q=karpuz%3AbestSeller%3AinStockFlag%3Atrue&text=karpuz#"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour=carrefour,name="Karpuz")
        urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Karpuz kg|Karpuz Kg")]


        data=veriekle("Karpuz",data,urunler_df)"""


        carrefour=["https://www.carrefoursa.com/search?q=kavun%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1018"]
        migros=["https://www.migros.com.tr/arama?q=kavun&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kavun")


        data=veriekle("Kavun",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search/?q=kivi%3AbestSeller%3AinStockFlag%3Atrue&text=kivi#"]
        migros=["https://www.migros.com.tr/arama?q=kivi&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kivi")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("ml")]


        data=veriekle("Kivi",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=limon%3AbestSeller%3AproductPrimaryCategoryCode%3A1016%3AinStockFlag%3Atrue&text=limon#"]
        migros=["https://www.migros.com.tr/arama?q=limon&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Limon")

        data=veriekle("Limon",data,urunler_df)





        carrefour=["https://www.carrefoursa.com/search/?q=mandalina%3AbestSeller%3AinStockFlag%3Atrue&text=mandalina#"]
        migros=["https://www.migros.com.tr/arama?q=mandalina&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Mandalina")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("kg|Kg")]



        data=veriekle("Mandalina",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/search?q=muz%3AbestSeller%3AproductPrimaryCategoryCode%3A1022%3AinStockFlag%3Atrue&text=muz#"]
        migros=["https://www.migros.com.tr/arama?q=muz&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Muz")


        data=veriekle("Muz",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=%C5%9Feftali%3AbestSeller%3AproductPrimaryCategoryCode%3A1018%3AinStockFlag%3Atrue&text=%C5%9Feftali#"]
        migros=["https://www.migros.com.tr/arama?q=%C5%9Feftali&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Şeftali")


        data=veriekle("Şeftali",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=nar%3AbestSeller%3AproductPrimaryCategoryCode%3A1018%3AinStockFlag%3Atrue&text=nar#"]
        migros=["https://www.migros.com.tr/arama?q=nar&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Nar")


        data=veriekle("Nar",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=badem%3AbestSeller%3AproductPrimaryCategoryCode%3A1519%3AinStockFlag%3Atrue&text=badem#"]
        migros=["https://www.migros.com.tr/badem-c-280f"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Badem İçi")


        data=veriekle("Badem İçi",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=ceviz%3AbestSeller%3AproductPrimaryCategoryCode%3A1519%3AinStockFlag%3Atrue&text=ceviz#"]
        migros=["https://www.migros.com.tr/arama?q=ceviz&sayfa=1&kategori=1089"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Ceviz İçi")


        data=veriekle("Ceviz İçi",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=f%C4%B1nd%C4%B1k%3AbestSeller%3AproductPrimaryCategoryCode%3A1519%3AinStockFlag%3Atrue&text=f%C4%B1nd%C4%B1k#"]
        migros=["https://www.migros.com.tr/arama?q=f%C4%B1nd%C4%B1k&sayfa=1&kategori=1090","https://www.migros.com.tr/arama?q=f%C4%B1nd%C4%B1k&sayfa=1&kategori=1089"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Fındık İçi")


        data=veriekle("Fındık İçi",data,urunler_df)




        migros=["https://www.migros.com.tr/arama?q=Antep%20F%C4%B1st%C4%B1%C4%9F%C4%B1&sayfa=1&kategori=1090"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Antep Fıstığı")


        data=veriekle("Antep Fıstığı",data,urunler_df)


        migros=["https://www.migros.com.tr/arama?q=Yer%20F%C4%B1st%C4%B1%C4%9F%C4%B1&sayfa=1&kategori=1090"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Yer Fıstığı")


        data=veriekle("Yer Fıstığı",data,urunler_df)













        carrefour=["https://www.carrefoursa.com/search/?q=leblebi%3AbestSeller%3AinStockFlag%3Atrue&text=leblebi#"]
        migros=["https://www.migros.com.tr/arama?q=leblebi&sayfa=1&kategori=70651"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Leblebi")


        data=veriekle("Leblebi",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=ay%C3%A7ekirde%C4%9Fi%3AbestSeller%3AinStockFlag%3Atrue&text=ay%C3%A7ekirde%C4%9Fi#"]
        migros=["https://www.migros.com.tr/arama?q=ay%20%C3%A7ekirde%C4%9Fi"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Ay Çekirdeği")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Ayçekirdeği|Ayçekirdek|Şimşek")]



        data=veriekle("Ay Çekirdeği",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search/?q=kabak+%C3%A7ekirde%C4%9Fi%3AbestSeller%3AinStockFlag%3Atrue&text=kabak+%C3%A7ekirde%C4%9Fi#"]
        migros=["https://www.migros.com.tr/arama?q=kabak%20%C3%A7ekirde%C4%9Fi&sayfa=1&kategori=70651"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kabak Çekirdeği")
        

        data=veriekle("Kabak Çekirdeği",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=Kuru+%C3%9Cz%C3%BCm%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1519"]
        migros=["https://www.migros.com.tr/arama?q=Kuru%20%C3%9Cz%C3%BCm"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kuru Üzüm")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("üzüm|Üzüm")]

        data=veriekle("Kuru Üzüm",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=kuru+kay%C4%B1s%C4%B1%3AbestSeller%3AproductPrimaryCategoryCode%3A1519%3AinStockFlag%3Atrue&text=kuru+kay%C4%B1s%C4%B1#"]
        migros=["https://www.migros.com.tr/arama?q=kuru%20kay%C4%B1s%C4%B1"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kuru Kayısı")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("kayısı|Kayısı")]
        


        data=veriekle("Kuru Kayısı",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=%C3%A7arliston%3AbestSeller%3AproductPrimaryCategoryCode%3A1027%3AinStockFlag%3Atrue&text=%C3%A7arliston#"]
        migros=["https://www.migros.com.tr/arama?q=%C3%A7arliston&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Çarliston Biber")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Çarliston|çarliston")]

        data=veriekle("Çarliston Biber",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=Dolmal%C4%B1k+Biber%3AbestSeller%3AproductPrimaryCategoryCode%3A1027"]
        migros=["https://www.migros.com.tr/arama?q=Dolmal%C4%B1k%20Biber&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Dolmalık Biber")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Dolma|Dolmalık")]


        data=veriekle("Dolmalık Biber",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=Sivri+Biber%3AbestSeller%3AproductPrimaryCategoryCode%3A1027%3AinStockFlag%3Atrue&text=Sivri+Biber#"]
        migros=["https://www.migros.com.tr/arama?q=Sivri%20Biber"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Sivri Biber")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("sivri|Sivri")]

        data=veriekle("Sivri Biber",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/search/?q=dereotu%3AbestSeller%3AinStockFlag%3Atrue&text=dereotu#"]
        migros=["https://www.migros.com.tr/arama?q=dereotu"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Dereotu")


        data=veriekle("Dereotu",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=domates%3AbestSeller%3AinStockFlag%3Atrue&text=domates#"]
        migros=["https://www.migros.com.tr/arama?q=domates&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Domates")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Salçası", regex=True)]
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("kg", regex=True)]

            data=veriekle("Domates",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=taze+fasulye%3AbestSeller%3AinStockFlag%3Atrue%3AproductPrimaryCategoryCode%3A1031"]
        migros=["https://www.migros.com.tr/arama?q=taze%20fasulye&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Taze Fasulye")


        data=veriekle("Taze Fasulye",data,urunler_df)


        def scrape_migros_products(pages):
            product_data = []
            
            for url in pages:
                driver.get(url)

                try:
                    # Wait for the product names to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.product-name'))
                    )

                    # Get all product cards
                    product_cards = driver.find_elements(By.CSS_SELECTOR, 'sm-list-page-item')

                    for product_card in product_cards:
                        # Check if the product is sponsored by looking for a specific sponsored class or attribute
                        if "external-list-item" in product_card.get_attribute('class').lower():
                            print("Skipping sponsored product.")
                            continue  # Skip this sponsored product

                        try:
                            # Extract the product name
                            product_name = product_card.find_element(By.CSS_SELECTOR, '.product-name').text.strip()

                            # Try to extract the price from multiple possible locations
                            price_element = None
                            try:
                                # First attempt using the primary price selector
                                price_element = product_card.find_element(By.CSS_SELECTOR, '.price-new')
                            except Exception:
                                try:
                                    # If not found, try another potential selector for the price
                                    price_element = product_card.find_element(By.CSS_SELECTOR, '.price .amount')
                                except Exception:
                                    print(f"Price not found for product: {product_name}")
                                    continue  # Skip if no price is found

                            if price_element:
                                product_price_text = price_element.text.strip()
                                product_price = clean_price(product_price_text)  # Convert price to float
                                # Append product name and price to the list
                                product_data.append({"Product Name": product_name, "Price (TRY)": product_price})
                                print(f"Product: {product_name}, Price: {product_price} TRY")

                        except Exception as e:
                            print(f"Error scraping a product on page: {e}")

                except Exception as e:
                    print(f"Error loading products on page: {e}")

                # Sleep to avoid being detected as a bot
                sleep(2)
            
            return product_data



        carrefour=["https://www.carrefoursa.com/search?q=havu%C3%A7%3AbestSeller%3Acategory%3A1014"]
        migros=["https://www.migros.com.tr/arama?q=havu%C3%A7&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Havuç")


        data=veriekle("Havuç",data,urunler_df)


        try:
            carrefour=["https://www.carrefoursa.com/search?q=%C4%B1spanak%3AbestSeller%3AproductPrimaryCategoryCode%3A1030%3AinStockFlag%3Atrue&text=%C4%B1spanak#"]
            migros=["https://www.migros.com.tr/arama?q=%C4%B1spanak&sayfa=1&kategori=2&markalar=492&sirala=akilli-siralama"]
            options = Options()
            options.headless = False 


            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            urunler_df=vericek(carrefour,migros,"Ispanak")
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Ispanak")]

            data=veriekle("Ispanak",data,urunler_df)
        except:
            pass



        carrefour=["https://www.carrefoursa.com/search/?q=kabak%3AbestSeller%3AinStockFlag%3Atrue&text=kabak#"]
        migros=["https://www.migros.com.tr/arama?q=kabak"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kabak")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Sakız|Dolmalık|Adet")]

        data=veriekle("Kabak",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=karnabahar%3AbestSeller%3Acategory%3A1014%3AinStockFlag%3Atrue&text=karnabahar#"]
        migros=["https://www.migros.com.tr/arama?q=karnabahar&sayfa=1&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Karnabahar")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Karnabahar")]


        data=veriekle("Karnabahar",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=kuru+so%C4%9Fan%3AbestSeller%3AproductPrimaryCategoryCode%3A1033%3AinStockFlag%3Atrue&text=kuru+so%C4%9Fan#"]
        migros=["https://www.migros.com.tr/arama?q=kuru%20so%C4%9Fan"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kuru Soğan")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("soğan|Soğan")]

        data=veriekle("Kuru Soğan",data,urunler_df)



        migros=["https://www.migros.com.tr/arama?q=beyaz%20lahana&sayfa=1&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Beyaz Lahana")



        data=veriekle("Beyaz Lahana",data,urunler_df)



        migros=["https://www.migros.com.tr/arama?q=k%C4%B1rm%C4%B1z%C4%B1%20lahana&sayfa=1&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Kırmızı Lahana")


        data=veriekle("Kırmızı Lahana",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=mantar%3AbestSeller%3AinStockFlag%3Atrue&text=mantar#"]
        migros=["https://www.migros.com.tr/arama?q=mantar&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Mantar")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Mantar|mantar|mantarı|Mantarı")]
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Çorba|Pano|İstiridye|Salatası")]

        data=veriekle("Mantar",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=k%C4%B1v%C4%B1rc%C4%B1k%3AbestSeller%3AinStockFlag%3Atrue&text=k%C4%B1v%C4%B1rc%C4%B1k#"]
        migros=["https://www.migros.com.tr/arama?q=k%C4%B1v%C4%B1rc%C4%B1k&sayfa=1&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kıvırcık")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("kıvırcık|Kıvırcık")]
        data=veriekle("Kıvırcık",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search/?q=maydonoz%3AbestSeller%3AinStockFlag%3Atrue&text=maydonoz#"]
        migros=["https://www.migros.com.tr/arama?q=maydonoz&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Maydanoz")

        data=veriekle("Maydanoz",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=nane%3AbestSeller%3AproductPrimaryCategoryCode%3A1030%3AinStockFlag%3Atrue&text=nane#"]
        migros=["https://www.migros.com.tr/arama?q=nane&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Nane")

        data=veriekle("Nane",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=patl%C4%B1can%3AbestSeller%3AproductPrimaryCategoryCode%3A1031%3AinStockFlag%3Atrue&text=patl%C4%B1can#"]
        migros=["https://www.migros.com.tr/arama?q=patl%C4%B1can&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Patlıcan")

        data=veriekle("Patlıcan",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search/?q=p%C4%B1rasa%3AbestSeller%3AinStockFlag%3Atrue&text=p%C4%B1rasa#"]
        migros=["https://www.migros.com.tr/arama?q=p%C4%B1rasa"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Pırasa")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("pırasa|Pırasa")]

        data=veriekle("Pırasa",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search/?q=roka%3AbestSeller%3AinStockFlag%3Atrue&text=roka#"]
        migros=["https://www.migros.com.tr/arama?q=roka&sayfa=1&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Roka")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("roka|Roka")]
        data=veriekle("Roka",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=salatal%C4%B1k%3AbestSeller%3Acategory%3A1014%3AinStockFlag%3Atrue&text=salatal%C4%B1k#"]
        migros=["https://www.migros.com.tr/arama?q=salatal%C4%B1k&sayfa=1&markalar=492&sirala=akilli-siralama&kategori=102"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Salatalık")

        data=veriekle("Salatalık",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/kuru-sarimsak-kg-p-30024962"]
        migros=["https://www.migros.com.tr/arama?q=sar%C4%B1msak&sayfa=1&kategori=2"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Sarımsak")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Sarımsak", regex=True)]

            data=veriekle("Sarımsak",data,urunler_df)






        migros=["https://www.migros.com.tr/arama?q=k%C4%B1rm%C4%B1z%C4%B1%20turp"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Kırmızı Turp")
        data=veriekle("Kırmızı Turp",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=patates%3AbestSeller%3AproductPrimaryCategoryCode%3A1033%3AinStockFlag%3Atrue&text=patates#"]
        migros=["https://www.migros.com.tr/arama?q=patates&sayfa=1&kategori=1014&markalar=492&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Patates")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Sarımsak|Soğan", regex=True)]
            data=veriekle("Patates",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=kuru+fasulye%3AbestSeller%3AinStockFlag%3Atrue%3Acategory%3A1110"]
        migros=["https://www.migros.com.tr/arama?q=kuru%20fasulye&sayfa=1&kategori=5"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kuru Fasulye")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("fasulye|Fasulye")]

            data=veriekle("Kuru Fasulye",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=nohut%3AbestSeller%3AproductPrimaryCategoryCode%3A1152%3AinStockFlag%3Atrue&text=nohut#"]
        migros=["https://www.migros.com.tr/arama?q=nohut&sayfa=1&kategori=10136"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Nohut")
        data=veriekle("Nohut",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=mercimek%3AbestSeller%3AproductPrimaryCategoryCode%3A1152%3AinStockFlag%3Atrue&text=mercimek#"]
        migros=["https://www.migros.com.tr/arama?q=mercimek&sayfa=1&kategori=70601"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Mercimek")
        data=veriekle("Mercimek",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/diger-sebze/c/1193?q=%3AbestSeller&show=All","https://www.carrefoursa.com/yesil-sebze/c/1187?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10324",
                "https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10304",
                "https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10325",
                "https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10328",
                "https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10326",
                "https://www.migros.com.tr/arama?q=konserve&sayfa=1&kategori=10322"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Konserveler")
        data=veriekle("Konserveler",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=tur%C5%9Fu%3AbestSeller%3AinStockFlag%3Atrue&text=tur%C5%9Fu#"]
        migros=["https://www.migros.com.tr/arama?q=tur%C5%9Fu&sayfa=1&kategori=1108&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=tur%C5%9Fu&sayfa=2&kategori=1108&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Turşu")
        data=veriekle("Turşu",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/salca/c/1180?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/arama?q=sal%C3%A7a&sayfa=1&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=sal%C3%A7a&sayfa=2&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Salça")
        data=veriekle("Salça",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/zeytin/c/1356?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/arama?q=zeytin&sayfa=1&kategori=113&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=zeytin&sayfa=2&kategori=113&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=zeytin&sayfa=3&kategori=113&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=zeytin&sayfa=4&kategori=113&sirala=akilli-siralama"]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Zeytin")
        data=veriekle("Zeytin",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/cipsler/c/1552?q=%3AbestSeller%3Acategory%3A1552%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=cips&sayfa=1&kategori=1088&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=cips&sayfa=2&kategori=1088&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=cips&sayfa=3&kategori=1088&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=cips&sayfa=4&kategori=1088&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=cips&sayfa=5&kategori=1088&sirala=akilli-siralama",
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Cipsler")
        data=veriekle("Cipsler",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=Toz+%C5%9Eeker%3AbestSeller%3AinStockFlag%3Atrue&text=Toz+%C5%9Eeker#"]
        migros=["https://www.migros.com.tr/arama?q=Toz%20%C5%9Eeker&sayfa=1&kategori=172"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Toz Şeker")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Toz", regex=True)]
            data=veriekle("Toz Şeker",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=k%C3%BCp+%C5%9Feker%3AbestSeller%3AinStockFlag%3Atrue&text=k%C3%BCp+%C5%9Feker#"]
        migros=["https://www.migros.com.tr/arama?q=k%C3%BCp%20%C5%9Feker&sayfa=1&kategori=1347"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kesme Şeker")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Küp", regex=True)]
            data=veriekle("Kesme Şeker",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=re%C3%A7el%3AbestSeller%3AinStockFlag%3Atrue&text=re%C3%A7el#"]
        migros=["https://www.migros.com.tr/arama?q=re%C3%A7el&sayfa=1&kategori=10107&sirala=akilli-siralama","https://www.migros.com.tr/arama?q=re%C3%A7el&sayfa=2&kategori=10107&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Reçel")
        data=veriekle("Reçel",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/ballar/c/1362?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=bal&sayfa=1&kategori=1056&sirala=akilli-siralama","https://www.migros.com.tr/arama?q=bal&sayfa=2&kategori=1056&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Bal")
        data=veriekle("Bal",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=pekmez%3AbestSeller&show=All"]
        migros=["https://www.migros.com.tr/arama?q=pekmez&sayfa=1&kategori=10096"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Pekmez")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Pekmez|Pekmezi", regex=True)]
            data=veriekle("Pekmez",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=tahin+helva%3AbestSeller%3AproductPrimaryCategoryCode%3A1374%3AinStockFlag%3Atrue&text=tahin+helva#"]
        migros=["https://www.migros.com.tr/arama?q=tahin%20helvas%C4%B1&sayfa=1&kategori=10097"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Tahin Helvası")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Helvası|Helva", regex=True)]
            data=veriekle("Tahin Helvası",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/search?q=f%C4%B1nd%C4%B1k+ezmesi%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=f%C4%B1nd%C4%B1k%20ezmesi&sayfa=1&kategori=10104"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Fındık Ezmesi")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Fındık Ezmesi", regex=True)]
            data=veriekle("Fındık Ezmesi",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=tablet+%C3%A7ikolata%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=tablet%20%C3%A7ikolata"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Çikolata Tablet")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Tablet|Kare", regex=True)]
            data=veriekle("Çikolata Tablet",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=krem+%C3%A7ikolata%3AbestSeller%3AproductPrimaryCategoryCode%3A1381%3AinStockFlag%3Atrue&text=krem+%C3%A7ikolata#"]
        migros=["https://www.migros.com.tr/kakao-findik-kremalari-c-2779?sayfa=1"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Çikolata Krem")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Ezmesi", regex=True)]
            data=veriekle("Çikolata Krem",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=lokum%3AbestSeller%3AproductPrimaryCategoryCode%3A1494%3AinStockFlag%3Atrue&text=lokum#"]
        migros=["https://www.migros.com.tr/arama?q=lokum&sayfa=1&kategori=10268&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=lokum&sayfa=2&kategori=10268&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=lokum&sayfa=3&kategori=10268&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=lokum&sayfa=4&kategori=10268&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=lokum&sayfa=5&kategori=10268&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Lokum")
        data=veriekle("Lokum",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/search?q=sak%C4%B1z%3AbestSeller%3AproductPrimaryCategoryCode%3A1501%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=sak%C4%B1z&sayfa=1&kategori=1091&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=sak%C4%B1z&sayfa=2&kategori=1091&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Sakız")
        data=veriekle("Sakız",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/sekerleme/c/1494?q=%3AbestSeller%3Acategory%3ABRN-1949%3Acategory%3ABRN-2504%3Acategory%3ABRN-3185%3Acategory%3ABRN-2125%3Acategory%3ABRN-3091%3Acategory%3ABRN-2999%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/yumusak-seker-c-2818?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/yumusak-seker-c-2818?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/yumusak-seker-c-2818?sayfa=3&sirala=onerilenler",
                "https://www.migros.com.tr/draje-sekerleme-c-2816?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/draje-sekerleme-c-2816?sayfa=2&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kağıtlı Şeker")
        data=veriekle("Kağıtlı Şeker",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/kap-dondurma/c/1261?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All",
                "https://www.carrefoursa.com/tek-dondurma/c/1266?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/dondurma-c-41b?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/dondurma-c-41b?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/dondurma-c-41b?sayfa=3&sirala=onerilenler",
                "https://www.migros.com.tr/dondurma-c-41b?sayfa=4&sirala=onerilenler",
                "https://www.migros.com.tr/dondurma-c-41b?sayfa=5&sirala=onerilenler",
                "https://www.migros.com.tr/dondurma-c-41b?sayfa=6&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Dondurma")
        data=veriekle("Dondurma",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/baharat/c/1167?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/arama?q=baharat&sayfa=1&kategori=10180&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=baharat&sayfa=2&kategori=10180&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=baharat&sayfa=3&kategori=10180&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=baharat&sayfa=4&kategori=10180&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=baharat&sayfa=5&kategori=10180&sirala=akilli-siralama",
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Baharat")
        data=veriekle("Baharat",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/tuz/c/1166?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/tuz-c-436?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/tuz-c-436?sayfa=2&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Tuz")
        data=veriekle("Tuz",data,urunler_df)





        carrefour=["https://www.carrefoursa.com/search?q=kabartma%3AbestSeller%3AproductPrimaryCategoryCode%3A1282%3AinStockFlag%3Atrue&text=kabartma#"]
        migros=["https://www.migros.com.tr/kabartma-tozu-sekerli-vanilin-c-2893"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kabartma Maddeleri")
        data=veriekle("Kabartma Maddeleri",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search?q=sirke%3AbestSeller%3AproductPrimaryCategoryCode%3A1219%3AinStockFlag%3Atrue&text=sirke#"]
        migros=["https://www.migros.com.tr/arama?q=sirke&sayfa=1&kategori=10319&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=sirke&sayfa=2&kategori=10319&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Sirke")
        data=veriekle("Sirke",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/search/?q=ket%C3%A7ap%3AbestSeller%3AinStockFlag%3Atrue&text=ket%C3%A7ap#"]
        migros=["https://www.migros.com.tr/arama?q=ket%C3%A7ap&sayfa=1&kategori=10311"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Ketçap")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Mayonez", regex=True)]
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Ketçap")]

            data=veriekle("Ketçap",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=mayonez%3AbestSeller%3AproductPrimaryCategoryCode%3A1212%3AinStockFlag%3Atrue&text=mayonez#"]
        migros=["https://www.migros.com.tr/arama?q=mayonez&sayfa=1&kategori=10312"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Mayonez")
        data=veriekle("Mayonez",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/tahin-pekmez-helva/c/1374?q=%3AbestSeller%3Acategory%3A1310%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/arama?q=tahin&sayfa=1&kategori=10095"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Tahin")
        if urunler_df is not None:
            urunler_df=urunler_df[urunler_df["Ürün"].str.contains("Tahin", regex=True)]
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Pekmezi|Helva", regex=True)]
            data=veriekle("Tahin",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/hazir-corbalar/c/1224?q=%3AbestSeller&show=All"]
        migros=["https://www.migros.com.tr/arama?q=haz%C4%B1r%20%C3%A7orba&sayfa=1&kategori=1103&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=haz%C4%B1r%20%C3%A7orba&sayfa=2&kategori=1103&sirala=akilli-siralama"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Hazır Çorbalar")
        data=veriekle("Hazır Çorbalar",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/hazirlanacak-tatlilar/c/1300?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/toz-tatlilar-c-287d?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/toz-tatlilar-c-287d?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/toz-tatlilar-c-287d?sayfa=3&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Hazır Pakette Toz Tatlılar (Puding)")
        data=veriekle("Hazır Pakette Toz Tatlılar (Puding)",data,urunler_df)





        carrefour=["https://www.carrefoursa.com/search/?q=t%C3%BCrk+kahvesi%3AbestSeller%3AinStockFlag%3Atrue&text=t%C3%BCrk+kahvesi#"]
        migros=["https://www.migros.com.tr/arama?q=t%C3%BCrk%20kahvesi&sayfa=1&sirala=akilli-siralama&kategori=10436"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kahve")
        data=veriekle("Kahve",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/kahve/c/1467?q=%3AbestSeller%3Acategory%3A1467%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/hazir-kahve-c-11222?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/hazir-kahve-c-11222?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/hazir-kahve-c-11222?sayfa=3&sirala=onerilenler",
                "https://www.migros.com.tr/hazir-kahve-c-11222?sayfa=4&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Hazır Kahve")
        if urunler_df is not None:
            urunler_df=urunler_df[~urunler_df["Ürün"].str.contains("Türk", regex=True)]
            data=veriekle("Hazır Kahve",data,urunler_df)






        migros=["https://www.migros.com.tr/arama?q=%C3%A7ay&sayfa=1&kategori=10433&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=%C3%A7ay&sayfa=2&kategori=10433&sirala=akilli-siralama",
                "https://www.migros.com.tr/arama?q=%C3%A7ay&sayfa=1&kategori=70174",
                "https://www.migros.com.tr/arama?q=%C3%A7ay&sayfa=1&kategori=70175"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Çay")
        data=veriekle("Çay",data,urunler_df)



        migros=["https://www.migros.com.tr/bitki-cayi-c-28c0?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/bitki-cayi-c-28c0?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/bitki-cayi-c-28c0?sayfa=3&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Bitki ve Meyve Çayı (Poşet)")
        data=veriekle("Bitki ve Meyve Çayı (Poşet)",data,urunler_df)





        migros=["https://www.migros.com.tr/arama?q=kakaolu%20s%C3%BCt&sayfa=1&kategori=108"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Kakaolu Toz İçecekler")
        data=veriekle("Kakaolu Toz İçecekler",data,urunler_df)



        carrefour=["https://www.carrefoursa.com/sular/c/1411?q=%3AbestSeller%3AinStockFlag%3Atrue&show=All"]
        migros=["https://www.migros.com.tr/su-c-84?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/su-c-84?sayfa=2&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Su")
        data=veriekle("Su",data,urunler_df)





        carrefour=["https://www.carrefoursa.com/maden-sulari/c/1412?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/maden-suyu-c-85?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/maden-suyu-c-85?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/maden-suyu-c-85?sayfa=3&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Maden Suyu ve Sodası")
        data=veriekle("Maden Suyu ve Sodası",data,urunler_df)








        carrefour=["https://www.carrefoursa.com/search?q=gazoz%3AbestSeller&show=All"]
        migros=["https://www.migros.com.tr/gazoz-c-467?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/gazoz-c-467?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/gazoz-c-467?sayfa=3&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Gazoz Meyveli")
        data=veriekle("Gazoz Meyveli",data,urunler_df)










        carrefour=["https://www.carrefoursa.com/kola/c/1419?q=%3AbestSeller%3AinStockFlag%3Atrue&text=#"]
        migros=["https://www.migros.com.tr/kola-c-465?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/kola-c-465?sayfa=2&sirala=onerilenler"
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Kola")
        data=veriekle("Kola",data,urunler_df)





        carrefour=["https://www.carrefoursa.com/search?q=so%C4%9Fuk+%C3%A7ay%3AbestSeller&show=All"]
        migros=["https://www.migros.com.tr/soguk-cay-c-28be?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/soguk-cay-c-28be?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/soguk-cay-c-28be?sayfa=3&sirala=onerilenler",
                
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Soğuk Çay")
        data=veriekle("Soğuk Çay",data,urunler_df)








        carrefour=["https://www.carrefoursa.com/search?q=ayran%3AbestSeller&show=All"]
        migros=["https://www.migros.com.tr/ayran-c-47a?sayfa=1",
                
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Ayran")
        data=veriekle("Ayran",data,urunler_df)




        carrefour=["https://www.carrefoursa.com/search?q=meyve+suyu%3AbestSeller%3AinStockFlag%3Atrue&text=meyve+suyu#"]
        migros=["https://www.migros.com.tr/meyve-suyu-c-46c?sayfa=1&sirala=onerilenler",
                "https://www.migros.com.tr/meyve-suyu-c-46c?sayfa=2&sirala=onerilenler",
                "https://www.migros.com.tr/meyve-suyu-c-46c?sayfa=3&sirala=onerilenler",
                "https://www.migros.com.tr/meyve-suyu-c-46c?sayfa=4&sirala=onerilenler",
                "https://www.migros.com.tr/meyve-suyu-c-46c?sayfa=5&sirala=onerilenler",
                
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour,migros,"Meyve Suyu")
        data=veriekle("Meyve Suyu",data,urunler_df)








        migros=["https://www.migros.com.tr/arama?q=tulum%20peyniri&sayfa=1&kategori=10036",
                
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour="",migros=migros,name="Tulum Peyniri")
        data=veriekle("Tulum Peyniri",data,urunler_df)


        carrefour=["https://www.carrefoursa.com/search?q=kakao%3AbestSeller%3AproductPrimaryCategoryCode%3A1282%3AinStockFlag%3Atrue&text=kakao#"]
        migros=["https://www.migros.com.tr/arama?q=kakao&sayfa=1&kategori=1118"
                
        ]
        options = Options()
        options.headless = False 


        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        urunler_df=vericek(carrefour=carrefour,migros=migros,name="Kakao")
        data=veriekle("Kakao",data,urunler_df)


        


        # Function to convert numeric columns to float and drop rows where conversion fails
        def convert_to_float_and_drop_non_numeric(df):
            numeric_columns = df.columns[1:]  # Exclude the 'Ürün' column
            # Attempt to convert all numeric columns to float
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Drop rows where all numeric columns have NaN (i.e., non-convertible rows)
            df_cleaned = df.dropna(subset=numeric_columns, how='all')
            return df_cleaned

        # Apply the conversion and cleaning process
        df_cleaned = convert_to_float_and_drop_non_numeric(data.copy())

        # Function to fill NaN values from both right to left and left to right
        def fill_nan_both_directions(row):

            filled_row = row[::-1].fillna(method='ffill')[::-1]

            filled_row = filled_row.fillna(method='ffill')
            return filled_row

        def fill_nan_both_directions_corrected(df):
            numeric_columns = df.columns[1:]  # Exclude the 'Ürün' column
            df[numeric_columns] = df[numeric_columns].apply(fill_nan_both_directions, axis=1)
            return df


        df_filled_corrected = fill_nan_both_directions_corrected(df_cleaned)


        ağırlıklar=pd.read_csv("ağırlıklar.csv")
        ağırlıklar=ağırlıklar.set_index(ağırlıklar["Ürün"])
        ağırlıklar=ağırlıklar.drop("Ürün",axis=1)



        gfe=pd.read_csv("gfe.csv")
        gfe=gfe.set_index(pd.to_datetime(gfe["Tarih"]))
        gfe=gfe.drop("Tarih",axis=1)



        data1=df_filled_corrected.copy()
        degisim=(((data1.iloc[:,-1]/data1.iloc[:,1])-1)*100).fillna(0).groupby(level=0).mean().sort_index()



        ağırlıklar["Değişim"]=degisim



        ağırlıklar[f"Endeks_{bugün}"]=ağırlıklar["Endeks_2024-10-11"]*(1+(ağırlıklar["Değişim"]/100))

        ağırlıklar[f"Ağırlıklı Endeks_{bugün}"]=ağırlıklar[f"Endeks_{bugün}"]*ağırlıklar["Ağırlık"]
        gfe.loc[pd.to_datetime(bugün)]=ağırlıklar[f"Ağırlıklı Endeks_{bugün}"].sum()
        gfe.to_csv("gfe.csv",index=True)


        endeks_sutunlari = ağırlıklar.filter(like='Endeks_')
        endeksler = [col for col in ağırlıklar.columns if col.startswith('Endeks_')]
        ağırlıklar[endeksler].to_csv("endeksler.csv",index=True)


        ağırlıklar.to_csv("ağırlıklar.csv",index=True)


        data1.to_csv("sepet.csv")

        tarih=datetime.now().strftime("%Y-%m-%d %H:%M")
        tarih=pd.DataFrame({"Current DateTime": [tarih]})
        tarih.to_csv("tarih.csv")

        import os
        import subprocess
        from datetime import datetime
        import time
        import git
        from git import Repo
        import os
        repo_dir = ".git"  # Buraya Git deposunun yolunu girin

        def git_add_commit_push():
            try:
                # Repo nesnesini oluştur
                repo = Repo(repo_dir)
                assert not repo.bare

                # Git add: tüm değişiklikleri ekliyoruz
                repo.git.add(A=True)  # A=True ile tüm dosyalar eklenir

                # Commit işlemi
                commit_message = "update"
                repo.index.commit(commit_message)
                print(f"Commit işlemi başarılı: {commit_message}")

                # Push işlemi
                origin = repo.remote(name='origin')
                origin.push()
                print("Push işlemi başarılı.")

            except Exception as e:
                print(f"Git işlemi sırasında hata oluştu: {e}")

            # Ana fonksiyonu çağırma
        git_add_commit_push()

    except Exception as e:
            print(e)
            pass
    


