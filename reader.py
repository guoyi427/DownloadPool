import requests
import re

FirstUrl = "http://news.baidu.com"

UrlHistoryList = []

def analysisContent(responseText):
    quotationPattern = re.compile(r"(>[^ \f\n\r\t\v>]*[\u4e00-\u9fff]{5,}[^ \f\n\r\t\v<]*<)")
    quotationList = quotationPattern.findall(responseText)
    print(*quotationList, sep="\n")

def loadHtml(url):
    print("current url", url)
    if url in UrlHistoryList:
        print("mutiply url")
        return
    try:
        r = requests.get(url, timeout=5)
    except requests.ConnectionError as error:
        print("load detail error", error)
        return
    responseText = r.text
    UrlHistoryList.append(url)
    # 解析内容
    analysisContent(responseText)

    # 找到这个页面内的链接 递归加载
    pattern = re.compile(r'("http[s]*://[^ \f\n\r\t\vhttp]+")')
    resultList = pattern.findall(responseText)
    for detailUrl in resultList:
        replaceUrl = detailUrl.replace("\"", "")
        loadHtml(replaceUrl)

loadHtml(FirstUrl)