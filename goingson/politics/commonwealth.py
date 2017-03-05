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
URL = 'https://www.commonwealthclub.org/events/rss'
SOURCE = 'Commonwealth Club'

# Functions
def commonwealthXML():
    '''Takes The Commonwealth Club XML string from events RSS, returns DataFrame with cleaned values.

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
        xml_str = urllib2.urlopen(URL, timeout=5).read()
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

    # Within titles, extract titles and dates [format: "title - date", where title may include '-' character]
    dates = [x[x.rfind('-') + 2:] for x in titles]
    titles = [x[:x.rfind('-') - 1] for x in titles]

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(datetime.strptime(date, '%A, %B %d, %Y %I:%M %p'),
                        title, re.sub('(<[^<]+?>|\n|\t)', '', desc).encode('ascii', 'ignore'),
                        [re.sub('Location:\s{0,1}', '', line.encode('ascii', 'ignore'))
                         for line in re.sub('(<[^<]+?>)', '', desc).split('\n')
                         if re.search('Location', line) != None][0], link)
                       for (title, date, desc, link) in zip(titles, dates, descs, links)]) \
        .rename(columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Identify Source
    df['source'] = SOURCE
    df['category'] = 'Politics'

    # Print Success
    sys.stdout.write('\r')
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', SOURCE))
    sys.stdout.flush()

    return df