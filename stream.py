import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO
from datetime import datetime
from st_social_media_links import SocialMediaIcons
import base64
from streamlit_option_menu import option_menu
st.set_page_config(page_title="Web-Gıda Fiyat Endeksi",layout="wide")
social_media_links = {
    "X": {"url": "https://x.com/mborathe", "color": "#000000"},
    "GitHub": {"url": "https://github.com/kaboya19", "color": "#000000"},
    "LinkedIn": {"url": "https://www.linkedin.com/in/bora-kaya/", "color": "#000000"}
}
tabs=["Gıda Fiyat Endeksi","Harcama Grupları","Madde Endeksleri","Metodoloji Notu","Bültenler","Bülten Aboneliği"]
tabs = option_menu(
    menu_title=None,
    options=["Gıda Fiyat Endeksi", "Harcama Grupları","Madde Endeksleri", "Metodoloji Notu", "Bültenler", "Bülten Aboneliği"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#d6094d"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {
            "font-size": "20px", 
            "text-align": "center", 
            "margin": "0px", 
            "--hover-color": "#444", 
            "padding-left": "20px",  # Add padding for consistent spacing
            "padding-right": "20px",  # Add padding for consistent spacing
            "height": "50px",  # Set a fixed height for all buttons
            "min-width": "150px",  # Ensure buttons do not shrink too small
            "white-space": "normal",  # Allow text to wrap if necessary
            "display": "inline-flex",  # Use inline-flex to adjust width to text content
            "justify-content": "center",
            "align-items": "center",
        },
        "nav-link-selected": {"background-color": "orange"},
    }
)



page=st.sidebar.radio("Sekmeler",tabs)

social_media_icons = SocialMediaIcons(
        [link["url"] for link in social_media_links.values()],
        colors=[link["color"] for link in social_media_links.values()]
    )
social_media_icons.render(sidebar=True)

if page=="Bülten Aboneliği":
        
        st.title("E-posta Aboneliği")
        st.write("Bülten aboneliği için abone olun!")

       
        st.write("https://docs.google.com/forms/d/e/1FAIpQLSegOdm2XZ-4bZ3i1zXzmyv4Ejsbculmp0XX7Vj785yBQb3Bag/viewform?vc=0&c=0&w=1&flr=0")


if page=="Metodoloji Notu":
    
     

    # Başlık
    st.title("Web Gıda Fiyat Endeksi (W-GFE) Metodoloji Açıklaması")

    # Analitik Çerçeve ve Kapsam
    st.subheader("Analitik Çerçeve ve Kapsam")
    st.write("""
    Web Gıda Fiyat Endeksinin amacı, TÜFE’deki Gıda ve Alkolsüz İçecekler grubunda yer alan gıda ürünlerinin günlük değişimini ölçerek enflasyon oranını hesaplamaktır. 
    Bu çerçevede, 11 Ekim 2024 endeksi baz olarak "100" seçilmiştir.

    Endeksin kapsamı, TÜİK’in yayınlamış olduğu Aralık 2022 tarihli madde sepetinde yer alan 128 gıda ürünü ile sınırlıdır. Madde ağırlıkları ise bu tarihteki madde ağırlıklarının 2023 ve 2024'te yayınlanan değişikliklerle güncellenmiş halidir.
    """)

    # Hesaplama Kuralları
    st.subheader("Hesaplama Kuralları")
    st.image("1.png")
    st.image("2.png")
    st.image("3.png")
    st.image("4.png")
    st.image("5.png")

    # Mevsimsel Düzeltme
    st.subheader("Mevsimsel Düzeltme")
    st.write("""
    İlk aşamada verilerde mevsimsel düzeltme yapılmayacaktır. Ancak verilerin birikmesiyle ilerleyen dönemlerde, TÜİK’in açıklamış olduğu metodolojiye uygun olarak mevsimsel düzeltme yapılacaktır. 
    Bu sonuçlar web sitesinde ve e-posta aboneliği olan kullanıcılara ayrıca yeni bir endeks olarak bildirilecektir.
    """)

    # Veri Derleme
    st.subheader("Veri Derleme")
    st.write("""
    Toplanan veriler web scraping yöntemiyle Python üzerinden derlenmektedir. Şu an itibariyle her gün 7000'e yakın fiyat toplanmaktadır. 
    Kullanılan kaynaklar, Türkiye genelinde şubeleri bulunan ve online sipariş imkânı olan süpermarket zincirlerinin internet siteleridir.
    """)

    # Sonuçların Açıklanması
    st.subheader("Sonuçların Açıklanması")
    st.write("""
    Her gün toplanan verilerle hesaplanan W-GFE ve madde endeksleri günlük olarak internet sitemizde yayınlanmaktadır. 
    Her ayın 1'inde ise aylık enflasyon oranları duyurulacaktır. Aynı zamanda her bir ürün için kullanılan fiyatlar tablo olarak yayınlanmaktadır. 
    Bu sayede şeffaf bir şekilde yaşanan fiyat değişimleri izlenebilmektedir.
    """)

    # İmza
    st.write("""
    ---
    Bora Kaya  
    HSBC Asset Management Intern
    """)

