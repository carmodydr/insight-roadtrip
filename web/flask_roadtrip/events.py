import time
import requests
import operator
import numpy as np
import json


url = 'http://api.bandsintown.com/events/search'
appID = 'insightprojectDC'

# Attica
lat = 42.77
lon = -89.480560

startDate = '2016-07-06'
endDate = '2016-07-14'

def returnEvents(lat, lon, radius, startDate, endDate):
	url = 'http://api.bandsintown.com/events/search?location='+str(lat)+','+str(lon)+'&radius='+radius+'&date='+startDate+','+endDate+'&format=json&app_id=' + appID
	
	response = requests.request( 'get', url)
	parsedResponse = response.json()
	return parsedResponse

