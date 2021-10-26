from urllib.request import urlopen
import pandas as pd

def download_url(url):
    return urlopen(url).read().decode('utf-8')

def get_links(html):
    return 0

def ranker(url):
    return 0

if __name__ == "__main__":
    start_links = pd.read_csv('start_links.csv')['links'].tolist()
    print(start_links)
    downloaded_url = []
    controler = start_links
    while(controler):
        url = controler.pop(0)
        if (url not in downloaded_url):
            try:
                html = download_url(url)
                downloaded_url.append(url)
                #call html classifier
                links = get_links(html)
                controler.append(links)
                print(downloaded_url)
            except:
                print('Bad Download: ', url)