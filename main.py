from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import time
import csv
import re  # Metin içinden sayıları ayıklamak için

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get("https://www.hepsiemlak.com/")
time.sleep(2)

# Arama işlemi
input_box = driver.find_element(By.XPATH, '//*[@id="search-input"]')
input_box.send_keys("güngören")
button1 = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section[1]/div[1]/div/div/div/div[2]/div/div/div[1]/div[2]/button[1]')
button1.click()

time.sleep(2)

step = 0
ilan_listesi = []

while step < 10:
    ilanlar = driver.find_elements(By.CLASS_NAME, 'listing-item')
    for ilan in ilanlar:
        try:
            # İlan bilgilerini çek
            price = ilan.find_element(By.CLASS_NAME, 'list-view-price').text
            rooms = ilan.find_element(By.CLASS_NAME, 'houseRoomCount').text
            square_meter = ilan.find_element(By.CLASS_NAME, 'squareMeter').text
            age = ilan.find_element(By.CLASS_NAME, 'buildingAge').text
            floor = ilan.find_element(By.CLASS_NAME, 'floortype').text

            # Verileri dönüştür
            price = int(re.sub(r'\D', '', price))
            room1=rooms.split("+")
            room=int(room1[0])
            living_room=int(room1[1])
            square_meter = int(re.sub(r'\D', '', square_meter))
            age = int(re.sub(r'\D', '', age))

            # Bilgileri sözlüğe ekle
            ilan_bilgisi = {
                "Fiyat (TL)": price,
                "Oda": room,
                "Salon": living_room, # Oda sayısı metin formatında bırakıldı
                "Metrekare (m²)": square_meter,
                "Bina Yaşı": age,
                "Bulunduğu Kat": floor  # Kat bilgisi metin formatında
            }

            ilan_listesi.append(ilan_bilgisi)
        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

    step += 1

    # Sonraki sayfaya geç
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="listPage"]/div[1]/div/div/main/div[2]/div/section/div/a[2]')
        next_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Sonraki sayfa bulunamadı: {e}")
        break

# Tarayıcıyı kapat
driver.quit()

# CSV'ye yaz
csv_file = "ilan_bilgileri.csv"

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ilan_listesi[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(ilan_listesi)

print(f"İlan bilgileri '{csv_file}' dosyasına başarıyla kaydedildi.")
