''' 
	@sandeep007
   
		Made for fun purpose only, Bing wallpapers are really cool and usually downloading picture of day could be tedious task so this py script can come handy in dowloading 
		the image and setting it as the desktop wallpaper. (For linux)

        NOTE: if this script doesn't work and showing message something like this :
        GLib-GIO-Message: Using the 'memory' GSettings backend.  Your settings will not be saved or shared with other applications

        Try this command: export GIO_EXTRA_MODULES=/usr/lib/x86_64-linux-gnu/gio/modules/
'''

import os
import re
import time
import json
import requests
import urllib.request

# JSON data of bing page can be found on this page
page = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"

try:
    with urllib.request.urlopen(page) as url:
        data = json.loads(url.read().decode())
        #print(data)
        image_url = 'http://www.bing.com' + data['images'][0]['url']
        #print (image_url)
        
        imageDownload = 'http://www.bing.com/hpwp/' + data['images'][0]['hsh']
        #print (imageDownload)

        imageName = image_url[re.search("rb/", image_url).end():re.search('_EN', image_url).start()] + '.jpg'
        #print (imageName)
        
        path = os.environ['HOME'] + '/Pictures/Bing_Pic_of_the_Day/'
        
        if not os.path.exists(path):
            os.makedirs(path)

        path = path + imageName
        #print (path)

        if os.path.exists(path) is False:
            
            try:
                urllib.request.urlretrieve(imageDownload,path)
            except urllib.error.HTTPError:
                urllib.request.urlretrieve(image_url,path)

            Description = data['images'][0]['copyright']
            #print (Description)

            command = 'gsettings set org.gnome.desktop.background picture-uri file://'+path
            os.system(command)

            notification = 'notify-send -u critical "Wallpaper for the Day updated!" "' + Description + '"'
            os.system(notification)

        else:
            # if wallpaper for the day is already upadted
            notification = 'notify-send -u critical "Bing Wallpaper" "Wallpaper for the day has been updated already!"'
            os.system(notification)

except:
    notification = 'notify-send -u critical "Bing Wallpaper" "Wallpaper can\'t be updated!"'
    os.system(notification)

