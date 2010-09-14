from optparse import OptionParser

from sqlalchemy import *
from sqlalchemy.sql import select

import xapian as x

parser = OptionParser()
parser.add_option("--host", help="Hostname to connect to", default="localhost")
parser.add_option("-u", "--username", help="Username to connect as", default="root")
parser.add_option("-p", "--password", help="Password to connect with", default="hackme")
parser.add_option("-d", "--database", help="Database to use", default="uoit")
parser.add_option("-i", "--index", help="Path to index", default="uoit.idx")
(options, args) = parser.parse_args()

db = create_engine("mysql://%s:%s@%s/%s" % (options.username, options.password, options.host, options.database))
meta = MetaData(db)

idx = x.WritableDatabase(options.index, x.DB_CREATE_OR_OPEN)
indexer = x.TermGenerator()
stemmer = x.Stem("none")
indexer.set_stemmer(stemmer)

meta.reflect()

for table in meta.sorted_tables:
	s = select([table])
	result = s.execute()
	
	for row in result:
		for column in table.columns:
			doc = x.Document()
			value = str(row[column])
			doc.set_data(value)
			indexer.set_document(doc)
			indexer.index_text(value)
			
			doc.add_value(0, table.name)
			doc.add_value(1, column.name)
			doc.add_value(2, "value")
			
			idx.add_document(doc)
			#print "%s: %s" % (column.name, row[column])
