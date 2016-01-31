from getpass import getpass
import sys
from google import Mobileclient
import urllib
import urllib2
import json
import os
import argparse


if ".exe" in sys.argv[0]:
	os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), 'cacert.pem') ## This is needed to make the .exe version work

try: 
	import certifi
except:
	print "You need to easy_install certifi"
	input("Press enter to exit")
	sys.exit()
try:
	import gpsoauth
except:
	print "You need to easy_install gpsoauth"
	input("Press enter to exit")
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

def googlelogin():
	google_email = input("Enter Google email address: ")
	google_pass = getpass("Enter Google password: ")

	googleapi = Mobileclient()
	google_loggedin = googleapi.login(google_email, google_pass)
	if not google_loggedin:
		print "Invalid Google username/password"
		input("Press enter to exit")
		sys.exit()
	return googleapi

def main(args):

	if not args.dump:
		googleapi = googlelogin()
	print "Enter Spotify OAUTH Token from https://developer.spotify.com/web-api/console/get-current-user-playlists/ "
	oauth = input("Be sure to check the Relevant scopes checkbox: ")
	playlists = hitapi(oauth, 'https://api.spotify.com/v1/me/playlists')
	if 'error' in playlists.keys():
		print "The oauth token is invalid"
		print "Make sure you check the checkbox or checkboxes under 'Relevant scopes'. Clear your token and try again if needed"
		input("Press enter to exit")
		sys.exit()
	items = playlists['items']
	while playlists['next']:
		playlists = hitapi(oauth, playlists['next'])
		items += playlists['items']
	print len(items)
	
	f = open('ezportify-tracks.txt', 'w')
	
	for playlist in items:
		try:
			print playlist
			print playlist['name']
			f.write('\n:::' + playlist['name'] + ":::\n")
			queries = []
			gtracks = []
			trackresp = hitapi(oauth, playlist['href'])['tracks']
			tracks = trackresp['items']
			while trackresp['next']:
				trackresp = hitapi(oauth, trackresp['next'])
				tracks += trackresp['items']
			ot = 1
			for track in tracks:
				try:
					searchstr = ''
					if 'artists' in track['track'].keys() and track['track']['artists']:
						searchstr += track['track']['artists'][0]['name'] + ' - '
					searchstr += track['track']['name']
					searchstr_ascii = searchstr.encode("utf-8", "replace")
					f.write(searchstr_ascii + "\n")
					gtrack = None
					if not args.dump:
						gtrack = googleapi.find_best_track(searchstr_ascii)
					if gtrack:
						gtracks.append(gtrack["nid"])
						print ot, '/', len(tracks), 'found', searchstr_ascii
					else:
						print ot, '/', len(tracks), 'Not found', searchstr_ascii, 'for', playlist['name']
				except:
					print 'Track', ot, 'Failed'
				ot += 1
			if len(gtracks) > 0:
				print "Creating in Google Music... ",
				playlist_id = googleapi.create_playlist(playlist['name'])
				googleapi.add_songs_to_playlist(playlist_id, gtracks)
				print "Done"
		except:
			print playlist['name'], 'Failed to copy. Skipping'
	f.close()
	input("Press enter to exit")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Spotify To Google Playlist Transcription')
	parser.add_argument("-d", "--dump", help="Only Dump Playlists To File",
                    action="store_true")
	parser.add_argument('--version', action='version', version='%(prog)s 0.2')
	args = parser.parse_args()
	main(args)
