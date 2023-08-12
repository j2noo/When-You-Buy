import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  # 외부
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import time

import asyncio  # 외부
import logging  # 미사용?

# 국제선 상위 10개 노선 * 2 -> 20개노선 -> 18개
route_international = [
    ["ICN", "NRT"],
    ["NRT", "ICN"],
    ["ICN", "KIX"],
    ["KIX", "ICN"],
    ["ICN", "FUK"],
    ["FUK", "ICN"],
    ["ICN", "BKK"],
    ["BKK", "ICN"],
    ["ICN", "HKG"],
    ["HKG", "ICN"],
    ["ICN", "DAD"],
    ["DAD", "ICN"],
    ["ICN", "HAN"],
    ["HAN", "ICN"],
    ["ICN", "SGN"],
    ["SGN", "ICN"],
    ["GMP", "KIX"],
    ["KIX", "GMP"],
]
route_international2 = [
    ["ICN", "NRT"],
    ["ICN", "KIX"],
    ["ICN", "FUK"],
    ["ICN", "BKK"],
    ["ICN", "HKG"],
    ["ICN", "DAD"],
    ["ICN", "HAN"],
    ["ICN", "SGN"],
    ["ICN", "TPE"],
    ["ICN", "SIN"],
    ["ICN", "MNL"],
    ["ICN", "LAX"],
    ["GMP", "HND"],
    ["GMP", "KIX"],
    ["PUS", "FUK"],
    ["PUS", "KIX"],
    ["PUS", "NRT"],
    ["PUS", "DAD"],
    ["PUS", "BKK"],
    ["PUS", "TPE"],
]


async def parsing_async(airway_ID, date, crawledHtml_li):
    # 로딩이 끝나면 생기는 비동기 elem : div.flights List domestic_DomesticFlight__3wvCd
    # 요소의 className -> CSS선택자로 추출
    # 전체 : div.indivisual_IndivisualItem__3co62 result
    # 항공사 : b.name -> CSS
    # 출발시간/도착시간 : route_time__-2Z1T[2]
    # 소요시간 : route_info__1RhUH 의 2번째 텍스트
    # 카드 혜택 : item_type__2KJOZ
    # 가격 : item_num__3R0Vz
    parsed_li = []
    for elem in crawledHtml_li:
        try:
            airline = elem.find("b", class_="name").get_text()
            route_times = elem.find_all("b", class_="route_time__-2Z1T")
            time_departure = route_times[0].get_text()
            time_arrive = route_times[1].get_text()
            time_taken = elem.find("i", class_="route_info__1RhUH").get_text()
            card_benefit = elem.find("span", class_="item_type__2KJOZ").get_text()
            price = elem.find("i", class_="item_num__3R0Vz").get_text()
            """
            datas_li.append(
                [
                    "Flight Ticket ID",  # idx 후처리
                    "Searching Date",  # 조사날짜 후처 리 
                    "Departure Date",
                    "Airway ID",
                    "Depature Time",
                    "Arrive Time",
                    "Flight Time",
                    "Airline",
                    "Price",
                    "Card Benefit",
                ]
            )
            """
            li = [
                1,
                1,
                date[0:4] + "-" + date[4:6] + "-" + date[6:8],
                airway_ID,
                time_departure,
                time_arrive,
                time_taken[4:6] + ":" + time_taken[9:11],  # 소요시간 슬라이싱
                airline,
                int(price.replace(",", "")),
                card_benefit[3:],
            ]
            parsed_li.append(li)

        # 요소에 데이터가 없는경우 패스
        except:
            pass
    return parsed_li


async def crawl_async(airway_ID, date):
    global idx
    global currBrowser
    global countingURL
    global browserList

    departure = route_international[airway_ID][0]
    arrive = route_international[airway_ID][1]

    countingURL += 1
    url = (
        "https://m-flight.naver.com/flights/international/"
        + departure
        + "-"
        + arrive
        + "-"
        + date
        + "?adult=1&isDirect=true&fareType=Y"
    )
    # WebDriver에 Get요청 실패시 예외처리
    try:
        currBrowser.get(url)
    except:
        print("[ERROR] getUrl failed at ", departure, arrive, date)
        raise Exception("browser.get(url) Failed")
    # WebDriver를 이용한 비동기 html 로딩

    try:
        # 15초 이내 비동기 로딩 실패시 예외처리
        element = WebDriverWait(currBrowser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "flights.List.international_InternationalContainer__2sPtn")
            )
        )
    except:
        # webDriver 멈춤으로 인한 timeout
        idx = (idx + 1) % 4
        currBrowser = browserList[idx]
        print("[ERROR] 20s timeout at ", departure, arrive, date)
        print("[SYS] switching chrome browser to idx : ", idx)
        time.sleep(60)

        return list([])  # 재검색

    # bs4를 이용한 parsing

    soup = BeautifulSoup(currBrowser.page_source, "html.parser")
    crawledHtml_li = soup.find_all("div", class_="indivisual_IndivisualItem__3co62 result")
    parsing_li = await parsing_async(airway_ID, date, crawledHtml_li)  # bs4

    return parsing_li


