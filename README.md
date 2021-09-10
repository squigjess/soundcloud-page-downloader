# This project is unfortunately dead
**Given that SoundCloud is not allowing new apps to be registered to their API until further notice, this script is no longer usable.**

Once the API becomes open again and I can start register a new API key/client ID, I will update it. Until then, the script does not work and cannot be used (barring extenuating circumstances, such as if someone else finds a way to get this working without API access, in which case please DM me and I will unarchive).

As it stands, the code is quite messy and was written when I was a dumb teen, so it needs a serious rewriting; you probably won't find much of use here if you want to fork it for your own uses, sorry. It's also using Python 2, so there's a lot that needs to be done on that front alone.

--------------
SoundCloud Page Downloader
==========================
Download a SoundCloud user's music. All of it. Also takes care of ID3 tagging the files for you.

**Installation:**

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

**Usage Examples:**

* `python soundcloud-downloader.py` will prompt you to enter an artist name to download from.

* `python soundcloud-downloader.py -u diplo` will download all of Diplo's music into `<current directory>/soundcloud-downloads/diplo/`.

* `python soundcloud-downloader.py -u chainsawpolice` will download all of Chainsaw Police's music into `<current directory>/soundcloud-downloads/chainsawpolice/`.
