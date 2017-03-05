#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import urllib2
import sys

# Global Variables
URL = 'http://apeconcerts.com/'
SOURCE = 'Another Planet Entertainment'

# Functions
def apentertainmentHTML():
    '''Takes The Another Planet Entertainment website, returns DataFrame with cleaned values.

    This function scrapes the calendar section of the Bay-Area concert production company's website.  Since APE does
    not provide an RSS feed for XML parsing, we use BeautifulSoup to scrape the website.

    Args
        html_str (str) : html website

    '''

    # Print Status
    sys.stdout.write("[%-2s] %s" % ('', SOURCE))
    sys.stdout.flush()

    # Load Website, max 5 second timeout
    try:
        request = urllib2.Request(URL)
        request.add_header('User-Agent', 'Mozilla/4.0')
        opener = urllib2.build_opener()
        html_str = opener.open(request, timeout=4).read()
    except urllib2.URLError:
        sys.stdout.write('\r')
        sys.stdout.write("[%-4s] %s\n" % ('\033[91m' + 'fail' + '\033[0m', SOURCE))
        sys.stdout.flush()
        return None

    # Put XML into BeautifulSoup ResultSet Class
    soup = BeautifulSoup(html_str, 'lxml')

    # Identify All Concerts on APE Website
    concerts = soup.find_all('div', class_ = 'entry')
    showdates = soup.find_all('div', class_ = 'date-show')

    # Initialize GOSF Lists
    dates = []
    events = []
    descs = []
    locations = []
    links = []

    # Loop through each concert, scrape and deposit relevant field into each GOSF list
    for concert, showdate in zip(concerts, showdates):
        dates.append(showdate['content'])
        events.append(concert.h2.get_text())
        descs.append('INSERT DESCRIPTION FROM LINK Follow-up')
        locations.append(concert.find(class_='venue-location-name').get_text())
        links.append(concert.a['href'])

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(datetime.strptime(date, '%B %d, %Y %I:%M%p'), event.encode('ascii', 'ignore'),
                        desc.encode('ascii','ignore'), location.encode('ascii','ignore'), link)
                       for (date, event, desc, location, link) in zip(dates, events, descs, locations, links)])\
        .rename(columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Identify Source
    df['source'] = SOURCE
    df['category'] = 'Music'

    # Print Success
    sys.stdout.write('\r')
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', SOURCE))
    sys.stdout.flush()

    return df