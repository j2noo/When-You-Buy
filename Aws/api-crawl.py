import json  # json 파싱용
import time
from datetime import datetime, timedelta  # 크롤링 시간 측정
import requests  # http 통신
import concurrent.futures  # 멀티스레딩
import traceback  # 에러확인용

urlCnt = 0

routes = [
    ["ICN", "DAD"],
    # ["DAD", "ICN"],
    # ["ICN", "NRT"],
    # ["NRT", "ICN"],
    # ["ICN", "KIX"],
    # ["KIX", "ICN"],
    # ["ICN", "FUK"],
    # ["FUK", "ICN"],
    # ["ICN", "BKK"],
    # ["BKK", "ICN"],
    # ["ICN", "HKG"],
    # ["HKG", "ICN"],
    # ["ICN", "HAN"],
    # ["HAN", "ICN"],
    # ["ICN", "SGN"],
    # ["SGN", "ICN"],
    # ["GMP", "KIX"],
    # ["KIX", "GMP"],  # 18개
]

# 프로세스 시작 시간
startTime = datetime.today()


def getResponseJson(departureAirport, arrivalAirport, departureDate):
    # URL별 요청 시간 체크 - 시작 시간
    time.sleep(10)
    response_start = datetime.today()
    url = "https://airline-api.naver.com/graphql"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "1237",
        "Content-Type": "application/json",
        "Cookie": 'NNB=VLR5WESSPQGGI; NaverSuggestUse=unuse%26unuse; ASID=0e3f022600000186f517c1a00000004f; NDARK=N; _ga_K2ECMCJBFQ=GS1.1.1682860344.4.0.1682860351.0.0.0; _ga_SQ24F7Q7YW=GS1.1.1682860345.4.0.1682860351.0.0.0; NID_AUT=UzIruiM2+XOWEgpP8cWhtWXf1kx9HkgZJDGFwM+XpagtHDSMGvxpZv92j4ErSsue; NID_JKL=7SY5BYjkGfZagfgwDjhVBYmk+JQT9D96P6ABvYcXNU4=; _ga_YTT2922408=GS1.1.1686813881.80.0.1686813881.0.0.0; NV_WETR_LOCATION_RGN_M="MDk2ODAxMTI="; NV_WETR_LAST_ACCESS_RGN_M="MDk2ODAxMTI="; nx_ssl=2; _ga=GA1.2.713034617.1678596531; page_uid=iMwRuwp0JXosskNosSCssssstN4-390944; NID_SES=AAABpPwyzscjqtYyxtFwueSAYXyFqvPrXTWi9a2KtXQSYa7y50S48auDOpBUuWpmzx/vHhuoxd1Mitqx12C8CNllHztXyHHaEkGOO3zzWuZ+SW69zS8h4Y1eJox991uZBBbDiUSqYXr9oO49ey948BeIN+/7AMTeLhIPbmZBfbOjshjY+wKUHU1R9IlQFFf6gzq4E5dYpp9jf1USV5/GRRZ71G7EFqGPflf1zHDZqtlYrBaM4faaQoHUtzuuvQIzM8pA+lqPzdbUAWEIhDhORU5ibgg7szmdDq7FY0wSCfRDex5QM/+EIyyQaolP41hqxB4rg1s+bpQSlTnEnzfIajpm2jH64PwN0YfijYcnIM8y3Z4OudrHryqe9F1V/xFroSYiINX/mBRBndG3T+RZwRFyoicuICGgrDbjYbdAV7mzjSYc3AAhej+p7sOzgkUlx+JMAwTEWOi5kekbsizZMB0FUkrCp1mrAYMhkjxsMtnQXbdrkAgfzCCRqUIcestmFvZ8MxpIhSOhMjq21IiLhS53X09ocCTEH2/Z3Dzf0XJyKOe2pfbZ/rS8dKXgYg2leC694w==',
        "Origin": "https://flight.naver.com",
        "Referer": f"https://flight.naver.com/flights/international/{departureAirport}-{arrivalAirport}-{departureDate}?adult=1&isDirect=true&fareType=Y",
        "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }
    # GraphQL 요청 본문 데이터 정의 1
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
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = true, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    # GraphQL POST 요청 보내기 1
    try:
        first_response = requests.post(url, json=first_payload, headers=headers)
        if first_response.status_code != 200:
            print(
                f"{first_response.status_code} err at first POST, ",
                departureAirport,
                arrivalAirport,
                departureDate,
            )
            raise Exception("[Error] status code -1 : ", first_response.status_code)
    except:
        return first_response
        return {
            "request": "first",
            "responseCode": first_response.status_code,
            "departureAirport": departureAirport,
            "arrivalAirport": arrivalAirport,
            "departureDate": departureDate,
            "response json": first_response.text,
            "response header": first_response.headers,
        }

    # 첫 번째 요청에서 두개의 키 value 가져오기
    first_response_json = first_response.json()

    travel_biz_key = first_response_json["data"]["internationalList"]["travelBizKey"]
    galileo_key = first_response_json["data"]["internationalList"]["galileoKey"]
    # POST방식의 멱등성을 사용하지 않기 위해 서버에서 데이터를 로딩하는 시간 벌어주기
    time.sleep(20)

    # GraphQL 요청 본문 데이터 정의 2
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
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = true, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    # GraphQL POST 요청 보내기 2
    try:
        second_response = requests.post(url, json=second_payload, headers=headers)
        if second_response.status_code != 200:
            print(
                f"{second_response.status_code} err at second POST, ",
                departureAirport,
                arrivalAirport,
                departureDate,
            )
            raise Exception("[Error] status code -2 : ", second_response.status_code)
    except:
        # print(
        #     "실패2",
        #     {
        #         "request": "second",
        #         "responseCode": second_response.status_code,
        #         "departureAirport": departureAirport,
        #         "arrivalAirport": arrivalAirport,
        #         "departureDate": departureDate,
        #         "response json": second_response.text,
        #         "response header": second_response.headers,
        #     },
        # )
        return second_response
        # return {
        #     "request": "second",
        #     "responseCode": second_response.status_code,
        #     "departureAirport": departureAirport,
        #     "arrivalAirport": arrivalAirport,
        #     "departureDate": departureDate,
        #     "response json": second_response.text,
        # }
    # URL별 요청 시간 체크 - 종료 시간
    response_end = datetime.today()

    # print(second_response.status_code, second_response.headers, "@")
    return second_response


