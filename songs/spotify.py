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

url_rec = 'https://api.spotify.com/v1/recommendations'
url_access = 'https://accounts.spotify.com/api/token'
clientID = 'f463ac789e0b4d248b11e8c8907fad40'
clientSecret = 'f83af83594974c858b1616b1ad913e51'
_key = 1
_maxNumRetries = 10

# POST https://accounts.spotify.com/api/token

response = requests.post( url_access, data= {'grant_type': 'client_credentials'}, auth = (clientID, clientSecret))
access =  response.json()
access_key = access['access_token']
print access_key

#response = requests.request( 'get', 'https://api.spotify.com/v1/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_tracks=0c6xIDDpzE81m2q797ordA&min_energy=0.4&min_popularity=50&market=US', auth = 'BQDvE4_dt95Sftb5n8qFJdli3MHRdgXoH8FX9qASYiOdjC3lwWwvhgqwJ63hZKn-YOzEMKSMED07FTSqAtIoUw')

print response.content

def processRequest( json, data, headers ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = None )

        if response.status_code == 429: 

            print "Message: %s" % ( response.json()['error']['message'] )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print 'Error: failed after retrying!'
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print "Error code: %d" % ( response.status_code )
            print "Message: %s" % ( response.json()['error']['message'] )

        break
        
    return result

# URL direction to image
#urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'
urlImage = 'http://www.hechoparamama.com/wp-content/uploads/2012/06/Fotolia_40541938_Subscription_Monthly_XXL.jpg'
urlImage = 'http://static.kidspot.com.au/cm_assets/5991/australias-top-100-baby-names-20130402103500.jpg~q75,dx720y432u1r1gg,c--.jpg'

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json' 

json = { 'url': urlImage } 
data = None

#result = processRequest( json, data, headers )

#print result

# Load the original image, fetched from the URL
#arr = np.asarray( bytearray( requests.get( urlImage ).content ), dtype=np.uint8 )
#img = cv2.cvtColor( cv2.imdecode( arr, -1 ), cv2.COLOR_BGR2RGB )

#renderResultOnImage( result, img )

#img, ax = plt.subplots(figsize=(15, 20))
#ax.imshow( img )
