# flickrdownload
A python script for downloading your photosets from flickr with flickrapi

- flickrapi can be install from Sybren A. Stüvel (https://github.com/sybrenstuvel/flickrapi)

1. Create an app on your Flickr (https://www.flickr.com/services/apps/create/), for example "Get my photos".
2. Keep generated API key and secret for authentication and authorization.
3. Run script and follow instructions:
  python flickrdownload.py

- You can set extra params to download various size of photo (large, small, original,...)
- This script create folder for each photoset and information about photoset is writen in a XML file (filename is photoset ID)
- General information about each photo in photoset is writen in a XML file (filename is photo ID), all photo sizes are downloaded to photoset folder
