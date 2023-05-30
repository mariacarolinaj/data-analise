# -*- coding: utf-8 -*-
"""
@author: Maria Carolina
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def analysis(csv_file_name):
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
    
    # Realiza a vetorização dos textos dos comentários no formato TF-IDF ("Term Frequency-Inverse Document Frequency")
    # calculando aproximadamente a importância de cada termo em relação ao contexto geral onde está inserido
    # e armazena as características dos termos únicos encontrados em feature_names
    vectorizer = TfidfVectorizer()
    fit_transf = vectorizer.fit_transform(df['full_text'])
    feature_names = vectorizer.get_feature_names()
    
    # Realiza a divisão de clusteres para análise a partir da aplicação do algoritmo de k-means, definido inicialmente
    # em 2 para analisar duas comunidades distintas entre os comentários, nesse momento tratados em seus termos únicos
    # armazenados anteriormente na variável fit_transf
    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(fit_transf)
    
    # Identifica e armazena em uma nova coluna do dataset chamada "comunidade" os dados sobre os rótulos extraídos 
    # em cada uma das 2 comunidades definidas anteriormente pelo algoritmo de k-means para indicar a qual destes clusteres
    # ela corresponde
    labels = kmeans.labels_
    df['comunidade'] = labels
    
    # Realiza a análise de sentimento, atribuindo uma pontuação com base em uma abordagem definida pelo dicionário léxico 
    # da função SentimentIntensityAnalyzer (recurso do pacote nltk) usando critérios de positividade, negatividade e neutralidade
    sid = SentimentIntensityAnalyzer()
    df['sentimento'] = df['full_text'].apply(lambda x: sid.polarity_scores(x)['compound'])
    
    # Determina um limiar de sentimento positivo ou negativo e realiza essa separação em cada comunidade
    # O valor foi escolhido como 0 para representar uma nota de corte neutra para os valores analisados
    limiar_sentimento = 0
    df['gostou'] = df['sentimento'].apply(lambda x: 1 if x >= limiar_sentimento else 0)
    df['nao_gostou'] = df['sentimento'].apply(lambda x: 1 if x < -limiar_sentimento else 0)
    
    print(file)
    
    # Realiza uma análise um pouco mais detalhada de cada uma das duas comunidades delimitadas:
    for comunidade_id in df['comunidade'].unique():
        
        print("\nAnálise da comunidade", comunidade_id)
        
        # Filtro para utilizar apenas os dados da comunidade atual em análise
        dados_comunidade = df[df['comunidade'] == comunidade_id]
        
        # Somatório da quantidade de comentários que de acordo com a análise de sentimentos se enquadraram no perfil
        # de usuários que gostaram e não gostaram do conteúdo da publicação em questão
        contagem_gostou = dados_comunidade['gostou'].sum()
        contagem_nao_gostou = dados_comunidade['nao_gostou'].sum()
        
        print("Quantidade de comentários classificados como positivos:", contagem_gostou)
        print("Quantidade de comentários classificados como negativos:", contagem_nao_gostou)
        
        # Novamente com o uso do TfidfVectorizer realiza a análise das palavras-chave presentes na comunidade atual
        vectorizer = TfidfVectorizer()
        X_comunidade = vectorizer.fit_transform(dados_comunidade['full_text'])
        feature_names = vectorizer.get_feature_names()
        
        cluster_keywords = []
        for i in range(num_clusters):
            cluster_keywords.append([feature_names[ind] for ind in X_comunidade[i].toarray().argsort()[0][-5:]])
        print("Palavras-chave da comunidade:", cluster_keywords)
        
        # Calcula o valor médio da análise de sentimento dos comentários na comunidade
        sentimento_medio = dados_comunidade['sentimento'].mean()
        print("Sentimento médio da comunidade:", sentimento_medio)

        
social_networks_files = ['Twitter_dataset.csv', 'Youtube_dataset.csv', 'Instagram_dataset.csv']

for file in social_networks_files:
    analysis(file)
    print ()

