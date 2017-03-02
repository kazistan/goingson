#!/usr/bin/python

# Import Modules
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import re


# Functions
def sfmomaHTML(html_str='', exhibits=False):
    '''Takes the SF MoMa website, returns DataFrame with cleaned values.

    As a museum, we segregate possible return values into a list of several classes:
        exhibits: date ranges with special artwork
        events: specific events held at the museum (e.g. talks, parties)

    Args
        html_str (str) : html website
        exhibits (bool) : returns exhibits or events at museum

    TODO:
        - build "exhibitions" data structure, should include from and to dates
        - current datetime parse removes event endtime, should be better way to do this

    '''

    # Art Gallery Specific Search Term
    event_type = 'exhibition' if exhibits else 'event'


    # Put XML into BeautifulSoup ResultSet Class
    soup = BeautifulSoup(html_str, 'lxml')

    # Identify All Concerts on APE Website
    shows = [show for show in soup.find_all('div', class_ = 'event-in-list')
              if re.findall('/'+event_type, show.a['href']) and bool(re.search(r'Tour$',show.h6.get_text())) == False]

    # Initialize GOSF Lists
    dates = []
    events = []
    descs = []
    locations = []
    links = []

    # Loop through each art show, scrape and deposit relevant field into each GOSF list
    # Note: Scraping the SFMoMa is challenging - if error for dateClean(show) pass for now
    for show in shows:
        try:
            dates.append(dateClean(show))
            events.append(show.h6.get_text().encode('ascii', 'ignore'))
            descs.append(show.h4.get_text().encode('ascii', 'ignore'))
            locations.append('SFMoMA')
            links.append('https://www.sfmoma.org' + show.a['href'])
        except ValueError:
            pass

    # Put dates to datetime, remove HTML tags from description, and deposit title/link data into DataFrame
    df = pd.DataFrame([(date, event, desc, location, link) for (date, event, desc, location, link)
                       in zip(dates, events, descs, locations, links)])\
        .rename(columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

    # Identify Source
    df['source'] = 'SFMoMA'
    df['category'] = 'Art'

    return df

def multiple_replace(dict, text):
    '''Loops through dictionary of substitutions for regex with text
    :param dict: (dict, str:str) dictionary used for substitutions
    :param text: (str) text for regex manipulation
    :return: (str) with regex substitute over each key from dictionary
    original source: stackoverflow dicussion - http://bit.ly/2jn2cQy
    '''

    # Create a regular expression  from the dictionary keys
    regex = re.compile('(%s)' % '|'.join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda x: dict[x.string[x.start():x.end()]], text)


def dateClean(show):
    '''
    Function to clean up datestrings from beautiful soup objects
    :param show: beautiful soup sfmoma object
    :return: datetime variable
    '''
    # SFMoMa Unique String Substitutions
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    momaDict = dict({day:'' for day in days}.items() + \
                    {'noon':'12:00 pm', '\.':'', ',':'', 'Various Locations':''}.items())

    # Step 1: Build Clean Date String
    datestr = show.find('h5','h5--light no-margin').get_text(separator=' ').replace(u'\u2013', '-')
    # Step 2: Remove days of week and words for times
    datestr = multiple_replace(momaDict, datestr)
    # Step 3: Clip Whitespace
    datestr = datestr[len(datestr) - len(datestr.lstrip()):]
    # Step 4: If hyphen present, split
    if re.search('-', datestr):
        # Step 4a: Find am/pm associated before and after hyphen
        times = re.findall(r'[a/p]\.{0,1}[m]\.{0,1}', datestr[:datestr.index('-')]) + \
                re.findall(r'[a/p]\.{0,1}[m]\.{0,1}', datestr[datestr.index('-'):])
        # If both hours before and after hyphen have am/pm, use first - else use second
        if len(times) > 1:
            datestr = datestr[:datestr.index('-')]
        else:
            datestr = datestr[:datestr.index('-')] + ' ' + times[0]
        datestr = datetime.strptime(re.sub(r'[\.,\s]', '', datestr), '%B%d%Y%I%p')
    # Step 5: If no hyphen present, but hour with no minute present
    elif re.search(r'[a/p]\.{0,1}[m]\.{0,1}', datestr) and not re.search(r'\:',datestr):
        datestr = datetime.strptime(re.sub(r'[\.,\s]', '', datestr), '%B%d%Y%I%p')
    # Step 5: If no hyphen present, but hour with and minute present
    elif re.search(r'[a/p]\.{0,1}[m]\.{0,1}', datestr):
        datestr = datetime.strptime(re.sub(r'[\.,\s]', '', datestr), '%B%d%Y%I:%M%p')
    # Step 6: If no hour present
    else:
        datestr = datetime.strptime(re.sub(r'[\.,\s]', '', datestr), '%B%d%Y')
    return datestr