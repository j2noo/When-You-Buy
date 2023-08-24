import json  # json 파싱용
import time
from datetime import datetime, timedelta  # 크롤링 시간 측정
import requests  # http 통신
import concurrent.futures  # 멀티스레딩
import threading  # threading 모듈 import


routes = [
    ["ICN", "NRT"],
    ["NRT", "ICN"],
    ["ICN", "KIX"],
    ["KIX", "ICN"],
    ["ICN", "FUK"],
    ["FUK", "ICN"],
]
routes2 = [
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
startTime = datetime.today()


def getResponseJson(departureAirport, arrivalAirport, departureDate):
    response_start = datetime.today()
    url = "https://airline-api.naver.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://m-flight.naver.com/flights/international/{departureAirport}-{arrivalAirport}-{departureDate}?adult=1&isDirect=true&fareType=Y",
    }

    # GraphQL 요청 본문 데이터 정의
    first_payload = {
        "operationName": "getInternationalList",
        "variables": {
            "adult": 1,
            "child": 0,
            "infant": 0,
            "where": "pc",
            "isDirect": True,
            "galileoFlag": True,
            "travelBizFlag": True,
            "fareType": "Y",
            "itinerary": [
                {
                    "departureAirport": departureAirport,
                    "arrivalAirport": arrivalAirport,
                    "departureDate": departureDate,
                }
            ],
            "stayLength": "",
            "trip": "OW",
            "galileoKey": "",
            "travelBizKey": "",
        },
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    first_response = requests.post(url, json=first_payload, headers=headers)
    first_response_json = first_response.json()

    travel_biz_key = first_response_json["data"]["internationalList"]["travelBizKey"]
    galileo_key = first_response_json["data"]["internationalList"]["galileoKey"]

    time.sleep(20)
    second_payload = {
        "operationName ": "getInternationalList",
        "variables": {
            "adult": 1,
            "child": 0,
            "infant": 0,
            "where": "pc",
            "isDirect": True,
            "galileoFlag": galileo_key != "",
            "travelBizFlag": travel_biz_key != "",  # 값이 없으면 false
            "fareType": "Y",
            "itinerary": [
                {
                    "departureAirport": departureAirport,
                    "arrivalAirport": arrivalAirport,
                    "departureDate": departureDate,
                }
            ],
            "stayLength": "",
            "trip": "OW",
            "galileoKey": galileo_key,
            "travelBizKey": travel_biz_key,
        },
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    # GraphQL POST 요청 보내기
    second_response = requests.post(
        url, json=second_payload, headers=headers
    )  # 가져올때도있고 아닐때도 있고. 비동기로 처리?
    second_response_json = second_response.json()

    response_end = datetime.today()

    print(
        f"{departureAirport} to {arrivalAirport} at {departureDate}\nstart time : {response_start}\n end  time : {response_end}\nrunnning time : {response_end-response_start}"
    )
    return second_response_json


def fetch_data(route, days):
    departureDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
    response_json = getResponseJson(route[0], route[1], departureDate)
    return response_json


crawled_data = {}


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for route in routes:
        for days in range(30, 35):
            futures.append(executor.submit(fetch_data, route, days))

    for future in concurrent.futures.as_completed(futures):
        response_json = future.result()

        results = response_json["data"]["internationalList"]["results"]
        schedules = results["schedules"][0]  # dict obj
        fares = results["fares"]

        print(f"{next(iter(schedules))} 항공편 개수:", len(schedules))
        if len(schedules) != len(fares):
            print("항공편 개수와 fare개수가 다릅니다!")

        for key, values in schedules.items():
            fareSum = 0
            for val in (fares.get(key))["fare"]["A01"][0]["Adult"].values():
                fareSum += int(val)
            crawled_data[key] = {
                "id": key,
                "departureAirport": route[0],
                "arrivalAirport": route[1],
                "departureDate": values["detail"][0]["sdt"][:8],  # 출발 날짜
                "airline": values["detail"][0]["av"],  # 항공
                "departureTime": values["detail"][0]["sdt"][-4:],  # 출발 시각
                "arrivalTime": values["detail"][0]["edt"][-4:],  # 도착 시각
                "fare": fareSum,
            }
        # print(json.dumps(crawled_data, indent=4)  )
        print(len(crawled_data))
        print()

print("All threads have finished")


endTime = datetime.today()

crawled_data["log"] = {
    "id": "log",
    "crawledDate": startTime.strftime("%Y%m%d"),
    "length": len(crawled_data),
    "start Time": str(startTime),
    "running Time": str(endTime - startTime),
}
# log 출력
with open("data2_no_indent.json", "w") as json_file:  # 덮어쓰기임
    json.dump(crawled_data, json_file)
