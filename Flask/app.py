# 가상 환경 접속 되어있는지 확인하기
# env\Scripts\activate

from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "안녕하세요. <h1> FBTM 웹서비스 제작중입니다. </h1>"
