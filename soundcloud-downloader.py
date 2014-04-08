import json
import os
import argparse
import platform
import sys

import requests
import mutagen
from robobrowser import RoboBrowser
from mutagen.easyid3 import EasyID3


CLIENTID = "2412b70da476791567d496f0f3c26b88"


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def resolve_profile_url(friendly_url):
    r = requests.get('http://api.soundcloud.com/resolve.json?url={}/tracks&client_id={}'.format(friendly_url, CLIENTID),
                     allow_redirects=False)
    resolved_profile_uri = json.loads(r.text)['location']
    return resolved_profile_uri


def get_song_links(soundcloud_url):
    browser = RoboBrowser(history=False)

    # Go to SoundFlush and ask to rip the specified track.
    browser.open('http://soundflush.com/')
    form = browser.get_form(id='form_download')
    form['track_url'].value = soundcloud_url
    browser.submit_form(form)

    # Grab the download link and filename from the download page.
    download_link = browser.select('a#btn_save')[0]
    download_url = download_link['href']
    download_name = download_link['download']
    return {'url': download_url, 'name': download_name}


def tag_file(file_name, song_title, song_artist, song_genre):
    file_path = file_name
    try:
        meta = EasyID3(file_path)
    except mutagen.id3.ID3NoHeaderError:
        meta = mutagen.File(file_path, easy=True)
        meta.add_tags()

    meta['title'] = song_title
    meta['artist'] = song_artist
    meta['genre'] = song_genre
    meta.save()


def main(args):
    clear_screen()
    print "SoundCloud Page Downloader\nBy J. Merriman - http://chainsawpolice.github.io/\n"

    # Clean up the profile URL to make sure it contains no slash at the end.
    if args.profilelink.endswith('/'):
        resolved_profile_uri = resolve_profile_url(args.profilelink[:-1])
    else:
        resolved_profile_uri = resolve_profile_url(args.profilelink)

    # Get all the user's tracks
    r = requests.get(resolved_profile_uri)
    all_tracks = json.loads(r.text)

    # Create a download dir, if one isn't made already.
    directory = 'soundcloud-downloader/' + all_tracks[0]['user']['permalink']
    if not os.path.exists(directory):
        os.makedirs(directory)

    track_amount = len(all_tracks)
    track_number = 1

    for this_song in all_tracks:
        # Grab links and filenames for the current song
        song_links = get_song_links(this_song['permalink_url'])
        print """Currently downloading song {}/{} ({})...\n
                ----------------------""".format(track_number, track_amount, this_song['title'])

        # Download and ID3 tag the file
        os.system("wget -c '{}' -O '{}/{}'".format(song_links['url'], directory, song_links['name']))
        file_location = "{}/{}".format(directory, song_links['name'])
        tag_file(file_location, this_song['title'], this_song['user']['username'], this_song['genre'])

        track_number += 1
        print "\n\n"

    print "All songs downloaded! Navigate to {} in {}'s directory to see your music.\n".format(directory, sys.argv[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download a SoundCloud user's music. All of it.")
    parser.add_argument('profilelink', metavar='profilelink', help="The user's SoundCloud profile URL.")
    parsed_args = parser.parse_args()
    main(parsed_args)