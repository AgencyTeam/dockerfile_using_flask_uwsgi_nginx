import pandas as pd
from path import UPLOAD_CHINA_FORM
from openpyxl import load_workbook

def excel2df(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except:
        print("엑셀파일을 불러오는데 실패했습니다.")
        return 0

def generate_df(brand,order_columns):
    # 빈 데이터프레임 선언
    data = pd.DataFrame()

    # 중국 서버용 형식에 맞게 변환 / 정확해보인것들 일부만 해봄.
    data["구분(품번)"] = brand["상품코드"]

    # 브랜드에서 한글로 제품명 제공한경우, 영문으로 바꿔야함
    # data["상품명"] = brand["상품명"]
    data["정상공급가"] = brand["최초소비자가"]
    data["색상(영문)"] = brand["색상"]
    data["재고수량"] = brand["총재고수량"]
    data["원산지(제조국)(영문)"] = brand["원산지"] + "/Korea"
    data["세탁방법"] = brand["세탁방법"]
    data["소재"] = brand["소재"]

    # 미입력시 기본값 적용되는 컬럼들.


    # 참조정보가 없는 컬럼 빈칸 처리
    for column in order_columns:
        if (column in data.columns):
            continue
        else:
            data[column] = ""

    data = data[order_columns]
    return data

def df2excel(df, form_path, new_path):
    wb = load_workbook(form_path)
    ws = wb['IMFORM']

    # 각 column의 값 추가
    col_cnt = 1
    for col in df.columns:
        row_cnt = 8
        for val in df[col]:
            ws.cell(row=row_cnt, column=col_cnt+1).value = val
            row_cnt += 1
        col_cnt += 1

    wb.save(new_path)

def brand2china(file_path,upload_path):
    order_columns = ['구분(품번)','상품명','정상공급가','할인율','할인공급가','색상(영문)','사이즈','사이즈(물산)','재고수량'
                    ,'원산지(제조국)(영문)','카테고리(대분류)','카테고리(중분류)','카테고리(소분류)','스타일+사이즈'
                    ,'상의-사이즈','상의-어깨너비','상의-가슴너비','상의-소매길이','상의-총장(앞)'
                    ,'하의-사이즈','하의-총장(아웃심)','하의-허리','하의-엉덩이','하의-허벅지','하의-밑위','하의-밑단'
                    ,'세탁방법','품목 및 모델명','소재','제품설명']

    brand_df = excel2df(file_path)
    del brand_df["이미지"]
    china_df = generate_df(brand_df, order_columns)
    df2excel(china_df,UPLOAD_CHINA_FORM,upload_path)
