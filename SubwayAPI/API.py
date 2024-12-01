# /* ------------------------------------------------------------------------------------------------ */




# 본 코드를 진행하기에 앞서
# 본 SubwayAPI는 현재 개발중에 있는 FlowRail의 기초가 되는 코드입니다.
# 원래 여기에서 FlowRail를 개발했었으며, 현재는 Flask를 이용한 API 호출 코드와 남아있는 HTML 템플릿만 작동합니다.

# 실제로 사용하고 싶으신 분들은, Flask 말고도 다른 방법을 이용하여 본 코드를 수정하고 사용하시길 바랍니다.
# 본 SubwayAPI는 지하철 관련 프로젝트를 간단하게 진행하고싶거나, API와 관련한 제가 겪었던 부분들을 저장해놓은 문서입니다.

# SubwayAPI -> app.py 부분은 서울시 공공데이터 실시간 지하철 도착정보 등의 지하철 관련 API를 가지고 응용해놓은 코드입니다.
# 2호선 내선/외선 순환 조회시, 내선 및 외선으로 오는 문제로 인해 2호선 정보 조회가 안되는 문제점이 있습니다.
# 그 문제점을 해결한 간단한 코드도 포함되어있으니 참고해보시면 좋을겁니다. :)

# SubwayAPI -> API.py 부분은 정말 기본적인 정보를 API를 통해 호출 할 수 있는 코드들이 있습니다.



# /* ------------------------------------------------------------------------------------------------ */
import requests


# [RTSA] 실시간 역 도착정보
# RTSA API KEY = 476a4267646572723737724355686d
RTSA_URL = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/1(1 ~ )/5( ~ 5)/(역이름)"

# [RTP] 열차 실시간 위치
# RTP API KEY = 795476586f6572723338674d467250
RTP_URL = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimePosition/1(1 ~ )/40( ~ 40)/(호선이름)"

# [RTSA 2호선 강남역(1002000222)<TEST>]
RTSA_url_Gangnam = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/1/40/강남"

# [RTP 2호선(1002)<TEST>]
RTP_url_line2 = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimePosition/1/40/2호선"




RTSA_get_info = requests.get(RTSA_url_Gangnam) # 실시간 역 도착정보 불러오기
RTSA_get_info = RTSA_get_info.json()
print("강남역")
print("==========================================")
print("열차번호")
print(RTSA_get_info['realtimeArrivalList'][0]['btrainNo'])
print("열차정보 생성 시간")
print(RTSA_get_info['realtimeArrivalList'][0]['recptnDt'])
print("첫번째 도착메시지")
print(RTSA_get_info['realtimeArrivalList'][0]['arvlMsg2']) # [RTSA] 첫번째 도착메시지
print("두번째 도착메시지")
print(RTSA_get_info['realtimeArrivalList'][0]['arvlMsg3']) # [RTSA] 두번째 도착메시지
print("열차도착예정시간 (초)")
print(RTSA_get_info['realtimeArrivalList'][0]['barvlDt']) # [RTSA] 열차도착예정시간
print("==========================================")

RTP_get_info = requests.get(RTP_url_line2)
RTP_get_info = RTP_get_info.json()
print(RTP_get_info['realtimePositionList'][0]['subwayId'])