# 스레드 단위 정의
def fetch_data(route, days):
    departureDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
    response_json = getResponseJson(route[0], route[1], departureDate)
    return response_json


# 수집 데이터
crawled_data = {}

# 멀티스레딩 라이브러리의 인스턴스를 생성하여 executor로써 관리함
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []

    # 스레드 생성
    for route in routes:
        for days in range(3, 202):
            futures.append(executor.submit(fetch_data, route, days))
            time.sleep(3)

    # 스레드가 완료될 때 마다 주기적으로 실행함
    for future in concurrent.futures.as_completed(futures):
        urlCnt += 1
        try:
            # 스레드 응답
            response = future.result()
            if response.status_code != 200:
                print(response.headers)
                raise Exception("response code REER", response.status_code)

            response_json = response.json()
            results = response_json["data"]["internationalList"]["results"]

            # schedules가 비어있으면 api 다시 호출하기
            if results["schedules"] == []:
                raise Exception("response is empty!")

            # 응답에서 필요한 데이터 파싱
            schedules = results["schedules"][0]  # 비행 정보
            fares = results["fares"]  # 가격 정보

            # 항공편 개수 파악
            print(f"{next(iter(schedules))[:14 ]} 항공편 개수:", len(schedules))
            if len(schedules) != len(fares):
                print("항공편 개수와 fare개수가 다릅니다!", len(schedules), len(fares))
                raise Exception("fare != schedules")
                # 다를수도 있다고!!!! fares에 맞춰서 해야ㅏㅁ.

            # 항공편 정보 추출하기
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

        except Exception as e:
            print("cnt: ", urlCnt, "response Err occured ->", e)
            err_msg = traceback.format_exc()
            with open("./Crawling/error/error.json", "a") as json_file:
                json.dump(
                    {
                        "error_message": err_msg,
                        # "response_header": response.headers,
                        # "response_json": response_json,
                    },
                    json_file,
                    indent=4,
                )
print("All threads have finished")


# 프로세스 종료 시간
endTime = datetime.today()

# 러닝타임 계산
print(
    f"start time : {startTime}\n end  time : {endTime}\nrunnning time : {endTime-startTime}"
)


crawled_data["log"] = {
    "id": "log",
    "crawledDate": startTime.strftime("%Y%m%d"),
    "length": len(crawled_data),
    "start Time": str(startTime),
    "running Time": str(endTime - startTime),
}
# log 출력
with open("./Crawling/data/data2_no_indent.json", "w") as json_file:  # 덮어쓰기임
    json.dump(crawled_data, json_file, indent=4)
