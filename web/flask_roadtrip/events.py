import time
import requests
import operator
import numpy as np
import json
from rankingSim import artistPath
from geocode import lldist
from pandas import to_datetime

BASEurl = 'http://api.bandsintown.com/events/search'
appID = 'insightprojectDC'

# Attica
lat = 42.77
lon = -89.480560

startDate = '2016-07-06'
endDate = '2016-07-14'

# need to create grid of lat and lon

def genLatLonPoints(startLat, startLon, endLat, endLon, startDate, endDate):
	fullDist = lldist( startLat, startLon, endLat, endLon)
	dayStart = to_datetime(startDate)
	dayEnd = to_datetime(endDate)
	deltaDays = abs(int( (dayEnd-dayStart).days ))

	# for right now - get starting location, ending location, and the appropriate number 
	# of waypoints in between
	places = []

	latVec = endLat - startLat
	lonVec = endLon - startLon

	dlatVec = latVec / deltaDays
	dlonVec = lonVec / deltaDays

	for i in range(deltaDays):
		places.append( (startLat + dlatVec*i, startLon + dlonVec*i) )
	
	return places


def topEvent(lat, lon, date, radius, seedArtist, g):
	url = BASEurl + '?location='+str(lat)+','+str(lon)+'&radius='+radius+'&date='+date+'&format=json&app_id=' + appID
        response = requests.request( 'get', url)
        parsedResponse = response.json()
        events = []
        for i in parsedResponse:
                for j in i['artists']:
                        try:
                                events.append(dict(band=j['name'], venue=i['venue']['name'], venLat=i['venue']['latitude'], venLon=i['venue']['longitude'], rank=artistPath(g, seedArtist, j['name']) ) )
                        except:
                                events.append(dict(band=j['name'], venue=i['venue']['name'], venLat=i['venue']['latitude'], venLon=i['venue']['longitude'], rank='1000' ) )
        sortEvents = sorted( events, key=lambda k: k['rank'] )
        if len(sortEvents) > 0:
		return sortEvents[0]
	else:
		print "No events for this location"
		return []

def returnTopEvents(latStart, lonStart, latEnd, lonEnd, radius, startDate, endDate, seedArtist, g):
	fullList = []

	places = genLatLonPoints( latStart, lonStart, latEnd, lonEnd, startDate, endDate )

	for i in places:
		l = topEvent( i[0], i[1], startDate, radius, seedArtist, g)
		# check to see if an event was actually returned
		if len(l) > 0:
			fullList.append( l )

	print fullList
	return fullList
