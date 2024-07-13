from flask import Flask,render_template, request
import requests
app = Flask(__name__)

# /* ------------------------------------------------------------------------------------------------ */

@app.route('/')
def hello_world():
    return render_template('form.html', arrivaltime = None , RTSA_firstMsg = None , RTSA_secondMsg = None , SW_INFOLIST = None)

@app.route('/subway')
def test_subway():
    return render_template('search.html')

# /* ------------------------------------------------------------------------------------------------ */

@app.route('/getform',methods=['POST', 'GET'])
def getForm():
    a = None
    if request.method == 'POST':
        name = request.form['stationName']
        #함수 호출 
        
        # [RTSA] 실시간 역 도착정보 # 활성화 하지 않음
        # RTSA API KEY = 476a4267646572723737724355686d
        RTSA_URL = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1(1 ~ )/5( ~ 5)/(역이름)"

        # [RTP] 열차 실시간 위치 # 활성화 하지 않음
        # RTP API KEY = 795476586f6572723338674d467250
        RTP_URL = "http://swopenAPI.seoul.go.kr/api/subway/795476586f6572723338674d467250/json/realtimePosition/1(1 ~ )/40( ~ 40)/(호선이름)"

        # [RTSA] 첫차 검색
        RTSA_url_First_search = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/0/0/"+name

        # [RTSA] TEST #테스트 배드 사용안함
        RTSA_url_test = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1/40/"+name

        # [RTSA 2호선 강남역(1002000222)<TEST>] # 활성화 하지 않음 (테스트 배드 사용 변수)
        RTSA_url_Gangnam = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1/40/"+name

        # [RTP 2호선(1002)<TEST>]
        RTP_url_line2 = "http://swopenAPI.seoul.go.kr/api/subway/795476586f6572723338674d467250/json/realtimePosition/1/40/2호선"
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



    return render_template('form.html', time=arrivaltime, firstMsg=RTSA_firstMsg, secondMsg=RTSA_secondMsg, SW_INFOLIST=info_list, testord = test_ord , line_check_updn = lineupdn)

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
    updnline2 = 'def'
    updnline3 = 'def'

    #이름 및 호선 지정
    name = request.form['stationName']
    line = request.form['line']
    updnline = request.form['updnline']

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
    RTSA_url_First_search = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/0/40/"+name
    
    # 실시간 역 도착정보 불러오기
    RTSA_get_info = requests.get(RTSA_url_First_search)

    # 정보 json 변환
    RTSA_get_info = RTSA_get_info.json()

    
    if updnline == '내선':
        updnline2 = '상행'

    
    elif updnline == '외선':
        updnline3 = '하행'
    # 2호선 내선순환 조회
    for i in range(len(RTSA_get_info['realtimeArrivalList'])):
        if RTSA_get_info['realtimeArrivalList'][i]['updnLine'] == updnline or  RTSA_get_info['realtimeArrivalList'][i]['updnLine'] == updnline2 or RTSA_get_info['realtimeArrivalList'][i]['updnLine'] == updnline3:

            if RTSA_get_info['realtimeArrivalList'][i]['subwayId'] == line:
                    
                    arrivaltime = RTSA_get_info['realtimeArrivalList'][i]['barvlDt']
                    infomation_test = RTSA_get_info['realtimeArrivalList'][i]['btrainNo']
                    updnline_checker = RTSA_get_info['realtimeArrivalList'][i]['updnLine']
                    first_info = RTSA_get_info['realtimeArrivalList'][i]['arvlMsg2']
                    second_info = RTSA_get_info['realtimeArrivalList'][i]['arvlMsg3']


            #arvlcode 한글변환 부분
                    if RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "0":
                        arvlcode = "진입"

                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "1":
                        arvlcode = "도착"
                    
                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "2":
                        arvlcode = "출발"

                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "3":
                        arvlcode = "전역출발"

                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "4":
                        arvlcode = "전역진입"
                    
                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "5":
                        arvlcode = "전역도착"

                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "6":
                        arvlcode = "이거뭐야"

                    elif RTSA_get_info['realtimeArrivalList'][i]['arvlCd'] == "99":
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
    return render_template('search.html', time = arrivaltime , arrivalcode = arvlcode , train_number = infomation_test , updn_check = updnline_checker , first_info = first_info , second_info = second_info)

# /* ------------------------------------------------------------------------------------------------ */

if __name__ == '__main__':
    app.run()