if page=="Bültenler":
     
     bülten=st.sidebar.selectbox("Bültenler:", ["Ekim 2024","Kasım 2024","Aralık 2024"])
     if bülten=="Aralık 2024":
        
        

        # Başlık
        st.markdown("### <span style='color:black; font-weight:bold;'>Web Gıda Fiyat Endeksi Aralık 2024 Bülteni</span>", unsafe_allow_html=True)

        # Alt başlık
        st.markdown("### <span style='color:red; font-weight:bold;'>Web Gıda Fiyat Endeksi Aralık'ta %2,53 arttı</span>", unsafe_allow_html=True)

        st.markdown("""
        *(Teknik notlara bültenin en aşağısından ulaşabilirsiniz)

        """)

        st.image("grafikler/gfe_aralık.png")

        # Açıklama paragrafı
        st.markdown("""
        Web Gıda Fiyat Endeksi Aralık'ta %2,53 artış kaydederken mevsimsellikten arındırılmış artış %1,42 oldu.
        Sepette ağırlığı en yüksek ürünlere bakıldığında:
        - **Domates**: -%9,37 azalırken
        - **Ayçiçek Yağı**: %2,79
        - **Kuzu Eti**: %1,13
        - **Ekmek**: %5,21
        - **Dana Eti**: %5,03
        - **Yumurta**: %2,14
        - **Tavuk Eti**: %0,07 artış kaydetti.""")

        # İlk resim ekleme
        st.image("grafikler/ürünleraralık.png")

        

        # İkinci resim ekleme
        st.image("grafikler/gruplar_aralık.png")

        # Ek görseller
        st.image("grafikler/harcamasaralık.png")
        st.image("grafikler/meyvesebze_aralık.png")
        st.image("grafikler/haric_aralık.png")
        st.image("grafikler/harcamasaralık.png")
        st.image("grafikler/özel_endeksler_aralık.png")
        

        st.markdown("""
        Mevsimsellikten arındırılmış olarak Web-GFE %1,42 ve fiyat değişimlerinin ortalaması %2,82 ve medyan artış %1,72 olmuştur.
        Meyve ve Sebze hariç fiyat artışı %2,90 ile manşet ile ayrışmıştır.
        SATRIM(Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %1,37 artmıştır
        """)

        st.image("grafikler/egilim_aralık.png")

        # Verisetine erişim bilgisi
        st.markdown("""
        Gıda Fiyat Endeksi ile ilgili tüm verisetlerine [https://web-gfe.streamlit.app](https://web-gfe.streamlit.app) sitesinden ulaşabilir ve indirebilirsiniz.
        """)

        # Küçük boyutta uyarı metni
        st.markdown("""
        <small>*Bu bültenin bir sonraki yayınlanma tarihi 24 Ocak 2025'tir. Burada yer alan bilgi ve analizler tamamen kişisel çalışma olup kesin bir doğruluk içermemekte ve yatırım tavsiyesi içermemektedir.*  
        *TÜİK’in hesaplamasıyla uyumlu olması açısından Aralık ayının ilk 24 günündeki veriler dikkate alınmıştır.*</small>
        """, unsafe_allow_html=True)

        # Hazırlayan bilgisi
        st.markdown("""
        **Hazırlayan**  
        Bora Kaya  
        
        """)






     if bülten=="Kasım 2024":
        

        

        

        # Başlık
        st.markdown("### <span style='color:black; font-weight:bold;'>Web Gıda Fiyat Endeksi Kasım 2024 Bülteni</span>", unsafe_allow_html=True)

        # Alt başlık
        st.markdown("### <span style='color:red; font-weight:bold;'>Web Gıda Fiyat Endeksi Kasım’da %5,32 arttı</span>", unsafe_allow_html=True)

        st.markdown("""
        *(Teknik notlara bültenin en aşağısından ulaşabilirsiniz)

        """)

        # Açıklama paragrafı
        st.markdown("""
        Web Gıda Fiyat Endeksi Kasım’da %5,32 artış kaydederken mevsimsellikten arındırılmış artış %4,31 oldu.
        Sepette ağırlığı en yüksek ürünlere bakıldığında:
        - **Domates**: %7,35
        - **Ayçiçek Yağı**: %6,36
        - **Kuzu Eti**: %8,85
        - **Ekmek**: %4,37
        - **Dana Eti**: %4,84
        - **Yumurta**: %7,28
        - **Tavuk Eti**: %3,47 artış kaydetti.

        a
        """)

        # İlk resim ekleme
        st.image("grafikler/gfe_02-01-2025.png")

        # Harcama gruplarına ilişkin analiz
        st.markdown("""
        Harcama gruplarına bakıldığında **Taze Sebze** grubunun önemli ölçüde endeksi yukarı taşıdığı görülmektedir. 
        Bu bağlamda %5,32 artış yaşanan endekse Taze Sebze grubu endekse 1,47 puan katkı yapmıştır.
        """)

        # İkinci resim ekleme
        st.image("grafikler/gruplar_02-01-2025.png")

        st.image("grafikler/özel_endeksler_02-01-2025.png")
        st.image("grafikler/ürünler_02-01-2025.png")
        st.image("grafikler/meyvesebze_02-01-2025.png")
        st.image("grafikler/haric_02-01-2025.png")
        st.image("grafikler/harcamasa02-01-2025.png")

        st.markdown("""
        Mevsimsel düzeltilmiş ana eğilim göstergelerine bakıldığında düzeltilmiş olarak Web-GFE %4,41 artarken,
        Taze Meyve/Sebze hariç fiyat artışı %5,06 olmuştur.
        Sepet eşit ağırlıklı alındığında fiyat değişimlerinin aritmetik ortalaması %4,17 ve medyan artış %3,59 olmuştur.
        SATRIM(Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %3,33 artmıştır.
        """)

        st.image("grafikler/egilim_02-01-2025.png")

        # Verisetine erişim bilgisi
        st.markdown("""
        Gıda Fiyat Endeksi ile ilgili tüm verisetlerine [https://web-gfe.streamlit.app](https://web-gfe.streamlit.app) sitesinden ulaşabilir ve indirebilirsiniz.
        """)

        # Küçük boyutta uyarı metni
        st.markdown("""
        <small>*Bu bültenin bir sonraki yayınlanma tarihi 24 Aralık 2024'tir. Burada yer alan bilgi ve analizler tamamen kişisel çalışma olup kesin bir doğruluk içermemekte ve yatırım tavsiyesi içermemektedir.*  
        *TÜİK’in hesaplamasıyla uyumlu olması açısından Kasım ayının ilk 24 günündeki veriler dikkate alınmıştır.*</small>
        """, unsafe_allow_html=True)

        # Hazırlayan bilgisi
        st.markdown("""
        **Hazırlayan**  
        Bora Kaya  
        HSBC Asset Management Intern
        """)

          
     if bülten=="Ekim 2024":

        with open("Ekim24.pdf", "rb") as file:
            pdf_data = file.read()

        st.download_button(
            label="📄 Bülteni PDF olarak indir",
            data=pdf_data,
            file_name="Web_Gida_Fiyat_Endeksi_Bulteni.pdf",
            mime="application/pdf"
    )
          

        

        st.markdown("### <span style='color:black; font-weight:bold;'>Web Gıda Fiyat Endeksi Ekim 2024 Bülteni</span>", unsafe_allow_html=True)

        st.markdown("### <span style='color:red; font-weight:bold;'>Web Gıda Fiyat Endeksi Ekim’de %1,79 arttı</span>", unsafe_allow_html=True)

        # Açıklama paragrafı
        st.markdown("""
        11 Ekim’de ölçüme başladığımız W-GFE 11-31 Ekim döneminde %1,79 artış kaydetti. 
        (Bu ay veri eksik olduğundan tahminen Ekim genelinde %2,5-3,0 dolayında artış yaşandığını tahmin ediyoruz)
        """)

        # İlk resim ekleme
        st.image("grafikler/gfe_01-11-2024.png", caption="Ekim 2024 Gıda Endeksi Grafiği")

        # Öne çıkan gruplar
        st.markdown("""
        Bu artışta taze sebze grubu öne çıktı. Sepette ağırlığı en yüksek gruplardan:
        - **Ekmek**: %2,2
        - **Dana Eti**: %1,96
        - **Tavuk Eti**: %0,82
        - **Kuzu Eti**: %1
        - **Ayçiçek Yağı**: %3,32 artış kaydetti.

        Fiyatı en çok artan ve azalan ürünlere bakıldığında: **Maydanoz**, **Kırmızı Lahana**, **Dereotu** artış olarak; **Dolmalık Biber**, **Beyaz Lahana**, **Kabak**, **Limon** ve **Kivi** ise en çok azalanlarda öne çıkmaktadır.
        """)

        # İkinci resim ekleme
        st.image("grafikler/ürünler_01-11-2024.png", caption="Fiyat Değişim Grafiği")

        # Ürün bazlı artışlar
    

        # Ortalama ve medyan değişimler
        st.markdown("""
        Sepet eşit ağırlıklı alındığında fiyat değişimlerinin aritmetik ortalaması %2,27 ve medyan artış %0,75 olmuştur. 
        **SATRIM** (Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %1,26 artmıştır.
        """)

        # Dördüncü resim ekleme
        st.image("grafikler/egilim_01-11-2024.png", caption="SATRIM Göstergesi Grafiği")

        # Verisetine erişim bilgisi
        st.markdown("""
        Gıda Fiyat Endeksi ile ilgili tüm verisetlerine [https://web-gfe.streamlit.app](https://web-gfe.streamlit.app) sitesinden ulaşabilir ve indirebilirsiniz.
        """)

        # Küçük boyutta uyarı metni
        st.markdown("<small>Bu bültenin bir sonraki yayınlanma tarihi 1 Aralık 2024'tür. Burada yer alan bilgi ve analizler tamamen kişisel çalışma olup kesin bir doğruluk içermemekte ve yatırım tavsiyesi içermemektedir.</small>", unsafe_allow_html=True)

        # Hazırlayan bilgisi
        st.markdown("""
        **Hazırlayan**  
        Bora Kaya  
        HSBC Asset Management Intern
        """)


     

