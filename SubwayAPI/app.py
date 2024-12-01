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


from flask import Flask, render_template, request
import requests
app = Flask(__name__)

line_number = {
    "1077" : "신분당선",
    "1002" : "2호선"
}
# /* ------------------------------------------------------------------------------------------------ */

@app.route('/')
def hello_world():
    return render_template('form.html', arrivaltime = None , RTSA_firstMsg = None , RTSA_secondMsg = None , SW_INFOLIST = None)

@app.route('/subway')
def test_subway():
    return render_template('search.html')

@app.route('/first')
def test_first_page():
    return render_template('./service_templates/index.html')

@app.route('/check-time')
def test_check_time_page():
    return render_template('./service_templates/check-time.html')

@app.route('/station-search')
def test_station_search_page():
    return render_template('./service_templates/station-search.html')

@app.route('/DI')
def test_subway_DI():
    return render_template('./service_templates/subway-DI.html')

# /* ------------------------------------------------------------------------------------------------ */

@app.route('/getform',methods=['POST', 'GET'])
def getForm():
    a = None
    if request.method == 'POST':
        name = request.form['stationName']
        #함수 호출 
        
        # [RTSA] 실시간 역 도착정보 # 활성화 하지 않음
        # RTSA API KEY = 476a4267646572723737724355686d
        RTSA_URL = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/1(1 ~ )/5( ~ 5)/(역이름)"

        # [RTP] 열차 실시간 위치 # 활성화 하지 않음
        # RTP API KEY = 795476586f6572723338674d467250
        RTP_URL = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimePosition/1(1 ~ )/40( ~ 40)/(호선이름)"

        # [RTSA] 첫차 검색
        RTSA_url_First_search = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/0/0/"+name

        # [RTSA] TEST #테스트 배드 사용안함
        RTSA_url_test = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/1/40/"+name

        # [RTSA 2호선 강남역(1002000222)<TEST>] # 활성화 하지 않음 (테스트 배드 사용 변수)
        RTSA_url_Gangnam = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/1/40/"+name

        # [RTP 2호선(1002)<TEST>]
        RTP_url_line2 = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimePosition/1/40/2호선"
        RTSA_get_info = requests.get(RTSA_url_test) # 실시간 역 도착정보 불러오기
        RTSA_get_info = RTSA_get_info.json()

# /* ------------------------------------------------------------------------------------------------ */
        
        # RTSA Index Terminal
        print("==========================================")
        print(name)
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
        print("* RTSA_INFOLIST *")
        print([RTSA_get_info['realtimeArrivalList'][0]['btrainNo'], RTSA_get_info['realtimeArrivalList'][0]['recptnDt'], RTSA_get_info['realtimeArrivalList'][0]['arvlMsg2']])
        print("==========================================")

# /* ------------------------------------------------------------------------------------------------ */

        RTP_get_info = requests.get(RTP_url_line2)
        print(RTSA_get_info)
        RTP_get_info = RTP_get_info.json()

        print(RTP_get_info['realtimePositionList'][0]['subwayId'])

        # barvlDt / arvlMsg2 / arvlMsg3 / infolist / ordkey / updnLine 표시
        arrivaltime = RTSA_get_info['realtimeArrivalList'][0]['barvlDt']
        RTSA_firstMsg = RTSA_get_info['realtimeArrivalList'][0]['arvlMsg2']
        RTSA_secondMsg = RTSA_get_info['realtimeArrivalList'][0]['arvlMsg3']
        info_list = [RTSA_get_info['realtimeArrivalList'][0]['btrainNo'], RTSA_get_info['realtimeArrivalList'][0]['recptnDt'], RTSA_get_info['realtimeArrivalList'][0]['arvlMsg2']]
        test_ord = RTSA_get_info['realtimeArrivalList'][0]['ordkey']
        lineupdn = RTSA_get_info['realtimeArrivalList'][0]['updnLine']



    return render_template('subway-DI.html', time=arrivaltime, firstMsg=RTSA_firstMsg, secondMsg=RTSA_secondMsg, SW_INFOLIST = info_list, testord = test_ord , line_check_updn = lineupdn)

# /* ------------------------------------------------------------------------------------------------ */

#subway 기능 구현 테스트배드
@app.route('/getsearch',methods=['POST', 'GET'])
def getsubway():

    #값 초기화
    arrivaltime = 0
    infomation_test = 1
    arvlcode = "default"
    updnline_checker = "default"
    first_info = "default"
    second_info = "default"
    inner_circle_line_to_up_line = 'default'
    outer_circle_line_to_dn_line = 'default'
    trainlinenum = 'default'

    #이름 및 호선 지정
    name = request.form['stationName']
    line = request.form['line']
    updnline = request.form['updnline']
    print(name,  line, updnline)
# /* ------------------------------------------------------------------------------------------------ */

    # [/subway] RTSA Line & UpdnLine Terminal
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("호선")
    print(line)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("상하행")
    print(updnline)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")

