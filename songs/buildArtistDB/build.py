import MySQLdb as mdb
import networkx as nx
import json
import pandas as pd
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


'''
	Goal: Build database of artists, genres, and related artists. Use networkx to find distances between artists?

	Steps:

	Start with list of major artists. Query Spotify for 
	
	1. Build a list of Spotify IDs.
	2. Using IDs, get related artists.



'''

db_name = 'spotifyArtists'
username = 'dan'
password = 'insight'

engine = create_engine('mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
#print engine.url

if not database_exists(engine.url):
    create_database(engine.url)
#print(database_exists(engine.url))

abirdID = '4uSftVc3FPWe6RJuMZNEe9'
# Andrew Bird Artist ID: 


results = sp.artist_related_artists(abirdID)
#results = f.read()
parsedResults = json.loads(json.dumps(results))
#pprint(parsedResults['artists'])

for i in parsedResults['artists']:
	print i['name'] + ',' + i['id'] + ',' +  json.dumps(i['genres'])


con = None
con = mdb.connect('localhost', username, pswd, dbname)

# query:
sql_query = """
SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';
"""
birth_data_from_sql = pd.read_sql_query(sql_query,con)

birth_data_from_sql.head()
