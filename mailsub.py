import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import time



# SMTP Ayarları
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "borakaya8@gmail.com"
SENDER_PASSWORD = "dqpp vgar wujr vhei"

# Abone listesi
SUBSCRIBERS_FILE = "subscribers.csv"

# E-Posta Gönderim Fonksiyonu
def send_email_with_images(to_email, subject, body, images):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Görselleri Ekle
    for img_id, img_path in images.items():
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_data = f.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', f'<{img_id}>')
                msg.attach(img)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"E-posta başarıyla gönderildi: {to_email}")
        return True
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")
        return False

# Toplu E-Posta Gönderimi
def send_bulk_email_with_images(subject, body, images):
    if os.path.exists(SUBSCRIBERS_FILE) and os.path.getsize(SUBSCRIBERS_FILE) > 0:
        df = pd.read_csv(SUBSCRIBERS_FILE)
        success_count = 0
        fail_count = 0
        for email in df["email"]:
            if send_email_with_images(email, subject, body, images):
                success_count += 1
                time.sleep(2)
            else:
                fail_count += 1
        print(f"{success_count} e-posta başarıyla gönderildi, {fail_count} e-posta gönderilemedi.")
    else:
        print("Abone listesi bulunamadı veya boş!")

# Ana E-Posta İçeriği ve Gönderimi
if __name__ == "__main__":
    subject = f"Web Gıda Fiyat Endeksi Aralık 2024 Bülteni"
    body = f"""
    <h2 style='color:black; font-weight:bold;'>Web Gıda Fiyat Endeksi Aralık 2024 Bülteni</h2>
    <h3 style='color:red; font-weight:bold;'>Web Gıda Fiyat Endeksi Aralık'ta %3,41 arttı</h3>
    <p><em>(Teknik notlara bültenin en aşağısından ulaşabilirsiniz)</em></p>
    <br>
    <img src="cid:image1" style="max-width:600px; margin: 10px 0;"/>
    <p>Web Gıda Fiyat Endeksi Aralık'ta %3,41 artış kaydederken mevsimsellikten arındırılmış artış %2,85 oldu.</p>
    <p>Sepette ağırlığı en yüksek ürünlere bakıldığında:</p>
    <ul>
        <li><strong>Domates</strong>: -%3,32 azalırken</li>
        <li><strong>Ayçiçek Yağı</strong>: %4,42</li>
        <li><strong>Kuzu Eti</strong>: %4,76</li>
        <li><strong>Ekmek</strong>: %3,67</li>
        <li><strong>Dana Eti</strong>: %3,43</li>
        <li><strong>Yumurta</strong>: %5,97</li>
        <li><strong>Tavuk Eti</strong>: %0,29 artış kaydetti.</li>
    </ul>
    <br>
    <img src="cid:image2" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image3" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image4" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image5" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image6" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image7" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image8" style="max-width:600px; margin: 10px 0;"/>
    <img src="cid:image9" style="max-width:600px; margin: 10px 0;"/>
    <br>
    <p>Mevsimsellikten arındırılmış olarak fiyat değişimlerinin ortalaması %2,72 ve medyan artış %2,80 olmuştur.</p>
    <p>Meyve ve Sebze hariç fiyat artışı %2,85 ile manşet ile aynı seviyededir.</p>
    <p>SATRIM(Mevsimsel Düzeltilmiş Budanmış Enflasyon) göstergesi ise %2,50 artmıştır.</p>
    <br>
    <img src="cid:image10" style="max-width:600px; margin: 10px 0;"/>
    <p><a href='https://web-gfe.streamlit.app'>Gıda Fiyat Endeksi ile ilgili tüm verilere buradan ulaşabilirsiniz.</a></p>
    <hr>
    <small>
        *Bu bültenin bir sonraki yayınlanma tarihi 24 Ocak 2025'tir. Burada yer alan bilgi ve analizler tamamen kişisel çalışma olup kesin bir doğruluk içermemekte ve yatırım tavsiyesi içermemektedir.*<br>
        *TÜİK’in hesaplamasıyla uyumlu olması açısından ayın ilk 24 günündeki veriler dikkate alınmıştır.*
    </small>
    <br>
    <p><strong>Hazırlayan:Bora Kaya</strong><br>
    <p>Twitter: <a href='https://x.com/mborathe'>https://x.com/mborathe</a></p>
    <p>Linkedin: <a href='https://www.linkedin.com/in/bora-kaya/'>https://www.linkedin.com/in/bora-kaya/</a></p>
   

    """

    # Görsellerin Yolları
    images = {
        "image1": "grafikler/gfe_24-12-2024.png",
        "image2": "grafikler/aylıkdegisim_24-12-2024.png",
        "image3": "grafikler/gruplar_24-12-2024.png",
        "image4": "grafikler/harcamasa24-12-2024.png",
        "image5": "grafikler/haric_24-12-2024.png",
        "image6": "grafikler/birim_24-12-2024.png",
        "image7": "grafikler/birimdüşen_24-12-2024.png",
        "image8": "grafikler/kümülatif_24-12-2024.png",
        "image9": "grafikler/egilim_24-12-2024.png"
    }

    # Toplu E-Posta Gönderimi
    send_bulk_email_with_images(subject, body, images)
