# -*- coding: UTF-8 -*-
# Time : 2024/6/29 下午4:29
# FILE : test.py
# PROJECT : myFilter
# Author : kkk

from urllib.parse import urlparse


url = "./node_modules/@xkit-yx/im-kit-ui/es/chat/components/ChatSettingDrawer/style/index.js"

# 获取待操作url
with open("./url.txt", encoding="utf-8") as fp:
    content = fp.read().strip()
    url_list = content.split('\n')

for url in url_list:
    parse_uri = urlparse(url)

    print(parse_uri)
