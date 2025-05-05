data=marketim("Kraker",data)
data=marketim("Gofret",data)
data=marketim("Pasta",data,filter="pasta")
data=marketim("Kek",data)
data=marketim("Baklava",data,filter="fıstıklı")

df=market_fiyat_api("Yufka")
df.index=["Ekmek Hamuru (Yufka)"]*len(df)
df.to_csv(f"{bugün}/Ekmek Hamuru (Yufka).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ekmek Hamuru (Yufka)",data,urunler_df)

data=marketim("Makarna",data)
data=marketim("Şehriye",data)
data=marketim("Tahıl Gevreği",data)

df=market_fiyat_api("Dana Kıyma")
df1=market_fiyat_api("Dana Kuşbaşı")
df2=market_fiyat_api("Dana Köfte")
df=pd.concat([df,df1,df2],axis=0)
df.index=["Dana Eti"]*len(df)
df.to_csv(f"{bugün}/Dana Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Dana Eti",data,urunler_df)

df=market_fiyat_api("Kuzu Kıyma")
df1=market_fiyat_api("Kuzu Kuşbaşı")
df2=market_fiyat_api("Kuzu Köfte")
df=pd.concat([df,df1,df2],axis=0)
df.index=["Kuzu Eti"]*len(df)
df.to_csv(f"{bugün}/Kuzu Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuzu Eti",data,urunler_df)


df=market_fiyat_api("Piliç")
df=df[df["categories"].str.contains("Kümes Hayvanları|piliç",case=False)]
df.index=["Tavuk Eti"]*len(df)
df.to_csv(f"{bugün}/Tavuk Eti.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Tavuk Eti",data,urunler_df)

df=market_fiyat_api("kokoreç")
df.index=["Sakatat"]*len(df)
df.to_csv(f"{bugün}/Sakatat.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Sakatat",data,urunler_df)

data=marketim("Sucuk",data)
data=marketim("Salam",data)

df=market_fiyat_api("kavurma")
df=df[df["categories"].str.contains("konserve|dondurulmuş",case=False)]
df.index=["Hazır Et Yemekleri"]*len(df)
df.to_csv(f"{bugün}/Hazır Et Yemekleri.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Et Yemekleri",data,urunler_df)

df=market_fiyat_api("balık")
df=df[df["categories"].str.contains("dondurulmuş",case=False)]
df.index=["Balık"]*len(df)
df.to_csv(f"{bugün}/Balık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Balık",data,urunler_df)

df=market_fiyat_api("balık")
df=df[df["categories"].str.contains("konserve",case=False)]
df.index=["Konserve Balık"]*len(df)
df.to_csv(f"{bugün}/Konserve Balık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Konserve Balık",data,urunler_df)


data=marketim("Süt",data)
data=marketim("Yoğurt",data)

df=market_fiyat_api("sütlü tatlı")
df.index=["Hazır Sütlü Tatlılar"]*len(df)
df.to_csv(f"{bugün}/Hazır Sütlü Tatlılar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Sütlü Tatlılar",data,urunler_df)

data=marketim("Beyaz Peynir",data)
data=marketim("Kaşar Peyniri",data)
data=marketim("Tulum Peyniri",data)
data=marketim("Krem Peynir",data)
data=marketim("Yumurta",data)

df=market_fiyat_api("Tereyağı")
df.index=["Tereyağı (Kahvaltılık)"]*len(df)
df.to_csv(f"{bugün}/Tereyağı (Kahvaltılık).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Tereyağı (Kahvaltılık)",data,urunler_df)

data=marketim("Margarin",data)
data=marketim("Zeytinyağı",data)
data=marketim("Ayçiçek Yağı",data)

df=market_fiyat_api("portakal")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler",case=False)]
df.index=["Portakal"]*len(df)
df.to_csv(f"{bugün}/Portakal.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Portakal",data,urunler_df)

df=market_fiyat_api("Üzüm")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Üzüm"]*len(df)
df.to_csv(f"{bugün}/Üzüm.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Üzüm",data,urunler_df)

df=market_fiyat_api("Armut")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Armut"]*len(df)
df.to_csv(f"{bugün}/Armut.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Armut",data,urunler_df)


df=market_fiyat_api("Ayva")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Ayva"]*len(df)
df.to_csv(f"{bugün}/Ayva.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ayva",data,urunler_df)

df=market_fiyat_api("Çilek")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Çilek"]*len(df)
df.to_csv(f"{bugün}/Çilek.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Çilek",data,urunler_df)

df=market_fiyat_api("Elma")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Elma"]*len(df)
df.to_csv(f"{bugün}/Elma.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Elma",data,urunler_df)

df=market_fiyat_api("Karpuz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Karpuz"]*len(df)
df.to_csv(f"{bugün}/Karpuz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Karpuz",data,urunler_df)

df=market_fiyat_api("Kavun")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Kavun"]*len(df)
df.to_csv(f"{bugün}/Kavun.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kavun",data,urunler_df)

df=market_fiyat_api("Kivi")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Kivi"]*len(df)
df.to_csv(f"{bugün}/Kivi.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kivi",data,urunler_df)

