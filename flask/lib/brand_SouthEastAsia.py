import pandas as pd
from path import UPLOAD_SEA_FORM
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

    # 동남아 서버용 형식에 맞게 변환 / 정확해보인것들 일부만 해봄.
    data["Product Name"] = brand["상품명"].str[0:255]
    # data["Product Description"] = brand[""]
    data["Maximum Purchase Quantity"] = brand["판매가능\n총수량"]
    data["Price"] = brand["최초소비자가"]
    data["Stock"] = brand["총재고수량"]
    data["Weight"] = brand["무게"].str[0:-1]
    data["Weight"] = pd.to_numeric(data["Weight"])/1000
    data["Weight"] = data["Weight"].round(2)    
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
    ws = wb['Template']

    # 각 column의 값 추가
    col_cnt = 1
    for col in df.columns:
        row_cnt = 6
        for val in df[col]:
            ws.cell(row=row_cnt, column=col_cnt).value = val
            row_cnt += 1
        col_cnt += 1

    wb.save(new_path)


def brand2SEA(file_path,upload_path):
    order_columns = ['Category','Product Name','Product Description','Maximum Purchase Quantity','Maximum Purchase Quantity - Start Date'
                    ,'Maximum Purchase Quantity - Time Period (in Days)','Maximum Purchase Quantity - End Date','Parent SKU','Variation Integration No.'
                    ,'Variation Name1','Option for Variation 1','Image per Variation','Variation Name2','Option for Variation 2','Price','Stock'
                    ,'SKU','Cover image','Item image 1','Item image 2','Item image 3','Item image 4','Item image 5','Item image 6','Item image 7','Item image 8'
                    ,'Weight','Length','Width','Height','Standard Express - Korea','Pre-order DTS']

    brand_df = excel2df(file_path)
    del brand_df["이미지"]
    sea_df = generate_df(brand_df,order_columns)
    df2excel(sea_df,UPLOAD_SEA_FORM,upload_path)