#!/usr/bin/python

"""
Music child classes of Goings On
"""

import goingson

CATEGORY = 'Music'

class Fillmore(goingson.GoingsOn):
	'''
	The Fillmore

	Address
	-------
	1805 Geary Blvd
	San Francisco, CA 94115

	Contact
	-------
	Phone: 415.346.3000
	Email: thefillmore@livenation.com

	Website
	-------
	http://thefillmore.com/faq/
		(Accessed on March 12, 2017)
	'''

	URL = 'http://thefillmore.com/calendar/'
	SOURCE = 'The Fillmore'
	CATEGORY = CATEGORY

	def parse_url(self):
		'''
		Parses web scrape into class attributes.
		'''

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object unless scrape failes
		try:
			soup = goingson.BeautifulSoup(html_str, 'lxml')
		except TypeError:
			return None

		# Identify All Events
		concerts = soup.find_all('div', class_ = 'faq_main calendar')

		# Loop through each concert, scrape and deposit relevant field into each GOSF list
		for concert in concerts:
			datestr = concert.find(class_='content').get_text()
			datestr = goingson.datetime.strptime(datestr[:datestr.index('//')].replace('.',''),
				'%A, %B %d, %YDoors %I:%M %p ')
			self.dates.append(datestr)
			self.titles.append(concert.find(class_='title').get_text().encode('ascii','ignore'))
			self.descs.append('INSERT DESCRIPTION FROM LINK Follow-up')
			self.locations.append(self.SOURCE)
			self.links.append(concert.a['href'])

		# Print Status
		self.stdoutWrite(True)

		return None

class APE(goingson.GoingsOn):
	'''
	Another Planet Entertainment

	Venues
	------
	Greek Theatreat atUC Berkeley, Bill Graham Civic Auditorium, The Independent, Fox Theater Oakland,
	Lake Tahoe Outdoors at Harveys, Outside Lands in Golden Gate Park, Treasure Island Music Festival,

	Contact
	-------
	Email: contact@anotherplanetent.com

	Website
	-------
	http://apeconcerts.com/about/
		(Accessed on March 11, 2017)
	'''

	URL = 'http://apeconcerts.com/'
	SOURCE = 'Another Planet Entertainment'
	CATEGORY = CATEGORY

	def parse_url(self):
		'''
		Parses web scrape into class attributes.
		'''

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object unless scrape failes
		try:
			soup = goingson.BeautifulSoup(html_str, 'lxml')
		except TypeError:
			return None

		# Identify All Events
		concerts = soup.find_all('div', class_ = 'entry')
		showdates = soup.find_all('div', class_ = 'date-show')

		# Loop through each concert, scrape and deposit relevant field into each GOSF list
		for concert, showdate in zip(concerts, showdates):
			self.dates.append(goingson.datetime.strptime(showdate['content'], '%B %d, %Y %I:%M%p'))
			self.titles.append(concert.h2.get_text().encode('ascii','ignore'))
			self.descs.append('INSERT DESCRIPTION FROM LINK Follow-up')
			self.locations.append(concert.find(class_='venue-location-name').get_text().encode('ascii','ignore'))
			self.links.append(concert.a['href'])

		# Print Status
		self.stdoutWrite(True)

		return None

class SFSymphony(goingson.GoingsOn):
	'''
	San Francisco Symphony

	Address
	-------
	201 Van Ness Ave
	San Francisco, CA 94102

	Box Office Hours
	----------------
	Mon-Fri: 10am-6pm
	Sat: 12pm-6pm
	Sun: 2hrs prior to concert

	Contact
	-------
	Phone: 415.864.6000
	Email: patronservices@sfsymphony.org

	Website
	-------
	http://www.sfsymphony.org
		(Accessed on March 12, 2017)
	'''

	URL = 'http://www.sfsymphony.org/Buy-Tickets/Calendar.aspx'
	SOURCE = 'San Francisco Symphony'
	CATEGORY = CATEGORY

	def parse_url(self):
		'''
		Parses web scrape into class attributes.
		'''

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object unless scrape failes
		try:
			soup = goingson.BeautifulSoup(html_str, 'lxml')
		except TypeError:
			return None

		# Identify All Events
		shows = [show for show in soup.find_all('div', class_='calendar-events-details')]

		# Loop through each concert, scrape and deposit relevant field into each GOSF list
		for show in shows:
			# Get List of Dates
			dt_range = self.sfsDateClean(show)
			n = len(dt_range)
			self.dates += dt_range
			self.titles += [show.h3.text.encode('ascii', 'ignore').strip()] * n
			self.descs += ['INSERT DESCRIPTION FROM LINK'] * n
			self.locations += ['Davies Symphony Hall, 201 Van Ness Ave San Francisco, CA 94102'] * n
			self.links += ['https://www.sfsymphony.org' + show.h3.a['href']] * n

		# Print Status
		self.stdoutWrite(True)

		return None

	def sfsDateClean(self, event):
		'''
		Returns DateTime index from beautiful soup text

		Parameters
		----------
		event : BeautifulSoup obejct

		Returns
		-------
		dateStr : DateTime Index
		'''

		# Extract Date
		dt = event.h6.text.encode('ascii', 'ignore')

		# Identify if Date Range (i.e. has "-")
		if bool(goingson.re.search('-', dt)):

			# 1: Start Date & Adjust Year
			start_dt = goingson.datetime.strptime(goingson.re.sub(r'\W', '', dt[:dt.index('-')]), '%A%B%d') \
			    .replace(year=goingson.datetime.today().year)

			# 2: End Date & Adjust Year
			end_dt = goingson.datetime.strptime(goingson.re.sub(r'\W', '', dt[dt.index('-'):]), '%A%B%d') \
			    .replace(year=goingson.datetime.today().year)

			# 3: Build Index Range
			dt_range = [start_dt + goingson.timedelta(days=x) for x in range(0, (end_dt - start_dt).days + 1)]

		else:

			# If False:
			dt_range = [goingson.datetime.strptime(goingson.re.sub(r'\W', '', dt), '%A%B%d').replace(year=goingson.datetime.today().year)]

		return dt_range
