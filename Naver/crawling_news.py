import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

class Crawler:
    def __init__(self,maxpage,query,sort,s_date,e_date): 
        self.maxpage = maxpage
        self.query = query
        self.sort = sort
        self.s_date = s_date
        self.e_date = e_date

        self.title_text=[]
        self.link_text=[]
        self.source_text=[]
        self.contents_text=[]
        self.result={}
        self.df=self.crawling()

    def contents_cleansing(self, contents):
        first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',str(contents)).strip()  #앞에 필요없는 부분 제거
        second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
        third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
        self.contents_text.append(third_cleansing_contents)

    def crawling(self):
        s_from = self.s_date.replace(".","")
        e_to = self.e_date.replace(".","")
        page = 1
        maxpage_t =(int(maxpage)-1)*10+1 
        while page <= maxpage_t:
            # (관련도순=0  최신순=1  오래된순=2)
            url = "https://search.naver.com/search.naver?where=news&query=" + self.query + "&sort="+self.sort+"&ds=" + self.s_date + "&de=" + self.e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            atags = soup.find_all('a', 'news_tit')
            for atag in atags:
                title = atag.get('title')
                self.title_text.append(title)     #제목
                self.link_text.append(atag['href'])   #링크주소

            source_lists = soup.find_all('a', 'info press')
            for source_list in source_lists:
                self.source_text.append(source_list.text)    #신문사

            contents_lists = soup.find_all('a','api_txt_lines dsc_txt_wrap')
            for contents_list in contents_lists:
                self.contents_cleansing(contents_list) #본문요약 정제화

            page += 10
            if int((page-1)/10) % 10 == 0: #10페이지마다 시간차 있어서 일단 이렇게 함
                print(f"page {int((page-1)/10)} crawled") #페이지 수 출력  

        self.result= {"title": self.title_text ,  "source" : self.source_text ,"contents": self.contents_text ,"link":self.link_text}
        try :
            df = pd.DataFrame(self.result)
            print("crawling complete")        
            self.crawled = 1
            df = df[~df.duplicated()].reset_index(drop=True)
            return df
        except :
            print(len(self.result['title']),len(self.result['source']),len(self.result['contents']),len(self.result['link'])) #제목, 신문사, 본문요약, 링크
            print("only save 'title' & 'contents'") #링크는 제거하지 않았으나, 신문사는 제거하여 저장
            df = pd.DataFrame() #빈 df 생성
            df['title'] = self.result['title'] #제목 저장
            df['contents'] = self.result['contents'] #본문요약 저장
            df = df[~df.duplicated()].reset_index(drop=True) #중복제거
            return df

    def save_df(self,path):
        self.df.to_excel(path, sheet_name='naver_news' , index=False)
        print("save complete")


def input_(input_text):
    while True:
        try : 
            inputs = input(input_text)
            return inputs
        except :
            print("잘못입력하셨습니다.")


if __name__=="__main__":
        query = input_("검색할 키워드 (예: 경기도 자전거)\n입력 : ")
        maxpage = input_("가져올 최대페이지\n입력 : ")
        sort = input_("가져올 순서 (관련도순=0  최신순=1  오래된순=2)\n입력 : ")
        s_date = input_("검색기간 시작일자 (입력양식:2022.01.14)\n입력 : ")
        e_date = input_("검색기간 종료일자 (입력양식:2022.04.14)\n입력 : ")
        path = input_("저장할 파일이름\n입력 : ") + ".xlsx"
        crawled = Crawler(maxpage,query,sort,s_date,e_date)
        crawled.save_df(path)