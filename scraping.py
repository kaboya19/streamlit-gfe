df=fetch_market_data_from_marketfiyat(market1, main_category=["Bakliyat"], keywords="pirinç")
if len(df)>0:
    df=df[~df["name"].str.contains("makarna|mantı",case=False)]
    df.index=["Pirinç"]*len(df)
    df.to_csv(f"{bugün}/pirinç.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    urunler_df.index=["Pirinç"]*len(urunler_df)
    data=veriekle("Pirinç",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Un ve İrmik"], keywords="un")
if len(df)>0:
    df.index=["Buğday Unu"]*len(df)
    df["name"]=df["name"]+" "+df["marketName"]
    df=df[df["categories"].str.contains("sade",case=False)]
    df.to_csv(f"{bugün}/buğdayunu.csv")
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    urunler_df.index=["Buğday Unu"]*len(urunler_df)
    data=veriekle("Buğday Unu",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Bebek Mamaları","Süt"], keywords="devam sütü")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Bebek Mamaları","Süt"], keywords="bebek sütü")
df=pd.concat([df,df1],axis=0)
if len(df)>0:
    df.index=["Bebek Sütü (Toz Karışım)"]*len(df)
    df.to_csv(f"{bugün}/bebeksütü.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    urunler_df.index=["Bebek Sütü (Toz Karışım)"]*len(urunler_df)
    data=veriekle("Bebek Sütü (Toz Karışım)",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bakliyat"], keywords="bulgur")
if len(df)>0:
    df.index=["Bulgur"]*len(df)
    df.to_csv(f"{bugün}/bulgur.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Bulgur",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Ekmek ve Unlu Mamüller"], keywords="ekmek")
if len(df)>0:
    df.index=["Ekmek"]*len(df)
    df.to_csv(f"{bugün}/ekmek.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ekmek",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bisküvi ve Kraker"], keywords="bisküvi")
if len(df)>0:
    df.index=["Bisküvi"]*len(df)
    df.to_csv(f"{bugün}/bisküvi.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Bisküvi",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bisküvi ve Kraker"], keywords="kraker")
if len(df)>0:
    df.index=["Kraker"]*len(df)
    df.to_csv(f"{bugün}/kraker.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kraker",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Gofret"], keywords="gofret")
if len(df)>0:
    df.index=["Gofret"]*len(df)
    df.to_csv(f"{bugün}/gofret.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Gofret",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kek"], keywords="pasta")
if len(df)>0:
    df.index=["Pasta"]*len(df)
    df.to_csv(f"{bugün}/pasta.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Pasta",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Kek"], keywords="kek")
if len(df)>0:
    df.index=["Kek"]*len(df)
    df.to_csv(f"{bugün}/kek.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kek",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Tatlılar","Diğer Ürünler"], keywords="baklava")
if len(df)>0:
    df.index=["Baklava"]*len(df)
    df.to_csv(f"{bugün}/baklava.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Baklava",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Ekmek ve Unlu Mamüller"], keywords="yufka")
if len(df)>0:
    df.index=["Ekmek Hamuru (Yufka)"]*len(df)
    df.to_csv(f"{bugün}/Ekmek Hamuru (Yufka).csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ekmek Hamuru (Yufka)",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Mantı Makarna ve Erişte"], keywords="makarna")
if len(df)>0:
    df=df[~df["name"].str.contains("şehriye|mantı|pirinç",case=False)]

    df.index=["Makarna"]*len(df)
    df.to_csv(f"{bugün}/Makarna.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Makarna",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Mantı Makarna ve Erişte"], keywords="şehriye")
if len(df)>0:
    df=df[df["name"].str.contains("şehriye",case=False)]
    df.index=["Şehriye"]*len(df)
    df.to_csv(f"{bugün}/Şehriye.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Şehriye",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Kahvaltılık Gevrek Bar ve Granola"], keywords="gevreği")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kahvaltılık Gevrek Bar ve Granola"], keywords="yulaf ezmesi")
df=pd.concat([df,df1],axis=0)
if len(df)>0:
    df.index=["Tahıl Gevreği"]*len(df)
    df.to_csv(f"{bugün}/Tahıl Gevreği.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tahıl Gevreği",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et"], keywords="kıyma")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et"], keywords="kuşbaşı")
df=pd.concat([df,df1],axis=0)
if len(df)>0:
    df=df[~df["categories"].str.contains("kuzu",case=False)]
    df.index=["Dana Eti"]*len(df)
    df.to_csv(f"{bugün}/Dana Eti.csv")

    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Dana Eti",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et"], keywords="kuzu")
if len(df)>0:
    df=df[df["categories"].str.contains("kuzu",case=False)]
    df.index=["Kuzu Eti"]*len(df)
    df.to_csv(f"{bugün}/Kuzu Eti.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kuzu Eti",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Beyaz Et"], keywords="piliç")
if len(df)>0:
    df=df[~df["name"].str.contains("nugget|schnitzel|şinitzel|döner",case=False)]
    df.index=["Tavuk Eti"]*len(df)
    df.to_csv(f"{bugün}/Tavuk Eti.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tavuk Eti",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Sakatat"], keywords="kokoreç")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Sakatat"], keywords="ciğer")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Sakatat"], keywords="işkembe")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Sakatat"], keywords="yürek")
df4=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Sakatat"], keywords="paça")

df=pd.concat([df,df1,df2,df3,df4],axis=0)
if len(df)>0:
    df.index=["Sakatat"]*len(df)
    df.to_csv(f"{bugün}/Sakatat.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Sakatat",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Şarküteri"], keywords="sucuk")
if len(df)>0:
    df.index=["Sucuk"]*len(df)
    df.to_csv(f"{bugün}/Sucuk.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Sucuk",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Şarküteri"], keywords="sosis")
if len(df)>0:
    df.index=["Sosis"]*len(df)
    df.to_csv(f"{bugün}/Sosis.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Sosis",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Şarküteri"], keywords="salam")
if len(df)>0:
    df.index=["Salam"]*len(df)
    df.to_csv(f"{bugün}/Salam.csv")
    df["name"]=df["name"]+" "+df["marketName"]
    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Salam",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Kırmızı Et","Beyaz Et","Hazır Gıda"], keywords="döner")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda"], keywords="köfte")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda","Beyaz Et"], keywords="nugget")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda","Beyaz Et"], keywords="schnitzel")
df4=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda","Beyaz Et"], keywords="tavuk dürüm")
df5=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda"], keywords="etli")
df=pd.concat([df,df1,df2,df3,df4,df5],axis=0)
if len(df)>0:
    df.index=["Hazır Et Yemekleri"]*len(df)
    df.to_csv(f"{bugün}/Hazır Et Yemekleri.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Hazır Et Yemekleri",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Deniz Ürünleri"], keywords="hamsi")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Deniz Ürünleri"], keywords="istavrit")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Deniz Ürünleri"], keywords="çipura")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Deniz Ürünleri"], keywords="levrek")

df=pd.concat([df,df1,df2,df3],axis=0)

if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df.index=["Balık"]*len(df)
    df.to_csv(f"{bugün}/Balık.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Balık",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="balık")
if len(df)>0:
    df.index=["Konserve Balık"]*len(df)
    df.to_csv(f"{bugün}/Konserve Balık.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Konserve Balık",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Süt"], keywords="süt")
if len(df)>0:
    df=df[~df["name"].str.contains("kakao|çilek|muz|protein|badem|ballı|barista|çikolata|aroma|hindistan|devam|bebek|kahve|nesquik|çocuk",case=False)]
    df.index=["Süt"]*len(df)
    df.to_csv(f"{bugün}/Süt.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Süt",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Yoğurt"], keywords="yoğurt")
if len(df)>0:
    df.index=["Yoğurt"]*len(df)
    df.to_csv(f"{bugün}/Yoğurt.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Yoğurt",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Tatlılar"], keywords="puding")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Tatlılar"], keywords="sütlaç")
df=pd.concat([df,df1],axis=0)
if len(df)>0:
    df=df[df["brand"].str.contains("eker|sütaş|mis|danette|içim|pınar",case=False)]
    df.index=["Hazır Sütlü Tatlılar"]*len(df)
    df.to_csv(f"{bugün}/Hazır Sütlü Tatlılar.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Hazır Sütlü Tatlılar",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Peynir"], keywords="beyaz peynir")
if len(df)>0:
    df.index=["Beyaz Peynir"]*len(df)
    df.to_csv(f"{bugün}/Beyaz Peynir.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Beyaz Peynir",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Peynir"], keywords="kaşar")
if len(df)>0:
    df.index=["Kaşar Peyniri"]*len(df)
    df.to_csv(f"{bugün}/Kaşar Peyniri.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kaşar Peyniri",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Peynir"], keywords="tulum")
if len(df)>0:
    df.index=["Tulum Peyniri"]*len(df)
    df.to_csv(f"{bugün}/Tulum Peyniri.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tulum Peyniri",data,urunler_df)   


df=fetch_market_data_from_marketfiyat(market1, main_category=["Peynir"], keywords="krem")
if len(df)>0:
    df.index=["Krem Peynir"]*len(df)
    df.to_csv(f"{bugün}/Krem Peynir.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Krem Peynir",data,urunler_df)   

df=fetch_market_data_from_marketfiyat(market1, main_category=["Yumurta"], keywords="yumurta")
if len(df)>0:
    df.index=["Yumurta"]*len(df)
    df.to_csv(f"{bugün}/Yumurta.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Yumurta",data,urunler_df)   

df=fetch_market_data_from_marketfiyat(market1, main_category=["Tereyağı ve Margarin"], keywords="tereyağ")
if len(df)>0:
    df=df[~df["name"].str.contains("margarin",case=False)]
    df.index=["Tereyağı (Kahvaltılık)"]*len(df)
    df.to_csv(f"{bugün}/Tereyağı (Kahvaltılık).csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tereyağı (Kahvaltılık)",data,urunler_df)  


df=fetch_market_data_from_marketfiyat(market1, main_category=["Tereyağı ve Margarin"], keywords="margarin")
if len(df)>0:
    df=df[df["name"].str.contains("margarin",case=False)]
    df.index=["Margarin"]*len(df)
    df.to_csv(f"{bugün}/Margarin.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Margarin",data,urunler_df)  

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sıvı Yağlar"], keywords="zeytinyağı")
if len(df)>0:
    df=df[~df["name"].str.contains("ayçiçek",case=False)]
    df.index=["Zeytinyağı"]*len(df)
    df.to_csv(f"{bugün}/Zeytinyağı.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Zeytinyağı",data,urunler_df)  


df=fetch_market_data_from_marketfiyat(market1, main_category=["Sıvı Yağlar"], keywords="ayçiçek")
if len(df)>0:
    df=df[~df["name"].str.contains("zeytin",case=False)]
    df.index=["Ayçiçek Yağı"]*len(df)
    df.to_csv(f"{bugün}/Ayçiçek Yağı.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ayçiçek Yağı",data,urunler_df)

def meyve(market1,key,data):
    df=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve"], keywords=key)
    if len(df)>0:
        df.index=[key]*len(df)
        df.to_csv(f"{bugün}/{key}.csv")
        df["name"]=df["name"]+" "+df["marketName"]

        urunler_df=df[["name","price","Şehir"]]
        urunler_df.columns=["Ürün",str(bugün),"Şehir"]
        data=veriekle(key,data,urunler_df)
        return data

data=meyve(market1,"Portakal",data)
data=meyve(market1,"Üzüm",data)
data=meyve(market1,"Armut",data)
data=meyve(market1,"Ayva",data)
data=meyve(market1,"Çilek",data)
data=meyve(market1,"Elma",data)
data=meyve(market1,"Karpuz",data)
data=meyve(market1,"Kavun",data)
data=meyve(market1,"Kivi",data)
data=meyve(market1,"Limon",data)
data=meyve(market1,"Mandalina",data)
data=meyve(market1,"Muz",data)
data=meyve(market1,"Nar",data)
data=meyve(market1,"Şeftali",data)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="antep fıstığı")
if len(df)>0:
    df.index=["Antep Fıstığı"]*len(df)
    df.to_csv(f"{bugün}/Antep Fıstığı.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Antep Fıstığı",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="badem içi")
if len(df)>0:
    df.index=["Badem İçi"]*len(df)
    df.to_csv(f"{bugün}/Badem İçi.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Badem İçi",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="ceviz içi")
if len(df)>0:
    df.index=["Ceviz İçi"]*len(df)
    df.to_csv(f"{bugün}/Ceviz İçi.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ceviz İçi",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="fındık içi")
if len(df)>0:
    df.index=["Fındık İçi"]*len(df)
    df.to_csv(f"{bugün}/Fındık İçi.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Fındık İçi",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="leblebi")
if len(df)>0:
    df.index=["Leblebi"]*len(df)
    df.to_csv(f"{bugün}/Leblebi.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Leblebi",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="ay çekirdeği")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="dakota")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="siyah çekirdek")
df=pd.concat([df,df1,df2],axis=0)
if len(df)>0:
    df.index=["Ay Çekirdeği"]*len(df)
    df.to_csv(f"{bugün}/Ay Çekirdeği.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ay Çekirdeği",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="kabak çekirdeği")

if len(df)>0:
    df.index=["Kabak Çekirdeği"]*len(df)
    df.to_csv(f"{bugün}/Kabak Çekirdeği.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kabak Çekirdeği",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="kuru üzüm")

if len(df)>0:
    df.index=["Kuru Üzüm"]*len(df)
    df.to_csv(f"{bugün}/Kuru Üzüm.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kuru Üzüm",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kuruyemiş ve Kuru Meyve"], keywords="kuru kayısı")

if len(df)>0:
    df.index=["Kuru Kayısı"]*len(df)
    df.to_csv(f"{bugün}/Kuru Kayısı.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kuru Kayısı",data,urunler_df)

def sebze(market1,data,key):
    df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords=key)

    if len(df)>0:
        df=df[df["brand"]=="Markasız"]
        df.index=[key]*len(df)
        df.to_csv(f"{bugün}/{key}.csv")
        df["name"]=df["name"]+" "+df["marketName"]

        urunler_df=df[["name","price","Şehir"]]
        urunler_df.columns=["Ürün",str(bugün),"Şehir"]
        data=veriekle(key,data,urunler_df)
        return data

data=sebze(market1,data,"Çarliston Biber")
data=sebze(market1,data,"Dolmalık Biber")
data=sebze(market1,data,"Sivri Biber")
data=sebze(market1,data,"Dereotu")
data=sebze(market1,data,"Domates")



data=sebze(market1,data,"Ispanak")
data=sebze(market1,data,"Kabak")
data=sebze(market1,data,"Karnabahar")
data=sebze(market1,data,"Beyaz Lahana")
data=sebze(market1,data,"Kırmızı Lahana")
data=sebze(market1,data,"Kıvırcık")
data=sebze(market1,data,"Nane")
data=sebze(market1,data,"Patlıcan")
data=sebze(market1,data,"Roka")
data=sebze(market1,data,"Patates")

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords="fasulye")

if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df.index=["Taze Fasulye"]*len(df)
    df.to_csv(f"{bugün}/Taze Fasulye.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Taze Fasulye",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve","Sebze"], keywords="havuç")

if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df.index=["Havuç"]*len(df)
    df.to_csv(f"{bugün}/Havuç.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Havuç",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords="soğan")

if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df=df[~df["name"].str.contains("yeşil|demet",case=False)]
    df.index=["Kuru Soğan"]*len(df)
    df.to_csv(f"{bugün}/Kuru Soğan.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kuru Soğan",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords="mantar")

if len(df)>0:
    df.index=["Mantar"]*len(df)
    df.to_csv(f"{bugün}/Mantar.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Mantar",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords="maydonoz")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze"], keywords="maydanoz")
df=pd.concat([df,df1],axis=0)
if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df.index=["Maydanoz"]*len(df)
    df.to_csv(f"{bugün}/Maydanoz.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Maydanoz",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sebze","Meyve"], keywords="salatalık")
if len(df)>0:
    df=df[df["brand"]=="Markasız"]
    df.index=["Salatalık"]*len(df)
    df.to_csv(f"{bugün}/Salatalık.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Salatalık",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bakliyat"], keywords="kuru fasulye")
if len(df)>0:
    df.index=["Kuru Fasulye"]*len(df)
    df.to_csv(f"{bugün}/Kuru Fasulye.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kuru Fasulye",data,urunler_df)


df=fetch_market_data_from_marketfiyat(market1, main_category=["Bakliyat"], keywords="nohut")
if len(df)>0:
    df.index=["Nohut"]*len(df)
    df.to_csv(f"{bugün}/Nohut.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Nohut",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bakliyat"], keywords="mercimek")
if len(df)>0:
    df.index=["Mercimek"]*len(df)
    df.to_csv(f"{bugün}/Mercimek.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Mercimek",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="biber")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="bezelye")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="fasulye")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="mısır")
df4=fetch_market_data_from_marketfiyat(market1, main_category=["Konserve"], keywords="patlıcan")
df=pd.concat([df,df1,df2,df3,df4],axis=0)
if len(df)>0:
    df=df[~df["name"].str.contains("salça",case=False)]
    df.index=["Konserveler"]*len(df)
    df.to_csv(f"{bugün}/Konserveler.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Konserveler",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Turşu"], keywords="turşu")
if len(df)>0:
    df.index=["Turşu"]*len(df)
    df.to_csv(f"{bugün}/Turşu.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Turşu",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Salça"], keywords="salça")
if len(df)>0:
    df.index=["Salça"]*len(df)
    df.to_csv(f"{bugün}/Salça.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Salça",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Zeytin"], keywords="zeytin")
if len(df)>0:
    df.index=["Zeytin"]*len(df)
    df.to_csv(f"{bugün}/Zeytin.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Zeytin",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Cips"], keywords="cips")
if len(df)>0:
    df.index=["Cips"]*len(df)
    df.to_csv(f"{bugün}/Cips.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Cipsler",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Şeker ve Tatlandırıcılar"], keywords="toz şeker")
if len(df)>0:
    df.index=["Toz Şeker"]*len(df)
    df.to_csv(f"{bugün}/Toz Şeker.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Toz Şeker",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Şeker ve Tatlandırıcılar"], keywords="küp şeker")
if len(df)>0:
    df.index=["Kesme Şeker"]*len(df)
    df.to_csv(f"{bugün}/Kesme Şeker.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kesme Şeker",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bal ve Reçel"], keywords="bal")
if len(df)>0:
    df.index=["Bal"]*len(df)
    df.to_csv(f"{bugün}/Bal.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Bal",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Sakız ve Şekerleme"], keywords="lokum")
if len(df)>0:
    df=df[~df["name"].str.contains("çikolata",case=False)]
    df.index=["Lokum"]*len(df)
    df.to_csv(f"{bugün}/Lokum.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Lokum",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Bal ve Reçel"], keywords="reçel")
if len(df)>0:
    df.index=["Reçel"]*len(df)
    df.to_csv(f"{bugün}/Reçel.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Reçel",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Helva Tahin ve Pekmez"], keywords="pekmez")
if len(df)>0:
    df=df[~df["name"].str.contains("tahin|helva",case=False)]
    df.index=["Pekmez"]*len(df)
    df.to_csv(f"{bugün}/Pekmez.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Pekmez",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Helva Tahin ve Pekmez"], keywords="tahin helvası")
if len(df)>0:
    df.index=["Tahin Helvası"]*len(df)
    df.to_csv(f"{bugün}/Tahin Helvası.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tahin Helvası",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Sürülebilir Ürünler ve Kahvaltılık Soslar"], keywords="fındık ezmesi")
if len(df)>0:
    df=df[~df["name"].str.contains("çokokrem",case=False)]
    df.index=["Fındık Ezmesi"]*len(df)
    df.to_csv(f"{bugün}/Fındık Ezmesi.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Fındık Ezmesi",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Çikolata"], keywords="tablet")
if len(df)>0:
    df.index=["Çikolata Tablet"]*len(df)
    df.to_csv(f"{bugün}/Çikolata Tablet.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Çikolata Tablet",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Sürülebilir Ürünler ve Kahvaltılık Soslar"], keywords="kakaolu")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Sürülebilir Ürünler ve Kahvaltılık Soslar"], keywords="nutella")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Sürülebilir Ürünler ve Kahvaltılık Soslar"], keywords="çokokrem")
df=pd.concat([df,df1,df2],axis=0)
if len(df)>0:
    df.index=["Çikolata Krem"]*len(df)
    df.to_csv(f"{bugün}/Çikolata Krem.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Çikolata Krem",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Sakız ve Şekerleme"], keywords="sakız")
if len(df)>0:
    df.index=["Sakız"]*len(df)
    df.to_csv(f"{bugün}/Sakız.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Sakız",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Dondurmalar"], keywords="dondurma")
if len(df)>0:
    df.index=["Dondurma"]*len(df)
    df.to_csv(f"{bugün}/Dondurma.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Dondurma",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="çörek otu")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="kekik")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="kimyon")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="nane")
df4=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="karabiber")
df5=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="kimyon")
df6=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="köri")
df7=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="biber")
df=pd.concat([df,df1,df2,df3,df4,df5,df6,df7],axis=0)
if len(df)>0:
    df.index=["Baharat"]*len(df)
    df.to_csv(f"{bugün}/Baharat.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Baharat",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Tuz Baharat ve Harçlar"], keywords="tuz")
if len(df)>0:
    df.index=["Tuz"]*len(df)
    df.to_csv(f"{bugün}/Tuz.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tuz",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Pasta Malzemeleri"], keywords="kabartma")
if len(df)>0:
    df.index=["Kabartma Maddeleri"]*len(df)
    df.to_csv(f"{bugün}/Kabartma Maddeleri.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kabartma Maddeleri",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Helva Tahin ve Pekmez"], keywords="tahin")
if len(df)>0:
    df=df[~df["name"].str.contains("pekmez|helva",case=False)]
    df.index=["Tahin"]*len(df)
    df.to_csv(f"{bugün}/Tahin.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Tahin",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Ketçap Mayonez Sos ve Sirkeler"], keywords="sirke")
if len(df)>0:

    df.index=["Sirke"]*len(df)
    df.to_csv(f"{bugün}/Sirke.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Sirke",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Ketçap Mayonez Sos ve Sirkeler"], keywords="ketçap")
if len(df)>0:
    df=df[~df["name"].str.contains("mayonez",case=False)]
    df.index=["Ketçap"]*len(df)
    df.to_csv(f"{bugün}/Ketçap.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ketçap",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Ketçap Mayonez Sos ve Sirkeler"], keywords="mayonez")
if len(df)>0:
    df=df[~df["name"].str.contains("ketçap",case=False)]
    df.index=["Mayonez"]*len(df)
    df.to_csv(f"{bugün}/Mayonez.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Mayonez",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Hazır Gıda"], keywords="çorba")
if len(df)>0:
    df=df[~df["name"].str.contains("kemik|kelle",case=False)]
    df.index=["Hazır Çorbalar"]*len(df)
    df.to_csv(f"{bugün}/Hazır Çorbalar.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Hazır Çorbalar",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Pasta Malzemeleri"], keywords="puding")
if len(df)>0:
    df.index=["Hazır Pakette Toz Tatlılar (Puding)"]*len(df)
    df.to_csv(f"{bugün}/Hazır Pakette Toz Tatlılar (Puding).csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Hazır Pakette Toz Tatlılar (Puding)",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="filtre")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="kapsül")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="türk")
df=pd.concat([df,df1,df2],axis=0)
if len(df)>0:
    df.index=["Kahve"]*len(df)
    df.to_csv(f"{bugün}/Kahve.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kahve",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="nescafe")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="latte")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Kahve"], keywords="mocha")

df=pd.concat([df,df1,df2],axis=0)
if len(df)>0:
    df.index=["Hazır Kahve"]*len(df)
    df.to_csv(f"{bugün}/Hazır Kahve.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Hazır Kahve",data,urunler_df)



df=fetch_market_data_from_marketfiyat(market1, main_category=["Çay ve Bitki Çayları"], keywords="siyah çay")


if len(df)>0:
    df.index=["Çay"]*len(df)
    df.to_csv(f"{bugün}/Çay.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Çay",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Çay ve Bitki Çayları"], keywords="bitki çayı")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Çay ve Bitki Çayları"], keywords="meyve çayı")
df=pd.concat([df,df1],axis=0)


if len(df)>0:
    df.index=["Bitki ve Meyve Çayı (Poşet)"]*len(df)
    df.to_csv(f"{bugün}/Bitki ve Meyve Çayı (Poşet).csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Bitki ve Meyve Çayı (Poşet)",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Pasta Malzemeleri"], keywords="kakao")





if len(df)>0:
    df.index=["Kakao"]*len(df)
    df.to_csv(f"{bugün}/Kakao.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kakao",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Süt","Gazsız İçecekler"], keywords="nesquik")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Süt","Gazsız İçecekler"], keywords="kakaolu süt")
df=pd.concat([df,df1],axis=0)

if len(df)>0:
    df.index=["Kakaolu Toz İçecekler"]*len(df)
    df.to_csv(f"{bugün}/Kakaolu Toz İçecekler.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kakaolu Toz İçecekler",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Su"], keywords="su")

if len(df)>0:
    df.index=["Su"]*len(df)
    df.to_csv(f"{bugün}/Su.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Su",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Maden Suyu"], keywords="maden suyu")

if len(df)>0:
    df.index=["Maden Suyu"]*len(df)
    df.to_csv(f"{bugün}/Maden Suyu.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Maden Suyu ve Sodası",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Gazlı İçecekler"], keywords="gazoz")

if len(df)>0:
    df.index=["Gazoz Meyveli"]*len(df)
    df.to_csv(f"{bugün}/Gazoz Meyveli.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Gazoz Meyveli",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Gazlı İçecekler"], keywords="kola")

if len(df)>0:
    df.index=["Kola"]*len(df)
    df.to_csv(f"{bugün}/Kola.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Kola",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Çay ve Bitki Çayları"], keywords="soğuk çay")

if len(df)>0:
    df.index=["Soğuk Çay"]*len(df)
    df.to_csv(f"{bugün}/Soğuk Çay.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Soğuk Çay",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Ayran ve Kefir"], keywords="ayran")

if len(df)>0:
    df.index=["Ayran"]*len(df)
    df.to_csv(f"{bugün}/Ayran.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Ayran",data,urunler_df)

df=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve Suyu"], keywords="kayısı")
df1=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve Suyu"], keywords="şeftali")
df2=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve Suyu"], keywords="vişne")
df3=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve Suyu"], keywords="elma")
df4=fetch_market_data_from_marketfiyat(market1, main_category=["Meyve Suyu"], keywords="karışık")
df=pd.concat([df,df1,df2,df3,df4],axis=0)
if len(df)>0:
    df.index=["Meyve Suyu"]*len(df)
    df.to_csv(f"{bugün}/Meyve Suyu.csv")
    df["name"]=df["name"]+" "+df["marketName"]

    urunler_df=df[["name","price","Şehir"]]
    urunler_df.columns=["Ürün",str(bugün),"Şehir"]
    data=veriekle("Meyve Suyu",data,urunler_df)