# -- coding:UTF-8 --
'''
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-08 00:40:02
LastEditTime: 2023-06-08 01:11:07
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
'''
import csv
import json

filename='./第五立面匹配结果_x.csv'

ffs = []
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    headers = next(csv_reader)  # 读取第一行每一列的标题
    print(headers)
    header_idx = {}
    for i, h in enumerate(headers):
        header_idx[h] = i
    for i, row in enumerate(csv_reader):  # 将csv 文件中的数据保存到data中
        if row[header_idx["file_path"]] == "":
            continue
        ff = {
            "index": i,
            "file_path": row[header_idx["file_path"]],
            "address_remark": row[header_idx["address_remark"]],
            "uni_address": row[header_idx["uni_address"]],
            "lng": row[header_idx["lng"]],
            "lat": row[header_idx["lat"]],
        }
        if len(row[header_idx["address_remark"]])>0:
            ff["imgs"]=["http://195.195.8.83/fusionFile/facade/"+row[header_idx["address_remark"]]+"_"+row[header_idx["lng"]]+"_"+row[header_idx["lat"]]+".jpg"]
        # print(ff)
        ffs.append(ff)

s = json.dumps(ffs, ensure_ascii=False)
print(s)