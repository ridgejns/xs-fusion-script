# -- coding:UTF-8 --
'''
Descripttion: 
Author: Lyu Yaopengfei, lypf@citycloud.com.cn
Date: 2023-06-13 16:59:16
LastEditTime: 2023-06-13 18:35:18
Copyright: (c) 2023 citycloud.com.cn All Rights Reserved.
'''
import json
import re
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup


class TengXunDocument():

    def __init__(self, document_url, local_pad_id, cookie_value):
        # excel文档地址
        self.document_url = document_url
        # 此值每一份腾讯文档有一个,需要手动获取
        self.localPadId = local_pad_id
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Cookie': cookie_value
        }

    def get_now_user_index(self):
        """
        # 获取当前用户信息,供创建下载任务使用
        :return:
            # nowUserIndex = '4883730fe8b94fbdb94da26a9a63b688'
            # uid = '144115225804776585'
            # utype = 'wx'
        """
        response_body = requests.get(url=self.document_url, headers=self.headers, verify=False)
        parser = BeautifulSoup(response_body.content, 'html.parser')

        parser_str = str(parser)
        parser_str = parser_str.replace(" ", "")
        parser_str = parser_str.replace("\n", "")
        global_multi_user_list = re.findall(re.compile('window.global_multi_user=(.*?);'), parser_str)
        if global_multi_user_list:
            user_dict = json.loads(global_multi_user_list[0])
            print(user_dict)
            return user_dict['nowUserIndex']
        return 'cookie过期,请重新输入'

    def export_excel_task(self, export_excel_url):
        """
        导出excel文件任务,供查询文件数据准备进度
        :return:
        """
        body = {
            'docId': self.localPadId, 'version': '2'
        }

        res = requests.post(url=export_excel_url,
                                      headers=self.headers, data=body, verify=False)
        operation_id = res.json()['operationId']
        return operation_id



    def download_excel(self, check_progress_url, file_name):
        """
        下载excel文件
        :return:
        """
        # 拿到下载excel文件的url
        start_time = time.time()
        file_url = ''
        while True:
            res = requests.get(url=check_progress_url, headers=self.headers, verify=False)
            progress = res.json()['progress']
            if progress == 100:
                file_url = res.json()['file_url']
                break
            elif time.time() - start_time > 30:
                print("数据准备超时,请排查")
                break
        if file_url:
            self.headers['content-type'] = 'application/octet-stream'
            res = requests.get(url=file_url, headers=self.headers, verify=False)
            with open(file_name, 'wb') as f:
                f.write(res.content)
            print('下载成功,文件名: ' + file_name)
        else:
            print("下载文件地址获取失败, 下载excel文件不成功")


if __name__ == '__main__':
    # excel文档地址
    document_url = 'https://docs.qq.com/sheet/DS3ZlYnlmSk10ZENI'
    # 此值每一份腾讯文档有一个,需要手动获取
    local_pad_id = '300000000$KvebyfJMtdCH'
    # 打开腾讯文档后,从抓到的接口中获取cookie信息
    cookie_value = 'traceid=c11c99648f; TOK=c11c99648f873ca9; hashkey=c11c9964; fingerprint=89b58a0d129d4e50bb5b11c9413a1df997; ES2=fef23716faa30c9c; low_login_enable=1; wx_appid=wxd45c635d754dbf59; openid=oDzL40FezocDlXqBEStsUP6jURBE; access_token=69_9Z_1zwzM3gQ91iRS-s6OZomwFkdl6iI50IjEDVRZwkdfla9UsxYKcQ_wRqkf6VfuumFZ6mxJLnFC06MBDtpWVHBMIdcQn1iyk9GQzYIVRig; refresh_token=69_zodFGeaeXucVcmXyDuHtAEzKUwiI_PcvXiaGMtLi-FZhOCNeqE_pvNV4bKVb-CexerEcs4JN-JH_nlschVItmBQ9d0kEUgbNlMPq5n-tCWI; DOC_SID=63413c26178f442b82ee0e4b0895083f0dc02576095844988b79120a0d33ba26; SID=63413c26178f442b82ee0e4b0895083f0dc02576095844988b79120a0d33ba26; loginTime=1686563883136'
    tx = TengXunDocument(document_url, local_pad_id, cookie_value)
    now_user_index = tx.get_now_user_index()
    # # 导出文件任务url
    export_excel_url = f'https://docs.qq.com/v1/export/export_office?u={now_user_index}'
    # # 获取导出任务的操作id
    operation_id = tx.export_excel_task(export_excel_url)
    check_progress_url = f'https://docs.qq.com/v1/export/query_progress?u={now_user_index}&operationId={operation_id}'
    current_datetime = datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S')
    file_name = f'{current_datetime}.xlsx'
    tx.download_excel(check_progress_url, file_name)


