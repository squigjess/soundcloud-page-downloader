#!/usr/bin/python
import json, requests, os, mutagen, argparse, platform, sys
from robobrowser import RoboBrowser
from mutagen.easyid3 import EasyID3
CLIENTID = "2412b70da476791567d496f0f3c26b88"


def clearScreen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def resolveProfileURL(friendlyURL):
	r = requests.get('http://api.soundcloud.com/resolve.json?url='+friendlyURL+'/tracks&client_id='+CLIENTID, allow_redirects=False)
	if r.status_code == 302:
		return json.loads(r.text)['location']
	else:
		return None


def getSongLinks(soundcloudURL):
	browser = RoboBrowser(history=False)

	# Go to SoundFlush and ask to rip the specified track.
	browser.open('http://soundflush.com/')
	form = browser.get_form(id='form_download')
	form['track_url'].value = soundcloudURL
	browser.submit_form(form)

	# Grab the download link and filename from the download page.
	downloadLink = browser.select('a#btn_save')[0]
	downloadURL = downloadLink['href']
	downloadName = downloadLink['download']
	return {'url' : downloadURL, 'name' : downloadName}


def tagFile(fileName, songTitle, songArtist, songGenre):
	filePath = fileName
	try:
		meta = EasyID3(filePath)
	except mutagen.id3.ID3NoHeaderError:
		meta = mutagen.File(filePath, easy=True)
		meta.add_tags()
	meta['title'] = songTitle
	meta['artist'] = songArtist
	meta['genre'] = songGenre
	meta.save()


def checkUrl(url):
	base = "http://soundcloud.com/"
	if base not in url:
		url = base + url
	return url


def main():
	parser = argparse.ArgumentParser(description="Download a SoundCloud user's music. All of it.")
	parser.add_argument('profilelink', metavar='profilelink', help="The user's SoundCloud profile URL.")
	args = parser.parse_args()

	clearScreen()
	print("SoundCloud Page Downloader\nBy J. Merriman - http://chainsawpolice.github.io/\n")

	# Clean up the profile URL to make sure it contains no slash at the end.
	if args.profilelink.endswith('/'):
		resolvedProfileURI = resolveProfileURL(checkUrl(args.profilelink[:-1]))
	else:
		resolvedProfileURI = resolveProfileURL(checkUrl(args.profilelink))

	if resolvedProfileURI == None:
		print("I can't get the user %s" % args.profilelink)
		exit(1)

	# Get all the user's tracks
	r = requests.get(resolvedProfileURI)
	allTracks = json.loads(r.text)

	if len(allTracks) == 0:
		print("%s don't have any track." % args.profilelink)
		exit(0)

	# Create a download dir, if one isn't made already.
	directory = 'soundcloud-downloader/'+allTracks[0]['user']['username']
	if not os.path.exists(directory):
		os.makedirs(directory)

	trackAmount = len(allTracks)
	trackNumber = 1

	for thisSong in allTracks:
		# Grab links and filenames for the current song
		songLinks = getSongLinks(thisSong['permalink_url'])
		print("Currently downloading song " + str(trackNumber) + "/" + str(trackAmount) + " (" + thisSong['title'] + ")...\n--------------------------------------\n")

		# Download and ID3 tag the file
		os.system("wget -c '" + songLinks['url'] + "' -O '"+directory+"/"+songLinks['name'] +"'")
		fileLocation = directory+"/"+songLinks['name']
		tagFile(fileLocation, thisSong['title'], thisSong['user']['username'], thisSong['genre'])

		trackNumber += 1
		print("\n\n")

	print("All songs downloaded! Navigate to " + directory + " in " + sys.argv[0] + "'s directory to see your music.\n")


if __name__ == "__main__":
	main()