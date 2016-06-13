import time 
import requests
import operator
import numpy as np



url = 'http://api.bandsintown.com/events/search'
appID = 'insightprojectDC'
url = 'http://api.bandsintown.com/events/search?location=35.379494,-118.828125&format=json&app_id=' + appID

response = requests.request( 'get', url)
print response.json()

#response = requests.request( 'get', 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_tracks=0c6xIDDpzE81m2q797ordA&min_energy=0.4&min_popularity=50&market=US', auth = 'BQDvE4_dt95Sftb5n8qFJdli3MHRdgXoH8FX9qASYiOdjC3lwWwvhgqwJ63hZKn-YOzEMKSMED07FTSqAtIoUw')

