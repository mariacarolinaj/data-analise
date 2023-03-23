# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:47:55 2023

@author: Maria
"""

from googleapiclient.discovery import build

api_key = ""
youtube = build('youtube', 'v3', developerKey=api_key)

channel_id = "UCLkAepWjdylmXSltofFvsYQ"
channel = youtube.channels().list(id=channel_id, part="snippet,contentDetails,statistics").execute()

print("Nome do canal:", channel['items'][0]['snippet']['title'])
print("Descrição do canal:", channel['items'][0]['snippet']['description'])
print("Número de inscritos:", channel['items'][0]['statistics']['subscriberCount'])
print("Número de visualizações:", channel['items'][0]['statistics']['viewCount'])
