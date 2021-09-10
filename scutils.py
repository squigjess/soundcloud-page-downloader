"""Assorted utilities for handling SoundCloud API stuff"""
import requests
from requests_html import HTMLSession
import json
import sys

def goldenID(TRACK_URL):
    """Scrape a SoundCloud webpage for the 'golden ID'"""
    session = HTMLSession() # Start a new session
    r = session.get(TRACK_URL) # Get the track's web page

    # Read the web page, slowly start nrrowing things down until we get the "golden ID"
    dirtyJS = r.html.find("script")[9] # Find the 10th <script> tag on the page.
    cleanedUpJS = json.loads(dirtyJS.text[24:-1]) # Truncate some of the start and end characters to make it JSON-serlialisable.
    waveformURL = cleanedUpJS[6]["data"]["waveform_url"] # Get the exact partof the JSON we need
    goldenID = waveformURL.split("_m.json")[0].split("https://wave.sndcdn.com/")[1] # Trim off the parts we don't need to get that special ID.
    return goldenID

print(goldenID(sys.argv[1]))
