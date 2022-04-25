from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

print("기다리세요....")

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)

url = "https://newrank.cn/user/login"
driver.get(url)
time.sleep(2)

print("QR코드를 스캔하세요")
input("로그인 완료 후 아무키나 입력하세요.")
print("크롤링 시작")

product_name = []
product_shuju = []

uid_list = pd.read_csv("uid_list.csv", encoding='utf-8')

for i in uid_list:    
    url = "https://xz.newrank.cn/data/d/up/trend/"+ str(uid_list)
    
    print(url)
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    html_product = soup.select('#scrollLayoutContent > div._AjX-qVtw > div > div._59qEUgVZ > div > div._sNU19GTF > div._gNo7MBpn > div:nth-child(2) > div:nth-child(1) > div > p._JvKVi0S1')
    html_shuju = soup.select('#scrollLayoutContent > div._AjX-qVtw > div > div._59qEUgVZ > div > div._sNU19GTF > div._gNo7MBpn > div:nth-child(2) > div:nth-child(1) > div > p._640ErTRQx')
    
    # 텍스트만 추출
    for i in html_product:
        product_name.append(i.get_text())
    
    for i in html_shuju:
        product_shuju.append(i.get_text())

list_sum = list(zip(product_name, product_shuju))

col = ['平均播放数','平均获赞数','平均收藏数','平均分享数','平均评论数','平均弹幕数','互动率','赞粉比','植入视频','定制视频','直发动态','转发动态']

df = pd.DataFrame(list_sum, columns=col)

df.to_excel('新bang.xlsx')

