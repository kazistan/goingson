#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


# Functions
def apentertainmentHTML(html_str=''):
    '''Takes The Another Planet Entertainment website, returns DataFrame with cleaned values.

    This function scrapes the calendar section of the Bay-Area concert production company's website.  Since APE does
    not provide an RSS feed for XML parsing, we use BeautifulSoup to scrape the website.

    Args
        html_str (str) : html website

    '''

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
    df['source'] = 'Another Planet Entertainment'; df['category'] = 'Music'

    return df