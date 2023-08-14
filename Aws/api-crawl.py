import json  # json 파싱용
import time
from datetime import datetime, timedelta  # 크롤링 시간 측정

import requests  # http 통신

routes = [
    ["ICN", "LAX"],
]

startTime = datetime.today()
# 10일 이후까지
for route in routes:
    for days in range(33, 34):
        departureDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
        print(departureDate)

        url = "https://airline-api.naver.com/graphql"
        headers = {
            "Content-Type": "application/json",
            "Referer": f"https://m-flight.naver.com/flights/international/{route[0]}-{route[1]}-{departureDate}?adult=1&isDirect=true&fareType=Y",
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
                    {"departureAirport": route[0], "arrivalAirport": route[1], "departureDate": departureDate}
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
        schedules = first_response_json["data"]["internationalList"]["results"]["schedules"]
        travel_biz_key = first_response_json["data"]["internationalList"]["travelBizKey"]
        galileo_key = first_response_json["data"]["internationalList"]["galileoKey"]

        # print(schedules)
        print(f"---{departureDate}---")
        print("travel key: ", travel_biz_key)
        print("galileo key: ", galileo_key)
        # print(response_data)

        time.sleep(3)
        second_payload = {
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
                "itinerary": [
                    {"departureAirport": route[0], "arrivalAirport": route[1], "departureDate": departureDate}
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
        # print(json.dumps(second_response_json, indent=4))

        errs = second_response_json["data"]["internationalList"]["results"]["errors"]
        # print("err : ", errs)

        results = second_response_json["data"]["internationalList"]["results"]["schedules"][0]  # dict obj
        print("len:", len(results))

        print(results.keys())
        result_li = results.items()

        fare_li = second_response_json["data"]["internationalList"]["results"]["fares"]

        print(len(fare_li))

        for obj in fare_li.values():
            # print(obj["fare"]["A01"])
            print(json.dumps(obj["fare"]["A01"][0]["Adult"], indent=4))
            sum = (
                0
                + int(obj["fare"]["A01"][0]["Adult"]["Fare"])
                + int(obj["fare"]["A01"][0]["Adult"]["NaverFare"])
                + int(obj["fare"]["A01"][0]["Adult"]["Tax"])
                + int(obj["fare"]["A01"][0]["Adult"]["QCharge"])
            )
            print("합계 : ", sum, obj["sch"])
            print(results.get(obj["sch"][0])["detail"][0]["sdt"])
            print(results.get(obj["sch"][0])["detail"][0]["edt"])
        # print(json.dumps(results, indent=4))
