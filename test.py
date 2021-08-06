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
    tem_url ='^'+'https://baike.baidu.com{}'.format(pageurl)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('head').find_all('link',href=re.compile('^https://baike.baidu.com(.*)')):
            a.append(link)
    sstr = str(link)
    num = re.findall(r"baidu.com(.+?)\"", sstr[5:100])

    return num[0]


#'/item/%E5%AD%94%E5%AD%90/1584'
def main():
    global pages
    pages = []
    global name
    name = []

    find_name = '刘德华'
    get_ = '/item/' + find_name
    find_name_url = 'https://baike.baidu.com{}'.format(urllib.parse.quote(get_))
    link =get_pri_url(urllib.parse.quote(get_), find_name)



    print(link)



if __name__ == "__main__":
    main()
