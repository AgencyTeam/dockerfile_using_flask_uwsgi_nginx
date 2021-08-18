from flask import Blueprint, render_template
# 'main' -> 나중에 함수명으로 URL을 찾아내는 url_for 함수에서 쓰는 이름
# __name__ -> 모듈명
# url_prefix -> 함수들의 URL 앞에 항상 붙게 되는 프리픽스 URL
# ex) '/' 대신 '/main' 이라고 선언하면, localhost:5000/ 대신 localhost:5000/main/ 이라고 호출해야함.
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def main():
    return render_template('main/main.html')


# @bp.route('/master_update', methods=['GET', 'POST'])
# def master():
#     return render_template('main/masterDB.html')
