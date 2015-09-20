import os
import sys
import time
from urllib import FancyURLopener
import urllib2
import simplejson

# Define search term
searchTerm = "normal flat mole"#str(sys.argv[1])
outfile = "test.txt" #str(sys.argv[2])

target = open(outfile,'w')

# Replace spaces ' ' in search term for '%20' in order to comply with request
searchTerm = searchTerm.replace(' ','%20')

target.write
# Set count to 0
count= 0

for i in range(0,100):
    # Notice that the start changes for each iteration in order to request a new set of images for each loop
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
    print url
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)

    # Get results using JSON
    results = simplejson.load(response)
    data = results['responseData']
    dataInfo = data['results']

    # Iterate for each result and get unescaped url
    for myUrl in dataInfo:
        count = count + 1
        if ".jpg" in str(myUrl['unescapedUrl']):
            target.write(str(myUrl['unescapedUrl']))
            target.write("\n")
            print myUrl['unescapedUrl']

        #myopener.retrieve(myUrl['unescapedUrl'],str(count)+'.jpg')

    # Sleep for one second to prevent IP blocking from Google
    time.sleep(2)
	
target.close()