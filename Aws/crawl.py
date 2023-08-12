import selenium  # selenium 라이브러리
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # XPath 클릭용
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By  # 비동기 크롤링
from selenium.webdriver.support.ui import WebDriverWait  # 비동기 크롤링
from selenium.webdriver.support import expected_conditions as EC  # 비동기 크롤링

import time
from datetime import datetime, timedelta  # 크롤링 시간 측정


chrome_options = Options()  # 웹드라이버 옵션 설정
chrome_options.add_experimental_option("detach", True)  # 꺼지지 않음


driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)


test_urls = [
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231001?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231002?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231003?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231004?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231005?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231006?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231007?adult=1&isDirect=true&fareType=Y",
    "https://m-flight.naver.com/flights/international/ICN-DAD-20231008?adult=1&isDirect=true&fareType=Y",
]

for url in test_urls:
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
