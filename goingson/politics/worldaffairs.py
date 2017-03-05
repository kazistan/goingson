#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
import re as re
import xml.etree.ElementTree as et
import urllib2
import sys
from datetime import datetime

# Global Variables
URL = 'http://www.worldaffairs.org/events?format=feed'
SOURCE = 'World Affairs Council'

# Functions

def worldaffairsXML():
    '''Takes the World Affairs Council XML string from events RSS, returns DataFrame with cleaned values.

    Parameters
    ----------
        xml_str : str
            string of XML RSS feed, imported using urllib2

    Dependencies
    ------------
        xml.etree.ElementTree as ET - ElementTree class from XML, used to build tree & child nodes of XML
        datetime as datetime - datetime class, primarily methods that parse date-strings
        re as re - regular expressions
        pandas as pd - pandas method

    '''

    # Print Status
    sys.stdout.write("[%-2s] %s" % ('', SOURCE))
    sys.stdout.flush()

    # Load Website, max 5 second timeout
    try:
        request = urllib2.Request(URL)
        request.add_header('User-Agent', 'Mozilla/4.0')
        opener = urllib2.build_opener()
        xml_str = opener.open(request, timeout=4).read()
    except urllib2.URLError:
        sys.stdout.write('\r')
        sys.stdout.write("[%-4s] %s\n" % ('\033[91m' + 'fail' + '\033[0m', SOURCE))
        sys.stdout.flush()
        return None

    # Put XML into ElementTree class
    root = et.fromstring(xml_str)

    # Identify all titles, descriptions, and links; Commonwealth XML puts these into child-nodes of item
    titles = [child.find('title').text.encode('ascii','ignore') for child in root.iter('item')]
    descs = [child.find('description').text for child in root.iter('item')]
    links = [child.find('link').text for child in root.iter('item')]

    # From descriptions, we'll extract dates, locations, and actual descriptions by using HTML tags
    dates = []
    locations = []
    fDescs = []

    for desc in descs:
        # Identify the start & end of a time stamp
        tStart = '<time datetime='
        tEnd = '<time>'
        iStart = '<img'

        # Isolate the date string
        dateStr = desc[desc.index(tStart) + len(tStart): desc.index(tEnd)]

        # Extract date using datetime.strftime method and directives
        date = datetime.strptime(''.join(dateStr.split(' ')[:5]), '"%a,%d%b%Y%H:%M:%S')

        # Extract location using <img> location and RE to remove all tags
        loc = re.sub('(<[^<]+?>|\n|\t)', '', desc[desc.index(tEnd):desc.index(iStart)]).encode('ascii', 'ignore')

        # Extract description
        fullDesc = re.sub('(<[^<]+?>|\n|\t)', '', desc[desc.index(iStart):]).encode('ascii', 'ignore')

        # Deposit into list
        dates.append(date)
        locations.append(loc)
        fDescs.append(fullDesc)

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(date, title, desc, loc, link) for (date, title, desc, loc, link) in
                       zip(dates, titles, fDescs, locations, links)]).rename(
        columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Define Categorical Variables
    df['source'] = 'World Affairs Council'
    df['category'] = 'Politics'

    # Print Success
    sys.stdout.write('\r')
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', SOURCE))
    sys.stdout.flush()

    return df