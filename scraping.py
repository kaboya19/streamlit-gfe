import pandas as pd
import requests
import time

def fetch_data(arama_terimi, lat, lng, distance=500, page=1):
    try:
        url = (
            f"https://roninbase.dev/api.php?"
            f"search={arama_terimi}&distance={distance}&page={page}"
            f"&lat={lat}&long={lng}"
        )
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['lat'] = lat
            df['lng'] = lng
            return df
        else:
            print(f"Hata {response.status_code} - {url}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Hata oluştu ({lat}, {lng}): {e}")
        return pd.DataFrame()

def market_fiyat_api(arama_terimi, konum_listesi, distance=500, page=1, bekleme_saniye=1):
    all_results = []

    for _, row in konum_listesi.iterrows():
        df = fetch_data(arama_terimi, row.lat, row.lng, distance, page)
        if not df.empty:
            df['il_adi'] = row.get('ilce_adi', '')
            all_results.append(df)
        time.sleep(bekleme_saniye)  # API'yı aşırı yüklememek için kısa bekleme

    if all_results:
        return pd.concat(all_results, ignore_index=True)
    else:
        return pd.DataFrame()



























df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="pirinç")
df.index=["Pirinç"]*len(df)
df.to_csv(f"{bugün}/pirinç.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
urunler_df.index=["Pirinç"]*len(urunler_df)
data=veriekle("Pirinç",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="un")
df=df[df["categories"].str.contains("sade unlar",case=False)]
df=pd.concat([df,market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="buğday unu")],axis=0)
df.index=["Buğday Unu"]*len(df)
df.to_csv(f"{bugün}/buğdayunu.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
urunler_df.index=["Buğday Unu"]*len(urunler_df)
data=veriekle("Buğday Unu",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="bebek sütü")
df.index=["Bebek Sütü (Toz Karışım)"]*len(df)
df.to_csv(f"{bugün}/bebeksütü.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
urunler_df.index=["Bebek Sütü (Toz Karışım)"]*len(urunler_df)
data=veriekle("Bebek Sütü (Toz Karışım)",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="bulgur")
df.index=["Bulgur"]*len(df)
df.to_csv(f"{bugün}/bulgur.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Bulgur",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="ekmek")
df.index=["Ekmek"]*len(df)
df.to_csv(f"{bugün}/ekmek.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ekmek",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="bisküvi")
df.index=["Bisküvi"]*len(df)
df.to_csv(f"{bugün}/bisküvi.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Bisküvi",data,urunler_df)
def market(ürün,data,filter=""):
    df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi=ürün)
    if filter!="":
        df=df[df["categories"].str.contains(filter,case=False)]
    df.index=[ürün]*len(df)
    df.to_csv(f"{bugün}/{ürün}.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price"]]
    urunler_df.columns=["Ürün",str(bugün)]
    data=veriekle(f"{ürün}",data,urunler_df)
    return data
data=market("Kraker",data)
data=market("Gofret",data)
data=market("Pasta",data,filter="pasta")
data=market("Kek",data)
data=market("Baklava",data,filter="fıstıklı")

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Yufka")
df.index=["Ekmek Hamuru (Yufka)"]*len(df)
df.to_csv(f"{bugün}/Ekmek Hamuru (Yufka).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ekmek Hamuru (Yufka)",data,urunler_df)

