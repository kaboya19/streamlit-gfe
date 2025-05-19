import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Verileri oku
df = pd.read_csv("marketli.csv", index_col=0)
df1 = pd.read_csv("C:/Users/Bora/Documents/GitHub/web-tufe/deneme3.csv", index_col=0)
df1=df1.rename(columns={"Ürün Adı":"Ürün"})
# En az 3 geçerli fiyatı olan ürünleri filtrele
df = df[df.iloc[:, -16:].notna().sum(axis=1) >= 3]
df1 = df1[df1.iloc[:, -8:].notna().sum(axis=1) > 1]

st.title("🛍️ Ürün Fiyat Takibi")

# Kullanıcıya gıda mı, gıda dışı mı diye seçim sun
veri_tipi = st.radio("Ürün Tipi Seçiniz:", ["Gıda", "Gıda Dışı"])

aktif_df = df if veri_tipi == "Gıda" else df1

# Kategori seçimi
kategoriler = aktif_df.index.unique()
secilen_kategori = st.selectbox("Bir ürün kategorisi seçin:", kategoriler)

df_kat = aktif_df.loc[secilen_kategori]

# Ürün adlarını ve marketleri ayıkla
if isinstance(df_kat, pd.Series):
    urun_adlari = [df_kat.get("Ürün", df_kat.get("Ürün Adı"))]
    marketler = [df_kat.get("Market", "Bilinmiyor")]
else:
    urun_adlari = df_kat.get("Ürün", df_kat.get("Ürün Adı")).values
    marketler = df_kat["Market"].values if "Market" in df_kat.columns else ["Bilinmiyor"] * len(df_kat)

# Fiyat değişimlerini hesapla
sonuclar = []

if isinstance(df_kat, pd.Series):
    if veri_tipi=="Gıda Dışı":
        del df_kat["ID"]
    fiyatlar = df_kat.drop(labels=["Ürün", "Market", "Ürün Adı"], errors='ignore')

    ilk_tarih = fiyatlar.first_valid_index()
    son_tarih = fiyatlar.last_valid_index() 
    

    if ilk_tarih is not None and son_tarih is not None and ilk_tarih != son_tarih:
        ilk_fiyat = fiyatlar[ilk_tarih]
        son_fiyat = fiyatlar[son_tarih]

        if ilk_fiyat != 0:  # sıfıra bölme hatasını engelle
            degisim = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100

            sonuclar.append({
                "Ürün": urun_adlari[0],
                "Market": marketler[0],
                "İlk Fiyat": ilk_fiyat,
                "Son Fiyat": son_fiyat,
                "Değişim (%)": round(degisim, 2),
                "İlk Fiyat Tarihi": ilk_tarih,
                "Son Fiyat Tarihi": son_tarih
            })

else:
    if veri_tipi=="Gıda Dışı":
        del df_kat["ID"]
    fiyatlar = df_kat.drop(columns=["Ürün", "Market", "Ürün Adı"], errors='ignore')
    for i, (idx, satir) in enumerate(fiyatlar.iterrows()):
        urun = urun_adlari[i]
        market = marketler[i]
        mevcut_fiyatlar = satir.copy()
        if len(mevcut_fiyatlar) > 0:
            ilk_tarih = mevcut_fiyatlar.first_valid_index()
            son_tarih = mevcut_fiyatlar.last_valid_index()
            if ilk_tarih is not None and son_tarih is not None and ilk_tarih != son_tarih:
                ilk_fiyat = mevcut_fiyatlar[ilk_tarih]
                son_fiyat = mevcut_fiyatlar[son_tarih]
                degisim = ((son_fiyat - ilk_fiyat) / ilk_fiyat) * 100

                sonuclar.append({
                    "Ürün": urun,
                    "Market": market,
                    "İlk Fiyat": ilk_fiyat,
                    "Son Fiyat": son_fiyat,
                    "Değişim (%)": round(degisim, 2),
                    "İlk Fiyat Tarihi": ilk_tarih,
                    "Son Fiyat Tarihi": son_tarih
                })

# Sonuçları tablo olarak göster
df_sonuc = pd.DataFrame(sonuclar)

st.subheader(f"{secilen_kategori} Ürünleri")
st.dataframe(
    df_sonuc.style.format({
        "İlk Fiyat": "{:.2f}",
        "Son Fiyat": "{:.2f}",
        "Değişim (%)": "{:+.2f}%"
    }).background_gradient(subset=["Değişim (%)"], cmap="RdYlGn"),
    use_container_width=True,
)

# Grafik için ürün seçimi
urun_secimi = st.selectbox("Fiyat grafiği için ürün seçin:", df_sonuc["Ürün"].values)

# Seçilen ürünün fiyat serisini al
if isinstance(df_kat, pd.Series):
    if urun_secimi == urun_adlari[0]:
        fiyat_verisi = df_kat.drop(labels=["Ürün", "Market", "Ürün Adı"], errors='ignore').dropna()
else:
    secilen_indeks = list(urun_adlari).index(urun_secimi)
    fiyat_verisi = df_kat.iloc[secilen_indeks].drop(labels=["Ürün", "Market", "Ürün Adı"], errors='ignore').dropna()

# Tarihleri datetime'a çevir
fiyat_verisi.index = pd.to_datetime(fiyat_verisi.index)

# Grafik çizimi
st.subheader(f"{urun_secimi} - Fiyat Zaman Serisi")

fig = px.line(
    x=fiyat_verisi.index,
    y=fiyat_verisi.values,
    labels={"x": "Tarih", "y": "Fiyat"},
    markers=True,
    title=f"{urun_secimi} Fiyat Grafiği"
)

fig.update_layout(
    title_font=dict(size=20, family="Arial", color="black", weight="bold"),
    xaxis_title_font=dict(size=16, family="Arial", color="black", weight="bold"),
    yaxis_title_font=dict(size=16, family="Arial", color="black", weight="bold"),
    xaxis=dict(
        tickfont=dict(size=14, family="Arial", color="black", weight="bold"),
        showgrid=True,
        gridcolor="LightGray",
    ),
    yaxis=dict(
        tickfont=dict(size=14, family="Arial", color="black", weight="bold"),
        showgrid=True,
        gridcolor="LightGray",
    ),
    plot_bgcolor="white",
    hovermode="x unified",
    margin=dict(l=60, r=40, t=60, b=60)
)

st.plotly_chart(fig, use_container_width=True)
