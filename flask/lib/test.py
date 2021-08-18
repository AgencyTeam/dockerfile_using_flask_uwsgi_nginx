string = """허리단면-28.5cm~40cm 밑위-34cm 밑단단면-30cm 총장-38cm 허벅지단면-31.5cm
허리단면-31cm~45cm 밑위-34.5cm 밑단단면-32cm 총장-44cm 허벅지단면-34.5cm"""

from numpy import true_divide
import pandas as pd

df = pd.read_excel("C:/Users/donga/Downloads/통합데이터포맷_샘플 (4).xlsx", sheet_name="위챗미니프로그램")

split_c = df["색상"][2:].str.split('\n')
#print(split_c)

result_c = split_c.apply(lambda x: pd.Series(x))
#print(result_c)

result_c = result_c.stack().reset_index(level=1, drop=True).to_frame('색상')
print(result_c)

split_s = df["사이즈"][2:].str.split('\n')
#print(split_s)

result_s = split_s.apply(lambda x: pd.Series(x))
#print(result_s)

result_s = result_s.stack().reset_index(level=1, drop=True).to_frame('사이즈')
print(result_s)

#split.stack()
#print(result)
merge_result = df.merge(result_c, left_index=True, right_index=True, how='left')
print(merge_result)

merge_result2 = df.merge(result_s, left_index=True, right_index=True, how='left')
print(merge_result2)

merge_result2.to_excel("C:/SS-workspace/project/sample.xlsx")