data=market("Makarna",data)
data=market("Şehriye",data)
data=market("Tahıl Gevreği",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Dana Kıyma")
df1=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Dana Kuşbaşı")
df2=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Dana Köfte")
df=pd.concat([df,df1,df2],axis=0)
df.index=["Dana Eti"]*len(df)
df.to_csv(f"{bugün}/Dana Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Dana Eti",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kuzu Kıyma")
df1=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kuzu Kuşbaşı")
df2=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kuzu Köfte")
df=pd.concat([df,df1,df2],axis=0)
df.index=["Kuzu Eti"]*len(df)
df.to_csv(f"{bugün}/Kuzu Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuzu Eti",data,urunler_df)


df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Piliç")
df=df[df["categories"].str.contains("Kümes Hayvanları|piliç",case=False)]
df.index=["Tavuk Eti"]*len(df)
df.to_csv(f"{bugün}/Tavuk Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Tavuk Eti",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="kokoreç")
df.index=["Sakatat"]*len(df)
df.to_csv(f"{bugün}/Sakatat.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Sakatat",data,urunler_df)

data=market("Sucuk",data)
data=market("Salam",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="kavurma")
df=df[df["categories"].str.contains("konserve|dondurulmuş",case=False)]
df.index=["Hazır Et Yemekleri"]*len(df)
df.to_csv(f"{bugün}/Hazır Et Yemekleri.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Et Yemekleri",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="balık")
df=df[df["categories"].str.contains("dondurulmuş",case=False)]
df.index=["Balık"]*len(df)
df.to_csv(f"{bugün}/Balık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Balık",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="balık")
df=df[df["categories"].str.contains("konserve",case=False)]
df.index=["Konserve Balık"]*len(df)
df.to_csv(f"{bugün}/Konserve Balık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Konserve Balık",data,urunler_df)


data=market("Süt",data)
data=market("Yoğurt",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="sütlü tatlı")
df.index=["Hazır Sütlü Tatlılar"]*len(df)
df.to_csv(f"{bugün}/Hazır Sütlü Tatlılar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Sütlü Tatlılar",data,urunler_df)

data=market("Beyaz Peynir",data)
data=market("Kaşar Peyniri",data)
data=market("Tulum Peyniri",data)
data=market("Krem Peynir",data)
data=market("Yumurta",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Tereyağı")
df.index=["Tereyağı (Kahvaltılık)"]*len(df)
df.to_csv(f"{bugün}/Tereyağı (Kahvaltılık).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Tereyağı (Kahvaltılık)",data,urunler_df)

data=market("Margarin",data)
data=market("Zeytinyağı",data)
data=market("Ayçiçek Yağı",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="portakal")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler",case=False)]
df.index=["Portakal"]*len(df)
df.to_csv(f"{bugün}/Portakal.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Portakal",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Üzüm")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Üzüm"]*len(df)
df.to_csv(f"{bugün}/Üzüm.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Üzüm",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Armut")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Armut"]*len(df)
df.to_csv(f"{bugün}/Armut.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Armut",data,urunler_df)


df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Ayva")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Ayva"]*len(df)
df.to_csv(f"{bugün}/Ayva.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ayva",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Çilek")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Çilek"]*len(df)
df.to_csv(f"{bugün}/Çilek.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Çilek",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Elma")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Elma"]*len(df)
df.to_csv(f"{bugün}/Elma.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Elma",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Karpuz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Karpuz"]*len(df)
df.to_csv(f"{bugün}/Karpuz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Karpuz",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kavun")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Kavun"]*len(df)
df.to_csv(f"{bugün}/Kavun.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kavun",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kivi")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Kivi"]*len(df)
df.to_csv(f"{bugün}/Kivi.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kivi",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Limon")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Limon"]*len(df)
df.to_csv(f"{bugün}/Limon.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Limon",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Mandalina")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Mandalina"]*len(df)
df.to_csv(f"{bugün}/Mandalina.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mandalina",data,urunler_df)


df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Muz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Muz"]*len(df)
df.to_csv(f"{bugün}/Muz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Muz",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Nar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler|meyve Sebze",case=False)]
df.index=["Nar"]*len(df)
df.to_csv(f"{bugün}/Nar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nar",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Şeftali")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler|meyve Sebze",case=False)]
df.index=["Şeftali"]*len(df)
df.to_csv(f"{bugün}/Şeftali.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Şeftali",data,urunler_df)

data=market("Badem İçi",data)
data=market("Ceviz İçi",data)
data=market("Fındık İçi",data)
data=market("Yer Fıstığı",data,filter="kuruyemiş")
data=market("Antep Fıstığı",data,filter="kuruyemiş")
data=market("Leblebi",data)
data=market("Ay Çekirdeği",data)
data=market("Kabak Çekirdeği",data)
data=market("Kuru Üzüm",data)
data=market("Kuru Kayısı",data)
data=market("Çarliston Biber",data)
data=market("Dolmalık Biber",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Sivri Biber")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Sivri Biber"]*len(df)
df.to_csv(f"{bugün}/Sivri Biber.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Sivri Biber",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Dereotu")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Dereotu"]*len(df)
df.to_csv(f"{bugün}/Dereotu.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Dereotu",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Domates")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Domates"]*len(df)
df.to_csv(f"{bugün}/Domates.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Domates",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Fasulye")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Taze Fasulye"]*len(df)
df.to_csv(f"{bugün}/Taze Fasulye.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Taze Fasulye",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Havuç")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Havuç"]*len(df)
df.to_csv(f"{bugün}/Havuç.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Havuç",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Ispanak")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Ispanak"]*len(df)
df.to_csv(f"{bugün}/Ispanak.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ispanak",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kabak")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kabak"]*len(df)
df.to_csv(f"{bugün}/Kabak.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kabak",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Karnabahar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Karnabahar"]*len(df)
df.to_csv(f"{bugün}/Karnabahar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Karnabahar",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Soğan")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kuru Soğan"]*len(df)
df.to_csv(f"{bugün}/Kuru Soğan.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuru Soğan",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Beyaz Lahana")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Beyaz Lahana"]*len(df)
df.to_csv(f"{bugün}/Beyaz Lahana.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Beyaz Lahana",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kırmızı Lahana")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kırmızı Lahana"]*len(df)
df.to_csv(f"{bugün}/Kırmızı Lahana.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kırmızı Lahana",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Mantar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Mantar"]*len(df)
df.to_csv(f"{bugün}/Mantar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mantar",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kıvırcık")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kıvırcık"]*len(df)
df.to_csv(f"{bugün}/Kıvırcık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kıvırcık",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Maydanoz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Maydanoz"]*len(df)
df.to_csv(f"{bugün}/Maydanoz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Maydanoz",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Nane")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Nane"]*len(df)
df.to_csv(f"{bugün}/Nane.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nane",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Patlıcan")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Patlıcan"]*len(df)
df.to_csv(f"{bugün}/Patlıcan.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Patlıcan",data,urunler_df)



df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Roka")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Roka"]*len(df)
df.to_csv(f"{bugün}/Roka.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Roka",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Salatalık")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Salatalık"]*len(df)
df.to_csv(f"{bugün}/Salatalık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Salatalık",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Patates")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Patates"]*len(df)
df.to_csv(f"{bugün}/Patates.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Patates",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kuru Fasulye")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Kuru Fasulye"]*len(df)
df.to_csv(f"{bugün}/Kuru Fasulye.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuru Fasulye",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Nohut")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Nohut"]*len(df)
df.to_csv(f"{bugün}/Nohut.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nohut",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Mercimek")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Mercimek"]*len(df)
df.to_csv(f"{bugün}/Mercimek.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mercimek",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Konserve")
df=df[~df["categories"].str.contains("balık",case=False)]
df.index=["Konserveler"]*len(df)
df.to_csv(f"{bugün}/Konserveler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Konserveler",data,urunler_df)

data=market("Turşu",data)
data=market("Salça",data)
data=market("Zeytin",data)
df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Cips")
df.index=["Cipsler"]*len(df)
df.to_csv(f"{bugün}/Cipsler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Cipsler",data,urunler_df)

data=market("Toz Şeker",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Küp Şeker")
df.index=["Kesme Şeker"]*len(df)
df.to_csv(f"{bugün}/Kesme Şeker.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kesme Şeker",data,urunler_df)

data=market("Reçel",data)
data=market("Bal",data)
data=market("Pekmez",data)
data=market("Tahin Helvası",data)
data=market("Fındık Ezmesi",data)
data=market("Çikolata Tablet",data)
data=market("Lokum",data)
data=market("Sakız",data)
data=market("Dondurma",data)
data=market("Baharat",data)
data=market("Tuz",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="Kabartma")
df.index=["Kabartma Maddeleri"]*len(df)
df.to_csv(f"{bugün}/Kabartma Maddeleri.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kabartma Maddeleri",data,urunler_df)

data=market("Sirke",data)
data=market("Ketçap",data)
data=market("Mayonez",data)
data=market("Tahin",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="hazır çorba")
df.index=["Hazır Çorbalar"]*len(df)
df.to_csv(f"{bugün}/Hazır Çorbalar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Çorbalar",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="puding")
df=df[df["categories"].str.contains("hazır",case=False)]
df.index=["Hazır Pakette Toz Tatlılar (Puding)"]*len(df)
df.to_csv(f"{bugün}/Hazır Pakette Toz Tatlılar (Puding).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Pakette Toz Tatlılar (Puding)",data,urunler_df)

data=market("Kahve",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="kahvesi")
df.index=["Kahve"]*len(df)
df.to_csv(f"{bugün}/Kahve.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kahve",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="nescafe")
df.index=["Hazır Kahve"]*len(df)
df.to_csv(f"{bugün}/Hazır Kahve.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Kahve",data,urunler_df)

data=market("Çay",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="bitki çayı")
df.index=["Bitki ve Meyve Çayı (Poşet)"]*len(df)
df.to_csv(f"{bugün}/Bitki ve Meyve Çayı (Poşet).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Bitki ve Meyve Çayı (Poşet)",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="toz kakao")
df=df[df["categories"].str.contains("kakao",case=False)]
df.index=["Kakao"]*len(df)
df.to_csv(f"{bugün}/Kakao.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kakao",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="kakaolu içecek")
df=df[df["categories"].str.contains("kakao",case=False)]
df.index=["Kakaolu Toz İçecekler"]*len(df)
df.to_csv(f"{bugün}/Kakaolu Toz İçecekler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kakaolu Toz İçecekler",data,urunler_df)

data=market("Su",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="maden suyu")
df.index=["Maden Suyu ve Sodası"]*len(df)
df.to_csv(f"{bugün}/Maden Suyu ve Sodası.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Maden Suyu ve Sodası",data,urunler_df)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="gazoz")
df.index=["Gazoz Meyveli"]*len(df)
df.to_csv(f"{bugün}/Gazoz Meyveli.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Gazoz Meyveli",data,urunler_df)

data=market("Kola",data)

df=market_fiyat_api(konum_listesi=konum_listesi,arama_terimi="soğuk çay")
df1=market_fiyat_api("icetea")
df=pd.concat([df,df1],axis=0)
df.index=["Soğuk Çay"]*len(df)
df.to_csv(f"{bugün}/Soğuk Çay.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Soğuk Çay",data,urunler_df)

data=market("Ayran",data)
data=market("Meyve Suyu",data)