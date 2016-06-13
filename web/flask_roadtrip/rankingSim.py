# Given a pair of artists, return rank

import networkx as nx

def artistPath( g, artist1, artist2):
    return nx.shortest_path_length( g, artist1, artist2)

