#!/usr/bin/python

"""
Art sub-classes of Goings On Wedscrape Class
"""

import goingson

CATEGORY = 'Art'

class SFMoMA(goingson.GoingsOn):

	URL = 'https://www.sfmoma.org/exhibitions-events/?days=30'
	SOURCE = 'SFMoMA'
	CATEGORY = CATEGORY

	def parse_url(self):

		# Print Status
		self.stdoutWrite(None)

		# Scrape Website
		html_str = self.scrapeWebsite()

		# Put into BeautifulSoup Object unless scrape error
		try:
			soup = goingson.BeautifulSoup(html_str, 'lxml')
		except TypeError:
			return None

		# Identify Items
		event_type = 'event'
		events = [show for show in soup.find_all('div', class_ = 'event-in-list') 
			if goingson.re.findall('/'+event_type, show.a['href']) 
			and bool(goingson.re.search(r'Tour$',show.h6.get_text())) == False]

		# Loop through each event, scrape and deposit
		for event in events:
			try:
				self.dates.append(self.dateClean(event))
				self.titles.append(event.h6.get_text().encode('ascii', 'ignore'))
				self.descs.append(event.h4.get_text().encode('ascii', 'ignore'))
				self.locations.append(self.SOURCE)
				self.links.append('https://www.sfmoma.org' + event.a['href'])
			except ValueError:
				pass

		# Print Status
		self.stdoutWrite(True)

		return None

	def dateClean(self, event):
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
		dateStr = event.find('h5','h5--light no-margin').get_text(separator=' ').replace(u'\u2013', '-')
		# Step 2: Remove days of week and words for times
		dateStr = self.multiple_replace(momaDict, dateStr)
		# Step 3: Clip Whitespace
		dateStr = dateStr[len(dateStr) - len(dateStr.lstrip()):]
		# Step 4: If hyphen present, split
		if goingson.re.search('-', dateStr):
			# Step 4a: Find am/pm associated before and after hyphen
			times = goingson.re.findall(r'[a/p]\.{0,1}[m]\.{0,1}', dateStr[:dateStr.index('-')]) + \
					goingson.re.findall(r'[a/p]\.{0,1}[m]\.{0,1}', dateStr[dateStr.index('-'):])
			# If both hours before and after hyphen have am/pm, use first - else use second
			if len(times) > 1:
				dateStr = dateStr[:dateStr.index('-')]
			else:
				dateStr = dateStr[:dateStr.index('-')] + ' ' + times[0]
			dateStr = goingson.datetime.strptime(goingson.re.sub(r'[\.,\s]', '', dateStr), '%B%d%Y%I%p')
		# Step 5: If no hyphen present, but hour with no minute present
		elif goingson.re.search(r'[a/p]\.{0,1}[m]\.{0,1}', dateStr) and not goingson.re.search(r'\:',dateStr):
			dateStr = goingson.datetime.strptime(goingson.re.sub(r'[\.,\s]', '', dateStr), '%B%d%Y%I%p')
		# Step 5: If no hyphen present, but hour with and minute present
		elif goingson.re.search(r'[a/p]\.{0,1}[m]\.{0,1}', dateStr):
			dateStr = goingson.datetime.strptime(goingson.re.sub(r'[\.,\s]', '', dateStr), '%B%d%Y%I:%M%p')
		# Step 6: If no hour present
		else:
			dateStr = goingson.datetime.strptime(goingson.re.sub(r'[\.,\s]', '', dateStr), '%B%d%Y')

		return dateStr

	def multiple_replace(self, dict, text):
		'''Loops through dictionary of substitutions for regex with text
		:param dict: (dict, str:str) dictionary used for substitutions
		:param text: (str) text for regex manipulation
		:return: (str) with regex substitute over each key from dictionary
		original source: stackoverflow dicussion - http://bit.ly/2jn2cQy
		'''

		# Create a regular expression  from the dictionary keys
		regex = goingson.re.compile('(%s)' % '|'.join(map(goingson.re.escape, dict.keys())))

		# For each match, look-up corresponding value in dictionary
		return regex.sub(lambda x: dict[x.string[x.start():x.end()]], text)

