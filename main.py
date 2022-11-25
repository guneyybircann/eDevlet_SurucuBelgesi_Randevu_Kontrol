from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from info import *
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

while 1:

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()

    wait = WebDriverWait(driver, 10)
    driver.get("https://giris.turkiye.gov.tr/Giris/gir")
    driver.implicitly_wait(30)
    for _ in ["tridField","egpField","submitButton"]:
        wait.until(EC.element_to_be_clickable((By.NAME, _)))
    for _, infos in zip(["tridField","egpField"], [kimlik,sifre]):
        driver.find_element(By.NAME, _).send_keys(infos)
    driver.find_element(By.NAME, "submitButton").click()

    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mfp-close")))
        driver.find_element(By.CLASS_NAME, "mfp-close").click()
    except:
        pass

    driver.get("https://www.turkiye.gov.tr/nvi-surucu-belgesi-basvuru-randevusu")
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "new")))
    driver.find_element(By.CLASS_NAME, "new").click()

    wait.until(EC.element_to_be_clickable((By.ID, "onay")))
    onay = driver.find_element(By.ID, "onay")
    driver.execute_script("arguments[0].click();", onay)

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submitButton")))
    closeButton = driver.find_element(By.CLASS_NAME, "submitButton")

    driver.execute_script("arguments[0].click();", closeButton)

    status = list()
    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "il")))
        driver.find_element(By.NAME, "il").click()

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[value="34"]'))) # istanbul plaka kodu
        driver.find_element(By.CSS_SELECTOR, '[value="34"]').click()

        wait.until(EC.element_to_be_clickable((By.NAME, "ilce")))
        driver.find_element(By.NAME, "ilce").click()
        i = 2
        try:
            for _ in range(100):
                bilgi = '//*[@id="ilce"]/option[' + str(i) + "]"
                status.append(driver.find_element(By.XPATH, bilgi).text)
                i += 1
        except:
            pass
    except:
        pass
    try:
        if status:
            NewStatus = "\n".join(status)
            mail = SMTP("smtp.gmail.com",587)
            mail.ehlo()
            mail.starttls()
            mail.login(mailUser,mailPass)
            mesaj = MIMEMultipart()
            mesaj["From"] = mailUser
            mesaj["To"] = "gonderilecek mail adresi"
            mesaj["Subject"] = "Ehliyet Randevu Bilgileri"
            body = NewStatus
            body_text = MIMEText(body, "plain")
            mesaj.attach(body_text)
            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            mail.close()
    except:
        pass
    driver.close()
    sleep(600)
