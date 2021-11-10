from urllib.request import urlopen
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import unicodedata

def download_url(url):
    return urlopen(url,timeout=1.0).read().decode('utf-8')

def get_links(html,url):
    links = []
    soup = BeautifulSoup(html,'lxml')
    for link in soup.find_all('a'):
        link = link.get('href')
        if(link and link != url and link[0:5] == 'https'):
            links.append((link, ranker(link)))
    
    return links

def ranker(url):
    domain_words = {"smartphone","celular", "smartphones", "celulares", "samsung", "apple","motorola","xiaomi", "android", "ios", "galaxy", "moto", "lenovo", "tela", "zenfone", "lg", "telefone","asus","camera","core","mobile","phone","phones"}
    counter = 0
    for word in domain_words:
        if url.lower().find(word) != -1:
            counter += 1
    return counter

def pre_processor_model_page(txt,stopwords_en,stopwords_br):

    txt_nfkd = ' '.join(unicodedata.normalize('NFKD', txt).lower().replace('_',' ').replace('!',' ').replace('<',' ').replace('>',' ').replace("'"," ").replace('/',' ').replace('|',' ').replace('?',' ').replace('"',' ').replace('=',' ').replace(';',' ').replace(':',' ').replace('+',' ').replace('-',' ').replace('-',' ').replace('.',' ').replace(',',' ').replace('@',' ').replace('#',' ').replace('$',' ').replace('%',' ').replace('&',' ').replace('*',' ').replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' '). replace('}',' ').split()) 
    txt_remove_accents = txt_nfkd.encode('ASCII', 'ignore').decode('ascii')

    txt_backup = " ".join([word for word in str(txt_remove_accents).split() if (word not in stopwords_br and len(word) >= 3)])
    txt_remove_stopword = " ".join([word for word in str(txt_backup).split() if (word not in stopwords_en and len(word) >= 3)])

    text_final = " ".join([word for word in str(txt_remove_stopword).split() if (word.isalpha())])

    text_bow = CountVectorizer()
    data = text_bow.fit_transform([text_final])

    df_bow = pd.DataFrame(data.toarray(),columns=text_bow.get_feature_names())
    return df_bow