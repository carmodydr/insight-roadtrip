# Takes in a location and produces lat and lon
from geopy.geocoders import Nominatim

def latlon(place):
	geolocator = Nominatim()
	location = geolocator.geocode("San Diego, CA")
	lat = location.latitude
	lon = location.longitude
	return lat,lon
