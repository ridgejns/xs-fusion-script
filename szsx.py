# -- coding:UTF-8 --
'''
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-08 02:15:12
LastEditTime: 2023-06-08 03:00:41
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
'''
import csv
import json
import random

depts = ["智慧交通","数字公安","智慧消防","数字城管"]
cs = []
for i, dept in enumerate(depts):
    c = {      
            "category": "实战实效",
            "label": "任务监测",
            "department": dept,
            "ai_num":random.randint(400, 1000),
            "event_num":random.randint(50, 80),
      }
    c["raito"]="%.2f"%(c["event_num"]/c["ai_num"])
    cs.append(c)

s = json.dumps(cs, ensure_ascii=False)
print(s)
