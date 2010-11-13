from database import Searcher

from datetime import date, datetime
from monthdelta import monthmod

import sys

class Trends:
	def __init__(self, topics, path='pubmed.idx'):
		"""
		Initializes the class.  Topics must be either a string or list.  Path
		is optional.
		"""
		if isinstance(topics, str):
			self.topics = map(lambda x: x.strip(), topics.split(','))
		elif isinstance(topics, list):
			self.topics = topics
		else:
			raise Exception("Topics must be a string or list.")
		
		self.searcher = Searcher(path)
		self.offset = None
		self.num_months = None

	def histogram(self, num_bins=25):
		"""
		Generates a histogram based on the hits found and when they occurred.
		"""
		self.num_bins = num_bins
		dates = self._materialize_dates()
		self.offset = self._date_to_num_months(min(self._flatten(dates)))

		# Pre-populate the bins with zeroes.
		bins = [[0 for j in range(self.num_bins)] for i in range(len(self.topics))]
		i = 0
		
		# Fill the bins!
		for date_set in dates:
			for d in date_set:
				bins[i][self._date_to_bin_num(d)] += 1

			i += 1

		# Returns not only the bins, but also the maximum number of bins.  This
		# is only temporary for the Google Charting API.
		return (bins, max(self._flatten(bins)))

	def google_charts_api_url(self, hist):
		colours = ",".join(["%06x" % randint(0, 16777215) for x in range(len(topics))])
		data = "|".join(map(lambda x: ",".join(map(str, x)), hist[0]))
		url = "http://chart.apis.google.com/chart?chxr=0,0,%d&chxt=y&chbh=a&chs=600x400&cht=bvg&chco=%s&chds=0,%d&chdl=%s&chd=t:%s" % (hist[1], colours, hist[1], "|".join(topics), data)
		return url

	def _flatten(self, lol):
		"""
		Flattens a list of lists.  Only works on 2D lists.
		"""
		return [item for sublist in lol for item in sublist]

	def _materialize_dates(self):
		"""
		Creates a list of lists of dates.  The items in the first dimension
		correspond to the topics.  The second dimension corresponds to the
		dates returned by the search of that topic.
		"""
		i = 0
		all_dates = [[] for j in range(len(self.topics))]

		for topic in self.topics:
			dates = []

			for result in self.searcher.search(topic):
				dates.append(date(int(result.document.get_value(2)),
					int(result.document.get_value(1)), 1))

			all_dates[i] = dates
			i += 1

		return all_dates

	def _date_to_bin_num(self, d):
		"""
		Determines which bin to place the given date into.
		"""
		return (self._date_to_num_months(d) - self.offset) % self.num_bins

	def _date_to_num_months(self, d):
		"""
		Determines how many months since the beginning the given date is.
		"""
		return d.year * 12 + d.month

if __name__ == '__main__':
	from random import randint
	topics = sys.argv[1:]
	
	if not topics:
		raise Exception("Usage:  %s <topics>" % sys.argv[0])
	
	t = Trends(topics)
	hist = t.histogram()
	colours = ",".join(["%06x" % randint(0, 16777215) for x in range(len(topics))])
	data = "|".join(map(lambda x: ",".join(map(str, x)), hist[0]))
	url = "http://chart.apis.google.com/chart?chxr=0,0,%d&chxt=y&chbh=a&chs=600x400&cht=bvg&chco=%s&chds=0,%d&chdl=%s&chd=t:%s" % (hist[1], colours, hist[1], "|".join(topics), data)
	print(url)
