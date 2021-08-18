from flask import Blueprint, render_template, request
from lib.brand_domestic import brand2domestic
from lib.brand_SouthEastAsia import brand2SEA
from lib.brand_china import brand2china
from path import UPLOAD_DIR_PATH
import datetime as dt
from zipfile import ZipFile
import pandas as pd

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=['GET', 'POST'])
def upload():
    return render_template('upload/upload.html')


@bp.route('/complete', methods=['GET', 'POST'])
def upload_complete():
    if request.method == 'POST':
        try:
            # 브랜드 압축파일 해제, file=브랜드엑셀파일경로, zip_file_list=jpg리스트
            # zip_file = request.files['file']
            # with ZipFile(zip_file, 'r') as zip:
            #     zip_file_list = zip.namelist()
            #     for name in zip_file_list:
            #         if name.endswith("xlsx"):
            #             zip.extract(name,f"{UPLOAD_DIR_PATH}")
            #             file = f"{UPLOAD_DIR_PATH}/{name}"
            #             break

            file = request.files['file']

            # 서버선택리스트 받기
            server_list = request.form.getlist('server')

            x = dt.datetime.now()
            file_name = f"{x.year}{x.month}{x.day}{x.hour}{x.minute}{x.second}{x.microsecond}"

            if 'Domestic' in server_list:
                path_1 = f"{UPLOAD_DIR_PATH}/{file_name}국내서버업로드용.xlsx"
                brand2domestic(file,path_1)

            if 'SouthEastAsia' in server_list:
                path_2 = f"{UPLOAD_DIR_PATH}/{file_name}동남아서버업로드용.xlsx"
                brand2SEA(file,path_2)

            if 'China' in server_list:
                path_3 = f"{UPLOAD_DIR_PATH}/{file_name}중국(위챗)서버업로드용.xlsx"
                brand2china(file,path_3)
            

            return render_template('upload/upload_complete.html', server_list=server_list
                                    ,domestic_path = f"{file_name}국내서버업로드용.xlsx"
                                    ,sea_path = f"{file_name}동남아서버업로드용.xlsx"
                                    ,china_path = f"{file_name}중국(위챗)서버업로드용.xlsx")
        except:
            return '파일 변환에 실패하였습니다. 다시 시도해주세요.'
