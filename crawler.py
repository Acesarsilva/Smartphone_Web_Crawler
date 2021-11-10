import pandas as pd
import util
import pickle
import nltk
import socket
import urllib
from bs4 import BeautifulSoup

def main():
    nltk.download('stopwords')
    stopwords_br = nltk.corpus.stopwords.words('portuguese')
    stopwords_en = nltk.corpus.stopwords.words('english')
    start_links = pd.read_csv('start_links.csv')['links'].tolist()
    downloaded_url = []
    border = [(x,0) for x in start_links]
    model = pickle.load(open('model_perceptron', 'rb'))
    n_links = 1000
    while(n_links > 0 and border):
        url = border.pop(0)[0]
        if (url not in downloaded_url):
            try:
                html = util.download_url(url)
                links = util.get_links(html,url)
                border.extend(links)
                #border.sort(key=lambda x:x[1], reverse=True)
                data = util.pre_processor_model_page(BeautifulSoup(html,'lxml').get_text(),stopwords_en,stopwords_br)
                pred = model.predict(data)
                downloaded_url.append(url)
                n_links -= 1
            except:
                print('Bad Download: ', url)
                border.append((url,0))

if __name__ == "__main__":
    main()