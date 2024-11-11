import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO
from datetime import datetime
import base64
st.set_page_config(page_title="Web-Gıda Fiyat Endeksi")
tabs=["Gıda Fiyat Endeksi","Metodoloji Notu","Bültenler","Bülten Aboneliği"]
page=st.sidebar.radio("Sekmeler",tabs)

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
    st.write("""
    Endeks hesaplanırken, öncelikle her bir madde için günlük olarak fiyatlar toplanmakta, her gün sonunda önceki güne göre yüzde değişimi alınarak, bu değişimlerin o ürün bazında ortalaması alınıp üründe yaşanan ortalama günlük fiyat değişimi belirlenmektedir. 
    Sonrasında bu değişim önceki günün endeksine eklenerek yeni endeks seviyesi hesaplanmaktadır. (Örneğin, bir üründe baz endeks 100 seçildiğinde, ertesi günde ortalama değişim %2 olursa yeni endeks 102 olmaktadır.)

    Her bir madde için endeks seviyeleri hesaplandıktan sonra bu endeksler madde ağırlıklarıyla çarpılarak ağırlıklı endeks oluşturulur ve bunlar toplanarak Web Gıda Fiyat Endeksi’nin değeri hesaplanır.

    Günlük olarak elde edilen W-GFE’nin ay içindeki ortalaması alınarak, önceki ayın ortalamasıyla kıyaslanır ve aylık enflasyon bulunur.
    """)

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
     bülten=st.sidebar.selectbox("Bültenler:", ["Ekim 2024"])
     if bülten=="Ekim 2024":

        with open("Ekim24.pdf", "rb") as file:
            pdf_data = file.read()

        st.download_button(
            label="📄 Bülteni PDF olarak indir",
            data=pdf_data,
            file_name="Web_Gida_Fiyat_Endeksi_Bulteni.pdf",
            mime="application/pdf"
    )
          

        

        # Başlık, kalın ve kırmızı
        st.markdown("### <span style='color:red; font-weight:bold;'>Web Gıda Fiyat Endeksi Ekim’de %1,79 arttı</span>", unsafe_allow_html=True)

        # Açıklama paragrafı
        st.markdown("""
        11 Ekim’de ölçüme başladığımız W-GFE 11-31 Ekim döneminde %1,79 artış kaydetti. 
        (Bu ay veri eksik olduğundan tahminen Ekim genelinde %2,5-3,0 dolayında artış yaşandığını tahmin ediyoruz)
        """)

        # İlk resim ekleme
        st.image("gfe_01-11-2024.png", caption="Ekim 2024 Gıda Endeksi Grafiği")

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
        st.image("ürünler_01-11-2024.png", caption="Fiyat Değişim Grafiği")

        # Ürün bazlı artışlar
        st.markdown("""
        Ürün çeşidi özelinde fiyat değişimlerine baktığımızda en çok artış %120 ile **Kepek Ekmeği** ve %100 artış ile **Mısır Gevreği**nde görülmüştür. 
        En çok fiyat düşüşü yaşanan ürün çeşidi ise **Sardalya** olmuştur.
        """)

        # Üçüncü resim ekleme
        st.image("çeşitler_01-11-2024.png", caption="Ürün Bazlı Fiyat Değişim Grafiği")

        # Ortalama ve medyan değişimler
        st.markdown("""
        Sepet eşit ağırlıklı alındığında fiyat değişimlerinin aritmetik ortalaması %2,27 ve medyan artış %0,75 olmuştur. 
        **SATRIM** (Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %1,26 artmıştır.
        """)

        # Dördüncü resim ekleme
        st.image("egilim_01-11-2024.png", caption="SATRIM Göstergesi Grafiği")

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
    from statsmodels.tsa.statespace.structural import UnobservedComponents

    for col in endeksler1.columns:
        model=UnobservedComponents(endeksler1[col],level="local level",seasonal=7,stochastic_seasonal=True)
        results=model.fit()
        seasonal=results.smoothed_state[1]
        sa=endeksler1[col]-seasonal
        endeksler_sa[col]=sa

    for col in endeksler1.columns:
        endeksler_sa[col]=endeksler_sa[col]*ağırlıklar.loc[col]
    gfe_sa=endeksler_sa.sum(axis=1)
    
        

    

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


        # İlk ve son tarihleri belirleme
    first_date = selected_group_data.index[0].strftime("%d.%m.%Y")  # İlk tarihi formatlama
    last_date = selected_group_data.index[-1].strftime("%d.%m.%Y")  # Son tarihi formatlama

        # Değişim yüzdesini hesaplama
    first_value = selected_group_data.iloc[0,0]  # İlk değer
    last_value = selected_group_data.iloc[-1,0] # Son değer
    change_percent = ((last_value - first_value) / first_value) * 100  # Yüzde değişim
    monthly=np.round(((selected_group_monthly.iloc[-1,0])/(selected_group_monthly.iloc[-2,0])-1)*100,2)


    try:
        monthlylast=np.round(((selected_group_monthlyfull.iloc[-2,0])/(selected_group_monthlyfull.iloc[-3,0])-1)*100,2)
    except:
        monthlylast=np.round(((selected_group_monthlyfull.iloc[-2,0])/(100)-1)*100,2)

        # Yüzdeyi iki ondalık basamak ile sınırlama
    change_percent = round(change_percent, 2)

    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_group} Fiyat Endeksi</h2>", unsafe_allow_html=True)
    from statsmodels.tsa.statespace.structural import UnobservedComponents
    model=UnobservedComponents(selected_group_data.iloc[:,0],level="local level",seasonal=7,stochastic_seasonal=True)
    results=model.fit()
    seasonal=results.smoothed_state[1]
    seasonal_adjuested=np.round(selected_group_data[selected_group]-seasonal,2)

    

    

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
    
    if selected_group=="Gıda":
         figgalt.add_trace(go.Scatter(
            x=gfe_sa.index,
            y=gfe_sa.values,
            mode='lines+markers',
            name="Mevsimsel Düzeltilmiş",
            line=dict(color='red', width=4),
            marker=dict(size=8, color="orange")
        ))
         
    elif selected_group!="Gıda":

        figgalt.add_trace(go.Scatter(
                x=seasonal_adjuested.index,
                y=seasonal_adjuested.values,
                mode='lines+markers',
                name="Mevsimsel Düzeltilmiş",
                line=dict(color='red', width=4),
                marker=dict(size=8, color="orange")
            ))

        # X ekseninde özelleştirilmiş tarih etiketlerini ayarlıyoruz
    figgalt.update_layout(
            xaxis=dict(
                tickvals=selected_group_data.index[0:],  # Original datetime index
                ticktext=selected_group_data.index[0:].strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )
    tarih=pd.read_csv("tarih.csv")
    tarih=tarih.iloc[0,1]
    seasonal_adjuested_aylık=seasonal_adjuested.resample('M').mean()
    seasonal_adjuested_ekim=((seasonal_adjuested.resample('M').last()/100)-1)*100
    change_percent_sa=seasonal_adjuested_ekim.copy().iloc[-1]
    seasonal_adjuested_ekim1=np.round(seasonal_adjuested_ekim.loc["2024-10-31"],2)

    seasonal_adjusted_last=np.round(((seasonal_adjuested_aylık.iloc[-1]/seasonal_adjuested_aylık.iloc[-2])-1)*100,2)

    gfe_sa_aylık=gfe_sa.resample('M').mean()  
    gfe_sa_ekim=((gfe_sa.resample('M').last()/100)-1)*100
    change_percent_sa_gfe=gfe_sa_ekim.copy().iloc[-1]
    gfe_sa_ekim1=np.round(gfe_sa_ekim.loc["2024-10-31"],2)
    gfe_sa_last=np.round(((gfe_sa_aylık.iloc[-1]/gfe_sa_aylık.iloc[-2])-1)*100,2)  
    degisim30=np.round((gfe.pct_change(30).iloc[-1,0]*100),2)
    degisimsa30=np.round((seasonal_adjuested.pct_change(30).iloc[-1]*100),2)


    monthly30=np.round(((selected_group_monthly.iloc[-1,0])/(selected_group_monthly.iloc[-31,0])-1)*100,2)
    gfesa_30=gfe_sa.pct_change(30)*100

   
    if selected_group!="Gıda":

        st.markdown(f"""
            <h3 style='text-align:left; color:black;'>
                {first_date} - {last_date} Değişimi: <span style='color:red;'>%{change_percent}(Mevsimsel Düzeltilmiş:%{np.round(seasonal_adjuested_ekim.iloc[-1],2)})</span><br>
                Kasım Değişimi: <span style='color:red;'>%{ monthly}(Mevsimsel Düzeltilmiş:%{seasonal_adjusted_last})</span><br>
                30 Günlük Değişim: <span style='color:red;'>%{ monthly30}(Mevsimsel Düzeltilmiş:%{degisimsa30})</span><br>
                <span style='font-size:15px;'>*Aylık değişim ay içindeki ortalamalara göre hesaplanmaktadır.</span>

                Güncelleme Tarihi: {tarih}
            </h3>
            """, unsafe_allow_html=True)
        
    elif selected_group=="Gıda":
        st.markdown(f"""
            <h3 style='text-align:left; color:black;'>
                {first_date} - {last_date} Değişimi: <span style='color:red;'>%{change_percent}(Mevsimsel Düzeltilmiş:%{np.round(gfe_sa_ekim.iloc[-1],2)})</span><br>
                Kasım Değişimi: <span style='color:red;'>%{monthly}(Mevsimsel Düzeltilmiş:%{gfe_sa_last})</span><br>
                30 Günlük Değişim: <span style='color:red;'>%{ degisim30}(Mevsimsel Düzeltilmiş:%{gfesa_30})</span><br>
                <span style='font-size:15px;'>*Aylık değişim ay içindeki ortalamalara göre hesaplanmaktadır.</span>

                Güncelleme Tarihi: {tarih}
            </h3>
            """, unsafe_allow_html=True)


        # Grafik Streamlit'te gösteriliyor
    st.plotly_chart(figgalt)

        # Yüzde değişimi ve tarihleri yazdırma
    



    # Tarihleri belirli bir formatta alıyoruz
    formatted_dates = gfe.index.strftime("%d.%m.%Y")  # "06.10.2024" formatında

    data=pd.read_csv("sepet.csv")
    data=data.set_index(data["Unnamed: 0"]).drop("Unnamed: 0",axis=1)
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

    
    if selected_group == "Gıda":
        def to_excel(df):
            output = BytesIO()
            # Pandas'ın ExcelWriter fonksiyonunu kullanarak Excel dosyasını oluştur
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')  # index=False ile index'i dahil etmiyoruz
            processed_data = output.getvalue()  # Bellekteki dosya verisini al
            return processed_data

        # Excel dosyasını indirme düğmesi ekleme
        excel_data = to_excel(data)
        endeksler["Madde"]=endeksler.index
        sira = ['Madde'] + [col for col in endeksler.columns if col != 'Madde']


        endeksler = endeksler[sira]
        
        excel_data1 = to_excel(endeksler.drop("Gıda",axis=0))
        gfe["Tarih"]=pd.to_datetime(gfe.index)
        sira = ['Tarih'] + [col for col in gfe.columns if col != 'Tarih']
        gfe = gfe[sira]
        gfe["Adjusted"]=gfe_sa
        excel_data2 = to_excel(gfe)


        st.download_button(
            label="Fiyat Listesini İndir",
            data=excel_data,
            file_name='fiyatlar.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="Madde Endekslerini İndir",
            data=excel_data1,
            file_name='endeksler.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.download_button(
            label="Web-Gıda Fiyat Endeksi İndir",
            data=excel_data2,
            file_name='gfe.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
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
        if fiyat.dropna().empty:
            pass
        else:
                st.markdown(f"<h2 style='text-align:left; color:black;'>Aylık Artışlar</h2>", unsafe_allow_html=True)
                st.dataframe(aylık)
                st.dataframe(endeksler.drop("Madde",axis=1))
    else:
        st.markdown(f"<h2 style='text-align:left; color:black;'>Fiyat Listesi</h2>", unsafe_allow_html=True)
        st.dataframe(fiyat)

    

    






    


