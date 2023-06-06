#-- coding:UTF-8 --
"""
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-06 14:46:44
LastEditTime: 2023-06-06 15:01:40
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
"""
import csv
import uuid
import json
import sys
import random

filename = "三网融合驾驶舱-首页体征.csv"

if len(sys.argv) == 1:
    raise Exception("未设置解析文件")

filename = sys.argv[1]

city_indexs = []
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    headers = next(csv_reader)  # 读取第一行每一列的标题
    print(headers)
    header_idx = {}
    for i, h in enumerate(headers):
        header_idx[h] = i
    for i, row in enumerate(csv_reader):  # 将csv 文件中的数据保存到data中
        if row[header_idx["指标"]] == "":
            continue
        ci = {
            "index": i,
            "label": row[header_idx["指标"]],
            "value": random.randint(1, 5000),
            "unit": row[header_idx["单位"]],
            "color": "",
            "compare": {
                "prefix": row[header_idx["均比前缀"]]
                if len(row[header_idx["均比前缀"]]) > 0
                else "日均",
                "precent": random.randint(1, 50),
            },
            "category_field_6": row[header_idx["领域"]],
            "category_field_6_2": row[header_idx["二级指标"]],
            "category_2": row[header_idx["分类"]],
            "value_url": row[header_idx["接口地址"]],
            "alarm": False,
        }
        if row[header_idx["告警"]]=="是":
            ci["alarm"]=True

        if len(row[header_idx["静态值"]]) > 0:
            try:
                ci["value"] = float(row[header_idx["静态值"]])
            except Exception as e:
                 print(row[header_idx["指标"]], "静态值", e)
        if len(row[header_idx["均比值"]]) > 0:
            try:
                ci["compare"]["precent"] = float(row[header_idx["均比值"]])
            except Exception as e:
                print(row[header_idx["指标"]], "均比值", e)
        city_indexs.append(ci)

s = json.dumps(city_indexs, ensure_ascii=False)
# print(s)

with open("cityIndexs.json", "w") as f:
    f.write(s)
