import pandas as pd
import datetime
import time
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options = webdriver.ChromeOptions()

# # headless 옵션 설정
# options.add_argument('headless') 
# options.add_argument("no-sandbox") 

# # 브라우저 윈도우 사이즈
# options.add_argument('window-size=1920x1080')

# # 사람처럼 보이게 하는 옵션들
# options.add_argument("disable-gpu")   # 가속 사용 x
# options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
# options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

# 오늘 날짜 파일명 생성
filename = datetime.datetime.now().strftime("%Y-%m-%d") 

chrome_driver_path = r'chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_driver_path)

url = 'https://www.tiktok.com/'
driver.get(url)
time.sleep(2)

driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/button').click()

print('로그인 완료 후 링크를 입력해주세요. ')

# 크롤링 URL
# 향후 찾고 싶은 영상 URL만 변경
url_path = input('영상 링크를 넣어주세요 : ' )

print("크롤링 시작")

# 크롤링 반복 횟수
repeat = int(input('스크롤 횟수를 입력해주세요. :' ))

# 댓글 작성자
commenter_lst = []
# 댓글
comment_lst=[]
# 좋아요 개수
like_count_lst = []


with Chrome as driver:
    # 찾으려는 대상이 불러올 때까지 지정된 시간만큼 대기하도록 설정한다.
    # 인자는 초(second) 단위이며, Default 값은 0초이다. 
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) # 영상 url
    time.sleep(3)
    
    # 최초 1회 PAGE_DOWN
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)
    time.sleep(3)

    # END 반복 실행
    # 실행 횟수 체크
    for item in tqdm(range(repeat)): # END버튼 반복 횟수, 1회당 20개씩 댓글 업데이트 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(1) # END버튼 클릭 이후, 1초 대기 후, 다시 END 버튼 진행
                
    # 크롤링 데이터 수집 진행

    # 작성자 가져오기
    # 댓글 작성자 중 확인된 사용자, 공식 아티스트 채널 값은 text로 가져올 시, (공백) 처리됨
    try:
        for commenter in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'comment-username-1')))): #comment-username-1
            # 작성자 이름 없는 경우에, 공백 표시
            # 확인된 사용자, 공식 아티스트 채널의 경우, innertext를 가져옴
            if commenter.text != '':
                commenter_lst.append(commenter.text)
            else:
                commenter_temp = commenter.get_attribute("innerText").strip().replace('\n', '') 
                commenter_lst.append(commenter_temp)                
    except:
        # 크롤링 값이 없을 경우에
        commenter_lst.append('')

    # 댓글 가져오기    
    try:
        for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'comment-level-1')))): #comment-level-1
            if comment.text != '':
                comment_temp = comment.text.replace('\n', ' ')
                comment_lst.append(comment_temp)
            else:
                comment_lst.append(' ')            
    except:
        # 크롤링 값이 없을 경우에
        comment_lst.append('')
                
    # 좋아요 개수 가져오기
    try:
        for like_count in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'comment-like-count')))): #comment-like-count'
            if like_count.text != '':
                like_count_lst.append(like_count.text)
            else:
                like_count_lst.append('0')
    except:
        # 좋아요 개수가 없을 경우에
        like_count_lst.append('0') 
        
print('done')

# 저장 위치
save_path = r'' # 저장 경로

df = pd.DataFrame({'댓글 작성자' : commenter_lst,
                   '댓글' : comment_lst,
                   '좋아요 개수' : like_count_lst,
                   })

# 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
df.to_csv(save_path + filename + ' 틱톡 댓글 크롤링 .csv' , encoding='utf-8-sig')

print('save done')