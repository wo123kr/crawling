from matplotlib import image
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

class Crawler:
    def __init__(self,maxpage,query,sort): 
        self.maxpage = maxpage
        self.query = query
        self.sort = sort

        self.title_text=[]
        self.link_text=[]
        self.source_text=[]
        self.item_text=[]
        self.location_text=[]
        self.price_text=[]
        self.deal_text=[]
        self.result={}
        self.df=self.crawling()

    def crawling(self):
        page = 1
        maxpage_t =(int(maxpage)-1)*44
        while page <= maxpage_t:
            #default(综合), sale-desc(销量从高到低), credit-desc(信用从高到低), price-asc(价格从低到高), price-desc(价格从高到低)
            url = "https://s.1688.com/selloffer/offer_search.htm?keywords="+ +"&spm=a26352.13672862.searchbox.input"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            atags = soup.find_all('div', 'row row-2 title') #제목
            for atag in atags:
                title = atag.get_text()
                self.title_text.append(title)     #제목
                self.link_text.append(atag['href'])   #링크주소

            source_lists = soup.find_all('a', 'dsrs') #출처
            for source_list in source_lists:
                self.source_text.append(source_list.text)
                
            item_images = soup.find_all('div', 'row row-1 content') #상품이미지
            for item_image in item_images:
                self.item_text.append(item_image['href']) #링크주소
                
            locations = soup.find_all('div', 'location') #위치
            for location in locations:
                location = location.get_text()
                self.location_text.append(location) 
            
            prices = soup.find_all('div', 'price g_price g_price-highlight') #가격
            for price in prices:
                price = price.get_text()
                self.price_text.append(price)
                
            deals = soup.find_all('div', 'deal-cnt') #거래수
            for deal in deals:
                deal = deal.get_text()
                self.deal_text.append(deal)

            page += 10
            if int((page-1)/10) % 10 == 0: #10페이지마다 시간차 있어서 일단 이렇게 함
                print(f"page {int((page-1)/10)} crawled") #페이지 수 출력  
            
        self.result = {'title':self.title_text, 'link':self.link_text, 'source':self.source_text, 'item':self.item_text, 'location':self.location_text, 'price':self.price_text, 'deal':self.deal_text}
        try :
            df = pd.DataFrame(self.result)
            print("crawling complete")        
            self.crawled = 1
            df = df[~df.duplicated()].reset_index(drop=True)
            return df
        except :
            print(len(self.result['title']),len(self.result['link']),len(self.result['source']),len(self.result['item']),len(self.result['location']),len(self.result['price']),len(self.result['deal'])) #제목, 링크, 출처, 상품이미지, 위치, 가격, 거래수
            print("only save 'title' & 'source'") #제목, 출처만 저장
            df = pd.DataFrame() #빈 df 생성
            df['title'] = self.result['title'] #제목 저장
            df['source'] = self.result['source'] #본문요약 저장
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
        query = input_("검색할 키워드 (예: 动物用品)\n입력 : ")
        maxpage = input_("가져올 최대페이지\n입력 : ")
        sort = input_("default(综合), sale-desc(销量从高到低), credit-desc(信用从高到低), price-asc(价格从低到高), price-desc(价格从高到低)\n입력 : ")
        path = input_("저장할 파일이름\n입력 : ") + ".xlsx"
        crawled = Crawler(maxpage,query,sort)
        crawled.save_df(path)