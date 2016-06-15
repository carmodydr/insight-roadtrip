from flask import render_template, request
from flask_roadtrip import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import MySQLdb as mdb
from a_Model import ModelIt
from events import returnTopEvents
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

@app.route('/map')
def map():
	start = request.args.get('start_location')
	startlat, startlon = latlon(start)

	end = request.args.get('end_location')
	endlat, endlon = latlon(end)

	seedArtist = request.args.get('seed_artist')
	events = []
	topEvents = []

	topEvents = returnTopEvents( startlat, startlon, endlat, endlon, '100', '2016-07-06', '2016-07-14', seedArtist, g) 

	placesList = []
	for i in topEvents:
		placesList.append( [i['venLat'], i['venLon']] )

#	placesList = [[37,-70], [38.913184,-77.031952], [37.775408,-122.413682] , [42, -80]]
	return render_template("map.html", placesList = placesList)

@app.route("/output")
def roadtrip_output():
	start = request.args.get('start_location')
	startlat, startlon = latlon(start)

	end = request.args.get('end_location')
	endlat, endlon = latlon(end)

	seedArtist = request.args.get('seed_artist')
	events = []
	topEvents = []

	topEvents = returnTopEvents( startlat, startlon, endlat, endlon, '100', '2016-07-06', '2016-07-14', seedArtist, g) 

	return render_template("output.html", events = topEvents)
