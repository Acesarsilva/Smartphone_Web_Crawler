import pandas as pd
import util
import pickle
import nltk
import csv
import time
from bs4 import BeautifulSoup

def main():
    nltk.download('stopwords')
    stopwords_br = nltk.corpus.stopwords.words('portuguese')
    stopwords_en = nltk.corpus.stopwords.words('english')
    start_links = pd.read_csv('start_links.csv')['links'].tolist()
    downloaded_url = []
    border = [(x,0) for x in start_links]
    model = pickle.load(open('random_forest.pk', 'rb'))
    vocabulary = pickle.load(open('vocabulary.pk','rb'))
    n_links = 1000
    count = 0
    f = open('smartphone_links.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(["smartphone_links"])
    while(n_links > 0 and border):
        url = border.pop(0)[0]
        if ((url not in downloaded_url) and url.find('/e/') == -1):
            try:
                html = util.download_url(url)
                links = util.get_links(html,url)
                border.extend(links)
                #border.sort(key=lambda x:x[1], reverse=True)
                data = util.pre_processor_model_page(BeautifulSoup(html,'lxml').get_text(),vocabulary,stopwords_en,stopwords_br)
                pred = model.predict(data)
                count += pred[0]
                if(pred[0] == 1):
                    writer.writerow([url])
                downloaded_url.append(url)
                #time.sleep(1)
                print(n_links)
            except:
                print('Bad Download:', url)
                #border.append((url,0))
            
            n_links -= 1
    
    f.close()
    return count

if __name__ == "__main__":
    print(main())