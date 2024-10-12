import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO
st.set_page_config(page_title="Web-Gıda Fiyat Endeksi")
tabs=["Gıda Fiyat Endeksi"]
page=st.sidebar.radio("Sekmeler",tabs)


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


    endeksler = pd.concat([gida_index, other_indices])

    
        

    

    gruplar = endeksler.index


    selected_group = st.sidebar.selectbox("Ürün Seçin:", gruplar)
    formatted_dates = gfe.index.strftime("%d.%m.%Y")  # "06.10.2024" formatında

    
   

    
    
        
    selected_group_data = endeksler.loc[selected_group]

    selected_group_data=pd.DataFrame(selected_group_data)

        # Datetime index'i atıyoruz
    selected_group_data.index = gfe.index

        # İlk ve son tarihleri belirleme
    first_date = selected_group_data.index[0].strftime("%d.%m.%Y")  # İlk tarihi formatlama
    last_date = selected_group_data.index[-1].strftime("%d.%m.%Y")  # Son tarihi formatlama

        # Değişim yüzdesini hesaplama
    first_value = selected_group_data.iloc[0,0]  # İlk değer
    last_value = selected_group_data.iloc[-1,0] # Son değer
    change_percent = ((last_value - first_value) / first_value) * 100  # Yüzde değişim

        # Yüzdeyi iki ondalık basamak ile sınırlama
    change_percent = round(change_percent, 4)

    st.markdown(f"<h2 style='text-align:left; color:black;'>{selected_group} Fiyat Endeksi</h2>", unsafe_allow_html=True)


        # Grafiği çizme
    figgalt = go.Figure()
    figgalt.add_trace(go.Scatter(
            x=selected_group_data.index,
            y=selected_group_data.iloc[:,0].values,
            mode='lines+markers',
            name=selected_group,
            line=dict(color='blue', width=4),
            marker=dict(size=8, color="black")
        ))

        # X ekseninde özelleştirilmiş tarih etiketlerini ayarlıyoruz
    figgalt.update_layout(
            xaxis=dict(
                tickvals=selected_group_data.index,  # Original datetime index
                ticktext=selected_group_data.index.strftime("%d.%m.%Y"),  # Custom formatted labels
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            yaxis=dict(
                tickfont=dict(size=14, family="Arial Black", color="black")
            ),
            font=dict(family="Arial", size=14, color="black")
        )


    st.markdown(f"""
        <h3 style='text-align:left; color:black;'>
            {first_date} - {last_date} Değişimi: <span style='color:red;'>%{change_percent}</span>
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
        excel_data1 = to_excel(endeksler)
  


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
        
        if fiyat.dropna().empty:
            pass
        else:
            st.dataframe(endeksler.drop("Madde",axis=1))
    else:
        st.markdown(f"<h2 style='text-align:left; color:black;'>Fiyat Listesi</h2>", unsafe_allow_html=True)
        st.dataframe(fiyat)

    

    






    


