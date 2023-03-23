# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:14:47 2023

@author: Maria

Gera um grafo com a relação entre os seguidores de uma conta semente e os 
seguidores dos seguidores dela.
"""

import instaloader
import networkx as nx

def obterFollowers(username):
    il = instaloader.Instaloader()
    
    usernameLogin = 'pixiedust.png'
    passwordLogin = ''

    il.load_session_from_file(usernameLogin)

    profile = instaloader.Profile.from_username(il.context, username)
    
    followers = []
    for follower in profile.get_followers():
        followers.append(follower.username)

    return followers

graph = nx.Graph()

perfilGerador = 'pixiedust.png'

followersPerfilGerador = obterFollowers(perfilGerador)

for follower in followersPerfilGerador:
    graph.add_node(perfilGerador)
    graph.add_edge(perfilGerador, follower)
    
    followersPerfilSeguidor = obterFollowers(follower)
    for followerSeguidor in followersPerfilSeguidor:
        graph.add_node(follower)
        graph.add_edge(follower, followerSeguidor)
    
nx.draw(graph, with_labels=True, arrows=True)

