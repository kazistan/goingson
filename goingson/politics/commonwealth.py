#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
from datetime import datetime
import re as re
import xml.etree.ElementTree as et


# Functions
def commonwealthXML(xml_str):
    '''Takes The Commonwealth Club XML string from events RSS, returns DataFrame with cleaned values.

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
    df['source'] = 'Commonwealth Club'; df['category'] = 'Politics'

    return df