import os

from lxml import etree
from progressbar import ProgressBar

class PubMedArticleExtractor:
	def __init__(self, root_dir, ext='.nxml'):
		"""
		This method initializes the class.
		"""
		self.root_dir = root_dir
		self.ext = ext
		self.p_month = etree.XPath('//month')
		self.p_year = etree.XPath('//year')
		self.p_title = etree.XPath('//article-title')
		self.pbar = ProgressBar()
		self.size = None
		self.cb_progress = None
		self.cb_finished = None
	
	def __iter__(self):
		"""
		Simply points the caller to the generator of this class
		that does the bulk of the work.
		"""
		return self._extract()
	
	def __len__(self):
		"""
		Initially calling the len() function will be an expensive 
		operation.  The result is cached to make sure this only 
		happens once.
		"""
		if not self.size:
			self.size = 0
		
			for x in self._walk():
				self.size += 1
		
		return self.size
	
	def _walk(self):
		"""
		Finds all of the files with the matching extension (self.ext)
		and yields their full path for further processing.
		"""
		for (root, dirs, files) in os.walk(self.root_dir):
			for name in files:
				if os.path.splitext(name)[1] == self.ext:
					yield os.path.join(root, name)
	
	def _extract(self):
		"""
		This method does the heavy lifting of the class.  It's 
		responsible for parsing out all the details from every
		XML document found by _walk().
		
		It's marked private as the caller should use the class
		as an iterator instead of calling this method manually.
		"""
		i = 0
		
		for file in self._walk():
			i += 1
			f = open(file)
			tree = etree.parse(f)
			
			title = self.p_title(tree)[0].text
			month = self.p_month(tree)[0].text
			year = self.p_year(tree)[0].text
			
			f.close()
			
			# Report progress back to the caller if necessary.
			if i % 100 == 0:
				if self.cb_progress:
					self.cb_progress(i)
			
			yield (title, month, year)

		if self.cb_finished:
				self.cb_finished()
