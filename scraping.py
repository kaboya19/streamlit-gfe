import requests

url = "https://api.marketfiyati.org.tr/api/v2/searchByCategories"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://marketfiyati.org.tr/",
    "Origin": "https://marketfiyati.org.tr",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "menuCategory": True,
    "keywords": "Meyve ve Sebze",
    "pages": 0,
    "size": 24,
    "latitude": 41.05782553985235,
    "longitude": 28.91199587449858,
    "distance": 1,
    "depots": [
        "bim-B543", "sok-7168", "a101-H553", "a101-G663", "sok-13161",
        "sok-7270", "a101-1508", "sok-11296"
    ]
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status code: {response.status_code}")
if response.ok:
    data = response.json()
    print(data)
else:
    print("Hata oluştu:", response.text)
