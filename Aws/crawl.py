import selenium  # selenium 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # XPath 클릭용
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By  # 비동기 크롤링
from selenium.webdriver.support.ui import WebDriverWait  # 비동기 크롤링
from selenium.webdriver.support import expected_conditions as EC  # 비동기 크롤링

from bs4 import BeautifulSoup # 파싱라입러리

import time
from datetime import datetime, timedelta  # 크롤링 시간 측정


chrome_options = Options()  # 웹드라이버 옵션 설정
chrome_options.add_experimental_option("detach", True)  # 꺼지지 않음


driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)




for date in range(20231001, 20231005):  # 총 30일
    url = f"https://m-flight.naver.com/flights/international/ICN-DAD-{date}?adult=1&isDirect=true&fareType=Y"

    startTime = datetime.today()
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "flights.List.international_InternationalContainer__2sPtn")
            )
        )
        print("로딩완료", end="")
    except Exception as e:
        print("로딩 중 오류 발생:", e, end="")
    middleTime = datetime.today()
    print("소요시간 :", middleTime - startTime)

    try:
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "loadingProgress_loadingProgress__1LRJo"))
        )
        print("로딩 후 대기완료", end="")
    except Exception as e:
        print("로딩 후 대기 중 오류 발생:", e, end="")

    endTime = datetime.today()
    print("소요시간 :", endTime - middleTime)

    # 첫 번째 버튼 클릭
    first_button = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div[2]/button'
    ).click()
    time.sleep(0.1)
    # 두 번째 버튼 클릭
    second_button = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[1]/div/div[2]/div/button[2]'
    ).click()
    time.sleep(1)

    # selenium을 이용한 parsing ---------------------------------------------------------------------------------------
    before_se = datetime.today()
    crawledhtml = driver.find_elements(By.CSS_SELECTOR, "div.indivisual_IndivisualItem__3co62.result")
    after_se = datetime.today()
    print(f" crawl-selen : {after_se-before_se}(ms) cnt : {len(crawledhtml)} ")

    # bs4를 이용한 parsing=======================================================
    before_bs4 = datetime.today()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    crawledHtml_li = soup.find_all("div", class_="indivisual_IndivisualItem__3co62 result")
    after_bs4 = datetime.today()
    print(f"crawl-bs4..: {after_bs4-before_bs4}(ms) cnt : {len(crawledHtml_li)} ")

print("평균 소요 시간")
print(f"selenium :")