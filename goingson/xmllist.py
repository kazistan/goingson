#!/usr/bin/python

# Import Moduels
import urllib2

# Define XML variables
url_str = 'https://www.commonwealthclub.org/events/rss'
cwc = urllib2.urlopen(url_str).read()
url_str = 'http://www.worldaffairs.org/events?format=feed'
request = urllib2.Request(url_str)
request.add_header('User-Agent', 'Mozilla/4.0')
opener = urllib2.build_opener()
wac = opener.open(request).read()

# Define HTML variables
url_str = 'http://apeconcerts.com/'
request = urllib2.Request(url_str)
request.add_header('User-Agent', 'Mozilla/4.0')
opener = urllib2.build_opener()
ape = opener.open(request).read()