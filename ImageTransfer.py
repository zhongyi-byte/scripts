#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author     : codekiller
# @Time       : 2022/2/13 20:42
# @Email      : jcl1345414527@163.com
# @File       : MdImage.py
# @Description: 用来进行md文件中图片的获取，保存在本地，并修改md文件。只需要修改ua和文件的位置就行了
import os
import re
import string

import requests
import time

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
     "(KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
headers = {"User-Agent": ua}

# 文件的位置
file_root = r'/Users/chuyan/Zyi-hugoBlog/'
file_dir = 'content/posts/tech/'
file_n = 'Lucene学习笔记'
file_suffix = '.md'
fileName = file_root + file_dir + file_n + file_suffix

# 存储图片的位置
img_tsrc = file_root + "assets/img/"
img_src = img_tsrc + file_n

if not os.path.exists(img_src):
    os.mkdir(img_src)

with open(file=fileName, mode="r", encoding='utf-8') as f1:
    # 用来计数
    s_count = 0
    fail_count = 0
    sus_count = 0

    lines = f1.readlines()
    for i in range(0, len(lines)):
        url = re.findall('!\[image\]\(.*?\)', lines[i], re.S)
        if len(url) != 0:
            # TODO 这里很笨的方法截取出了url，以后优化为直接正则识别出url
            url = url[0]
            url = url[9:]
            url = url[:len(url) - 1]
            # 处理本地图片
            if len(re.findall(img_tsrc + '.*', url, re.S)) != 0:
                print('第', i, '行：为本地图片')
                s_count += 1
                continue

            # 获取时间作为图片文件名
            timestamp = int(time.time())
            image_name = str(time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))) + str(i) + ".png"

            # 请求图片
            img = requests.get(url, headers=headers)
            # 判断是否获取
            if img.status_code != 200:
                print('第', i, '行：', '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',
                      img.status_code)
                fail_count += 1
                continue

            # 存储
            target = open(img_src + '/' + image_name, 'ab')
            target.write(img.content)
            target.close()
            lines[i] = lines[i].replace(url, img_src + '/' + image_name)
            print('第', i, '行：', url + '成功转为' + img_src + '/' + image_name)
            sus_count += 1
    print('---本地图片为：', s_count, '个---')
    print('---获取失败为：', fail_count, '个---')
    print('---转化成功为：', sus_count, '个---')
    if sus_count == 0:
        os.rmdir(img_src)

# 将处理过的cNames写入新的文件中
fileName2 = file_dir + file_n + '-修改' + file_suffix
with open(file=fileName2, mode='w', encoding='utf-8') as f2:
    f2.writelines(lines)
