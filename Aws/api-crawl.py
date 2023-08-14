import json  # json 파싱용

import time
from datetime import datetime, timedelta  # 크롤링 시간 측정

import requests  #


url = "https://airline-api.naver.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Referer": "https://m-flight.naver.com/flights/international/ICN-DAD-20230907?adult=1&isDirect=true&fareType=Y",
}  # 필요한 경우 사용자 에이전트 정보 추가
payload1 = {
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
        "itinerary": [{"departureAirport": "ICN", "arrivalAirport": "DAD", "departureDate": "20230907"}],
        "stayLength": "",
        "trip": "OW",
        "galileoKey": "",
        "travelBizKey": "",
    },
    "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
}
response = requests.post(url, json=payload1, headers=headers)
response_data = response.json()
schedules = response_data["data"]["internationalList"]["results"]["schedules"]
travel_biz_key = response_data["data"]["internationalList"]["travelBizKey"]
galileo_key = response_data["data"]["internationalList"]["galileoKey"]
# print(schedules)
print("travle: ", travel_biz_key)
print("galileo : ", galileo_key)
# print(response_data)

time.sleep(5)


payload2 = {
    "operationName": "getInternationalList",
    "variables": {
        "adult": 1,
        "child": 0,
        "infant": 0,
        "where": "pc",
        "isDirect": True,
        "galileoFlag": galileo_key != "",
        "travelBizFlag": travel_biz_key != "",  # 값이 없으면 false
        "fareType": "Y",
        "itinerary": [{"departureAirport": "ICN", "arrivalAirport": "DAD", "departureDate": "20230907"}],
        "stayLength": "",
        "trip": "OW",
        "galileoKey": galileo_key,
        "travelBizKey": travel_biz_key,
    },
    "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
}
response2 = requests.post(url, json=payload2, headers=headers)  # 가져올때도있고 아닐때도 있고. 비동기로 처리?
response_data2 = response2.json()
print(json.dumps(response_data2, indent=4))
errs = response_data2["data"]["internationalList"]["results"]["errors"]
print("err : ", errs)
results = response_data2["data"]["internationalList"]["results"]["schedules"][0]  # dict obj
print("len:", len(results))
result_li = results.keys()
print(result_li)
# print(json.dumps(results, indent=4))


# GraphQL 요청 본문 데이터 정의


# GraphQL POST 요청 보내기
# response = requests.post(url, json=payload, headers=headers)

# 응답 데이터 확인
