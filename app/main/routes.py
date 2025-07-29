from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return '''
    <h1>Flame-Boundary-Tracking-Module</h1>
    <p>제작 중입니다.</p>
    <p>링크를 클릭하세요: <a href="/test">테스트 페이지</a></p>
    '''

@main_bp.route('/test')
def test():
    return render_template('test.html') 