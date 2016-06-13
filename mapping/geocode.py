# Takes in a location and produces lat and lon
from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("San Diego, CA")
lat = location.latitude
lon = location.longitude

print lat,lon
