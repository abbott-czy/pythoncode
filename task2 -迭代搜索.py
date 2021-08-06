import re
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup


def get_pri_url(pageurl, find_name):
    a = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    html = urlopen(urllib.request.Request('https://baike.baidu.com{}'.format(pageurl), headers=headers))
    tem_url = '^' + 'https://baike.baidu.com{}'.format(pageurl)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('head').find_all('link', href=re.compile('^https://baike.baidu.com(.*)')):
        a.append(link)
    sstr = str(link)
    num = re.findall(r"baidu.com(.+?)\"", sstr[5:100])

    return num[0]


def getLink(pageurl, find_name):
    tem_relation = []
    tem_name = []
    tem_url1 = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    print('https://baike.baidu.com{}'.format(pageurl))
    html = urlopen(urllib.request.Request('https://baike.baidu.com{}'.format(pageurl), headers=headers))
    bs = BeautifulSoup(html, 'html.parser')
    flag = []

    try:
        for link in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('a',
                                                                                         href=re.compile('^(/item/)')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    flag.append(1)
                    newpage = link.attrs['href']
                    pages.append(newpage)
                    tem_url1.append("https://baike.baidu.com" + newpage)
                else:
                    flag.append(0)
        print(tem_url1)
        tem = 0
        for text in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('span', {'class': 'title'}):
            if flag[tem]:
                name.append(text.get_text())
                tem_name.append(text.get_text())
            else:
                pass
            tem = tem + 1
        print(tem_name)
        tem1 = 0
        for text in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('span', {'class': 'name'}):
            if flag[tem1]:
                tem_relation.append((text.get_text()))
            else:
                pass
            tem1 = tem1 + 1
        print(tem_relation)

        # print(len(name))


    except:
        print("经查询 %s 未查到人物关系! " % (find_name))
        print("即将为您查询明星关系\n")

    try:
        if len(tem_relation) == 0 | len(tem_name) == 0:
            flag = []
            for link in bs.find('div', {'class': 'star-info-block relations'}).find_all('a',
                                                                                        href=re.compile(
                                                                                            '^(/item/)')):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        flag.append(1)
                        newpage = link.attrs['href']
                        pages.append(newpage)
                        tem_url1.append("https://baike.baidu.com" + newpage)
                    else:
                        flag.append(0)
                print(tem_url1)
            tem = 0
            for i in bs.find('div', {'class': 'star-info-block relations'}).find_all('em'):
                if tem == 0:
                    pass
                else:
                    if flag[tem - 1]:
                        name.append(i.get_text())
                        tem_name.append(i.get_text())
                tem = tem + 1
            print(tem_name)
            tem1 = 0
            for i in bs.find('div', {'class': 'star-info-block relations'}).find_all('div', {'class': 'name'}):
                if flag[tem1]:
                    tem_relation.append(i.contents[0])
                else:
                    pass
                tem1 = tem1 + 1
            print(tem_relation)
            # while (temp < len(tag)):
            #    relation.append(tag[temp][:int(len(tag[temp]) - int(len(name[temp])))])
            #    temp = temp + 1
            # print(relation)

    except:
        print("经查询 %s 未查到明星关系！ " % (find_name))

    return tem_relation, tem_name, tem_url1


def save_txt(find_name, find_name_url, relation, url1):
    with open('./人物/' + find_name + '.txt', "w", encoding='utf-8') as f:
        for m, n in zip(relation, url1):
            f.writelines(str("%s,%s,%s" % (find_name_url, m, n)) + '\n')


def save_graph(find_name, find_name_url, relation, url1):
    with open('./人物迭代/' + find_name + '.txt', "w", encoding='utf-8') as f:
        for m, n in zip(relation, url1):
            f.writelines(str("%s,%s,%s" % (find_name_url, m, n)) + '\n')


def main():
    global pages
    pages = []
    global name
    name = []
    find_name = '刘德华'
    get_ = '/item/' + find_name
    find_name_url = get_pri_url(urllib.parse.quote(get_), find_name)
    # link =get_pri_url(urllib.parse.quote(get_), find_name)
    print(get_)
    print(format(urllib.parse.quote(get_)))
    pages.append(find_name_url)
    name.append(find_name)
    tem_relation, tem_name, tem_url1 = getLink(urllib.parse.quote(get_), find_name)
    if len(tem_relation) | len(tem_name):
        # save_txt(find_name, relation, name)
        save_graph(find_name, find_name_url, tem_relation, tem_url1)
    tem = 1
    while True:
        # try:
        if pages[tem]:
            tem_relation, tem_name, tem_url1 = getLink(pages[tem], name[tem])
            save_name_url = 'https://baike.baidu.com' + pages[tem]
            save_graph(find_name, save_name_url, tem_relation, tem_url1)
            print("人物name有")
            print(name)
            print(pages)
        tem = tem + 1
        if (tem == len(pages)):
            return
    # except:
    # print("迭代结束")
    # return


if __name__ == "__main__":
    main()

