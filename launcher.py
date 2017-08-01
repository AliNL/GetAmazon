import gzip
from urllib import request

import appJar
from bs4 import BeautifulSoup

URL_COM_1 = "https://www.amazon.com/gp/search/ref=sr_il_to_mobile?fst=as%3Aon&rh=k%3A"
URL_COM_2 = "%2Cn%3A2335752011%2Cn%3A2407760011%2Cn%3A3081461011&lo=none"
URL_DE = "https://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords="
URL_UK = "https://www.amazon.co.uk/s/ref=nb_sb_noss_2/261-4880887-8776658?url=search-alias%3Daps&field-keywords="
URL_JP = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2/358-9024954-2951136?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords="


def get_search_result(base, key, i):
    key = key.replace(" ", "+")
    page = "&page=" + str(i)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    if base == "美国":
        url = URL_COM_1 + key + URL_COM_2 + "&keywords=" + key + page
        headers['Host'] = 'www.amazon.com'
    elif base == "德国":
        url = URL_DE + key + page
        headers['Host'] = 'www.amazon.de'
    elif base == "英国":
        url = URL_UK + key + page
        headers['Host'] = 'www.amazon.co.uk'
    else:
        url = URL_JP + key + page
        headers['Host'] = 'www.amazon.co.jp'
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
            if item.h5:
                result += item.h5.contents[0] + "    "
            else:
                result += "     "
            result += item.h2.text + '    '
            result += item.h2.find_next("div").text + '    '
            # price = item.select("span.a-offscreen")
            price = item.h2.find_next("a")
            if 'aria-label' in price.span.attrs:
                result += price['aria-label'] + '    '
            else:
                result += price.text + '    '
            star = item.select("i.a-icon-star span.a-icon-alt")
            if star:
                result += star[0].text + '    '
                result += star[0].find_next('a').text
            result += '\n\n'
    return result, url


def search_key(app):
    base = app.getOptionBox("base")
    key = app.getEntry("key")
    page = app.getEntry("page")
    i = int(page)
    get_next = True
    fl = open(key + base + '.txt', 'wb')
    while get_next:
        message, url = get_search_result(base, key, i)
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
    app.addLabel("base", "网站", 0, 0, 1, 1)
    app.addOptionBox("base", ["美国", "德国", "英国", "日本"], 0, 1, 1, 1)
    app.addLabel("key", "搜索词", 1, 0, 1, 1)
    app.addEntry("key", 1, 1, 1, 1)
    app.addLabel("page", "开始页", 2, 0, 1, 1)
    app.addNumericEntry("page", 2, 1, 1, 1)
    app.setEntry("page", "1")
    app.addButton("开始", search, 3, 0, 2, 1)
    app.go()


main()
