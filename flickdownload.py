'''https://github.com/n0c3rt/flickrdownload'''
import os
import flickrapi
import webbrowser
from lxml import etree
import urllib.request

#Your API key and secret from Flickr account
api_key = u''
api_secret = u''
#Your user ID
user_id = ''
if(not api_key or not api_secret or not user_id):
    print("Missing api_key, api_secret or user_id!")
    exit()
    
#Folder name for photoset
folder_name = 'photoset'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
print('Authentication...')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='read'):
    flickr.get_request_token(oauth_callback='oob')
    authorize_url = flickr.auth_url(perms='read')
    print (authorize_url)
    webbrowser.open_new_tab(authorize_url)
    print ("Paste this URL in your browser to get Verifier code: "+authorize_url)
    verifier = str(input('Verifier code: '))
    flickr.get_access_token(verifier)

print('Creating photosets folder ...')
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
### uncomment following 4 lines for ovewriting photoset folder
#else:
#    import shutil
#    shutil.rmtree(folder_name)
#    os.mkdir(folder_name)

photosets = flickr.photosets.getList(user_id=user_id)
count = 1

#extra prams for photo
extra_params = [
    ### uncomment params, which you want to get, by default, using 'url_o' - URL of original size image

    #'date_taken', # Date item was taken
    #'date_upload', #Date item was uploaded
    #'geo', #Geotagging latitude, longitude and accuracy
    #'icon_server', #Item owner icon fields
    #'last_update', #Date item was last updated
    #'license', #Item License
    #'machine_tags', #Machine tags
    #'media', #Item Format: photo or video
    #'o_dims', #Original item dimensions
    #'original_format', #Original item secret and format
    #'owner_name', #Item owner ID
    #'path_alias', #Path alias for owner like /photos/USERNAME
    #'tags', #Item clean tags (safe for HTML, URLs)
    #'url_c', #URL of medium 800, 800 on longest size image
    #'url_m', #URL of small, medium size image
    #'url_n', #URL of small, 320 on longest side size image
    'url_o', #URL of original size image
    #'url_q', #URL of large square 150x150 size image
    #'url_s', #URL of small suqare 75x75 size image
    #'url_sq', #URL of square size image
    #'url_t', #URL of thumbnail, 100 on longest side size image
    #'views', #Number of times item has been viewed
]

for photoset in photosets[0]:
    attrib = photoset.attrib
    print('=== Download photoset '+ attrib['id'] + ': ' + str(count) + ' of '+ photosets[0].attrib['total'] + ' ===')
    count = count + 1
    print('Creating folder for photoset id ' + attrib['id'] + '...')
    os.mkdir(folder_name + '/'+attrib['id'])
    #'Writing information of photoset to XML file 
    tree = etree.ElementTree(photoset)
    tree.write(folder_name + '/'+attrib['id']+ '/' +attrib['id']+'.xml')
    photos_count = photoset.attrib['photos']
    item = 1
    extra_info = ','.join(extra_params)
    walk_set = flickr.walk_set(attrib['id'], extras=extra_info)
    for p in walk_set:
        photo_id = str(p.get('id'))
        
        photo = etree.ElementTree(p)
        photo.write(folder_name + '/'+attrib['id']+ '/' + photo_id + '.xml')
        
        print('Getting urls from photo ' + photo_id + ': ' + str(item) + ' of ' + str(photos_count) + '...')
      
        download_link = [param for param in extra_params if "url" in param]
        if not download_link:
            break
        print(download_link)
        for link in download_link:
            download_complete = False
            while(not download_complete):
                url = p.get(link)
                filename = folder_name + '/'+attrib['id']+ '/' + p.get(link).split('/')[-1] 
                try:
                    print('Downloading ' + url)    
                    urllib.request.urlretrieve(url,filename)
                    download_complete = True     
                except urllib.error.ContentTooShortError: 
                    print('Download ' + url + ' failed, retry... ')    
        item = item + 1
        break
    print('=== Download photoset ' + attrib['id'] + ' completed! ===')
    break
print('=== All photosets downloaded! ===')
