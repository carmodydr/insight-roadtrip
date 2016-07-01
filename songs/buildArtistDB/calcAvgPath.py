# coding: utf-8
# Calculate the average path length in this network
import pandas as pd
import networkx as nx
from random import randint
df = pd.read_csv('relArtist_parse.csv')
g = nx.from_pandas_dataframe(df, 'Artist', 'RelArtist')

h = list(nx.connected_component_subgraphs(g))

len(h[0])

total = len(h[0])

allArtists = h[0].nodes()

for i in range(0,2):
	sum = 0
	searchArtist = allArtists[ randint(0, total) ]
	for j in allArtists:
		sum += nx.shortest_path_length(h[0], searchArtist, j)
	print 1.0*sum / total
    