if page=="Gıda Fiyat Endeksi":

    st.markdown(
    """
    <style>
    .title {
        font-size: 36px;  
        font-family: 'Freestyle Script', Courier !important;  
        color: red !important;  
        text-align: center;  
    }
    </style>
    <h1 class="title">Hazırlayan: Bora Kaya</h1>
    """, 
    unsafe_allow_html=True)
    
    


    # Örnek veri yükleniyor ve işleniyor
    gfe = pd.read_csv("gfe.csv")
    gfe = gfe.set_index(pd.to_datetime(gfe["Tarih"]))
    gfe = gfe.drop("Tarih", axis=1)

    endeksler=pd.read_csv("endeksler.csv")
    endeksler=endeksler.set_index(endeksler["Ürün"])
    endeksler=endeksler.drop("Ürün",axis=1)
    
   
    endeksler.loc["Gıda"]=gfe["GFE"].values

    

    gida_index = endeksler.loc[['Gıda']]  # "Gıda Fiyat Endeksi"ni seç
    other_indices = endeksler.drop('Gıda').sort_index()  # Geri kalanları alfabetik sıraya koy
    ağırlıklar=pd.read_csv("ağırlıklar.csv")
    ağırlıklar=ağırlıklar.set_index("Ürün")
    ağırlıklar=ağırlıklar.sort_index()
    ağırlıklar=ağırlıklar["Ağırlık"]

    endeksler = pd.concat([gida_index, other_indices])
    endeksler1=endeksler.T
    endeksler1=endeksler1.set_index(pd.date_range(start="2024-10-11",freq="D",periods=(len(endeksler1))))
    endeksler1=endeksler1.drop("Gıda",axis=1)
    endeksler_sa=pd.DataFrame()
    
    
        

    

    gruplar = endeksler.index


    selected_group = st.sidebar.selectbox("Ürün Seçin:", gruplar)
    formatted_dates = gfe.index.strftime("%d.%m.%Y")  # "06.10.2024" formatında

    
   

    
    
        
    selected_group_data = endeksler.loc[selected_group]

   

    selected_group_data=pd.DataFrame(selected_group_data)

        # Datetime index'i atıyoruz
    selected_group_data.index = gfe.index
    selected_group_data["Endeks_2024-10-11"]=100
    selected_group_monthly=selected_group_data.resample('M').mean()
    selected_group_monthlyfull=selected_group_data.resample('M').last()
    from datetime import datetime,timedelta
    import pytz
    gfe1=gfe.copy()
    gfe1["Date"]=pd.to_datetime(gfe1.index)
    gfe1["Ay"]=gfe1["Date"].dt.month
    gfe1["Yıl"]=gfe1["Date"].dt.year    
    month = gfe1["Ay"].iloc[-1]
    onceki=gfe1["Ay"].iloc[-32]
    year=gfe1["Yıl"].iloc[-1] 
    oncekiyear=gfe1["Yıl"].iloc[-1] 
   

        # İlk ve son tarihleri belirleme
    first_date = selected_group_data.index[0].strftime("%d.%m.%Y")  # İlk tarihi formatlama
    last_date = selected_group_data.index[-1].strftime("%d.%m.%Y")  # Son tarihi formatlama
    selected_group_data1=selected_group_data.copy()
    selected_group_data1["Tarih"]=pd.to_datetime(selected_group_data1.index)
    ay_data = selected_group_data1[selected_group_data1['Tarih'].dt.month == month]
    oncekiay_data = selected_group_data1[selected_group_data1['Tarih'].dt.month == onceki]
    
    ilk=ay_data.index[0].strftime("%d.%m.%Y")
    son=ay_data.index[-1].strftime("%d.%m.%Y")

        # Değişim yüzdesini hesaplama
    first_value = selected_group_data.iloc[0,0]  # İlk değer
    last_value = selected_group_data.iloc[-1,0] # Son değer
    change_percent = ((last_value - first_value) / first_value) * 100  # Yüzde değişim
    monthly=np.round(((selected_group_monthly.iloc[-1,0])/(selected_group_monthly.iloc[-2,0])-1)*100,2)

    def hareketli_aylik_ortalama(df):
        değer = df.name  # Kolon ismi
        df = pd.DataFrame(df)
        df["Tarih"] = pd.to_datetime(df.index)  # Tarih sütununu datetime formatına çevir
        df["Gün Sırası"] = df.groupby(df["Tarih"].dt.to_period("M")).cumcount() + 1  # Her ay için gün sırasını oluştur
        
        # Her ay için ilk 24 günü sınırla ve hareketli ortalama hesapla
        df["Aylık Ortalama"] = (
            df[df["Gün Sırası"] <= 24]
            .groupby(df["Tarih"].dt.to_period("M"))[değer]
            .expanding()
            .mean()
            .reset_index(level=0, drop=True)
        )
        
        # Orijinal indeksi geri yükle
        df.index = pd.to_datetime(df.index)
        return df
    

    def hareketli_aylik_ortalama1(df):
            değer=df.name
            df=pd.DataFrame(df)
            df["Tarih"]=pd.to_datetime(df.index)
            df['Aylık Ortalama'] = df.groupby(df['Tarih'].dt.to_period('M'))[değer].expanding().mean().reset_index(level=0, drop=True)
            df.index=pd.to_datetime(df.index)
            return df