df=market_fiyat_api("Limon")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Limon"]*len(df)
df.to_csv(f"{bugün}/Limon.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Limon",data,urunler_df)

df=market_fiyat_api("Mandalina")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Mandalina"]*len(df)
df.to_csv(f"{bugün}/Mandalina.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mandalina",data,urunler_df)


df=market_fiyat_api("Muz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler",case=False)]
df.index=["Muz"]*len(df)
df.to_csv(f"{bugün}/Muz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Muz",data,urunler_df)

df=market_fiyat_api("Nar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler|meyve Sebze",case=False)]
df.index=["Nar"]*len(df)
df.to_csv(f"{bugün}/Nar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nar",data,urunler_df)

df=market_fiyat_api("Şeftali")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|meyveler|meyve Sebze",case=False)]
df.index=["Şeftali"]*len(df)
df.to_csv(f"{bugün}/Şeftali.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Şeftali",data,urunler_df)

data=marketim("Badem İçi",data)
data=marketim("Ceviz İçi",data)
data=marketim("Fındık İçi",data)
data=marketim("Yer Fıstığı",data,filter="kuruyemiş")
data=marketim("Antep Fıstığı",data,filter="kuruyemiş")
data=marketim("Leblebi",data)
data=marketim("Ay Çekirdeği",data)
data=marketim("Kabak Çekirdeği",data)
data=marketim("Kuru Üzüm",data)
data=marketim("Kuru Kayısı",data)
data=marketim("Çarliston Biber",data)
data=marketim("Dolmalık Biber",data)

df=market_fiyat_api("Sivri Biber")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Sivri Biber"]*len(df)
df.to_csv(f"{bugün}/Sivri Biber.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Sivri Biber",data,urunler_df)

df=market_fiyat_api("Dereotu")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Dereotu"]*len(df)
df.to_csv(f"{bugün}/Dereotu.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Dereotu",data,urunler_df)

df=market_fiyat_api("Domates")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Domates"]*len(df)
df.to_csv(f"{bugün}/Domates.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Domates",data,urunler_df)

df=market_fiyat_api("Fasulye")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Taze Fasulye"]*len(df)
df.to_csv(f"{bugün}/Taze Fasulye.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Taze Fasulye",data,urunler_df)

df=market_fiyat_api("Havuç")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Havuç"]*len(df)
df.to_csv(f"{bugün}/Havuç.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Havuç",data,urunler_df)

df=market_fiyat_api("Ispanak")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Ispanak"]*len(df)
df.to_csv(f"{bugün}/Ispanak.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Ispanak",data,urunler_df)

df=market_fiyat_api("Kabak")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kabak"]*len(df)
df.to_csv(f"{bugün}/Kabak.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kabak",data,urunler_df)

df=market_fiyat_api("Karnabahar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Karnabahar"]*len(df)
df.to_csv(f"{bugün}/Karnabahar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Karnabahar",data,urunler_df)

df=market_fiyat_api("Soğan")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kuru Soğan"]*len(df)
df.to_csv(f"{bugün}/Kuru Soğan.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuru Soğan",data,urunler_df)

df=market_fiyat_api("Beyaz Lahana")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Beyaz Lahana"]*len(df)
df.to_csv(f"{bugün}/Beyaz Lahana.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Beyaz Lahana",data,urunler_df)

df=market_fiyat_api("Kırmızı Lahana")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kırmızı Lahana"]*len(df)
df.to_csv(f"{bugün}/Kırmızı Lahana.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kırmızı Lahana",data,urunler_df)

df=market_fiyat_api("Mantar")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Mantar"]*len(df)
df.to_csv(f"{bugün}/Mantar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mantar",data,urunler_df)

df=market_fiyat_api("Kıvırcık")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Kıvırcık"]*len(df)
df.to_csv(f"{bugün}/Kıvırcık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kıvırcık",data,urunler_df)

df=market_fiyat_api("Maydanoz")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Maydanoz"]*len(df)
df.to_csv(f"{bugün}/Maydanoz.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Maydanoz",data,urunler_df)

df=market_fiyat_api("Nane")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Nane"]*len(df)
df.to_csv(f"{bugün}/Nane.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nane",data,urunler_df)

df=market_fiyat_api("Patlıcan")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Patlıcan"]*len(df)
df.to_csv(f"{bugün}/Patlıcan.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Patlıcan",data,urunler_df)



df=market_fiyat_api("Roka")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Roka"]*len(df)
df.to_csv(f"{bugün}/Roka.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Roka",data,urunler_df)

df=market_fiyat_api("Salatalık")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Salatalık"]*len(df)
df.to_csv(f"{bugün}/Salatalık.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Salatalık",data,urunler_df)

df=market_fiyat_api("Patates")
df=df[df["categories"].str.contains("Meyve Ve Sebzeler|sebzeler|yeşillikler",case=False)]
df.index=["Patates"]*len(df)
df.to_csv(f"{bugün}/Patates.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Patates",data,urunler_df)

