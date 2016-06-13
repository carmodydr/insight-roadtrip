from flask import render_template, request
from flask_roadtrip import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import MySQLdb as mdb
from a_Model import ModelIt
from events import returnEvents
from geocode import latlon
from rankingSim import artistPath
import networkx as nx

username = 'dan'
host = 'localhost'
dbname = 'music'
pswd = 'insight'

engine = create_engine('mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = mdb.connect('localhost', username, pswd, dbname)
simArtists = pd.read_sql_table('relArtist',con='mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
g = nx.from_pandas_dataframe(simArtists,'Artist','RelArtist')



@app.route('/')
@app.route('/index/')
def index():
	user = { 'nickname': 'Dan' } # fake user
	return render_template("index.html",
		title = 'Home',
		user = user)

@app.route('/input')
def roadtrip_input():
	return render_template("input.html")

@app.route("/output")
def roadtrip_output():
	#pull 'birth_month' from input field and store it
	start = request.args.get('start_location')
	startlat, startlon = latlon(start)

	end = request.args.get('end_location')
	endlat, endlon = latlon(end)

	seedArtist = request.args.get('seed_artist')
	#just select the Cesareans from the birth database for the month that the user inputs
	#query = "SELECT idx, attendant, birth_month FROM birth_data_table3 WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
	#print query
	#query_results = pd.read_sql_query(query,con)
	#print query_results
	events = []
	topEvents = []
	eventResponse = returnEvents( startlat, startlon, '100', '2016-07-06', '2016-07-14')	
	for i in eventResponse:
		for j in i['artists']:
			try:
				events.append(dict(band=j['name'], venue=i['venue']['name'], rank=artistPath(g, seedArtist, j['name']) ) )
			except:
				events.append(dict(band=j['name'], venue=i['venue']['name'], rank='1000' ) )
	sortEvents = sorted( events, key=lambda k: k['rank'] )
	topEvents.append( sortEvents[0] )

	

	return render_template("output.html", events = topEvents)
