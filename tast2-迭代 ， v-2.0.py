import re
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup

pages = []
name = []
relation = []
url1 = []


def getLink(pageurl, find_name):
    global generation
    global relation
    global name
    global url1
    global pages
    if generation <=5:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
        }
        print('https://baike.baidu.com{}'.format(pageurl))
        html = urlopen(urllib.request.Request('https://baike.baidu.com{}'.format(pageurl), headers=headers))
        bs = BeautifulSoup(html, 'html.parser')

        try:
            flag_who = []
            sum_who =0
            for text in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('span', {'class': 'title'}):
                if text.get_text() in name:
                    flag_who.append(0)
                else:
                    name.append(text.get_text())
                    flag_who.append(1)
                sum_who = sum_who +1
            print(name)
            #print(flag_who)
            tem = 0
            for text in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('span', {'class': 'name'}):
                if flag_who[tem] == 1 :
                    relation.append(text.get_text())
                tem = tem +1

            print(relation)
            for link in bs.find('div', {'class': 'lemma-relation-module viewport'}).find_all('a',
                                                                                             href=re.compile('^(/item/)')):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        newpage = link.attrs['href']
                        url1.append("https://baike.baidu.com" + newpage)
                        generation = generation+1
                        getLink(newpage, "测试")

            print(url1)

        except:
            print("经查询 %s 未查到人物关系! " % (find_name))
            print("即将为您查询明星关系\n")

        try:
            if len(relation) == 0 | len(name) == 0:
                for i in bs.find('div', {'class': 'star-info-block relations'}).find_all('div', {'class': 'name'}):
                    relation.append(i.contents[0])
                print(relation)
                for i in bs.find('div', {'class': 'star-info-block relations'}).find_all('em'):
                    name.append(i.get_text())
                del (name[0])
                print(name)
                for link in bs.find('div', {'class': 'star-info-block relations'}).find_all('a',
                                                                                            href=re.compile('^(/item/)')):
                    if 'href' in link.attrs:
                        if link.attrs['href'] not in pages:
                            newpage = link.attrs['href']
                            url1.append("https://baike.baidu.com" + newpage)

                print(url1)
        except:
            print("经查询 %s 未查到明星关系！ " % (find_name))

    else:
        return



def save_txt(find_name, find_name_url, relation, url1):
    with open('./人物迭代/' + find_name + '.txt', "w", encoding='utf-8') as f:
        for m, n in zip(relation, url1):
            f.writelines(str("%s,%s,%s" % (find_name_url, m, n)) + '\n')


def main():
    find_name = '孔子'
    get_ = '/item/' + find_name
    find_name_url = 'https://baike.baidu.com{}'.format(urllib.parse.quote(get_))
    print(get_)
    global generation
    generation = 0
    getLink(urllib.parse.quote(get_), find_name)
    if len(relation) | len(name):
        # save_txt(find_name, relation, name)
        save_txt(find_name, find_name_url, relation, url1)



if __name__ == "__main__":
    main()


#  document.querySelector("#J-lemma-relation-module")
#  document.querySelector("#J-lemma-relation-module > ul > li:nth-child(1) > a > div")
#  document.querySelector("#J-lemma-relation-module > ul > li:nth-child(1) > a > div > span.name")
#  document.querySelector("#J-lemma-relation-module > ul > li:nth-child(1) > a > div > span.title")
# // *[ @ id = "J-lemma-relation-module"] / ul / li[1] / a / div
# /html/body/div[3]/div[2]/div/div[1]/div[7]/div[3]/ul/li[1]/a/div/span[1]
# /html/body/div[3]/div[2]/div/div[1]/dl[1]/dd/h1
# document.querySelector("body > div.body-wrapper > div.content-wrapper > div > div.main-content.J-content > dl.lemmaWgt-lemmaTitle.lemmaWgt-lemmaTitle- > dd > h1")
