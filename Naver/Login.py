from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import requests

options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(executable_path="C:/workspace/adoba_work/Development_adoba/crawling/chromedriver.exe", options=options) #chromedriver 파일을 설치한 절대 경로를 다시 입력해 주어야 함.
browser.maximize_window()

# User Agent 구하기
url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent"
browser.get(url)
user_agent = browser.find_element_by_id("detected_value")
headers = {
    'User-Agent' : 'user_agent'
}
# 네이버 로그인 페이지 이동
url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"
browser.get(url)
# 아이디 와 비밀번호를 id와 pw구역에 붙여넣기
browser.find_element_by_name('id').click()
pyperclip.copy('아이디')
browser.find_element_by_name('id').send_keys(Keys.CONTROL, 'v')

browser.find_element_by_name('pw').click()
pyperclip.copy('비밀번호')
browser.find_element_by_name('pw').send_keys(Keys.CONTROL, 'v')

browser.find_element_by_id('log.login').click()
time.sleep(2)
# 세션 추가로 로그인 유지
s=requests.Session()
s.headers.update(headers)
# 로그인 쿠키정보 requests로 옮기기
browser.get_cookies()
for cookie in browser.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)
# url을 필요한 곳에서 가져온 후 데이터 긁어오기
# url = '' 
# ex) url = 'https://mail.naver.com/'
browser.get(url)
# 이 밑으로는 html을 읽어서 필요한 데이터를 사용하세요


# browser.quit()