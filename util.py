from urllib.request import urlopen
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import unicodedata
import math

def download_url(url):
    return urlopen(url,timeout=3).read().decode('utf-8')

def get_links(html,url):
    links = []
    soup = BeautifulSoup(html,'lxml')
    for link in soup.find_all('a'):
        anc = link.text
        link = link.get('href')
        if(link and link != url and link[0:5] == 'https'):
            links.append((link, ranker(anc),anc))
    
    return links

def ranker(url):
    domain_words = {"smartphone","celular", "samsung", "apple","motorola","xiaomi", "ios", "galaxy", "moto", "lenovo", "tela", "zenfone", "lg", "telefone","asus","camera","core","mobile","phone","cell", "bateria", "memory", "pixel"}
    counter = 0
    for word in domain_words:
        if url.lower().find(word) != -1:
            counter += 1
    return counter

def pre_processor_model_page(txt,vocabulary,stopwords_en,stopwords_br):

    txt_nfkd = ' '.join(unicodedata.normalize('NFKD', txt).lower().replace('_',' ').replace('!',' ').replace('<',' ').replace('>',' ').replace("'"," ").replace('/',' ').replace('|',' ').replace('?',' ').replace('"',' ').replace('=',' ').replace(';',' ').replace(':',' ').replace('+',' ').replace('-',' ').replace('-',' ').replace('.',' ').replace(',',' ').replace('@',' ').replace('#',' ').replace('$',' ').replace('%',' ').replace('&',' ').replace('*',' ').replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' '). replace('}',' ').split()) 
    txt_remove_accents = txt_nfkd.encode('ASCII', 'ignore').decode('ascii')

    txt_backup = " ".join([word for word in str(txt_remove_accents).split() if (word not in stopwords_br and len(word) >= 3)])
    txt_remove_stopword = " ".join([word for word in str(txt_backup).split() if (word not in stopwords_en and len(word) >= 3)])

    text_final = " ".join([word for word in str(txt_remove_stopword).split() if (word.isalpha())])

    text_bow = CountVectorizer(vocabulary=vocabulary)
    data = text_bow.fit_transform([text_final])

    df_bow = pd.DataFrame(data.toarray(),columns=text_bow.get_feature_names())
    return df_bow

def cossine_similarity(query,document):
    xx, xy, yy = 0,0,0
    for d in range(len(query)):
        x = query[d]
        y = document[d]
        xx += x*x
        xy += x*y
        yy += y*y

    return (xy/math.sqrt(xx*yy))

def spearman(rank1, rank2):
    n = len(rank1)
    rank1_pos = [-1]*n
    rank2_pos = [-1]*n
    for x in range(n):
        rank1_pos[rank1[x]-1] = x
        rank2_pos[rank2[x]-1] = x
    
    sum_of_square_dist = 0
    for x in range(n):
        sum_of_square_dist += (rank1_pos[x] - rank2_pos[x])**2
    
    spearman = 1 - ((6*sum_of_square_dist)/(n*((n**2) - 1)))
    
    return spearman

def kendal_tau(rank1, rank2):
    n = len(rank1)
    rank1_pair_set = set((rank1[x],rank1[y]) for x in range(n) for y in range(x+1,n))
    rank2_pair_set = set((rank2[x],rank2[y]) for x in range(n) for y in range(x+1,n))
    
    n_pair = len(rank1_pair_set)
    convergence = len(rank1_pair_set.intersection(rank2_pair_set))
    divergence = n_pair - convergence

    return ((convergence/n_pair) - (divergence/n_pair))