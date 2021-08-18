# from webproject_1.main.index import index
import pandas as pd
import json
# from collections import OrderedDict
# from numpyencoder import NumpyEncoder
# import os

def excel2json(excel_path, json_path):
    df = pd.read_excel(excel_path)
    df.to_json(json_path, force_ascii = False, orient="index")

    json_data = {}
    with open(json_path, 'r', encoding='utf-8') as make_file:
        json_data = json.load(make_file)
        for data in json_data:
            del json_data[data]["Unnamed: 0"]
    
    with open(json_path, 'w', encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent='\t')