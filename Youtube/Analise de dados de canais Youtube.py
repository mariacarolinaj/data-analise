# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:47:55 2023

@author: Maria
"""

from googleapiclient.discovery import build
import networkx as nx

api_key = ""
youtube = build('youtube', 'v3', developerKey=api_key)

# ChannelId de alguns canais de música
bts = "UCLkAepWjdylmXSltofFvsYQ"
brunoMars = "UCoUM-UJ7rirJYP8CQ0EIaHA"
backstreetBoys = "UC1OR2YNQLZJYFdQjFrPWvVw"
linkinPark = "UCZU9T1ceaOgwfLRq7OKFU4Q"
systemOfADown = "UC7-YMmnc0ppcWmio8t1WdcA"

channels = [bts, brunoMars, backstreetBoys, linkinPark, systemOfADown]

graph = nx.DiGraph() # Grafo direcionado

# Análise: canais influentes - CANAIS DEVEM TER TODAS AS INFOS PUBLICAS!!
for channel in channels:
    # Busca os canais relacionados ao canal atual e adiciona no grafo direcionado
    results = youtube.subscriptions().list(part='snippet', channelId=channel, maxResults=50).execute()
    for item in results['items']:
        graph.add_edge(channel, item['snippet']['resourceId']['channelId'])

# Execute o algoritmo PageRank para identificar os canais mais influentes
pagerank = nx.pagerank(graph)

# Exibe os canais mais influentes
canaisInfluentes = sorted(pagerank, key=pagerank.get, reverse=True)[:10]

print("Os canais mais influentes na rede são:")
for channel in canaisInfluentes:
    print(channel, " - PageRank:", pagerank[channel])

# Análise: canais influentes - CANAIS DEVEM TER TODAS AS INFOS PUBLICAS!!
for channel in channels:
    request = youtube.subscriptions().list(
        part="snippet",
        channelId=channel,
        maxResults=100
    )
    response = request.execute()
    for item in response["items"]:
        subscriber_id = item["snippet"]["resourceId"]["channelId"]
        subscriber_name = item["snippet"]["title"]
        graph.add_node(subscriber_id, name=subscriber_name)

