# coding: utf-8

# In[1]:

import time 
import requests
import operator
import numpy as np
import json


# In[ ]:

url = 'http://api.bandsintown.com/events/search'
appID = 'insightprojectDC'

# Attica
lat = 42.77
lon = -89.480560

startDate = '2016-07-06'
endDate = '2016-07-14'

#def returnEvents(lat, lon, radius=100, dateRange)
url = 'http://api.bandsintown.com/events/search?location='+str(lat)+','+str(lon)+'&date='+startDate+','+endDate+'&format=json&app_id=' + appID

response = requests.request( 'get', url)
parsedResponse = response.json()


# In[17]:

l = []

for i in parsedResponse[0:3]:
    for j in i['artists']:
        print i['venue']['name'], i['venue']['latitude'], i['venue']['longitude'], j['name'], i['datetime']
    l.append(i)

'''
useful quantities in the JSON:
url, ticket_url
venue: city, name, url, country, region, longitude, latitude, id
on_sale_datetime, datetime
artists: url, mbid, name
'''

print l
# ### Calculate distances to the original point
# 
# 
# ```
# dlon = lon2 - lon1
# dlat = lat2 - lat1
# a = (sin(dlat/2))^2 + cos(lat1) * cos(lat2) * (sin(dlon/2))^2
# c = 2 * atan2( sqrt(a), sqrt(1-a) )
# d = R * c (where R is the radius of the Earth) 
# ```
# 
# Taken from http://andrew.hedges.name/experiments/haversine/

# In[15]:

def deg2rad(deg):
    return deg * (np.pi/180)


# In[16]:

lat1 = lat
lon1 = lon

lat2 = parsedResponse[0]['venue']['latitude']
lon2 = parsedResponse[0]['venue']['longitude']

dlat = deg2rad(lat2 - lat1)
dlon = deg2rad(lon2 - lon1)

print dlat, dlon

R = 3959 # radius of the Earth in miles

a = (np.sin(dlat/2))**2 + np.cos( deg2rad(lat1) ) * np.cos( deg2rad(lat2) ) * (np.sin(dlon/2))**2
c = 2* np.arctan2( np.sqrt(a), np.sqrt(1-a) )
d = R * c

print d


# In[ ]:



