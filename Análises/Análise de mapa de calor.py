# -*- coding: utf-8 -*-
"""
@author: Maria
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
nltk.download('vader_lexicon')

def heatmapAnalysis(csv_file_name):
    graph = nx.Graph()

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
    
    tokens = [word_tokenize(comment.lower()) for comment in df['full_text']]
    
    edges = []
    for token_list in tokens:
        for w1, w2 in itertools.combinations(set(token_list), 2):
            edges.append((w1, w2))

    graph.add_edges_from(edges)

    # Contagem de frequência das palavras
    word_freq = Counter([word for edge in edges for word in edge[:2]])
    
    for w1, w2 in edges:
        weight = word_freq[w1] + word_freq[w2]
        graph.add_edge(w1, w2, weight=weight)

    # Obtém os pesos das arestas, baseado com a frequência de cada conexão (aqui considerando
    # todas as palavras dos comentários)
    weights = [graph[u][v]['weight'] for u, v in graph.edges()]
    
    # Para fins de exibição, o número máximo de palavras será limitado a apenas as 25 mais frequentes
    # para a geração do grafo de mapa de calor
    max_words = 25
    top_words = [word for word, _ in word_freq.most_common(max_words)]
    
    # Cria um subgrafo contendo apenas as palavras mais frequentes
    subgraph = graph.subgraph(top_words)
    
    # Calcula o peso de cada aresta para definição da sua cor no grafo
    weights = [subgraph[u][v]['weight'] for u, v in subgraph.edges()]
    
    # Configura a montagem do grafo
    pos = nx.spring_layout(subgraph, k=9)
    nx.draw_networkx_edges(subgraph, pos, edge_color=weights, edge_cmap=plt.cm.YlOrRd)
    nx.draw_networkx_nodes(subgraph, pos, node_color='lightgreen')
    labels = {node: node for node in subgraph.nodes()}
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=8, font_family='sans-serif')
    
    titulo = csv_file_name.split('_')[0]
    plt.title(titulo)
    plt.rcParams['figure.dpi'] = 300  
    plt.axis('off')
    plt.show()

social_networks_files = ['Twitter_dataset.csv', 'Youtube_dataset.csv', 'Instagram_dataset.csv']

for file in social_networks_files:
    heatmapAnalysis(file)