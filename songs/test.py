import spotipy
sp = spotipy.Spotify(auth='BQCPcq0nCp6wYTYTXZ1A1FxVYjbOe8M8-FkrHRjOHdu1DP5h6QqjrzeQn0c6w5x0_ftcwnHKmbtXRfABScF7-Q')

results = sp.recommendations(seed_artists=['3jOstUTkEu2JkjvRdBA5Gu'], limit=2)
print results

#for i, t in enumerate(results['tracks'][0]):
#for i, t in enumerate(results['tracks']['items']):
#    print ' ', i, t['name']
