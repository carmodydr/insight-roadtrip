from geopy.geocoders import Nominatim
from numpy import sin, cos, arctan2, sqrt, pi

# Takes in a location and produces lat and lon
def latlon(place):
	print "Place:", place
	geolocator = Nominatim()
	location = geolocator.geocode(place)
	lat = location.latitude
	lon = location.longitude
	return lat,lon

# returns great circle distance b/w two lat,lon pairs
def lldist( lat1, lon1, lat2, lon2):
	dlat = deg2rad(lat2 - lat1)
	dlon = deg2rad(lon2 - lon1)

	R = 3959 # radius of the Earth in miles

	a = (sin(dlat/2))**2 + cos( deg2rad(lat1) ) * cos( deg2rad(lat2) ) * (sin(dlon/2))**2
	c = 2* arctan2( sqrt(a), sqrt(1-a) )
	d = R * c

	return d

def deg2rad(deg):
    return deg * (pi/180)
