from transform.auth import login_required
from flask import Blueprint, render_template, request
from lib.order_transform import make_excel
from path import UPLOAD_DIR_PATH
import datetime as dt

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def order():
    return render_template('order/order.html')


@bp.route('/complete', methods=['GET', 'POST'])
def order_complete():
    if request.method == 'POST':

        # 파일 이름 생성
        x = dt.datetime.now()
        file_name = f"{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}{x.microsecond}"

        # form 데이터 받기
        file = request.files['file']
        form_data = request.form
        upload_path = f"{UPLOAD_DIR_PATH}/{file_name}.xlsx"

        # 받은 데이터를 엑셀로 변환하여 저장하기
        make_excel(file, form_data, upload_path)

        return render_template('order/order_complete.html', filename=f"{file_name}.xlsx")