df=market_fiyat_api("Kuru Fasulye")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Kuru Fasulye"]*len(df)
df.to_csv(f"{bugün}/Kuru Fasulye.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kuru Fasulye",data,urunler_df)

df=market_fiyat_api("Nohut")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Nohut"]*len(df)
df.to_csv(f"{bugün}/Nohut.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Nohut",data,urunler_df)

df=market_fiyat_api("Mercimek")
df=df[df["categories"].str.contains("bakliyat",case=False)]
df.index=["Mercimek"]*len(df)
df.to_csv(f"{bugün}/Mercimek.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Mercimek",data,urunler_df)

df=market_fiyat_api("Konserve")
df=df[~df["categories"].str.contains("balık",case=False)]
df.index=["Konserveler"]*len(df)
df.to_csv(f"{bugün}/Konserveler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Konserveler",data,urunler_df)

data=marketim("Turşu",data)
data=marketim("Salça",data)
data=marketim("Zeytin",data)
df=market_fiyat_api("Cips")
df.index=["Cipsler"]*len(df)
df.to_csv(f"{bugün}/Cipsler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Cipsler",data,urunler_df)

data=marketim("Toz Şeker",data)

df=market_fiyat_api("Küp Şeker")
df.index=["Kesme Şeker"]*len(df)
df.to_csv(f"{bugün}/Kesme Şeker.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kesme Şeker",data,urunler_df)

data=marketim("Reçel",data)
data=marketim("Bal",data)
data=marketim("Pekmez",data)
data=marketim("Tahin Helvası",data)
data=marketim("Fındık Ezmesi",data)
data=marketim("Çikolata Tablet",data)
data=marketim("Lokum",data)
data=marketim("Sakız",data)
data=marketim("Dondurma",data)
data=marketim("Baharat",data)
data=marketim("Tuz",data)

df=market_fiyat_api("Kabartma")
df.index=["Kabartma Maddeleri"]*len(df)
df.to_csv(f"{bugün}/Kabartma Maddeleri.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kabartma Maddeleri",data,urunler_df)

data=marketim("Sirke",data)
data=marketim("Ketçap",data)
data=marketim("Mayonez",data)
data=marketim("Tahin",data)

df=market_fiyat_api("hazır çorba")
df.index=["Hazır Çorbalar"]*len(df)
df.to_csv(f"{bugün}/Hazır Çorbalar.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Çorbalar",data,urunler_df)

df=market_fiyat_api("puding")
df=df[df["categories"].str.contains("hazır",case=False)]
df.index=["Hazır Pakette Toz Tatlılar (Puding)"]*len(df)
df.to_csv(f"{bugün}/Hazır Pakette Toz Tatlılar (Puding).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Pakette Toz Tatlılar (Puding)",data,urunler_df)

data=marketim("Kahve",data)

df=market_fiyat_api("kahvesi")
df.index=["Kahve"]*len(df)
df.to_csv(f"{bugün}/Kahve.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kahve",data,urunler_df)

df=market_fiyat_api("nescafe")
df.index=["Hazır Kahve"]*len(df)
df.to_csv(f"{bugün}/Hazır Kahve.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Hazır Kahve",data,urunler_df)

data=marketim("Çay",data)

df=market_fiyat_api("bitki çayı")
df.index=["Bitki ve Meyve Çayı (Poşet)"]*len(df)
df.to_csv(f"{bugün}/Bitki ve Meyve Çayı (Poşet).csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Bitki ve Meyve Çayı (Poşet)",data,urunler_df)

df=market_fiyat_api("toz kakao")
df=df[df["categories"].str.contains("kakao",case=False)]
df.index=["Kakao"]*len(df)
df.to_csv(f"{bugün}/Kakao.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kakao",data,urunler_df)

df=market_fiyat_api("kakaolu içecek")
df=df[df["categories"].str.contains("kakao",case=False)]
df.index=["Kakaolu Toz İçecekler"]*len(df)
df.to_csv(f"{bugün}/Kakaolu Toz İçecekler.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Kakaolu Toz İçecekler",data,urunler_df)

data=marketim("Su",data)

df=market_fiyat_api("maden suyu")
df.index=["Maden Suyu ve Sodası"]*len(df)
df.to_csv(f"{bugün}/Maden Suyu ve Sodası.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Maden Suyu ve Sodası",data,urunler_df)

df=market_fiyat_api("gazoz")
df.index=["Gazoz Meyveli"]*len(df)
df.to_csv(f"{bugün}/Gazoz Meyveli.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Gazoz Meyveli",data,urunler_df)

data=marketim("Kola",data)

df=market_fiyat_api("soğuk çay")
df1=market_fiyat_api("icetea")
df=pd.concat([df,df1],axis=0)
df.index=["Soğuk Çay"]*len(df)
df.to_csv(f"{bugün}/Soğuk Çay.csv")
df["name"]=df["name"]+" "+df["marketName"]
urunler_df=df[["name","price"]]
urunler_df.columns=["Ürün",str(bugün)]
data=veriekle("Soğuk Çay",data,urunler_df)

data=marketim("Ayran",data)
data=marketim("Meyve Suyu",data)