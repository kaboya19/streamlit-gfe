import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import time

# Abone listesi dosyası
SUBSCRIBERS_FILE = "subscribers.csv"

# SMTP ayarları
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "borakaya8@gmail.com"  # Kendi Gmail adresiniz
SENDER_PASSWORD = "dqpp vgar wujr vhei"  # Gmail Uygulama Şifreniz (normal şifrenizi değil, uygulama şifrenizi kullanın)

def send_email_with_images(to_email, subject, body, images):
    # E-posta içeriği
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    # HTML içerik (Dinamik olarak değişkenleri kullanıyoruz)
    html_body = f"""
    <html>
    <body>
        <h1 style="color: red; font-weight: bold;">Web Gıda Fiyat Endeksi Ekim’de %1,79 arttı</h1>
        <p>11 Ekim’de ölçüme başladığımız W-GFE 11-31 Ekim döneminde %1,79 artış kaydetti.
        (Bu ay veri eksik olduğundan tahminen Ekim genelinde %2,5-3,0 dolayında artış yaşandığını tahmin ediyoruz)
        <p><img src="cid:image1"><br></p>
        Bu artışta taze sebze grubu öne çıktı. Sepette ağırlığı en yüksek gruplardan;</p>
        
        <ul>
            <li><strong>Ekmek:</strong> %2,2</li>
            <li><strong>Dana Eti:</strong> %1,96</li>
            <li><strong>Tavuk Eti:</strong> %0,82</li>
            <li><strong>Kuzu Eti:</strong> %1</li>
            <li><strong>Ayçiçek Yağı:</strong> %3,32 artış kaydetti.</li>
        </ul>
        
        <p>Fiyatı en çok artan ve azalan ürünlere bakıldığında:
        <strong>Maydanoz, Kırmızı Lahana, Dereotu</strong> artış olarak;
        <strong>Dolmalık Biber, Beyaz Lahana, Kabak, Limon ve Kivi</strong> ise en çok azalanlarda öne çıkmaktadır.</p>
        <p><img src="cid:image2"><br></p>
        
        <p>Ürün çeşidi özelinde fiyat değişimlerine baktığımızda en çok artış %120 ile Kepek Ekmeği ve %100 artış ile
        Mısır Gevreğinde görülmüştür. En çok fiyat düşüşü yaşanan ürün çeşidi ise Sardalya olmuştur.</p>
        <p><img src="cid:image3"><br></p>
        
        <p>Sepet eşit ağırlıklı alındığında fiyat değişimlerinin aritmetik ortalaması %2,27 ve medyan artış %0,75 olmuştur.
        SATRIM (Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %1,26 artmıştır.</p>
        <p><img src="cid:image4"><br></p>
        
        <p>Gıda Fiyat Endeksi ile ilgili tüm verisetlerine 
        <a href="https://web-gfe.streamlit.app">https://web-gfe.streamlit.app</a> sitesinden ulaşabilir ve indirebilirsiniz.</p>
        
        <p><small><i>Bu bültenin bir sonraki yayınlanma tarihi 1 Aralık 2024'tür.
        Burada yer alan bilgi ve analizler tamamen kişisel çalışma olup kesin bir doğruluk içermemekte ve
        yatırım tavsiyesi içermemektedir.</i></small></p>
        
        <p>Hazırlayan<br>Bora Kaya<br>HSBC Asset Management Intern</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Görselleri ekleme
    for img_id, img_path in images.items():
        with open(img_path, 'rb') as f:
            img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', f'<{img_id}>')  # Görsellerin HTML içinde kullanılacak ID'lerini ekliyoruz
            msg.attach(img)

    # SMTP sunucusuyla bağlantı kurma ve e-posta gönderme
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Güvenli bağlantı
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"E-posta başarıyla gönderildi: {to_email}")
        return True
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return False

# Abonelere toplu e-posta gönderme fonksiyonu
def send_bulk_email_with_images(subject, body, images):
    if os.path.exists(SUBSCRIBERS_FILE) and os.path.getsize(SUBSCRIBERS_FILE) > 0:
        df = pd.read_csv(SUBSCRIBERS_FILE)
        success_count = 0
        fail_count = 0
        for email in df["email"]:
            if send_email_with_images(email, subject, body, images):
                success_count += 1
                time.sleep(5)  # Gönderim arasına bekleme süresi eklenmesi
            else:
                fail_count += 1
        print(f"{success_count} e-posta başarıyla gönderildi, {fail_count} e-posta gönderilemedi.")
    else:
        print("Abone listesi bulunamadı.")

# Ana fonksiyon
if __name__ == "__main__":
    # E-posta konusu ve içeriği
    subject = "Ekim 2024 Gıda Fiyat Endeksi Bülteni"
    body = "Gıda Fiyat Endeksi Bülteni"
    today = datetime.today().strftime("%d-%m-%Y")

    images = {
        "image1": f"C:/Users/Bora/Documents/GitHub/streamlit-gfe/gfe_{today}.png",
        "image2": f"C:/Users/Bora/Documents/GitHub/streamlit-gfe/ürünler_{today}.png",
        "image3": f"C:/Users/Bora/Documents/GitHub/streamlit-gfe/çeşitler_{today}.png",
        "image4": f"C:/Users/Bora/Documents/GitHub/streamlit-gfe/egilim_{today}.png",
    }

    # Toplu e-posta gönder
    send_bulk_email_with_images(subject, body, images)
