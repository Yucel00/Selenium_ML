from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
chromedriver_autoinstaller.install()
driver=webdriver.Chrome()
driver.get("https://www.hepsiemlak.com/")
time.sleep(2)


input_box=driver.find_element(By.XPATH,'//*[@id="search-input"]')
input_box.send_keys("güngören")
button1=driver.find_element(By.XPATH,'//*[@id="__layout"]/div/section[1]/div[1]/div/div/div/div[2]/div/div/div[1]/div[2]/button[1]')
button1.click()

time.sleep(2)

step=0
ilan_listesi=[]
while step<10:

    ilanlar=followers = driver.find_elements(By.CLASS_NAME, 'listing-item')
    for i in ilanlar:
        price=driver.find_element(By.CLASS_NAME, 'list-view-price')
        room=driver.find_element(By.CLASS_NAME, 'houseRoomCount')
        square_meter=driver.find_element(By.CLASS_NAME, 'squareMeter ')
        age=driver.find_element(By.CLASS_NAME, 'buildingAge')
        floor=driver.find_element(By.CLASS_NAME, 'floortype')
        ilan_bilgisi = {
                "Fiyat": price.text,
                "Oda Sayısı": room.text,
                "Metrekare": square_meter.text,
                "Bina Yaşı": age.text,
                "Bulunduğu Kat": floor.text
            }
        ilan_listesi.append(ilan_bilgisi)
       
    step+=1
    next=driver.find_element(By.XPATH,'//*[@id="listPage"]/div[1]/div/div/main/div[2]/div/section/div/a[2]')
    next.click()
    time.sleep(2)

csv_file = "ilan_bilgileri.csv"

# Dosya oluştur ve yazma işlemi başlat
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Sütun başlıklarını (sözlük anahtarlarını) al
    fieldnames = ilan_listesi[0].keys()
    
    # CSV yazıcısı oluştur
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Başlık satırını dosyaya yaz
    writer.writeheader()
    
    # Liste içindeki her sözlüğü dosyaya yaz
    writer.writerows(ilan_listesi)