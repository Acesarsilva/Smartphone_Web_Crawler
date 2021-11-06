from urllib.request import urlopen
from bs4 import BeautifulSoup

def download_url(url):
    return urlopen(url).read().decode('utf-8')

def get_links(html,url):
    links = []
    soup = BeautifulSoup(html,'lxml')
    for link in soup.find_all('a'):
        print(link.text)
        link = link.get('href')
        if(link and link != url and link[0:5] == 'https'):
            links.append(link)
    
    return links

def ranker(url):
    return 0