from cgi import *
from trends import Trends

values = FieldStorage()
topics = values.getfirst("topics", "")

if topics:
	print "<h1>%s</h1>" % topics