# /* ------------------------------------------------------------------------------------------------ */

   #열차 검색을 위한 RTSA_url_First_search
    RTSA_url_First_search = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/0/40/"+name
    RTSA_url_Second_search = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/0/40/"+name
    RTSA_url_Third_search = "http://swopenAPI.seoul.go.kr/api/subway/(API KEY INPUT)/json/realtimeStationArrival/2/2/"+name
    # 실시간 역 도착정보 불러오기
    RTSA_get_info = requests.get(RTSA_url_First_search)
    RTSA_Second_get_info = requests.get(RTSA_url_Second_search)

    # 정보 json 변환
    RTSA_get_info = RTSA_get_info.json()
    RTSA_Second_get_info = RTSA_Second_get_info.json()

    
    if updnline == '내선':
        inner_circle_line_to_up_line = '상행'

    
    elif updnline == '외선':
        outer_circle_line_to_dn_line = '하행'
    # 2호선 내선순환 조회
    for Timelist in range(len(RTSA_get_info['realtimeArrivalList'])):
        if RTSA_get_info['realtimeArrivalList'][Timelist]['updnLine'] == updnline or  RTSA_get_info['realtimeArrivalList'][Timelist]['updnLine'] == inner_circle_line_to_up_line or RTSA_get_info['realtimeArrivalList'][Timelist]['updnLine'] == outer_circle_line_to_dn_line:

            if RTSA_get_info['realtimeArrivalList'][Timelist]['subwayId'] == line:
                    
                    arrivaltime = RTSA_get_info['realtimeArrivalList'][Timelist]['barvlDt']
                    infomation_test = RTSA_get_info['realtimeArrivalList'][Timelist]['btrainNo']
                    updnline_checker = RTSA_get_info['realtimeArrivalList'][Timelist]['updnLine']
                    first_info = RTSA_get_info['realtimeArrivalList'][Timelist]['arvlMsg2']
                    second_info = RTSA_get_info['realtimeArrivalList'][Timelist]['arvlMsg3']

            
                            #arvlcode 한글변환 부분
                    if RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "0":
                        arvlcode = "진입"

                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "1":
                        arvlcode = "도착"
                    
                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "2":
                        arvlcode = "출발"

                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "3":
                        arvlcode = "전역출발"

                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "4":
                        arvlcode = "전역진입"
                    
                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "5":
                        arvlcode = "전역도착"


                    elif RTSA_get_info['realtimeArrivalList'][Timelist]['arvlCd'] == "99":
                        arvlcode = "운행중"
                    break
    



    for S_Timelist in range(len(RTSA_Second_get_info['realtimeArrivalList'])):
        if RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['updnLine'] == updnline or RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['updnLine'] == inner_circle_line_to_up_line or RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['updnLine'] == outer_circle_line_to_dn_line:
            
            if RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['subwayId'] == line:
                    second_arrivaltime = RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['barvlDt']
                    second_infomation_test = RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['btrainNo']
                    second_updnline_checker = RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['updnLine']
                    second_first_info = RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlMsg2']
                    two_second_info = RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlMsg3']


                    
                    if RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "0":
                        arvlcode = "진입"

                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "1":
                        arvlcode = "도착"
                    
                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "2":
                        arvlcode = "출발"

                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "3":
                        arvlcode = "전역출발"

                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "4":
                        arvlcode = "전역진입"
                    
                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "5":
                        arvlcode = "전역도착"


                    elif RTSA_Second_get_info['realtimeArrivalList'][S_Timelist]['arvlCd'] == "99":
                        arvlcode = "운행중"
                    break

# /* ------------------------------------------------------------------------------------------------ */

    # [/subway] RTSA Command Terminal
    print("/* ------------------------------------------------------------------------------------------------ */")
    print("/*                                     RTSA Command Terminal                                        */")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("열차도착예정시간(arrivaltime)")
    print(arrivaltime)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("도착코드 (arvlCd)")
    print(arvlcode)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("열차번호 (btrainNm)")
    print(infomation_test)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("상하행선 구분 (updnLine)")
    print(updnline_checker)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("첫번째 도착 메시지 (arvlMsg2)")
    print(first_info)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(" ")
    print("두번째 도착 메시지 (arvlMsg3)")
    print(second_info)
    print(" ")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print("/*                                                                                                  */")
    print("/* ------------------------------------------------------------------------------------------------ */")
    print(infomation_test) # 열차 번호
    print(first_info)
    print(second_info) # 현재 역
    print(arvlcode) # 도착 코드

    return render_template('./service_templates/subway-DI.html', name = name, line=line_number[line] ,time = arrivaltime , arrivalcode = arvlcode , train_number = infomation_test ,updn_check = updnline_checker , first_info = first_info , second_info = second_info,second_arrivaltime = second_arrivaltime, second_infomation_test = second_infomation_test,second_updnline_checker = second_updnline_checker, second_first_info = second_first_info, two_second_info = two_second_info)

# /* ------------------------------------------------------------------------------------------------ */
@app.route("/test")
def test():
    return render_template("station_search_test.html")
if __name__ == '__main__':
    app.run()
