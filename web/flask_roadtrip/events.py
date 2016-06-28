import time
import requests
import operator
import numpy as np
import json
from rankingSim import artistPath
from geocode import lldist, osrmDist
from pandas import to_datetime
from datetime import timedelta
import networkx as nx

BASEurl = 'http://api.bandsintown.com/events/search'
appID = 'ConcertripRouteFinder'

rank_norm = 13.2 # the average shortest path between artists, on average

# Attica
#lat = 42.77
#lon = -89.480560

#startDate = '2016-07-06'
#endDate = '2016-07-14'

# need to create grid of lat and lon
def genLatLonPoints(startLat, startLon, endLat, endLon, startDate, endDate, radius):
	fullDist = lldist( startLat, startLon, endLat, endLon) # lat/lon distance from start to end
	dayStart = to_datetime(startDate)
	dayEnd = to_datetime(endDate)
	
	deltaDays = abs(int( (dayEnd-dayStart).days )) + 1

	# for right now - get starting location, ending location, and the appropriate number 
	# of waypoints in between
	places = []

	latVec = endLat - startLat
	lonVec = endLon - startLon

	dayRange = 1
	# want to ensure unique search areas
	if (fullDist/deltaDays > 2.0*int(radius)): 
	# if the distance traveled/day is greater than the search radius, just use the daily distance traveled
		dlatVec = latVec / deltaDays
		dlonVec = lonVec / deltaDays
		numSegments = deltaDays
	else:
		numSegments = int(fullDist / (2.0*int(radius)))
		if (numSegments < 1): numSegments = 1
		dayRange = deltaDays/numSegments
		dlatVec = latVec / numSegments
		dlonVec = lonVec / numSegments
	
	# elements to create a search grid
	minDistDay = lldist(0,0,dlatVec,dlonVec)
	dy = dlonVec * (2*float(radius)/minDistDay) 
	dx = dlatVec * (2*float(radius)/minDistDay)


	for i in range(numSegments):
		# append places with lat, lon, day of trip to search, range of days to search
		places.append( (startLat + dlatVec*(i+1), startLon + dlonVec*(i+1), (i+1)*dayRange, dayRange) )
		places.append( (startLat + dlatVec*(i+1)+dy, startLon + dlonVec*(i+1) - dx, (i+1)*dayRange, dayRange) )
		places.append( (startLat + dlatVec*(i+1)-dy, startLon + dlonVec*(i+1) + dx, (i+1)*dayRange, dayRange) )
	print places	
	return places

def topEvent(lat, lon, searchDateStart, searchDateEnd, radius, seedArtist, g):
	# For a given location, find a list of events, rank them, and return the best one
	limit = '100'
	url = BASEurl + '?location='+str(lat)+','+str(lon)+'&radius='+radius+'&date='+searchDateStart+','+searchDateEnd+'&per_page='+limit+'&format=json&app_id=' + appID
        response = requests.request( 'get', url)
        parsedResponse = response.json()
        events = []
        for i in parsedResponse:
                for j in i['artists']:
                        try:
                                events.append(dict(ind=j['name']+i['datetime'], band=j['name'], venue=i['venue']['name'], venLat=i['venue']['latitude'], venLon=i['venue']['longitude'], rank=artistPath(g, seedArtist, j['name']), date=to_datetime(i['datetime']).ctime() , eventUrl=i['url'], chosen=0 ))
                        except:
                                events.append(dict(ind=j['name']+i['datetime'], band=j['name'], venue=i['venue']['name'], venLat=i['venue']['latitude'], venLon=i['venue']['longitude'], rank='1000', date=i['datetime'], eventUrl=i['url'], chosen=0 ))

        sortEvents = sorted( events, key=lambda k: k['rank'] )
        if len(sortEvents) > 0:
		return sortEvents[0]
	else:
		print "No events for this location"
		return []

