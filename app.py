import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

df = pd.read_csv("veri.csv", index_col=0)

st.title("🛍️ Ürün Fiyat Takibi")

kategoriler = df.index.unique()
secilen_kategori = st.selectbox("Bir ürün kategorisi seçin:", kategoriler)

df_kat = df.loc[secilen_kategori]

if isinstance(df_kat, pd.Series):
    urun_adlari = [df_kat["Ürün"]]
    marketler = [df_kat["Market"]]
else:
    urun_adlari = df_kat["Ürün"].values
    marketler = df_kat["Market"].values

sonuclar = []

if isinstance(df_kat, pd.Series):
    fiyatlar = df_kat.drop(labels=["Ürün", "Market"], errors='ignore')
    mevcut_fiyatlar = fiyatlar.dropna()
    if len(mevcut_fiyatlar) > 0:
        ilk_tarih = mevcut_fiyatlar.index[0]
        son_tarih = mevcut_fiyatlar.index[-1]
        ilk_fiyat = mevcut_fiyatlar.iloc[0]
        son_fiyat = mevcut_fiyatlar.iloc[-1]
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
    fiyatlar = df_kat.drop(columns=["Ürün", "Market"], errors='ignore')
    for i, (idx, satir) in enumerate(fiyatlar.iterrows()):
        urun = urun_adlari[i]
        market = marketler[i]
        mevcut_fiyatlar = satir.dropna()
        if len(mevcut_fiyatlar) > 0:
            ilk_tarih = mevcut_fiyatlar.index[0]
            son_tarih = mevcut_fiyatlar.index[-1]
            ilk_fiyat = mevcut_fiyatlar.iloc[0]
            son_fiyat = mevcut_fiyatlar.iloc[-1]
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

urun_secimi = st.selectbox("Fiyat grafiği için ürün seçin:", df_sonuc["Ürün"].values)
import plotly.express as px
if isinstance(df_kat, pd.Series):
    if urun_secimi == urun_adlari[0]:
        fiyat_verisi = df_kat.drop(labels=["Ürün", "Market"], errors='ignore').dropna()
else:
    secilen_indeks = list(urun_adlari).index(urun_secimi)
    fiyat_verisi = df_kat.iloc[secilen_indeks].drop(labels=["Ürün", "Market"], errors='ignore').dropna()

fiyat_verisi.index = pd.to_datetime(fiyat_verisi.index)

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
