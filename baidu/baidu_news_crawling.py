 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

#한글깨짐 방지
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#각 크롤링 결과 저장하기 위한 리스트 선언
title_text=[]
link_text=[]
source_text=[]
contents_text=[]
result={}

#엑셀로 저장하기 위한 변수
RESULT_PATH =''  #결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기

#내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    #print(contents_text)

#크롤링 시작
def crawler(maxpage,query,sort):
    page = 0
    maxpage_t = (int(maxpage)-1)*10 #페이지 수   
    while page <= maxpage_t:
        url = "https://www.baidu.com/s?ie=utf-8&medium=0&rtt=" + sort + "&bsst=1&rsv_dl=news_b_pn&cl=2&wd="+ query + "&tn=news&rsv_bp=1&tfflag=0&x_bfe_rqs=03E8000000000000000044&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn=" + str((page))
        response = requests.get(url)
        html = response.text

        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        #<a>태그에서 제목과 링크주소 (a 태그 중 class 명이  news-title-font_1xS-Fz 인 것)
        atags = soup.find_all('a', 'news-title-font_1xS-F')
        for atag in atags:
            title = atag.get('aria-label')
            title_text.append(title)     #제목
            link_text.append(atag['href'])   #링크주소
        
        #print(link_text)

        #신문사 추출 (a 태그 중 class 명이 source-link_Ft1ov인 것)
        source_lists = soup.find_all('a', 'source-link_Ft1ov')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사
        
        #print(source_text)

        #본문요약본 
        contents_lists = soup.find_all('span','c-font-normal c-color-text')
        for contents_list in contents_lists:
            contents_cleansing(contents_list) #본문요약 정제화
            
        #모든 리스트 딕셔너리형태로 저장
        result= {"title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }
        print(page)
        
        df = pd.DataFrame(result)  #df로 변환
        page += 10 #페이지 증가
        

    # 새로 만들 파일이름 지정
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(outputFileName,sheet_name='sheet1')

#메인함수
def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ") #최대 크롤링할 페이지 수 입력
    query = input("검색어 입력: ") #입력한 검색어
    sort = input("뉴스 검색 방식 입력(按焦点排序(제목순) = 1  按时间排序(날짜순) = 4 ): ")    # 1=제목순, 4=날짜순
    crawler(maxpage,query,sort)
    print("------------크롤링 완료-------------")

#메인함수 수행
main()