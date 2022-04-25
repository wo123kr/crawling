import pandas as pd
import datetime
import time
from tqdm.auto import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

 # 파일명 설정
filename = datetime.datetime.now().strftime("%Y-%m-%d")

# 크롤링 전 세팅
chrome_driver_path = r'chromedriver.exe'

# 크롤링 URL
# 향후 찾고 싶은 영상 URL만 변경
url_path = input('抖音 영상 링크를 붙여넣어주세요 : ' )

# 크롤링 반복 횟수
repeat = int(input('스크롤 횟수를 입력해주세요.:' ))

# 댓글 작성자
commenter_lst = []
# 댓글
comment_lst=[]
# 좋아요 개수
like_count_lst = []
# 날짜 리스트
date_count_lst = []

with Chrome(executable_path = chrome_driver_path) as driver:
    # 찾으려는 대상이 불러올 때까지 지정된 시간만큼 대기하도록 설정한다.
    # 인자는 초(second) 단위이며, Default 값은 0초이다. 
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) # 영상 url
    time.sleep(3)
    
    print("QR코드를 스캔하세요")
    input("로그인 작업 등 모든 걸 완료 후 아무키나 입력하세요.")
    print("크롤링 시작 !!!")
    
    # 영상 멈춤
    # if driver.find_element_by_class_name("xgplayer-start hide").get_attribute('data-state') == 'pause':  
    #         driver.find_element_by_class_name("xgplayer-start hide").click()
    # else:
    #     pass
    
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
        for commenter in tqdm(wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'nEg6zlpW')))): # 댓글 작성자
            # 작성자 이름 없는 경우에, 공백 표시
            # 확인된 사용자, 공식 아티스트 채널의 경우, innertext를 가져옴
            if commenter.text != '':
                commenter_lst.append(commenter.text)
            else:
                commenter_temp = commenter.get_attribute("innerText").strip().replace('\n', '')  # 작성자 이름 없는 경우, innerText를 가져옴
                commenter_lst.append(commenter_temp)                
    except:
        # 크롤링 값이 없을 경우에
        commenter_lst.append('')

    # 댓글 가져오기    
    try:
        # for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.VD5Aa1A1')))): # 댓글
        for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'VD5Aa1A1')))): # 댓글
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
        for like_count in tqdm(wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'eJuDTubq')))): # 좋아요 개수
            if like_count.text != '':
                like_count_lst.append(like_count.text)
            else:
                like_count_lst.append('0')
    except:
        # 좋아요 개수가 없을 경우에
        like_count_lst.append('0') 
    
    try:
        for date_count in tqdm(wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dn67MYhq')))): # 날짜
            if date_count.text != '':
                date_count_lst.append(date_count.text)
            else:
                date_count_lst.append('0')
    except:
        # 날짜 없을 경우에
        date_count_lst.append('0')
        
print('done')

# 저장 위치
save_path = r'' # 저장 경로

df = pd.DataFrame({'댓글 작성자' : commenter_lst,
                   '댓글' : comment_lst,
                   '좋아요 개수' : like_count_lst,
                   '날짜' : date_count_lst
                   })

# 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
df.to_csv(save_path + filename + ' 도우인 댓글 크롤링 .csv' , encoding='utf-8-sig')

print('save done')