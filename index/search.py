import sys
import xapian as x

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--index", help="Path to index", default="uoit.idx")
(options, args) = parser.parse_args()

idx = x.Database(options.index)
enquire = x.Enquire(idx)
query_str = str.join(' ', args)

qp = x.QueryParser()
stemmer = x.Stem("none")
qp.set_stemmer(stemmer)
qp.set_database(idx)

query = qp.parse_query(query_str)

enquire.set_query(query)
matches = enquire.get_mset(0, 10)

print "%i results found." % matches.get_matches_estimated()
print "Results 1-%i:" % matches.size()

for m in matches:
	print "%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())

	for value in m.document.values():
		print value.value