# Hareketli aylık ortalama hesaplama
    hareketlima = hareketli_aylik_ortalama(selected_group_data.iloc[:,0])
    hareketlima["Aylık Ortalama"]=hareketlima["Aylık Ortalama"].fillna(method="ffill")
    hareketlima1 = hareketli_aylik_ortalama1(selected_group_data.iloc[:,0])
    



    try:
        monthlylast=np.round(((selected_group_monthlyfull.iloc[-2,0])/(selected_group_monthlyfull.iloc[-3,0])-1)*100,2)
    except:
        monthlylast=np.round(((selected_group_monthlyfull.iloc[-2,0])/(100)-1)*100,2)

        # Yüzdeyi iki ondalık basamak ile sınırlama
    change_percent = round(change_percent, 2)

    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_group} Fiyat Endeksi</h2>", unsafe_allow_html=True)
    
    
    
  
    

    

    

        # Grafiği çizme
    figgalt = go.Figure()
    figgalt.add_trace(go.Scatter(
            x=selected_group_data.index[0:],
            y=selected_group_data.iloc[0:,0].values,
            mode='lines+markers',
            name=selected_group,
            line=dict(color='blue', width=4),
            marker=dict(size=8, color="black")
        ))
    
   
   

        # X ekseninde özelleştirilmiş tarih etiketlerini ayarlıyoruz
    figgalt.update_layout(
            xaxis=dict(
                tickvals=selected_group_data.index[::3],  # Original datetime index
                ticktext=selected_group_data.index[::3].strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
    tarih=pd.read_csv("tarih.csv")
    tarih=tarih.iloc[0,1]
   
    

  
   
    degisim30=np.round((gfe.pct_change(30).iloc[-1,0]*100),2)
    
    from datetime import datetime,timedelta
    import pytz
    gfe1=gfe.copy()
    gfe1["Date"]=pd.to_datetime(gfe1.index)
    gfe1["Ay"]=gfe1["Date"].dt.month
    gfe1["Yıl"]=gfe1["Date"].dt.year    
    month = gfe1["Ay"].iloc[-1]
    onceki=gfe1["Ay"].iloc[-32]
    year=gfe1["Yıl"].iloc[-1] 
    oncekiyear=gfe1["Yıl"].iloc[-32] 

    monthly30=np.round(((selected_group_data.iloc[-1,0])/(selected_group_data.iloc[-31,0])-1)*100,2)
    

    artıs30=selected_group_data.pct_change(30).dropna()*100
    aylıkort=selected_group_data.resample('M').mean()
    aylıkort.loc["2024-10-31"]=selected_group_data.loc["2024-10-12"]

 


    aylıkdegisim=np.round(((((hareketlima1["Aylık Ortalama"].loc[f"{year}-{month}":])/selected_group_data.resample('M').mean().iloc[-2,0]))-1)*100,2)
    degisim_2_24=np.round(((((hareketlima["Aylık Ortalama"].loc[f"{year}-{month}":])/hareketlima["Aylık Ortalama"].loc[f"{oncekiyear}-{onceki}-24"]))-1)*100,2)
    degisim24=np.round(((((hareketlima["Aylık Ortalama"].iloc[-1])/hareketlima["Aylık Ortalama"].loc[f"{oncekiyear}-{onceki}-24"]))-1)*100,2)

    
    
    figg30 = go.Figure()
    figg30.add_trace(go.Scatter(
            x=degisim_2_24.index[0:],
            y=np.round(degisim_2_24.values,2),
            mode='lines+markers',
            name="24 Günlük Değişim",
            line=dict(color='blue', width=4),
            marker=dict(size=8, color="black")
        ))
    figg30.add_trace(go.Scatter(
            x=aylıkdegisim.index[0:],
            y=np.round(aylıkdegisim.values,2),
            mode='lines+markers',
            name="Aylık Ortalama Değişimi",
            line=dict(color='purple', width=4),
            marker=dict(size=8, color="black")
        ))
    figg30.update_layout(
            xaxis=dict(
                tickvals=degisim_2_24.index[0:],  # Original datetime index
                ticktext=degisim_2_24.index[0:].strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )


    
    import plotly.graph_objects as go

    ohlc=pd.read_csv("ohlc.csv").set_index("Unnamed: 0")
    ohlc.index=pd.to_datetime(ohlc.index)
    ohlc.columns= ["High" ,"Low",  "Open", "Close"]
    ohlc=ohlc[["Open","High","Low","Close"]]
    ohlc_data=ohlc.copy()
    


    # Önceki kapanışa göre renkleri belirle
    ohlc_data['Prev_Close'] = ohlc_data['Close'].shift(1)

    # Kapanış değeri önceki kapanıştan yüksekse 'green', düşükse 'red' olacak şekilde renkleri belirle
    ohlc_data['Color'] = ohlc_data['Close'] > ohlc_data['Prev_Close']
    ohlc_data['Color'] = ohlc_data['Color'].map({True: 'green', False: 'red'})

    # Plotly mum grafiğini çiz
    figmum = go.Figure()

    # Yükselen ve düşen mumlar için ayrı ayrı çizgi ekleyerek her mumun rengini özelleştirelim
    for i in range(len(ohlc_data)):
        color = ohlc_data['Color'].iloc[i]
        figmum.add_trace(go.Candlestick(
            x=[ohlc_data.index[i]],
            open=[ohlc_data['Open'].iloc[i]],
            high=[ohlc_data['High'].iloc[i]],
            low=[ohlc_data['Low'].iloc[i]],
            close=[ohlc_data['Close'].iloc[i]],
            increasing_line_color=color,  # Yükselen mumların rengi
            decreasing_line_color=color,  # Düşen mumların rengi
            increasing_fillcolor=color,  # Yükselen mumların dolgu rengi
            decreasing_fillcolor=color,
            name="Web-GFE"   # Düşen mumların dolgu rengi
        ))

    figmum.update_layout(
        title='Web-GFE Mum Grafiği',
        xaxis_title='Tarih',
        yaxis_title='Değer',
        xaxis_rangeslider_visible=False,  # Range slider'ı gizle
        xaxis_tickformat='%d.%m.%Y',  # X eksenindeki tarihi dd.mm.YYYY formatında göster
        width=1400,  # Grafik genişliğini artır
        height=800,  # Grafik yüksekliğini artır
        showlegend=False,  # Legend'ı gizle
        title_font=dict(size=24, family='Arial'),  # Başlık fontu
        xaxis=dict(
            title_font=dict(size=18, family='Arial v'),  # X ekseni başlık fontu
            tickfont=dict(size=14, family='Arial Black')  # X ekseni değer fontu
        ),
        yaxis=dict(
            title_font=dict(size=18, family='Arial Black'),  # Y ekseni başlık fontu
            tickfont=dict(size=14, family='Arial Black')  # Y ekseni değer fontu
        ),
        plot_bgcolor='lightgray',  # Grafik arka plan rengini değiştirme
        paper_bgcolor='white',  # Kağıt arka plan rengini değiştirme
        xaxis_showgrid=True,  # X ekseni grid çizgilerini gösterme
        yaxis_showgrid=True  # Y ekseni grid çizgilerini gösterme

    )
    turkey_tz = pytz.timezone('Europe/Istanbul')
    gfe1=gfe.copy()
    gfe1["Date"]=pd.to_datetime(gfe1.index)
    gfe1["Ay"]=gfe1["Date"].dt.month
    gfe1["Yıl"]=gfe1["Date"].dt.year    
    monthh = gfe1["Ay"].iloc[-1]
    onceki=gfe1["Ay"].iloc[-32]
    year=gfe1["Yıl"].iloc[-1]  
    ay = monthh
    
    months = {1:"Ocak",
              2:"Şubat",
              3:"Mart",
              4:"Nisan",
              5:"Mayıs",
              6:"Haziran",
              7:"Temmuz",
              8:"Ağustos",
              9:"Eylül",
              10:"Ekim",
              11: "Kasım",
              12: "Aralık"
        }
    month=months.get(ay)
    from datetime import datetime,timedelta
    import pytz
    gfe1=gfe.copy()
    gfe1["Date"]=pd.to_datetime(gfe1.index)
    gfe1["Ay"]=gfe1["Date"].dt.month
    gfe1["Yıl"]=gfe1["Date"].dt.year    
    monthh = gfe1["Ay"].iloc[-1]
    onceki=gfe1["Ay"].iloc[-32]
    year=gfe1["Yıl"].iloc[-1]    
    oncekiyear=gfe1["Yıl"].iloc[-32]    
    
    aybasısonu=((ay_data.iloc[-1,0]/oncekiay_data.iloc[-1,0])-1)*100

      

  
   

   

   
    if selected_group!="Gıda":

        st.markdown(f"""
            <h3 style='text-align:left; color:black;'>
                {first_date} - {last_date} Değişimi: <span style='color:red;'>%{change_percent}</span><br>
                {ilk} - {son} Değişimi: <span style='color:red;'>%{np.round(aybasısonu,2)}</span><br>
                {month} Değişimi: <span style='color:red;'>%{ degisim24}</span><br>
                <span style='font-size:15px;'>*Aylık değişim ay içindeki ortalamalara göre hesaplanmaktadır.</span>

                Güncelleme Tarihi: {tarih}
            </h3>
            """, unsafe_allow_html=True)
        
        st.plotly_chart(figgalt)


        
    elif selected_group=="Gıda":
        periyot = st.sidebar.selectbox("Grafik Tipi:", ["Çizgi","Mum"])
   
        st.markdown(f"""
            <h3 style='text-align:left; color:black;'>
                {first_date} - {last_date} Değişimi: <span style='color:red;'>%{change_percent}</span><br>
                {ilk} - {son} Değişimi: <span style='color:red;'>%{np.round(aybasısonu,2)}</span><br>
                {month} Değişimi: <span style='color:red;'>%{ degisim24}</span><br>
                <span style='font-size:15px;'>*Aylık değişim 24 günlük ortalamalara göre hesaplanmaktadır.</span><br>
                

                Güncelleme Tarihi: {tarih}
            </h3>
            """, unsafe_allow_html=True)
        
        if periyot=="Çizgi":
             st.plotly_chart(figgalt)
        elif periyot=="Mum":
             st.plotly_chart(figmum)
             


    
    
    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_group} Fiyat Endeksi Değişimi(%) </h2>", unsafe_allow_html=True)
    st.plotly_chart(figg30)
    
  
    
    
    



    # Tarihleri belirli bir formatta alıyoruz
    formatted_dates = gfe.index.strftime("%d.%m.%Y")  # "06.10.2024" formatında
    def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data

    data=pd.read_csv("sepet.csv")
    try:
        data=data.set_index(data["Unnamed: 0"]).drop("Unnamed: 0",axis=1)
    except:
         data=data.set_index(data["original_index"]).drop("original_index",axis=1)


    fiyatlar=pd.read_csv("sepet.csv")
    try:
        fiyatlar=fiyatlar.set_index(fiyatlar["Unnamed: 0"])
    except:
         fiyatlar=fiyatlar.set_index(fiyatlar["original_index"])
    fiyatlar.index.name="Madde"
    fiyatlar=fiyatlar.sort_index()
    fiyatlar=fiyatlar.rename(columns={"original_index":"Madde"})
    excel_data = to_excel(fiyatlar)
    

    #data=data.drop("Grup",axis=1)
    data.index.name=""
    data=data.drop_duplicates()
    data.loc["Gıda","Ürün"]="Gıda"

    gfe=pd.read_csv("gfe.csv")
    gfe=gfe.set_index(pd.to_datetime(gfe["Tarih"]))
    gfe=gfe.drop("Tarih",axis=1)

    data[data.index=="Gıda"].iloc[:,-1]=gfe.T


    

# Apply the function to each row to calculate the "Değişim" column
    data["Değişim"]=((data.iloc[:,-1].values/data.iloc[:,1].values)-1)*100
    fiyat = data.loc[selected_group]

    endeksler["Değişim"]=((endeksler.iloc[:,-1].values/endeksler.iloc[:,0].values)-1)*100

    def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data

    aylıkenf=np.round(float(((hareketlima["Aylık Ortalama"].resample("M").last().loc[f"{year}-{monthh}"]/hareketlima["Aylık Ortalama"].resample("M").last().loc[f"{oncekiyear}-{onceki}"].iloc[0])-1)*100),2)
    aylıkenf=np.round(hareketlima["Aylık Ortalama"].resample("M").last().pct_change()*100,2).dropna().iloc[1:]

    aylıklar=pd.DataFrame()
    
    kasım=np.round((((selected_group_data.iloc[:,0].loc["2024-11-30"]/selected_group_data.iloc[:,0].loc["2024-10-31"]))-1)*100,2)
    aralık=np.round((((selected_group_data.iloc[:,0].loc["2024-12-31"]/selected_group_data.iloc[:,0].loc["2024-11-30"]))-1)*100,2)
    aylıkenf.loc["2024-11-30"]=kasım
    aylıkenf.loc["2024-12-31"]=aralık
    aylıkenf=aylıkenf.sort_index()
    aylıkenf=pd.DataFrame(aylıkenf)
    aylıkenf.columns=["Aylık Değişim"]
    aylıkenf["Tarih"]=pd.to_datetime(aylıkenf.index)
    
    aylıkenf["Tarih"]=aylıkenf["Tarih"].dt.strftime("%Y-%m")
    aylıkenf=aylıkenf[["Tarih","Aylık Değişim"]]
    aylıkenf=to_excel(aylıkenf)

    
    if selected_group == "Gıda":
        def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data
        
        

        
        endeksler["Madde"]=endeksler.index
        sira = ['Madde'] + [col for col in endeksler.columns if col != 'Madde']


        endeksler = endeksler[sira]
        
        excel_data1 = to_excel(endeksler.drop("Gıda",axis=0))
        gfe["Tarih"]=pd.to_datetime(gfe.index)
        sira = ['Tarih'] + [col for col in gfe.columns if col != 'Tarih']
        gfe = gfe[sira]
       
        excel_data2 = to_excel(gfe)

        aylıkenf=np.round(float(((hareketlima["Aylık Ortalama"].resample("M").last().loc[f"{year}-{monthh}"].iloc[0]/hareketlima["Aylık Ortalama"].resample("M").last().loc[f"{oncekiyear}-{onceki}"].iloc[0])-1)*100),2)
        aylıkenf=np.round(hareketlima["Aylık Ortalama"].resample("M").last().pct_change()*100,2).dropna().iloc[1:]
        aylıklar=pd.DataFrame()
        kasım=np.round((((selected_group_data.iloc[:,0].loc["2024-11-30"]/selected_group_data.iloc[:,0].loc["2024-10-31"]))-1)*100,2)
        aralık=np.round((((selected_group_data.iloc[:,0].loc["2024-12-31"]/selected_group_data.iloc[:,0].loc["2024-11-30"]))-1)*100,2)
        aylıkenf.loc["2024-11-30"]=kasım
        aylıkenf.loc["2024-12-31"]=aralık
        aylıkenf=aylıkenf.sort_index()
        aylıkenf=pd.DataFrame(aylıkenf)
        aylıkenf.columns=["Aylık Değişim"]
        aylıkenf["Tarih"]=pd.to_datetime(aylıkenf.index)
        
        aylıkenf["Tarih"]=aylıkenf["Tarih"].dt.strftime("%Y-%m")
        aylıkenf=aylıkenf[["Tarih","Aylık Değişim"]]
        aylıkenf=to_excel(aylıkenf)
        

        endeksler1=pd.read_csv("endeksler.csv")
        endeksler1=endeksler1.set_index("Ürün")

        endeksler1=(endeksler1).T
        endeksler1=endeksler1.set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(endeksler1)))
        aylık=endeksler1.resample('M').last()
        ekim=endeksler1.resample('M').last()
        
        aylık.loc[pd.to_datetime("2024-09-30")]=100
        aylık=aylık.sort_index()
        aylık=aylık.pct_change().dropna()*100
        aylık=aylık.set_index(pd.date_range(start="2024-10-31",freq="M",periods=len(aylık)))
        aylık.loc["2024-10-31"]=((ekim.loc["2024-10-31"]/100)-1)*100
        aylık.index=aylık.index.strftime("%Y-%m-%d")
        aylık=aylık.T
        toplam=((endeksler1.iloc[-1]/endeksler1.iloc[0])-1)*100
        aylık["Toplam"]=toplam
        aylıkenf1=pd.DataFrame()
        
        for col in endeksler1.columns:

            hareketlimadde=hareketli_aylik_ortalama(endeksler1[col])
            hareketlimadde["Aylık Ortalama"]=hareketlimadde["Aylık Ortalama"].fillna(method="ffill")
            aylıık=hareketlimadde["Aylık Ortalama"].resample("M").last().pct_change().dropna()*100
            aylıık.loc["2024-11-30"]=((hareketlimadde["Aylık Ortalama"].resample("M").last().loc["2024-11-30"]/endeksler1[col].loc["2024-10-12"])-1)*100
            aylıkenf1["Tarih"]=pd.to_datetime(aylıkenf1.index).strftime('%Y-%m')
            aylıkenf1[col]=aylıık

        aylıkenf1.index=aylıkenf1.index.strftime('%Y-%m')

        aylıkenf1=to_excel(aylıkenf1)

        weighted_indices=pd.read_csv("weighted_indices.csv",index_col=0)
        weighted_indices.index=pd.to_datetime(weighted_indices.index)
        weighted_indices_aylık=pd.DataFrame(index=["2024-11","2024-12","2025-01"],columns=weighted_indices.columns)
        for col in weighted_indices.columns:
            weighted_indices_aylık[col].loc["2024-11"]=((hareketli_aylik_ortalama(weighted_indices[col])["Aylık Ortalama"].fillna(method="ffill").loc["2024-11-30"]/weighted_indices[col].loc["2024-10-12"])-1)*100
        for col in weighted_indices.columns:
            weighted_indices_aylık[col].loc["2024-12"]=((hareketli_aylik_ortalama(weighted_indices[col])["Aylık Ortalama"].fillna(method="ffill").loc["2024-12-31"]/hareketli_aylik_ortalama(weighted_indices[col])["Aylık Ortalama"].fillna(method="ffill").loc["2024-11-30"])-1)*100
        tarih=datetime.now().strftime("%Y-%m")
        oncekitarih=(datetime.now()-timedelta(days=31)).strftime("%Y-%m")
        for col in weighted_indices.columns:
            weighted_indices_aylık[col].loc[f"{tarih}"]=((hareketli_aylik_ortalama(weighted_indices[col])["Aylık Ortalama"].fillna(method="ffill").loc[f"{tarih}"].iloc[-1]/hareketli_aylik_ortalama(weighted_indices[col])["Aylık Ortalama"].fillna(method="ffill").loc[f"{oncekitarih}"].iloc[-1])-1)*100
        weighted_indices_aylık["Tarih"]=(weighted_indices_aylık.index)
        sira = ['Tarih'] + [col for col in weighted_indices_aylık.columns if col != 'Tarih']
        weighted_indices_aylık = weighted_indices_aylık[sira]
        weighted_indices_aylık=to_excel(weighted_indices_aylık)


        data=pd.read_excel("harcama gruplarina gore endeks sonuclari.xlsx")
        data=data.iloc[1:,17:].drop([3],axis=0)
        data.columns=data.iloc[0,:]
        data=data.drop(1,axis=0)
        data=data.drop(2,axis=0)
        data=data.set_index(pd.date_range(start="2005-01-31",freq="M",periods=len(data)))
        ağırlık=pd.read_excel("tuketici fiyat endeksi ana grup ve temel baslik agirliklari.xls")


        ağırlık=ağırlık.iloc[:,[0,1,3]]
        ağırlık=ağırlık.dropna()
        ağırlık=ağırlık.iloc[1:]
        ağırlık.columns=["Kod","Madde","Ağırlık"]
        data=data[ağırlık["Kod"].values]
        data.columns=ağırlık["Madde"].values
        weighted_indices=weighted_indices.rename(columns={"Taze Meyveler":"Taze meyveler"})
        ağırlık=ağırlık[ağırlık["Madde"].isin(weighted_indices.columns)]
        ağırlık["Ağırlık"]=ağırlık["Ağırlık"]/ağırlık["Ağırlık"].sum()
        
        gfe_meyvesebze=weighted_indices[["Taze meyveler","Taze sebzeler (patates hariç)","Patates"]]
        ağırlık_meyvesebze=ağırlık[ağırlık["Madde"].isin(gfe_meyvesebze.columns)]
        ağırlık_meyvesebze["Ağırlık"]=ağırlık_meyvesebze["Ağırlık"]/ağırlık_meyvesebze["Ağırlık"].sum()
        tazemeyvesebzeendeks=((gfe_meyvesebze.iloc[:,0]*ağırlık_meyvesebze["Ağırlık"].iloc[0])+((gfe_meyvesebze.iloc[:,1]*ağırlık_meyvesebze["Ağırlık"].iloc[1]))+((gfe_meyvesebze.iloc[:,2]*ağırlık_meyvesebze["Ağırlık"].iloc[2])))
        import numpy as np
        w=pd.read_excel("Weights_2022.xlsx").iloc[:133,:6]
        w["Unnamed: 5"]=w["Unnamed: 5"].fillna(method="ffill")
        meyveler=w[w["Unnamed: 5"].isin(["Taze Meyveler"])]["Unnamed: 1"].values
        sebzeler=w[w["Unnamed: 5"].isin(["Taze sebzeler (patates hariç)"])]["Unnamed: 1"].values
        meyvesebze=np.concatenate([meyveler,sebzeler])

        endekslerr=pd.read_csv("endeksler.csv",index_col=0)

        degisimler=[]
        for col in endekslerr.index:
            ma24=hareketli_aylik_ortalama(pd.DataFrame(endekslerr.loc[col].T).set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(endekslerr.loc[col].T))).iloc[:,0])
            ma24=ma24["Aylık Ortalama"].fillna(method="ffill")
            ay=datetime.now().month
            yıl=datetime.now().year

            ay=f"0{ay}"
            önceki_ay=(datetime.now()-timedelta(days=31)).month
            önceki_yıl=(datetime.now()-timedelta(days=31)).year
            degisim=(((ma24.loc[f"{yıl}-{ay}"].iloc[-1]/ma24.loc[f"{önceki_yıl}-{önceki_ay}"].iloc[-1]))-1)*100
            degisimler.append(degisim)

        endekslerr["Değişim"]=degisimler 

        ağırlıklar=pd.read_csv("ağırlıklar.csv",index_col=0)
        ağırlıklar["Ürün"]=ağırlıklar.index
        ağırlıklar=ağırlıklar.sort_index()
        del ağırlıklar["Unnamed: 0"]
        ağırlıklar["Ürün"]=ağırlıklar.index
        meyvesebzeharic=ağırlıklar[~ağırlıklar["Ürün"].isin(meyvesebze)]["Ürün"].values

        ağırlık_meyvesebzeharic=ağırlıklar[ağırlıklar["Ürün"].isin(meyvesebzeharic)]
        ağırlık_meyvesebzeharic["Ağırlık"]=ağırlık_meyvesebzeharic["Ağırlık"]/ağırlık_meyvesebzeharic["Ağırlık"].sum()

        meyvesebze_haricendeks=[]
        for range in endekslerr.columns[:-1]:
            
            meyvesebze_haricendeks.append((endekslerr[range].loc[meyvesebzeharic]*ağırlık_meyvesebzeharic["Ağırlık"].values).sum())
        meyvesebze_haricendeks=pd.DataFrame(meyvesebze_haricendeks,index=endekslerr.columns[:-1],columns=["Meyve Sebze Haric Endeks"])
        meyvesebze_haricendeks=meyvesebze_haricendeks.set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(meyvesebze_haricendeks)))

        özelgöstergeler=pd.DataFrame()
        özelgöstergeler["Tarih"]=tazemeyvesebzeendeks.index
        özelgöstergeler["Taze Meyve-Sebze"]=tazemeyvesebzeendeks.values
        özelgöstergeler["Meyve/Sebze Hariç"]=meyvesebze_haricendeks.values
        özelgöstergeler=to_excel(özelgöstergeler)

                
        st.download_button(
            label="📊 Fiyat Listesini İndir",
            data=excel_data,
            file_name='fiyatlar.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="📊 Madde Endekslerini İndir",
            data=excel_data1,
            file_name='endeksler.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="📊 Web-Gıda Fiyat Endeksi İndir",
            data=excel_data2,
            file_name='gfe.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        

        st.download_button(
            label="📊 Web-GFE Aylık Değişim Oranlarını İndir",
            data=aylıkenf,
            file_name='gfeaylıkdegisimoranları.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="📊 Maddeler Aylık Değişim Oranlarını İndir",
            data=aylıkenf1,
            file_name='maddeaylıkdegisimoranları.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="📊 Harcama Grupları Aylık Değişim Oranlarını İndir",
            data=weighted_indices_aylık,
            file_name='harcamagruplarıaylıkdegisimoranları.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="📊 Özel Kapsamlı GFE Göstergeleri İndir",
            data=özelgöstergeler,
            file_name='özelgöstergeler.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        import streamlit as st

        # Sidebar layout
        import streamlit as st

# Sidebar layout
        import streamlit as st

        
        
          



        endeksler1=pd.read_csv("endeksler.csv")
        endeksler1=endeksler1.set_index("Ürün")

        endeksler1=(endeksler1).T
        endeksler1=endeksler1.set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(endeksler1)))
        aylık=endeksler1.resample('M').last()
        ekim=endeksler1.resample('M').last()
        
        aylık.loc[pd.to_datetime("2024-09-30")]=100
        aylık=aylık.sort_index()
        aylık=aylık.pct_change().dropna()*100
        aylık=aylık.set_index(pd.date_range(start="2024-10-31",freq="M",periods=len(aylık)))
        aylık.loc["2024-10-31"]=((ekim.loc["2024-10-31"]/100)-1)*100
        aylık.index=aylık.index.strftime("%Y-%m-%d")
        aylık=aylık.T
        toplam=((endeksler1.iloc[-1]/endeksler1.iloc[0])-1)*100
        aylık["Toplam"]=toplam
        
    else:
        st.markdown(f"<h2 style='text-align:left; color:black;'>Fiyat Listesi</h2>", unsafe_allow_html=True)
        try:
            st.dataframe(fiyat.drop("Değişim",axis=1))
        except:
             st.dataframe(fiyat)

