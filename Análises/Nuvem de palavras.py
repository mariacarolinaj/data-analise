# -*- coding: utf-8 -*-
"""
@author: Maria
"""

import matplotlib.pyplot as plt
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
nltk.download('vader_lexicon')

def wordCloudAnalysis(csv_file_name):
    # Cria um dataframe com os dados do .csv que serão analisados
    df = pd.read_csv(csv_file_name)
    
    # Padroniza todo o conteúdo da coluna full_text, que armazena em todos os datasets
    # o conteúdo de cada comentário extraído tanto do Youtube quanto do Instagram e Twitter.
    # Remove todos os caracteres que não são letras e converte para lower case o resultado filtrado
    df['full_text'] = df['full_text'].str.replace('[^\w\s]', '')
    df['full_text'] = df['full_text'].str.lower()
    
    # Usando o nltk, obtém todas as "stopwords" conhecidas pelo pacote na língua portuguesa e 
    # as remove de cada comentário presente no dataframe
    nltk.download('stopwords')
    stop_words = set(stopwords.words('portuguese'))
    df['full_text'] = df['full_text'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words]))
    
    # Usando o nltk, obtém os dados do lematizador "wordnet", que transforma todas as palavras
    # filtradas do dataframe em suas formas canônicas para facilitar o agrupamento e análise do
    # contexto em que cada uma delas estão inseridas posteriormente
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    df['full_text'] = df['full_text'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)]))
    
    # Concatenando os comentários em uma única string e gera um plot com a nuvem de palavras
    comentarios = ' '.join(df['full_text'])
    wordcloud = WordCloud().generate(comentarios)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.rcParams['figure.dpi'] = 300  
    titulo = csv_file_name.split('_')[0]
    plt.title(titulo)
    plt.show()
    
social_networks_files = ['Twitter_dataset.csv', 'Youtube_dataset.csv', 'Instagram_dataset.csv']

for file in social_networks_files:
    wordCloudAnalysis(file)
