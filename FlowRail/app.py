from flask import Flask,render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('form.html')

@app.route('/getform',methods=['POST'])
def getForm():
    name = request.form['stationName']
    #함수 호출 
    a = "3분"
    return render_template('form.html', time=a)

@app.route('/test/<int:a>')
def hello_world2(a):
    print(a)
    return render_template('search.html')


if __name__ == '__main__':
    app.run()
