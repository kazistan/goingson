#!/usr/bin/python

"""
Data Structure for 5-feature web-scrape and various package operations
"""

import urllib2
import sys
import os
import socket
import ssl
import pandas as pd
import re as re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# Define GoingsOn Class

class GoingsOn(object):
	'''
	Data Structure for 5-feature web-scrape and package operations.

	Abstract Class used to construct child GoingsOn classes.  All instance
	attributes are 1-n lists which the parse_url() method deposits from
	the scrapeWebiste() method.  The parse_url() method is defined within each
	child class according to the scraping requirements for each website.

	All other methods detailed below are used within the parse_url() method
	or output results to a different data stucture (e.g. toDF() for a
	Pandas DataFrame).

	Parameters
	----------
	dates : list, DateTime dates
	    Dates for each event
	titles : list, str
	    Title of event
	descs: list, str
	    Description of event
	locations: list, str
	    Location of event (default value SOURCE)
	link: list, str
	    Link to event on website
	'''

	URL = ''
	SOURCE = ''
	CATEGORY = ''

	def __init__(self):

		self.dates = []
		self.titles = []
		self.descs = []
		self.locations = []
		self.links = []
		self.parse_url()

	def scrapeWebsite(self, headers={'User-Agent':'Mozilla/4.0'}):
		'''
		Returns text from website scrape using urllib2.

		This method builds a url request defaulting to a simple browser header.
		Request is made to the URL variable with a 4 second timeout, in case
		the website is under maintenance.

		If request hangs, print [fail] to stdout.

		Parameters
		----------
		headers : dict
			Dictionary of headers to pass to urllib2 request builder

		Returns
		-------
		result : str
			Text of scraped website

		'''
		try:
			# Build Request
			request = urllib2.Request(self.URL)

			# Add Headers
			for key, value in headers.iteritems():
				request.add_header(key, value)

			# Connect to Website
			opener = urllib2.build_opener()
			result = opener.open(request, timeout=4).read()
			return result

		except (urllib2.URLError, socket.timeout, ssl.SSLError):
			self.stdoutWrite(False)
			return None


	def stdoutWrite(self, success=True):
		'''
		Writes colored status to stdout.

		Parameters
		----------
		success : bool or None
			Boolean indicates completion/failure of operation.  None
			leaves status box empty
		'''

		if success not in {True, False, None}:
			raise ValueError('Success must be boolean or NoneType')
		elif success == None:
			sys.stdout.write("[%-2s] %s" % ('', self.SOURCE))
			sys.stdout.flush()
		elif success == True:
			sys.stdout.write('\r')
			sys.stdout.write("[%-2s] %s\n" % ('\033[92m' + 'ok' + '\033[0m', self.SOURCE))
			sys.stdout.flush()
		else:
			sys.stdout.write('\r')
			sys.stdout.write("[%-4s] %s\n" % ('\033[91m' + 'fail' + '\033[0m', self.SOURCE))
			sys.stdout.flush()

		return None

	def toDF(self):
		'''
		Writes instance arguments to a Pandas DataFrame.

		Returns
		-------
		df : Pandas DataFrame
		'''

		df = pd.DataFrame([(date, title, desc, loc, link) for (date, title, desc, loc, link) in 
			zip(self.dates, self.titles, self.descs, self.locations, self.links)]).rename(
			columns={0: 'date', 1: 'event', 2: 'desc', 3: 'location', 4: 'link'})

		# Define Categorical Variables
		df['source'] = self.SOURCE
		df['category'] = self.CATEGORY

		return df

def printSection(CATEGORY='start'):
	'''
	Writes section title to stdout.

	Cosmetic function to help user visualize status of web scrapes.

	Parameters
	----------
	CATEGORY : str
		String takes either "start", "end", or global CATEGEORY variable
	'''

	if CATEGORY == 'start':
		sys.stdout.write("%s\n" % ('-' * len('Goings On About San Francisco')) +
			"Goings On About \033[94mSan Francisco\033[0m\n" +
			"%s\n" % ('-' * len('Goings On About San Francisco')))

	elif CATEGORY == 'end':
		message = 'File Saved to ' + sys.argv[1] + 'goingson.csv'
		sys.stdout.write("\n%s\n%s\n%s\n" % ('-'*len(message), message, '-'*len(message)))

	else:
		sys.stdout.write("\n%-20s\n" % ('-'*((20-len(' ' + CATEGORY + ' '))/2) + 
			' ' + CATEGORY + ' ' + '-'*((20-len(' ' + CATEGORY + ' '))/2)))

	return None

def combine_results(goingsonsf):
	'''
	Build single data structure of GoingsOn results starting from today.

	Parameters
	----------
	goingsonsf : Pandas DataFrame
		DataFrame from GoingsOn child classes

	Returns
	-------
	goingsonsf : Pandas DataFrame
		Single DataFrame of all events, starting from today

	'''

	# Concatinate
	goingsonsf = pd.concat(goingsonsf, axis=0)
	goingsonsf.sort_values('date', inplace = True)
	goingsonsf.index = range(len(goingsonsf.index))

	# Drop events before today
	dt = datetime.today()
	goingsonsf = goingsonsf[goingsonsf.date >= pd.datetime.today()]

	return goingsonsf[['date', 'event', 'desc', 'location', 'link', 'source', 'category']]

def outputResults(goingson_df, arg1=sys.argv[1]):
	'''
	Outputs GoingsOn resutls to passed directory from commandline arguments

	Parameters
	----------
	goingson_df : Pandas DataFrame
		DataFrame of a GoingsOn child class
	arg1 : str
		Output directory retrieved from commandline arguments
	'''

	# Check if valid directory is given
	try:
		arg1 = sys.argv[1]
	except IndexError:
		print("Usage: main.py <directory>")
		sys.exit(1)
	
	assert os.path.isdir(arg1), '<directory> is not absolute path: %r' % arg1

	# Writeout if no assertion raised
	goingson_df.to_csv(arg1 + 'goingson.csv', encoding='utf-8', index=False)

	return None
