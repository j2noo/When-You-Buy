import json  # json 파싱용
import time
from datetime import datetime, timedelta  # 크롤링 시간 측정
import requests  # http 통신
import concurrent.futures  # 멀티스레딩
import traceback  # 에러확인용


routes = [
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

# 프로세스 시작 시간
startTime = datetime.today()


def getResponseJson(departureAirport, arrivalAirport, departureDate):
    # URL별 요청 시간 체크 - 시작 시간
    response_start = datetime.today()
    url = "https://airline-api.naver.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://m-flight.naver.com/flights/international/{departureAirport}-{arrivalAirport}-{departureDate}?adult=1&isDirect=true&fareType=Y",
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
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    # GraphQL POST 요청 보내기 1
    try:
        first_response = requests.post(url, json=first_payload, headers=headers)
        first_response_json = first_response.json()

    except:
        return {
            "request": "first",
            "responseCode": first_response.status_code,
            "departureAirport": departureAirport,
            "arrivalAirport": arrivalAirport,
            "departureDate": departureDate,
        }

    # 첫 번째 요청에서 두개의 키 value 가져오기
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
        "query": 'query getInternationalList($trip: String!, $itinerary: [InternationalList_itinerary]!, $adult: Int = 1, $child: Int = 0, $infant: Int = 0, $fareType: String!, $where: String = "pc", $isDirect: Boolean = false, $stayLength: String, $galileoKey: String, $galileoFlag: Boolean = true, $travelBizKey: String, $travelBizFlag: Boolean = true) {\n  internationalList(\n    input: {trip: $trip, itinerary: $itinerary, person: {adult: $adult, child: $child, infant: $infant}, fareType: $fareType, where: $where, isDirect: $isDirect, stayLength: $stayLength, galileoKey: $galileoKey, galileoFlag: $galileoFlag, travelBizKey: $travelBizKey, travelBizFlag: $travelBizFlag}\n  ) {\n    galileoKey\n    galileoFlag\n    travelBizKey\n    travelBizFlag\n    totalResCnt\n    resCnt\n    results {\n      airlines\n      airports\n      fareTypes\n      schedules\n      fares\n      errors\n    }\n  }\n}\n',
    }

    # GraphQL POST 요청 보내기 2
    try:
        second_response = requests.post(url, json=second_payload, headers=headers)
        second_response_json = second_response.json()
    except:
        return {
            "request": "second",
            "responseCode": second_response.status_code,
            "departureAirport": departureAirport,
            "arrivalAirport": arrivalAirport,
            "departureDate": departureDate,
        }
    # URL별 요청 시간 체크 - 종료 시간
    response_end = datetime.today()

    # print(
    #     f"{departureAirport} to {arrivalAirport} at {departureDate}\nstart time : {response_start}\n end  time : {response_end}\nrunnning time : {response_end-response_start}"
    # )
    return second_response_json


# 스레드 단위 정의
def fetch_data(route, days):
    departureDate = (startTime + timedelta(days=days)).strftime("%Y%m%d")
    response_json = getResponseJson(route[0], route[1], departureDate)
    return response_json


# 수집 데이터
crawled_data = {}

# 멀티스레딩 라이브러리의 인스턴스를 생성하여 executor로써 관리함
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []

    # 스레드 생성
    for route in routes:
        for days in range(30, 40):
            futures.append(executor.submit(fetch_data, route, days))

    # 스레드가 완료될 때 마다 주기적으로 실행함
    for future in concurrent.futures.as_completed(futures):
        try:
            # 스레드 응답
            response_json = future.result()
            results = response_json["data"]["internationalList"]["results"]

            # schedules가 비어있으면 api 다시 호출하기
            if results["schedules"] == []:
                raise Exception("response가 비었습니다")

            # 응답에서 필요한 데이터 파싱
            schedules = results["schedules"][0]  # 비행 정보
            fares = results["fares"]  # 가격 정보

            # 항공편 개수 파악
            print(f"{next(iter(schedules))[:14 ]} 항공편 개수:", len(schedules))
            if len(schedules) != len(fares):
                print("항공편 개수와 fare개수가 다릅니다!")

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
            print("response err 발생", e)
            err_msg = traceback.format_exc()
            with open("./Crawling/error/error.json", "aa\") as json_file:
                json.dump(
                    {"error_message": err_msg, "response_json": response_json},
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
