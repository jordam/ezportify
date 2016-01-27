from getpass import getpass
import sys
from google import Mobileclient
import urllib
import urllib2
import json
try: 
	import certifi
except:
	print "You need to easy_install certifi"
	sys.exit()
try:
	import gpsoauth
except:
	print "You need to easy_install gpsoauth"
	sys.exit()

try:
	input = raw_input
except NameError:
	pass


def hitapi(oauth, url):
	headers = { 'Authorization' : 'Bearer ' +  oauth}
	req = urllib2.Request(url, headers=headers)
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		response = e.fp
	the_page = response.read()
	return json.loads(the_page)


def main():

	google_email = input("Enter Google email address: ")
	google_pass = getpass("Enter Google password: ")

	googleapi = Mobileclient()
	google_loggedin = googleapi.login(google_email, google_pass)
	if not google_loggedin:
	    print "Invalid Google username/password"
	    sys.exit(1)

	oauth = input("Enter Spotify OAUTH Token (from https://developer.spotify.com/web-api/console/get-current-user-playlists/ ):")
	playlists = hitapi(oauth, 'https://api.spotify.com/v1/me/playlists')
	if 'error' in playlists.keys():
		print "The oauth token is invalid"
		print "Make sure you check the checkbox or checkboxes under 'Relevant scopes'. Clear your token and try again if needed"
		sys.exit()
	items = playlists['items']
	while playlists['next']:
		playlists = hitapi(oauth, playlists['next'])
		items += playlists['items']
	print len(items)
	
	for playlist in items:
		print playlist
		print playlist['name']
		queries = []
		gtracks = []
		trackresp = hitapi(oauth, playlist['href'])['tracks']
		tracks = trackresp['items']
		while trackresp['next']:
			trackresp = hitapi(oauth, trackresp['next'])
			tracks += trackresp['items']
		ot = 1
		for track in tracks:
			searchstr = ''
			if 'artists' in track['track'].keys() and track['track']['artists']:
				searchstr += track['track']['artists'][0]['name'] + ' - '
			searchstr += track['track']['name']
			searchstr_ascii = searchstr.encode("utf-8", "replace")
			gtrack = googleapi.find_best_track(searchstr_ascii)
			if gtrack:
				gtracks.append(gtrack["nid"])
				print ot, '/', len(tracks), 'found', searchstr_ascii
			else:
				print ot, '/', len(tracks), 'Not found', searchstr_ascii, 'for', playlist['name']
			ot += 1
		if len(gtracks) > 0:
			print "Creating in Google Music... ",
			playlist_id = googleapi.create_playlist(playlist['name'])
			googleapi.add_songs_to_playlist(playlist_id, gtracks)
			print "Done"

if __name__ == '__main__':
	main()
