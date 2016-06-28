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
import unicodedata
import HTMLParser
from secrets import username, host, dbname, pswd

engine = create_engine('mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = mdb.connect('localhost', username, pswd, dbname)
simArtists = pd.read_sql_table('relArtistFull',con='mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
g = nx.from_pandas_dataframe(simArtists,'Artist','RelArtist')



#@app.route('/')
#@app.route('/index/')
#def index():
#	user = { 'nickname': 'Dan' } # fake user
#	return render_template("index.html",
#		title = 'Home',
#		user = user)

@app.route('/')
@app.route('/index')
def roadtrip_input():
	return render_template("input.html")

@app.route('/about')
def roadtrip_about():
	return render_template("about.html")

@app.route('/map')
def map():
	start = request.args.get('start_location')
	startdate = request.args.get('start_date')
	end = request.args.get('end_location')
	enddate = request.args.get('end_date')
	seedArtist = request.args.get('seed_artist')
	relWeight = request.args.get('points')
	
	startlat, startlon = latlon(start)
	
	endlat, endlon = latlon(end)

#	try:
#		temp = pd.to_datetime(startDate)
#		temp = pd.to_datetime(endDate)
#	except:
#		return render_template("date_error.html")

	events = []
	topEvents = []

	radius = '100'

	topEvents = returnTopEvents( startlat, startlon, endlat, endlon, radius, startdate, enddate, seedArtist, g, float(relWeight)) 

	placesList = []
	bandList = []
	venueList = []
	eventList = []
	parser = HTMLParser.HTMLParser()
	for i in topEvents:
		placesList.append( [i['venLat'], i['venLon']] )

#	placesList = [[37,-70], [38.913184,-77.031952], [37.775408,-122.413682] , [42, -80]]
	print bandList
	return render_template("map.html", placesList = placesList, eventList = topEvents, startName = start, endName = end)

@app.route("/output")
def roadtrip_output():
	try:
		start = request.args.get('start_location')
		startlat, startlon = latlon(start)
		startdate = request.args.get('start_date')
		
		end = request.args.get('end_location')
		endlat, endlon = latlon(end)
		enddate = request.args.get('end_date')

		seedArtist = request.args.get('seed_artist')
	except:
		return render_template("error.html")
	events = []
	topEvents = []

	radius = '150'

	topEvents = returnTopEvents( startlat, startlon, endlat, endlon, radius, startdate, enddate, seedArtist, g) 

	return render_template("output.html", events = topEvents)

@app.route("/test")
def test():
	return render_template("test.html")
