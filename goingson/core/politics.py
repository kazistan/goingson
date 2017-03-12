#!/usr/bin/python

"""
Politics child classes of Goings On
"""

import goingson

CATEGORY = 'Politics'

class Commonwealth(goingson.GoingsOn):
	'''
	The Commonwealth Club of California: San Francisco

	Address
	-------
	555 Post Street
	San Francisco, CA 94102-9824

	Office Hours
	------------
	Mon-Thu: 10am-5pm
	Fri: 10am-2pm

	Contact
	-------
	Phone: 415.597.6700
	Email: info@commonwealthclub.org

	Website
	-------
	https://www.commonwealthclub.org/about
		(Accessed on March 12, 2017)
	'''

	URL = 'https://www.commonwealthclub.org/events/rss'
	SOURCE = 'Commonwealth Club'
	CATEGORY = CATEGORY

	def parse_url(self):
		'''
		Parses web scrape into class attributes.
		'''

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object unless scrape error
		try:
			soup = goingson.BeautifulSoup(html_str, 'xml')
		except TypeError:
			return None

		# Identify Items
		events = soup.find_all('item')

		# Loop through each event, scrape and deposit
		for event in events:

			dateStr, title, desc, loc = self.extract_variables(event)

			self.dates.append(dateStr)
			self.titles.append(title)
			self.descs.append(desc)
			self.locations.append(loc)
			self.links.append(event.find('link').text)

		# Print Status
		self.stdoutWrite(True)

		return None

	def extract_variables(self, event):
		'''
		Returns DateTime object, event title, description, and location for BeautifulSoup text

		Parameters
		----------
		event : BeautifulSoup Object

		Returns
		-------
		dateStr : DateTime Object
		title : str
		desc : str
		loc : str
		'''

		# Isolate Datestring
		dateStr = event.find('title').text[event.find('title').text.rfind('-')+2:]

		# Format Datestring
		dateStr = goingson.datetime.strptime(dateStr, '%A, %B %d, %Y %I:%M %p')

		# Extract Title
		title = event.find('title').text[:event.find('title').text.rfind('-')-1].encode('ascii','ignore')

		# Remove HTML elements from Description
		desc = goingson.re.sub('(<[^<]+?>|\n|\t)', '',
			event.find('description').text).encode('ascii','ignore').replace('\r', ' ')

		# Identify Location
		loc = [goingson.re.sub('Location:\s{0,1}', '', line.encode('ascii', 'ignore'))
				for line in goingson.re.sub('(<[^<]+?>)', '', event.text)
				.split('\n') if goingson.re.search('Location', line) != None][0]

		return dateStr, title, desc, loc

class WorldAffairsCouncil(goingson.GoingsOn):
	'''
	World Affairs Council of Northern California

	Address
	-------
	312 Sutter Street, Suite 200
	San Francisco, CA 94108

	Contact
	-------
	Phone: 415.293.4600

	Website
	-------
	https://www.worldaffairs.org/about-us
		(Accessed on March 12, 2017)
	'''

	URL = 'http://www.worldaffairs.org/events?format=feed'
	SOURCE = 'World Affairs Council'
	CATEGORY = CATEGORY

	def parse_url(self):
		'''
		Parses web scrape into class attributes.
		'''

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object
		try:
			soup = goingson.BeautifulSoup(html_str, 'xml')
		except TypeError:
			return None

		# Identify Events
		events = soup.find_all('item')

		# Loop through each event, scrape and deposit relevant field into each GOSF list
		for event in events:
			
			dateStr, loc, desc = self.desc_parse(event.description.text)

			self.dates.append(dateStr)
			self.titles.append(event.title.text)
			self.descs.append(desc)
			self.locations.append(loc)
			self.links.append(event.link.text)

		# Print Status
		self.stdoutWrite(True)

		return None

	def desc_parse(self, desc):
		'''
		Returns DateTime Object, Location, and Description of Event.

		Parameters
		----------
		desc : str

		Returns
		-------
		dateStr: DateTime Object
		loc: str
		description: str
		'''

		# List relevant html timestamp syntax
		tStart, tEnd, iStart = '<time datetime=', '<time>', '<img'

		# Isolate Datestring
		dateStr = desc[desc.index(tStart) + len(tStart) : desc.index(tEnd)]

		# Extract Date using Datetime Methods
		dateStr = goingson.datetime.strptime(''.join(dateStr.split(' ')[:5]), '"%a,%d%b%Y%H:%M:%S')

		# Extract Location using <img> location + regex
		loc = goingson.re.sub('(<[^<]+?>|\n|\t)', '', desc[desc.index(tEnd):desc.index(iStart)])

		# Extract Description
		description = goingson.re.sub('(<[^<]+?>|\n|\t)', '', desc[desc.index(iStart):]).strip()

		return dateStr, loc, description