async def main_async():
    global countingURL
    global datas_li
    global startTime

    global idx
    global currBrowser
    global countingURL
    global browserList

    countingURL = 0
    datas_li = []

    for airway_ID in range(len(route_international)):
        routeTotalFlights = 0
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser0 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
        browser1 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
        browser2 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
        browser3 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
        time.sleep(3)  # 브라우저 열고 잠깐 기다림
        browserList = [browser0, browser1, browser2, browser3]
        idx = 0
        currBrowser = browserList[idx]

        for days in range(3, 183):  # 3일뒤 항공편부터 존재(해외) 6개월까지
            # 90번마다 브라우저 리셋
            if days == 90:
                print("WebDriver Reload..")
                browser0.quit()
                browser1.quit()
                browser2.quit()
                browser3.quit()
                time.sleep(3)

                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                browser0 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
                browser1 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
                browser2 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
                browser3 = webdriver.Chrome("chromedriver.exe", options=options)  # 브라우저 실행
                time.sleep(3)  # 브라우저 열고 잠깐 기다림
                browserList = [browser0, browser1, browser2, browser3]
                idx = 0
                currBrowser = browserList[idx]

            departure = route_international[airway_ID][0]
            arrive = route_international[airway_ID][1]
            searchedDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
            before_crawl_async = datetime.today() + timedelta(hours=9)
            parsed_li = await crawl_async(airway_ID, searchedDate)
            after_crawl_async = datetime.today() + timedelta(hours=9)
            crawl_time = after_crawl_async - before_crawl_async
            print(
                f"{airway_ID}-{days}. {departure} to {arrive} at {searchedDate} have {len(parsed_li)} flights. Running Time : {crawl_time}(ms)"
            )

            routeTotalFlights += len(parsed_li)

            datas_li += parsed_li
        print(f">> {departure} to {arrive} flights : {routeTotalFlights}  --TOTAL FLIGHTS : {len(datas_li)}")
        print("----------------changing route----------------------\n")

        # 브라우저 리셋 - 끄기
        browser0.quit()
        browser1.quit()
        browser2.quit()
        browser3.quit()

    # Flight Ticket ID, searchingDate 후처리
    for i in range(len(datas_li)):
        datas_li[i][0] = i
        datas_li[i][1] = startTime.strftime("%Y-%m-%d")


# main------------------------------------------------------------------------

global startTime
global idx
global currBrowser
global countingURL

# Running Time Check
startTime = datetime.today() + timedelta(hours=9)

todayFileNameFormatting = startTime.strftime("%Y%m%d_%H%M%S")
print("today : ", todayFileNameFormatting)
print("20초 후 크롬드라이버 실행. 세션을 종료하세요")
time.sleep(20)

loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())  # 비동기
loop.close

# Running Time Check
endTime = datetime.today() + timedelta(hours=9)

print(f"[Start Time] {startTime}\n")
print(f"[End Time] {endTime}\n")
print(f"[Running Time] : { endTime - startTime} (ms)\n")
print(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")

# csv 출력
fd = open(f"crawledFiles/{todayFileNameFormatting}.csv", "w", encoding="utf-8", newline="")
csvWriter = csv.writer(fd)
for li in datas_li:
    csvWriter.writerow(li)
fd.close()
print("[INFO]   ", todayFileNameFormatting, ".csv generated")


# log 출력
log_fd = open("crawledFiles/timelog.txt", "a", newline="")
log_fd.write(f"[Start Time] {startTime}\n")
log_fd.write(f"[End Time] {endTime}\n")
log_fd.write(f"[Running Time] : { endTime - startTime} (ms)\n")
log_fd.write(f"[File Length] {countingURL} url, {len(datas_li)} rows \n\n")
log_fd.close()

print("[LOGGED] timelog.txt generated")


# 기존 csv에 추가

fd2 = open("crawledFiles/flights.csv", "r", encoding="UTF-8")  # 마지막인덱스찾기
csvReader = csv.reader(fd2)
lastIdx = 1
for i in csvReader:
    lastIdx = i[0]
lastIdx = int(lastIdx)
print("lastidx : ", lastIdx)
fd2.close()
for i in range(len(datas_li)):
    datas_li[i][0] = i + lastIdx + 1

fd3 = open("crawledFiles/flights.csv", "a", encoding="utf-8", newline="")
csvWriter = csv.writer(fd3)
for li in datas_li:
    csvWriter.writerow(li)
fd3.close()
print("[UPDATE] flights.csv updated")
