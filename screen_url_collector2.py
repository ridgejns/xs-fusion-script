# -- coding:UTF-8 --
"""
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-12 10:49:02
LastEditTime: 2023-06-12 15:05:57
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
sort_nums = []
with open(filename, encoding="utf-8-sig") as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    headers = next(csv_reader)  # 读取第一行每一列的标题
    print(headers)
    header_idx = {}
    for i, h in enumerate(headers):
        header_idx[h] = i

    for row in csv_reader:  # 将csv 文件中的数据保存到data中
        if row[header_idx["一级标题（0612更新）"]] == "":
            continue
        item_tree = None
        for t in tree:
            if row[header_idx["一级标题（0612更新）"]] == t["abbreviationName"]:
                item_tree = t
        if item_tree is None:
            tb = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[header_idx["一级标题（0612更新）"]],
                "depth": 1,
                "children": [],
            }
            item_tree = tb
            print("1:", item_tree)
            tree.append(item_tree)

        item_tree2 = None
        for t in item_tree["children"]:
            if row[header_idx["二级标题（0612更新）"]] == t["abbreviationName"]:
                item_tree2 = t
        if item_tree2 is None:
            srn = int(row[header_idx["标题优先级"]])
            tb2 = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[header_idx["二级标题（0612更新）"]],
                "depth": 2,
                "children": [],
                "sort_num": srn,
            }
            item_tree2 = tb2
            print("2:", item_tree2)
            if len(sort_nums) > 0:
                idx = 0
                for sort_num in sort_nums:
                    if sort_num < srn:
                        idx += 1
                sort_nums.insert(idx, srn)
                item_tree["children"].insert(idx, item_tree2)
            else:
                sort_nums.append(int(row[header_idx["标题优先级"]]))
                item_tree["children"].append(item_tree2)

            # item_tree["children"].append(item_tree2)

        item_tree3 = None
        for t in item_tree2["children"]:
            if row[header_idx["三级标题（旧）"]] == t["abbreviationName"]:
                item_tree3 = t
        if item_tree3 is None:
            tb3 = {
                "id": str(uuid.uuid4()),
                "abbreviationName": row[header_idx["三级标题（旧）"]]
                if len(row[header_idx["三级标题（旧）"]]) > 0
                else row[header_idx["应用名称"]],
                "depth": 3,
                "children": [],
            }
            item_tree3 = tb3
            print("3:", item_tree3)
            item_tree2["children"].append(item_tree3)

        final_item_tree = item_tree3

        final_item_tree["panelUrl"] = row[header_idx["链接地址"]]
        final_item_tree["panelImgUrls"] = []
        if len(row[header_idx["系统截图链接"]]) > 0:
            final_item_tree["panelImgUrls"] = row[header_idx["系统截图链接"]].split("\n")
        if len(final_item_tree["panelImgUrls"]) > 0:
            final_item_tree["panelImgUrl"] = final_item_tree["panelImgUrls"][0]

        final_item_tree["sketchUrls"] = []
        if len(row[header_idx["图片链接"]]) > 0:
            final_item_tree["sketchUrls"] = row[header_idx["图片链接"]].split("\n")
        if len(final_item_tree["sketchUrls"]) > 0:
            final_item_tree["sketchUrl"] = final_item_tree["sketchUrls"][0]

        final_item_tree["is32"] = False
        if row[header_idx["是否为32:9"]] == "是":
            final_item_tree["is32"] = True
        final_item_tree["click"] = False
        if row[header_idx["点击"]] == "是":
            final_item_tree["click"] = True
        row[header_idx["排序号"]] = row[header_idx["排序号"]].strip()
        if len(row[header_idx["排序号"]]) > 0:
            try:
                sortNumber = int(row[header_idx["排序号"]])
                final_item_tree["sortNumber"] = sortNumber
            except Exception as e:
                print(e)

s = json.dumps(tree, ensure_ascii=False)
# print(s)

with open("screenURL.json", "w") as f:
    f.write(s)

if len(sys.argv) > 2:
    print("do data update in "+sys.argv[2])
    if sys.argv[2] == "datam":
        # ------------------ #
        # 如有变更，请手动更新
        host = "http://39.170.15.45:8311"
        oid = "0908c70c-8139-4299-a2d2-28052a2810bf"
        # 如有变更，请手动更新
        # ------------------ #
        x = requests.post(
            host + "/access-manager/auth/login",
            json={
                "account": "qiangqiang",
                "password": "28634125dd2a76f56054e8415992b9f9523104a0171660cf6e01978c729016aa",
                "encoding": "hex",
            },
        )
        token = x.json()["data"]["access_token"]
        x = requests.post(
            host + "/data-manager/dataset/" + oid + "/update",
            json={"content": tree, "update_mode": "overwrite"},
            headers={"Authorization": "Bearer " + token},
        )
        print(x.json())
    elif sys.argv[2] == "css":
        # ------------------ #
        # 如有变更，请手动更新
        host = "http://10.162.12.144"
        resultIndexId = "13"
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
