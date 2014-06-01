SoundCloud Page Downloader
==========================

Download a SoundCloud user's music. All of it. Also takes care of ID3 tagging the files for you.

**Note:** Requires Requests and Mutagen packages to run. Simply do `pip install requests robobrowser` before installing.

**Usage Examples:**
* `python soundcloud-downloader.py` will prompt you to enter an artist name to download from.

* `python soundcloud-downloader.py -u diplo` will download all of Diplo's music into `<current directory>/soundcloud-downloads/diplo/`.

* `python soundcloud-downloader.py -u chainsawpolice` will download all of Chainsaw Police's music into `<current directory>/soundcloud-downloads/chainsawpolice/`.