import time
import requests
#import cv2
import operator
import numpy as np

# Import library to display results
import matplotlib.pyplot as plt
#%matplotlib inline 
# Display images within Jupyter

# Variables

url_access = 'https://accounts.spotify.com/api/token'
clientID = 'f463ac789e0b4d248b11e8c8907fad40'
clientSecret = 'f83af83594974c858b1616b1ad913e51'

# POST https://accounts.spotify.com/api/token

response = requests.post( url_access, data= {'grant_type': 'client_credentials'}, auth = (clientID, clientSecret))
print response

access =  response.json()
access_key = access['access_token']
print access_key

