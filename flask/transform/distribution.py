from flask import Blueprint, render_template, request
from transform.auth import login_required
from lib.distribution_transform import distribution_from_orderinfo
from pathlib import Path
import datetime as dt
from path import UPLOAD_DIR_PATH

bp = Blueprint('distribution', __name__, url_prefix='/distribution')

#distribution page (distribution.html 실행)
@bp.route('/', methods = ['GET', 'POST'])
@login_required
def distribution():
    return render_template('distribution/distribution.html')

@bp.route('/complete', methods = ['GET', 'POST'])
def distribution_complete():
    if request.method == 'POST':
        #파일 이름 생성
        x = dt.datetime.now()
        file_name = f"{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}{x.microsecond}"
        
        # form 데이터받기
        file = request.files['file']
        form_data = request.form
        upload_path = f"{UPLOAD_DIR_PATH}/{file_name}물류파일.xlsx"

        #받은 데이터를 엑셀로 변환하여 저장하기
        distribution_from_orderinfo(file, form_data, upload_path)
            
        return render_template('distribution/distribution_complete.html', filename=f"{file_name}물류파일.xlsx" )