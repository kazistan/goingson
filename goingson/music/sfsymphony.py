#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import urllib2
import sys
import re

# Global Variables
URL = 'http://www.sfsymphony.org/Buy-Tickets/Calendar.aspx'
SOURCE = 'San Francisco Symphony'

# Functions
def sfsymphonyHTML():
    '''Generates Data Frame of Schedule from Current Month's Performances
    :return: DataFrame for Goings On List'''

    # Print Status
    sys.stdout.write("[%-2s] %s" % ('', SOURCE))
    sys.stdout.flush()

    # Load Webpage
    html_str = scrapeWebsite(url=URL)

    # Put XML into BeautifulSoup ResultSet Class
    soup = BeautifulSoup(html_str, 'lxml')

    # Identify all Concerts for SFSymphony
    shows = [show for show in soup.find_all('div', class_='calendar-events-details')]

    # Initialize GOSF Lists
    dates = []
    events = []
    descs = []
    locations = []
    links = []

    # Loop through each art show, scrape and deposit relevant field into each GOSF list
    for show in shows:
        # Get List of Dates
        dt_range = sfsDateClean(show)
        n = len(dt_range)
        dates += dt_range
        events += [show.h3.text.encode('ascii', 'ignore').strip()] * n
        descs += ['INSERT DESCRIPTION FROM LINK'] * n
        locations += ['Davies Symphony Hall, 201 Van Ness Ave San Francisco, CA 94102'] * n
        links += ['https://www.sfsymphony.org' + show.h3.a['href']] * n

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(date, event, desc, location, link) for (date, event, desc, location, link)
                       in zip(dates, events, descs, locations, links)]) \
        .rename(columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Identify Source
    df['source'] = SOURCE;
    df['category'] = 'Music'

    # Print "ok" result
    sys.stdout.write('\r')
    sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', SOURCE))
    sys.stdout.flush()

    return df


def sfsDateClean(event):
    '''Takes BeautifulSoup Event, Returns list of Dates
    :param event:BeautifulSoup Object - soup object scraped from SFSymphony Website
    :return: list of dates
    '''

    # Extract Date
    dt = event.h6.text.encode('ascii', 'ignore')

    # 0: Identify if Date Range (i.e. has "-")
    is_range = bool(re.search('-', dt))

    # If True:
    if bool(re.search('-', dt)):

        # 1: Start Date & Adjust Year
        start_dt = datetime.strptime(re.sub(r'\W', '', dt[:dt.index('-')]), '%A%B%d') \
            .replace(year=datetime.today().year)

        # 2: End Date & Adjust Year
        end_dt = datetime.strptime(re.sub(r'\W', '', dt[dt.index('-'):]), '%A%B%d') \
            .replace(year=datetime.today().year)

        # 3: Build Index Range
        dt_range = [start_dt + timedelta(days=x) for x in range(0, (end_dt - start_dt).days + 1)]

    else:

        # If False:
        dt_range = [datetime.strptime(re.sub(r'\W', '', dt), '%A%B%d').replace(year=datetime.today().year)]

    return dt_range

def scrapeWebsite(url, headers={'User-Agent':'Mozilla/4.0'}):
    '''Returns HTML file scraped from website for use in BeautifulSoup scrape
    :param url:str - url of target website
    :param headers:dict - dictionary of header files
    :return:str - html of website
    '''

    # Build Request
    request = urllib2.Request(url)

    # Add Headers
    for key, value in headers.iteritems():
        request.add_header(key, value)

    # Connect to Website
    opener = urllib2.build_opener()
    result = opener.open(request).read()

    return result