def routeOptimizer(topEvents, relWeight):
	# Gets a list of the top events from multiple areas, creates a weighted graph, finds best route

	l = len(topEvents)
	fullDist = 1.0*lldist( topEvents[0]['venLat'], topEvents[0]['venLon'], topEvents[l-1]['venLat'], topEvents[l-1]['venLon']) # lat/lon distance from start to end	
	
	# MUST MAKE SURE START AND END ARE IN THE LIST
	DG = nx.DiGraph() # create a new directed graph
	
	for i in topEvents:
		DG.add_node(i['ind'],date=i['date'])
		DG.add_node(i['ind'],venue=i['venue'])
		DG.add_node(i['ind'],band=i['band'])
  		for j in topEvents:
        		day1 = to_datetime(i['date']).date()
        		day2 = to_datetime(j['date']).date()
        		deltaDay = day2 - day1
			dist = 1.0*lldist( i['venLat'], i['venLon'], j['venLat'], j['venLon'] ) 
			#dist = 1.0*osrmDist( i['venLat'], i['venLon'], j['venLat'], j['venLon'] ) 
			tooFar = 500 # in miles
			#tooFar = 300000 # in 10ths of seconds, about 8 hours
        		if (deltaDay.days > 0):
				if (dist/deltaDay.days < tooFar): # only link two events if the second is forward in time, and they're not too far
            				#wght = dist*np.exp((float(j['rank'])/rank_norm)-1)
            				wght = ((1.0-relWeight/100.0) *(dist/fullDist) - (relWeight/100.0)*(1-float(j['rank'])/rank_norm))
		#			wght = np.exp(wght) # map wght to between 0 and 1
	#				if (wght <= 0): wght = (j['rank']/rank_norm)*(dist/fullDist)
					print i['ind'],j['ind'],wght
            				DG.add_weighted_edges_from([(i['ind'],j['ind'],wght)])

	pred, dist = nx.bellman_ford(DG,'Start','weight')
	node = 'End'
	nodeList = []
	while (node != 'Start'):
		nodeList.append(node)
		node = pred[node]
	#path = nx.shortest_path(DG,'Start','End','weight') # the nodes are labeled by ind, so that's all this will return at the moment
	#print path
	return nodeList

def returnTopEvents(latStart, lonStart, latEnd, lonEnd, radius, startDate, endDate, seedArtist, g, relWeight):
	'''
	Get the intitial information and then, using other functions:
	1. Get a list of places to check.
	2. Find the best event in each location.
	3. [Not yet done] Optimize for rank and distance.
	4. Return the desired list.
	'''
	fullList = []

	# get a list of places to check
	places = genLatLonPoints( latStart, lonStart, latEnd, lonEnd, startDate, endDate, radius )

	sDate = to_datetime(startDate)
	
	# add point for start
	fullList.append(dict(ind='Start', band='Start', venue='Start', venLat=latStart, venLon=lonStart, rank=0, date=startDate, eventUrl='', chosen=1 ) )
	
	# find the top event for each one of those places
	for i in places:
		d1 = sDate + timedelta(days=i[2]) - timedelta(days=i[3]/2)
		d2 = sDate + timedelta(days=i[2]) + timedelta(days=i[3]/2)
		#d1 = to_datetime(startDate)
		#d2 = to_datetime(endDate)
		l = topEvent( i[0], i[1], d1.strftime('%Y-%m-%d'), d2.strftime('%Y-%m-%d'), radius, seedArtist, g)
		# check to see if an event was actually returned
		# and that it's better than average
		if (len(l) > 0):
			if l['rank'] < rank_norm:
				fullList.append( l )

	#uniquify
	ls = [dict(y) for y in set(tuple(x.items()) for x in fullList)]
	newlist = sorted(ls, key=lambda k: to_datetime(k['date']))

	fullList = newlist
	# add point for end
	fullList.append(dict(ind='End', band='End', venue='End', venLat=latEnd, venLon=lonEnd, rank=rank_norm, date=endDate, eventUrl='', chosen=1 ) )
	

	# call a function that plots the shortest route, optimizing for distance and rank
	print "Checking optimizer:"
	chosenEvents = routeOptimizer(fullList, relWeight)
	
	for i in chosenEvents:
		for j in fullList:
			if (j['ind'] == i):
				j['chosen'] = 1
	
	return newlist
