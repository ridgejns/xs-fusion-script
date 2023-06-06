#-- coding:UTF-8 --
"""
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-06 11:08:28
LastEditTime: 2023-06-06 11:33:51
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
"""
import csv
import uuid
import json
import sys
import requests

filename = "三网融合驾驶舱-场景地址及ppt.csv"

if len(sys.argv) == 1:
    raise Exception("未设置解析文件")

filename = sys.argv[1]

tree = []

data = []
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    headers = next(csv_reader)  # 读取第一行每一列的标题
    print(headers)
    for i,h in enumerate(headers):
        print(i, h)
        
    for row in csv_reader:  # 将csv 文件中的数据保存到data中
        if row[0] == "":
            continue
        item_tree = None
        for t in tree:
            if row[0] == t["abbreviationName"]:
                item_tree = t
        if item_tree is None:
            tb = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[0],
                "depth": 1,
                "children": [],
            }
            item_tree = tb
            print("1:", item_tree)
            tree.append(item_tree)

        item_tree2 = None
        for t in item_tree["children"]:
            if row[1] == t["abbreviationName"]:
                item_tree2 = t
        if item_tree2 is None:
            tb2 = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[1],
                "depth": 2,
                "children": [],
            }
            item_tree2 = tb2
            print("2:", item_tree2)
            item_tree["children"].append(item_tree2)

        item_tree3 = None
        for t in item_tree2["children"]:
            if row[2] == t["abbreviationName"]:
                item_tree3 = t
        if item_tree3 is None:
            tb3 = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[2] if len(row[2])>0 else row[3],
                "depth": 3,
                "children": [],
            }
            item_tree3 = tb3
            print("3:", item_tree3)
            item_tree2["children"].append(item_tree3)

        final_item_tree = item_tree3
        if (
            item_tree["abbreviationName"] == "融合场景"
            and item_tree2["abbreviationName"] == "流程再造"
        ):
            item_tree4 = None
            for t in item_tree3["children"]:
                if row[3] == t["abbreviationName"]:
                    item_tree4 = t
            if item_tree4 is None:
                tb4 = {
                    "id": str(uuid.uuid4()),
                    "abbreviationName": row[3],
                    "depth": 4,
                    "children": [],
                }
                item_tree4 = tb4
                print("4:", item_tree4)
                item_tree3["children"].append(item_tree4)
            final_item_tree = item_tree4


        final_item_tree["panelUrl"] = row[4]
        final_item_tree["panelImgUrls"] = []
        if len(row[5]) > 0:
            final_item_tree["panelImgUrls"] = row[5].split("\n")
        if len(final_item_tree["panelImgUrls"]) > 0:
            final_item_tree["panelImgUrl"] = final_item_tree["panelImgUrls"][0]

        final_item_tree["sketchUrls"] = []
        if len(row[6]) > 0:
            final_item_tree["sketchUrls"] = row[6].split("\n")
        if len(final_item_tree["sketchUrls"]) > 0:
            final_item_tree["sketchUrl"] = final_item_tree["sketchUrls"][0]

        final_item_tree["is32"] = False
        if row[7] == "是":
            final_item_tree["is32"] = True
        final_item_tree["click"] = False
        if row[8] == "是":
            final_item_tree["click"] = True
        row[9] = row[9].strip()
        if len(row[9]) > 0:
            try:
                sortNumber = int(row[9])
                final_item_tree["sortNumber"] = sortNumber
            except Exception as e:
                print(e)

s = json.dumps(tree, ensure_ascii=False)
# print(s)

with open("screenURL.json", "w") as f:
    f.write(s)

if len(sys.argv) > 2:
    print("do data update")
    x = requests.post(
        "http://39.170.15.45:8311/access-manager/auth/login",
        json={
            "account": "qiangqiang",
            "password": "28634125dd2a76f56054e8415992b9f9523104a0171660cf6e01978c729016aa",
            "encoding": "hex",
        },
    )
    token = x.json()["data"]["access_token"]
    x = requests.post(
        "http://39.170.15.45:8311/data-manager/dataset/2cd0cdd6-86fb-4db7-b1bd-4124cd40920e/update",
        json={"content": tree, "update_mode": "overwrite"},
        headers={"Authorization": "Bearer " + token},
    )
    print(x.json())