import requests
import os
import re
import time

# https://www.google.com/search?tbm=isch&q=chinese
FirstUrl = "https://baozougif.com"
history = []

# 下载图片
def downloadPicture(content):
    pattern = re.compile(r'(http[s]*://[\S]*\.(gif))')
    pictureUrlList = pattern.findall(content)
    # print(*pictureUrlList, sep="\n")

    chunkSize = 1024 * 64

    for pictureSet in pictureUrlList:
        picUrl = pictureSet[0]
        try:
            downloadReq = requests.get(picUrl, stream=True, timeout=10)
        except requests.ConnectionError as error:
            print("download error ", error)
            continue

        fileName = picUrl.split('/')[-1]

        # 下载片段计时
        startTime = time.time()

        with open(fileName, 'wb') as f:
            for chunk in downloadReq.iter_content(chunk_size=chunkSize):
                chunkTime = time.time() - startTime
                if chunkTime > 10:
                    print("download timeout %fs" %chunkTime)
                    break
                if chunk:
                    f.write(chunk)

#获取详情页
def findDetailHtml(url):
    try:
        r = requests.get(url, timeout=10)
    except requests.ConnectionError as error:
        print("request error ", error)
        return
    responseText = r.text
    pattern = re.compile(r'(http[s]*://[\S]*\.html)')
    detailUrlList = pattern.findall(responseText)
    
    for detailUrl in detailUrlList:
        # 判断是否加载过该详情页
        if detailUrl in history:
            continue
#        print("current url = " + detailUrl)
        try:
            detailRequest = requests.get(detailUrl, timeout=10)
        except requests.ConnectionError as error:
            print("request error ", error)
            continue
        detailResponse = detailRequest.text
        # 下载该详情页图片
        downloadPicture(detailResponse)
        # 记录详情页
        history.append(detailUrl)
        # 递归查找详情页
        findDetailHtml(detailUrl)

findDetailHtml(FirstUrl)

