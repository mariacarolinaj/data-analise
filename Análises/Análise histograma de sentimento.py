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
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def sentimentAnalysis(csv_file_name):
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
    
    
    # Realiza a análise de sentimento, atribuindo uma pontuação com base em uma abordagem definida pelo dicionário léxico 
    # da função SentimentIntensityAnalyzer (recurso do pacote nltk) usando critérios de positividade, negatividade e neutralidade
    sid = SentimentIntensityAnalyzer()
    df['sentimento'] = df['full_text'].apply(lambda x: sid.polarity_scores(x)['compound'])
    
    # Monta o histograma com base na análisie da pontuação de sentimentos
    plt.hist(df['sentimento'], bins=10)
    plt.rcParams['figure.dpi'] = 300  
    titulo = csv_file_name.split('_')[0]
    plt.title('Histograma de sentimentos - ' + titulo)
    plt.xlabel('Pontuação')
    plt.ylabel('Frequência')
    
    
    plt.show()
    
social_networks_files = ['Twitter_dataset.csv', 'Youtube_dataset.csv', 'Instagram_dataset.csv']

for file in social_networks_files:
    sentimentAnalysis(file)