if page=="Madde Endeksleri":
    def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data
    def hareketli_aylik_ortalama(df):
        değer = df.name  # Kolon ismi
        df = pd.DataFrame(df)
        df["Tarih"] = pd.to_datetime(df.index)  # Tarih sütununu datetime formatına çevir
        df["Gün Sırası"] = df.groupby(df["Tarih"].dt.to_period("M")).cumcount() + 1  # Her ay için gün sırasını oluştur
        
        # Her ay için ilk 24 günü sınırla ve hareketli ortalama hesapla
        df["Aylık Ortalama"] = (
            df[df["Gün Sırası"] <= 24]
            .groupby(df["Tarih"].dt.to_period("M"))[değer]
            .expanding()
            .mean()
            .reset_index(level=0, drop=True)
        )
        
        # Orijinal indeksi geri yükle
        df.index = pd.to_datetime(df.index)
        return df
    data=pd.read_csv("sepet.csv")
    try:
        data=data.set_index(data["Unnamed: 0"]).drop("Unnamed: 0",axis=1)
    except:
         data=data.set_index(data["original_index"]).drop("original_index",axis=1)
    fiyatlar=pd.read_csv("sepet.csv")
    try:
        fiyatlar=fiyatlar.set_index(fiyatlar["Unnamed: 0"])
    except:
         fiyatlar=fiyatlar.set_index(fiyatlar["original_index"])

    fiyatlar.index.name="Madde"
    fiyatlar=fiyatlar.sort_index()
    fiyatlar=fiyatlar.rename(columns={"original_index":"Madde"})
    
   
    

    #data=data.drop("Grup",axis=1)
    data.index.name=""
    data=data.drop_duplicates()
    data.loc["Gıda","Ürün"]="Gıda"

    gfe=pd.read_csv("gfe.csv")
    gfe=gfe.set_index(pd.to_datetime(gfe["Tarih"]))
    gfe=gfe.drop("Tarih",axis=1)

    data[data.index=="Gıda"].iloc[:,-1]=gfe.T
    endeksler1=pd.read_csv("endeksler.csv")
    endeksler1=endeksler1.set_index("Ürün")

    endeksler1=(endeksler1).T
    endeksler1=endeksler1.set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(endeksler1)))
    aylık=endeksler1.resample('M').last()
    ekim=endeksler1.resample('M').last()
    
    aylık.loc[pd.to_datetime("2024-09-30")]=100
    aylık=aylık.sort_index()
    aylık=aylık.pct_change().dropna()*100
    aylık=aylık.set_index(pd.date_range(start="2024-10-31",freq="M",periods=len(aylık)))
    aylık.loc["2024-10-31"]=((ekim.loc["2024-10-31"]/100)-1)*100
    aylık.index=aylık.index.strftime("%Y-%m-%d")
    aylık=aylık.T
    toplam=((endeksler1.iloc[-1]/endeksler1.iloc[0])-1)*100
    aylık["Toplam"]=toplam
    


    
 

    st.dataframe(endeksler1)
    st.markdown(f"<h2 style='text-align:left; color:black;'>Aylık Artışlar(Ay Başı-Ay Sonu Artışı)</h2>", unsafe_allow_html=True)
    st.dataframe(aylık)



    


     
