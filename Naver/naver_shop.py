# BeautifulSoup은 HTML 과 XML 파일로부터 데이터를 수집하는 라이브러리
# pip install bs4
# pip install requests
# pip install fake-useragent
# pip install xlsxwriter 
 
import requests
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
# 엑셀 처리 임포트
import xlsxwriter
 
# Excel 처리 선언
savePath = ""
# workbook = xlsxwriter.Workbook(savePath + 'shopItemList.xlsx')
workbook = xlsxwriter.Workbook('shopItemList.xlsx')
 
# 워크 시트
worksheet = workbook.add_worksheet()
 
# 파싱할 대상 Web URL
url = "https://search.shopping.naver.com/best100v2/detail.nhn?catId=50004603"
# 크롬브라우저가 실행하는 것처럼 속이기
headers = { 'User-Agent': UserAgent().chrome }
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.content,'html.parser')
# print(soup)
 
# 엑셀 행 수
excel_row = 1
 
worksheet.set_column('A:A', 40) # A 열의 너비를 40으로 설정
worksheet.set_row(0,18) # A열의 높이를 18로 설정
worksheet.set_column('B:B', 12) # B 열의 너비를 12로 설정
worksheet.set_column('C:C', 12) # C 열의 너비를 12로 설정
worksheet.set_column('D:D', 60) # D 열의 너비를 60으로 설정
 
worksheet.write(0, 0, '제품명')
worksheet.write(0, 1, '가격')
worksheet.write(0, 2, '리뷰수')
worksheet.write(0, 3, '링크')
 
# 스크래핑하고자 하는 전체 데이터를 선택
# items = soup.find_all("li", attrs={"class":re.compile("^^_itemSection")})
items = soup.select('#productListArea > ul > li')
# print(items)
 
shopItemList = [] # 리스트 생성
for item in items:
    # name = item.find('a')['title']#제품명
    name = item.select_one('#productListArea > ul > li > div.thumb_area > a').get('title')
    # price = item.find('span', attrs = {'class':'num'}).get_text() + '원' #가격 
    price = item.select_one('#productListArea > ul > li > div.price > strong > span.num').text + '원'
    # link = item.find('div', attrs={'class':'thumb_area'}).find('a')['href'] #링크 
    link = item.select_one('#productListArea > ul > li > div.thumb_area > a').get('href')
    # review_count = item.find('span',attrs = {'class':'mall'}).find('em').text #리뷰수
    review_count = item.select_one('#productListArea > ul > li > div.info > span > a.txt > em').text
    # print(review_count)
    review_count = review_count[1:-1]
    
    # 엑셀 저장(텍스트)
    worksheet.write(excel_row, 0, name)
    worksheet.write(excel_row, 1, price)
    worksheet.write(excel_row, 2, review_count)
    worksheet.write(excel_row, 3, link)
 
    # 엑셀 행 증가
    excel_row += 1
 
# 엑셀 파일 닫기
workbook.close() # 저장