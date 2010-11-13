from xapian import *

TITLE = 0
MONTH = 1
YEAR = 2

class Indexer:
	def __init__(self, path):
		self.database = WritableDatabase(path, DB_CREATE_OR_OPEN)
		self.indexer = TermGenerator()
		self.indexer.set_stemmer(Stem("english"))
	
	def index(self, source):
		for (title, month, year) in source:
				doc = Document()
				doc.set_data(title)
				
				self.indexer.set_document(doc)
				self.indexer.index_text(title)

				doc.add_value(TITLE, title)
				doc.add_value(MONTH, month)
				doc.add_value(YEAR, year)

				self.database.add_document(doc)

class Searcher:
	def __init__(self, path):
		self.database = Database(path)
		self.enquire = Enquire(self.database)
		self.qp = QueryParser()
		self.qp.set_default_op(Query.OP_AND)
		self.qp.set_stemmer(Stem("english"))
		self.qp.set_stemming_strategy(QueryParser.STEM_SOME)

	def search(self, keywords):
		if isinstance(keywords, list):
			keywords = " ".join(keywords)
		
		query = self.qp.parse_query(keywords)
		self.enquire.set_query(query)
		
		return self.enquire.get_mset(0, self.database.get_doccount())

if __name__ == '__main__':
	import sys
	s = Searcher('pubmed.idx')
	s.search(sys.argv[1:])