if page=="Harcama Grupları":
    import pytz
    def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data
    gfe = pd.read_csv("gfe.csv")
    gfe = gfe.set_index(pd.to_datetime(gfe["Tarih"]))
    gfe = gfe.drop("Tarih", axis=1)
    endeksler=pd.read_csv("endeksler.csv")
    endeksler=endeksler.set_index(endeksler["Ürün"])
    endeksler=endeksler.drop("Ürün",axis=1)
    endeksler=endeksler.T
    endeksler=endeksler.set_index(pd.date_range(start="2024-10-11",freq="D",periods=len(endeksler)))
    ağırlıklar=pd.read_excel("Weights_2022.xlsx")
    cols=ağırlıklar["Unnamed: 1"].dropna().iloc[2:130].values
    ağırlıklar=ağırlıklar[["Unnamed: 5","Unnamed: 4"]]
    ağırlıklar["Unnamed: 4"]=ağırlıklar["Unnamed: 4"]*100
    ağırlıklar=ağırlıklar.iloc[4:132]
    ağırlıklar=ağırlıklar.fillna(method="ffill")
    ağırlıklar.columns=["Grup","Ağırlık"]
    endeksler=endeksler[cols]
    gruplar=pd.concat([ağırlıklar.reset_index().drop("index",axis=1),endeksler.T.reset_index().iloc[:,1:]],axis=1)
    

    # Drop 'Toplam_Ağırlık' for display purposes
    weighted_indices=pd.read_csv("weighted_indices.csv",index_col=0)
    weighted_indices.index=pd.to_datetime(weighted_indices.index)
    cols=weighted_indices.columns
    gfe=pd.read_csv("gfe.csv")
    gfe=gfe.set_index(pd.to_datetime(gfe["Tarih"]))
    gfe=gfe.drop("Tarih",axis=1)
    harcamam=weighted_indices.copy()
    harcamam["Web-GFE"]=gfe["GFE"]

   
    

    selected_indice = st.sidebar.selectbox("Grup Seçin:", cols)


    selected_indice_data=weighted_indices[selected_indice]
 

    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_indice} Fiyat Endeksi</h2>", unsafe_allow_html=True)

    first=selected_indice_data.index[0].strftime("%d.%m.%Y")
    last=selected_indice_data.index[-1].strftime("%d.%m.%Y")

    toplam=np.round((((selected_indice_data[-1])/selected_indice_data[0])-1)*100,2)
    aylık=np.round(((selected_indice_data.resample('M').mean().iloc[-1]/selected_indice_data.resample('M').mean().iloc[-2])-1)*100,2)
    degisim30=np.round(selected_indice_data.pct_change(30).iloc[-1]*100,2)
    artıs30harcama=np.round(selected_indice_data.pct_change(30).dropna()*100,2)

    def hareketli_aylik_ortalama(df):
        değer = df.name  # Kolon ismi
        df = pd.DataFrame(df)
        df["Tarih"] = pd.to_datetime(df.index)  # Tarih sütununu datetime formatına çevir
        df["Gün Sırası"] = df.groupby(df["Tarih"].dt.to_period("M")).cumcount() + 1  # Her ay için gün sırasını oluştur
        
        # Her ay için ilk 24 günü sınırla ve hareketli ortalama hesapla
        df["Aylık Ortalama"] = (
            df[df["Gün Sırası"] <= 24]
            .groupby(df["Tarih"].dt.to_period("M"))[değer]
            .expanding()
            .mean()
            .reset_index(level=0, drop=True)
        )
        
        # Orijinal indeksi geri yükle
        df.index = pd.to_datetime(df.index)
        return df

    def hareketli_aylik_ortalama1(df):
            değer=df.name
            df=pd.DataFrame(df)
            df["Tarih"]=pd.to_datetime(df.index)
            df['Aylık Ortalama'] = df.groupby(df['Tarih'].dt.to_period('M'))[değer].expanding().mean().reset_index(level=0, drop=True)
            df.index=pd.to_datetime(df.index)
            return df
    hareketlimaharcama = hareketli_aylik_ortalama(selected_indice_data)
    hareketlimaharcama["Aylık Ortalama"]=hareketlimaharcama["Aylık Ortalama"].fillna(method="ffill")
    hareketlimaharcama1 = hareketli_aylik_ortalama1(selected_indice_data)


    from datetime import datetime,timedelta
    turkey_tz = pytz.timezone('Europe/Istanbul')
    ay = datetime.now(tz=turkey_tz).month
    months = {1:"Ocak",
              2:"Şubat",
              3:"Mart",
              4:"Nisan",
              5:"Mayıs",
              6:"Haziran",
              7:"Temmuz",
              8:"Ağustos",
              9:"Eylül",
              10:"Ekim",
              11: "Kasım",
              12: "Aralık"
        }
    
    gfe1=gfe.copy()
    gfe1["Date"]=pd.to_datetime(gfe1.index)
    gfe1["Ay"]=gfe1["Date"].dt.month
    gfe1["Yıl"]=gfe1["Date"].dt.year    
    month = gfe1["Ay"].iloc[-1]
    ay = gfe1["Ay"].iloc[-1]
    onceki=gfe1["Ay"].iloc[-32]
    year=gfe1["Yıl"].iloc[-1] 
    oncekiyear=gfe1["Yıl"].iloc[-32] 
    month=months.get(month)
    
    weighted_indices["Web-GFE"]=gfe["GFE"]
    for grup in harcamam.columns:

        ort24=hareketli_aylik_ortalama(harcamam[grup])
        harcamam[grup]=ort24["Aylık Ortalama"].fillna(method="ffill")
    harcamaort=weighted_indices.resample('M').mean()
    harcamaort.loc["2024-10-31"]=weighted_indices.loc["2024-10-12"]
    grouped=pd.DataFrame()
    grouped[f"{month} Artış Oranı"]=((harcamam.iloc[-1]/harcamam.loc[f"{oncekiyear}-{onceki}-24"])-1)*100
    grouped=grouped.sort_values(by=f"{month} Artış Oranı")
    grouped=grouped.astype(float)

    aylıkortharcama=selected_indice_data.resample('M').mean()
    aylıkortharcama.loc["2024-10-31"]=selected_indice_data.loc["2024-10-12"]
    aylıkdegisimharcama=np.round(((((hareketlimaharcama1["Aylık Ortalama"].loc[f"{year}-{ay}-01":])/selected_indice_data.resample('M').mean().loc[f"{oncekiyear}-{onceki}"].iloc[0]))-1)*100,2)
    degisim24harcama=np.round(((((hareketlimaharcama["Aylık Ortalama"].loc[f"{year}-{ay}-01":])/hareketlimaharcama["Aylık Ortalama"].loc[f"{oncekiyear}-{onceki}-24"]))-1)*100,2)
    degisim24=np.round(((((hareketlimaharcama["Aylık Ortalama"].iloc[-1])/hareketlimaharcama["Aylık Ortalama"].loc[f"{oncekiyear}-{onceki}-24"]))-1)*100,2)


    
    




    st.markdown(f"""
            <h3 style='text-align:left; color:black;'>
                {first} - {last} Değişimi: <span style='color:red;'>%{toplam}</span><br>
                {month} Değişimi: <span style='color:red;'>%{degisim24}</span><br>
                <span style='font-size:15px;'>*Aylık değişim ay içindeki ortalamalara göre hesaplanmaktadır.</span>
            </h3>
            """, unsafe_allow_html=True)
    
    
    weighted_indices["Tarih"]=pd.to_datetime(weighted_indices.index)
    column_to_move = 'Tarih'
    cols = ["Tarih"] + [col for col in weighted_indices.columns if col != column_to_move]
    weighted_indices = weighted_indices[cols]
    harcamaenf=harcamam.resample('M').last().pct_change().dropna()*100
    harcamaenf.loc["2024-11-30"]=((harcamam.resample('M').last().loc["2024-11-30"]/harcamaort.loc["2024-10-31"])-1)*100
    harcamaenf=harcamaenf.set_index(pd.date_range(start="2024-10-31",freq="M",periods=len(harcamaenf)))
    
    
    for col in harcamaenf.columns:
        harcamaenf[col]=np.round(harcamaenf[col],2)
    harcamaenf=harcamaenf.T
    harcamaenf["Grup"]=harcamaenf.index
    sira = ['Grup'] + [col for col in harcamaenf.columns if col != 'Grup']


    harcamaenf = harcamaenf[sira]

    harcamaenf.columns = [col.strftime('%Y-%m') if isinstance(col, pd.Timestamp) else col for col in harcamaenf.columns]

    
    harcamaylıklar=to_excel(harcamaenf)
    
    excel_data10 = to_excel(weighted_indices)
    st.download_button(
            label="📊 Harcama Grupları İndir",
            data=excel_data10,
            file_name='harcamagrupları.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    st.download_button(
            label="📊 Harcama Grupları Aylık Artış Oranları İndir",
            data=harcamaylıklar,
            file_name='harcamagruplarıaylıkartışlar.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


    figggrup = go.Figure()
    figggrup.add_trace(go.Scatter(
            x=selected_indice_data.index[0:],
            y=selected_indice_data.values,
            mode='lines+markers',
            name=selected_indice,
            line=dict(color='blue', width=4),
            marker=dict(size=8, color="black")
        ))
    

    
    

    
    
    figggrup.update_layout(
            xaxis=dict(
                tickvals=selected_indice_data.index[0:],  # Original datetime index
                ticktext=selected_indice_data.index[0:].strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
    
    figg31 = go.Figure()
    figg31.add_trace(go.Scatter(
            x=degisim24harcama.index[0:],
            y=np.round(degisim24harcama.values,2),
            mode='lines+markers',
            name="24 Günlük Değişim",
            line=dict(color='blue', width=4),
            marker=dict(size=8, color="black")
        ))
    figg31.add_trace(go.Scatter(
            x=aylıkdegisimharcama.index[0:],
            y=np.round(aylıkdegisimharcama.values,2),
            mode='lines+markers',
            name="Aylık Ortalama Değişimi",
            line=dict(color='purple', width=4),
            marker=dict(size=8, color="black")
        ))
    figg31.update_layout(
            xaxis=dict(
                tickvals=artıs30harcama.index[0:],  # Original datetime index
                ticktext=artıs30harcama.index[0:].strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
    
    st.plotly_chart(figggrup)
    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_indice} Grubu Değişimi(%) </h2>", unsafe_allow_html=True)
    st.plotly_chart(figg31)
    import numpy as np
    import plotly.graph_objects as go

  
    # Renkler
    import plotly.graph_objects as go
    


# Renkler
    colors = ['red' if label == 'Web-GFE' else 'blue' for label in grouped.index]

    # İlk 42 karakteri almak için index etiketlerini kısaltma
    shortened_index = [label[:42] for label in grouped.index]

    # Grafik oluşturma
    figartıs = go.Figure()

    # Verileri ekleme
    figartıs.add_trace(go.Bar(
        y=shortened_index,  # Kısaltılmış index etiketleri
        x=grouped[f'{month} Artış Oranı'],
        orientation='h', 
        marker=dict(color=colors),
        name=f'{month} Artış Oranı',
    ))

    # Başlık ve etiketler
    figartıs.update_layout(
        xaxis_title='Artış Oranı (%)',
        yaxis_title='Grup',
        xaxis=dict(tickformat='.2f'),
        bargap=0.2,  # Çubuklar arasındaki boşluk
        height=1200,  # Grafik boyutunu artırma
        font=dict(family="Arial Black", size=14, color="black"),  # Yazı tipi ve kalınlık
        yaxis=dict(
            tickfont=dict(family="Arial Black", size=14, color="black"),  # Y eksenindeki etiketlerin rengi
            tickmode='array',  # Manuel olarak etiketleri belirlemek için
            tickvals=list(range(len(grouped.index))),  # Her bir index için bir yer belirle
            ticktext=shortened_index  # Kısaltılmış index etiketleri
        )
    )

    # Etiket ekleme
    for i, value in enumerate(grouped[f'{month} Artış Oranı']):
        if value >= 0:
            # Pozitif değerler sol tarafta
            figartıs.add_annotation(
                x=value, 
                y=shortened_index[i], 
                text=f"{value:.2f}%", 
                showarrow=False, 
                font=dict(size=14, family="Arial Black"),  # Etiketler için yazı tipi
                align='left', 
                xanchor='left', 
                yanchor='middle'
            )
        else:
            # Negatif değerler sağ tarafta
            figartıs.add_annotation(
                x=value, 
                y=shortened_index[i], 
                text=f"{value:.2f}%", 
                showarrow=False, 
                font=dict(size=14, family="Arial Black"),  # Etiketler için yazı tipi
                align='right', 
                xanchor='right', 
                yanchor='middle'
            )




    st.markdown(f"<h2 style='text-align:left; color:black;'>Web-GFE Harcama Grupları {month} Ayı Artış Oranları(24 Günlük Ortalama)</h2>", unsafe_allow_html=True)
    st.plotly_chart(figartıs)



    

    






    


