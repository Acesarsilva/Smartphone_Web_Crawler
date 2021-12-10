import sys
import json
import math
from util import spearman, kendal_tau, cossine_similarity


def main(data_path):
    run = True
    f = open(data_path)
    data = json.load(f)
    while(run):
        on_query = True
        word_query = []
        while(on_query):
            print("Campos: [geral, memoria_rom, tela, memoria_ram, preço, marca, camera]")
            camp = input("Campo que deseja consultar: ")
            value = input("Valor que deseja neste campo: ")
            words = value.split()
            if(camp != "geral"):
                words = [(word + '.' + camp).lower() for word in words]
            
            word_query.extend(words)
            end_query = input("Deseja adicionar mais algo a esta consulta? [Y/n]: ")
            if(end_query == "n"):
                on_query = False
        
        print("Realizando consulta.....")
        rank = bool_query(word_query, data,84,10)
        print("Resultado encontrado: ", rank)
        end_run = input("Deseja fazer mais uma consulta? [Y/n]: ")
        if(end_run == "n"):
            run = False

    return ("Processo Finalizado")

def tfid_query(words, data, n_documents, K):
    #Doc-at-Time [Time: O(doc x query), Space: O(query)] vs Term-at-Time [Time: O(query), Space: O(doc x query)]
    N = len(words)
    sumyy = 0
    query = [0]*N
    documents = [(0,0)]*n_documents #Scores Parciais
    #Usando Term-at-Time
    for x in range(N):
        word = words[x]
        if(word in data.keys()):
            ni = data[word]['ni']
            docs = data[word]['occurrences']
            word_tfidf = math.log(1 + (n_documents/ni)) #Calculando TF-IDF para palavra na query
            sumyy += word_tfidf**2
            query[x] = word_tfidf
            for y in range(ni):
                doc = int(docs[y][0])
                tf = docs[y][1]
                tfidf = 1 + math.log(tf) #Calculando TF-IDF para palavra no documento
                tlp = documents[doc-1]
                documents[doc-1] = (tlp[0]+tfidf**2,tlp[1]+(tfidf*word_tfidf))
    
    rank = []
    scores = []
    for x in range(n_documents):
        score = 0
        if(documents[x][0] != 0):
            score = (documents[x][1]/(documents[x][0]*sumyy)) #Calculando similaridade por Cosseno

        if(score):
            for n in range(len(scores)):
                if (score >= scores[n]):
                    scores.insert(n,score)
                    rank.insert(n, x+1)
                    break
        else:
            scores.append(score)
            rank.append(x+1)

    return rank[:K]

def bool_query(words, data,n_documents, K):
    N = len(words)
    sumyy = 0
    query = [0]*N
    documents = [(0,0)]*n_documents #Scores Parciais
    #Usando Term-at-Time
    for x in range(N):
        word = words[x]
        if(word in data.keys()):
            ni = data[word]['ni']
            docs = data[word]['occurrences']
            word_tfidf = 1 
            sumyy += word_tfidf**2
            query[x] = word_tfidf
            for y in range(ni):
                doc = int(docs[y][0])
                tf = docs[y][1]
                tfidf = 1 #Calculando TF-IDF para palavra no documento
                tlp = documents[doc-1]
                documents[doc-1] = (tlp[0]+tfidf**2,tlp[1]+(tfidf*word_tfidf))
    
    rank = []
    scores = []
    for x in range(n_documents):
        score = 0
        if(documents[x][0] != 0):
            score = (documents[x][1]/(documents[x][0]*sumyy)) #Calculando similaridade por Cosseno

        if(score):
            for n in range(len(scores)):
                if (score >= scores[n]):
                    scores.insert(n,score)
                    rank.insert(n, x+1)
                    break
        else:
            scores.append(score)
            rank.append(x+1)

    return rank[:K]


if __name__ == "__main__":
    #data_path = sys.argv[1]
    data_path = 'json_general_final.json'
    print(main(data_path))