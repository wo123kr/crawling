from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime

print("기다리세요....")

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)

url = "https://world.taobao.com/"
driver.get(url)
time.sleep(2)

serchbox = driver.find_element_by_class_name("rax-textinput")
serchbox.send_keys(input("검색어를 입력하세요 >>> "))
serchbox.send_keys(Keys.ENTER)

Qr = driver.find_element_by_class_name("icon-qrcode")
Qr.click()

print("QR코드를 스캔하세요")
input("로그인 완료 후 아무키나 입력하세요.")
print("크롤링 시작 !!!")

taobao = []

price = driver.find_elements_by_class_name("price")
title = driver.find_elements(By.CLASS_NAME,"row-2")
buyer = driver.find_elements_by_class_name("deal-cnt")
seller = driver.find_elements_by_class_name("row-3")
location = driver.find_elements_by_class_name("location")

for price, title, buyer, seller, location in zip(price, title, buyer, seller, location):
        taobao.append([price.text, title.text, buyer.text, seller.text, location.text])

filename = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")

pd.DataFrame(taobao,columns=["price", "title", "buyer", "seller", "location"]).to_excel(filename+".xlsx")
print("1페이지 크롤링 완료")

print(price.text) #확인용