# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:47:55 2023

@author: Maria
"""

from googleapiclient.discovery import build
import networkx as nx

api_key = "AIzaSyCAqUYWQAIG4eMk73De0Xu2NgGBlbabCIA"
youtube = build('youtube', 'v3', developerKey=api_key)

graph = nx.DiGraph() # Grafo direcionado

video = "BuRgB-xd-Gs"
request = youtube.commentThreads().list(
    part="snippet",
    videoId=video,
    maxResults=100
)
response = request.execute()

# Gera um grafo direcionado dos comentaristas do vídeo
for item in response["items"]:
    id = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
    name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
    graph.add_node(id, name=name)
    graph.add_edge(id, video)

nx.draw(graph, with_labels=True, arrows=True)

# Usa centralidade para identificar os comentaristas mais populares do vídeo
centralityIn = nx.in_degree_centrality(graph)

print("Os usuários com os comentários mais populares são:")
for node, score in sorted(centralityIn.items(), key=lambda x: x[1], reverse=True)[:10]:
    if bool(graph.nodes[node]):
        print(f"- {graph.nodes[node]['name']}")

# Usa centralidade para identificar os comentaristas que mais engajaram em comentários de outros
centralityOut = nx.out_degree_centrality(graph)

print("\nOs usuários que mais comentaram em outros comentários são:")
for node, score in sorted(centralityOut.items(), key=lambda x: x[1], reverse=True)[:10]:
    if bool(graph.nodes[node]):
        print(f"- {graph.nodes[node]['name']}")
    

