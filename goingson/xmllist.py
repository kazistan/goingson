#!/usr/bin/python

# Import Moduels
import urllib2
import sys

# Start
########
sys.stdout.write("%s\n" % ('-'*len('Goings On About San Francisco')) +
                 "Goings On About \033[94mSan Francisco\033[0m\n" +
                 "%s\n" % ('-'*len('Goings On About San Francisco')) +
                 "[%-2s] %s" % ('', 'Scraping Websites'))
sys.stdout.flush()

# Define XML variables
# ####################
#
# Commonwealth
url_str = 'https://www.commonwealthclub.org/events/rss'
cwc = urllib2.urlopen(url_str).read()
# World Affairs Council
url_str = 'http://www.worldaffairs.org/events?format=feed'
request = urllib2.Request(url_str)
request.add_header('User-Agent', 'Mozilla/4.0')
opener = urllib2.build_opener()
wac = opener.open(request).read()

# Define HTML variables
########################
#
# Another Planet Entertainment
url_str = 'http://apeconcerts.com/'
request = urllib2.Request(url_str)
request.add_header('User-Agent', 'Mozilla/4.0')
opener = urllib2.build_opener()
ape = opener.open(request).read()
# Filmore
url_str = 'http://thefillmore.com/calendar/'
request = urllib2.Request(url_str)
request.add_header('User-Agent', 'Mozilla/4.0')
opener = urllib2.build_opener()
fillmore = opener.open(request).read()
# SFMoMa
#url_str = 'https://www.sfmoma.org/exhibitions-events/?days=30'
#request = urllib2.Request(url_str)
#request.add_header('User-Agent', 'Mozilla/4.0')
#opener = urllib2.build_opener()
#sfmoma = opener.open(request).read()

# End
#####
sys.stdout.write('\r')
sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', 'Scraping Websites'))
sys.stdout.flush()