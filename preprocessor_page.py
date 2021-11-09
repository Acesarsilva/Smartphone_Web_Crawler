from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import unicodedata

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