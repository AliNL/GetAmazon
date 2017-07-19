import appJar
from urllib import request
from bs4 import BeautifulSoup

URL = "https://www.amazon.com/gp/search/ref=sr_il_to_mobile?fst=as%3Aon&rh=%2Cn%3A3081461011"
START = '<ul i'
END = 'v></div></li></ul>'


def get_search_result(key, i):
    key = "&keywords=" + key.replace(" ", "+")
    page = "&page=" + str(i)
    url = URL + key + page
    res = request.urlopen(url)

    # res = request.urlopen("https://www.amazon.com/gp/search/ref=sr_il_to_mobile?fst=as%3Aon&rh=%2Cn%3A3081461011&keywords=iphone+6+case&page=2")
    html = str(res.read())
    start = html.find(START)
    end = html.find(END) + len(END)
    html = html[start:end]
    soup = BeautifulSoup(html, "html.parser")

    return html


def search(app):
    key = app.getEntry("key")
    i = 1
    get_next = True
    while get_next:
        message = get_search_result(key, i)
        get_next = app.yesNoBox("第" + i + "页", message)
        i += 1


def main():
    app = appJar.gui("晓狗")
    app.setGuiPadding(30, 30)
    app.addLabel("key", "搜索词", 0, 0, 1, 1)
    app.addEntry("key", 0, 1, 1, 1)
    app.addButton("开始", search(app), 1, 0, 2, 1)
    app.go()


main()
