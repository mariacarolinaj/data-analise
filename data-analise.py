import json
import networkx as nx

# realiza a leitura dos dados presentes no json futuramente extraído e tratado 
# da API do twitter

file = open('twitter-data.json')

data = json.load(file)

file.close()

graph = nx.Graph()

for i in data:
    graph.add_node(i['username'])
    graph.add_edge(i['username'], i['followerUsername'])
    
nx.draw(graph, with_labels=True, arrows=True)
