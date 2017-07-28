import gzip
from urllib import request

import appJar
from bs4 import BeautifulSoup

URL1 = "https://www.amazon.com/gp/search/ref=sr_il_to_mobile?fst=as%3Aon&rh=k%3A"
URL2 = "%2Cn%3A2335752011%2Cn%3A2407760011%2Cn%3A3081461011&lo=none"


def get_search_result(key, i):
    key = key.replace(" ", "+")
    page = "&page=" + str(i)
    url = URL1 + key + URL2 + "&keywords=" + key + page
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.amazon.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    my_request = request.Request(url=url, headers=headers)
    res = request.urlopen(my_request, timeout=20)
    html = res.read()
    data = gzip.decompress(html)
    data = str(data, 'utf-8')
    soup = BeautifulSoup(data, "html.parser")
    items = soup.select("div.s-item-container")
    result = ""
    if items:
        print(len(items))
        for item in items:
            if item.find(text="Sponsored"):
                result += "Sponsored    "
            else:
                result += "     "
            result += item.h2.text + '    '
            result += item.h2.find_next("div").text + '    '
            price = item.select("span.a-offscreen")
            if price:
                result += price[0].text + '    '
            else:
                price = item.select("span['aria-label']")
                result += price[0]['aria-label'] + '    '
            star = item.select("i.a-icon-star span.a-icon-alt")
            if star:
                result += star[0].text + '    '
                result += star[0].find_next('a').text
            result += '\n\n'
    return result, url


def search_key(app):
    key = app.getEntry("key")
    i = 1
    get_next = True
    fl = open(key + '.txt', 'wb')
    while get_next:
        message, url = get_search_result(key, i)
        if message == "":
            app.errorBox("没了", "上一页是最后一页")
            get_next = False
        else:
            fl.write(message.encode(errors='ignore'))
            get_next = app.yesNoBox("第" + str(i) + "页", url + "\n\n继续抓取下一页？")
        i += 1
    fl.close()


def main():
    def search(bt):
        search_key(app)

    app = appJar.gui("晓狗")
    app.setGuiPadding(30, 30)
    app.addLabel("key", "搜索词", 0, 0, 1, 1)
    app.addEntry("key", 0, 1, 1, 1)
    app.addButton("开始", search, 1, 0, 2, 1)
    app.go()


main()
