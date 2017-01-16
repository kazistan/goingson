#!/usr/bin/python

# Import Modules
from __future__ import print_function
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


# Functions
def fillmoreHTML(html_str=''):
    '''Takes the Fillmore website, returns DataFrame with cleaned values.

    Args
        html_str (str) : html website

    '''

    # Put XML into BeautifulSoup ResultSet Class
    soup = BeautifulSoup(html_str, 'lxml')

    # Identify All Concerts on APE Website
    concerts = soup.find_all('div', class_ = 'faq_main calendar')
    showdates = soup.find_all('div', class_ = 'date-show')

    # Initialize GOSF Lists
    dates = []
    events = []
    descs = []
    locations = []
    links = []

    # Loop through each concert, scrape and deposit relevant field into each GOSF list
    for concert in concerts:
        datestr = concert.find(class_='content').get_text()
        datestr = datetime.strptime(datestr[:datestr.index('//')].replace('.',''),
                                    '%A, %B %d, %YDoors %I:%M %p ')
        dates.append(datestr)
        events.append(concert.find(class_='title').get_text().encode('ascii','ignore'))
        descs.append('INSERT DESCRIPTION FROM LINK Follow-up')
        locations.append('The Fillmore')
        links.append(concert.a['href'])

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(date, event, desc, location, link) for (date, event, desc, location, link)
                       in zip(dates, events, descs, locations, links)])\
        .rename(columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Identify Source
    df['source'] = 'The Fillmore'; df['category'] = 'Music'

    return df