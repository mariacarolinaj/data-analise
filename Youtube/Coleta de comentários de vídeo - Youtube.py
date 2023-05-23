# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:10:53 2023

@author: Maria
"""

from googleapiclient.discovery import build
import csv
import re

api_key = "AIzaSyCAqUYWQAIG4eMk73De0Xu2NgGBlbabCIA"
youtube = build('youtube', 'v3', developerKey=api_key)
video = "wkn-Gb-Fhac"
comments = []
next_page_token = None

while len(comments) < 150:
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video,
        pageToken=next_page_token,
        maxResults=100
    ).execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comment_id = item['id']
        author = comment['authorDisplayName']
        content = comment['textDisplay']
        like_count = comment['likeCount']
        reply_count = item['snippet']['totalReplyCount']
        published_at = comment['publishedAt']

        comments.append([comment_id, author, content, like_count, reply_count, published_at])

    next_page_token = response.get('nextPageToken')

    if not next_page_token:
        break

# Salvar os comentários em um arquivo CSV
with open('Youtube_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'user/name', 'full_text', 'favorite_count', 'reply_count', 'created_at'])

    for comment in comments:
        writer.writerow(comment)
        
print('Os dados do vídeo foram armazenados no arquivo com sucesso.')
