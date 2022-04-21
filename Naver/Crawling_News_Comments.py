# step1. 관련 패키지 및 모듈 불러오기
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup

# step2. 네이버 뉴스 댓글정보 수집 함수
def get_naver_news_comments(url, wait_time=5, delay_time=0.1):

    # 크롬 드라이버로 해당 url에 접속
    driver = webdriver.Chrome('./chromedriver')

    # (크롬)드라이버가 요소를 찾는데에 최대 wait_time 초까지 기다림 (함수 사용 시 설정 가능하며 기본값은 5초)
    driver.implicitly_wait(wait_time)

    # 인자로 입력받은 url 주소를 가져와서 접속
    driver.get('https://n.news.naver.com/article/comment/016/0001977261')

    # 더보기가 안뜰 때 까지 계속 클릭 (모든 댓글의 html을 얻기 위함)
    while True:

        # 예외처리 구문 - 더보기 광클하다가 없어서 에러 뜨면 while문을 나감(break)
        try:
            more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
            more.click()
            time.sleep(delay_time)

        except:
            break

    # 본격적인 크롤링 타임

    # selenium으로 페이지 전체의 html 문서 받기
    html = driver.page_source

    # 위에서 받은 html 문서를 bs4 패키지로 parsing
    soup = BeautifulSoup(html, 'lxml')

    # 1)작성자
    nicknames = soup.select('span.u_cbox_nick')
    list_nicknames = [nickname.text for nickname in nicknames]

    # 2)댓글 시간
    datetimes = soup.select('span.u_cbox_date')
    list_datetimes = [datetime.text for datetime in datetimes]

    # 3)댓글 내용
    contents = soup.select('span.u_cbox_contents') 
    list_contents = [content.text for content in contents]


    # 4)작성자, 댓글 시간, 내용을 셋트로 취합
    list_sum = list(zip(list_nicknames,list_datetimes,list_contents))

    # 드라이버 종료
    driver.quit()

    # 함수를 종료하며 list_sum을 결과물로 제출
    return list_sum

# step3. 실제 함수 실행 및 엑셀로 저장
if __name__ == '__main__': # 설명하자면 매우 길어져서 그냥 이렇게 사용하는 것을 권장

    # 원하는 기사 url 입력
    url = '댓글 크롤링 원하는 기사의 url (주의! 댓글보기를 클릭한 상태의 url이어야 함'

    # 함수 실행
    comments = get_naver_news_comments(url)

    # 엑셀의 첫줄에 들어갈 컬럼명
    col = ['작성자','시간','내용']

    # pandas 데이터 프레임 형태로 가공
    df = pd.DataFrame(comments, columns=col)

    # 데이터 프레임을 엑셀로 저장 (파일명은 'news.xlsx', 시트명은 '뉴스 기사 제목')
    df.to_excel('news.xlsx', sheet_name='뉴스 기사 제목')