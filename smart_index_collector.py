# -- coding:UTF-8 --
"""
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-06 18:41:26
LastEditTime: 2023-06-08 16:22:48
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
"""
import csv
import uuid
import json
import sys
import random
import requests

filename = "三网融合驾驶舱-AI-指标.csv"

if len(sys.argv) == 1:
    raise Exception("未设置解析文件")

filename = sys.argv[1]

city_indexs = []
with open(filename, encoding="utf-8-sig") as csvfile:
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
            "category_field_6": row[header_idx["六大领域"]],
            "type": row[header_idx["类型"]],
            "value_url": row[header_idx["接口地址"]],
            "alarm": False,
        }
        if len(row[header_idx["均比值"]]) > 0:
            ci["compare"] = {
                "prefix": row[header_idx["均比前缀"]]
                if len(row[header_idx["均比前缀"]]) > 0
                else "日均",
                "precent": random.randint(1, 50),
            }
        if row[header_idx["告警"]] == "是":
            ci["alarm"] = True

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

with open("smartIndexs.json", "w") as f:
    f.write(s)

if len(sys.argv) > 2:
    print("do data update in "+sys.argv[2])
    if sys.argv[2] == "datam":
        # ------------------ #
        # 如有变更，请手动更新
        host = "http://39.170.15.45:8311"
        oid = "d529bfbf-519b-41be-9016-91a97fd07526"
        # 如有变更，请手动更新
        # ------------------ #
        x = requests.post(
            host+"/access-manager/auth/login",
            json={
                "account": "qiangqiang",
                "password": "28634125dd2a76f56054e8415992b9f9523104a0171660cf6e01978c729016aa",
                "encoding": "hex",
            },
        )
        token = x.json()["data"]["access_token"]
        x = requests.post(
            host+"/data-manager/dataset/"+oid+"/update",
            json={"content": city_indexs, "update_mode": "overwrite"},
            headers={"Authorization": "Bearer " + token},
        )
        print(x.json())
    elif sys.argv[2] == "css":
        # ------------------ #
        # 如有变更，请手动更新
        host = "http://10.162.12.144"
        resultIndexId = "14"
        # 如有变更，请手动更新
        # ------------------ #
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        x = requests.post(
            host + "/v1/index/login",
            headers=headers,
            data={"userNo": "admin", "password": "sa"},
        )
        token = x.json()["data"]["accessToken"]
        headers["Accesstoken"] = token

        x = requests.get(
            host + "/v1/sys/indextemplate/findDetail?resultIndexId=" + resultIndexId,
            headers=headers,
        )
        data = x.json()["data"][0]
        data["resultData"] = s

        x = requests.post(
            host + "/v1/sys/indextemplate/update",
            headers=headers,
            data=data,
        )
        print(x.json())

