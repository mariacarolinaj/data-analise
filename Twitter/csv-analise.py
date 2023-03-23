# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:12:11 2023

@author: Maria
"""

import pandas as pd

class TwitterUser:
    id = 0
    screenName = ""
    friends = []

data = pd.read_csv('data.csv', error_bad_lines=False, header=0)
num_colunas = len(data.columns)
print(num_colunas)
#novo_nome_colunas = [f'{i}' for i in range(num_colunas)]
#data.columns = novo_nome_colunas

accounts = data['id'].tolist()

colunas_a_remover = ['id', 'screenName', 'tags', 'avatar', 'followersCount', 'friendsCount',
       'lang', 'lastSeen', 'tweetId']

followers = data.iloc[:, 9:]

df_concatenado = pd.concat([followers[coluna] for coluna in followers.columns], axis=1, join='outer', ignore_index=False, keys=None, sort=False, verify_integrity=False, copy=True)
print(followers)
followers.to_csv('a.csv', index=False)
"""
for c in followers:
    print(c)
"""