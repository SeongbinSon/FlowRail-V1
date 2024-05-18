from flask import Flask,render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('form.html', arrivaltime = None)

@app.route('/getform',methods=['POST', 'GET'])
def getForm():
    a = None
    if request.method == 'POST':
        name = request.form['stationName']
        #함수 호출 
        
        # [RTSA] 실시간 역 도착정보
        # RTSA API KEY = 476a4267646572723737724355686d
        RTSA_URL = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1(1 ~ )/5( ~ 5)/(역이름)"

        # [RTP] 열차 실시간 위치
        # RTP API KEY = 795476586f6572723338674d467250
        RTP_URL = "http://swopenAPI.seoul.go.kr/api/subway/795476586f6572723338674d467250/json/realtimePosition/1(1 ~ )/40( ~ 40)/(호선이름)"

        # [RTSA 2호선 강남역(1002000222)<TEST>]
        RTSA_url_Gangnam = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1/40/"+name

        # [RTP 2호선(1002)<TEST>]
        RTP_url_line2 = "http://swopenAPI.seoul.go.kr/api/subway/795476586f6572723338674d467250/json/realtimePosition/1/40/2호선"
        RTSA_get_info = requests.get(RTSA_url_Gangnam) # 실시간 역 도착정보 불러오기
        RTSA_get_info = RTSA_get_info.json()
        print(name)
        print("==========================================")
        print("열차번호")
        print(RTSA_get_info['realtimeArrivalList'][1]['btrainNo'])
        print("열차정보 생성 시간")
        print(RTSA_get_info['realtimeArrivalList'][1]['recptnDt'])
        print("첫번째 도착메시지")
        print(RTSA_get_info['realtimeArrivalList'][1]['arvlMsg2']) # [RTSA] 첫번째 도착메시지
        print("두번째 도착메시지")
        print(RTSA_get_info['realtimeArrivalList'][1]['arvlMsg3']) # [RTSA] 두번째 도착메시지
        print("열차도착예정시간 (초)")
        print(RTSA_get_info['realtimeArrivalList'][1]['barvlDt']) # [RTSA] 열차도착예정시간
        print("==========================================")

        RTP_get_info = requests.get(RTP_url_line2)
        RTP_get_info = RTP_get_info.json()
        print(RTP_get_info['realtimePositionList'][1]['subwayId'])
        arrivaltime = RTSA_get_info['realtimeArrivalList'][1]['barvlDt']
        
    return render_template('form.html', time=arrivaltime)

@app.route('/test/<int:a>')
def hello_world2(a):
    print(a)
    return render_template('search.html')


@app.route('/subway')
def index():
    name = request.form['stationName']
    RTSA_url_Gangnam = "http://swopenAPI.seoul.go.kr/api/subway/476a4267646572723737724355686d/json/realtimeStationArrival/1/40/"+name
    RTSA_get_info = requests.get(RTSA_url_Gangnam) # 실시간 역 도착정보 불러오기
    RTSA_get_info = RTSA_get_info.json()
    list = [RTSA_get_info['realtimeArrivalList'][1]['btrainNo'], RTSA_get_info['realtimeArrivalList'][1]['recptnDt'], RTSA_get_info['realtimeArrivalList'][1]['arvlMsg2']]


if __name__ == '__main__':
    app.run()
