import requests
import json
import argparse
import sys
import mutagen
import os
import platform
from urllib.request import urlopen
from mutagen.easyid3 import EasyID3
CLIENTID = '2412b70da476791567d496f0f3c26b88'


def resolve_profile_tracks_url(friendly_url):
	r = requests.get('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/{}/tracks&client_id={}'.format(friendly_url, CLIENTID), allow_redirects=False)

	if 'errors' in json.loads(r.text):
		print("{}\nCannot find the specified user.".format(json.loads(r.text)['errors'][0]['error_message']))
		sys.exit(1)
	else:
		resolved_profile_uri = json.loads(r.text)['location']
		return resolved_profile_uri


def get_profile_tracks(tracks_url):
	r = requests.get(tracks_url)
	return json.loads(r.text)


def get_download_link(waveform_url):
	unique_id = waveform_url[21:][:-6]
	return 'http://media.soundcloud.com/stream/{}'.format(unique_id)


def download_file(download_url, artist_name, artist_friendlyname, song_name, song_genre):
	directory = os.path.join('soundcloud-downloads', artist_friendlyname)
	if not os.path.exists(directory):
		os.makedirs(directory)

	file_name = "soundcloud-downloads/{}/{}.mp3".format(artist_friendlyname, song_name)
	# urllib2 file download implementation by PabloG @ StackOverflow - http://stackoverflow.com/a/22776
	u = urlopen(download_url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta["Content-Length"])
	print("Downloading: {} (Bytes: {})".format(song_name, file_size))

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8)*(len(status)+1)
		print(status),

	f.close()

	try:
		meta = EasyID3(file_name)
	except mutagen.id3.ID3NoHeaderError:
		meta = mutagen.File(file_name, easy=True)
		meta.add_tags()
	meta['title'] = song_name
	meta['artist'] = artist_name
	meta['genre'] = song_genre
	meta.save()


def main(args):
	print("SoundCloud Page Downloader\nBy J. Merriman - http://chainsawpolice.github.io/")

	if not args.u:
		print('\nPlease enter The user\'s SoundCloud permalink (a.k.a The link to their profile, without the "http://soundcloud.com" at the start).\ne.g. chainsawpolice, diplo, skrillex, etc.\n')
		username = input('> ')
	else:
		username = args.u

	directory = os.path.join('soundcloud-downloads')
	if not os.path.exists(directory):
		os.makedirs(directory)

	tracks_url = resolve_profile_tracks_url(username)
	track_listing = get_profile_tracks(tracks_url)

	track_amount = [1, len(track_listing)]

	for track in track_listing:
		print('\nTrack {}/{}'.format(track_amount[0], track_amount[1]))
		username = track["user"]["username"]
		track_title = track["title"]
		track_genre = track["genre"]

		download_link = get_download_link(track['waveform_url'])
		print(username)
		download_file(download_link, username, track['user']['permalink'], track_title, track_genre)
		print("\n")
		track_amount[0] += 1

	print('\n\nFinished downloading all music\nYou can find the music in the soundcloud-downloads/ folder, which should be in the same directory as this file.\n\nHappy listening!\n')
	if platform.system() == 'Windows':
		input('Press enter to continue...')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download a SoundCloud user\'s music. All of it.')
	parser.add_argument('-u', help='The user\'s SoundCloud permalink (a.k.a The link to their profile, without the "http://soundcloud.com" at the start).')
	parsed_args = parser.parse_args()
	main(parsed_args)
