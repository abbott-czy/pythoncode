import re
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup

pages = set()


def getLink(pageurl):
    global pages
    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"

    }
    print('https://baike.baidu.com{}'.format(pageurl))
    html = urlopen(urllib.request.Request('https://baike.baidu.com{}'.format(pageurl), headers=headers))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        for text in bs.find('div', {'class': 'lemma-summary'}).find_all('div', {'class': 'para'}):
            print(text.get_text())
        '''for link in bs.find('div', {'class': 'para'}).find_all('a'):
            if 'href' in link.attrs:
                print(link.attrs['href'])
            else:
                print('-----非链接-----')
                print(link)
                print('-----非链接-----')'''
    except AttributeError:
        print("yemianqieshaoshuxing")

    for link in bs.find('div', {'class': 'para'}).find_all('a', href=re.compile('^(/item/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newpage = link.attrs['href']
                print('-' * 20)

                print(newpage)
                pages.add(newpage)
                getLink(newpage)






def  main():
    get_ = '/item/刘德华'
    print(get_)
    getLink(urllib.parse.quote(get_))


if __name__ == "__main__":
    main()