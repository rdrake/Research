import time
import xapian as x

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--index", help="Path to index", default="uoit.idx")
parser.add_option("-s", "--stemmer", help="Language stemmer to use", default="none")
(options, phrase) = parser.parse_args()

idx = x.Database(options.index)
enquire = x.Enquire(idx)
phrasing = []

qp = x.QueryParser()
stemmer = x.Stem(options.stemmer)
qp.set_stemmer(stemmer)
qp.set_database(idx)
qp.set_default_op(x.Query.OP_AND)

def does_exist(phrase):
	query = qp.parse_query(phrase)
	enquire.set_query(query)
	
	return enquire.get_mset(0, 10).empty() == False

i = 0
j = 1

start = time.time()

while j <= len(phrase):
	if does_exist(" ".join(phrase[i:j])):
		j += 1
	else:
		if (j - i) == 1:
			phrasing.append(phrase[i:j])
			j += 1
		else:
			phrasing.append(phrase[i:j-1])
		
		i = j - 1

phrasing.append(phrase[i:j])
elapsed = time.time() - start

print phrasing
print "Segmented %d words into %d phrases in %fs." % (len(phrase), len(phrasing), elapsed)
