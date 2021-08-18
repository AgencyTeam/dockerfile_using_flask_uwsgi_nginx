import os
from pathlib import Path

ROOT_PATH = str(Path(os.path.realpath(__file__)).parent)
ORDER_EXCEL_FORM = ROOT_PATH + '/transform/static/excel_form/발주form.xlsx'
UPLOAD_DIR_PATH = ROOT_PATH + '/upload_files'
DISTRIBUTION_EXCEL_FORM = ROOT_PATH +  '/transform/static/excel_form/물류form.xlsx'
UPLOAD_DOMESTIC_FORM = ROOT_PATH + '/transform/static/excel_form/domestic_form.xlsx'
UPLOAD_SEA_FORM = ROOT_PATH + '/transform/static/excel_form/SouthEastAsia_form.xlsx'
UPLOAD_CHINA_FORM = ROOT_PATH + '/transform/static/excel_form/china_form.xlsx'
